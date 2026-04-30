# Resume Bullet Explainer — What I Actually Did
### Jayanti Vishnoi | 5.6 Years | Java Full-Stack Developer at GSTN (Infosys)
### For each resume bullet: My role, the CRs I worked on, the files I touched, and how the code works

> **Purpose of this document:**
> This is an interviewer-ready companion to Resume_Bullets_Final.md. For each of the 5 resume bullets, this document explains:
> 1. **What I was actually involved in** — specific CR numbers, sub-tasks, and ownership
> 2. **Which files I coded in** — with real file paths from the codebase
> 3. **How the code works end-to-end** — flow descriptions an interviewer can verify
> 4. **What was pre-existing vs what I built** — honesty about scope
> 5. **Interview follow-up answers** — ready-made responses for deep-dive questions

---

## BULLET 1 — 12-Scenario Financial State Machine + Double-Entry Ledger

### Resume Text
> Designed and implemented a 12-scenario financial order-processing engine for India's national tax dispute platform (15.2 million taxpayers, 28 state jurisdictions) — built a decision-matrix state machine handling multi-tier demand chains (original demand, first-appeal order, subsequent order) with conditional demand creation, inter-account balance transfers, dispute reversals, and refund triggers; each scenario generates immutable double-entry ledger transactions (debit/credit) across 3 databases, impacting 75+ Java classes across 5 microservice modules.

---

### What I Was Involved In

**Primary CR:** CR28625A — Subsequent Order + Simultaneous Combine Order
**Scope:** ~40 unique files across LitigationAPI, LitigationAPI2, CaseMgmtFwk, and DCR modules

Before CR28625A, the system only handled first-appeal outcomes (APL01→APL04). When a taxpayer files a first appeal (APL01) and also a second-tier appeal (APL03) against the same original demand (DRC-07), and an order is passed on the first appeal while the second-tier appeal is also active — this creates a "subsequent order" scenario. My work was to implement the **complete financial and case lifecycle for subsequent orders** across all 12 combinations of outcomes.

**The 12 scenarios I implemented (firstAppealOutcome × subsequentOutcome):**

| First Appeal (APL03-APL04) | Subsequent Order (APL01-APL04) | My Implementation |
|---|---|---|
| Confirmed | Confirmed | D1 dispute reversal → D2 closure (credit + transfer-out) → D3 creation |
| Confirmed | Modified | D1 dispute reversal → D2 closure → D3 with modified determined amt |
| Confirmed | Rejected | D1 dispute reversal → D2 closure (transfer-out) → D1 status restore |
| Modified | Confirmed | D1 dispute reversal → D2 closure (credit determine + transfer-out) → D3 creation |
| Modified | Modified | D1 dispute reversal → D2 closure → D3 with new determined amt |
| Modified | Rejected | D1 dispute reversal → D2 closure → D1 status = Subsequent Order Rejected |
| Rejected | Confirmed | No D2 exists → standard D3 creation from D1 |
| Rejected | Modified | No D2 exists → D3 with modified determined amt from D1 |
| Rejected | Rejected | No D2, no D3 → D1 status = Subsequent Order Rejected (zero ledger changes) |
| Confirmed | Admitted | D1 demand stay + APL04 demand stay (if positive balance) |
| Modified | Admitted | D1 demand stay + APL04 demand stay |
| Rejected | Admitted | D1 demand stay only (no prior APL04) |

**D1** = Original demand (DRC-07), **D2** = First appeal order demand (APL03-APL04), **D3** = Subsequent order new demand

---

### Files I Coded In

**Core implementation files (I wrote the subsequent order blocks in these):**

