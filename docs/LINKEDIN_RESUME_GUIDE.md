# LinkedIn + Resume Guide — Jayanti Vishnoi
# Goal: Maximum shortlist rate from career sites + referrals at top companies
# Both documents must work in 30 seconds — that's all recruiters give them

---

## THE 30-SECOND RULE

```
Recruiter on career site:     Reviews 200+ resumes per role.
                               Your resume has 10–15 seconds.
                               They look at: Title → Company → Bullet 1 → Skills.

Recruiter on LinkedIn:        Searches: "Java AND Kafka AND Spring Boot AND Bangalore"
                               Your profile must surface in that search.
                               They look at: Headline → Current role → About (first 2 lines).

Hiring manager referral:      Reads more carefully — 1-2 minutes.
                               They look at: What did you build? At what scale? What impact?

Your job: Pass the 30-second screen. Everything else happens in the interview.
```

---

# PART 1 — LINKEDIN

## Profile Completeness Checklist (do ALL of these)

- [ ] Professional photo (not selfie — light background, business casual, smiling)
- [ ] Headline optimized (see formula below)
- [ ] Location: Bengaluru, Karnataka, India
- [ ] Open to Work: ON — Visible to recruiters only (not public)
- [ ] About section written (see template below)
- [ ] All 3 GSTN experience entries with bullet points
- [ ] 10+ skills listed (ATS keywords — see list below)
- [ ] Skills endorsed by colleagues (ask 3-4 ex-GSTN colleagues)
- [ ] Education complete
- [ ] Featured section: link to GitHub project
- [ ] 500+ connections (actively connect with engineers at target companies)
- [ ] Activity: 1 post per week (even just sharing an article with 1 comment)

---

## Headline Formula

**BAD:** "Software Developer at GSTN"
**BAD:** "Java Developer | Spring Boot | Microservices"
**GOOD:**

```
Backend Engineer | Java · Spring Boot · Kafka · Redis · Microservices | 5.5 YOE | Open to SDE-2/SDE-3
```

**Why this works:**
- "Backend Engineer" — what recruiters search for
- Specific tech stack — ATS keyword match for Java, Kafka, Redis
- 5.5 YOE — immediately signals experience band
- "Open to SDE-2/SDE-3" — removes ambiguity about what you want

**Alternative if you want fintech emphasis:**
```
Backend Engineer | Java · Spring Boot · Kafka · Distributed Systems | GSTN (14M users) | SDE-2/SDE-3
```

---

## About Section Template

```
I'm a backend engineer with 5.5 years of experience building large-scale, high-reliability
distributed systems at GSTN — India's national tax infrastructure serving 14 million
registered taxpayers and processing 3 billion+ invoices per year.

My core stack: Java 11/17, Spring Boot, Hibernate, Apache Kafka, Redis (JBoss DataGrid),
MySQL, HBase, Docker, Kubernetes, AWS, Golang.

What I've built at GSTN:
• Distributed cache layer (JBoss DataGrid + EhCache) reducing DB load by 40% across 45+ microservices
• Kafka consumer framework with DLQ and exactly-once semantics for async event processing
• XA distributed transaction system (Atomikos JTA) ensuring consistency across appeal, ledger, and notification services
• Case workflow engine using Strategy + Factory pattern, supporting 10+ adjudication case types
• Real-time ledger processing with HBase (petabyte scale) + MySQL (ACID compliance)

I'm now looking for SDE-2 or SDE-3 roles at product-based companies where I can apply
this distributed systems experience to consumer-scale products.

Open to: Backend / Platform / Infrastructure engineering roles.
Location: Bangalore (open to hybrid/remote)
```

**Key rules for About:**
- First 2 lines visible without expanding — make them count
- Numbers everywhere: 14M, 45+, 40%, 3B+
- Stack keywords in the body (ATS indexing)
- Clear intent at the end

---

## Experience — How to Write Each Bullet

**Formula:** `[Action verb] [what you built] [technology] → [metric impact]`

### GSTN Entry (your main role) — write it like this:

**Title:** Specialist Programmer L2 (equivalent: Backend Engineer / SDE-2)
**Company:** GSTN — Goods & Services Tax Network
**Duration:** [Start date] – Present · 5 years 6 months
**Location:** Delhi/Noida, India

**Bullets (copy-paste these, adjust with your actual numbers):**

```
• Architected distributed caching layer using JBoss DataGrid + EhCache across 45+
  Spring Boot microservices, reducing database load by ~40% during peak filing season
  serving 14M+ registered taxpayers

• Built Kafka consumer framework with pluggable processor interface, 3-tier error handling
  (main → error → DLQ), and scheduled retry — achieving exactly-once event processing
  across 10+ async pipelines

• Implemented XA distributed transactions (Atomikos JTA) coordinating across Appeal,
  Ledger, and Notification services — ensuring ACID compliance for tax credit operations
  worth thousands of crores

• Designed case management workflow engine using Strategy + Factory patterns supporting
  10+ litigation case types (appeals, adjudication, tribunal orders) with full audit trails

• Built tax ledger operations on HBase (petabyte scale) + MySQL, handling 300Cr+ invoices
  per year with < 2 second SLA during peak filing (July 31 deadline)
```

