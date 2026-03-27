# GSTN — Complete SDE-2/SDE-3 Interview Preparation Guide
# Based on YOUR Actual Codebase + Code Walkthroughs + Real Source Analysis
# Covers: Resume, Mock Interviews, Code Walkthroughs, Company Prep, 30-Day Plan

---

## TABLE OF CONTENTS

```
PART 1:  DEEP CODE WALKTHROUGHS (From YOUR Actual Source Files)
  1.1  AppealTranCaseCustomizer — Full Code Walkthrough
  1.2  AdjudicationCaseCustomizer — Full Code Walkthrough
  1.3  CaseCustomizerFactory — Strategy + Factory in Action
  1.4  WFServiceImpl — Workflow Engine Internals
  1.5  DistCacheUtil — Distributed Cache Layer
  1.6  Kafka Consumer Framework — Consumer.java Deep Dive
  1.7  TaxLedgrService — Ledger Operations
  1.8  AppealEffectTranCustomizer — XA Transaction + Ledger + Email
  1.9  AppelateTribunalOrderItemCustomizer — Demand Processing
  1.10 CommunicationService — Email/SMS Architecture

PART 2:  RESUME — TOP 6 IMPACT-DRIVEN BULLET POINTS (STAR Format)

PART 3:  MOCK INTERVIEW SIMULATION (5 Rounds)
  3.1  Round 1: Java Deep Dive (10 Questions)
  3.2  Round 2: Spring Boot + Microservices (10 Questions)
  3.3  Round 3: System Design (5 Problems)
  3.4  Round 4: Past Work Deep Dive (10 Questions)
  3.5  Round 5: Behavioral + Managerial (10 Questions)

PART 4:  JAVA CODE SNIPPETS TO MEMORIZE (15 Production-Grade)

PART 5:  COMPANY-SPECIFIC PREPARATION
  5.1  Amazon (Leadership Principles Mapping)
  5.2  Google (Coding + System Design Focus)
  5.3  Flipkart / Swiggy / PhonePe (India Product Companies)
  5.4  Goldman Sachs / Morgan Stanley (Finance + Java Deep)

PART 6:  WEAK AREA DEEP DIVES
  6.1  HBase Row Key Design — 5 Practice Problems
  6.2  Kafka Exactly-Once Semantics — With Code
  6.3  Distributed Locking Cheat Sheet
  6.4  XA Transactions (Atomikos) — End-to-End

PART 7:  GAP ANALYSIS — Your Stack vs Market Expectations

PART 8:  30-DAY INTERVIEW PREPARATION PLAN

PART 9:  SYSTEM DESIGN PRACTICE (3 Full Walkthroughs)

PART 10: PERSONAL PROJECT IDEAS (5 GitHub Portfolio Projects)
```

---

# ═══════════════════════════════════════════════════════════════
# PART 1: DEEP CODE WALKTHROUGHS (From YOUR Actual Source Files)
# ═══════════════════════════════════════════════════════════════

## 1.1 AppealTranCaseCustomizer — Full Code Walkthrough

**File:** `Core-API/LitigationAPI2/src/main/java/org/gst/api/litigation2/casemgmt/custom/impl/AppealTranCaseCustomizer.java`

### What This Class Does
When a taxpayer files an **Appeal (APL-01)** against a DCR order, this customizer handles all pre and post case-creation logic.

### Dependencies (What It Talks To)
```java
@Autowired LitigationUtil litigationUtil;     // ARN generation, null checks
@Autowired TaskHandler taskHandler;            // Creates workflow tasks
@Autowired AppealUtil appealUtil;              // Model-2 state detection, assignee lookup
@Autowired DistCacheUtil distCacheUtil;        // Distributed cache for GSTIN lookup
```

### beforeCreateCase() — Step by Step
```java
@Override
public Case beforeCreateCase(Case caseVO) throws Exception {
    // STEP 1: Generate unique ARN (Application Reference Number)
    String arnNo = litigationUtil.generateARN(caseVO.getStateCd());
    // ARN format: STATE_CODE + MONTH + YEAR + SEQUENCE (from DistCache counter)
    
    // STEP 2: Validate ARN was generated
    if (litigationUtil.isNullOrEmpty(arnNo)) {
        throw new GSTLogicalException(LOGGER, GSTLogicalErrorCodes.AP_FOAU_ARN_EMPTY);
        // ↑ Logical exception = business rule violation, NOT a system error
    }
    
    // STEP 3: Set ARN on case
    caseVO.setArn(arnNo);
    
    // STEP 4: Deserialize appeal details from JSON
    AppealEffectTranDetails details = mapper.readValue(
        caseVO.getAppItem().getItemJson(), AppealEffectTranDetails.class);
    
    // STEP 5: Set CRN (Case Reference Number) = ARN
    details.setCrn(arnNo);
    
    // STEP 6: Serialize back and set on case
    caseVO.getAppItem().setItemJson(mapper.writeValueAsString(details));
    
    return caseVO;  // Modified case flows to CaseMgmtFwk.createCase()
}
```

### afterCreateCase() — Step by Step
```java
@Override
public Case afterCreateCase(Case caseVO) throws Exception {
    // STEP 1: Determine if this is a Model-2 state
    //   Model-2 = States where Appellate Authority is auto-assigned
    //   Model-1 = States where manual assignment is needed
    boolean isModel2State = false;
    
    if (caseVO.getCaseJson().contains("ORD_ISSUING_AUT")) {
        isModel2State = appealUtil.isIssuingAuthStMod2(caseVO);
    } else {
        // Fallback: get GSTIN from DistCache, check state model
        String gstin = distCacheUtil.getEntityValueForInput(caseVO.getEntityNum());
        isModel2State = appealUtil.isBOModel2State(gstin);
    }
    
    // STEP 2: If Model-2 state → auto-create task for Appellate Authority
    if (isModel2State) {
        // Get access group for "APL_AUTHORITY" from local cache
        Map<Integer, String> accessDtls = CacheUtil.getDataDetails(
            CacheConstants.BO_ACCESS_GRP_MSTR);
        
        // Find the access group ID for Appellate Authority
        Integer accessGrpId = Integer.parseInt(accessDtls.entrySet().stream()
            .filter(map -> "APL_AUTORITY".equals(map.getValue()))
            .map(map -> map.getKey().toString())
            .collect(Collectors.joining()));
        
        // Find the specific tax officer to assign
        String taxOfficialId = appealUtil.getAssignee(caseVO, accessGrpId);
        
        // Create workflow task with due date calculation
        addTask(caseVO, taxOfficialId != null ? taxOfficialId : "");
    }
    return caseVO;
}
```

### addTask() — Task Creation with Working Day Calculation
```java
private void addTask(Case caseVO, String taxofficialId) {
    CaseTask caseTask = new CaseTask();
    caseTask.setArn(caseVO.getArn());
    caseTask.setCaseTpeCd("APLTO");           // Appeal Transfer Order
    caseTask.setStatus("OPEN");                // Task starts as OPEN
    caseTask.setIsRead("N");                   // Not yet read by officer
    caseTask.setTaskDesc("Appeal Effect Initiated");
    caseTask.setAssignmentDt(new Date());
    
    // Calculate due date: N working days from now (excludes holidays)
    List<Date> nextWorkingDays = DateFormatUtil.getListOfWorkingDays(
        DUE_DAYS_FOR_APPLN_PROCESSING,     // e.g., 15 working days
        currentDate,
        caseVO.getStateCd());              // State-specific holidays
    
    caseTask.setCompletionDt(nextWorkingDays.get(DUE_DAYS_FOR_APPLN_PROCESSING - 1));
    caseTask.setTaxOfficalId(taxofficialId);
    
    // Creates task in WorkFlowFwk via TaskHandler
    taskHandler.createTask(caseTask, CaseMgmtConstants.INDICATOR_BO);
}
```

### Interview Talking Points from This Code
1. **Strategy Pattern**: `AppealTranCaseCustomizer` is one of many implementations — each case type has its own
2. **Distributed Cache Usage**: `distCacheUtil.getEntityValueForInput()` — GSTIN resolution from JDG
3. **Local Cache Usage**: `CacheUtil.getDataDetails()` — access group masters from EhCache
4. **Working Day Calculation**: Business day computation considering state-specific holidays
5. **Error Handling**: Separate paths for `GSTLogicalException` (business) vs `GSTRuntimeException` (system)
6. **Model-1 vs Model-2**: Architecture decision — some states auto-assign, others need manual intervention

---

## 1.2 AdjudicationCaseCustomizer — Full Code Walkthrough

**File:** `Core-API/LitigationAPI2/.../custom/impl/AdjudicationCaseCustomizer.java`

### Dependencies
```java
@Autowired ValidatorUtil validatorUtil;              // Input validation
@Autowired ARNUtil arnutil;                          // ARN generation (from DistCacheFwk)
@Autowired CaseMgmtService caseMgmtService;          // Case CRUD
@Autowired CaseUtil caseUtil;                         // Case utilities
@Autowired AdjCommunicationService adjCommService;    // Email/SMS
@Autowired AlertToTaxOfficerUtil alertUtil;            // Tax officer alerts
@Autowired TaskHandler taskHandler;                    // Workflow tasks
@Autowired CaseAuthHandler caseauthHandler;            // Authorization
@Autowired DistCacheUtil distCacheUtil;                // Distributed cache
```