| File | What I added | Line references |
|---|---|---|
| `Core-API/LitigationAPI/.../AppealOrderItemCustomizer.java` | updateDemandStatus() — 12 scenario blocks for subsequent order; updateDemandStatusMfy() — duplicate for MFY flow; updateSimultaneousCaseStatus(); convertJsonToDemandAmountVO(); isApl03ReversalEntryExists(); updateDemandByIdForFirstAppealOrder() | Lines 8500-8910 (subsequent order changes), DCR block at 8462-8499, helper methods after line 8810 |
| `Core-API/LitigationAPI/.../AppealCaseCustomizer.java` | Demand stay logic for subsequent APL01 — when APL03 has already issued AOP | Lines 841-974 (subsequent order demand stay) |
| `Core-API/LitigationAPI2/.../AppealValidations.java` | isSimulCombinedOrd() — checks if current order is part of simultaneous appeal; isEligibleToProvideEffect(); getCountOfAppealApplications() | Validation methods used across all 12 scenarios |
| `Commons/CaseMgmtFwk/.../CaseServiceImpl.java` | getLatestAplDtlsForSimulApl() — queries both APL01 and APL03 for a given demand ID, returns JSON with status flags (isApl01Issued, isApl03Issued, AOPOnAPL01, AOPOnAPL03, appelAdmAplcn, appelApltdAdmAplcn) | Called at the start of updateDemandStatus to determine which scenario applies |
| `Commons/CaseMgmtFwk/.../Case.java` | Added subsequentOrd boolean flag, simulCombinedOrd flag | JPA entity changes |
| `Core-API/LitigationAPI/.../AppealOrderItemJson.java` | Added apl03ordNum, apl03dispamt, apl03dtramt fields for subsequent order JSON structure | VO changes |
| `Core-API/LitigationAPI/.../AppealServiceImpl.java` | Subsequent order flow wiring — calls updateDemandStatus with subsequent flags | Service orchestration |
| `Commons/CaseMgmtFwk/.../DemandProcessingUtil.java` | getDmndStatusByOutstandingAmnt(); setUpdateDemandReqVO(); convertJsonToDemandAmountVO(); getOutstandingAmntForPositiveBalStatus() — utility methods for demand financial calculations | Lines 1733-4796 (6+ blocks) |
| `Commons/CaseMgmtFwk/.../DCRConstants.java` | Added constants: SUBSEQUENT_ORDER_REJECTED, SUBSEQUENT_ORDER_ISSUED_FIRST_APPEAL_DEMAND_CLOSED, DEMAND_CREATED_AGAINST_SUBSEQUENT_ORDER_OF_FIRST_APPEAL_ORDER | New status codes |
| `Core-API/LitigationAPI/.../AppealNotceCustomizer.java` | Subsequent order notice handling | CR28625A tag |
| `Core-API/LitigationAPI/.../AppealReplyItemCustomizer.java` | Reply item handling for subsequent orders | CR28625A tag |
| `Core-API/LitigationAPI/.../AppealWithdrawalCustomizer.java` | Withdrawal logic for subsequent orders | CR28625A tag |
| `Core-API/LitigationAPI/.../AppealWithdrawOrderItemCustomizer.java` | Withdraw order for subsequent | CR28625A tag |

**What was pre-existing vs what I built:**
- **Pre-existing:** The first-appeal order flow (APL01→APL04 with 3 outcomes: confirmed/modified/rejected) was already implemented. The ledger transaction framework (NonReturnLiabLedger), demand update APIs, and case management framework existed.
- **What I built:** The entire subsequent order processing layer — the 12-scenario decision matrix, D2 closure logic (credit determine + transfer-out + transfer-in reversal), D1 dispute reversal entries, simultaneous case status update (`updateSimultaneousCaseStatus`), APL03 reversal entry check (`isApl03ReversalEntryExists`), JSON-to-DemandAmountVO converter, demand stay logic for subsequent APL01 admission, and the MFY (Modified Format YAML) duplicate flow.

---

### How It Works End-to-End (Example: Confirm-Reject Scenario)

```
1. Officer issues APL04 order on APL01 with outcome = REJECTED, item.isSubsequentOrd() = true
2. System calls caseService.getLatestAplDtlsForSimulApl(origDmndId)
   → Returns: isApl03Issued=true, AOPOnAPL03=true, prevOrdStatus=CONFIRMED
3. Enters subsequent order block in updateDemandStatus()
4. Step 1 - D1 Dispute Reversal:
   → Fetch APL03 dispute amount from item JSON (apl03dispamt)
   → Insert NonReturnLiabLedger entry: demandId=D1, tranCd=REVERSAL_OF_DISPUTED_AMOUNT_APL03, type=DEBIT_TRANS
5. Step 2 - D2 Closure:
   → Update D2 (APL04-for-APL03) demand status = SUBSEQUENT_ORDER_ISSUED_FIRST_APPEAL_DEMAND_CLOSED
   → If prior transfers exist (Transfer-Out from D1 to D2): reverse both entries
   → Credit D2 with APL03 determine amount (REDUCTION_TRANS)
   → Check D2 outstanding: if negative, transfer-out remaining balance from D2, transfer-in to D1
6. Step 3 - D1 Status Update:
   → Update D1 demand status = SUBSEQUENT_ORDER_REJECTED
   → Set demandStayed = NO
7. No D3 created (rejected = no new demand)
```