---

## Skills Section — ATS Keywords (add ALL of these)

```
Core (add these first — highest search frequency):
  Java, Spring Boot, Spring Framework, Microservices, Apache Kafka, Redis,
  Hibernate, JPA, REST API, Distributed Systems, MySQL, Docker, Kubernetes

Secondary (add these next):
  HBase, MongoDB, Apache Solr, JMS, JTA, Atomikos, Spring Security,
  Spring Batch, Spring Cloud, JUnit, Mockito, Maven, Git, CI/CD

Platform:
  AWS, Linux, Docker Compose

Bonus (if you've touched these):
  Go (Programming Language), Golang, Angular, Python, PostgreSQL
```

---

## Activity Strategy (what actually gets recruiter DMs)

```
1. Post once per week minimum. Options:
   → Share an article about Java/Kafka/distributed systems with 2 lines of your take
   → Share a LeetCode problem you found interesting + what you learned
   → Share a system design insight from your prep

2. Comment on posts from senior engineers at target companies (shows up in their followers)

3. Connect with recruiters at: PhonePe, Razorpay, Swiggy, Amazon, Flipkart
   → "Hi [name], I'm a backend engineer with 5.5 YOE in Java/Kafka distributed systems.
      I'm exploring SDE-2/SDE-3 opportunities. Would love to connect."

4. Join groups: "Software Engineers in India", "Java Developers", "Backend Engineering"
```

---

# PART 2 — RESUME

## Non-Negotiable Rules

```
1. ONE PAGE. No exceptions. Senior engineers with 10+ years can do 2 pages. You cannot.
2. PDF format only. Never Word (formatting breaks in ATS).
3. No photo. No date of birth. No marital status. (Indian resumes often include these — don't)
4. ATS-friendly font: Calibri, Arial, Helvetica (size 10-11 for body, 14-16 for name)
5. No tables, no columns, no graphics (ATS cannot parse these)
6. File name: Jayanti_Vishnoi_Backend_Engineer_Resume.pdf
7. Contact: Email + LinkedIn URL + GitHub URL + Mobile (optional)
8. No "Objective" section. Wastes space.
```

---

## Resume Structure (in this exact order)

```
[NAME — large, bold]
[Email] | [LinkedIn URL] | [GitHub URL] | [Mobile] | Bangalore, India

SKILLS
─────────
[One dense section with all tech keywords]

EXPERIENCE
─────────
[Most recent job first]

PROJECTS
─────────
[GitHub project — brief but impactful]

EDUCATION
─────────
[Degree, university, year]
```

---

## Full Resume Template (copy and fill in)

---

**JAYANTI VISHNOI**
jayanti@email.com | linkedin.com/in/jayanti-vishnoi | github.com/jayanti-vishnoi | +91-XXXXXXXXXX | Bangalore, India

---

**SKILLS**

**Languages:** Java 11/17, Golang, SQL, JavaScript
**Frameworks:** Spring Boot, Spring MVC, Spring Security, Spring Batch, Hibernate/JPA
**Distributed:** Apache Kafka, Redis (JBoss DataGrid), HBase, Apache Solr, Atomikos JTA
**Databases:** MySQL, MongoDB, HBase
**Infrastructure:** Docker, Kubernetes, AWS (EC2, S3, RDS, SQS), Linux, Maven, Git, Jenkins

---

**EXPERIENCE**

**Specialist Programmer L2 (SDE-2)** | GSTN — Goods & Services Tax Network | [Year]–Present
*Backend engineer for India's national tax infrastructure — 14M+ taxpayers, 45+ microservices, 3B+ annual transactions*

- Designed distributed cache layer (JBoss DataGrid + EhCache) across 45+ Spring Boot microservices, **reducing database load ~40%** during peak GST filing season
- Built Kafka consumer framework with pluggable processor interface and 3-tier DLQ error handling, enabling **exactly-once event processing** across 10+ async pipelines
- Implemented XA distributed transactions (Atomikos JTA) coordinating appeal, ledger, and notification services — ensuring ACID consistency for tax credit operations
- Designed case workflow engine using **Strategy + Factory patterns** supporting 10+ litigation case types with configurable state machines and audit trails
- Optimised HBase read path with composite row key design (GSTIN|Period|ReturnType), supporting **300Cr+ annual invoice** retrieval at < 2s SLA during peak load

[Previous role if any — brief, 2-3 bullets]

---

**PROJECTS**