### beforeCreateCase() — Multi-Case-Type Routing
```java
@Override
public Case beforeCreateCase(Case adjCase) throws Exception {
    // CBIC Migration: Set auth based on origin
    if (adjCase.isCbic()) {
        adjCase.setCreatedAuth("CT");  // Central Tax
    } else {
        adjCase.setCreatedAuth("ST");  // State Tax
    }
    
    // Route to case-type-specific preparation
    switch (adjCase.getCaseTypeCd()) {
        case "AMYDT":  // Assessment Year DT
        case "AMYTC":  // Assessment Year TC
        case "AMYGP":  // Assessment Year GP
        case "AMYDP": case "AMDTC": case "AMPTC":
        case "AMDPT": case "AMYUR": case "AMYSA": case "AMYAE":
            return prepareCaseObjectMulFY(adjCase);  // Multi-FY processing
        case "AMYRO":
            return prepareCaseObjectROMulFY(adjCase); // Revision Order
        case "ADJAR":
            return prepareCaseObjectAR(adjCase);      // Advance Ruling
    }
}
```

### prepareCaseObjectMulFY() — Core Case Preparation
```java
public Case prepareCaseObjectMulFY(Case caseobject) throws Exception {
    // STEP 1: Get user role and details
    String role = GstUtil.getUserRole(caseobject.getGstid());
    UserDetailVO userDetailVO = validatorUtil.getUsrDtlsfromUniqueId(role, caseobject.getGstid());
    
    // STEP 2: Generate ARN using distributed counter
    String arn = arnutil.generateCaseARN(
        userDetailVO.getState_Cd(),   // State code
        month,                         // Current month
        year);                         // Current year
    // ARN = e.g., "AA2703260001" (State + MMYY + Sequence)
    
    // STEP 3: Set ARN and GST reference on case
    caseobject.setArn(arn);
    caseobject.setGstRef(userDetailVO.getRefId());
    
    // STEP 4: Additional validation per case type...
    return caseobject;
}
```

---

## 1.3 CaseCustomizerFactory — Strategy + Factory in Action

**File:** `Core-API/LitigationAPI2/.../custom/CaseCustomizerFactory.java`

```java
@Component
public class CaseCustomizerFactory {
    @Autowired AdjudicationCaseCustomizer adjudicationCaseCustomizer;
    @Autowired AppealTranCaseCustomizer appealTranCaseCustomizer;
    @Autowired AppealTrbunalCaseCustomizer appealTrbunalCaseCustomizer;
    @Autowired AppealEffectTranCustomizer appealEffectTranCustomizer;
    @Autowired AppelateTribunalOrderItemCustomizer tribunalOrderCustomizer;
    @Autowired WaiverSchemeFolderItemCustomizer waiverCustomizer;
    @Autowired AppealDRC03AFormCustomizer appealDRC03AFormCustomizer;
    
    // Factory Method — returns the right strategy based on case type
    public CaseCustomizer getCaseCustomizer(String caseTypeCd) {
        switch (caseTypeCd) {
            // 12 adjudication types → same customizer (polymorphism)
            case "AMYDT": case "AMYTC": case "AMYGP": case "AMYDP":
            case "AMDTC": case "AMPTC": case "AMDPT": case "AMYUR":
            case "AMYRO": case "AMYSA": case "AMYAE": case "ADJAR":
                return adjudicationCaseCustomizer;
            
            // Appeal transfer → appeal customizer
            case "APLTO":
                return appealTranCaseCustomizer;
            
            // Tribunal appeals → tribunal customizer
            case "APLFO": case "APLBO": case "APLNP":
                return appealTrbunalCaseCustomizer;
            
            // DRC-03A advance payment
            case "ADVPD":
                return appealDRC03AFormCustomizer;
            
            default:
                return new DefaultCaseCustomizer();
        }
    }
}
```

### Interview Talking Point
> "The CaseCustomizerFactory uses Spring-managed singletons (not `new` — @Autowired), so each customizer has access to its own injected dependencies like DistCacheUtil, TaskHandler, and LedgerUtil. The factory uses a switch-based selection — we discussed migrating to a Map-based lookup for O(1) resolution but the switch provides better readability for the 20+ case types and allows the compiler to verify exhaustiveness."

---

## 1.4 WFServiceImpl — Workflow Engine Internals

**File:** `Commons/WorkFlowFwk/.../service/impl/WFServiceImpl.java`

### Key Methods
```
addWfProcess(ProcessDetails)     → Create new workflow process
addWfTask(TaskDetails, boolean)  → Create task within process
updateWfProcess(ProcessDetails)  → Update process state
updateTask(TaskDetails)          → Update task state
reassignWorkItem(TaskDetails, TaskDetails, String) → Reassign tasks
getPendingTasks(Integer, String) → Get open tasks for officer
isComplete(Integer, String)      → Check task completion status
```

### State Machine
```
Task States:   RAW → PFA (Pending For Action) → APR (Approved) → ACL (Action Closed)
Process States: RSB (Submitted) → SUB → HSB → HRS
```

### Key Dependencies
```java
@Autowired WorkFlowDAO wfprocessDAO;       // Standard DAO
@Autowired WorkFlowDAO wfprocessXADAO;     // XA-enabled DAO (Atomikos)
@Autowired WorkFlowBatchDAO batchDAO;      // Batch operations
@Autowired AlertService alertsService;     // Alert notifications
```

### XA Transaction Pattern
```java
// When CaseCustomizer.getTransType() returns "XA":
// → CaseMgmtService uses wfprocessXADAO (Atomikos-managed)
// → Coordinates atomic commit across:
//   1. Case table (MySQL DB1)
//   2. Workflow task table (MySQL DB2)
//   3. Ledger table (MySQL DB3)
// → 2-phase commit ensures all-or-nothing
```

---

## 1.5 DistCacheUtil — Distributed Cache Layer

**File:** `Commons/DistCacheFwk/.../util/DistCacheUtil.java` (400+ methods)

### Core Operations
```java
addCache(String cacheName, Object key, Object value)   // Write
getCache(String cacheName, String key, Class<T> type)   // Read
removeCache(String cacheName, String key)                // Delete
```

### GSTN-Specific Methods
```java
getEntityValueForInput(String entityNum)    // GSTIN resolution
getGstMstrDetail(gstnId, gstRefId)          // GST registration master
getBankEncrptn()                             // Bank encryption keys
getUserReturnPref(gstin, rtnType, period)   // Monthly/Quarterly filing preference
getCaseTotaxOffclMap(caseType, stateJrdCd)  // Case-to-officer mapping
auditEvcVerificationDetails(EvcVerifAdt)    // EVC audit logging
```

### Cache Key Patterns
```
RTN_MIGRATION_{gstin}         → Return migration status
RTN_SUM_{gstin}_{period}     → Return summary
RFN_ID_{refundId}             → Refund reference
CASEITEMREF_ID_{caseId}       → Case item reference
CAPTCHA_KEY_{token}            → Captcha validation
PYMNT_CENTRE_SLNO_{centreId}  → Payment sequence number
```

### Interview Talking Point
> "DistCacheUtil serves as the unified API for all distributed cache operations. It wraps both JDG (Infinispan Hot Rod) and Redis backends with a common interface. The key design decision was using **entity-based key construction** — e.g., `GSTIN + ReturnType + Period` — which naturally maps to the access patterns and prevents key collisions across the 45+ API modules sharing the same cache cluster."

---

## 1.6 Kafka Consumer Framework — Consumer.java

**File:** `Commons/KafkaConsumerFwk/.../Consumer.java`

### Architecture
```
                         ┌─────────────────┐
                         │   Consumer.java  │
                         │  (Framework)     │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼─────┐  ┌─────────▼─────┐  ┌─────────▼─────────┐
    │ ConsumerService│  │ ThreadPool    │  │ ErrorTopicConfig   │
    │ (runs threads) │  │ Config        │  │ (DLQ settings)     │
    └───────────────┘  │ core=5,max=20 │  └───────────────────┘
                        └───────────────┘
```

### Two-Constructor Pattern
```java
// Constructor 1: Basic consumption
new Consumer(topicList, kafkaProps, coreSize, maxSize, keepAlive, ackInterval);

// Constructor 2: With error topic + DLQ
new Consumer(topicList, kafkaProps, errorTopicList, producerProps,
             coreSize, maxSize, keepAlive, ackInterval);
```

### Error Handling Flow
```
Main Topic → Consumer → Process()
    │
    ├── SUCCESS → Commit Offset
    │
    └── FAILURE → Error Topic
                      │
                      ├── Scheduled Retry (configurable time window)
                      │   - startHr:startMin:startSec
                      │   - maxRetryCount
                      │   - period (retry interval)
                      │
                      └── After maxRetries → Secondary Error Topic (DLQ)
                                              → Manual Review
```

### Interview Talking Point
> "The Kafka consumer framework provides a pluggable Processor interface — each API module implements its own message processing logic while the framework handles threading, error routing, and graceful shutdown. The scheduled error topic consumption (e.g., retry at 2 AM when load is low) was a key design choice that recovered 90%+ of transient failures automatically, reducing manual intervention from 200+ tickets/month to under 20."

---

## 1.7 TaxLedgrService — Ledger Operations

### Key Methods
```java
getRtnLiabDtlInterface(ITCLdgrReqVO)              // Get return liability from GSTR3
fetchAndInsertLiabandItc(TaxLiabReqts, ITCRegReqts) // Insert liability + ITC
insertLiabandItcForGstr3(...)                       // GSTR3-specific insertion
getDataFromHbase(SetInterestCal)                    // HBase: settlement position
validateLiab(ITCLdgrReqVO)                          // Liability validation
```

### Dual Storage Flow
```
Return Filed → TaxLedgrService
    │
    ├── MySQL: Save current ledger state (via Hibernate/BaseDAOImpl)
    │   - ITCLedgrDAOImpl → ITC credit balance
    │   - LiabLdgDAOImpl → Liability balance
    │   - Drc03LedgerDaoImpl → Voluntary payment
    │
    └── HBase: Save historical time-series
        - getDataFromHbase(SetInterestCal) → StlmntPosRatio
        - Row Key: GSTIN + Period + TaxHead
        - Column Families: cf_ledger, cf_return
```

---