---

### Key Code Pattern I Implemented

```java
// In AppealOrderItemCustomizer.updateDemandStatus() — CR28625A
if(item.isSubsequentOrd()){
    item.setSimulCombinedOrd(false);
    // Fetch APL03 case details via case folder ID
    JSONObject simulApldtl = itmJson.getJSONObject("simulApldtl");
    JSONObject ApltdCase = simulApldtl.getJSONObject("latestApltdCase");
    apltdcaseVo = caseutil.getCaseByCaseFolderId(apl03caseFldrId);
    // ... fetch APL03 appeal details for demand calculations
}

// Decision matrix entry point
typeOfAplAplcn = caseService.getLatestAplDtlsForSimulApl(origDmndId);
boolean AOPOnAPL01 = typeOfAplAplcn.getBoolean("AOPOnAPL01");
boolean AOPOnAPL03 = typeOfAplAplcn.getBoolean("AOPOnAPL03");

// Each outcome branch (confirmed/modified/rejected) checks item.isSubsequentOrd()
// and branches into D2 closure + D3 creation logic
```

---

## BULLET 2 — Concurrent Order Issuance + Distributed Transactions

### Resume Text
> Engineered a defense-in-depth concurrency control system for adjudication order issuance — implemented Redis distributed locks (SETNX with TTL) at the API gateway to prevent duplicate requests across clustered instances, JPA optimistic locking (@Version) at the persistence layer as a safety net, and XA/Atomikos 2-phase commit to guarantee atomicity across case management, financial ledger, and workflow databases; this eliminated race conditions where two officers could simultaneously issue conflicting orders on the same demand.

---

### What I Was Involved In

**CRs involved:** This spans multiple CRs — the concurrency pattern is embedded throughout the order issuance flows I worked on (CR28625A, CR27893-D).

The concurrency issue: when two tax officers (or the same officer in two tabs) try to pass an appeal order on the same case simultaneously, both could pass the "is case in valid state?" check, both proceed, and you end up with two conflicting orders and corrupt financial data.

**My involvement in each layer:**

1. **Redis SETNX (API boundary):** Used via DistCacheFwk in the controller/service layer. Before processing an order issuance, acquire a distributed lock keyed on caseId+demandId. If lock exists, reject with "operation in progress" error. Lock has TTL to prevent deadlock.

2. **JPA @Version (persistence layer):** The `Case` entity has a version field. When I update case status in `updateSimultaneousCaseStatus()` or `caseHandler.updateCaseStatus()`, JPA adds `WHERE version=N` to the UPDATE. If another transaction modified the case between my read and write, the update affects 0 rows → `OptimisticLockException` → retry or fail.

3. **XA/Atomikos 2-Phase Commit (cross-database):** The order issuance touches 3 databases:
   - Case management DB (case status, case folder items)
   - Financial ledger DB (NonReturnLiabLedger entries, demand status)
   - Workflow DB (tasks, assignments)
   
   These are coordinated via Atomikos XA transaction manager configured in WorkFlowFwk. The `@Transactional` annotation with XA propagation ensures all 3 databases commit or all rollback.

---

### Files I Coded In

| File | What I touched | Concurrency relevance |
|---|---|---|
| `Core-API/LitigationAPI/.../AppealOrderItemCustomizer.java` | The entire `updateDemandStatus()` method runs inside an XA transaction. My subsequent order code (6+ ledger writes across 2 DBs) relies on XA atomicity. | XA 2PC ensures all my ledger entries commit together |
| `Core-API/LitigationAPI/.../AppealCaseCustomizer.java` | Case status updates for subsequent APL01 demand stay | Uses @Version on Case entity |
| `Core-API/LitigationAPI2/.../WaiverLedgerUpdateCtrl.java` | REST controller with `@PostMapping /v0.1/recovery/updateLedgerEntries` — sets DB routing via DbContextHolder before service call | Request-scoped ThreadLocal + @Transactional |
| `Core-API/LitigationAPI2/.../WaiverLdgrUpdServiceImpl.java` | `@Transactional(propagation = Propagation.REQUIRED)` — calculates waiver amounts and inserts ledger entries atomically | Single-DB transactional boundary |
| `Commons/DistCacheFwk/` | Redis-based distributed cache framework used for SETNX lock pattern | I used this framework; it was pre-existing |
| `Commons/WorkFlowFwk/` | Atomikos XA transaction configuration | I used this framework; config was pre-existing |

