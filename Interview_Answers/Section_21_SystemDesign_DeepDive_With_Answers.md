# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM DESIGN INTERVIEW — DEEP DIVE (8 FULL PROBLEMS WITH COMPLETE ANSWERS)
# Based on YOUR Actual GSTN Codebase Architecture
# ═══════════════════════════════════════════════════════════════════════════════
#
# How to use this document:
#   1. Each problem follows the EXACT system design interview framework:
#      Clarify → Estimate → High-Level Design → Deep Dive → Bottlenecks → Tradeoffs
#   2. Every answer maps DIRECTLY to real classes/patterns in your codebase
#   3. You can say "I've built this" — because you have
#
# Problems Covered:
#   1. Design a GST Return Filing System (14M taxpayers, 500M+ filings/year)
#   2. Design a Case Management Workflow Engine (20+ case types, state machine)
#   3. Design a Distributed Tax Ledger (dual-storage MySQL + HBase)
#   4. Design a Distributed Caching Layer (70+ cache regions, 2-tier)
#   5. Design an Async Event Processing Pipeline (Kafka + DLQ + retry)
#   6. Design a Notification System (Email + SMS, template-driven, async)
#   7. Design an E-Invoice System with QR & Digital Signatures (IRN, IRP)
#   8. Design an Authentication & Authorization System (LDAP + OTP + RBAC)
#
# BONUS: Market-Gap Learning Plan + 3 Portfolio Projects
# ═══════════════════════════════════════════════════════════════════════════════

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 1: Design a GST Return Filing System                           ║
# ║  (Scale: 14M taxpayers, 500M+ filings/year, month-end 10x spikes)      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Taxpayer saves draft return (GSTR-1, GSTR-3B, GSTR-9, etc.)
2. Taxpayer submits return → system validates (syntax + business rules)
3. Taxpayer files return with digital signature (DSC) or electronic verification (EVC/OTP)
4. System generates ARN (Acknowledgment Reference Number) on successful filing
5. System auto-calculates liability, interest, and ITC (Input Tax Credit)
6. System updates ledger (cash, ITC, liability) post-filing
7. Dashboard shows filing status per GSTIN per period
8. Support for amendments (GSTR-1A, GSTR-3B amendments)

### Non-Functional Requirements
- **Availability**: 99.9% (government critical infrastructure)
- **Latency**: < 2s for save/submit, < 5s for filing (includes DSC verification)
- **Throughput**: 500 filings/sec during peak (month-end last 3 days)
- **Data retention**: 7+ years (legal mandate)
- **Consistency**: Strong consistency for ledger updates, eventual for search/dashboard
- **Security**: DSC/EVC mandatory, GSTIN-level access control, encrypted PII

---

## Step 2: Scale Estimation

```
Taxpayers:          14M registered GSTINs
Return types:       ~10 (GSTR-1, 3B, 4, 5, 6, 7, 8, 9, 9A, 9C)
Filing frequency:   Monthly (GSTR-1, 3B), Quarterly (GSTR-4), Annual (GSTR-9)
Annual filings:     14M × 12 months × 2 main returns = 336M + annual = ~400M/year

Peak load:
  - 70% of filings happen in last 3 days of month
  - 400M × 0.7 / 12 months / 3 days = ~650K filings/day peak
  - 650K / 8 hours = ~81K/hour = ~22/second steady, 10x spike = 220/sec burst
  - With GSTR-1 + GSTR-3B on same deadline: 500/sec burst

Storage:
  - Average return payload: ~50 KB (JSON)
  - 400M × 50 KB = 20 TB/year raw
  - With 7-year retention + compression: ~50 TB in HBase

Ledger entries:
  - Each filing creates 3-5 ledger entries (ITC, Cash, Liability)
  - 400M × 4 = 1.6B ledger rows/year
```

---

## Step 3: High-Level Architecture

```
                        ┌──────────────────┐
                        │   Load Balancer   │
                        │   (F5 / HAProxy)  │
                        └────────┬─────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                   ▼
     ┌─────────────┐   ┌─────────────┐     ┌─────────────┐
     │ ReturnAPI    │   │ ReturnAPI   │     │ ReturnAPI   │
     │ Instance 1   │   │ Instance 2  │     │ Instance N  │
     │ (Stateless)  │   │ (Stateless) │     │ (Stateless) │
     └──────┬───────┘   └──────┬──────┘     └──────┬──────┘
            │                  │                    │
            └──────────────────┼────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                      ▼
  ┌─────────────┐     ┌──────────────┐      ┌──────────────┐
  │  Infinispan  │     │    Kafka     │      │    HBase     │
  │  (JDG Cache) │     │  (20+ parts) │      │  (Returns)   │
  │  - Sessions  │     │  - Filing    │      │  - Payload   │
  │  - Txn State │     │  - Ledger    │      │  - History   │
  │  - Masters   │     │  - Search    │      │  Row: GSTIN| │
  └─────────────┘     │  - Notify    │      │  Period|Type │
                      └──────┬───────┘      └──────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                   ▼
   ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
   │ Ledger      │   │ Solr Index   │   │ Communication│
   │ Consumer    │   │ Consumer     │   │ Consumer     │
   │ (MySQL)     │   │ (Search)     │   │ (Email/SMS)  │
   └─────────────┘   └──────────────┘   └──────────────┘
```

### Your Actual Codebase Mapping:
| Component | Actual Class/Module |
|-----------|-------------------|
| ReturnAPI (Save/Submit) | `Core-API/ReturnAPI/` → `IGstr3BService.saveGstr3BFile()` |
| ReturnAPI (File) | `IGstr3BService.fileReturn()`, `fileEvcReturn()` |
| Validation Engine | `Commons/ValidationUtilFwk/` → `Validations.validateType1Data()` |
| Filing Engine | `Commons/FilingUtilFwk/` → `ReturnFilingEngine` (Template Method) |
| Proceed-to-File | `ProceedToFileEngine` → insertToDb → addToCache → pushToKafka |
| HBase Storage | `Commons/HbaseAccessFwk/` → `GSTMutator.write()`, `GSTReader.lookup()` |
| Cache Layer | `Commons/DistCacheFwk/` → `DistCacheUtil` (70+ regions) |
| Kafka Pipeline | `Commons/KafkaConsumerFwk/` → `Consumer.java`, `ProducerService.java` |
| Ledger Update | `Commons/LedgerUtilFwk/` → `UtilizeFundsLedgServiceImpl` |
| Signature Verify | `DscEvcValidation`, `TokenGeneratorUtil` |

---

## Step 4: Deep Dive — Component Design

### 4A. Return Filing Engine (Template Method Pattern)

```
YOUR ACTUAL PATTERN (ReturnFilingEngine.java):

  ┌─────────────────────────────────┐
  │    ReturnFilingEngine           │  ← Abstract base class
  │  ──────────────────────────     │
  │  doPreValidations()         [F] │  ← Final: form filed? ready? in-process?
  │  doFormSpecificValidation() [A] │  ← Abstract: GSTR-1 vs 3B vs 9 rules
  │  doSummaryPayloadValidation [A] │  ← Abstract: section totals match?
  │  doOffsetValidation()       [A] │  ← Abstract: ITC offset rules
  │  doSignValidation()         [F] │  ← Final: DSC or EVC verification
  │  executeFiling()            [F] │  ← Final: persist + ARN + events
  └───────────┬─────────────────────┘
              │ extends
    ┌─────────┴──────────┐
    ▼                    ▼
┌──────────┐      ┌──────────┐
│ Gstr3B   │      │ Gstr1    │
│ Filing   │      │ Filing   │
│ Engine   │      │ Engine   │
└──────────┘      └──────────┘
```

**Why Template Method?**
- 10+ return types share 60% common logic (pre-validation, signing, ARN generation)
- Each return type has unique validation rules (GSTR-3B has 7 sections, GSTR-1 has 13)
- Adding a new return type = implement 3 abstract methods, zero changes to base class
- **Interview answer**: "We used Template Method instead of Strategy because the execution ORDER matters. Pre-validation must happen before form-specific, which must happen before signing. Template Method enforces this sequence while Strategy doesn't."

### 4B. Proceed-to-File Pipeline

```
YOUR ACTUAL FLOW (ProceedToFileEngine.java):

  User clicks "File" button
        │
        ▼
  ┌── doPreValidations() ──┐
  │  • Is return "SUBMITTED"?│
  │  • Not already filed?    │
  │  • No concurrent req?   │
  └──────────┬──────────────┘
             ▼
  ┌── doFormSpecificValidation() ──┐
  │  • Section totals match         │
  │  • Auto-calc liability          │
  │  • Interest computation         │
  └──────────┬─────────────────────┘
             ▼
  ┌── insertToDb() ──────────────┐
  │  • Insert RET_REQ_DETL table  │
  │  • Status = "PROCESSING"      │
  │  • @Transactional(REQUIRED)   │
  └──────────┬───────────────────┘
             ▼
  ┌── addToCache() ──────────────┐
  │  • API_TRANSACTION_CACHE      │  ← Prevents duplicate submissions
  │  • RETURN_SUBMIT_STATUS_CACHE │  ← Dashboard shows "In Progress"
  └──────────┬───────────────────┘
             ▼
  ┌── pushRequestToKafka() ──────┐
  │  • Topic: FILING_REQUEST      │
  │  • Async processing begins    │
  │  • Storm/Consumer picks up    │
  └──────────┬───────────────────┘
             ▼
  ┌── ASYNC CONSUMER ────────────┐
  │  1. Validate payload hash     │  ← MD5 integrity check
  │  2. Write return to HBase     │  ← GSTMutator.write()
  │  3. Update ledger (MySQL)     │  ← Credit/Debit entries
  │  4. Update Solr index         │  ← Search/dashboard
  │  5. Generate ARN              │
  │  6. Send notification         │  ← Email/SMS via CommunicationAPI
  │  7. Update cache status       │  ← FILED
  └──────────────────────────────┘
```

### 4C. HBase Row Key Design for Returns

```
Row Key: {GSTIN_HASH}|{GSTIN}|{RET_PERIOD}|{RET_TYPE}|{SECTION}

Example: A7F3|27AABCU9603R1ZM|122025|GSTR3B|3.1

Why this design:
  ├── GSTIN_HASH (first 4 chars of MD5)
  │     → Prevents region hotspots (salting)
  │     → 16^4 = 65,536 possible prefixes → even distribution
  │
  ├── GSTIN (15 chars)
  │     → Natural partition key
  │     → All data for one taxpayer is co-located
  │
  ├── RET_PERIOD (MMYYYY)
  │     → Enables period-based range scans
  │
  ├── RET_TYPE
  │     → Filter by return type
  │
  └── SECTION
        → Sub-document access without full scan

Actual class: RowKey (org.gst.hbase.access.layer0.impl)
  - Builder pattern with up to 15 components
  - getPositionOfHashedField() → salt position
  - getPositionOfConstantField() → fixed fields
  - Immutable (Guava ImmutableList)
```

### 4D. Payload Validation (Multi-Level)

```
YOUR ACTUAL PATTERN (PayloadValidationUtil.java + Validations.java):

Level 1: HASH INTEGRITY
  │  isValidHash(inputPayload, storedPayload)
  │  → MD5 comparison: was the payload tampered after submit?
  │
Level 2: PROFILE-BASED SECTION VALIDATION
  │  isPayloadContainingValidSections(gstin, retPrd, list, profile)
  │  → Sahaj (SJ): Only B2C, REV sections allowed
  │  → Sugam (SM): B2B, B2BA + Sahaj sections
  │  → Normal (QN/MN): All 13 sections
  │  → Prevents small taxpayer from claiming large-business exemptions
  │
Level 3: FIELD-LEVEL VALIDATION
  │  validateType1Data(validations, data, category, globalFieldMap)
  │  → Type-safe generics: List<T> of any section model
  │  → Separates valid vs error records
  │  → Cross-field validation via globalFieldMap
  │
Level 4: BUSINESS RULE VALIDATION
     → ITC offset rules (IGST before CGST/SGST)
     → Interest calculation (late filing)
     → Auto-liability computation
     → Negative liability balance check (NegativeLiabilityBalanceVO)
```

