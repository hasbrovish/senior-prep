# DAY 1 TO INTERVIEW-READY
## The Complete Self-Study Guide — Backend Engineering + GenAI
### For a developer with 5 years experience, full-time availability, starting from scratch

---

## THE REALITY CHECK

You have NO job right now. That's not a weakness — it's a **strategic advantage.**

Most people prep while working 8 hours and studying 2 hours in the evening half-asleep. You can do 6-8 focused hours per day. That means what takes others 6 months, you can compress into **12-14 weeks** if you're disciplined.

But here's the trap: having all day means you'll be tempted to study 10 hours, burn out in week 2, and quit. Don't.

**Your daily budget: 6 hours of FOCUSED study. Not 10. Not 8. Six.**

The rest of your day: exercise, eat well, sleep 8 hours, talk to humans. This is a marathon that you're running at sprint pace. Recovery matters.

---

## THE SPLIT: BACKEND PREP vs GENAI

You need BOTH. Here's how to split your time:

```
Weeks 1-6:   70% Backend Fundamentals + DSA  |  30% GenAI Learning
Weeks 7-10:  50% System Design + LLD         |  50% GenAI Projects
Weeks 11-14: 60% Mock Interviews + Polish     |  40% GenAI Portfolio
```

Why this split? Backend fundamentals are the foundation. Without them, your GenAI knowledge has nothing to stand on. But GenAI is your differentiator — the thing that makes you more than "another backend developer."

---

## YOUR DAILY SCHEDULE (Full-Time Study)

```
7:00 AM    — Wake up, exercise (even 20 min walk)
8:00 AM    — Session 1: DSA Problems (90 min, deep focus)
9:30 AM    — 15 min break
9:45 AM    — Session 2: Backend Concepts (90 min — read, whiteboard, take notes)
11:15 AM   — Break / Lunch
12:30 PM   — Session 3: GenAI Learning (90 min — course + hands-on coding)
2:00 PM    — 15 min break
2:15 PM    — Session 4: Practice/Build (90 min — varies by week)
             Week 1-6:  SQL problems OR System Design reading
             Week 7-10: LLD problems OR System Design practice
             Week 11-14: Mock interviews OR GenAI project
3:45 PM    — Done for the day
4:00 PM    — Review: 15 min write notebook entry
             Evening: REST. Do NOT study. Your brain consolidates while resting.
```

**Total: 6 hours focused work. 4 sessions × 90 minutes.**

This is based on research on deliberate practice. Beyond 4-5 hours of deep focus per day, quality drops sharply. Don't fight biology.

---

## PHASE 1: FOUNDATION (Weeks 1-6)

### BACKEND FUNDAMENTALS — THE CURATED RESOURCES

**I'm giving you THE ONE resource per topic. Not 10 options. The one that works.**

---

#### 1. DSA (Every single day, Session 1)

**THE resource: NeetCode 150**
→ https://neetcode.io/practice

Why this one: Pattern-based, not random. Grouped by technique (Two Pointers, Sliding Window, etc.). Video explanations for every problem. This is what 90% of people who crack FAANG used.

**THE video explanations: NeetCode YouTube**
→ https://youtube.com/@NeetCode

**How to use it (daily routine):**

```
Week 1-2: Arrays, Two Pointers, Sliding Window, Stack
  → 2-3 problems per day
  → Watch NeetCode video AFTER attempting for 25 min
  → Write the pattern in your own words in notebook

Week 3-4: Binary Search, Linked Lists, Trees
  → Same pace
  → Focus on recognizing WHEN to use each pattern

Week 5-6: Graphs (BFS/DFS), Heap, DP basics
  → Graphs are critical for DoorDash and Amazon
  → DP: just learn the framework, not 100 problems
```

**The problem-solving protocol (use this EVERY time):**

```
1. Read problem. Identify: what pattern does this look like?
2. Try solving for 25 minutes. Whiteboard first, then code.
3. If stuck after 25 min → watch NeetCode video
4. Code the solution yourself (don't copy-paste)
5. Next day: re-solve yesterday's problems from memory
6. Mark in tracker: "solved clean" or "needed help"
```

**Don't do this:** Solve 5 easy problems and feel productive. Do 2 mediums properly instead.

---