**What was pre-existing vs what I built:**
- **Pre-existing:** DistCacheFwk (Redis client wrapper), WorkFlowFwk (Atomikos XA config), @Version annotation on Case entity, intRevCellDaoXa (XA-enabled DAO)
- **What I built/leveraged:** My code paths (subsequent order, waiver ledger updates) execute within the XA boundary. I ensured correct transaction propagation for multi-DB writes. I used the Redis lock pattern in controller layers for mutual exclusion. The `WaiverLedgerUpdateCtrl` controller I wrote explicitly sets `DbContextHolder.setDbType()` before the transactional service call.

---

### How It Works End-to-End

```
1. Officer clicks "Pass Order" in BO-Web portal
2. Request hits API controller → Redis SETNX lock acquired on caseId (TTL=30s)
   → If lock already held → HTTP 409 "Operation in progress, please wait"
3. XA Transaction begins (Atomikos coordinates 3 DataSources)
4. Read case entity (JPA loads version=5)
5. Execute updateDemandStatus() → 6+ ledger writes to financial DB
6. Execute updateSimultaneousCaseStatus() → case management DB updates
7. Execute createTaskObj() → workflow DB insert
8. Update case entity → JPA generates UPDATE ... WHERE version=5
   → If another transaction already updated to version=6 → OptimisticLockException → XA ROLLBACK all 3 DBs
   → If no conflict → version becomes 6
9. XA Phase 1: All 3 DBs vote PREPARE (yes)
10. XA Phase 2: Coordinator sends COMMIT to all 3 DBs
11. Redis lock released (DELETE key) in finally block
```

---

## BULLET 3 — Waiver Payment Lifecycle + Void Order Reversal System

### Resume Text
> Built an end-to-end government compliance waiver lifecycle spanning 7 order types (application, payment confirmation, approval, void, rejection, appeal integration, DRC-03 reconciliation) — implemented the approval flow with ledger credit entries to reduce outstanding demand, void order issuance with compensating debit reversals to restore original balances, and cross-module appeal integration enabling taxpayers to appeal rejected waivers; the system handles demand status transitions, recovery case updates, and automated email/SMS notifications across the complete lifecycle.

---

### What I Was Involved In

**Primary CR:** CR27893 — Waiver Scheme (SPL01–SPL07)
**Sub-CRs I worked on:**
- **CR27893-A:** SPL01 (waiver application creation) + SPL02 (payment confirmation) — case creation logic in AdjudicationCaseCustomizer
- **CR27893-B:** SPL03 (officer notice/show cause) + SPL05 (approval order) — created the `WaiverSchemeFolderItemCustomizer` class from scratch + ledger credit entries
- **CR27893-C:** DRC-03 payment status tracking — Drc03LedgerServiceImpl, Drc03LedgerDaoImpl
- **CR27893-D:** SPL06 (void order — compensating debit) + withdrawal handling
- **CR27893-D1:** Auto-approval email notification
- **CR27893-D2:** Appeal on SPL07 rejection — DCR integration for AppealOrderItemCustomizer + DemandOrderFetchStrategy SPL05/SPL06 item availability check

**Total scope:** ~55 unique files across LitigationAPI, LitigationAPI2, CaseMgmtFwk, DCR, BO-Web

---

### Files I Coded In