**Kafka Event Pipeline with DLQ** | Java 17, Spring Boot 3, Apache Kafka, Docker Compose
- Production-grade Kafka consumer framework with pluggable processor, 3-tier error handling (main → error → DLQ), scheduled retry, and exactly-once semantics
- github.com/jayanti-vishnoi/kafka-pipeline

---

**EDUCATION**

**B.Tech / MCA / [Your Degree]** — [University Name] — [Year] — [CGPA if > 7.5]

---

## Bullet Writing Rules — The Difference Between Shortlisted and Ignored

**Pattern: Action + What + Tech + Number**

❌ WEAK: "Worked on distributed caching using Redis"
✅ STRONG: "Designed JBoss DataGrid + EhCache layer across 45+ microservices, reducing DB load ~40%"

❌ WEAK: "Developed Kafka consumers for event processing"
✅ STRONG: "Built Kafka consumer framework with pluggable processor + DLQ retry, enabling exactly-once semantics across 10+ pipelines"

❌ WEAK: "Built REST APIs for litigation workflow"
✅ STRONG: "Designed case management engine using Strategy + Factory patterns for 10+ litigation case types serving 2M+ litigation cases"

**Numbers to use (rough estimates are fine):**
- 14M+ taxpayers
- 45+ microservices
- 3B+ invoices/year
- 300Cr+ tax credits
- ~40% DB load reduction
- < 2s SLA
- 10+ case types
- 32+ shared frameworks

---

## Tailoring for Specific Companies

### For Amazon / Flipkart (product e-commerce)
- Lead with SCALE: "serving 14M users", "3B+ transactions"
- Use: "designed", "architected", "built"
- Add: reliability, availability, SLA mentions

### For Goldman / Morgan Stanley (finance)
- Lead with CONSISTENCY: "ACID compliance", "XA transactions", "audit trails"
- Use: "financial data", "tax ledger", "credit settlement"
- Add: compliance, correctness, zero data loss

### For PhonePe / Razorpay (fintech)
- Lead with PAYMENTS ANALOGY: "tax credit settlement = payment settlement"
- Use: "idempotency", "distributed transactions", "reconciliation"
- Add: exactly-once, retry, DLQ

### For Swiggy / Zomato (logistics tech)
- Lead with EVENT PROCESSING: "real-time", "async", "Kafka pipelines"
- Mention: consumer lag, throughput, fault tolerance

---

## ATS Optimisation Checklist

```
Before submitting to any company:
  [ ] Job description keywords match resume keywords (copy key terms exactly)
  [ ] "Java" appears at least 3x in resume
  [ ] "Spring Boot" appears at least 2x
  [ ] "Microservices" appears at least once
  [ ] Numbers in every experience bullet
  [ ] No tables, no columns
  [ ] Saved as PDF
  [ ] File under 500KB
  [ ] Proofread: zero typos (typos = immediate rejection at FAANG screening)
```

---

## Referral Strategy — This Doubles Your Callback Rate

```
Step 1: Find connection
  LinkedIn search: "[Company name]" + "Software Engineer" + "India" + "Bengaluru"
  Also search: "[Company name]" + "GSTN" (any GSTN alumni who moved to that company)

Step 2: Message template (COPY THIS EXACTLY)
  ─────────────────────────────────────────
  Hi [Name],

  I'm Jayanti Vishnoi, a backend engineer with 5.5 years of Java/Kafka
  distributed systems experience at GSTN (India's tax infrastructure).

  I'm actively exploring SDE-2/SDE-3 backend roles and [Company] is my
  top choice because of [1 specific reason — their tech blog, their product,
  a talk their engineer gave].

  Would you be open to referring me? I'd be happy to share my resume.
  No pressure at all — I completely understand if you'd prefer not to.

  Thanks,
  Jayanti
  ─────────────────────────────────────────

Step 3: Follow up once (5 days later) if no reply. Don't chase more than twice.

Step 4: When they say yes — send resume + job link immediately. Make it easy for them.

Referral statistics (2025-2026 India tech):
  Cold application callback rate:    8–15%
  With referral callback rate:       35–55%
  GSTN alumni at target companies:   Amazon (many), Goldman (some), Flipkart (some)
```

---

## Career Site vs Referral — Which to Use

| Method | Callback Rate | Best For |
|---|---|---|
| Company career site (cold) | 8–15% | All companies — always apply |
| LinkedIn Easy Apply | 5–12% | Lower volume roles, not FAANG |
| Employee referral | 35–55% | Priority — use for every dream company |
| Recruiter DM | 20–40% | If recruiter contacts you |
| Job portal (Naukri/LinkedIn Jobs) | 8–15% | Good for visibility, esp. Tier 3 |

**Strategy: Apply via career site AND get referral simultaneously. Don't wait for referral to apply.**

---

*Updated: March 2026 | Revise this after every 10 applications based on your callback rate*