#### 2. OPERATING SYSTEMS + NETWORKING + DB INTERNALS (Session 2, Weeks 1-3)

**THE resource for OS: Operating Systems: Three Easy Pieces (FREE)**
→ https://pages.cs.wisc.edu/~remzi/OSTEP/

Why: Written by professors, free, explains with humor, covers exactly what interviews ask. Read Chapters: 4-7 (Processes), 26-33 (Concurrency — this is GOLD for Java multithreading interviews), 13-24 (Memory — skim).

**THE resource for Networking: Computer Networking: A Top-Down Approach**
→ If you don't want to buy the book, use:
→ **Hussein Nasser YouTube** — https://youtube.com/@haborhossain
→ Specifically these playlists:
  - "Fundamentals of Networking" 
  - "Backend Communication Design Patterns"

Topics to cover (2-3 days each):
- TCP vs UDP (handshake, reliability, congestion control)
- HTTP/1.1 vs HTTP/2 vs HTTP/3 (multiplexing, server push)
- TLS handshake (high level)
- DNS resolution (recursive, iterative)
- WebSocket vs SSE vs Long Polling
- REST vs gRPC (when to use which)
- L4 vs L7 load balancers

**THE resource for Database Internals: DDIA Chapters 2, 3, 7**
→ "Designing Data-Intensive Applications" by Martin Kleppmann
→ **This is the #1 most important book for system design interviews. Buy it.**

Chapters to read in this phase:
- Chapter 2: Data Models and Query Languages (relational vs document)
- Chapter 3: Storage and Retrieval (B-trees, LSM trees, SSTables) — THIS chapter alone is worth the book price
- Chapter 7: Transactions (ACID, isolation levels, MVCC)

**THE companion: Jordan Has No Life YouTube**
→ https://youtube.com/@jordanhasnolife5163
→ He literally goes through DDIA chapter by chapter on video

**DB Design Practice (from your 5-step framework):**
→ Do 1 schema design per week alongside reading
→ Week 1: E-commerce (Amazon)
→ Week 2: Food Delivery (DoorDash)
→ Week 3: Social Media (Instagram)

**SQL Practice:**
→ **LeetCode Database Problems** — https://leetcode.com/problemset/database/
→ Do 3-4 SQL problems per week during Session 4
→ Focus on: JOINs, Window Functions, GROUP BY with HAVING, CTEs

---

#### 3. JVM + JAVA CONCURRENCY (Session 2, Weeks 4-6)

**THE resource: Java Concurrency in Practice by Brian Goetz**
→ Read Chapters: 1-5 (Thread Safety, Sharing Objects, Building Blocks), 8 (Thread Pools), 10 (Deadlock), 11-12 (Performance, Testing)

**THE video companion: Jakob Jenkov's Java Concurrency Tutorial**
→ https://jenkov.com/tutorials/java-concurrency/index.html
→ Free, text-based, extremely clear. Better than most video courses.

**THE practical exercises (code these yourself):**
```
Week 4:
  - Implement Producer-Consumer with wait/notify
  - Implement Producer-Consumer with BlockingQueue
  - Create a deadlock, then fix it
  - Implement Singleton: lazy, eager, double-checked, enum

Week 5:
  - Build a custom ThreadPool from scratch
  - Use CompletableFuture to chain 3 async operations
  - Implement ReadWriteLock usage example
  - ConcurrentHashMap vs synchronized HashMap benchmark

Week 6:
  - Write a simple REST API with Spring Boot
  - Use @Transactional with different propagation levels
  - Implement @ControllerAdvice exception handling
  - Take thread dump with jstack, analyze it
```

**Spring Boot (practical, not theoretical):**
→ **Baeldung** — https://www.baeldung.com
→ Don't read tutorials passively. Build the examples.
→ Key articles to work through:
  - "Introduction to Spring Boot"
  - "Spring Bean Scopes"
  - "Guide to @Transactional"
  - "Exception Handling in Spring MVC"

---

### GENAI LEARNING (Session 3, Weeks 1-6)

**THE learning path — in this exact order:**

This is critical. Don't jump to building agents before understanding the fundamentals. Here's the sequence:

```
Week 1: HOW LLMs WORK (conceptual understanding)
Week 2: PROMPT ENGINEERING (the skill that makes everything else work)
Week 3: RAG FUNDAMENTALS (the most in-demand GenAI skill)
Week 4: LANGCHAIN BASICS (the framework)
Week 5: LANGGRAPH + AGENTS (where the real value is)
Week 6: BUILD YOUR FIRST PROJECT
```

#### Week 1: Understanding LLMs

**THE resource: 3Blue1Brown — "But What Is a GPT?"**
→ https://youtube.com/@3blue1brown — Neural Networks playlist
→ Watch: "But what is a GPT? Visual intro to Transformers"
→ You don't need to understand the math. You need to understand:
  - What tokens are and why they matter
  - What a context window is
  - Why LLMs hallucinate
  - What temperature and top-p do
  - Why embeddings matter

**Also read (1 hour):**
→ Anthropic's "Claude's Constitution" — understand how AI companies think about safety
→ OpenAI's "Prompt Engineering Guide" — https://platform.openai.com/docs/guides/prompt-engineering

#### Week 2: Prompt Engineering

**THE resource: DeepLearning.AI — "ChatGPT Prompt Engineering for Developers"**
→ https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/
→ FREE, 1.5 hours, taught by Andrew Ng + OpenAI
→ Co-created by the people who built the models

**Practice:** After the course, spend 2-3 days trying these techniques:
- System prompts: Write 5 different system prompts for different use cases
- Few-shot prompting: Give examples to get structured output
- Chain-of-thought: Make the model reason step by step
- Output parsing: Get JSON output reliably

#### Week 3: RAG Fundamentals

**THE resource: DeepLearning.AI — "LangChain: Chat with Your Data"**
→ https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/
→ FREE, covers the full RAG pipeline: loading, splitting, embedding, retrieval, generation

**THE deeper resource: Activeloop "RAG Course"**
→ https://learn.activeloop.ai/courses/rag
→ FREE, goes from basic to advanced RAG, includes real projects
→ 25+ lessons, 10 practical projects
→ Taught with LangChain + LlamaIndex

**Concepts you MUST understand after this week:**
```
- Document loading and chunking (why chunk size matters)
- Embeddings (what they are, how they work)
- Vector databases (what they store, how similarity search works)
- The RAG pipeline: Query → Embed → Retrieve → Augment → Generate
- Why basic RAG fails (wrong chunks retrieved, lost context)
```

#### Week 4: LangChain Foundations

**THE resource: LangChain Academy (FREE, from the creators)**
→ https://academy.langchain.com/courses/intro-to-langgraph
→ Official, free, maintained by LangChain team
→ Modules 0-3: Setup, basics, chains, state management

**Also do: DeepLearning.AI — "LangChain for LLM Application Development"**
→ https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/
→ FREE, taught by Harrison Chase (LangChain founder)

**Build while learning:**
→ Take the RAG pipeline from Week 3
→ Rebuild it using LangChain components
→ Notice what the framework simplifies vs. what it adds

#### Week 5: LangGraph + Agents

**THE resource: LangChain Academy — Full Course (FREE)**
→ https://academy.langchain.com/courses/intro-to-langgraph
→ Modules 4-6: Agents, multi-agent systems, deployment
→ This is the official course from the people who built it

**THE video supplement: DeepLearning.AI — "AI Agents in LangGraph"**
→ https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
→ Taught by LangChain and Tavily founders
→ Build an agent from scratch, then rebuild with LangGraph

**Key concepts to master:**
```
- ReAct pattern (Reasoning + Acting)
- Tool use / Function calling
- Agent state management
- Memory: short-term (context window) vs long-term (database)
- Human-in-the-loop patterns
- Multi-agent orchestration
```

#### Week 6: Build Your First GenAI Project

**Project: "Document Q&A Assistant"**
Build a RAG application that:
1. Loads PDF documents (use your DDIA book notes!)
2. Chunks and embeds them
3. Stores in a vector database (start with FAISS, then try pgvector)
4. Has a chat interface where you can ask questions
5. Returns answers WITH source citations
6. Has conversation memory

Tech stack: Python + FastAPI + LangChain + FAISS + Streamlit frontend

**Why this project:** It demonstrates RAG, embeddings, vector databases, API design, and is genuinely useful for your own study.

→ Push to GitHub. Write a good README. This is portfolio piece #1.

---

## PHASE 2: DEPTH + PRACTICE (Weeks 7-10)