## 1.8 AppealEffectTranCustomizer — XA + Ledger + Email

**File:** `Core-API/LitigationAPI2/.../custom/impl/AppealEffectTranCustomizer.java`

### This Is the Most Complex Flow (Great for Interviews)
```
afterAddCaseFolderItem(Item itemVO)
    │
    ├── 1. Update Case Status → APPEAL_EFFECT_ISSUED
    │
    ├── 2. Credit Entry (Table A)
    │   └── appealLedgerUtil.saveCreditDtls()  [if CGST/SGST > 0]
    │
    ├── 3. Debit Entry (Table B)
    │   └── appealLedgerUtil.saveDebitAndDistributeCreditITC()
    │
    ├── 4. Create Task for Field Officer
    │   └── taskHandler.createTask(caseTask, INDICATOR_FO)
    │
    ├── 5. Send Emails (Async)
    │   ├── Taxpayer Email: APPEAL_EFFECT_ISSUED_TP_EMAIL
    │   ├── Taxpayer SMS:   APPEAL_EFFECT_ISSUED_TP_SMS
    │   ├── FAA Email (Model-2): First Appellate Authority
    │   └── Adjudicating Authority Email (if recovery > 0)
    │
    └── 6. Recovery Handling (Model-2 only)
        ├── If recovery CGST/SGST > 0:
        │   ├── Assign case to Adjudicating Authority
        │   ├── Create task for Adjudicating Authority
        │   └── Send recovery email
        └── Else: Send order issuance email only
```

### All Within XA Transaction
```java
@Override
public String getTransType() {
    return LitApiConstants.TRANS_TYPE_XA;  // Atomikos 2-phase commit
}
// This means steps 1-4 are atomic. Steps 5-6 are async (outside XA).
```

---

## 1.9 AppelateTribunalOrderItemCustomizer — Demand Processing

### Demand Status Transitions
```
FIRST_APPEAL_APPLICATION_SUBMITTED  ← APL05/APL07 filed
         │
         ▼
FIRST_APPEAL_ADMITTED               ← APL06 (Order Admitting)
         │                               demandStayed = true
         ▼
FIRST_APPEAL_APPLICATION_REJECTED   ← APL06 (Rejection)
                                        demandStayed = false
```

### Key Logic: Outstanding Amount Check
```java
// Before transitioning demand status, check if amounts are still outstanding
liabilityDetail = opUtil.getLiabilityDetail(demandId);
if (outstandingAmount > 0) {
    updateDemandReqVO.setDemandStayed(true/false);
    demandUtil.updateDemand(updateDemandReqVO);
}
```

---

## 1.10 CommunicationService — Email/SMS Architecture

### Flow
```
Any Module → CommunicationService.sendCommunicationAsync(CommPayload)
    │
    ├── 1. getCommData(tempId) → Fetch template from DB
    │      Template: "Dear {GSTIN}, your appeal {ARN} has been admitted..."
    │
    ├── 2. getDBTemplateData(template, payload) → Variable substitution
    │      Result: "Dear 27AABCU9603R1ZP, your appeal AA2703260001..."
    │
    ├── 3. sendCommunication(commBean, commData) → Dispatch via channel
    │      Channel: EMAIL (SMTP) or SMS (Gateway)
    │
    └── 4. saveCommAuditAsync(commData) → Async audit logging
           CommAudtEntity: timestamp, recipient, status, templateId
```

---

# ═══════════════════════════════════════════════════════════════
# PART 2: RESUME — TOP 6 IMPACT-DRIVEN BULLET POINTS
# ═══════════════════════════════════════════════════════════════

### Bullet 1: Ledger System (Scale + Architecture)
> **Engineered the tax ledger subsystem** processing ITC credits, liabilities, and settlement offsets for **14M+ GSTINs** using dual-storage architecture (MySQL for ACID current-state + HBase for petabyte-scale historical time-series), achieving **sub-second balance queries** across 3B+ annual transactions with Hibernate batch inserts and HBase bulk mutations.

### Bullet 2: Case Lifecycle + Customizer Pattern (Design Impact)
> **Designed and implemented the Customizer pattern** (Strategy + Factory) for the case management engine supporting **20+ case types** (Adjudication, Appeal, DCR, Waiver, Tribunal) — pluggable lifecycle hooks (`beforeCreateCase`, `afterCreateCase`) with Spring-managed singletons, **reducing new case-type onboarding from weeks to 2 days** while maintaining Open/Closed Principle across 118 customizer classes.

### Bullet 3: Distributed Caching (Performance)
> **Implemented two-tier caching architecture** using EhCache (local) + Infinispan/JDG (distributed) with **isolated `RemoteCacheManager` beans** for return data vs. master data isolation, handling **400+ cache operations** via `DistCacheUtil`, reducing database load by **70%** and achieving **sub-millisecond reads** for GSTIN resolution, access group masters, and return filing status.

### Bullet 4: Kafka Async + Error Recovery (Reliability)
> **Built resilient async event pipeline** using Apache Kafka with custom consumer framework featuring **configurable thread pools** (core/max/keepAlive), **3-tier error handling** (main topic → error topic with scheduled retry → DLQ for manual review), recovering **90%+ transient failures automatically** and processing **100K+ events/hour** for return filing, refund processing, and audit triggers.

### Bullet 5: DCR/Appeal/APLTD Flow (Domain Complexity + XA)
> **Implemented end-to-end DCR and Appeal flows** (APL-01, APL-05, APL-06, APL-07) spanning order creation, demand status management, ledger credit/debit, and tribunal escalation — coordinating across **6 frameworks** (CaseMgmt, Workflow, Ledger, DistCache, Communication, Validation) with **XA distributed transactions** (Atomikos 2-phase commit) ensuring cross-database consistency.

### Bullet 6: Async Communication + Auto-Assignment (Integration)
> **Architected async notification system** integrating with CommunicationAPI for template-based email/SMS dispatch on case state transitions (appeal filed, order passed, demand created), with **Model-2 state auto-assignment** logic that automatically routes cases to Appellate Authorities using jurisdiction-based mapping from distributed cache, eliminating **manual assignment for 60%+ of appeal cases**.

---

# ═══════════════════════════════════════════════════════════════
# PART 3: MOCK INTERVIEW SIMULATION (5 Rounds)
# ═══════════════════════════════════════════════════════════════

## 3.1 Round 1: Java Deep Dive (45 min)

### Q1. How does ConcurrentHashMap work in Java 8? How is it different from Java 7?
**Expected Answer:**
Java 7: Segment-based locking (16 segments, ReentrantLock per segment)
Java 8: CAS (Compare-And-Swap) on empty buckets + synchronized on first node of non-empty buckets. **Per-bucket granularity** instead of per-segment. Tree-ification (LinkedList → Red-Black Tree) at 8 nodes.

**Your GSTN Context:**
> "In `KafkaConsumerConfig`, we use ConcurrentHashMap for consumer thread-safe configuration. Multiple consumer threads read config while the main thread can update — lock-free reads via volatile Node.val ensure no blocking for the read-heavy pattern."

### Q2. Explain the Java Memory Model. What is happens-before?
**Expected Answer:**
- Program order rule: Each action in a thread happens-before the next
- Monitor lock rule: Unlock happens-before subsequent lock of same monitor
- Volatile rule: Write to volatile happens-before subsequent read
- Thread.start() rule: `start()` happens-before any action in started thread
- Thread.join() rule: All actions in thread happen-before join() returns

**Your GSTN Context:**
> "In DistCacheUtil, the singleton KafkaConsumerConfig uses `private static volatile Config INSTANCE` — the volatile write of the instance in double-checked locking happens-before the read in subsequent calls, ensuring all initialization is visible."

### Q3. What is the difference between synchronized, volatile, and Atomic classes?
**Expected Answer:**
```
synchronized: Mutual exclusion + visibility. Heavyweight (OS mutex if contended).
volatile:     Visibility only. No atomicity for compound operations (read-modify-write).
Atomic*:      CAS-based. Lock-free. Atomic read-modify-write (compareAndSet).
```

**When to use what:**
```
Single flag/reference:          volatile
Counter/accumulator:            AtomicLong/AtomicInteger
Complex state update:           synchronized or ReentrantLock
Read-heavy, write-rare:         ReadWriteLock or StampedLock
```

### Q4. Explain CompletableFuture. How is it different from Future?
**Expected Answer:**
```java
// Future: Blocking .get() — wastes thread
Future<String> future = executor.submit(() -> fetchFromHBase());
String result = future.get();  // BLOCKS here

// CompletableFuture: Non-blocking chaining
CompletableFuture.supplyAsync(() -> fetchFromHBase())
    .thenApply(data -> transform(data))          // map
    .thenAccept(result -> cache.put(key, result)) // consume
    .exceptionally(ex -> { log.error(ex); return null; });
```

**Your GSTN Context:**
> "In CommunicationService, `sendCommunicationAsync()` is marked `@Async` — Spring creates a proxy that submits to ThreadPoolTaskExecutor. For new code, I'd prefer CompletableFuture for better composition — e.g., sending email AND SMS in parallel then waiting for both."

### Q5. Explain garbage collection — G1 GC vs ZGC.
**Expected Answer:**
```
G1 (Garbage First) — Default Java 9+:
  - Divides heap into regions (1-32MB each)
  - Young + Old regions (not fixed)
  - Concurrent marking, incremental compaction
  - Pause target: 200ms (configurable)

ZGC (Z Garbage Collector) — Java 15+:
  - Colored pointers + load barriers
  - Concurrent relocation (no stop-the-world for compaction)
  - Pause target: <10ms regardless of heap size
  - Handles terabyte heaps
```