| File | What I built | CR sub-task |
|---|---|---|
| `Core-API/LitigationAPI2/.../WaiverSchemeFolderItemCustomizer.java` | **New class created from scratch.** Implements `CaseFolderItemCustomizer`. Handles `afterAddCaseFolderItem()` lifecycle hook for SPL03/SPL05 order types. Processes waiver approval by triggering ledger credit entries. | CR27893-B |
| `Core-API/LitigationAPI2/.../WaiverLedgerUpdateCtrl.java` | REST controller `@PostMapping /v0.1/recovery/updateLedgerEntries`. Accepts SPL05ItemJson. Sets DB routing via DbContextHolder. | CR27893-B |
| `Core-API/LitigationAPI2/.../WaiverLdgrUpdServiceImpl.java` | `@Transactional` service. Calculates waiver reduction amounts per tax head (IGST, CGST, SGST, Cess, ITC). Inserts NonReturnLiabLedger entries with `tranTypeInd=REDUCTION_TRANS`. Updates demand status. | CR27893-B |
| `Core-API/LitigationAPI/.../AppealOrderItemCustomizer.java` | SPL05 (APROD) approval order processing, SPL06 (VORDR) void order debit reversal, SPL07 (ARJOD) rejection status restore — in `createTaskObj()` around lines 1032+ and in DCR block | CR27893-D, D2 |
| `Core-API/LitigationAPI2/.../DemandOrderFetchStrategy.java` | SPL05/SPL06 item availability check — checks if waiver approval/void items exist before allowing certain operations | Lines 557-577 (CR27893-D2) |
| `Core-API/LitigationAPI/.../AppealCaseCustomizer.java` | DCR for appeal on SPL07 rejection — enables taxpayers to file APL01 against waiver rejection | Lines 988+ (CR27893-D2) |
| `Core-API/LitigationAPI2/.../AdjudicationCaseCustomizer.java` | SPL01/SPL02 case creation logic — how waiver application creates a case in the system | CR27893-A |
| `Core-API/LitigationAPI2/.../DemandListServiceImpl.java` | Waiver demand list — retrieves demands eligible for waiver application | CR27893-A |
| `Core-API/LitigationAPI2/.../DemandCtrl.java` | Demand controller endpoints for waiver flows | CR27893-A |
| `Core-API/LitigationAPI2/.../DemandDAOImpl.java` | DAO queries for waiver demand retrieval | CR27893-A |
| `Core-API/LitigationAPI2/.../Drc03LedgerDaoImpl.java` | DRC-03 payment ledger DAO — tracks waiver-related payments | CR27893-C |
| `Core-API/LitigationAPI2/.../Drc03LedgerServiceImpl.java` | DRC-03 ledger service — processes payment confirmations for waiver | CR27893-C |
| `Core-API/LitigationAPI2/.../AdjCommunicationServiceImpl.java` | Email/SMS notifications — auto-approval email, rejection notification | CR27893-D1 |
| `Core-API/LitigationAPI2/.../WaiverValidations.java` | Validation rules for waiver operations | CR27893-B |
| `Core-API/LitigationAPI2/.../CaseCustomizerFactory.java` | Registered WaiverSchemeFolderItemCustomizer as new case type in factory | CR27893-B |
| `BO-Web/BOServicesWeb/.../BORevampViewCtrl.java` | Landing page controller — added waiver route `/auth/landing/waivers` | CR27893 |
| Various constants, VOs, entities | LitApiConstants, LitWebConstants, AdjCommonConstant, CommPayload, Case.java, WithdrawalDtls.java, DemandOrderDetails.java | Multiple sub-CRs |

**What was pre-existing vs what I built:**
- **Pre-existing:** The CaseFolderItemCustomizer interface, the NonReturnLiabLedger framework, the communication framework (email templates), the DRC-03 base module, CaseCustomizerFactory structure
- **What I built:** `WaiverSchemeFolderItemCustomizer` (entirely new class), WaiverLedgerUpdateCtrl + WaiverLdgrUpdServiceImpl (waiver-specific REST + service), SPL05/SPL06/SPL07 order processing in AppealOrderItemCustomizer, DemandOrderFetchStrategy waiver check, appeal-on-SPL07-rejection integration, auto-approval email flow, waiver landing page route

---

### How It Works End-to-End

**The 7 Order Types and My Role in Each:**

```
SPL01 (Application) — Taxpayer submits waiver application
  → AdjudicationCaseCustomizer creates a case with type=WAIVER
  → DemandListServiceImpl fetches eligible demands
  → My code: Case creation logic, demand eligibility query

SPL02 (Payment Confirmation) — Payment is confirmed for waiver
  → Drc03LedgerServiceImpl records the payment
  → My code: DRC-03 ledger entries for waiver payments

SPL03 (Show Cause / Notice) — Officer issues notice to taxpayer
  → WaiverSchemeFolderItemCustomizer.afterAddCaseFolderItem() triggers
  → My code: Created this customizer class, lifecycle hook implementation

SPL05 (Approval Order) — Officer approves waiver
  → WaiverLedgerUpdateCtrl receives request
  → DbContextHolder.setDbType() routes to correct state DB
  → WaiverLdgrUpdServiceImpl calculates per-head reduction amounts
  → Inserts NonReturnLiabLedger with REDUCTION_TRANS (credit entry)
  → Outstanding demand is reduced
  → My code: Controller, service, ledger calculation, demand status update

SPL06 (Void Order) — Officer voids a previously approved waiver
  → AppealOrderItemCustomizer processes VORDR item type
  → Inserts compensating DEBIT_TRANS entry (reverses the SPL05 credit)
  → Restores demand status from origOrdDmdStatusBfrSpl06 field
  → Updates recovery case to RECOVERABLE status
  → My code: Void processing block, status restoration logic

SPL07 (Rejection Order) — Officer rejects waiver application
  → AppealOrderItemCustomizer processes ARJOD item type
  → Creates a case that is appealable (taxpayer can file APL01)
  → AppealCaseCustomizer DCR enables appeal creation against SPL07
  → DemandOrderFetchStrategy checks SPL05/SPL06 availability
  → My code: Rejection processing, appeal integration, demand fetch strategy

Auto-Approval Email — Automated notification after SPL05
  → AdjCommunicationServiceImpl sends email/SMS
  → My code: Email trigger in waiver approval flow (CR27893-D1)
```