---

## Step 5: Bottlenecks & Solutions

| Bottleneck | Solution in Your Architecture |
|-----------|------------------------------|
| Month-end spike (10x) | Kafka absorbs burst → consumers scale horizontally |
| Duplicate filing | API_TRANSACTION_CACHE check before processing |
| HBase write hotspot | Salted row key (GSTIN_HASH prefix) |
| Ledger consistency | @Transactional(REQUIRES_NEW) + XA for cross-DB |
| Large payload (GSTR-1 with 10K invoices) | Chunked upload + HBase wide-column per section |
| Concurrent edits to same return | Distributed lock via cache (isExists + addToCache) |
| 7-year data retention | HBase TTL per column family, MySQL archive partitions |

---

## Step 6: Key Tradeoffs

| Decision | Tradeoff | Why This Choice |
|----------|----------|-----------------|
| HBase over MongoDB | No joins, harder queries vs petabyte scale, auto-sharding | Returns are write-heavy, read-by-key, rarely joined |
| Kafka over RabbitMQ | Higher throughput, no priority queue vs complex setup | 500/sec peak, need replay capability for audits |
| Template Method over Strategy | Rigid sequence vs flexible composition | Filing sequence MUST be enforced (validate→sign→persist) |
| Sync DSC + Async ledger | User waits for signature but not ledger | Signature is user-blocking; ledger can be eventual |
| Cache-aside over write-through | Extra cache-miss on cold start vs simpler consistency | Masters change rarely; session data is ephemeral |

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2: Design a Case Management Workflow Engine                    ║
# ║  (20+ case types, state machine, multi-actor, SLA tracking)            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Create cases for 20+ types: Adjudication, Appeal, DCR, APLTD, Waiver, Rectification, Revision...
2. Each case type has DIFFERENT pre/post-creation logic
3. Assign cases to officers with jurisdiction-based routing
4. Track case lifecycle: Created → Assigned → In-Progress → Hearing → Order → Closed
5. SLA enforcement: each task has a due date, escalation on breach
6. Task reassignment across officers
7. Full audit trail (who did what, when)
8. Workflow tasks: notice issuance, hearing scheduling, order passing, appeal filing