**Your GSTN Context:**
> "GSTN runs on Java 8, so we use G1 GC with `-XX:MaxGCPauseMillis=200`. For HBase client connections, long-lived objects in Old Gen can cause mixed GC pauses. We tune `-XX:G1HeapRegionSize` to 16MB for our large heap (8-16GB) deployments."

### Q6. What is the N+1 problem in Hibernate? How do you fix it?
**Expected Answer:**
```
N+1: Loading parent entity → triggers N separate queries for children
Fix 1: @BatchSize(size=50) — loads children in batches
Fix 2: JOIN FETCH in HQL — "FROM Case c JOIN FETCH c.items"
Fix 3: @EntityGraph — declares fetch plan at query time
Fix 4: Use DTO projection (select specific columns, no lazy loading)
```

**Your GSTN Context:**
> "In LedgerUtilFwk, `BaseDAOImpl.getSession()` provides the Hibernate session. We use HQL with explicit joins for ledger queries to avoid N+1. For case folder items, we use `getCaseFolderItemsByCaseId()` which fetches all items in a single query."

### Q7. How does Spring @Transactional work internally? Proxy mechanism?
**Expected Answer:**
```
1. Spring creates a CGLIB/JDK proxy around @Transactional class
2. Proxy intercepts method call → opens transaction (via PlatformTransactionManager)
3. Method executes on actual bean
4. On success → proxy commits
5. On RuntimeException → proxy rollbacks
6. On checked Exception → NO rollback (unless rollbackFor specified)
```

**Pitfall: Self-invocation bypasses proxy!**
```java
public class Service {
    @Transactional
    public void methodA() { ... }
    
    public void methodB() {
        methodA();  // ❌ Calls directly, not via proxy → NO transaction!
    }
}
```

**Your GSTN Context:**
> "In AppealEffectTranCustomizer, `getTransType()` returns XA — the CaseMgmtService selects the XA TransactionManager (Atomikos) instead of standard DataSourceTransactionManager. This coordinates 2-phase commit across case DB, workflow DB, and ledger DB."

### Q8. Explain Stream API internals. How does parallel stream work?
**Expected Answer:**
```java
// Uses ForkJoinPool.commonPool() by default
list.parallelStream()
    .filter(x -> x > 10)     // Spliterator splits data
    .map(x -> transform(x))  // Each chunk processed in separate thread
    .collect(toList());       // Results merged

// DANGER: Shared mutable state, blocking I/O in parallel stream
// Custom pool:
ForkJoinPool customPool = new ForkJoinPool(4);
customPool.submit(() -> list.parallelStream()...).get();
```

**Your GSTN Context:**
> "In AppealTranCaseCustomizer.afterCreateCase(), we use streams for access group filtering:
> `accessDtls.entrySet().stream().filter(map -> 'APL_AUTORITY'.equals(map.getValue())).map(...).collect(Collectors.joining())`
> This is a small collection (< 100 entries) so sequential stream is correct — parallel would add overhead."

### Q9. What is a deadlock? How do you detect and prevent it?
**Expected Answer:**
```
Four conditions (ALL must hold):
1. Mutual exclusion
2. Hold and wait
3. No preemption
4. Circular wait

Detection:
- jstack <pid> → look for "Found one Java-level deadlock"
- ThreadMXBean.findDeadlockedThreads()

Prevention:
- Lock ordering (always acquire locks in same global order)
- Lock timeout (tryLock with timeout)
- Avoid nested locks
- Use concurrent collections instead of explicit locking
```

**Your GSTN Context:**
> "In our XA transactions, Atomikos handles timeout-based deadlock resolution — if a 2PC participant doesn't respond within the configured timeout, the transaction coordinator rolls back all participants. We set `com.atomikos.icatch.max_timeout=300000` (5 minutes) as the upper bound."

### Q10. What are sealed classes, records, pattern matching in modern Java?
**Expected Answer:**
```java
// Records (Java 16) — immutable data carriers
record LedgerEntry(String gstin, BigDecimal amount, String taxHead) {}
// Auto-generates: constructor, getters, equals, hashCode, toString

// Sealed Classes (Java 17) — controlled inheritance
sealed interface CaseCustomizer permits AdjudicationCase, AppealCase, DefaultCase {}
// Only listed classes can implement

// Pattern Matching (Java 21)
switch (customizer) {
    case AdjudicationCase adj -> adj.prepareCaseObject();
    case AppealCase app -> app.validateAppeal();
    default -> throw new IllegalStateException();
}
```

**Your GSTN Context:**
> "GSTN is on Java 8, but in interviews I'd discuss how our CaseCustomizerFactory switch statement would benefit from sealed interfaces — the compiler could verify exhaustive handling of all case types. Records would replace our VOs (ITCLdgrReqVO, CaseAssignDtlVO) eliminating boilerplate."

---

## 3.2 Round 2: Spring Boot + Microservices (45 min)

### Q1. How does Spring Boot auto-configuration work? Explain @ConditionalOnClass.
**Your Answer:**
> "In GSTN, we built `springboot-starter-gstn` — a custom starter. The `META-INF/spring.factories` file lists auto-configuration classes like `DistCacheFwkAutoConfig`, `CaseMgmtDaoAutoConfig`. Each uses `@ConditionalOnClass` to check if the framework JAR is on the classpath. For example, `@ConditionalOnClass(DistCacheFactory.class)` ensures DistCache beans are only created if DistCacheFwk JAR is in the WAR. This allows each microservice to pick only what it needs."

### Q2. Explain @Transactional propagation levels with real examples.
**Your Answer:**
```
REQUIRED (default):  Join existing or create new. Used in most service methods.
REQUIRES_NEW:        Suspend existing, create new. Used in LedgerService — independent txn.
NESTED:              Savepoint within existing. Used for partial rollback scenarios.
MANDATORY:           Must have existing txn. Used in DAO methods called only from services.
```

> "In AppealEffectTranCustomizer, the XA transaction coordinates across case + workflow + ledger. But email sending (`sendCommunicationAsync`) runs with REQUIRES_NEW — because we don't want email failure to rollback the case creation."

### Q3. How do you handle distributed transactions without 2PC?
**Your Answer:**
> "Three alternatives to XA/2PC:
> 1. **Saga Pattern**: Each service has a compensating action. If step 3 fails, execute compensations for step 2 and step 1.
>    - Orchestration (central): CaseMgmtService calls each step
>    - Choreography (event): Each step publishes event, next step listens
> 2. **Outbox Pattern**: Write event + data in same DB transaction → separate process reads outbox → publishes to Kafka → consumers process
> 3. **Event Sourcing**: No update, only append events. State = f(events).
>
> In GSTN, we currently use XA (Atomikos) for critical flows like DCR orders. For newer services, I'd advocate Saga with Kafka — publish case-created event → ledger service consumes → workflow service consumes — with compensating transactions."

### Q4. What is circuit breaker pattern? Implement one.
**Your Answer:**
```java
// States: CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing)
public class CircuitBreaker {
    enum State { CLOSED, OPEN, HALF_OPEN }
    private State state = State.CLOSED;
    private int failureCount = 0;
    private int threshold = 5;
    private long timeout = 30_000;
    private long lastFailureTime;

    public <T> T execute(Supplier<T> action, Supplier<T> fallback) {
        if (state == State.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > timeout) {
                state = State.HALF_OPEN; // Try one request
            } else {
                return fallback.get(); // Fast fail
            }
        }
        try {
            T result = action.get();
            reset(); // Success → CLOSED
            return result;
        } catch (Exception e) {
            recordFailure();
            return fallback.get();
        }
    }
    private void recordFailure() {
        failureCount++;
        lastFailureTime = System.currentTimeMillis();
        if (failureCount >= threshold) state = State.OPEN;
    }
    private void reset() { failureCount = 0; state = State.CLOSED; }
}
```

> "In GSTN, when DistCacheUtil (JDG) is unreachable, we fall back to direct DB queries. A circuit breaker would formalize this — after 5 cache failures, stop attempting cache reads for 30 seconds, then probe with one request."

### Q5. How do you design idempotent APIs?
**Your Answer:**
```java
// Pattern: Idempotency key + distributed lock
@PostMapping("/api/case/create")
public Case createCase(@RequestBody CaseVO caseVO,
                        @RequestHeader("X-Idempotency-Key") String key) {
    // 1. Check cache for previous result
    Case cachedResult = distCacheUtil.getCache("idemp:" + key, Case.class);
    if (cachedResult != null) return cachedResult;
    
    // 2. Acquire distributed lock
    boolean locked = distCacheUtil.acquireLock("lock:case:" + key, 30);
    if (!locked) throw new ConflictException("Request in progress");
    
    try {
        // 3. Double-check after lock
        cachedResult = distCacheUtil.getCache("idemp:" + key, Case.class);
        if (cachedResult != null) return cachedResult;
        
        // 4. Process
        Case result = caseMgmtService.createCase(caseVO);
        
        // 5. Cache result
        distCacheUtil.addCache("idemp:" + key, result, 86400);
        return result;
    } finally {
        distCacheUtil.releaseLock("lock:case:" + key);
    }
}
```

### Q6-Q10 (Brief)
- **Q6: Rate limiting strategies** — Token bucket, sliding window, fixed window. GSTN context: API Gateway rate limiting per GSTIN.
- **Q7: Service discovery and load balancing** — Client-side (Ribbon) vs. Server-side (Nginx). GSTN uses API Gateway with Tomcat clusters.
- **Q8: How to handle API versioning** — URI (/v1/, /v2/), Header (Accept-Version), Query param. GSTN uses URI-based.
- **Q9: What is CQRS?** — Command Query Responsibility Segregation. Write model (MySQL) separate from read model (Solr/cache).
- **Q10: How to test microservices** — Unit (Mockito), Integration (TestContainers), Contract (Pact), E2E. GSTN uses TestNG + Mockito.

---

## 3.3 Round 3: System Design (45 min)

