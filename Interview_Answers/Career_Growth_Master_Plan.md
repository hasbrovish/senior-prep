# Career Growth Master Plan — Complete Guide
## From SDE (5.6 yrs, Infosys/GSTN) → SDE-2/SDE-3 at Product Companies
### Jayanti Vishnoi | Compiled: April 29, 2026
### Covers: Gen AI Roadmap, Side Project, Gap Analysis, Online Presence, Learning Plan

---

# TABLE OF CONTENTS

1. [Gen AI & Agentic AI Roadmap](#1-gen-ai--agentic-ai-roadmap)
2. [Side Project: CodeLens AI — Full Concept](#2-side-project-codelens-ai)
3. [Extension & Library Options](#3-extension--library-options)
4. [Gap Analysis vs Senior Engineers](#4-gap-analysis-vs-senior-engineers)
5. [Resume Selection Chances Assessment](#5-resume-selection-chances)
6. [How To Fill Gaps Without Active Project](#6-fill-gaps-without-active-project)
7. [Topaz Fabric Studio — Leveraging Current Assignment](#7-topaz-fabric-studio)
8. [Online Presence Blueprint](#8-online-presence-blueprint)
9. [12-Week Master Schedule](#9-twelve-week-master-schedule)

---

# 1. GEN AI & AGENTIC AI ROADMAP

## What You Already Have That Maps Directly

| Your Existing Skill | Gen AI Equivalent |
|---|---|
| Kafka event-driven architecture | Agent-to-agent message passing, tool orchestration |
| Strategy + Factory patterns | Tool/function routing in agents (pick the right tool for the task) |
| Redis caching | Vector store caching, embedding cache, conversation memory |
| REST API design | Tool APIs that agents call, function-calling schemas |
| Graph traversal (your appeal case DFS) | Agent reasoning chains, ReAct loops, tree-of-thought |
| Rule engine (your compliance engine) | Guardrails, output validation, prompt routing |
| Multi-tenant routing (ThreadLocal) | Multi-model routing (pick GPT-4 vs Claude vs local model per task) |
| HTTP Interceptor (Chain of Responsibility) | Middleware chains in LangChain/LangGraph |

## Skills to Add (Priority Order)

### Tier 1 — Must Have (1-2 months)

| Skill | What to Learn | Why |
|---|---|---|
| **Python** | Basics + FastAPI + async/await | 90% of Gen AI tooling is Python-first |
| **LLM Fundamentals** | Tokens, temperature, context window, prompt engineering, few-shot, chain-of-thought | Foundation for everything |
| **OpenAI / Anthropic APIs** | Chat completions, function calling, structured outputs, streaming | The "Hello World" of Gen AI |
| **RAG (Retrieval-Augmented Generation)** | Embeddings → vector DB → retrieval → LLM prompt | Most common production Gen AI pattern |
| **Vector Databases** | Pinecone, Weaviate, pgvector, or ChromaDB | Where embeddings live |

### Tier 2 — Agentic AI (2-3 months)

| Skill | What to Learn | Why |
|---|---|---|
| **LangChain / LangGraph** | Chains, agents, tools, memory, graph-based workflows | Industry-standard agent framework |
| **Function Calling / Tool Use** | OpenAI function calling, Anthropic tool use, MCP protocol | How agents interact with external systems |
| **ReAct Pattern** | Reason → Act → Observe → Repeat | Core agent loop — your graph traversal is already this |
| **Agent Memory** | Short-term (conversation), long-term (vector store), episodic | How agents retain context across tasks |
| **Multi-Agent Systems** | CrewAI, AutoGen, LangGraph multi-agent | Multiple specialized agents collaborating |

### Tier 3 — Production-Grade (3-6 months)

| Skill | What to Learn | Why |
|---|---|---|
| **Fine-tuning** | LoRA, QLoRA on open models (Llama, Mistral) | Custom models for domain-specific tasks |
| **Guardrails & Eval** | LLM output validation, RAGAS, LangSmith, prompt injection defense | Production safety — maps to your compliance rule engine mindset |
| **Orchestration** | LangGraph state machines, conditional edges, human-in-the-loop | Your FSM experience maps perfectly here |
| **Observability** | LangSmith, Weights & Biases, token cost tracking | Debugging agents in production |
| **MCP (Model Context Protocol)** | Anthropic's standard for tool integration | Emerging standard for agent-tool communication |

## Fastest Learning Path From Your Stack

```
Week 1-2:  Python basics + FastAPI (you already know Spring Boot — same concepts)
Week 3-4:  OpenAI API + prompt engineering + build a simple chatbot
Week 5-6:  RAG pipeline: embed your GSTN docs → ChromaDB → query with LLM
Week 7-8:  LangChain agent with tools (DB lookup, API call, file search)
Week 9-10: LangGraph — build a multi-step agent with state machine (your FSM maps here)
Week 11-12: Multi-agent system (one agent researches, one writes, one reviews)
```

## Resume Bullet After Learning Gen AI

```
• Built a RAG-based document retrieval agent using Python, LangChain, and
  OpenAI API with vector search (ChromaDB/pgvector) — enabling natural-language
  queries over [domain] documents with context-aware responses and source
  citations.

• Designed a multi-agent workflow using LangGraph with tool-calling, ReAct
  reasoning loops, and structured output validation — automating [task]
  with human-in-the-loop approval gates.
```

## Key Insight

Your **strongest differentiator** isn't "I know LangChain" (everyone will). It's:

> "I've built production financial state machines, distributed transaction systems, and graph-traversal engines in Java — and I can apply that same systems-thinking to design reliable, observable, guardrailed AI agent pipelines."

Agentic AI is **distributed systems + state machines + tool orchestration**. You already think in those patterns. The gap is just Python + LLM APIs + vector stores.

---

# 2. SIDE PROJECT: CODELENS AI

## Product Vision

> CodeLens AI: Index any codebase → Search it semantically → Get AI-powered reviews, docs, and answers.

### Problem Statement
- Developers spend 60% of time **reading** code, not writing it
- Onboarding to a new codebase takes 3-6 months
- Code reviews are manual, inconsistent, and slow
- Documentation is always outdated or missing
- Existing tools (Sourcegraph, SonarQube) are expensive and don't have AI

### Solution
A **CLI-first, extension-powered** code intelligence tool that:
1. Indexes any codebase locally (Go binary — fast, zero infrastructure)
2. Makes it searchable (exact + semantic)
3. Auto-generates documentation
4. Reviews code for bugs, security issues, and code smells
5. Answers natural-language questions about the codebase

## How Each Technology Is Used FOR ITS ACTUAL STRENGTH

| Technology | What It's Known For | How You Use It |
|---|---|---|
| **Go** | Concurrency, speed, CLI tools | Git webhook consumer, file crawler, concurrent code indexer (goroutines), CLI tool |
| **Elasticsearch** | Full-text search, aggregations | Code search ("find all functions that call Redis"), symbol search, log search |
| **MongoDB** | Flexible schema, document storage | Store analysis results (each file analysis has different shape), agent conversation history, project configs |
| **GraphQL** | Flexible queries, no over-fetching | Frontend fetches exactly what it needs — dashboard needs counts, code view needs full file + annotations |
| **OpenTelemetry** | Distributed tracing, metrics | Trace every AI agent call end-to-end, measure token costs, latency per agent, error rates |
| **Java/Spring Boot** | Enterprise backend, transactions | User auth, billing, org management, API gateway, Kafka orchestration |
| **Python/FastAPI** | AI/ML ecosystem | LangGraph agents, RAG pipeline, embeddings, LLM calls |
| **Angular** | Enterprise SPA | Web dashboard, code viewer, chat interface |
| **Redis** | Caching, pub/sub | Embedding cache, search result cache, real-time WebSocket pub/sub |
| **Kafka** | Event streaming | Async job pipeline: index → analyze → review → notify |

## Full Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENTS (Cross-Platform)                       │
│                                                                   │
│  ┌──────────┐  ┌──────────────┐  ┌─────────┐  ┌──────────────┐ │
│  │ Angular  │  │ Electron App │  │ Flutter │  │ Go CLI Tool  │ │
│  │ Web App  │  │ (Mac/Win)    │  │ Android │  │ $ codelens   │ │
│  └────┬─────┘  └──────┬───────┘  └────┬────┘  └──────┬───────┘ │
│       └────────────────┴───────────────┴──────────────┘         │
│                            │                                     │
│                    GraphQL API (single endpoint)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              GO — API GATEWAY + INDEXER SERVICE                   │
│                                                                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ GraphQL Server  │  │ Git Webhook      │  │ Code Indexer   │ │
│  │ (gqlgen)        │  │ Consumer         │  │ (goroutines)   │ │
│  │                 │  │ push/PR events   │  │ parse → chunk  │ │
│  └────────┬────────┘  └────────┬─────────┘  │ → embed → store│ │
│           │                    │             └───────┬────────┘ │
│           │                    │                     │          │
│  ┌────────▼────────────────────▼─────────────────────▼────────┐ │
│  │                    Kafka Producer                           │ │
│  │  Topics: code-index │ code-review │ doc-gen │ search-query │ │
│  └────────────────────────────┬───────────────────────────────┘ │
│                               │                                  │
│  OpenTelemetry Instrumentation (traces + metrics on every op)    │
└─────────────────────────────────────────────────────────────────┘
         │              │                │
         ▼              ▼                ▼
┌──────────────┐ ┌─────────────┐ ┌────────────────────────────────┐
│    KAFKA     │ │   REDIS     │ │  JAVA / SPRING BOOT            │
│              │ │             │ │  Business Logic Service          │
│ code-index   │ │ embed cache │ │                                  │
│ code-review  │ │ search cache│ │  • User auth (JWT + OAuth)      │
│ doc-gen      │ │ WS pub/sub  │ │  • Org & project management     │
│ search-query │ │ rate limit  │ │  • Billing / subscription       │
│ notification │ │             │ │  • Kafka consumer (notifications)│
└──────┬───────┘ └─────────────┘ │  • Audit trail                  │
       │                         └────────────────────────────────┘
       ▼
┌─────────────────────────────────────────────────────────────────┐
│              PYTHON / FASTAPI — AI AGENT SERVICE                 │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              LangGraph Orchestrator                    │       │
│  │                                                        │       │
│  │   ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │       │
│  │   │ INDEXER   │  │ REVIEWER │  │ DOC WRITER        │  │       │
│  │   │ Agent     │  │ Agent    │  │ Agent             │  │       │
│  │   │ embed code│  │ find bugs│  │ generate docs     │  │       │
│  │   └──────────┘  └──────────┘  └───────────────────┘  │       │
│  │   ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │       │
│  │   │ Q&A      │  │ REFACTOR │  │ SECURITY SCANNER  │  │       │
│  │   │ Agent    │  │ Agent    │  │ Agent (OWASP)     │  │       │
│  │   │ RAG chat │  │ suggest  │  │ vuln detection    │  │       │
│  │   └──────────┘  └──────────┘  └───────────────────┘  │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  OpenTelemetry: trace every LLM call, token count, latency       │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ Elasticsearch│   │     MongoDB      │   │   ChromaDB /     │
│              │   │                  │   │   pgvector        │
│ • Code search│   │ • Analysis docs  │   │                  │
│ • Symbol idx │   │ • Agent outputs  │   │ • Code embeddings│
│ • Log search │   │ • Chat history   │   │ • Semantic search│
│ • Aggregation│   │ • Project config │   │                  │
│   (metrics)  │   │ • Audit events   │   │                  │
└──────────────┘   └──────────────────┘   └──────────────────┘
```

## Why Go Is Perfect For Core Engine (Not Java)

| Task | Why Go Wins | Why Not Java |
|---|---|---|
| Git webhook consumer | Goroutines handle 1000s of concurrent webhook events | Thread-per-request is heavier |
| File crawler/indexer | 10x faster file I/O, tiny memory footprint | JVM startup + GC overhead for file processing |
| CLI tool (`$ codelens analyze .`) | Single binary, no runtime needed | Requires JVM installed |
| GraphQL gateway | gqlgen is type-safe, fast, code-generated | Spring GraphQL works but Go is lighter for gateway |
| Real-time streaming | Goroutine + channel for WebSocket fan-out | Reactive Spring works but more complex |

**Java stays for what it's best at:** Business logic, transactions, auth, billing — where Spring Boot's ecosystem (Security, JPA, Kafka) is unmatched.

## Why MongoDB Fits (Not Just Postgres)

```json
// Each file analysis has a DIFFERENT shape — perfect for MongoDB's flexible schema

// Java file analysis
{
  "file": "DemandProcessingUtil.java",
  "language": "java",
  "analysis": {
    "classes": 1,
    "methods": 47,
    "cyclomatic_complexity": 89,
    "design_patterns": ["Strategy", "Factory"],
    "spring_annotations": ["@Service", "@Transactional"]
  }
}

// TypeScript file analysis — completely different shape
{
  "file": "appeal-effect.service.ts",
  "language": "typescript",
  "analysis": {
    "components": 0,
    "services": 1,
    "rxjs_operators": ["BehaviorSubject", "switchMap"],
    "bundle_size_impact": "2.3kb"
  }
}
```

## Why Elasticsearch (Not Just Vector Search)

```
# Exact code search — "find every file that calls Redis SETNX"
# Aggregation — "which modules have the most security issues?"
# Fuzzy symbol search — "find functions named like 'process*Demand*'"

ChromaDB does SEMANTIC search ("find code that handles payments").
Elasticsearch does EXACT search + aggregations + fuzzy matching.
You need both.
```

## Why GraphQL (Not REST)

```graphql
# Dashboard page — needs just counts
query DashboardData($projectId: ID!) {
  project(id: $projectId) {
    name
    fileCount
    issueCount
    lastAnalyzedAt
  }
}

# Code viewer page — needs full file + annotations
query FileDetail($fileId: ID!) {
  file(id: $fileId) {
    path
    content
    analysis { issues { line type message } }
  }
}

# Same API, completely different data shapes — zero over-fetching
```

## OpenTelemetry — Full Observability

```
Trace: user-query-abc123
├─ Span: go-gateway/graphql-resolve         12ms
├─ Span: kafka/produce/search-query          3ms
├─ Span: python-ai/rag/embed-query          85ms   ← OpenAI embedding call
├─ Span: python-ai/rag/vector-search        23ms   ← ChromaDB query
├─ Span: python-ai/llm/generate-answer     1.2s    ← GPT-4 call
│   └─ Attributes: tokens_in=2340, tokens_out=890, cost=$0.04
├─ Span: mongodb/save-conversation           5ms
└─ Span: go-gateway/websocket-push           1ms
                                    Total: 1.35s
```

## Build Phases (6 Phases, 16 Weeks)

| Phase | Weeks | What You Build | Skills Practiced |
|---|---|---|---|
| 1 | 1-4 | Go CLI + Local Engine | Go, goroutines, embeddings, SQLite-vss, Ollama |
| 2 | 5-8 | VS Code Extension | TypeScript, VS Code API, child_process |
| 3 | 9-12 | Cloud Backend | Java/Spring Boot, Kafka, ES, MongoDB, Angular |
| 4 | 13-14 | Chrome Extension | TypeScript, Manifest V3, content scripts |
| 5 | 15-16 | CI/CD + Launch | GitHub Actions, Docker, Product Hunt |

## Monetization

| Tier | Price | Features |
|---|---|---|
| **Free** | $0 | CLI (local only), 5 VS Code queries/day, local LLM |
| **Pro** | $8/month | Unlimited queries, GPT-4/Claude, cloud sync, PR review |
| **Team** | $15/user/month | Shared knowledge base, org dashboard, GitHub Action |
| **Enterprise** | $500+/month | Self-hosted, SSO, custom models, audit logs, SLA |

## Resume Bullet After Completing Project

```
• Designed and built an AI-powered code analysis platform using Java/Spring
  Boot, Python/FastAPI, LangGraph, and Angular — featuring a RAG pipeline
  over code repositories (ChromaDB vector search), multi-agent orchestration
  with state-machine-based workflow routing, Kafka async processing for
  long-running AI tasks, and Redis response caching; agents perform automated
  code review, documentation generation, and natural-language Q&A with
  source-cited responses and human-in-the-loop approval gates.
```

## Interview Story This Enables

> "I noticed that my Gen AI learning was disconnected from my backend experience, so I built a project that combined both. The Java API gateway handles auth and routes requests to a Python AI service via Kafka. The AI service uses LangGraph — which is essentially a state machine for agents, and I'd already built financial state machines in Java, so the mental model transferred directly. The RAG pipeline reminded me of my graph traversal work — walking a codebase's import graph is structurally similar to walking appeal case chains. The biggest lesson was that **agentic AI is just distributed systems with non-deterministic components** — you need the same patterns: retry, fallback, idempotency, observability."

---

# 3. EXTENSION & LIBRARY OPTIONS

## Option 1: VS Code Extension (BEST FIRST MOVE)

**Why this wins:** 30M+ VS Code users. Marketplace handles distribution. You already know TypeScript.

```
What it does:
├── Sidebar: AI chat about your open project
├── Inline: Code annotations (issues, docs, complexity)
├── Command palette: "CodeLens: Review this file"
├── Hover: Explain this function / suggest refactor
├── Status bar: File complexity score
└── Right-click: "Generate docs for this function"
```

**Tech stack:**

| Layer | Technology | Why |
|---|---|---|
| Extension host | TypeScript (VS Code API) | Required by VS Code |
| Local indexing | Go binary (bundled) | Fast file crawling, AST parsing — runs as child process |
| AI calls | OpenAI / Anthropic API (direct) | No backend needed for v1 |
| Embeddings store | SQLite + sqlite-vss (local) | Zero infrastructure — everything runs on user's machine |

**No backend server needed for v1.** Everything runs locally. User provides their own API key.

```
Monetization:
  Free tier:  5 AI queries/day, basic code review
  Pro ($8/mo): Unlimited queries, full project indexing, auto-docs
  Team ($15/user): Shared team knowledge base, PR review bot
```

**Build time:** 4-6 weeks for MVP

## Option 2: Chrome Extension — AI Code Review for GitHub/GitLab

```
What it does on github.com:
├── PR page: "Review with AI" button → inline comments on diff
├── File view: Complexity badge, auto-generated summary
├── Repo page: "Ask about this repo" chat sidebar
├── Issues: "Suggest fix" button on bug reports
└── Search: Enhanced code search with semantic understanding
```

**Tech stack:**

| Layer | Technology | Why |
|---|---|---|
| Extension | TypeScript + Chrome APIs | Content scripts inject into GitHub pages |
| Popup/Sidebar | Preact or Svelte (tiny bundle) | Lighter than Angular for extension popup |
| AI Backend | Go + FastAPI microservice (hosted) | Chrome extensions can't run heavy AI locally |
| Auth | GitHub OAuth | One-click "Connect GitHub" |

```
Monetization:
  Free:     3 PR reviews/month
  Pro ($10/mo): Unlimited PR reviews, repo Q&A
  Team ($12/user): Org-wide code standards, custom rules
```

**Build time:** 6-8 weeks for MVP

## Option 3: npm / pip / Go Library (Open Source → Paid Cloud)

```bash
# Go CLI — install and run
$ go install github.com/jayanti/codelens@latest
$ codelens review ./src
$ codelens docs ./src --output docs/
$ codelens search "how does auth work" --project .

# npm package — for JS/TS projects
$ npx codelens-js review ./src

# Python package
$ pip install codelens-py
$ codelens review ./src
```

```
Monetization:
  CLI (free):     Local analysis, local LLM (Ollama)
  Cloud ($8/mo):  GPT-4 powered, history, dashboard
  CI/CD ($20/mo): GitHub Action / GitLab CI integration
  Enterprise:     Self-hosted, custom models, SSO
```

**Build time:** 3-4 weeks for CLI MVP

## Option 4: JetBrains Plugin (IntelliJ, WebStorm, GoLand)

Same concept as VS Code but for JetBrains IDEs. **Written in Java/Kotlin** — your Java skills apply directly.

**Build time:** 6-8 weeks (JetBrains plugin API is more complex)

## Recommended Build Order

```
CLI → Library → VS Code Extension → Chrome Extension → SaaS

Each layer WRAPS the previous one:

┌──────────────────────────────────┐
│  SaaS (Angular dashboard)        │ ← Your Angular skills
│  ┌────────────────────────────┐  │
│  │ Chrome Extension           │  │ ← TypeScript
│  │  ┌──────────────────────┐  │  │
│  │  │ VS Code Extension    │  │  │ ← TypeScript + VS Code API
│  │  │  ┌────────────────┐  │  │  │
│  │  │  │ Go CLI Binary  │  │  │  │ ← Your Go skills
│  │  │  │ (core engine)  │  │  │  │
│  │  │  └────────────────┘  │  │  │
│  │  └──────────────────────┘  │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘

The Go CLI is the CORE. Everything else is a wrapper.
You build the hard part once, then ship it everywhere.
```

## Fastest Path to First Dollar

| Week | Milestone | Revenue |
|---|---|---|
| 4 | Go CLI on GitHub | $0 (build stars) |
| 8 | VS Code ext (free tier) | $0 (build installs) |
| 10 | VS Code ext (Pro tier) | First $8/mo subscribers |
| 12 | Chrome ext + GitHub Action | Team tier $15/user |
| 16 | Product Hunt launch | Spike in signups |

---

# 4. GAP ANALYSIS VS SENIOR ENGINEERS

## Scorecard: You vs The SDE-2/SDE-3 Bar

| Dimension | Top Company SDE-2/3 Bar | Your Current Score | Gap |
|---|---|---|---|
| **Technical Depth** | Owns one domain end-to-end | 9/10 | Minimal — your financial state machine is SDE-3 caliber |
| **System Design** | Can design systems at scale (HLD+LLD) | 6/10 | You've BUILT systems but haven't practiced DESIGNING from scratch on whiteboard |
| **Scale & Numbers** | Can articulate latency, throughput, QPS | 5/10 | You know 15.2M users but do you know your API's p99 latency? RPS? Cache hit rate? |
| **Ownership** | End-to-end delivery including oncall, monitoring | 6/10 | You own code but unclear if you own production (alerts, dashboards, incident response) |
| **Cross-team Impact** | Influenced other teams' design decisions | 4/10 | Your work is within your team — no evidence of cross-team technical leadership |
| **Technical Writing** | Design docs, RFCs, ADRs | 3/10 | No evidence of written technical proposals that influenced decisions |
| **Open Source / Visibility** | GitHub, blog, talks, community | 2/10 | Zero public presence — invisible to hiring managers |
| **DSA** | LeetCode medium consistently, some hard | 5/10 (assumed) | Must grind — this is the gatekeeper at every company |
| **Mentoring** | Guides junior devs, reviews their designs | 5/10 | Likely happens informally but you don't articulate it |
| **Production Mindset** | Monitoring, alerting, SLIs, incident response | 4/10 | No mention of Grafana, alerts, oncall, postmortems |
| **Testing** | Strong testing culture, TDD or at least high coverage | 5/10 | No mention of test strategy, coverage, integration tests |
| **CI/CD** | Owns deployment pipeline, feature flags, canary releases | 4/10 | Jenkins exists but no evidence of you owning the pipeline |
| **Communication** | Articulates complex problems simply | 6/10 | Your prep docs show you can, but no public evidence |
| **Product Thinking** | Understands WHY a feature exists, proposes alternatives | 5/10 | You build what's asked — limited evidence of pushing back or proposing |
| **Company Caliber** | Previous top-company experience | 2/10 | "Infosys + Government" is a red flag pattern for screeners |

## Top 10 Gaps (Ranked by Impact)

### GAP #1: Zero Public Presence
**What seniors have:** GitHub profile with pinned repos, 2-3 blog posts, maybe a tech talk
**What you have:** Nothing visible externally
**Impact:** Recruiters Google you. They find nothing. Skip.

**FIX (2 weeks):**
- GitHub profile + README + pinned repos
- LinkedIn headline + summary + project descriptions
- 2 blog posts on dev.to converting your existing GSTN knowledge into articles

### GAP #2: No Production/Observability Story
**What seniors have:** "I set up Grafana dashboards, defined SLIs (p99 < 200ms), handled a production incident where..."
**What you have:** No mention of monitoring, alerting, or incident response

**FIX:** Build an "Observability Lab" locally (Spring Boot + Prometheus + Grafana + Jaeger in Docker Compose). Takes 1 weekend.

### GAP #3: No System Design Practice (Whiteboard Format)
**What seniors have:** Can design Twitter/Uber/payment system in 45 minutes on whiteboard
**What you have:** You've BUILT real systems, but haven't practiced the interview FORMAT

**FIX:** 10 system design problems using framework: Requirements → Estimation → HLD → Deep Dive → Tradeoffs. 3-4 mock interviews on Pramp.

### GAP #4: No Measurable Performance Numbers
**What seniors say:** "Reduced API latency from 800ms to 120ms by implementing caching"
**What you say:** "Built two-tier caching"

**FIX:** Derive reasonable estimates from what you know:
- Officers per state × actions/hour → approximate RPS
- Reference data cache keys: 100 types × 28 states → ~2,800 keys
- Cache hit rate for reference data: ~90-95% (reasonable estimate)

### GAP #5: No Cross-Team / Technical Leadership Story
**What seniors have:** "I proposed a new caching strategy adopted by 3 other teams"
**What you have:** Strong individual work, contained within your team

**FIX:** Reframe what you already have:
- "The Strategy+Factory framework I designed is used by 20+ proceeding types developed by other team members"
- "The 21 micro-libraries in gstn-apps are shared across 5 back-office modules"

### GAP #6: Weak Testing Story
**What seniors have:** "Integration tests with Testcontainers, 85% coverage, caught regression"
**What you have:** No mention of testing strategy

**FIX:** Build strong tests in side project. Use table-driven tests (Go), JUnit 5 + Mockito + Testcontainers (Java), pytest (Python). Show coverage badges.

### GAP #7: No Design Doc / RFC Experience
**What seniors have:** "I wrote a design doc for the migration strategy, got buy-in from 3 teams"
**What you have:** No evidence of written technical proposals

**FIX:** Write 3 design docs for your CodeLens project (Architecture, Agent Orchestration, Indexing Pipeline). Each 2-4 pages.

### GAP #8: DSA Gap (Assumed)
**What seniors have:** Solve LeetCode medium in 20-25 minutes consistently
**Minimum bar:** 100 problems (60 medium, 30 easy, 10 hard)

### GAP #9: No CI/CD Ownership
**What seniors have:** "I designed the deployment pipeline with canary releases and automated rollback"

**FIX:** Own full pipeline in side project: GitHub Actions → test → build → release.

### GAP #10: No Product Thinking / Pushback Story
**What seniors have:** "PM wanted X, I proposed Y instead because of Z constraint"

**FIX:** Reframe — "When the waiver CR came in, initial requirement was 4 scenarios. I analyzed edge cases and identified void-order reversal needed compensating transactions. I proposed the snapshot approach which was adopted."

---

# 5. RESUME SELECTION CHANCES

## Current Profile (GSTN Only)

| Company Tier | Selection Rate | Why |
|---|---|---|
| Service companies (TCS, Wipro) | 85-90% | Your exp is more than enough |
| Mid-tier product (Zoho, Freshworks) | 50-60% | Strong domain, but "government project" bias |
| Top product (Flipkart, PhonePe, Swiggy) | 30-40% | Solid system design, no visible side projects |
| Big Tech (Google, Microsoft, Amazon) | 15-25% | "Infosys + government" screener bias |
| Startups (funded) | 40-50% | Full-stack valued, but want "shipped product" proof |

## With GSTN + CodeLens AI Project

| Company Tier | Selection Rate | Change | Why |
|---|---|---|---|
| Service companies | 95% | +5% | Overkill — you'd get SDE-3 easily |
| Mid-tier product | 75-85% | +25% | Side project demolishes "service company dev" bias |
| Top product | 55-65% | +25% | Open-source CLI + VS Code extension = visible proof |
| Big Tech | 35-45% | +20% | Polyglot + Gen AI signals modern engineer |
| Startups | 70-80% | +30% | Shipped product + monetization thinking = startup-ready |
| Gen AI roles | 60-70% | NEW | LangGraph + RAG + agents = qualified for AI engineer roles |

## What Moves The Needle Most

```
GitHub stars on CLI (>100)                 +15% (visible proof)
VS Code extension with real installs       +15% (shipped product)
"Go + Java + Python" on resume            +10% (polyglot signal)
"LangGraph / RAG / AI agents" on resume   +10% (hot skill demand)
Blog posts explaining architecture         +5%  (communication signal)
OpenTelemetry / observability mention      +5%  (production mindset)
```

## The Real Bottleneck

```
Recruiter sees: "Infosys · 5.6 years · Government project"
Recruiter thinks: "Service company, probably does CRUD, skip"

Recruiter sees: "Infosys · 5.6 years · Government project
                 + Open-source Go CLI (★ 200) 
                 + VS Code extension (5K installs)
                 + Built with LangGraph + Kafka + Elasticsearch"
Recruiter thinks: "This person builds things. Interview."
```

The side project **breaks the pattern matching** that gets your resume auto-rejected.

---

# 6. FILL GAPS WITHOUT ACTIVE PROJECT

## Not being on a project is your ADVANTAGE

```
People ON projects:     6 hours of work → too tired to study → weekends only
You (OFF project):      6 hours of focused prep/building per day → 12 weeks = transformed profile
```

## GAP #1 FIX: Public Presence (1 Week)

```
Day 1: Create GitHub account + profile README
Day 2-3: Write blog post #1 — "How I Designed a 12-Scenario Financial State Machine in Java"
         (Convert Resume_Bullets_Explainer.md into a teaching article)
Day 4-5: Write blog post #2 — "Migrating 70K LOC AngularJS to Angular Without a Rewrite"
Day 6-7: Update LinkedIn profile fully, create "Today I Learned" GitHub repo
```

## GAP #2 FIX: Observability (1 Weekend)

```
Build "Observability Lab" — Docker Compose with:
  - Simple Spring Boot REST API
  - PostgreSQL + Redis
  - OpenTelemetry Collector
  - Prometheus (metrics)
  - Grafana (dashboards: p50/p95/p99 latency, RPS, error rate, cache hit ratio)
  - Jaeger (distributed tracing)
  - Generate load with k6 or Apache Benchmark
  - Screenshot everything → GitHub repo + blog post
```

## GAP #3 FIX: System Design (4-6 Weeks)

```
FREE RESOURCES:
- github.com/donnemartin/system-design-primer (200K+ stars)
- github.com/karanpratapsingh/system-design (great diagrams)
- ByteByteGo Newsletter (free tier)
- YouTube: Alex Xu, Tech Dummies (Narendra L), Gaurav Sen

Practice 1 problem per day, 45 minutes:
Week 1-2: URL Shortener, Rate Limiter, Notification System
Week 3-4: Distributed Cache, Payment System, Workflow Engine
Week 5-6: Chat System, Search Autocomplete, AI Agent Platform

Then: 3-4 mock interviews on Pramp.com (free, peer-to-peer)
```

## GAP #4 FIX: Numbers (Estimate From Memory)

```
| Metric | How to Estimate | Your Answer |
|---|---|---|
| Daily active officers | 28 states × ~50-100 per state | ~1,400-2,800 |
| Your API's likely RPS | 2,800 officers × 10 actions/hr ÷ 3600 | ~8-10 (peak ~50) |
| Redis cache keys | 100 ref types × 28 states | ~2,800 keys |
| Cache hit rate | Ref data rarely changes | ~90-95% |
| p99 latency | Typical Spring Boot + DB + Redis | ~200-500ms |

In interviews, say: "Based on approximately 2,500 active officers, our
appeal module handles roughly 10-50 RPS during peak hours..."
Reasonable estimates + reasoning = credible.
```

## GAP #5 FIX: Cross-Team Impact (Reframe Existing Work)

```
Already cross-team (just frame it right):
1. "Strategy+Factory framework used by 20+ proceeding types developed by other team members"
2. "AppealCaseService called by 4 controllers other developers maintain"
3. "21 micro-libraries shared across 5 back-office modules"
4. "Waiver CR required coordinating across LitigationAPI, CaseMgmtFwk, and ReturnAPI"
```

## GAP #6 FIX: Testing (Build In Side Project)

```
Go CLI: table-driven tests, 80%+ coverage on core packages
Java Backend: JUnit 5 + Mockito + Testcontainers
Python AI: pytest with mocked LLM responses
Every repo: CI with GitHub Actions + coverage badge
```

## GAP #7 FIX: Design Docs (Write For Side Project)

```
Write 3 design docs:
1. "CodeLens AI — System Architecture" (problem, goals, components, tradeoffs)
2. "Agent Orchestration Design" (LangGraph state machine, error handling, token budgets)
3. "Indexing Pipeline Design" (goroutine pool, incremental hashing, failure modes)
```

## GAP #8 FIX: DSA (8-Week Plan, 1.5 hrs/day)

```
Week 1: Arrays + Hashing (12 problems)
Week 2: Two Pointers + Sliding Window (12 problems)
Week 3: Stack + Linked List (10 problems)
Week 4: Trees (12 problems) ← your graph traversal maps here
Week 5: Graphs (12 problems) ← STRONGEST AREA
Week 6: Dynamic Programming (12 problems)
Week 7: Backtracking + Advanced (10 problems)
Week 8: Mock Interviews (timed — 1 medium in 25 min)

CONNECT DSA TO YOUR EXPERIENCE:
- Graph problems → "I built a DFS graph traversal for appeal case chains"
- Memoization → "I used Set-based deduplication to avoid recomputation"
- State machines → "I modeled 12 financial scenarios as state transitions"
```

## GAP #9 FIX: CI/CD (Build In Side Project)

```
From Day 1 of CodeLens:
.github/workflows/ci.yml:
├── On every push: lint + test + build
├── On PR: tests + coverage report as PR comment
├── On tag (v*): cross-platform binaries via goreleaser
└── Weekly: dependency update (Dependabot)
```

## GAP #10 FIX: Product Thinking (Practice Mini PRDs)

```
Write "mini PRDs" for features you would add to CodeLens:
├── Problem: Devs forget to run code review before pushing
├── Solution: Webhook triggers AI review, posts comments on PR
├── Success metrics: 80% reviews have actionable findings, < 60s latency
├── Scope cut: No auto-fix in v1, text config only
└── Open questions: How to handle PRs > 500 lines?
```

## Daily Schedule (Off Project)

```
MORNING (2 hours):
├── 1 hour: DSA (LeetCode — 1-2 problems)
└── 1 hour: System Design (read 1 chapter or design 1 system)

AFTERNOON (3 hours):
├── 2.5 hours: Build CodeLens project (write actual code)
└── 0.5 hours: Write notes / design doc / blog draft

EVENING (1 hour):
├── 30 min: Read tech blogs (ByteByteGo, Martin Fowler, Spring blog)
└── 30 min: Review DSA solutions from morning

WEEKLY:
├── Monday: Write/publish 1 blog post or push significant code
├── Wednesday: 1 mock interview (alternate DSA and system design)
├── Friday: Review week's progress, plan next week
└── Weekend: Larger coding sessions (4-5 hours) for side project milestones
```

---

# 7. TOPAZ FABRIC STUDIO

## Why This Assignment Is Extremely Valuable

| What You're Doing | What You're Actually Learning |
|---|---|
| Performance testing agents | How agentic workflows behave under load |
| Testing MCP servers | The MCP protocol (Anthropic's standard for tool use) — cutting-edge |
| JMeter on AI workflows | How LLM calls scale (token latency, queue depth, timeout patterns) |
| Observing agent orchestration | How tools/workflows are chained in production |
| Testing tool creation APIs | API design for AI tooling platforms |

## Traditional vs AI Performance Testing

```
Traditional API testing:
  Request → Response → Measure latency
  Predictable. Deterministic. Same input = same output.

AI/Agent performance testing (what you're doing):
  Request → Agent reasons → Calls tool → Waits for LLM → Maybe retries → Response
  NON-DETERMINISTIC. Variable latency. Token-based costs. Cold starts.

UNIQUE CHALLENGES:
- LLM calls take 1-10+ seconds (not milliseconds like REST APIs)
- Agent workflows have VARIABLE step counts (based on reasoning)
- Token throughput matters more than request throughput
- Cost per request varies (simple = $0.01, complex reasoning = $0.50)
- Cold start vs warm inference (GPU scheduling)
```

## What To Learn While On This Assignment

```
ASK AND UNDERSTAND:
├── What is MCP (Model Context Protocol)?
│   → Request format, tool definitions, response format
│   → How Topaz implements it
├── How does agent orchestration work?
│   → State machine? DAG? ReAct loop?
│   → How are tools selected?
├── What LLMs are being used?
│   → GPT-4? Claude? Open source?
│   → Token budget per request?
├── How are workflows defined?
│   → YAML? JSON? Visual builder?
└── Infrastructure?
    → GPU allocation, queue management, scaling
```

## How To Maximize It

```
Beyond just writing JMeter scripts:
1. PROPOSE: "Can I build a Grafana dashboard for performance results?"
   → Shows observability skills
2. PROPOSE: "Can I document the performance baseline and bottleneck analysis?"
   → Shows technical writing skills
3. PROPOSE: "Can I create a load test pipeline in CI/CD that runs nightly?"
   → Shows automation/DevOps skills
4. PROPOSE: "Can I profile which tool calls are the bottleneck?"
   → Shows system-level thinking
```

## Resume Bullet From Topaz

```
"Designed and executed performance test suites for an enterprise AI agent
orchestration platform (Infosys Topaz Fabric Studio) using JMeter —
benchmarking agent workflow throughput, MCP server response times, and
LLM inference latency under concurrent load; identified bottlenecks in
tool-calling chains and established SLI baselines for agent response
time (p50/p95/p99) across 50+ concurrent agent sessions."
```

## Direct Connection to CodeLens Side Project

```
TOPAZ LEARNING                    →    CODELENS APPLICATION
───────────────────────────────────────────────────────────
MCP protocol structure           →    Your agents can expose MCP tools
Agent workflow orchestration      →    Your LangGraph design is validated
Performance baselines for AI     →    Realistic latency targets for your agents
Tool-calling patterns            →    Your CLI tools follow same contracts
Scaling LLM inference            →    When to use Ollama vs cloud
Token cost at scale              →    Pricing for CodeLens Pro tier
```

## Combined Resume (GSTN + Topaz + CodeLens)

```
EXPERIENCE:
Infosys Limited — SDE                                    [Date] – Present

Project 1: GSTN — National Tax Platform (5 years)
  Tech: Java, Spring Boot, Angular, Redis, Kafka, Oracle
  [Your 8 existing bullets]

Project 2: Topaz Fabric Studio — AI Agent Platform (current)
  Tech: JMeter, Grafana, MCP Protocol, Agent Orchestration
  • Designed performance benchmarks for enterprise AI agent platform...

SIDE PROJECT: CodeLens AI — Code Intelligence Platform
  Tech: Go, Python, LangGraph, Elasticsearch, Angular
  [Your CodeLens bullet]
```

---

# 8. ONLINE PRESENCE BLUEPRINT

## GitHub Profile README

```markdown
# Hi, I'm Jayanti Vishnoi

**Software Development Engineer | 5.6 Years | Full-Stack + AI/Agents**

Building India's national tax platform (15.2M taxpayers) by day.
Building AI-powered developer tools by night.

## What I Work With
Backend: Java · Spring Boot · Redis · Kafka · XA Transactions
Frontend: Angular · TypeScript · RxJS · AngularJS (legacy migration)
AI/Agents: Python · LangGraph · RAG · MCP Protocol · Ollama
Systems: Go · Elasticsearch · MongoDB · GraphQL · Docker

## Featured Projects
- CodeLens AI — CLI + VS Code extension for AI code review & docs
- Observability Lab — Spring Boot + Prometheus + Grafana + Jaeger
- System Design Notes — Solutions to 20+ system design problems

## Recent Blog Posts
[links to dev.to articles]

## LeetCode Stats
[badge from leetcard.jacoblin.cool]
```

## Repos to Create (Priority Order)

| Repo | What It Shows | When |
|---|---|---|
| `codelens-cli` | Go, goroutines, AI, CLI tools | Week 1-4 |
| `codelens-vscode` | TypeScript, VS Code API, extension | Week 5-8 |
| `observability-lab` | Docker, Grafana, Prometheus, Jaeger | Week 2 (weekend) |
| `system-design-notes` | Architecture thinking, diagrams | Ongoing |
| `leetcode-solutions` | DSA, clean code, multiple languages | Ongoing |

## What Makes a Repo Stand Out

```
EVERY repo MUST have:
├── README.md (description, architecture diagram, screenshots/GIF, how to run)
├── Clean commit history (meaningful messages)
├── CI/CD badge (GitHub Actions — green ✓)
├── Coverage badge (Codecov)
├── Issues tab (even self-created tasks)
└── Releases (tagged versions with changelogs)
```

## Tech Blog Strategy

**Platform: Start with dev.to** (largest built-in audience, instant SEO)

### Blog Post Plan (12 Posts Over 12 Weeks)

| # | Title | Based On | Week |
|---|---|---|---|
| 1 | "How I Designed a 12-Scenario Financial State Machine in Java" | Bullet 1 / CR28625A | 1 |
| 2 | "Migrating 70K+ LOC from AngularJS to Angular — The Strangler Fig Way" | Bullet 6 / gstn-apps | 2 |
| 3 | "3 Layers of Concurrency Control That Saved Us From Race Conditions" | Bullet 2 / Redis+XA | 4 |
| 4 | "Building a Code Intelligence CLI in Go — Architecture & Decisions" | CodeLens project | 5 |
| 5 | "Performance Testing AI Agent Platforms: What's Different?" | Topaz work | 6 |
| 6 | "I Added OpenTelemetry to My Spring Boot App — Here's What I Found" | Observability lab | 7 |
| 7 | "Graph Traversal on the Frontend: DFS With Cycle Detection in JS" | Bullet 5 | 8 |
| 8 | "Publishing My First VS Code Extension — What I Learned" | CodeLens extension | 9 |
| 9 | "Multi-Tenant DB Routing With Spring: ThreadLocal + AbstractRoutingDataSource" | Bullet 4 | 10 |
| 10 | "RAG Pipeline From Scratch: Indexing a Codebase for Semantic Search" | CodeLens AI | 11 |
| 11 | "LangGraph Agents: Building a Code Review Bot With State Machine Orchestration" | CodeLens agents | 12 |
| 12 | "What I Learned Building a Side Project With 6 Technologies" | Retrospective | 12 |

### Blog Post Template

```markdown
# Title (How I [Did X] Using [Technology] — [Result])

## The Problem (2-3 sentences)
## Why It's Hard (3-4 sentences)
## The Solution (main content — code + diagrams)
## What I Learned (3-5 bullet points)
## Connect With Me (links)
```

### Amplification After Each Post

```
1. Share on LinkedIn with 3-line hook + link
2. Share on Twitter/X with key takeaway
3. Post in relevant subreddits (r/java, r/angular, r/programming)
4. Share in Discord communities
5. Cross-post to Hashnode (canonical URL to dev.to)
```

## LinkedIn Optimization

### Headline
```
Software Development Engineer | Java · Spring Boot · Angular · Go · AI Agents
Building India's national tax platform (15.2M users) | Side: AI Code Intelligence Tools
```

### About Section
```
Full-stack engineer with 5.6 years building distributed systems at scale.

Currently: Performance engineering for AI agent platforms (Infosys Topaz)
Previously: Financial state machines, multi-tenant routing, graph-traversal
            engines for India's GST platform (15.2M taxpayers)
Side project: CodeLens AI — open-source code intelligence CLI + VS Code extension

What I build:
• Backend: Java/Spring Boot — distributed transactions, event-driven architectures
• Frontend: Angular/TypeScript — incremental migration of 70K+ LOC legacy systems
• AI/Agents: Python/LangGraph — RAG pipelines, multi-agent orchestration, MCP tools
• Systems: Go — high-concurrency CLI tools, concurrent indexing engines

Open to SDE-2/SDE-3 roles in distributed systems, platform engineering, or AI infrastructure.
```

### Featured Section (Pin These)
1. Best blog post
2. CodeLens GitHub repo
3. VS Code extension marketplace link
4. A system design diagram

## LeetCode Profile

```
TARGET: 150+ problems, 100+ medium, rating 1800+

DAILY: 1-2 problems
WEEKLY: Sunday contest (builds rating)
TRACK: Streak badge, rating card on GitHub README

Organize solutions in GitHub:
leetcode-solutions/
├── arrays-hashing/ (with pattern explanations)
├── graphs/ ("How this relates to my appeal case traversal")
├── dynamic-programming/
├── system-design/ (LRU cache, design Twitter, rate limiter)
└── weekly-contests/
```

## Twitter/X Strategy

```
Bio: "SDE | 5.6 yrs | Java · Spring Boot · Go · Angular · AI Agents
      Building @codelens_ai | Writing about distributed systems"

DAILY: 1 tweet (what you learned, code snippet, progress)
WEEKLY: 1 thread (deep dive on a technical topic)
MONTHLY: 1 milestone post (shipped something)
```

## Where to Post/Share

| Platform | What | When |
|---|---|---|
| **Hacker News (Show HN)** | CLI tool, extension | After working MVP |
| **Product Hunt** | VS Code extension, web app | After polished launch |
| **Reddit** | r/programming, r/java, r/angular, r/golang, r/LocalLLaMA | Weekly |
| **Dev.to** | All blog posts | Weekly |
| **IndieHackers** | Monetization journey | Monthly updates |
| **Twitter/X** | Daily insights, threads, project updates | Daily |

## System Design Portfolio (GitHub Repo)

```
system-design-notes/
├── README.md
├── problems/
│   ├── 01-url-shortener.md
│   ├── 02-rate-limiter.md
│   ├── 05-payment-system.md          ← your actual experience
│   ├── 06-workflow-engine.md          ← your actual experience
│   ├── 07-multi-tenant-routing.md     ← your actual experience
│   └── 10-ai-agent-platform.md       ← from Topaz experience
├── concepts/
│   ├── caching-strategies.md
│   ├── distributed-transactions.md    ← your actual experience
│   └── consistency-models.md
└── diagrams/
```

## Must-Read Resources

### System Design
```
FREE:
- github.com/donnemartin/system-design-primer (200K+ stars)
- github.com/karanpratapsingh/system-design
- ByteByteGo Newsletter (weekly, free tier)
- Martin Fowler's blog
- highscalability.com

BOOKS:
- "System Design Interview Vol 1 & 2" — Alex Xu
- "Designing Data-Intensive Applications" — Martin Kleppmann
```

### Java / Spring Boot
```
- Baeldung.com (reference for any Spring topic)
- "Effective Java" — Joshua Bloch
- "Java Concurrency in Practice" — Brian Goetz
- Vlad Mihalcea's blog (JPA/Hibernate deep dives)
```

### Go
```
- gobyexample.com (quick start)
- "Let's Go" by Alex Edwards
- "Concurrency in Go" — Katherine Cox-Buday
```

### AI / Agents / LLMs
```
- LangChain / LangGraph docs
- Anthropic's MCP spec (modelcontextprotocol.io)
- Simon Willison's blog
- Andrej Karpathy's YouTube
```

### Career Growth
```
- staffeng.com (what senior+ engineers actually do)
- "The Staff Engineer's Path" — Tanya Reilly
- Gergely Orosz's Pragmatic Engineer newsletter
```

---

# 9. TWELVE-WEEK MASTER SCHEDULE

## Weekly Routine

```
MONDAY:    DSA (45 min) → Build project (2-3 hrs) → Blog/LinkedIn post
TUESDAY:   DSA (45 min) → Build project (2-3 hrs) → System design (45 min)
WEDNESDAY: DSA (45 min) → Build project (2-3 hrs) → Mock interview
THURSDAY:  DSA (45 min) → Build project (2-3 hrs) → Read tech articles
FRIDAY:    DSA (45 min) → Build project (2-3 hrs) → Review week + plan next
SATURDAY:  LC contest (1.5 hrs) → Project deep work (4 hrs)
SUNDAY:    System design (2 hrs) → Blog writing (2 hrs) → REST
```

## Week-by-Week Tracker

```
WEEK 1:  □ GitHub profile    □ 7 LC problems  □ Blog #1 drafted    □ CLI scaffold
WEEK 2:  □ Blog #1 published □ 14 LC total    □ Observability lab  □ Embeddings work
WEEK 3:  □ LinkedIn updated  □ 21 LC total    □ CLI review works   □ Blog #2 drafted
WEEK 4:  □ CLI v0.1 released □ 28 LC total    □ Blog #2 published  □ 1st mock interview
WEEK 5:  □ VSCode ext start  □ 35 LC total    □ Blog #3 published  □ System design repo
WEEK 6:  □ Ext chat works    □ 42 LC total    □ Blog #4 drafted    □ 2nd mock interview
WEEK 7:  □ Ext published     □ 50 LC total    □ Blog #4 published  □ Share in communities
WEEK 8:  □ 3rd mock interv   □ 60 LC total    □ Blog #5 drafted    □ Topaz blog drafted
WEEK 9:  □ Java backend      □ 70 LC total    □ Blog #5 published  □ START APPLYING
WEEK 10: □ 4th mock interv   □ 80 LC total    □ Blog #6 drafted    □ Kafka pipeline
WEEK 11: □ Angular dashboard □ 90 LC total    □ Show HN post       □ Blog #6 published
WEEK 12: □ Full stack done   □ 100 LC total   □ Product Hunt prep  □ APPLY ACTIVELY
```

## At Week 12 You Will Have

```
✅ 100+ LeetCode problems (with contest rating)
✅ 2+ GitHub repos with stars and CI/CD green badges
✅ VS Code extension on marketplace with installs
✅ 6+ published tech blog posts on dev.to
✅ LinkedIn fully optimized with recommendations + activity
✅ 3+ mock interviews completed (DSA + system design)
✅ System design notes repo with 10+ problems
✅ Observability lab with Grafana screenshots
✅ Twitter/X presence with followers
✅ Show HN post (if CLI is ready)
✅ Design docs in your repo (architecture, agents, indexing)
✅ Testing strategy with 80%+ coverage on core packages
✅ CI/CD pipeline you own (GitHub Actions)
✅ Topaz performance testing experience + blog post
```

## Where People Find You

```
Google "Jayanti Vishnoi developer" →
  ├── LinkedIn (optimized, active, recommendations)
  ├── GitHub (pinned repos, green activity, stars)
  ├── dev.to blog (6+ technical articles)
  ├── VS Code Marketplace (extension with installs)
  └── Twitter/X (consistent technical content)

What they see:
  ├── "This person BUILDS things" (repos, extension, CLI)
  ├── "This person THINKS deeply" (blog posts, design docs)
  ├── "This person COMMUNICATES well" (clear writing, diagrams)
  ├── "This person solves HARD problems" (LeetCode, system design)
  └── "This person is CURRENT" (AI agents, Go, MCP, observability)

What they conclude:
  "This is not a typical service-company developer.
   This person has depth, visibility, and ships things.
   Let's interview them."
```

---

# HONEST TRUTH

Your **technical depth is already SDE-3 caliber** — the 12-scenario state machine, XA 2PC, graph traversal with cycle detection, migration architecture. Most SDE-2s at product companies haven't built anything this complex.

Your gap is **visibility + format**, not skill:
1. Nobody can SEE your work (no GitHub, no blog, no public signal)
2. You haven't practiced the INTERVIEW FORMAT (system design whiteboard, LC timing)
3. You don't articulate NUMBERS (latency, QPS, cache hit rate)
4. You don't articulate LEADERSHIP (it probably exists but you don't say it)

Fix those 4 things and you're competitive at Flipkart/PhonePe/Razorpay/Swiggy level — and borderline for Amazon/Google.

Not being on a project right now is your **best-case scenario** — 6 hours of focused daily prep for 12 weeks = a transformed profile that's stronger than most SDE-2s at product companies who are too busy with work to build anything visible.

---

*Last Updated: April 29, 2026*
*Compiled from full conversation: Gen AI roadmap, side project plan, gap analysis, online presence blueprint*
*Related documents:*
- *Resume_FullStack_Final.md — 8 ATS resume bullets*
- *CodeLens_AI_Project_Plan.md — detailed project plan with data models, API design, agent design*
- *Resume_Bullets_Explainer.md — what you actually did for each bullet*
- *Interview_Preparation_Guide.md — 4-week study plan, concepts, walkthroughs*
- *SDE2_SDE3_Complete_Prep_Reference.md — 18-section master reference*