### Session 1: DSA continues (harder problems)

```
Week 7-8: Revisit weak patterns, add Hard problems
  → Go back to NeetCode 150 problems you marked "needed help"
  → Solve them again without looking
  → Add company-tagged problems from your interview prep guide

Week 9-10: Timed practice
  → Set timer: 25 min for Medium, 40 min for Hard
  → Practice explaining your approach out loud while coding
  → This simulates the actual interview
```

### Session 2: System Design + LLD

**THE System Design resource: Alex Xu's System Design Interview Vol 1**
→ Buy the book. Read one chapter per day.
→ Each chapter IS one system design problem.

**THE System Design video: ByteByteGo YouTube**
→ https://youtube.com/@ByteByteGo
→ Watch the video version of whatever chapter you just read

**THE free alternative: System Design Primer on GitHub**
→ https://github.com/donnemartin/system-design-primer
→ Comprehensive, free, covers everything

**THE LLD resource: Concept && Coding YouTube**
→ https://youtube.com/@ConceptandCoding
→ Best LLD tutorials in Java
→ Watch: Parking Lot, Elevator, BookMyShow, Vending Machine

**Also use:**
→ https://github.com/ashishps1/awesome-low-level-design — curated LLD problems with solutions
→ https://workat.tech/machine-coding — practice problems

**System Design practice schedule:**
```
Week 7:  URL Shortener + Distributed Cache
Week 8:  Key-Value Store + Apple Music
Week 9:  Order Management + Notification System
Week 10: Rate Limiter + Chat System
```

**For each design, practice the 7-step framework:**
```
1. Clarify requirements (functional + non-functional)
2. Estimation (users, storage, bandwidth)
3. API design
4. Data model (use your 5-step DB framework!)
5. High-level architecture (draw on whiteboard)
6. Deep dives (2-3 components)
7. Bottlenecks + tradeoffs
```

**Record yourself** presenting each design for 35 minutes. Watch it back. This is the single most effective system design prep technique most people skip.

### Session 3: GenAI — Deeper + Build

**Week 7-8: Advanced RAG + Vector Databases**

**THE resource: Udemy — "LangChain: Develop AI Agents with LangChain & LangGraph" by Eden Marco**
→ https://www.udemy.com/course/langchain/
→ 19+ hours, for software engineers (not beginners), project-based
→ Covers: RAG, agents, documentation helper, code interpreter
→ Wait for Udemy sale ($10-15)

**Also learn: pgvector (PostgreSQL extension for vectors)**
→ This is where your DB knowledge shines
→ Tutorial: https://github.com/pgvector/pgvector
→ Vectors are just another column type. Similarity search is just another query.

**Week 9-10: Build Your Interview Coach Project**