---

### Key Code Pattern — SPL06 Void (Compensating Transaction)

```java
// In AppealOrderItemCustomizer — CR27893-D
// When SPL06 (void order) is issued:

// 1. Insert compensating debit to reverse SPL05 credit
nonReturnLedgerReqVO.setTranTypeInd(LedgerConstants.DEBIT_TRANS);  // reversal
nonReturnLedgerReqVO.setTranCd(TRAN_CD_VOID_ORDER);
nonReturnLiabLedgerUtil.insertNonReturnLiabLedger(nonReturnLedgerReqVO);

// 2. Restore demand status to what it was BEFORE the waiver
// origOrdDmdStatusBfrSpl06 stores the pre-waiver status (not hardcoded)
updateDemandReqVO.setDemandStatus(origOrdDmdStatusBfrSpl06);

// 3. Update recovery case status
caseVO.setStatus(RECOVERABLE);  // waiver void = demand is recoverable again
```

**Why `origOrdDmdStatusBfrSpl06` matters:**
The demand could have been in ANY status before the waiver (CREATED, FIRST_APPEAL_ISSUED, RECTIFICATION_ISSUED, etc.). A hardcoded restore value would be wrong. So we snapshot the exact status before SPL05 approval and restore it exactly on SPL06 void.

---

## BULLET 4 — Multi-Tenant Database Routing + Two-Tier Caching + Counter APIs

### Resume Text
> Architected multi-tenant database routing across 28 state jurisdictions using Spring's AbstractRoutingDataSource with ThreadLocal request-scoped context propagation, paired with a two-tier caching strategy — JVM in-process cache for 100+ reference data types loaded at startup via @PostConstruct, and Redis distributed cache for 40+ shared data types with TTL-based eviction — built aggregation counter APIs for officer dashboards that compute real-time case counts (pending, action-required, total) per jurisdiction without redundant database round trips.

---

### What I Was Involved In

**Multi-Tenant Routing:** Every API request in GSTN carries a state code. The platform serves 28 state jurisdictions, each with its own database shard. I work with this pattern daily — every controller I write must set/clear the DB context.

**Counter APIs:** I built specific counter/aggregation APIs for the back-office (BO) dashboard that officers use to see case counts (pending appeals, action-required, total). These needed to be efficient (single SQL with GROUP BY, not N separate queries).

**Two-Tier Caching:** I work within the existing cache architecture — JVM-level `@PostConstruct` initialization for reference data and Redis-based DistCacheFwk for shared mutable data.

---

### Files I Coded In

| File | What I did | Involvement |
|---|---|---|
| `Core-API/LitigationAPI2/.../WaiverLedgerUpdateCtrl.java` | Explicitly sets `DbContextHolder.setDbType(stateCd)` before service call and `clearDbType()` in finally block | Multi-tenant routing — I wrote this controller |
| `Core-API/LitigationAPI2/.../RetDashboardAPI/.../ReturnsServiceImpl.java` | `getCountOfApplnsForBO()` — counter API that computes case counts per jurisdiction per status. Uses single SQL with GROUP BY. | Counter API — I built this |
| `Commons/DistCacheFwk/` | Used for caching shared reference data (case types, status codes, jurisdiction mappings) across instances with TTL | I use this framework in all my APIs |
| `Commons/CommonUtilFwk/.../DbContextHolder.java` | ThreadLocal-based DB context — `setDbType()`, `getDbType()`, `clearDbType()`. AbstractRoutingDataSource reads this. | I call this in every controller I write |
| `Core-API/LitigationAPI/.../ConfigStore.java` | `@PostConstruct` loading of 100+ reference data types into JVM in-memory cache at application startup | I added waiver-related config entries |
| `BO-Web/BOServicesWeb/.../BORevampViewCtrl.java` | Landing page with waiver route — uses cached reference data for dropdown values | I added the waiver landing route |
| Various controllers across LitigationAPI, LitigationAPI2 | Every REST endpoint follows the pattern: setDbType → business logic → clearDbType | Standard pattern in all my code |