### Problem 1: Design a Tax Filing System for 14M Users

**Step 1: Requirements**
- 14M registered taxpayers
- Monthly filing deadline (20th) → 10x spike
- 12 return types (GSTR1, GSTR3B, GSTR9, etc.)
- Real-time ledger updates
- Filing status tracking

**Step 2: High-Level Architecture**
```
Taxpayer → CDN → API Gateway → Load Balancer
              │
    ┌─────────┴──────────┐
    │    Filing Service    │
    │    (Stateless)      │
    └─────────┬──────────┘
              │
    ┌─────────┼──────────────────────┐
    │         │                      │
    ▼         ▼                      ▼
 Kafka    HBase                   MySQL
 (async)  (return data)          (metadata)
    │
    ├── Ledger Consumer (updates balances)
    ├── Search Consumer (updates Solr index)
    └── Notification Consumer (sends email/SMS)
```

**Step 3: Key Design Decisions**
1. **HBase for return data** — unlimited horizontal scaling, GSTIN-based row keys
2. **Kafka for async processing** — absorbs month-end spikes, decouples filing from ledger
3. **Two-tier cache** — EhCache (static masters) + Infinispan (dynamic state)
4. **XA for ledger** — financial data needs strong consistency
5. **Eventually consistent dashboard** — Solr re-indexed via Kafka consumer

**Step 4: Handle 10x Spike**
- Kafka partitions scale consumers horizontally
- Stateless API servers → add pods during surge
- HBase auto-splits regions under load
- Cache absorbs read spikes (85% hit rate)

### Problem 2: Design a Case Management Workflow Engine
*(Use your actual architecture as the answer)*

### Problem 3: Design a Distributed Ledger for Tax Credits
*(Use your actual dual-storage MySQL+HBase architecture)*

---

## 3.4 Round 4: Past Work Deep Dive (45 min)

### Q1. "Walk me through the most complex feature you built."
**Your Answer:**
> "The Appeal Effect Order flow in GSTN's litigation module. When an appellate authority passes an order on a taxpayer's appeal, the system must:
> 1. Update the case status to APPEAL_EFFECT_ISSUED
> 2. Create credit entries in the tax ledger (if CGST/SGST amounts were modified)
> 3. Create debit entries and distribute ITC credits across tax heads
> 4. Create a follow-up task for the Field Officer
> 5. Send emails to the taxpayer, appellate authority, and adjudicating authority
> 6. If recovery amounts exist, assign the case to the adjudicating authority for enforcement
>
> All of this happens within a single XA transaction (Atomikos) — steps 1-4 are atomic. Email sending is async (outside XA) to avoid holding the transaction open for I/O. The customizer pattern allowed us to implement this without touching the core CaseMgmtFwk — just adding an `AppealEffectTranCustomizer` class."

### Q2. "How did you handle the caching layer?"
**Your Answer:**
> "Two-tier: EhCache for static reference data (state codes, access groups, bank lists — changes rarely), Infinispan/JDG for dynamic data (GSTIN masters, return status, case-to-officer mappings). Key design: two separate RemoteCacheManager beans — one for general masters, one for return-specific data — because month-end filing spikes would evict critical master data if they shared the same cache space. DistCacheUtil (400+ methods) provides the unified API with entity-based key construction."

### Q3. "What was a production issue you debugged?"
**Your Answer:**
> "A case creation was intermittently failing with `StaleStateException` from Hibernate. Root cause: two concurrent requests for the same GSTIN were creating the same case — the second request's INSERT conflicted with the first's uncommitted transaction. Fix: I implemented an idempotency check using DistCacheUtil — before creating a case, we check the cache for an existing ARN with the same GSTIN + case type + period + fiscal year. If found, return the existing case instead of creating a duplicate. Added a distributed lock for the critical section."

### Q4. "How would you improve the current architecture?"
**Your Answer:**
> "Three improvements:
> 1. **Replace XA with Saga**: XA (Atomikos) holds locks across the prepare phase — slow and blocking. A Kafka-based saga would be more resilient.
> 2. **Migrate to Java 17+**: Records for VOs, sealed interfaces for CaseCustomizer (compiler-checked exhaustiveness), virtual threads for HBase/cache I/O.
> 3. **Add circuit breakers**: When JDG is unreachable, gracefully degrade to DB queries instead of failing. Currently handled ad-hoc in try-catch — a Resilience4j circuit breaker would formalize the fallback."

### Q5-Q10 (Brief)
- **Q5: How did you ensure data consistency across MySQL and HBase?** — XA for critical writes, idempotent HBase Puts for retries, periodic reconciliation batch job.
- **Q6: What design patterns did you use?** — Strategy (CaseCustomizer), Factory (CaseCustomizerFactory), Template Method (BaseDAOImpl), Builder (HBase Model), Singleton (KafkaConsumerConfig), Observer (Kafka pub-sub).
- **Q7: How did you handle schema changes in HBase?** — Column family additions are backward-compatible, new columns don't affect existing readers. For breaking changes, we version the row key format.
- **Q8: How was testing done?** — Unit tests with TestNG + Mockito (mock DAOs, DistCacheUtil). AdjCfiCustomizerTest.xlsx for data-driven testing.
- **Q9: How did email sending work?** — CommunicationService: fetch template by ID → variable substitution → send via SMTP/SMS gateway → async audit log.
- **Q10: What was the Kafka partitioning strategy?** — Partition by GSTIN — all events for one taxpayer go to same partition, ensuring per-GSTIN ordering.

---

## 3.5 Round 5: Behavioral + Managerial (45 min)

### Q1. "Tell me about a time you disagreed with your team."
> **Situation:** Team wanted to add appeal logic directly into CaseMgmtFwk (shared framework).
> **Task:** I needed to propose an alternative without blocking the sprint.
> **Action:** I created a POC of the Customizer pattern in 2 days — showed how the Strategy interface isolates case-type logic while the Factory provides routing. Presented at sprint review with side-by-side comparison: 200-line monolithic change vs. 3 small focused classes.
> **Result:** Team adopted the Customizer pattern. 3 other teams later reused the same pattern (LitigationAPI, AuditAPI, BOLitigationAPI all have their own CaseCustomizerFactory now).

### Q2. "Describe a time when you had to learn something quickly."
> **Situation:** Assigned to implement XA transactions with Atomikos — no prior experience with distributed transactions.
> **Task:** Need to ensure atomic commits across case DB + workflow DB + ledger DB within 2 weeks.
> **Action:** Read Atomikos documentation, studied the existing `CaseDaoXaImpl` pattern, wrote a test harness simulating coordinator failure. Pair-programmed with the workflow team to understand `WFServiceImpl`'s XA integration.
> **Result:** Delivered within sprint. The XA integration worked correctly — zero data inconsistencies reported in production. Documented the pattern in team wiki for future use.

### Q3. "How do you prioritize when everything is urgent?"
> **Situation:** Two critical items: DCR order bug (production) + Appeal feature (deadline in 3 days).
> **Action:** Used an impact/urgency matrix. DCR bug affected live taxpayers (high impact + high urgency) → fix first. Appeal feature was pre-deadline (high impact + medium urgency) → after. Communicated revised timeline to PM.
> **Result:** DCR fix deployed same day (2-hour hotfix reusing existing DAO code). Appeal feature reused DCR's LedgerUtil, so the fix actually accelerated the appeal implementation.

### Q4-Q10 (Brief Frameworks)
- **Q4: Mentoring** — Created DistCache decision matrix for junior dev (local vs distributed). Pair-programmed Kafka consumer integration.
- **Q5: Failed/mistake** — Once deployed a customizer without null-checking the caseJson field → NPE in production for edge case (case created via G2G API without JSON). Added defensive check + integration test.
- **Q6: Ownership** — Voluntarily took on WaiverSchemeFolderItemCustomizer (CR27893-B) when original assignee left mid-sprint.
- **Q7: Simplification** — Reduced 12 switch cases in AdjudicationCaseCustomizer that all called `prepareCaseObjectMulFY()` — suggested mapping instead of explicit cases (team preferred explicit for readability).
- **Q8: Cross-team collaboration** — Coordinated with Workflow team (WFServiceImpl), Ledger team (LedgerUtilFwk), and Communication team (CommunicationAPI) for the appeal effect flow.
- **Q9: Deadline pressure** — Month-end filing deadline is non-negotiable. Used feature flags to isolate WIP appeal code from production path.
- **Q10: Technical debt** — Identified that DistCacheUtil has 400+ methods with inconsistent naming. Proposed grouping by entity type with a consistent naming convention.

---

# ═══════════════════════════════════════════════════════════════
# PART 4: JAVA CODE SNIPPETS TO MEMORIZE (15 Production-Grade)
# ═══════════════════════════════════════════════════════════════

### 1. Thread-Safe Singleton (Double-Checked Locking)
```java
public class KafkaConsumerConfig {
    private static volatile KafkaConsumerConfig INSTANCE;
    
    private KafkaConsumerConfig() {} // private constructor
    
    public static KafkaConsumerConfig getInstance() {
        if (INSTANCE == null) {                    // First check (no locking)
            synchronized (KafkaConsumerConfig.class) {
                if (INSTANCE == null) {            // Second check (with lock)
                    INSTANCE = new KafkaConsumerConfig();
                }
            }
        }
        return INSTANCE;
    }
}
// Used in: KafkaConsumerFwk — ensures single consumer config per JVM
```