**Project: "System Design Interview Coach" (Portfolio Piece #2)**
Build an AI agent that:
1. Has a knowledge base of system design concepts (embed your notes, DDIA summaries)
2. Acts as an interviewer — asks you a system design question
3. Listens to your answer, asks follow-up questions
4. At the end, gives feedback on what you covered and what you missed
5. Tracks your progress across sessions (which topics you're weak on)
6. Uses LangGraph for the conversation flow with multiple agent states

Tech stack: Python + FastAPI + LangGraph + pgvector + React frontend

**This project demonstrates:** Advanced RAG, agent orchestration, state management, database design, full-stack thinking. AND it's useful for your own prep.

→ Deploy it (even on a free tier). Push to GitHub. This is portfolio piece #2.

---

## PHASE 3: POLISH + MOCK INTERVIEWS (Weeks 11-14)

### Session 1+2: Mock Interviews (alternate DSA / System Design / Behavioral)

**Free mock interviews:**
→ **Pramp** — https://www.pramp.com — Free peer-to-peer mocks
→ **LeetCode Mock Interview** — Timed, simulates real interview
→ Record yourself on your phone during practice

**Paid (if budget allows):**
→ **Interviewing.io** — https://interviewing.io — Anonymous mocks with FAANG engineers
→ **Exponent** — https://www.tryexponent.com — System design mocks

**Schedule:**
```
Week 11: Mon/Wed/Fri = DSA mock, Tue/Thu = System Design practice
Week 12: Mon/Wed = System Design mock, Tue/Thu/Fri = DSA
Week 13: Full mock days (DSA + System Design + Behavioral in one day)
Week 14: Light review, STAR stories polish, confidence building
```

### Behavioral Prep (weave into weeks 11-14)

**Write 10-12 STAR stories.** Map each to Amazon Leadership Principles.

**THE resource: Dan Croitor YouTube**
→ https://youtube.com/@DanCroitor
→ 100+ videos specifically on Amazon LP interview prep

**Your stories should cover:**
```
1. Ownership — went beyond your role
2. Dive Deep — found root cause through investigation
3. Bias for Action — decided with incomplete info
4. Disagree and Commit — disagreed but executed
5. Customer Obsession — prioritized user experience
6. Deliver Results — met tight deadline
7. Earn Trust — admitted mistake, built trust
8. Invent and Simplify — simplified something complex
9. Production incident — how you handled it
10. Mentoring — how you helped junior engineers
11. Ambiguity — handled unclear requirements
12. Conflict — resolved disagreement with teammate
```

### Session 3+4: GenAI Polish + Portfolio

**Week 11-12: Production Skills**
→ Add evaluation/testing to your projects (how do you know RAG is working well?)
→ Add monitoring (track token usage, latency, error rates)
→ Add guardrails (handle when LLM outputs garbage)
→ Containerize with Docker

**Week 13-14: Portfolio Polish**
→ Clean up GitHub repos (good READMEs, architecture diagrams)
→ Write one blog post: "How I Built an AI Interview Coach with RAG and LangGraph"
→ Update LinkedIn with GenAI keywords
→ Be ready to demo your projects in interviews

---

## THE COMPLETE RESOURCE LIST (ONE per category, in priority order)

### Books (Buy These)

| # | Book | What It Teaches | When to Read |
|---|------|----------------|--------------|
| 1 | **DDIA** — Martin Kleppmann | System Design + Distributed Systems | Weeks 1-6, Chapters as listed above |
| 2 | **System Design Interview Vol 1** — Alex Xu | Structured system designs | Weeks 7-10, one chapter per day |
| 3 | **Java Concurrency in Practice** — Brian Goetz | Threading + Concurrency | Weeks 4-6 |
| 4 | **Effective Java 3rd Ed** — Joshua Bloch | Clean Java patterns | Reference, read specific items |
| 5 | **Clean Code** — Robert C. Martin | Writing maintainable code | Skim Weeks 9-10 |

### Free Online Resources (THE ones to use)

| Resource | What It Covers | URL |
|----------|---------------|-----|
| **NeetCode 150** | DSA problems by pattern | https://neetcode.io/practice |
| **OSTEP** | Operating Systems (free book) | https://pages.cs.wisc.edu/~remzi/OSTEP/ |
| **System Design Primer** | Everything system design (free) | https://github.com/donnemartin/system-design-primer |
| **Jenkov Java Concurrency** | Java threading (free, text) | https://jenkov.com/tutorials/java-concurrency/ |
| **Baeldung** | Spring Boot tutorials | https://www.baeldung.com |
| **LeetCode Database** | SQL practice problems | https://leetcode.com/problemset/database/ |
| **Refactoring Guru** | Design patterns explained visually | https://refactoring.guru/design-patterns |
| **Use The Index, Luke** | Database indexing deep dive | https://use-the-index-luke.com |

### YouTube Channels (Watch only what's relevant to THIS week's topic)

| Channel | Use For | URL |
|---------|---------|-----|
| **NeetCode** | DSA problem explanations | https://youtube.com/@NeetCode |
| **ByteByteGo** | System design visuals | https://youtube.com/@ByteByteGo |
| **Jordan Has No Life** | DDIA chapter walkthroughs | https://youtube.com/@jordanhasnolife5163 |
| **Hussein Nasser** | Networking, DB, backend deep dives | https://youtube.com/@haborhossain |
| **Concept && Coding** | LLD / Machine coding in Java | https://youtube.com/@ConceptandCoding |
| **Dan Croitor** | Amazon behavioral prep | https://youtube.com/@DanCroitor |

### GenAI Learning Path (FREE courses, in order)

| # | Course | Platform | Duration | URL |
|---|--------|----------|----------|-----|
| 1 | ChatGPT Prompt Engineering for Developers | DeepLearning.AI | 1.5 hrs | https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/ |
| 2 | LangChain for LLM Application Development | DeepLearning.AI | 1 hr | https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/ |
| 3 | LangChain: Chat with Your Data (RAG) | DeepLearning.AI | 1 hr | https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/ |
| 4 | Functions, Tools and Agents with LangChain | DeepLearning.AI | 1 hr | https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/ |
| 5 | AI Agents in LangGraph | DeepLearning.AI | 1 hr | https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/ |
| 6 | Introduction to LangGraph (Full Course) | LangChain Academy | 5+ hrs | https://academy.langchain.com/courses/intro-to-langgraph |
| 7 | RAG Course (Advanced) | Activeloop | 10+ hrs | https://learn.activeloop.ai/courses/rag |

**Total free learning: ~20+ hours of structured courses. That's your first 2 weeks of Session 3.**

### GenAI (Paid, if budget allows)

| Course | Platform | Price | URL |
|--------|----------|-------|-----|
| LangChain & LangGraph — Eden Marco | Udemy | ~$15 on sale | https://www.udemy.com/course/langchain/ |
| IBM RAG and Agentic AI Certificate | Coursera | Free audit / $49 cert | https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai |

---

## WEEK-BY-WEEK CHECKLIST

### Week 1
- [ ] Set up study space: whiteboard, notebook, laptop
- [ ] Buy DDIA book (or find PDF)
- [ ] Create NeetCode account, start Arrays + Two Pointers
- [ ] Read OSTEP Chapters 4-7 (Processes, Threads)
- [ ] Watch 3Blue1Brown "What is a GPT?" 
- [ ] Complete DeepLearning.AI Prompt Engineering course
- [ ] Solve 10 DSA problems (Arrays, Two Pointers)
- [ ] Log every day in your tracker

### Week 2
- [ ] Continue DSA: Sliding Window, Stack patterns
- [ ] Read OSTEP Chapters 26-33 (Concurrency — critical!)
- [ ] Watch Hussein Nasser: TCP, HTTP/2, WebSocket videos
- [ ] Complete DeepLearning.AI LangChain course
- [ ] Start DeepLearning.AI "Chat with Your Data" (RAG)
- [ ] Solve 10 more DSA problems
- [ ] Design your first DB schema: E-commerce

### Week 3
- [ ] Continue DSA: Binary Search, Linked Lists
- [ ] Read DDIA Chapter 3 (Storage and Retrieval — B-trees, LSM)
- [ ] Read DDIA Chapter 7 (Transactions — ACID, isolation levels)
- [ ] Complete RAG course (DeepLearning.AI)
- [ ] Start Activeloop RAG course (first 10 lessons)
- [ ] SQL: 5 LeetCode SQL problems (JOINs, Window functions)
- [ ] Design DB schema: Food Delivery app

### Week 4
- [ ] DSA: Trees (BFS, DFS, Max Path Sum)
- [ ] Start Java Concurrency in Practice: Chapters 1-5
- [ ] Code: Producer-Consumer, Deadlock, Singleton patterns
- [ ] Start LangChain Academy — Modules 0-2
- [ ] Complete DeepLearning.AI Functions + Tools course
- [ ] SQL: 5 more LeetCode SQL problems (CTEs, subqueries)

### Week 5
- [ ] DSA: Graphs (BFS, DFS, multi-source BFS)
- [ ] Java Concurrency: Chapters 8, 10 (ThreadPools, Deadlock)
- [ ] Code: Custom ThreadPool, CompletableFuture chains
- [ ] LangChain Academy: Modules 3-4 (Agents)
- [ ] DeepLearning.AI: AI Agents in LangGraph
- [ ] SQL: 5 more problems (Advanced: RANK, LAG, LEAD)

### Week 6
- [ ] DSA: Heap, DP basics (Coin Change, Edit Distance)
- [ ] Build Spring Boot REST API with error handling
- [ ] Read DDIA Chapter 5 (Replication) — start distributed systems
- [ ] Complete LangChain Academy: Modules 5-6
- [ ] BUILD: Document Q&A Assistant (Portfolio Project #1)
- [ ] Push project to GitHub with good README

### Week 7
- [ ] DSA: Re-solve all "needed help" problems from weeks 1-6
- [ ] System Design: Read Alex Xu Chapter 1-3 + ByteByteGo videos
- [ ] Practice Design: URL Shortener (whiteboard, record yourself)
- [ ] Practice Design: Distributed Cache
- [ ] Start Udemy LangChain course (or Activeloop advanced RAG)
- [ ] Learn pgvector basics

### Week 8
- [ ] DSA: Company-tagged problems (Apple, Amazon, DoorDash)
- [ ] System Design: Read Alex Xu Chapter 4-7
- [ ] Practice Design: Key-Value Store, Apple Music
- [ ] Read DDIA Chapter 6 (Partitioning) + Chapter 9 (Consistency)
- [ ] Continue GenAI course + start Interview Coach project
- [ ] LLD: Parking Lot System (Concept && Coding video + code it)

### Week 9
- [ ] DSA: Timed practice (25 min medium, 40 min hard)
- [ ] System Design: Order Management, Notification System
- [ ] LLD: Elevator System, LRU Cache (thread-safe)
- [ ] Read DDIA Chapter 11 (Stream Processing) — Kafka understanding
- [ ] Continue building Interview Coach project
- [ ] Start writing STAR stories (draft 4 stories)

### Week 10
- [ ] DSA: Continue timed practice
- [ ] System Design: Rate Limiter, Chat System
- [ ] LLD: Vending Machine, Rate Limiter
- [ ] Design Patterns: implement Singleton, Factory, Observer, Strategy in Java
- [ ] Finish Interview Coach project, deploy it
- [ ] Push to GitHub. Portfolio Piece #2 complete.
- [ ] Write 4 more STAR stories (total 8)

### Week 11
- [ ] Start mock interviews on Pramp (2 per week)
- [ ] Practice: DSA mock Mon/Wed/Fri, System Design Tue/Thu
- [ ] Polish STAR stories (total 10-12)
- [ ] Add Docker to GenAI projects
- [ ] Add evaluation/testing to RAG pipeline
- [ ] Read DoorDash engineering blog (3-4 articles)

### Week 12
- [ ] Mock interviews: increase to 3 per week
- [ ] Focus on weak areas identified in mocks
- [ ] Practice explaining system designs out loud (35 min each)
- [ ] Write blog post about your GenAI project
- [ ] Clean up GitHub profile and project READMEs

### Week 13
- [ ] Full mock interview days (DSA + SD + Behavioral in sequence)
- [ ] Review all STAR stories, practice telling them naturally
- [ ] Review all system design notes on whiteboard
- [ ] Update LinkedIn profile
- [ ] Start applying to companies

### Week 14
- [ ] Light review only — DO NOT cram new material
- [ ] 1 mock interview per day (alternate type)
- [ ] Review your notebook: key insights from 13 weeks
- [ ] Practice weak spots only
- [ ] Rest well. Sleep 8 hours. Exercise.
- [ ] You're ready.

---

## WHAT TO DO TODAY (literally right now)

1. **Download your tracker** (the React one I built you). Log Day 1.
2. **Go to NeetCode.io**, create account, open first Arrays problem.
3. **Open OSTEP Chapter 4** in your browser. Read for 30 minutes.
4. **Sign up for DeepLearning.AI** and bookmark the Prompt Engineering course.
5. **Buy DDIA** (or find it — you need this book).
6. **Write in your notebook:** "Day 1. I have 14 weeks. Today I solve my first problem."

That's it. Don't plan more. Don't organize more. Don't watch motivational videos. Start solving.

---

## WHAT SUCCESS LOOKS LIKE IN 14 WEEKS

By week 14, if you follow this plan, you will have:

```
✓ 120+ DSA problems solved (patterns internalized, not memorized)
✓ 8-10 system designs practiced and recorded
✓ 6-8 LLD problems coded in Java
✓ DDIA core chapters read and understood
✓ Java concurrency deeply understood (coded, not just read)
✓ Spring Boot practical knowledge
✓ 30+ SQL problems solved
✓ Full understanding of RAG, agents, LangChain, LangGraph
✓ 2 deployed GenAI projects on GitHub
✓ 1 blog post published
✓ 10-12 polished STAR stories
✓ 15+ mock interviews completed
✓ A notebook with 100+ daily entries — your personal interview bible
```

That's a senior engineer's preparation. With 5 years of work experience backing it up, you will be ready.