**What was pre-existing vs what I built:**
- **Pre-existing:** DbContextHolder, AbstractRoutingDataSource config, DistCacheFwk, ConfigStore base loading
- **What I built:** Counter APIs (getCountOfApplnsForBO), WaiverLedgerUpdateCtrl with explicit DB routing, added waiver-specific config to ConfigStore, ensured correct setDbType/clearDbType in all my controllers

---

### How Multi-Tenant Routing Works

```
1. HTTP Request arrives: POST /v0.1/recovery/updateLedgerEntries
   → Header contains stateCd (e.g., "07" for Delhi)
2. WaiverLedgerUpdateCtrl.updateLedgerEntries():
   → DbContextHolder.setDbType("07")  // ThreadLocal stores "07"
3. Spring's AbstractRoutingDataSource.determineCurrentLookupKey():
   → Reads ThreadLocal → returns "07"
   → Routes to Delhi's database connection pool
4. waiverLdgrUpdServiceImpl.processLedgerEntries():
   → All SQL queries go to Delhi's DB
5. Finally block:
   → DbContextHolder.clearDbType()  // CRITICAL: prevents ThreadLocal leak
   → Without this, next request on same thread goes to Delhi's DB regardless of actual state
```

**Counter API Pattern:**
```java
// Single SQL instead of N+1
SELECT case_status, COUNT(*) 
FROM cases 
WHERE state_cd = ? AND jurisdiction_cd = ?
GROUP BY case_status
// Returns: {PENDING: 45, ACTION_REQUIRED: 12, COMPLETED: 230}
// Instead of 3 separate COUNT queries
```

---

## BULLET 5 — Plugin-Based Case Lifecycle Framework + Cross-Cutting Validation

### Resume Text
> Designed a plugin-based case lifecycle framework using Strategy + Factory patterns supporting 20+ legally distinct proceeding types — each type registers a CaseCustomizer and CaseFolderItemCustomizer with pre/post lifecycle hooks, configurable transaction modes (XA vs non-XA), and type-specific validation rules; built a reusable cross-cutting validation layer handling jurisdiction eligibility, officer role authorization, simultaneous appeal detection, and financial amount consistency checks — enabling new case types (including waiver scheme types) to be onboarded by adding one customizer class with zero changes to framework code.

---

### What I Was Involved In

**Framework Extension (Not Framework Creation):** The Strategy + Factory pattern (CaseCustomizer interface + CaseCustomizerFactory) was pre-existing. My contribution was:
1. **Created `WaiverSchemeFolderItemCustomizer`** — a brand new customizer class implementing the CaseFolderItemCustomizer interface, registered in the factory for waiver case types (SPL01-SPL07). This is the **proof** that the framework is extensible: I onboarded an entirely new business domain (waiver scheme) by adding one class + one factory registration, zero changes to CaseHandler or CaseService.
2. **Extended `AppealCaseCustomizer`** with subsequent order logic (CR28625A)
3. **Extended `AppealOrderItemCustomizer`** with 12 subsequent order scenarios + waiver order types
4. **Built validation methods in `AppealValidations`** — cross-cutting checks used by multiple case types

---

### Files I Coded In

| File | What I built | Pattern role |
|---|---|---|
| `Core-API/LitigationAPI2/.../WaiverSchemeFolderItemCustomizer.java` | **New class.** Implements CaseFolderItemCustomizer. afterAddCaseFolderItem() hook processes waiver-specific lifecycle events. | Strategy implementation (new plugin) |
| `Core-API/LitigationAPI2/.../CaseCustomizerFactory.java` | Registered waiver case type → WaiverSchemeFolderItemCustomizer mapping | Factory extension |
| `Core-API/LitigationAPI/.../AppealCaseCustomizer.java` | Extended with subsequent order demand stay, appeal-on-SPL07 DCR | Strategy implementation (extended existing) |
| `Core-API/LitigationAPI/.../AppealOrderItemCustomizer.java` | Extended with 12 subsequent scenarios + SPL05/SPL06/SPL07 processing | Strategy implementation (extended existing) |
| `Core-API/LitigationAPI2/.../AppealValidations.java` | Cross-cutting validations: getCaseStatusForWithdrawReject(), getCountOfAppealApplications(), isSimulCombinedOrd(), isEligibleToProvideEffect() | Validation layer (@Component) |
| `Commons/CaseMgmtFwk/.../GenericCaseCustomizer.java` | Template method base class — I extended this pattern | Template Method pattern (pre-existing) |
| `Commons/CaseMgmtFwk/.../CaseHandler.java` | Facade that delegates to the correct customizer via factory | Facade pattern (pre-existing, I use it) |

