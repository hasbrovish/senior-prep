# How to Add These Files to Your senior-prep Repo

## Step 1: Copy Interview_Answers
```bash
cd ~/Documents/dev/senior-prep
cp -r /path/to/downloaded/Interview_Answers .
```

## Step 2: Replace knowledge_base.py
```bash
cp /path/to/downloaded/intel/knowledge_base.py intel/knowledge_base.py
```

## Step 3: Re-index the Knowledge Base
```bash
python3 -m intel.knowledge_base --init --force
```

## Step 4: Verify
```bash
python3 -m intel.knowledge_base --stats
# Should show: 284 chunks, 23 sources, 6 categories

python3 -m intel.knowledge_base --search "kafka consumer lag"
# Should return relevant results from Section_04_05_06
```

## Step 5: Commit
```bash
git add Interview_Answers/ intel/knowledge_base.py
git commit -m "feat: add Interview_Answers KB (17 files, 1790 lines) + enhance RAG search

- Created all 17 Interview_Answers files expected by knowledge_base.py
- Content covers: Java Core, Spring Boot, Microservices/Kafka/Redis,
  Databases, System Design, DSA Patterns, LLD, Behavioral/STAR,
  FAANG Advanced, Company-Specific, OA Patterns
- All answers anchored to GSTN experience (14M users, 100K concurrent)
- Covers flagged weak areas: SLF4J/Logback, Spring Profiles, @Value
- Enhanced knowledge_base.py: domain-specific keyword boosting,
  bigram extraction, heading-based scoring
- KB now fully indexed: 23 sources, 284 chunks, 6 categories"
git push
```

## What Was Created

| File | Category | Content |
|------|----------|---------|
| Section_01_Java_Core.md | java | JVM, GC, HashMap, concurrency, streams (Q1-Q25) |
| Section_02_Spring_Boot.md | java | DI, @Transactional, Profiles, @Value, SLF4J, Security (Q26-Q60) |
| Section_04_05_06_*.md | java | Microservices, Kafka deep dive, Redis data structures (Q91-Q135) |
| Section_07_08_*.md | system_design | Indexing, sharding, SQL optimization, consensus (Q136-Q165) |
| Section_21_SystemDesign_*.md | system_design | 8 full designs with estimation + tradeoffs |
| GSTN_Architecture_Reference.md | system_design | Full GSTN architecture (your #1 interview asset) |
| Section_LLD_Complete.md | lld | 6 LLD problems + SOLID + patterns reference |
| Section_DSA_Java_Patterns.md | dsa | 8 patterns with Java templates + complexity |
| Amazon_LP_STAR_Bank.md | behavioral | 8 LP stories mapped to your experience |
| Section_20_FAANG_*.md | general | Advanced questions for Google/Stripe/Anthropic level |
| Company_Questions_Phase1.md | general | Razorpay, Juspay, CRED, MakeMyTrip prep |
| Company_Questions_Phase2.md | general | Amazon, Google, Stripe, Anthropic, Goldman prep |
| OA_Patterns_*.md | dsa | OA patterns, mock structure, revision schedule |
| Section_Modern_Java_*.md | java | Java 11-21 features, observability, CQRS |
| Section_Behavioral_DB_Golang.md | behavioral | Behavioral answers, DB deep dive, Go patterns |
| Section_SD_Consumer_Products.md | system_design | Twitter, Instagram, Uber, YouTube, WhatsApp designs |
| GSTN_Complete_*.md | general | Mock rounds, code walkthroughs |