### Non-Functional Requirements
- **Consistency**: Strong (can't lose a case or create duplicates)
- **Audit**: Every state change must be logged (legal compliance)
- **Concurrency**: Multiple officers working on same GSTIN's cases simultaneously
- **SLA**: Real-time SLA tracking, alerts on approaching deadlines

---

## Step 2: Scale Estimation

```
Active GSTINs:      14M
Cases created/year:  ~2M (adjudication, demands, appeals, etc.)
Active cases:        ~500K at any time
Tasks per case:      3-8 tasks average → 1.5M-4M tasks active
Officers:            ~50K tax officers across 36 states
Reads (dashboard):   50K officers × 20 checks/day = 1M reads/day
Writes (updates):    500K case updates/day
```

---

## Step 3: High-Level Architecture

```
                    ┌────────────────────┐
                    │  LitigationAPI2    │  ← REST controllers
                    │  (Case Operations) │
                    └────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐ ┌───────────┐ ┌────────────┐
     │ CaseMgmt     │ │ WorkFlow  │ │ AlertSvc   │
     │ Service      │ │ Service   │ │ (SLA)      │
     └──────┬───────┘ └─────┬─────┘ └────────────┘
            │               │
            ▼               ▼
     ┌──────────────┐ ┌───────────────┐
     │ Customizer   │ │ WfProcess +   │
     │ Factory      │ │ WfTask Tables │
     │ (Strategy)   │ │ (MySQL)       │
     └──────┬───────┘ └───────────────┘
            │
    ┌───────┼───────────────┬──────────────────┐
    ▼       ▼               ▼                  ▼
┌────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐
│Adjud.  │ │Appeal   │ │DCR       │ │Waiver        │
│Custom. │ │Custom.  │ │Custom.   │ │Custom.       │
└────────┘ └─────────┘ └──────────┘ └──────────────┘
```

### Your Actual Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Case Service | `CaseMgmtService` (Commons/CaseMgmtFwk) |
| Customizer Interface | `CaseCustomizer` — `beforeCreateCase()`, `afterCreateCase()`, `getTransType()` |
| Factory | `CaseCustomizerFactory` (@Component, switch-based routing) |
| Adjudication | `AdjudicationCaseCustomizer` — multi-case-type routing, CBIC migration |
| Appeal | `AppealTranCaseCustomizer` — ARN generation, Model-2 state detection |
| Workflow Engine | `WFServiceImpl` — `addWfProcess()`, `addWfTask()`, `updateTaskStatus()` |
| Task Entity | `WfTask` (@Entity) — taskId, assignedTo, dueDt, isComplete |
| Process Entity | `WfProcess` (@Entity) — processId, arnNum, processStatus |
| History | `WfTaskHistory`, `WfProcessHistory` — audit trail |

---

## Step 4: Deep Dive

### 4A. Strategy + Factory Pattern (CaseCustomizerFactory)

```java
// YOUR ACTUAL CODE (CaseCustomizerFactory.java):

@Component
public class CaseCustomizerFactory {

    @Autowired AdjudicationCaseCustomizer adjudicationCustomizer;
    @Autowired AppealTranCaseCustomizer appealTranCustomizer;
    @Autowired WaiverSchemeFolderItemCustomizer waiverCustomizer;
    @Autowired DefaultCaseCustomizer defaultCustomizer;
    // ... 20+ customizers autowired

    public CaseCustomizer getCustomizer(String caseType) {
        switch (caseType) {
            case "AMYDT": case "AMYTC": case "AMYGP":
                return adjudicationCustomizer;
            case "APLTD": case "APLHC": case "APLSC":
                return appealTranCustomizer;
            case "WVRSM":
                return waiverCustomizer;
            // ... 20+ case types
            default:
                return defaultCustomizer;
        }
    }
}
```

**Interview explanation:**
> "We have 20+ case types, each with different initialization logic. Adjudication needs CBIC migration checks. Appeal needs ARN generation and Model-2 state detection. DCR needs demand letter creation. Instead of a 2000-line if-else, we used Strategy pattern — each customizer implements the same interface (`beforeCreateCase`, `afterCreateCase`) with type-specific logic. The Factory resolves which strategy to use at runtime.

> Adding a new case type like 'Rectification' means: (1) create `RectificationCaseCustomizer implements CaseCustomizer`, (2) add one line to the factory switch. Zero changes to the case creation flow."

### 4B. Case Lifecycle — State Machine

```
YOUR ACTUAL STATE MACHINE (WfProcess + WfTask):

WfProcess States:
  INITIATED ──→ IN_PROGRESS ──→ COMPLETED
                     │
                     ├──→ CANCELLED (by officer)
                     └──→ ON_HOLD (pending hearing)

WfTask States:
  RAW ──→ PFA (Pending For Action) ──→ APR (Approved) ──→ ACL (Action Closed)
   │           │                            │
   │           ├──→ RJT (Rejected)          └──→ RMD (Remanded back)
   │           └──→ RSN (Reassigned)
   └──→ EXP (Expired — SLA breached)

Task Lifecycle Example (Appeal Case):

  1. Taxpayer files APL-01 (Appeal application)
     └── beforeCreateCase():
           ├── Generate ARN: ARN = litigationUtil.generateARN(stateCd)
           ├── Detect Model-2 state: appealUtil.isModel2State(stateCd)
           └── Set caseVO.setArnNo(arnNo)

  2. afterCreateCase():
     └── Create WfTask:
           ├── taskHandler.createTask(assignee, dueDt, caseId)
           ├── dueDt = workingDayCalc(today + 30, holidays[])
           ├── assignee = appealUtil.getAssigneeByJurisdiction(gstin)
           └── alertService.sendTaskAlert(assignee, caseId)

  3. Officer reviews case → updateTaskStatus(PFA → APR)
     └── WFServiceImpl.updateTaskStatus():
           ├── Update WfTask.taskStatus = "APR"
           ├── Insert WfTaskHistory row (audit trail)
           └── If final task → WfProcess.processStatus = "COMPLETED"

  4. If officer reassigns:
     └── WFServiceImpl.assignTask(ReassignVO):
           ├── Old task → status = RSN
           ├── New task created for new officer
           ├── Both changes in same @Transactional
           └── Alert sent to new assignee
```

### 4C. XA Transaction in Appeal Processing

```
YOUR ACTUAL FLOW (AppealEffectTranCustomizer.java):

  When an appeal ORDER is passed, THREE databases must update atomically:

  ┌─── Atomikos XA Transaction Manager ───────────────────────┐
  │                                                            │
  │  DB 1 (Litigation MySQL):                                  │
  │    UPDATE case SET status = 'ORDER_PASSED'                 │
  │    INSERT order_details (penalties, dates, paragraphs)     │
  │                                                            │
  │  DB 2 (Ledger MySQL):                                      │
  │    INSERT cash_ldgr_entry (debit/credit per order)         │
  │    UPDATE itc_balance (if ITC reversed/restored)           │
  │    INSERT liability_entry (demand adjustment)              │
  │                                                            │
  │  DB 3 (Workflow MySQL):                                    │
  │    UPDATE wf_task SET status = 'ACL'                       │
  │    INSERT wf_task_history (audit)                          │
  │    UPDATE wf_process SET status = 'COMPLETED'              │
  │                                                            │
  │  → If ANY fails → ALL rollback (2-Phase Commit)            │
  └────────────────────────────────────────────────────────────┘
  
  POST-COMMIT (async, non-transactional):
    → @Async sendCommunicationAsync(email to taxpayer)
    → @Async saveCommAuditAsync(audit trail)
    → Kafka event for downstream (search index, dashboard)
```

**Interview explanation:**
> "An appeal order affects three separate databases — litigation for the case, ledger for financial entries, and workflow for task completion. We can't have the ledger updated but the case still showing 'in-progress'. We use Atomikos XA transaction manager for 2-phase commit across all three. Email notifications are async (@Async) post-commit because notification failure shouldn't roll back a legal order."

### 4D. Working Day Calculator for SLA

```
Due date calculation (from AppealTranCaseCustomizer):

  Input:  todayDate, slaWorkingDays=30, state="27" (Maharashtra)
  
  Step 1: Fetch holiday list from cache
          holidays = distCacheUtil.getFromCache("HOLIDAY_" + stateCd)
  
  Step 2: Count working days (skip weekends + holidays)
          workingDaysCount = 0
          while (workingDaysCount < slaWorkingDays) {
              candidateDate = candidateDate.plusDays(1)
              if (!isWeekend(candidateDate) && !holidays.contains(candidateDate)) {
                  workingDaysCount++
              }
          }
  
  Step 3: dueDt = candidateDate
  
  Why cache holidays?
  → Holiday list changes once/year
  → 50K officers checking SLA = 50K cache hits vs 50K DB queries
  → Cache region: HOLIDAY_CACHE, TTL: 24 hours
```

---

## Step 5: Data Model

```sql
-- WfProcess (Workflow Process)
CREATE TABLE wf_process (
    process_id    BIGINT PRIMARY KEY AUTO_INCREMENT,
    arn_num       VARCHAR(30) UNIQUE,
    gstin         VARCHAR(15) NOT NULL,
    case_type     VARCHAR(10) NOT NULL,          -- AMYDT, APLTD, DCR, etc.
    process_status VARCHAR(20) DEFAULT 'INITIATED', -- INITIATED, IN_PROGRESS, COMPLETED
    created_by    VARCHAR(50),
    created_dt    TIMESTAMP,
    updated_dt    TIMESTAMP,
    INDEX idx_gstin (gstin),
    INDEX idx_status (process_status, case_type)
);

-- WfTask (Individual tasks within a process)
CREATE TABLE wf_task (
    task_id       BIGINT PRIMARY KEY AUTO_INCREMENT,
    process_id    BIGINT REFERENCES wf_process(process_id),
    task_type     VARCHAR(30),           -- HEARING, NOTICE, ORDER, REVIEW
    task_status   VARCHAR(10),           -- RAW, PFA, APR, ACL, RJT, RSN, EXP
    assigned_to   VARCHAR(50),           -- Officer user ID
    due_dt        DATE,                  -- SLA deadline
    is_complete   BOOLEAN DEFAULT FALSE,
    created_dt    TIMESTAMP,
    completed_dt  TIMESTAMP,
    INDEX idx_assignee (assigned_to, task_status),
    INDEX idx_due (due_dt, task_status)
);

-- WfTaskHistory (Audit trail)
CREATE TABLE wf_task_history (
    history_id    BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id       BIGINT,
    old_status    VARCHAR(10),
    new_status    VARCHAR(10),
    changed_by    VARCHAR(50),
    change_reason VARCHAR(500),
    changed_dt    TIMESTAMP
);
```

---

## Step 6: Key Tradeoffs

| Decision | Tradeoff | Why |
|----------|----------|-----|
| Strategy+Factory over inheritance | More classes vs flexible composition | 20+ types → deep inheritance = fragile. Strategy isolates change |
| MySQL over NoSQL for workflow | Limited scale vs ACID + complex queries | Officer dashboards need JOINs (process+task+assignee). Strong consistency needed |
| XA (Atomikos) over Saga | Blocking + slow vs strong consistency | Legal orders cannot be "compensated" — partial ledger update is illegal |
| Working-day calc in app vs DB | App CPU vs DB function | Holiday list cached in JDG → app calc is faster than DB query per task |
| Audit history table vs CDC | Storage overhead vs simpler implementation | Legal requirement needs explicit trail; CDC alone isn't queryable enough |

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 3: Design a Distributed Tax Ledger                             ║
# ║  (Dual-storage MySQL + HBase, 1.6B entries/year, financial consistency) ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Three ledger types: **Cash Ledger**, **ITC (Input Tax Credit) Ledger**, **Liability Ledger**
2. Credit operations: payment received, ITC claimed, refund credit
3. Debit operations: tax liability set-off, demand order, penalty
4. Balance inquiry: current balance per GSTIN per head (IGST/CGST/SGST/Cess)
5. Statement generation: complete history for a period range
6. Offset/settlement: ITC offsets liability in specific order (IGST → CGST → SGST)
7. Interest calculation: on late payment/filing
8. Dual-storage: MySQL (current state) + HBase (complete history)

### Non-Functional Requirements
- **Consistency**: Financial ledger = ZERO tolerance for inconsistency
- **Durability**: Every credit/debit MUST be persisted (legal evidence)
- **Audit**: Full trail — who, what, when, why for every entry
- **Scale**: 1.6B entries/year, 7-year retention = 11.2B rows in history
- **Performance**: Balance lookup < 100ms, statement generation < 3s

---

## Step 2: Scale Estimation

```
Annual filings:      400M
Ledger entries/filing: ~4 (ITC credit, cash debit, liability debit, cess)
Annual entries:       1.6B
7-year retention:     11.2B rows total

Entry size:           ~200 bytes (GSTIN, head, amount, date, type, ref)
Annual storage:       1.6B × 200B = 320 GB/year
7-year:               2.24 TB → HBase (compressed ~500 GB)

MySQL (current state): 14M GSTINs × 4 heads × 3 ledgers = 168M rows (~30 GB)

Peak writes:          During filing peak: 500 filings/sec × 4 entries = 2000 writes/sec
Balance reads:        14M GSTINs checking balance → cached heavily
```

---

## Step 3: Architecture — Dual Storage Design

```
                    ┌───────────────────┐
                    │  LedgerAPI /      │
                    │  PaymentAPI       │
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │  LedgerUtilFwk    │
                    │  Service Layer    │
                    └────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼                              ▼
     ┌─────────────────┐          ┌──────────────────┐
     │  MySQL (MASTER)  │          │  HBase (HISTORY)  │
     │                  │          │                    │
     │  cash_balance    │          │  cash_ldgr_hist    │
     │  itc_balance     │          │  itc_ldgr_hist     │
     │  liab_balance    │          │  liab_ldgr_hist    │
     │                  │          │                    │
     │  ┌─────────────┐ │          │  Row Key:          │
     │  │ GSTIN  HEAD │ │          │  {HASH}|{GSTIN}|   │
     │  │ IGST   5000 │ │          │  {PERIOD}|{TYPE}|  │
     │  │ CGST   3000 │ │          │  {TXNID}           │
     │  │ SGST   3000 │ │          │                    │
     │  └─────────────┘ │          │  Columns: amt,     │
     │                  │          │  dt, ref, head,     │
     │  ACID, JOINs,    │          │  cr_dr, who, why   │
     │  balance queries │          │                    │
     └─────────────────┘          │  Petabyte scale,   │
                                  │  range scans,      │
                                  │  7-year retention   │
                                  └──────────────────┘
```

### Your Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Current Balance | `CashBalEntity`, `ITCBalEntity` (MySQL) |
| Ledger Entries | `CashLdgrEntity`, `ITCLdgrEntity`, `DebitTransEntity` |
| Dual-storage Service | `TaxLedgrService.getDataFromHbase()` for history |
| Balance Query | `UtilizeFundsLedgServiceImpl.getITCBalance()`, `getCashBalance()` |
| Settlement | `UtilizeFundsServiceImpl.processPaymentUtilization()` |
| Offset Logic | `Gstr3UtilItcCshReq` — ITC/Cash utilization request |
| XA Transaction | Atomikos — `@Transactional(Propagation.REQUIRES_NEW)` |

---

## Step 4: Deep Dive

### 4A. Write Path — Credit/Debit Operation

```
When a return is filed (e.g., GSTR-3B):

  ┌─── @Transactional (XA if cross-DB) ──────────────────────┐
  │                                                            │
  │  Step 1: Calculate liability from return sections           │
  │    liab = calculateLiability(gstr3b.section3_1)            │
  │    → IGST: ₹10,000, CGST: ₹5,000, SGST: ₹5,000          │
  │                                                            │
  │  Step 2: Debit ITC ledger (offset liability)               │
  │    OFFSET ORDER (per GST law):                             │
  │      1. IGST ITC → against IGST liability                  │
  │      2. IGST ITC → against CGST liability                  │
  │      3. IGST ITC → against SGST liability                  │
  │      4. CGST ITC → against CGST liability                  │
  │      5. SGST ITC → against SGST liability                  │
  │                                                            │
  │    itcLedgerDAO.debit(gstin, "IGST", 10000, "OFFSET_3B")  │
  │    itcBalanceDAO.updateBalance(gstin, "IGST", -10000)      │
  │                                                            │
  │  Step 3: If ITC insufficient → debit Cash ledger            │
  │    remaining = liability - itcUtilized                      │
  │    cashLedgerDAO.debit(gstin, "CGST", remaining)           │
  │    cashBalanceDAO.updateBalance(gstin, "CGST", -remaining)  │
  │                                                            │
  │  Step 4: Clear liability                                    │
  │    liabLedgerDAO.credit(gstin, period, 0, "SETTLED")       │
  │                                                            │
  └────────────────────────────────────────────────────────────┘

  POST-COMMIT (async):
    → HBase write: GSTMutator.write(ledgerHistoryRecord)
    → Mirror propagation: GSTMutator.getPropogableInstance(primary, mirrors)
    → Kafka event: "LEDGER_UPDATED" topic
```

### 4B. Read Path — Balance vs History

```
┌─────────────────────────────────────────────────────────────┐
│  USE CASE 1: "What's my current ITC balance?"               │
│                                                              │
│  Path: API → Cache check → MySQL (if miss)                   │
│                                                              │
│  DistCacheUtil.getFromCache("LEDGER_CACHE", gstin + "_ITC") │
│    → Cache HIT (95%): Return cached balance                  │
│    → Cache MISS:                                             │
│         SELECT igst_bal, cgst_bal, sgst_bal, cess_bal        │
│         FROM itc_balance WHERE gstin = ?                     │
│         → Put in cache with TTL = 5 min                      │
│         → Return                                             │
│                                                              │
│  Latency: ~5ms (cache hit), ~50ms (DB hit)                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  USE CASE 2: "Show my cash ledger for Apr 2025 - Mar 2026"  │
│                                                              │
│  Path: API → HBase (range scan)                              │
│                                                              │
│  GSTReader reader = GSTReader.lookup(                        │
│      indexRowKey: {gstin_hash}|{gstin}|042025,               │
│      endRowKey:   {gstin_hash}|{gstin}|032026,               │
│      model: "cash_ldgr_hist",                                │
│      columns: [amt, dt, ref, head, cr_dr]                    │
│  );                                                          │
│  while (reader.hasNext()) {                                  │
│      DataRecord record = reader.next();  // Lazy loading     │
│      entries.add(map(record));                                │
│  }                                                           │
│  reader.close();  // Closeable resource management           │
│                                                              │
│  Latency: ~200ms for 12-month scan (~50 entries)             │
│  Latency: ~2s for 7-year full history (~300+ entries)        │
└─────────────────────────────────────────────────────────────┘
```

### 4C. Why Dual Storage?

```
                    MySQL                    HBase
─────────────────────────────────────────────────────────
Query type       Balance (point lookup)    History (range scan)
Data volume      168M rows (30 GB)         11.2B rows (500+ GB)
Access pattern   gstin + head → balance    gstin + period range → entries
Consistency      Strong (ACID)             Eventual (WAL + async)
JOINs needed?    Yes (balance + txn)       No (denormalized)
Retention        Current only              7 years
Update pattern   UPDATE balance in-place   APPEND-only (immutable)
Throughput       ~5K TPS (read-heavy)      ~50K writes/sec (batch)

TRADEOFF: We pay the cost of dual writes (MySQL + HBase) to get:
  ✓ Fast balance lookups (MySQL indexed)
  ✓ Infinite history retention (HBase auto-shards)
  ✓ Legal-grade audit trail (HBase immutable rows)
  ✓ Statement generation without impacting balance queries
```

---

## Step 5: Critical Scenarios

### Scenario A: Double-Debit Prevention
```
Problem: Network timeout → client retries → same debit applied twice

Solution (YOUR architecture):
  1. Each ledger operation has a unique txnRefId (idempotency key)
  2. Before debit: SELECT COUNT(*) FROM cash_ldgr WHERE txn_ref_id = ?
  3. If exists → skip (idempotent)
  4. If not → proceed with debit
  5. txnRefId in HBase row key: {hash}|{gstin}|{period}|{txn_ref_id}
     → HBase Put is idempotent by design (same row key = overwrite)
```

### Scenario B: Settlement/Reconciliation
```
Problem: MySQL balance and HBase history must agree

Solution:
  1. Nightly reconciliation batch job
  2. SUM(credits) - SUM(debits) from HBase for each GSTIN
  3. Compare with MySQL balance
  4. If mismatch → alert + auto-correct from HBase (source of truth for history)
  5. MySQL is "materialized view" — can be rebuilt from HBase
```

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 4: Design a Distributed Caching Layer                          ║
# ║  (70+ cache regions, 2-tier, 14M entities, sub-10ms lookups)           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Cache user sessions (OTP, CAPTCHA, login state)
2. Cache entity master data (GSTIN details, signatories, jurisdiction)
3. Cache return filing status and transaction state
4. Cache reference data (tax rates, HSN codes, state codes, holidays)
5. Support TTL-based expiry AND idle-based expiry
6. Support 70+ logically separated cache regions

### Non-Functional Requirements
- **Latency**: < 5ms for cache hit (p99)
- **Scale**: 14M GSTINs cached, 500K concurrent sessions
- **Availability**: Cache failure must NOT take down the system (fallback to DB)
- **Consistency**: Eventual (cache-aside with TTL)
- **Operations**: Cache invalidation, bulk eviction, cluster rebalancing

---

## Step 2: Architecture — 2-Tier Design

```
YOUR ACTUAL ARCHITECTURE:

  ┌──────────────────────────────────────────────────────────┐
  │                    Application Server                     │
  │                                                          │
  │  ┌─────────────────────────────────────────────────┐     │
  │  │         TIER 1: EhCache (Local / In-JVM)        │     │
  │  │                                                  │     │
  │  │  • Tax rates, HSN codes, state codes             │     │
  │  │  • Reference data that NEVER changes mid-day     │     │
  │  │  • ~50 MB heap per instance                      │     │
  │  │  • TTL: 24 hours (or until server restart)       │     │
  │  │  • Latency: < 1ms (no network hop)               │     │
  │  └───────────────────────┬─────────────────────────┘     │
  │                          │ MISS                           │
  │                          ▼                                │
  │  ┌─────────────────────────────────────────────────┐     │
  │  │    TIER 2: Infinispan / JDG (Distributed)       │     │
  │  │                                                  │     │
  │  │  • User sessions, OTP, CAPTCHA                   │     │
  │  │  • Entity details (GSTIN, signatory)             │     │
  │  │  • Filing status, transaction state              │     │
  │  │  • Ledger balances (short TTL)                   │     │
  │  │  • HotRod protocol (binary, TCP)                 │     │
  │  │  • Latency: 2-5ms (one network hop)              │     │
  │  │  • 70+ named cache regions                       │     │
  │  │  • CLUSTER_A: sessions + entity (25 regions)     │     │
  │  │  • CLUSTER_B: returns + ledger (15 regions)      │     │
  │  └───────────────────────┬─────────────────────────┘     │
  │                          │ MISS                           │
  └──────────────────────────┼───────────────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  MySQL / HBase   │
                    │  (Source of Truth)│
                    └─────────────────┘
```

### Your Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Cache Utility | `DistCacheUtil` (400+ methods) — `addToCache()`, `getFromCache()`, `removeFromCache()` |
| Cache Store | `DistCacheStore` — Infinispan `RemoteCacheManager` (HotRod) |
| Local Cache | `CacheStore` — EhCache fallback |
| TTL Support | `addToCache(key, value, expiryTimeMinutes)` |
| Idle TTL | `addToCacheWithIdleTime()` — dual expiry (max life + idle timeout) |
| Existence Check | `isExists(key)` — used for distributed locking / dedup |

---

## Step 3: Deep Dive — Cache Region Design

### 70+ Cache Regions Categorized:

```
SESSION CACHES (TTL: 30 min, idle: 15 min):
  ├── OTP_CACHE              — OTP for EVC verification
  ├── CAPTCHA_CACHE          — CAPTCHA challenge-response
  ├── PRE_LOGIN_USR_DATA_CACHE — Pre-auth user context
  └── USER_JURS_CACHE        — User jurisdiction mapping

ENTITY CACHES (TTL: 1 hour):
  ├── ENTITY_DETAILS_CACHE   — Full GSTIN registration data
  ├── GSTIN_DTLS_CACHE       — GSTIN status, trade name, type
  ├── GSTIN_SIGNATORY_DTLS_CACHE — Authorized signatories
  └── ENTITY_PAN_CACHE       — PAN-GSTIN mapping

RETURN CACHES (TTL: 5 min):
  ├── RET_INVOICE_PAYLOAD_CACHE   — Invoice data being edited
  ├── RET_BULK_PAYLOAD_CACHE      — Bulk upload data
  ├── RETURN_STATUS_TRACK_CACHE   — Filing status per GSTIN
  └── RETURN_SUBMIT_STATUS_CACHE  — Submit vs Filed status

LEDGER CACHES (TTL: 5 min):
  ├── LEDGER_CACHE            — Current balance (invalidated on update)
  ├── RET_SET_OFF_CACHE       — ITC offset calculation
  └── DEMAND_CACHE            — Outstanding demand per GSTIN

TRANSACTION CACHES (TTL: 10 min):
  ├── API_TRANSACTION_CACHE   — Duplicate request prevention
  └── ASYNC_REQ_STATUS_CACHE  — Async job completion tracking

CASE MGMT CACHES (TTL: 30 min):
  ├── CASEMGMT_DATA_CACHE     — Case details
  ├── CASE_ASSND_DTLS_CACHE   — Officer assignment data
  └── HOLIDAY_CACHE           — Holiday list per state (TTL: 24h)

MASTER DATA (EhCache, TTL: 24h):
  ├── TAX_RATE_CACHE          — GST rates per HSN chapter
  ├── HSN_CODE_CACHE          — HSN/SAC code master
  ├── STATE_CODE_CACHE        — State/UT codes
  └── NOTIFICATION_CACHE      — Government notification dates
```

### Cache-Aside Pattern Implementation:

```java
// YOUR ACTUAL PATTERN (DistCacheUtil usage across codebase):

public GstinDetails getGstinDetails(String gstin) {
    // Step 1: Check cache
    String cacheKey = "GSTIN_" + gstin;
    GstinDetails cached = (GstinDetails) distCacheUtil
        .getFromCache("GSTIN_DTLS_CACHE", cacheKey);
    
    if (cached != null) {
        return cached;  // Cache HIT (~95% of requests)
    }
    
    // Step 2: Cache MISS → query DB
    GstinDetails fromDb = gstinDAO.findByGstin(gstin);
    
    // Step 3: Populate cache with TTL
    distCacheUtil.addToCache("GSTIN_DTLS_CACHE", cacheKey, fromDb, 60);
    // ← 60 minutes TTL
    
    return fromDb;
}

// For transient data (OTP):
distCacheUtil.addToCacheInSeconds("OTP_CACHE", otpKey, otpValue, 300);
// ← 300 seconds (5 minutes) TTL

// For session-like data (dual TTL):
distCacheUtil.addToCacheWithIdleTime("SESSION_CACHE", sessKey, session, 
    30,   // max life: 30 minutes
    15    // idle timeout: 15 minutes (reset on access)
);
```

### Distributed Lock via Cache:

```java
// YOUR ACTUAL PATTERN (using isExists + addToCache):

public boolean acquireLock(String resourceId, int lockDurationSeconds) {
    String lockKey = "LOCK_" + resourceId;
    
    // Check if lock exists
    if (distCacheUtil.isExists("API_TRANSACTION_CACHE", lockKey)) {
        return false;  // Already locked → prevent duplicate processing
    }
    
    // Acquire lock with auto-expiry
    distCacheUtil.addToCacheInSeconds(
        "API_TRANSACTION_CACHE", lockKey, "LOCKED", lockDurationSeconds
    );
    return true;
}

// Used for:
// 1. Preventing duplicate return filing (same GSTIN + period)
// 2. Preventing concurrent case updates by two officers
// 3. Preventing double-payment for same challan
```

---

## Step 4: Bottlenecks & Solutions

| Bottleneck | Solution |
|-----------|---------|
| Cache stampede (many requests on cold key) | Lock-based cache loading: first request acquires lock, loads from DB; others wait |
| Stale data after DB update | Short TTL (5 min for ledger) + explicit invalidation on write path |
| JDG cluster node failure | Infinispan replication: 2 owners per key (consistent hashing) |
| EhCache inconsistency across servers | Only static/reference data in EhCache; never mutable state |
| Memory pressure (70 regions) | Cluster split: CLUSTER_A (session-heavy) vs CLUSTER_B (data-heavy) |
| Hot key (popular GSTIN) | Client-side EhCache tier absorbs hot reads before JDG |

---

## Step 5: Key Tradeoffs

| Decision | Tradeoff | Why |
|----------|----------|-----|
| JDG over Redis | Less ecosystem, harder ops vs JBoss-native, Java-native HotRod | JBoss/Wildfly stack — seamless integration, no extra sidecar |
| 2-tier over single tier | Complexity vs performance | Static data costs 0 network hops with EhCache |
| TTL over explicit invalidation | Stale window vs complexity | For 70 regions, tracking invalidation points is unmaintainable |
| Cache-aside over write-through | Extra code vs auto-population | Write-through populates cache with data that may never be read |
| Separate clusters (A/B) | Operational overhead vs isolation | Session spike (login surge) shouldn't impact ledger cache |

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 5: Design an Async Event Processing Pipeline                   ║
# ║  (Kafka + Error Topics + DLQ + Scheduled Retry)                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Asynchronous processing of events: filing, payment, ledger update, notification
2. Multiple consumer groups processing same event for different concerns
3. Failed messages → error topic (not lost forever)
4. Scheduled retry of error topic messages (configurable time window)
5. Permanently failed messages → Dead Letter Queue (DLQ)
6. Monitoring: consumer lag, error rates, DLQ depth

### Non-Functional Requirements
- **Durability**: Zero message loss (acks=all)
- **Ordering**: Per-partition ordering (partition by GSTIN)
- **Throughput**: 2000+ events/sec during peak
- **Latency**: < 5s end-to-end for critical paths (ledger)
- **Retry**: Configurable retry count and delay

---

## Step 2: Architecture — 3-Tier Error Handling

```
YOUR ACTUAL ARCHITECTURE (Consumer.java + ProducerService.java):

  ┌──────────────────────────────────────────────────────────────┐
  │                    KAFKA CLUSTER (20+ partitions)            │
  └──────────────────────────┬───────────────────────────────────┘
                             │
  ┌──────────────────────────▼───────────────────────────────────┐
  │                    MAIN TOPIC                                 │
  │  e.g., GSTR3B_FILING, LEDGER_UPDATE, CASE_CREATED           │
  │                                                               │
  │  Consumer loop (ConsumerService.java):                        │
  │    while(true) {                                              │
  │      records = consumer.poll(1000ms)                          │
  │      for (record : records) {                                 │
  │        ProcessorThread thread = new ProcessorThread(          │
  │            processor,   // ← pluggable business logic        │
  │            message,                                           │
  │            this         // ← acker reference                  │
  │        );                                                     │
  │        do {                                                   │
  │          future = poolExecutor.submit(thread);                │
  │          resultMap.put(topic|partition|offset, future);       │
  │        } while(RejectedExecutionException);                   │
  │          // ↑ Retry on full thread pool (back-pressure)       │
  │      }                                                        │
  │      msLastPolled = now();  // 18-sec heartbeat tracking      │
  │    }                                                          │
  │                                                               │
  │  On FAILURE:                                                  │
  │    → ProducerService.produceMessage(failedMsg, errorTopics)   │
  │    → Synchronous send: future.get() (blocking until ack)      │
  │    → Logs: topic, partition, offset of error message          │
  └──────────┬────────────────────────────────────────────────────┘
             │ Failed messages
             ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                    ERROR TOPIC                                │
  │  e.g., GSTR3B_FILING_ERROR                                   │
  │                                                               │
  │  Scheduled consumption (NOT real-time):                       │
  │    scheduleErrorTopicConsumptionAt(                            │
  │      startHr: 2,      // Start at 2:00 AM                    │
  │      startMin: 0,                                             │
  │      startSec: 0,                                             │
  │      period: 3600,    // Every 1 hour                         │
  │      stopInSecs: 1800, // Process for 30 min, then pause     │
  │      maxRetryCount: 3, // Max 3 retry attempts                │
  │      secondaryErrorTopics: [DLQ_TOPIC]                        │
  │    );                                                         │
  │                                                               │
  │  Logic:                                                       │
  │    1. ScheduledExecutorService.scheduleAtFixedRate()           │
  │    2. Calculate next scheduled time                            │
  │    3. If time has passed today → schedule for tomorrow         │
  │    4. Process error messages with same Processor               │
  │    5. If still fails after maxRetry → push to DLQ             │
  └──────────┬────────────────────────────────────────────────────┘
             │ Permanently failed (after 3 retries)
             ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                    DEAD LETTER QUEUE (DLQ)                    │
  │  e.g., GSTR3B_FILING_DLQ                                     │
  │                                                               │
  │  Manual intervention:                                         │
  │    → Operations team reviews                                  │
  │    → Fixes root cause (data issue, downstream dependency)     │
  │    → Replays messages from DLQ                                │
  │    → OR archives as permanently failed with audit trail       │
  └──────────────────────────────────────────────────────────────┘
```

### Your Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Consumer Framework | `Consumer.java` — 2 constructors (basic + error topic) |
| Consumer Loop | `ConsumerService.java` — poll + thread pool + acker |
| Thread Pool | `ThreadPoolConfig` — poolCoreSize, poolMaxSize, keepAliveMs |
| Processor Interface | PluggableProcessor — business logic per topic |
| Error Topic Retry | `Consumer.scheduleErrorTopicConsumptionAt()` |
| Producer | `ProducerService.java` — sync send with `future.get()` |
| Heartbeat | `msLastPolled` — 18-second tracking to prevent rebalance |

---

## Step 3: Deep Dive — Thread Pool Design

```
YOUR ACTUAL THREAD POOL ARCHITECTURE:

  ┌──────────────────────────────────────────────────────┐
  │            Consumer Thread (Main Loop)                │
  │                                                       │
  │  Kafka poll() every 1 second                          │
  │     │                                                 │
  │     ▼                                                 │
  │  For each record:                                     │
  │     ├── Create ProcessorThread(processor, msg, this)  │
  │     ├── Submit to ThreadPoolExecutor                  │
  │     │     ├── Core: 10 threads                        │
  │     │     ├── Max: 50 threads                         │
  │     │     ├── Keep-alive: 60s                         │
  │     │     └── Queue: SynchronousQueue (no buffering)  │
  │     │                                                 │
  │     └── If RejectedExecutionException:                │
  │           └── Retry in tight loop (back-pressure)     │
  │               → Consumer stops polling                │
  │               → Kafka heartbeat maintained via        │
  │                 msLastPolled tracking                  │
  │                                                       │
  │  Acker Thread (parallel):                             │
  │     └── Every msAckerInterval:                        │
  │           ├── Iterate resultMap                        │
  │           ├── future.isDone()? → commit offset         │
  │           ├── future.get() == false? → error topic     │
  │           └── Remove from map                          │
  └──────────────────────────────────────────────────────┘

  WHY SynchronousQueue (not LinkedBlockingQueue)?
    → With LinkedBlockingQueue: messages buffer silently → OOM risk
    → With SynchronousQueue: immediate backpressure → consumer pauses polling
    → This is a CONSCIOUS DESIGN choice for bounded resource usage
```

### Back-Pressure Mechanism:

```
Normal flow (pool not saturated):
  poll() → submit() → success → poll() → submit() → ...
  Throughput: ~500 msg/sec

Back-pressure (pool saturated — all 50 threads busy):
  poll() → submit() → RejectedExecution! 
         → retry submit (tight loop)
         → no new poll() until thread frees up
         → Kafka sees no poll() but heartbeat OK (18-sec window)
         → Eventually thread completes → submit succeeds → resume

  Effect: Consumer auto-throttles to processing capacity
  No message loss, no OOM, no rebalance (within heartbeat window)
```

---

## Step 4: Key Tradeoffs

| Decision | Tradeoff | Why |
|----------|----------|-----|
| Custom framework over Spring Kafka | More code to maintain vs full control | Spring Kafka's error handling didn't support scheduled retry at that time |
| SynchronousQueue over LinkedBlockingQueue | Lower throughput vs bounded memory | Government system: predictability > peak throughput |
| Sync producer (future.get()) over async | Higher latency vs guaranteed delivery | Error topic message MUST NOT be lost — blocking is acceptable |
| Scheduled retry over immediate retry | Delayed processing vs DB/service recovery time | If MySQL is down, retrying immediately is useless; wait for recovery |
| 3-tier (main/error/DLQ) over 2-tier | More operational complexity vs clear escalation | Transient errors (timeout) need retry; permanent errors (bad data) need human |

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 6: Design a Notification System                                ║
# ║  (Email + SMS, template-driven, async, audit trail)                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Send transactional notifications: filing confirmation, demand notice, order copy
2. Support Email and SMS channels
3. Template-driven: dynamic variable substitution (taxpayer name, ARN, amount)
4. Bulk notification support (e.g., remind all non-filers)
5. Complete audit trail (what was sent, to whom, when, delivery status)
6. User preferences (opt-in/opt-out per channel)

### Non-Functional Requirements
- **Delivery**: At-least-once (retry on failure)
- **Latency**: < 30s for transactional, < 1 hour for bulk
- **Scale**: 14M potential recipients, 5M+ notifications/day during deadlines
- **Audit**: Legal compliance — proof of notice delivery

---

## Step 2: Architecture

```
                    ┌──────────────────────────┐
                    │  Any API Service          │
                    │  (Filing, Case, Payment)  │
                    └────────────┬──────────────┘
                                 │
                    @Async sendCommunicationAsync(payload)
                                 │
                    ┌────────────▼──────────────┐
                    │  CommunicationService      │
                    │  (Core-API/CommunicationAPI)│
                    │                             │
                    │  Step 1: getCommData(tempId) │ ← Fetch template
                    │    → CommMstr entity         │   from cache/DB
                    │    → subject, body template  │
                    │                             │
                    │  Step 2: getDBTemplateData() │ ← FreeMarker render
                    │    → ${taxpayerName} → "ABC" │
                    │    → ${arnNo} → "ARN123"     │
                    │    → ${amount} → "₹50,000"   │
                    │                             │
                    │  Step 3: sendCommunication() │ ← Dispatch
                    │    ├── EmailUtil.send()       │
                    │    └── SMSUtil.send()         │
                    │                             │
                    │  Step 4: saveCommAuditAsync()│ ← Audit trail
                    │    → CommAudtEntity           │
                    │    → who, what, when, status  │
                    └─────────────────────────────┘
```

### Your Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Service Interface | `CommunicationService` — `sendCommunication()`, `sendCommunicationAsync()` |
| Template Entity | `CommMstr` — template ID, subject, body, channel |
| Template Engine | FreeMarker — `${variable}` syntax |
| Bulk Support | `storeBulkCommDetails(BulkComm)` → batch ID |
| Audit Entity | `CommAudtEntity` — what, when, to whom, status |
| User Prefs | `UserCommEntity` — channel preferences |
| Template DAO | `CommMstrDataDao` (templates), `CommAudtDataDao` (audit) |

---

## Step 3: Deep Dive — Template Engine

```
Template Storage (CommMstr):
  ┌──────────────────────────────────────────────────────────────┐
  │ template_id │ channel │ subject              │ body          │
  │─────────────│─────────│──────────────────────│───────────────│
  │ FILING_ACK  │ EMAIL   │ Return Filed - ${ret}│ Dear ${name}, │
  │             │         │                      │ Your ${ret}   │
  │             │         │                      │ for period    │
  │             │         │                      │ ${period} has │
  │             │         │                      │ been filed.   │
  │             │         │                      │ ARN: ${arn}   │
  │─────────────│─────────│──────────────────────│───────────────│
  │ FILING_ACK  │ SMS     │ (N/A)                │ GST: ${ret}   │
  │             │         │                      │ filed for     │
  │             │         │                      │ ${period}.    │
  │             │         │                      │ ARN: ${arn}   │
  │─────────────│─────────│──────────────────────│───────────────│
  │ DEMAND_NTC  │ EMAIL   │ Demand Notice -      │ Dear ${name}, │
  │             │         │ ${gstin}             │ A demand of   │
  │             │         │                      │ ₹${amount}... │
  └──────────────────────────────────────────────────────────────┘

Runtime Rendering:
  CommPayload payload = new CommPayload();
  payload.put("name", "Jayanti Vishnoi");
  payload.put("ret", "GSTR-3B");
  payload.put("period", "Dec 2025");
  payload.put("arn", "ARN20251200000001");

  String rendered = commService.getDBTemplateData(templateData, payload);
  // Output: "Dear Jayanti Vishnoi, Your GSTR-3B for period Dec 2025 has been filed. ARN: ARN20251200000001"
```

### Bulk Notification Flow:

```
Use case: Remind 2M non-filers 3 days before GSTR-3B deadline

  Step 1: BackOffice generates non-filer list
          SELECT gstin, email, mobile FROM entity
          WHERE gstin NOT IN (SELECT gstin FROM return_status
                             WHERE ret_type='GSTR3B' AND period='122025')

  Step 2: storeBulkCommDetails(BulkComm bulkComm)
          → Returns batchId
          → Inserts metadata: batchId, templateId, totalCount, status=QUEUED

  Step 3: Kafka producer pushes 2M messages
          Topic: BULK_NOTIFICATION
          Message: {batchId, gstin, email, mobile, templateId, variables}
          Partitioned by: gstin.hashCode() % 20 partitions

  Step 4: 20 consumer threads pick up messages in parallel
          Each thread: render template → send email/SMS → audit
          Throughput: 20 threads × 10 msg/sec = 200 notifications/sec
          2M / 200 = 10,000 seconds ≈ 2.8 hours

  Step 5: Audit: CommAudtEntity per notification
          → Track delivery status (SENT, FAILED, BOUNCED)
          → Dashboard shows batch progress
```

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 7: Design an E-Invoice System                                 ║
# ║  (IRN generation, QR codes, digital signatures, IRP integration)       ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Generate IRN (Invoice Reference Number) — unique per invoice across India
2. Generate QR code containing IRN + digital signature
3. Validate invoice schema (JSON Schema)
4. Support Digital Signature Certificate (DSC) and Electronic Verification Code (EVC)
5. Store invoice data for retrieval (per GSTIN, per period)
6. Integrate with IRP (Invoice Registration Portal) for national registry
7. Batch generation (Excel upload for bulk invoices)

### Non-Functional Requirements
- **Uniqueness**: IRN must be globally unique (collision = legal issue)
- **Integrity**: QR code contains cryptographic signature (tamper-proof)
- **Scale**: 3B+ invoices/year → ~10K IRN generations/sec during peak
- **Storage**: Invoice XML/JSON + QR binary = ~10 KB/invoice × 3B = 30 TB/year
- **Compliance**: Government-mandated format (GSTN schema v1.1)

---

## Step 2: Architecture

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  Taxpayer    │     │  GSP (API    │     │  ERP System  │
  │  Portal      │     │  Partners)   │     │  (Tally/SAP) │
  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  EinvoiceAPI     │
                    │  (REST + Batch)  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────────────┐
              ▼              ▼                       ▼
     ┌──────────────┐ ┌───────────┐        ┌──────────────┐
     │  Schema      │ │  IRN Gen  │        │  QR Code     │
     │  Validator   │ │  Service  │        │  Generator   │
     │  (JSON       │ │           │        │  (IRN +      │
     │  Schema)     │ │  UUID +   │        │  DigSig)     │
     └──────────────┘ │  Hash     │        └──────┬───────┘
                      └─────┬─────┘               │
                            │                     │
                    ┌───────▼─────────────────────▼───┐
                    │          Dual Storage            │
                    │                                  │
                    │  MySQL           HBase            │
                    │  ├ IRN metadata   ├ Invoice JSON  │
                    │  ├ Status         ├ QR binary     │
                    │  ├ Timestamps     ├ Full payload  │
                    │  └ Index (search) └ Row: GSTIN|   │
                    │                     period|IRN    │
                    └──────────────────────────────────┘
```

### Your Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Service | `EInvoiceServiceImpl` — `generateFileDetails()`, `getEInvoice()` |
| IRN Generation | Part of `generateFileDetails(gstin, retPeriod, retType, flag, fileType)` |
| QR Code | `QRHelperResponseModel` — IRN + digital signature in QR |
| Schema Validation | `JsonSchemaFactory` + `ProcessingReport` |
| DSC Verification | `DscEvcValidation` |
| HBase DAO | `EinvoiceHbaseDao` — invoice payload, QR binary |
| MySQL DAO | `EInvoiceCoreDAO` — metadata, `EInvoiceReturnDAO` — return invoices |
| Batch | `BatchDAO` — Excel upload batch processing |
| Error Handling | `EInvoiceException`, `EInvoiceErrorCodes` enum → HTTP status mapping |

---

## Step 3: Deep Dive

### IRN Generation + QR Code Flow:

```
  EInvoiceServiceImpl.generateFileDetails(gstin, retPeriod, retType, flag, fileType):

  Step 1: VALIDATE SCHEMA
    JsonSchema schema = JsonSchemaFactory.byDefault().getJsonSchema(schemaNode)
    ProcessingReport report = schema.validate(invoiceJsonNode)
    if (!report.isSuccess()) → throw EInvoiceException(INVALID_SCHEMA)

  Step 2: VALIDATE SIGNATURE
    DscEvcValidation.validate(invoicePayload, authToken)
    → DSC: X.509 Class 3 certificate chain validation
    → EVC: OTP-based electronic verification code

  Step 3: GENERATE IRN
    IRN = SHA256(supplier_gstin + doc_type + doc_no + financial_year)
    → Deterministic: same invoice always gets same IRN
    → Collision-free: SHA256 + unique doc_no per supplier
    → Example: "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7b8c9d0..."

  Step 4: GENERATE QR CODE
    QR Content = {
      "irn": "a1b2c3d4...",
      "sellerGstin": "27AABCU9603R1ZM",
      "buyerGstin": "29AABCU9603R1ZN",
      "docNo": "INV-2025-001",
      "docDate": "19-03-2026",
      "totalValue": 118000,
      "items": 3,
      "signature": RSA_SIGN(irn, privateKey)  // Tamper-proof
    }
    QR binary = QRCodeGenerator.encode(content, UTF-8)
    Base64 QR = Base64.encode(qrBinary)

  Step 5: PERSIST (DUAL STORAGE)
    MySQL (EInvoiceCoreDAO):
      INSERT INTO einvoice_master (irn, gstin, doc_no, status, created_dt)
    
    HBase (EinvoiceHbaseDao):
      GSTMutator.write({
        rowKey: {gstin_hash}|{gstin}|{period}|{irn},
        columns: {invoice_json, qr_binary, signature, timestamp}
      })

  Step 6: KAFKA EVENT
    Topic: EINVOICE_GENERATED
    → Downstream: Return auto-population, analytics, IRP sync
```

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 8: Design an Authentication & Authorization System             ║
# ║  (LDAP + OTP + Risk-Based Auth + RBAC for 50K+ officers)              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Step 1: Clarify Requirements

### Functional Requirements
1. Login via LDAP credentials (50K tax officers, 14M taxpayer users)
2. Two-factor auth: password + OTP (SMS)
3. Risk-based authentication (device, location, behavior analysis)
4. CAPTCHA verification (anti-bot)
5. Role-based access control (RBAC): officer roles → allowed API endpoints
6. Session management: token-based, cache-backed, idle timeout
7. Single sign-on for back-office applications

### Non-Functional Requirements
- **Security**: OWASP Top 10 compliant, encryption at rest and transit
- **Scale**: 50K concurrent officer sessions, 500K taxpayer sessions
- **Availability**: Auth failure = entire platform down → 99.99%
- **Latency**: Login < 2s, token validation < 10ms

---

## Step 2: Architecture

```
  ┌──────────┐                              ┌──────────────┐
  │  Browser  │ ────── HTTPS ──────────────▶│  API Gateway  │
  └──────────┘                              │  (Rate Limit) │
                                            └──────┬───────┘
                                                   │
                                   ┌───────────────┼───────────────┐
                                   ▼               ▼               ▼
                         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
                         │ TokenAuth    │ │ DatabaseAuth │ │ Public       │
                         │ Filter       │ │ Manager      │ │ Endpoints    │
                         │ (every req)  │ │ (RBAC check) │ │ (no auth)    │
                         └──────┬───────┘ └──────┬───────┘ └──────────────┘
                                │                │
                     ┌──────────▼────────────────▼──────────┐
                     │         Authentication Flow           │
                     │                                       │
                     │  1. CAPTCHA verify (CaptchaCache)     │
                     │  2. LDAP authenticate                 │
                     │  3. Risk assessment (Arcot RiskPoint) │
                     │  4. OTP generate + send SMS           │
                     │  5. OTP verify                        │
                     │  6. Create session → JDG cache        │
                     │  7. Return auth token                 │
                     └──────────┬────────────────────────────┘
                                │
                     ┌──────────▼────────────────────────────┐
                     │         Authorization (per request)    │
                     │                                        │
                     │  TokenAuthenticationFilter:             │
                     │    1. Extract token from header         │
                     │    2. SessionCacheUtil.isSessionValid() │
                     │    3. Load GstUserDetails from cache    │
                     │    4. Update lastActivityTimestamp      │
                     │    5. Set SecurityContext                │
                     │                                        │
                     │  DatabaseAuthorizationManager:           │
                     │    1. Extract user session               │
                     │    2. Get request URL                    │
                     │    3. roleAuthorizationUtil              │
                     │       .checkRoleBasedAccess(session,url) │
                     │    4. Return AuthorizationDecision       │
                     └────────────────────────────────────────┘
```

### Your Codebase Mapping:
| Component | Actual Class |
|-----------|-------------|
| Auth Service | `Authentication2ServiceImpl` — `authenticateUserFromLDAP()`, `validateUserOTP()` |
| Token Filter | `TokenAuthenticationFilter` (OncePerRequestFilter) |
| User Details | `GstUserDetailsService` implements `UserDetailsService` |
| Authorization | `DatabaseAuthorizationManager` implements `AuthorizationManager` |
| Security Config | `SecurityConfig` — `@ConditionalOnProperty("gst.security.fo.enabled")` |
| LDAP | `AuthenticationLdapUtil` |
| OTP | `OtpUtil` — generate + send via SMS |
| Risk Assessment | `RBAHelperUtil` — Arcot RiskPoint SDK |
| Session Cache | `SessionCacheUtil.isSessionValid()` + `DistCacheUtil` |
| Role Check | `RoleAuthorizationUtil.checkRoleBasedAccess(session, url)` |

---

## Step 3: Deep Dive — Session Management

```
Session Storage in JDG (Infinispan):

  Cache Region: USER_SESSION_CACHE
  Key: authToken (UUID-based, 128-bit)
  Value: Map<String, String>
    {
      "userId": "jayanti.vishnoi",
      "gstin": "27AABCU9603R1ZM",
      "role": "TAX_OFFICER",
      "jurisdiction": "MH_MUMBAI_CENTRAL",
      "loginTime": "2026-03-19T10:30:00",
      "lastActivity": "2026-03-19T11:45:00",
      "deviceFingerprint": "a3f2c1...",
      "riskScore": "LOW"
    }
  TTL: 30 minutes (max session life)
  Idle: 15 minutes (reset on each request)

Token Validation Flow (per request):

  Request → TokenAuthenticationFilter.doFilterInternal()
    │
    ├── Extract token: request.getHeader("Authorization")
    ├── If null → pass to next filter (might be public endpoint)
    │
    ├── GstUserDetailsService.loadUserByUsername(authToken)
    │     ├── SessionCacheUtil.isSessionValid(authToken)
    │     │     └── distCacheUtil.getFromCache("USER_SESSION_CACHE", token)
    │     │           → If null → session expired/invalid → 401
    │     │           → If found → continue
    │     │
    │     ├── Update lastActivity timestamp in cache
    │     │     └── distCacheUtil.addToCache("USER_SESSION_CACHE", token, 
    │     │           updatedSession, 30)  // Reset TTL
    │     │
    │     └── Return GstUserDetails (wraps FoUserSession)
    │
    ├── DatabaseAuthorizationManager.check()
    │     ├── Extract URL: /api/v1/returns/gstr3b/file
    │     ├── Extract role: TAX_OFFICER
    │     ├── roleAuthorizationUtil.checkRoleBasedAccess()
    │     │     └── DB lookup: SELECT allowed FROM role_url_mapping
    │     │           WHERE role = ? AND url LIKE ?
    │     │     └── Cached in ROLE_CACHE for performance
    │     │
    │     └── Return AuthorizationDecision(allowed / denied)
    │
    └── If authorized → proceed to controller
        If denied → 403 Forbidden (JSON response)
```

### RBAC Model:

```sql
-- Role hierarchy
CREATE TABLE roles (
    role_id     VARCHAR(30) PRIMARY KEY,    -- TAX_OFFICER, SUPERINTENDENT, COMMISSIONER
    role_name   VARCHAR(100),
    parent_role VARCHAR(30) REFERENCES roles(role_id)  -- Hierarchy
);

-- URL-Pattern to Role mapping
CREATE TABLE role_url_mapping (
    role_id     VARCHAR(30),
    url_pattern VARCHAR(200),    -- /api/v1/cases/**
    http_method VARCHAR(10),     -- GET, POST, PUT, DELETE
    allowed     BOOLEAN,
    PRIMARY KEY (role_id, url_pattern, http_method)
);

-- Examples:
-- TAX_OFFICER   | /api/v1/cases/**       | GET  | true  (can view cases)
-- TAX_OFFICER   | /api/v1/cases/*/order  | POST | false (cannot pass orders)
-- SUPERINTENDENT| /api/v1/cases/*/order  | POST | true  (can pass orders)
-- COMMISSIONER  | /api/v1/cases/**       | *    | true  (full access)
```

---

## Step 4: Key Tradeoffs

| Decision | Tradeoff | Why |
|----------|----------|-----|
| LDAP over OAuth2 | No federated login vs enterprise-grade, existing infrastructure | Government network: all employees in LDAP, no third-party IdP needed |
| Cache-backed sessions over JWT | Network hop per request vs revocation support | Need instant session revocation (officer suspended = immediate lockout) |
| Database RBAC over annotation-based | DB query per request vs compile-time safety | 50K officers, roles change by government order — can't redeploy for role change |
| Risk-based auth before OTP | Extra latency vs reduced OTP spam | If risk=HIGH (unknown device+location), challenge with CAPTCHA before SMS OTP |
| Conditional security config | Feature toggling complexity vs backward compatibility | `@ConditionalOnProperty` — old modules on Spring 4 don't enable security filter |

---

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  BONUS: HOW TO PRESENT IN AN INTERVIEW                                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## System Design Answer Framework (Use for ALL 8 problems above)

```
TIME ALLOCATION (45-minute system design round):

  Minutes 0-5:   CLARIFY requirements (ask 3-5 questions)
  Minutes 5-10:  ESTIMATE scale (back-of-envelope math)
  Minutes 10-20: HIGH-LEVEL ARCHITECTURE (draw boxes + arrows)
  Minutes 20-35: DEEP DIVE into 2-3 components (interviewer picks)
  Minutes 35-40: BOTTLENECKS & SOLUTIONS
  Minutes 40-45: TRADEOFFS & ALTERNATIVES

KEY PHRASES TO USE:
  ✓ "In my experience at GSTN, we solved this by..."
  ✓ "We evaluated X vs Y and chose Y because..."
  ✓ "The tradeoff we accepted was..."
  ✓ "At our scale of 14M entities and 500M transactions/year..."
  ✓ "One bottleneck we hit was... and we solved it with..."
  ✓ "If I were designing this from scratch today, I'd also consider..."
```

## Quick Reference — Pattern-to-Problem Mapping

```
┌─────────────────────────┬───────────────────────────────────────────────┐
│  DESIGN PATTERN         │  WHERE YOU USED IT                            │
├─────────────────────────┼───────────────────────────────────────────────┤
│  Strategy + Factory     │  CaseCustomizerFactory (20+ case types)       │
│  Template Method        │  ReturnFilingEngine (10+ return types)        │
│  Builder                │  HBase RowKey construction (15 components)    │
│  Decorator              │  UserSwitchedCloudSolrClient (add auth/pref) │
│  Observer/Event         │  Kafka topic publish → multiple consumers     │
│  Facade                 │  GSTMutator/GSTReader (wraps Layer0 HBase)   │
│  Cache-Aside            │  DistCacheUtil (70+ regions, 2-tier)          │
│  Circuit Breaker Effect │  SynchronousQueue → backpressure on full pool │
│  Retry + DLQ            │  Consumer → ErrorTopic → DLQ (3-tier)        │
│  Idempotency            │  txnRefId in ledger + HBase row key overwrite │
│  CQRS (lightweight)     │  MySQL (write/balance) + HBase (read/history) │
│  Saga-like (XA)         │  Atomikos 2PC for cross-DB order processing   │
│  Template Engine        │  FreeMarker for notification templates        │
│  Filter Chain           │  TokenAuthFilter → DbAuthManager → Controller │
└─────────────────────────┴───────────────────────────────────────────────┘
```

## Numbers to Memorize for Impact

```
14M    registered GSTINs
3B+    invoices processed/year
500M+  return filings/year
1.6B   ledger entries/year
45+    REST API microservices
32+    shared framework libraries
70+    cache regions (2-tier: EhCache + JDG)
20+    case types with Strategy pattern
10+    return types with Template Method
50K    concurrent officer sessions
3-tier Kafka error handling (main → error → DLQ)
2-phase commit for cross-database consistency

"I worked on India's national tax platform serving 14 million taxpayers,
 processing 3 billion invoices annually across 45+ microservices."
```

---

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  MARKET-GAP LEARNING PLAN + PORTFOLIO PROJECTS                          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

## Gap Analysis: Your Stack → Market Expectation

```
┌──────────────┬─────────────────┬────────────────────────────────────┬──────────┐
│ Area         │ Your Current    │ Market (SDE-2/3)                   │ Priority │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Java         │ Java 8          │ Java 17-21 (Records, Sealed,       │ 🔴 HIGH  │
│              │                 │  Virtual Threads, Pattern Matching) │          │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Spring       │ Spring 4.3 +    │ Spring Boot 3.x + Spring 6         │ 🔴 HIGH  │
│              │ Boot 2.4        │ (Jakarta EE, native, VThreads)     │          │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Containers   │ WAR on Tomcat   │ Docker + Kubernetes                │ 🔴 HIGH  │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Testing      │ TestNG+Mockito  │ JUnit5 + Testcontainers + WireMock │ 🟡 MED   │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Observability│ Logback+basic   │ ELK/Grafana + Jaeger/Zipkin        │ 🟡 MED   │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ CI/CD        │ Basic/manual    │ GitHub Actions + Docker + GitOps   │ 🟡 MED   │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Cloud        │ On-prem JDG     │ AWS (SQS,SNS,DynamoDB,ECS) / GCP  │ 🟡 MED   │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ Reactive     │ Servlet/blocking│ WebFlux (conceptual)               │ 🟢 LOW   │
├──────────────┼─────────────────┼────────────────────────────────────┼──────────┤
│ API Design   │ REST only       │ REST + gRPC + GraphQL (conceptual) │ 🟢 LOW   │
└──────────────┴─────────────────┴────────────────────────────────────┴──────────┘
```

---

## 12-WEEK LEARNING PLAN (3 months, 2 hours/day)

### PHASE 1: Foundations (Weeks 1-4) — Java 17 + Spring Boot 3 + Docker

```
WEEK 1: Java 17-21 Features
─────────────────────────────
Day 1-2: Records, Sealed Classes, Pattern Matching for instanceof
  - Create a record: record LedgerEntry(String gstin, BigDecimal amount, LocalDate date) {}
  - Sealed interface: sealed interface CaseCustomizer permits AdjudicationCustomizer, AppealCustomizer {}
  - Pattern matching: if (obj instanceof LedgerEntry entry) { entry.gstin(); }

Day 3-4: Text Blocks, Switch Expressions, Helpful NullPointerException
  - Multiline SQL: var sql = """
      SELECT gstin, balance
      FROM cash_ledger
      WHERE gstin = ?
      """;
  - Switch expression: var handler = switch(caseType) {
      case "AMYDT" -> adjudicationCustomizer;
      case "APLTD" -> appealCustomizer;
      default -> defaultCustomizer;
  };

Day 5-7: Virtual Threads (Java 21 — Project Loom)
  - Thread.ofVirtual().start(() -> processCase(caseId));
  - ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
  - Why it matters: Your Kafka consumer uses 50-thread pool.
    With virtual threads: 10,000 concurrent tasks, zero thread starvation.
  
  Practice: Rewrite your Consumer thread pool using virtual threads

WEEK 2: Spring Boot 3 + Spring 6
─────────────────────────────────
Day 1-2: Migration from Spring 5 → 6
  - javax.* → jakarta.* namespace change
  - New @HttpExchange (declarative HTTP clients)
  - Spring Security 6 AuthorizationManager (you already have this!)

Day 3-4: Spring Boot 3 features
  - GraalVM native compilation (AOT)
  - spring.main.virtual-threads=true (auto virtual threads)
  - Observability with Micrometer + OpenTelemetry
  - @ConditionalOnProperty (you already use this!)

Day 5-7: Build a Spring Boot 3 REST API
  - Use Java 17 records as DTOs
  - Spring Security 6 with JWT (instead of cache-backed sessions)
  - OpenAPI 3.0 (springdoc-openapi-starter-webmvc-ui)
  
  Practice: Create a mini Case Management API with Spring Boot 3

WEEK 3: Docker + Docker Compose
────────────────────────────────
Day 1-2: Docker basics
  - Dockerfile for Spring Boot: FROM eclipse-temurin:21-jre
  - Multi-stage build (build with Maven, run with JRE)
  - Layer optimization: COPY --from=build

Day 3-4: Docker Compose for full stack
  - docker-compose.yml with:
    - app (Spring Boot)
    - MySQL 8
    - Redis (replaces JDG)
    - Kafka + Zookeeper
    - Grafana + Prometheus (monitoring)

Day 5-7: Build & run your project in Docker
  - docker compose up → full local environment
  - Volume mounts for hot reload
  - Health checks (Spring Actuator + Docker HEALTHCHECK)

WEEK 4: Testing (JUnit 5 + Testcontainers + WireMock)
──────────────────────────────────────────────────────
Day 1-2: JUnit 5 migration from TestNG
  - @Test, @BeforeEach, @ParameterizedTest
  - Assertions.assertAll() for grouped assertions
  - @Nested classes for organized tests

Day 3-4: Testcontainers (real DB in tests)
  - @Container MySQLContainer mysql = new MySQLContainer<>("mysql:8");
  - @Container KafkaContainer kafka = new KafkaContainer("7.5.1");
  - Integration test with real MySQL → no more H2 surprises

Day 5-7: WireMock (mock external APIs)
  - WireMockServer.stubFor(post("/irp/generate-irn").willReturn(ok("...")))
  - Simulate IRP downtime → test your retry logic
  - Contract testing basics
```

### PHASE 2: Cloud + Observability (Weeks 5-8)

```
WEEK 5: AWS Fundamentals
──────────────────────────
Day 1-2: Core services mapping
  Your stack           →  AWS equivalent
  ─────────────────────────────────────
  JDG (Infinispan)     →  ElastiCache (Redis)
  Kafka                →  MSK or SQS+SNS
  MySQL                →  RDS Aurora
  HBase                →  DynamoDB (managed NoSQL)
  Solr                 →  OpenSearch (ElasticSearch)
  Tomcat/JBoss         →  ECS Fargate or EKS

Day 3-4: Hands-on with AWS Free Tier
  - Launch RDS MySQL instance
  - Create ElastiCache Redis cluster
  - Create SQS queue + SNS topic
  - Deploy Spring Boot to ECS Fargate

Day 5-7: Architecture diagram on AWS
  - Re-draw your Return Filing System on AWS
  - API Gateway → ECS → SQS → Lambda (consumer) → DynamoDB
  - Practice: "Design a tax filing system on AWS" (interview question)

WEEK 6: Kubernetes (K8s)
─────────────────────────
Day 1-2: K8s core concepts
  - Pod, Deployment, Service, ConfigMap, Secret
  - kubectl basics: apply, get, describe, logs

Day 3-4: Deploy your Spring Boot app to K8s
  - Deployment YAML with 3 replicas
  - Service (ClusterIP + LoadBalancer)
  - ConfigMap for application.properties
  - Secret for DB credentials
  - HorizontalPodAutoscaler (HPA): scale on CPU/memory

Day 5-7: K8s advanced
  - Liveness/Readiness probes (Spring Actuator endpoints)
  - Rolling updates (zero downtime deployment)
  - Resource limits and requests

WEEK 7: Observability Stack
────────────────────────────
Day 1-2: Structured Logging
  - Logback → structured JSON logs
  - MDC (Mapped Diagnostic Context): traceId, gstin, requestId
  - ELK stack: Elasticsearch + Logstash + Kibana (Docker Compose)

Day 3-4: Metrics with Micrometer + Prometheus + Grafana
  - spring-boot-starter-actuator
  - Micrometer registry: prometheus
  - Custom metrics: ledger_debit_total, case_created_total
  - Grafana dashboard: QPS, latency percentiles, error rate

Day 5-7: Distributed Tracing
  - Micrometer Tracing + Zipkin (or Jaeger)
  - Trace across: API → Kafka → Consumer → DB
  - Spring Boot 3 auto-instruments with Micrometer
  - Visualize: "filing took 3.2s → 2.1s in HBase write + 0.5s in validation"

WEEK 8: CI/CD Pipeline
────────────────────────
Day 1-2: GitHub Actions basics
  - .github/workflows/build.yml
  - Trigger on push/PR
  - Steps: checkout → setup-java → maven build → test → docker build

Day 3-5: Full pipeline
  - Build → Test (Testcontainers in CI) → Docker push → Deploy to K8s
  - SonarQube for code quality (optional)
  - Dependency scanning (Dependabot)

Day 6-7: GitOps concept
  - ArgoCD: Git repo as source of truth for K8s state
  - Helm charts for templated K8s manifests
```

### PHASE 3: Advanced + Portfolio (Weeks 9-12)

```
WEEK 9-10: Advanced Concepts
──────────────────────────────
Day 1-3: gRPC service
  - Proto3 schema definition
  - Spring Boot + grpc-spring-boot-starter
  - Build a LedgerService gRPC API (getLedgerBalance, debitLedger)
  - Performance comparison: REST vs gRPC (benchmark with JMH)

Day 4-5: GraphQL (conceptual)
  - Spring for GraphQL
  - Schema-first: type Case { id: ID!, status: String, tasks: [Task] }
  - Resolver: @QueryMapping List<Case> cases(@Argument String gstin)
  
Day 6-7: Reactive (conceptual)
  - Spring WebFlux basics: Mono<T>, Flux<T>
  - Reactive Kafka consumer
  - When to use: high I/O concurrency (10K+ connections)
  - When NOT to use: CPU-bound processing (your validation logic)

WEEK 11-12: Portfolio Project (The Capstone)
─────────────────────────────────────────────
→ See PROJECT details below
```

---

## THREE PORTFOLIO PROJECTS (Pick any 1 as capstone, all 3 for max impact)

---

### PROJECT 1: "TaxFlow" — Mini Tax Filing Platform
**Estimated Build Time: 3-4 weekends**
**GitHub Repo Name: `taxflow-platform`**

```
TECH STACK (all market-standard):
  ├── Java 21 + Spring Boot 3.3
  ├── Spring Security 6 (JWT auth)
  ├── MySQL 8 (ledger, workflow)
  ├── Redis 7 (cache, distributed lock, session)
  ├── Apache Kafka 3.x (async events)
  ├── Docker Compose (full stack local)
  ├── JUnit 5 + Testcontainers + WireMock
  ├── Micrometer + Prometheus + Grafana (observability)
  ├── GitHub Actions (CI/CD)
  └── Kubernetes manifests (deploy-ready)

MODULES (mirrors YOUR GSTN experience):

  Module 1: Filing Service
    ├── POST /api/v1/returns/{gstin}/{period}   — Save draft
    ├── PUT  /api/v1/returns/{gstin}/{period}    — Submit (validate)
    ├── POST /api/v1/returns/{gstin}/{period}/file — File (sign + persist)
    ├── GET  /api/v1/returns/{gstin}/{period}    — Get return
    │
    ├── Template Method pattern:
    │     abstract class FilingEngine {
    │       final void file(Request req) {
    │         preValidate(req);          // common
    │         formSpecificValidate(req); // abstract
    │         sign(req);                 // common (JWT-based mock)
    │         persist(req);              // common (MySQL + event)
    │       }
    │     }
    │     class Gstr3bFilingEngine extends FilingEngine { ... }
    │     class Gstr1FilingEngine extends FilingEngine { ... }
    │
    └── Kafka event: RETURN_FILED → consumed by Ledger + Notification

  Module 2: Ledger Service
    ├── POST /api/v1/ledger/{gstin}/credit   — Credit entry
    ├── POST /api/v1/ledger/{gstin}/debit    — Debit entry
    ├── GET  /api/v1/ledger/{gstin}/balance  — Current balance
    ├── GET  /api/v1/ledger/{gstin}/history  — Transaction history
    │
    ├── Dual storage: MySQL (balance) + event log (append-only)
    ├── ITC offset logic: IGST → CGST → SGST order
    ├── Idempotency: txnRefId prevents double-debit
    ├── Redis cache: balance cached with 5-min TTL
    │
    └── Double-entry bookkeeping: every debit has a corresponding credit

  Module 3: Case Workflow Service
    ├── POST /api/v1/cases                    — Create case
    ├── GET  /api/v1/cases/{caseId}           — Get case details
    ├── PUT  /api/v1/cases/{caseId}/tasks/{taskId}  — Update task
    ├── POST /api/v1/cases/{caseId}/reassign  — Reassign
    │
    ├── Strategy + Factory:
    │     sealed interface CaseCustomizer permits
    │       AdjudicationCustomizer, AppealCustomizer, DefaultCustomizer {
    │       Case beforeCreate(Case c);
    │       Case afterCreate(Case c);
    │     }
    │     @Component class CaseCustomizerFactory {
    │       CaseCustomizer get(CaseType type) {
    │         return switch(type) {
    │           case ADJUDICATION -> adjudicationCustomizer;
    │           case APPEAL -> appealCustomizer;
    │           default -> defaultCustomizer;
    │         };
    │       }
    │     }
    │
    ├── State machine: CREATED → ASSIGNED → IN_PROGRESS → COMPLETED
    ├── SLA tracking: dueDate with working-day calculator
    └── Audit trail: case_history table (every status change)

  Module 4: Notification Service
    ├── Kafka consumer: listens to RETURN_FILED, CASE_CREATED, etc.
    ├── Template engine: FreeMarker (${name}, ${arn}, ${amount})
    ├── Channels: email (JavaMailSender) + mock SMS
    ├── Audit: notification_audit table
    └── Async: @Async + CompletableFuture

  Module 5: API Gateway + Auth
    ├── Spring Security 6 + JWT
    ├── RBAC: roles table → endpoint access
    ├── Rate limiting: Bucket4j
    └── Swagger/OpenAPI 3.0

INFRASTRUCTURE:
  docker-compose.yml:
    services:
      app:        image: taxflow:latest, ports: 8080
      mysql:      image: mysql:8, ports: 3306
      redis:      image: redis:7-alpine, ports: 6379
      kafka:      image: confluentinc/cp-kafka:7.5, ports: 9092
      zookeeper:  image: confluentinc/cp-zookeeper:7.5
      prometheus: image: prom/prometheus
      grafana:    image: grafana/grafana, ports: 3000
      zipkin:     image: openzipkin/zipkin, ports: 9411

  k8s/ folder:
    deployment.yaml, service.yaml, configmap.yaml,
    hpa.yaml, ingress.yaml

  .github/workflows/ci.yml:
    - Build (Maven)
    - Test (JUnit5 + Testcontainers)
    - Docker build + push
    - Deploy to K8s (optional)

README.md HIGHLIGHTS:
  "Inspired by India's national tax platform (14M taxpayers, 500M filings/year).
   Implements production patterns: Strategy+Factory for polymorphic case handling,
   Template Method for filing workflow, dual-storage ledger, 3-tier Kafka error
   handling, distributed caching, RBAC auth with JWT."
```

**Why This Project Wins Interviews:**
- Shows you can build an END-TO-END system, not just a CRUD app
- Uses patterns from REAL production experience (not textbook)
- Modern stack (Java 21, Spring Boot 3, Docker, K8s, Observability)
- Directly matches system design questions you'll be asked

---

### PROJECT 2: "EventPipe" — Production-Grade Kafka Pipeline Framework
**Estimated Build Time: 2 weekends**
**GitHub Repo Name: `eventpipe-kafka-framework`**

```
TECH STACK:
  ├── Java 21 + Spring Boot 3.3
  ├── Apache Kafka 3.x
  ├── Redis (for DLQ tracking dashboard)
  ├── Docker Compose
  ├── JUnit 5 + Testcontainers (KafkaContainer)
  └── Micrometer metrics

WHAT IT DOES (production-grade Kafka framework):

  1. PLUGGABLE PROCESSOR INTERFACE:
     @FunctionalInterface
     interface EventProcessor<T> {
       ProcessResult process(T event, EventMetadata metadata);
     }
     
     enum ProcessResult { SUCCESS, RETRY, DEAD_LETTER }

  2. 3-TIER ERROR HANDLING (mirrors YOUR Consumer.java):
     Main Topic → Error Topic (scheduled retry) → DLQ
     
     Config:
       eventpipe.topics.main=ORDER_CREATED
       eventpipe.topics.error=ORDER_CREATED_ERROR
       eventpipe.topics.dlq=ORDER_CREATED_DLQ
       eventpipe.retry.max-attempts=3
       eventpipe.retry.schedule-cron=0 0 2 * * *   # 2 AM daily
       eventpipe.retry.window-minutes=30

  3. BACK-PRESSURE (mirrors YOUR SynchronousQueue pattern):
     - Virtual thread executor (Java 21)
     - Configurable concurrency
     - Auto-throttle on consumer lag

  4. OBSERVABILITY:
     Metrics (Micrometer):
       eventpipe_messages_processed_total{topic, result}
       eventpipe_processing_duration_seconds{topic}
       eventpipe_error_topic_depth{topic}
       eventpipe_dlq_depth{topic}
     
     Dashboard (Grafana):
       - Processing rate
       - Error rate
       - DLQ depth alerts

  5. SPRING BOOT STARTER:
     Just add dependency + implement EventProcessor:
     
     @Bean
     EventProcessor<OrderEvent> orderProcessor() {
       return (event, meta) -> {
         orderService.process(event);
         return ProcessResult.SUCCESS;
       };
     }

README.md HIGHLIGHTS:
  "Production-grade Kafka consumer framework with 3-tier error handling
   (main → retry → DLQ), back-pressure, and observability. Inspired by
   a framework processing 2000+ events/sec on India's national tax platform."
```

---

### PROJECT 3: "CacheForge" — Distributed Cache Abstraction Layer
**Estimated Build Time: 2 weekends**
**GitHub Repo Name: `cacheforge`**

```
TECH STACK:
  ├── Java 21 + Spring Boot 3.3
  ├── Redis 7 (distributed tier)
  ├── Caffeine (local tier — replaces EhCache)
  ├── Docker Compose
  ├── JUnit 5 + Testcontainers
  └── JMH (Java Microbenchmark Harness)

WHAT IT DOES (mirrors YOUR 2-tier cache):

  1. 2-TIER CACHE ABSTRACTION:
     @CacheForge(region = "ENTITY_DETAILS", ttl = 60, tier = DISTRIBUTED)
     public EntityDetails getEntity(String gstin) { ... }

     @CacheForge(region = "TAX_RATES", ttl = 1440, tier = LOCAL)
     public List<TaxRate> getRates() { ... }

  2. CACHE REGIONS (named, isolated, configurable):
     cacheforge:
       regions:
         ENTITY_DETAILS:
           tier: DISTRIBUTED
           ttl-minutes: 60
           max-idle-minutes: 30
         TAX_RATES:
           tier: LOCAL
           ttl-minutes: 1440
           max-entries: 1000

  3. DISTRIBUTED LOCKING:
     @DistributedLock(key = "'FILING_' + #gstin + '_' + #period", ttl = 300)
     public void fileReturn(String gstin, String period) { ... }

  4. CACHE-ASIDE HELPER:
     cacheForge.getOrLoad("ENTITY_DETAILS", gstin, () -> entityDao.find(gstin));

  5. STAMPEDE PROTECTION:
     - First request acquires lock, loads from DB
     - Concurrent requests wait (short timeout) then read from cache
     - Prevents thundering herd on cold cache

  6. BENCHMARKS (JMH):
     Caffeine (local):       ~50 ns/op
     Redis (distributed):    ~500 μs/op (1000x slower but shared)
     2-tier (local hit):     ~50 ns/op
     2-tier (local miss):    ~500 μs/op
     DB (no cache):          ~5 ms/op (10,000x slower)

README.md HIGHLIGHTS:
  "Spring Boot starter for 2-tier caching (local Caffeine + distributed Redis).
   Named cache regions, TTL/idle configuration, distributed locking, stampede
   protection. Inspired by a 70-region cache layer serving 14M entities."
```

---

## WHICH PROJECT TO BUILD FIRST?

```
┌─────────────┬────────────────────────────────────────┬───────────────────┐
│ Project     │ Best For                               │ Interview Impact  │
├─────────────┼────────────────────────────────────────┼───────────────────┤
│ TaxFlow     │ Full-stack system design showcase       │ ⭐⭐⭐⭐⭐          │
│             │ Product companies (Amazon, Flipkart)    │ "Built end-to-end │
│             │ Shows breadth: patterns, DB, cache,     │  platform"        │
│             │ Kafka, auth, observability, K8s          │                   │
├─────────────┼────────────────────────────────────────┼───────────────────┤
│ EventPipe   │ Framework/infrastructure roles          │ ⭐⭐⭐⭐           │
│             │ Platform teams (Google, LinkedIn)        │ "Built a reusable │
│             │ Shows depth: Kafka internals, error      │  framework"       │
│             │ handling, observability                  │                   │
├─────────────┼────────────────────────────────────────┼───────────────────┤
│ CacheForge  │ Performance-focused roles               │ ⭐⭐⭐⭐           │
│             │ Finance (Goldman, Morgan Stanley)        │ "Built a caching  │
│             │ Shows: benchmarking, abstraction,        │  abstraction"     │
│             │ Spring Boot starter creation             │                   │
└─────────────┴────────────────────────────────────────┴───────────────────┘

RECOMMENDATION:
  → Start with PROJECT 1 (TaxFlow) — it covers ALL market gaps in one project
  → Then pick PROJECT 2 or 3 based on your target companies
  → All three together = unstoppable GitHub portfolio
```

---

*Generated from actual GSTN JAVA_Maintrunk codebase analysis — March 2026*
*8 System Design Problems + Complete Answers + Learning Plan + 3 Portfolio Projects*