**What was pre-existing vs what I built:**
- **Pre-existing:** CaseCustomizer interface, CaseCustomizerFactory, CaseHandler facade, GenericCaseCustomizer base class, the overall plugin architecture
- **What I built:** WaiverSchemeFolderItemCustomizer (entirely new plugin class), AppealValidations cross-cutting methods, extensions to AppealCaseCustomizer and AppealOrderItemCustomizer, waiver case type registration in factory

---

### How the Plugin Framework Works

```
1. Request: "Add SPL05 approval order to waiver case"
2. CaseHandler.addCaseFolderItem(case, item) — Facade
3. CaseCustomizerFactory.getCustomizer(case.getCaseTypeCd())
   → caseTypeCd = "WAIVER" → returns WaiverSchemeFolderItemCustomizer
4. customizer.beforeAddCaseFolderItem(case, item) — pre-hook validation
5. Framework persists item to database
6. customizer.afterAddCaseFolderItem(case, item) — post-hook
   → My code: triggers WaiverLedgerUpdateCtrl to create ledger entries
   → My code: sends email notification
7. Framework returns response

Adding a new case type (e.g., SPL08):
→ Create SPL08CaseFolderItemCustomizer implements CaseFolderItemCustomizer
→ Add one case in CaseCustomizerFactory: "SPL08" → new SPL08CaseFolderItemCustomizer()
→ Zero changes to CaseHandler, CaseService, or any existing customizer
→ This is the Open/Closed Principle in action
```

---

### Cross-Cutting Validation Layer

```java
// AppealValidations.java — @Component, injected across multiple services

// 1. Jurisdiction eligibility
public boolean isEligibleToProvideEffect(Case caseVO, String stateCd) {
    // Checks: does officer's jurisdiction match case jurisdiction?
    // Used before ANY order can be passed
}

// 2. Simultaneous appeal detection (CR28625A)
public boolean isSimulCombinedOrd(String origDmndId) {
    // Checks: does this demand have both APL01 and APL03 active?
    // Determines if subsequent order logic applies
}

// 3. Application count check
public int getCountOfAppealApplications(String demandId) {
    // Prevents duplicate appeal filing on same demand
}

// 4. Case status validation
public String getCaseStatusForWithdrawReject(Case caseVO) {
    // Determines valid transitions for withdrawal/rejection
}
```

---

## OVERALL SUMMARY — My Contribution Map

| Area | My Role | Evidence |
|---|---|---|
| **Subsequent Order (CR28625A)** | Designed and implemented 12-scenario financial engine | ~40 files, AppealOrderItemCustomizer 8500-8910+ |
| **Waiver Scheme (CR27893)** | Built entire waiver lifecycle across 6 sub-CRs | ~55 files, WaiverSchemeFolderItemCustomizer (new class) |
| **Concurrency Control** | Used defense-in-depth pattern (Redis + @Version + XA) | WaiverLedgerUpdateCtrl, all order issuance paths |
| **Multi-Tenant Routing** | Applied DbContextHolder pattern in every controller | Standard pattern across all my APIs |
| **Counter APIs** | Built BO dashboard aggregation APIs | ReturnsServiceImpl.getCountOfApplnsForBO() |
| **Plugin Framework Extension** | Created new customizer, registered in factory | WaiverSchemeFolderItemCustomizer = proof of extensibility |
| **Cross-Cutting Validation** | Built reusable validation methods | AppealValidations — used across 10+ flows |

**Total code footprint:** ~95 unique files across LitigationAPI, LitigationAPI2, CaseMgmtFwk, DCR, BO-Web
**Primary CRs:** CR28625A (~40 files) + CR27893 A-D2 (~55 files)
**Key new artifacts I created from scratch:** WaiverSchemeFolderItemCustomizer, WaiverLedgerUpdateCtrl, WaiverLdgrUpdServiceImpl, WaiverValidations

---

*Last Updated: April 2026*
*Companion to: Resume_Bullets_Final.md (v2)*
*Backed by: actual codebase exploration of CR28625A and CR27893 across GSTN Maintrunk*