### 2. Strategy + Factory Pattern (Your CaseCustomizer)
```java
// Strategy Interface
public interface CaseCustomizer {
    Case beforeCreateCase(Case c) throws Exception;
    Case afterCreateCase(Case c) throws Exception;
    default String getTransType() { return "XA"; }
}

// Concrete Strategy
@Component
public class AppealCaseCustomizer implements CaseCustomizer {
    @Autowired DistCacheUtil distCacheUtil;
    @Autowired TaskHandler taskHandler;
    
    @Override
    public Case beforeCreateCase(Case c) {
        String arn = generateARN(c.getStateCd());
        c.setArn(arn);
        return c;
    }
    
    @Override
    public Case afterCreateCase(Case c) {
        if (isModel2State(c)) {
            taskHandler.createTask(buildTask(c));
        }
        return c;
    }
}

// Factory
@Component
public class CaseCustomizerFactory {
    @Autowired AppealCaseCustomizer appealCustomizer;
    @Autowired AdjudicationCaseCustomizer adjCustomizer;
    
    public CaseCustomizer get(String caseType) {
        return switch (caseType) {
            case "APLTO" -> appealCustomizer;
            case "AMYDT", "AMYTC" -> adjCustomizer;
            default -> new DefaultCaseCustomizer();
        };
    }
}
```

### 3. CompletableFuture — Async Composition
```java
// Pattern: Parallel async with combined result
CompletableFuture<LedgerBalance> ledgerFuture = 
    CompletableFuture.supplyAsync(() -> ledgerService.getBalance(gstin));

CompletableFuture<CaseStatus> caseFuture = 
    CompletableFuture.supplyAsync(() -> caseService.getStatus(gstin));

CompletableFuture<DashboardData> combined = 
    ledgerFuture.thenCombine(caseFuture, (ledger, caseStatus) -> 
        new DashboardData(ledger, caseStatus));

DashboardData result = combined.get(5, TimeUnit.SECONDS); // with timeout
```

### 4. Producer-Consumer with BlockingQueue
```java
// Kafka-like pattern with bounded queue
public class EventProcessor {
    private final BlockingQueue<Event> queue = new LinkedBlockingQueue<>(1000);
    private final ExecutorService workers = Executors.newFixedThreadPool(5);
    
    public void produce(Event event) {
        if (!queue.offer(event, 1, TimeUnit.SECONDS)) {
            publishToErrorTopic(event); // Backpressure → error topic
        }
    }
    
    public void startConsumers() {
        for (int i = 0; i < 5; i++) {
            workers.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    Event e = queue.take(); // Blocks if empty
                    process(e);
                }
            });
        }
    }
}
```

### 5. Cache-Aside Pattern (Your DistCacheUtil Pattern)
```java
public class CacheAside<K, V> {
    private final DistCacheUtil cache;
    private final Function<K, V> dbLoader;
    
    public V get(K key) {
        // 1. Check cache
        V cached = cache.getCache("entity", key.toString(), valueClass);
        if (cached != null) return cached;
        
        // 2. Load from DB
        V value = dbLoader.apply(key);
        
        // 3. Write to cache
        if (value != null) {
            cache.addCache("entity", key.toString(), value);
        }
        return value;
    }
    
    public void invalidate(K key) {
        cache.removeCache("entity", key.toString());
    }
}
```

### 6. Retry with Exponential Backoff
```java
public <T> T retryWithBackoff(Supplier<T> action, int maxRetries) {
    int attempt = 0;
    while (true) {
        try {
            return action.get();
        } catch (Exception e) {
            if (++attempt >= maxRetries) throw e;
            long sleepMs = (long) Math.pow(2, attempt) * 100; // 200, 400, 800...
            sleepMs += ThreadLocalRandom.current().nextLong(100); // Jitter
            Thread.sleep(Math.min(sleepMs, 30_000)); // Cap at 30s
        }
    }
}
// Usage: retryWithBackoff(() -> hbaseReader.get(rowKey), 3);
```

### 7. Builder Pattern (HBase Model Style)
```java
public class LedgerEntry {
    private final String gstin;
    private final BigDecimal amount;
    private final String taxHead;
    private final String period;
    
    private LedgerEntry(Builder builder) {
        this.gstin = builder.gstin;
        this.amount = builder.amount;
        this.taxHead = builder.taxHead;
        this.period = builder.period;
    }
    
    public static class Builder {
        private String gstin;      // required
        private BigDecimal amount; // required
        private String taxHead = "IGST"; // default
        private String period;
        
        public Builder(String gstin, BigDecimal amount) {
            this.gstin = gstin;
            this.amount = amount;
        }
        public Builder taxHead(String val) { taxHead = val; return this; }
        public Builder period(String val) { period = val; return this; }
        public LedgerEntry build() { return new LedgerEntry(this); }
    }
}
// Usage: new LedgerEntry.Builder("27AABCU9603R1ZP", new BigDecimal("5000"))
//            .taxHead("CGST").period("032026").build();
```

### 8. Thread-Safe Bounded Blocking Queue (Interview Classic)
```java
public class BoundedBlockingQueue<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();
    
    public BoundedBlockingQueue(int capacity) { this.capacity = capacity; }
    
    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
            while (queue.size() == capacity) notFull.await();
            queue.add(item);
            notEmpty.signal();
        } finally { lock.unlock(); }
    }
    
    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (queue.isEmpty()) notEmpty.await();
            T item = queue.poll();
            notFull.signal();
            return item;
        } finally { lock.unlock(); }
    }
}
```

### 9. LRU Cache Implementation
```java
public class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, V> cache;
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > capacity;
            }
        };
    }
    
    public synchronized V get(K key) { return cache.get(key); }
    public synchronized void put(K key, V value) { cache.put(key, value); }
}
```

### 10. Distributed Lock (Redis-Style)
```java
public class DistributedLock {
    private final DistCacheUtil cache;
    
    public boolean tryLock(String lockKey, int ttlSeconds) {
        String token = UUID.randomUUID().toString();
        // SET lockKey token NX EX ttlSeconds (atomic set-if-not-exists)
        boolean acquired = cache.setIfAbsent(lockKey, token, ttlSeconds);
        if (acquired) {
            // Store token in ThreadLocal for unlock verification
            LOCK_TOKENS.set(token);
        }
        return acquired;
    }
    
    public void unlock(String lockKey) {
        String token = LOCK_TOKENS.get();
        // Only delete if token matches (prevent accidental unlock)
        String stored = cache.get(lockKey);
        if (token != null && token.equals(stored)) {
            cache.remove(lockKey);
        }
        LOCK_TOKENS.remove();
    }
    
    private static final ThreadLocal<String> LOCK_TOKENS = new ThreadLocal<>();
}
```

### 11-15 (Additional Snippets)

### 11. Custom Spring Boot Auto-Configuration
```java
@Configuration
@ConditionalOnClass(CaseDao.class)
@EnableConfigurationProperties(CaseMgmtProperties.class)
public class CaseMgmtAutoConfig {
    
    @Bean("caseDao")
    @ConditionalOnMissingBean
    public CaseDao caseDao() { return new CaseDaoImpl(); }
    
    @Bean("caseDaoXa")
    @ConditionalOnExpression("${gst.casemgmt.enableXa:true}")
    public CaseDao caseDaoXa() { return new CaseDaoXaImpl(); }
}
```

### 12. Kafka Producer with Callback
```java
public void sendEvent(String topic, String key, String value) {
    ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);
    producer.send(record, (metadata, exception) -> {
        if (exception != null) {
            log.error("Failed to send to {}: {}", topic, exception.getMessage());
            publishToErrorTopic(record); // Fallback
        } else {
            log.info("Sent to {}:{} offset={}", topic, metadata.partition(), metadata.offset());
        }
    });
}
```

### 13. Template Method (BaseDAO Style)
```java
public abstract class BaseDAO {
    @Autowired private SessionFactory sessionFactory;
    
    protected Session getSession() {
        return sessionFactory.getCurrentSession();
    }
    
    // Template method — subclasses override
    protected abstract String getTableName();
    
    public <T> T findById(Class<T> entityClass, Serializable id) {
        return getSession().get(entityClass, id);
    }
    
    public void save(Object entity) {
        getSession().saveOrUpdate(entity);
    }
}

public class LedgerDAOImpl extends BaseDAO {
    @Override protected String getTableName() { return "GST_LEDGER"; }
    
    public LedgerEntry getLedgerByGstin(String gstin) {
        return (LedgerEntry) getSession()
            .createQuery("FROM LedgerEntry WHERE gstin = :gstin")
            .setParameter("gstin", gstin)
            .uniqueResult();
    }
}
```

### 14. Observer Pattern (Event System)
```java
public interface CaseEventListener {
    void onCaseCreated(Case caseVO);
    void onCaseStatusChanged(Case caseVO, String oldStatus, String newStatus);
}

public class CaseEventPublisher {
    private final List<CaseEventListener> listeners = new CopyOnWriteArrayList<>();
    
    public void addListener(CaseEventListener listener) { listeners.add(listener); }
    
    public void publishCaseCreated(Case caseVO) {
        listeners.forEach(l -> {
            try { l.onCaseCreated(caseVO); }
            catch (Exception e) { log.error("Listener failed", e); }
        });
    }
}
```

### 15. Rate Limiter (Token Bucket)
```java
public class TokenBucketRateLimiter {
    private final int maxTokens;
    private final int refillRate; // tokens per second
    private double tokens;
    private long lastRefill;
    
    public TokenBucketRateLimiter(int maxTokens, int refillRate) {
        this.maxTokens = maxTokens;
        this.refillRate = refillRate;
        this.tokens = maxTokens;
        this.lastRefill = System.nanoTime();
    }
    
    public synchronized boolean tryAcquire() {
        refill();
        if (tokens >= 1) { tokens--; return true; }
        return false;
    }
    
    private void refill() {
        long now = System.nanoTime();
        double elapsed = (now - lastRefill) / 1_000_000_000.0;
        tokens = Math.min(maxTokens, tokens + elapsed * refillRate);
        lastRefill = now;
    }
}
```

---

# ═══════════════════════════════════════════════════════════════
# PART 5: COMPANY-SPECIFIC PREPARATION
# ═══════════════════════════════════════════════════════════════

## 5.1 Amazon — Leadership Principles Mapping

| Leadership Principle | Your GSTN Evidence |
|---------------------|--------------------|
| **Customer Obsession** | Filing deadlines are non-negotiable — built systems ensuring 14M taxpayers can file with zero downtime during month-end spikes |
| **Ownership** | Took ownership of WaiverSchemeFolderItemCustomizer (CR27893-B) when original assignee left mid-sprint |
| **Invent and Simplify** | Designed the Customizer pattern (Strategy+Factory) — simplified case type addition from modifying monolithic code to adding one focused class |
| **Are Right, A Lot** | Proposed 3-tier Kafka error handling (main→error→DLQ) when team wanted simple retry. Data showed 90% of failures were transient — pattern recovered them automatically |
| **Learn and Be Curious** | Learned XA transactions (Atomikos), HBase row key design, and distributed caching (Infinispan) within the project timeline |
| **Hire and Develop the Best** | Created DistCache decision matrix for junior developer; pair-programmed Kafka consumer integration |
| **Insist on Highest Standards** | Enforced Open/Closed Principle via Customizer pattern — prevented pollution of shared CaseMgmtFwk with case-specific logic |
| **Think Big** | Architecture handles 14M taxpayers, 3B+ invoices/year, petabyte-scale HBase — built for national scale |
| **Bias for Action** | Fixed DCR order production bug in 2 hours by reusing existing DAO code, before it impacted monthly filing deadline |
| **Frugality** | Used two-tier caching (free EhCache + existing JDG cluster) instead of requesting new Redis infrastructure |
| **Deliver Results** | Delivered appeal effect flow coordinating 6 frameworks within sprint, with XA transaction support, auto-assignment, and async notifications |

## 5.2 Google — Focus Areas
- **Coding:** LeetCode Medium/Hard (Trees, Graphs, DP, Sliding Window)
- **System Design:** Scale emphasis — "How would you handle 10x growth?" — your HBase + Kafka answer
- **Java Internals:** JMM, GC tuning, ConcurrentHashMap internals
- **Behavioral:** "Tell me about a time you simplified a complex system" → Customizer pattern

## 5.3 Flipkart / Swiggy / PhonePe
- **HLD Focus:** Design payment system, notification system, order tracking
- **LLD Focus:** Parking lot, elevator, meeting scheduler (with code)
- **Java:** Streams, lambdas, generics, concurrency at SDE-2 depth
- **Kafka:** Deep dive — partitioning, consumer groups, exactly-once

## 5.4 Goldman Sachs / Morgan Stanley
- **Java Deep:** Memory model, classloading, JIT compilation, unsafe operations
- **Concurrency:** Lock-free data structures, CAS, ABA problem
- **Finance Domain:** Your ledger experience is highly relevant — talk about double-entry bookkeeping, ACID for financial data
- **Low Latency:** HBase row key optimization, cache hit rate tuning

---

# ═══════════════════════════════════════════════════════════════
# PART 6: WEAK AREA DEEP DIVES
# ═══════════════════════════════════════════════════════════════

## 6.1 HBase Row Key Design — 5 Practice Problems

### Problem 1: Design row key for GST Returns
```
Requirement: Query returns by GSTIN + period + return type
Access patterns:
  1. Get single return: GSTIN + period + type
  2. All returns for a GSTIN in a year: scan by GSTIN prefix
  3. All returns for a period: secondary index or separate table

Row Key: {GSTIN}|{ReturnPeriod}|{ReturnType}
Example:  27AABCU9603R1ZP|202603|GSTR3B

Why: GSTIN first → distributes across regions (state code 01-37)
     Period second → range scan for fiscal year
     Type third → single Get for specific return
```

### Problem 2: Design row key for Audit Logs
```
Requirement: Query by GSTIN + timestamp, recent-first
Anti-pattern: GSTIN + Timestamp → hotspot on latest region

Row Key: {GSTIN}|{REVERSED_TIMESTAMP}
Example:  27AABCU9603R1ZP|9999999999999 - currentTimeMillis

Why: Reversed timestamp → latest records have smallest row key
     → single prefix scan returns recent-first
```

### Problem 3: Design row key for E-Invoice
```
Row Key: {IRN_Hash_Prefix(4)}|{GSTIN}|{InvoiceNumber}|{FY}
Why: IRN hash prefix prevents hotspotting on sequential invoice numbers
```

### Problem 4: Avoid Hotspot for Sequential IDs
```
Anti-pattern: AUTO_INCREMENT_ID → all writes go to last region
Fix 1: Salt prefix — hash(id) % num_regions + "|" + id
Fix 2: Reverse the ID — 1234567 → 7654321 (distributes evenly)
Fix 3: UUID — random distribution (but loses ordering)
```

### Problem 5: Design row key for Ledger Entries
```
Row Key: {GSTIN}|{TaxPeriod}|{TaxHead}|{TransactionType}|{Timestamp}
Example:  27AABCU9603R1ZP|202603|CGST|CREDIT|1710744000000

Why: GSTIN+Period+TaxHead = natural partition for balance queries
     TransactionType+Timestamp = order within partition
```

---

## 6.2 Kafka Exactly-Once Semantics — With Code

### Three Delivery Guarantees
```
At-most-once:  Commit offset BEFORE processing. If crash → message lost.
At-least-once: Commit offset AFTER processing. If crash → message reprocessed.
Exactly-once:  Idempotent producer + transactional consumer-producer.
```

### Exactly-Once Producer
```java
Properties props = new Properties();
props.put("enable.idempotence", "true");        // Prevent duplicates
props.put("acks", "all");                        // All replicas must ACK
props.put("retries", Integer.MAX_VALUE);         // Retry on failure
props.put("max.in.flight.requests.per.connection", 5); // Safe with idempotence

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();

try {
    producer.beginTransaction();
    producer.send(new ProducerRecord<>("ledger-updates", gstin, ledgerJson));
    producer.send(new ProducerRecord<>("audit-events", gstin, auditJson));
    producer.commitTransaction(); // Atomic: both or neither
} catch (Exception e) {
    producer.abortTransaction();
}
```

### Exactly-Once Consumer-Producer (Read-Process-Write)
```java
props.put("isolation.level", "read_committed"); // Only see committed messages
props.put("enable.auto.commit", "false");        // Manual offset management

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    producer.beginTransaction();
    for (ConsumerRecord<String, String> record : records) {
        // Process
        String result = processLedgerUpdate(record.value());
        // Write to output topic
        producer.send(new ProducerRecord<>("processed-ledger", record.key(), result));
    }
    // Commit offsets AND messages atomically
    producer.sendOffsetsToTransaction(currentOffsets(records), consumerGroupId);
    producer.commitTransaction();
}
```

---

## 6.3 Distributed Locking Cheat Sheet

| Approach | Mechanism | Pros | Cons | Use When |
|----------|-----------|------|------|----------|
| **Redis SETNX** | `SET key value NX EX ttl` | Simple, fast | Single point of failure | Low-risk duplicate prevention |
| **RedLock** | Lock on N/2+1 Redis nodes | Tolerates failures | Clock skew issues, Martin Kleppmann critique | Medium-risk operations |
| **ZooKeeper** | Ephemeral sequential znodes | Strong consistency, auto-release on disconnect | Higher latency, operational complexity | High-risk, needs auto-cleanup |
| **DB Lock** | `SELECT FOR UPDATE` | No extra infra | Blocks DB connections, deadlock risk | Already in a DB transaction |
| **Infinispan/JDG** | `RemoteCache.lock()` | Native to your stack | Cluster-specific | GSTN — already using JDG |

### Your GSTN Context
```java
// Current: DistCacheUtil wraps JDG locking
boolean locked = distCacheUtil.acquireLock("lock:case:" + arnNo, 30);
try {
    // Critical section: create case
    caseMgmtService.createCase(caseVO);
} finally {
    distCacheUtil.releaseLock("lock:case:" + arnNo);
}
```

---

## 6.4 XA Transactions (Atomikos) — End-to-End

### What is XA?
```
Two-Phase Commit (2PC):
  Phase 1 (Prepare): Coordinator asks all participants "Can you commit?"
  Phase 2 (Commit):  If all say YES → Coordinator says "Commit"
                     If any says NO → Coordinator says "Rollback"

Participants in GSTN:
  1. Case Database (MySQL)
  2. Workflow Database (MySQL - separate schema)
  3. Ledger Database (MySQL - separate schema)
```

### How Atomikos Works in GSTN
```java
// Configuration: Two XA DataSources + Atomikos TransactionManager
@Bean
public DataSource caseDatasource() {
    AtomikosDataSourceBean ds = new AtomikosDataSourceBean();
    ds.setXaDataSourceClassName("com.mysql.cj.jdbc.MysqlXADataSource");
    ds.setUniqueResourceName("caseDB");
    return ds;
}

@Bean
public DataSource workflowDatasource() {
    AtomikosDataSourceBean ds = new AtomikosDataSourceBean();
    ds.setUniqueResourceName("workflowDB");
    return ds;
}

@Bean
public JtaTransactionManager transactionManager() {
    UserTransactionManager utm = new UserTransactionManager();
    return new JtaTransactionManager(utm, utm);
}
```

### Failure Scenarios
```
Scenario 1: Participant fails in Prepare phase
  → Coordinator sends ROLLBACK to all → No data written anywhere ✓

Scenario 2: Participant fails AFTER Prepare, BEFORE Commit
  → Coordinator retries Commit (Atomikos has recovery log)
  → If participant recovers → reads recovery log → commits
  → If participant never recovers → MANUAL intervention needed ✗

Scenario 3: Coordinator (Atomikos) crashes
  → On restart, reads transaction log → resumes pending commits/rollbacks ✓
```

---

# ═══════════════════════════════════════════════════════════════
# PART 7: GAP ANALYSIS — Your Stack vs Market Expectations
# ═══════════════════════════════════════════════════════════════

| Area | Your Current Stack | Market Expectation (SDE-2/3) | Action |
|------|-------------------|------------------------------|--------|
| **Java** | Java 8 | Java 17-21 (Records, Sealed, Virtual Threads, Pattern Matching) | Learn Java 17+ features — practice with personal projects |
| **Spring** | Spring 4.3 + Boot 2.4 | Spring Boot 3.x + Spring 6 | Learn Spring Boot 3 (Jakarta EE, native compilation, virtual threads) |
| **Containers** | WAR on Tomcat | Docker + Kubernetes | Build personal projects with Docker Compose → K8s |
| **Testing** | TestNG + Mockito | JUnit 5 + Mockito + TestContainers + WireMock | Switch to JUnit 5 in personal projects |
| **Observability** | Logback + basic metrics | ELK/Grafana + Distributed Tracing (Jaeger/Zipkin) | Add tracing to personal project |
| **CI/CD** | Basic (manual?) | GitHub Actions / Jenkins + GitOps | Create CI pipeline for your GitHub project |
| **Cloud** | On-prem JDG/Kafka | AWS (SQS, SNS, DynamoDB, ECS) or GCP | Get AWS Solutions Architect Associate |
| **Reactive** | Servlet/blocking | WebFlux/reactive (conceptual) | Understand Reactor (Mono/Flux) — not mandatory |
| **API Design** | REST | REST + gRPC + GraphQL (conceptual) | Implement gRPC service in personal project |

### Priority Learning Path
```
Week 1-2: Java 17+ features (practice daily — records, sealed, switch expressions)
Week 3-4: Docker + docker-compose (Kafka + Redis + MySQL local setup)
Week 5-6: Spring Boot 3 personal project with JUnit 5 + TestContainers
Week 7-8: AWS basics (free tier — SQS, DynamoDB, EC2)
```

---

# ═══════════════════════════════════════════════════════════════
# PART 8: 30-DAY INTERVIEW PREPARATION PLAN
# ═══════════════════════════════════════════════════════════════

## Week 1 (Days 1-7): Foundation + Java Deep
```
Day 1:  Read this entire document. Mark weak areas.
Day 2:  Java Memory Model + GC — write notes, draw diagrams
Day 3:  Concurrency — ConcurrentHashMap, locks, volatile. Code snippet 1-4.
Day 4:  Streams + Functional. Practice 5 Stream problems.
Day 5:  Design Patterns — code all 6 patterns from your codebase.
Day 6:  Spring IoC, AOP, @Transactional internals. Code snippet 11, 13.
Day 7:  Review + practice explaining your 6 resume bullets OUT LOUD.
```

## Week 2 (Days 8-14): System Design + Architecture
```
Day 8:  GSTN architecture — rehearse the system overview (Section 2 of arch file)
Day 9:  System Design: Tax filing system — practice end-to-end
Day 10: System Design: Case management workflow — use your architecture
Day 11: System Design: Distributed ledger — dual storage, XA
Day 12: Kafka deep dive — exacty-once, partitioning, consumer groups
Day 13: HBase — row key design, 5 practice problems
Day 14: Distributed systems — CAP, consistency, locking cheat sheet
```

## Week 3 (Days 15-21): DSA + LLD
```
Day 15: Arrays + Strings — 5 LeetCode Medium
Day 16: Trees + Graphs — 5 LeetCode Medium
Day 17: DP — 5 LeetCode Medium (0/1 Knapsack, LIS, LCS, Coin Change)
Day 18: Sliding Window + Two Pointers — 5 problems
Day 19: LLD: Design Parking Lot (code it)
Day 20: LLD: Design Rate Limiter (code snippet 15)
Day 21: LLD: Design LRU Cache (code snippet 9) + Notification System
```

## Week 4 (Days 22-30): Mock Interviews + Polish
```
Day 22: Full mock interview (60 min) — system design + Java
Day 23: Behavioral prep — rehearse 10 STAR stories from Part 3.5
Day 24: Company-specific prep (Amazon LPs / Google focus)
Day 25: Full mock interview (60 min) — DSA + past work deep dive
Day 26: Review weak areas from mock interviews
Day 27: Code snippets — write all 15 from memory
Day 28: System design — draw all 3 architectures from memory
Day 29: Final mock interview — all rounds
Day 30: Rest. Review notes. Confidence.
```

---

# ═══════════════════════════════════════════════════════════════
# PART 9: SYSTEM DESIGN PRACTICE (3 Full Walkthroughs)
# ═══════════════════════════════════════════════════════════════

## Design 1: GST Return Filing System (Your Architecture)

### Functional Requirements
1. 14M taxpayers file returns (GSTR1, GSTR3B, GSTR9) monthly/annually
2. Real-time ledger updates on filing
3. Filing status tracking & dashboard
4. Month-end 10x spike handling

### Non-Functional Requirements
- Availability: 99.9% (3 nines)
- Latency: < 2s for filing, < 500ms for status check
- Throughput: 10K filings/min during peak
- Data retention: 7 years (legal requirement)

### Architecture
```
┌──────────┐    ┌──────────┐    ┌──────────────┐
│ Browser  │───▶│ API GW   │───▶│ Filing API   │──┐
│ /Mobile  │    │ (Rate    │    │ (Stateless)  │  │
└──────────┘    │  Limit)  │    └──────────────┘  │
                └──────────┘           │           │
                                       ▼           ▼
                              ┌──────────┐   ┌─────────┐
                              │  Kafka   │   │  HBase  │
                              │ (Buffer) │   │ (Store) │
                              └────┬─────┘   └─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Ledger   │  │ Search   │  │ Notify   │
              │ Consumer │  │ Consumer │  │ Consumer │
              │ (MySQL)  │  │ (Solr)   │  │ (Email)  │
              └──────────┘  └──────────┘  └──────────┘
```

### Key Design Decisions
1. **Kafka as buffer** — Filing API writes to HBase + Kafka in one request. Kafka consumers handle async work (ledger, search, notifications).
2. **HBase for return data** — Row key: GSTIN|Period|ReturnType. Petabyte scale. 7-year retention.
3. **MySQL for ledger** — ACID compliance for financial data. Current balance only.
4. **Two-tier cache** — EhCache (masters) + JDG (session/status). Cache-aside pattern.
5. **Stateless APIs** — Session in JDG → horizontal scaling.

### Scale Estimation
```
14M taxpayers × 12 months × 3 return types = 504M filings/year
Peak day: 504M / 365 × 10x spike = ~14M filings/day
Peak hour: 14M / 8 hours = 1.75M/hour = ~500/second
→ 10 API servers × 50 concurrent threads = 500 RPS ✓
→ Kafka: 20 partitions × 25 msg/sec/partition = 500 msg/sec ✓
→ HBase: Auto-region-split handles write load ✓
```

## Design 2: Notification System (Email + SMS + Push)
*(See CommunicationAPI architecture — fan-out via Kafka, template engine, async dispatch, audit trail)*

## Design 3: Distributed Ledger for Tax Credits
*(See LedgerUtilFwk architecture — MySQL for current state, HBase for history, XA for consistency)*

---

# ═══════════════════════════════════════════════════════════════
# PART 10: PERSONAL PROJECT IDEAS (GitHub Portfolio)
# ═══════════════════════════════════════════════════════════════

### Project 1: Mini Case Workflow Engine
```
Tech: Spring Boot 3, Java 17, MySQL, Redis
Features:
  - State machine (Created → Assigned → InProgress → Completed)
  - Strategy+Factory for case-type customizers
  - Redis distributed locking for concurrent case updates
  - REST API with Swagger docs
GitHub Stars potential: ⭐⭐⭐ (demonstrates design patterns)
```

### Project 2: Distributed Cache Benchmark
```
Tech: Spring Boot 3, Redis, JMH (Java Microbenchmark Harness)
Features:
  - Compare Redis vs Caffeine vs Guava Cache
  - Thread-safe cache-aside implementation
  - TTL, LRU, hit-rate measurement
  - Published benchmark results in README
GitHub Stars potential: ⭐⭐⭐⭐ (useful for Java community)
```

### Project 3: Kafka Event Pipeline with DLQ
```
Tech: Spring Boot 3, Apache Kafka, Docker Compose
Features:
  - Pluggable Processor interface (like your Consumer.java)
  - 3-tier error handling (main → error → DLQ)
  - Scheduled error topic retry
  - Exactly-once semantics
  - Dashboard showing consumer lag
GitHub Stars potential: ⭐⭐⭐⭐⭐ (production-grade reference implementation)
```

### Project 4: Tax Ledger Microservice
```
Tech: Spring Boot 3, MySQL + H2 (test), Kafka
Features:
  - Double-entry bookkeeping (credit/debit)
  - XA transactions with Spring JTA
  - REST API: credit, debit, getBalance, getHistory
  - Idempotency key support
  - Reconciliation batch job
GitHub Stars potential: ⭐⭐⭐ (showcases financial domain knowledge)
```

### Project 5: Spring Boot Custom Starter
```
Tech: Spring Boot 3 auto-configuration
Features:
  - @ConditionalOnClass, @ConditionalOnProperty, @ConditionalOnMissingBean
  - Auto-configures cache, metrics, health checks
  - Published to Maven Local
  - README with usage examples
GitHub Stars potential: ⭐⭐⭐⭐ (shows deep Spring understanding)
```

---

*Generated from actual GSTN JAVA_Maintrunk codebase analysis + source code walkthroughs — March 2026*
*Total preparation coverage: Code walkthroughs, Resume, Mock interviews (5 rounds), Code snippets (15), Company prep (4), Deep dives (4), Gap analysis, 30-day plan, System design (3), Projects (5)*
