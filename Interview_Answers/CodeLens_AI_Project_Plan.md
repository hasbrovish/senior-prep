# CodeLens AI — Project Plan & Execution Guide
## Intelligent Code Search, Review & Documentation Platform
### Author: Jayanti Vishnoi | Target: Side Project + Resume Booster + Monetizable Product

---

# TABLE OF CONTENTS

1. [Product Vision](#1-product-vision)
2. [Core Features (MVP)](#2-core-features-mvp)
3. [Architecture Decision Records](#3-architecture-decision-records)
4. [Tech Stack Justification](#4-tech-stack-justification)
5. [Data Models](#5-data-models)
6. [API Design](#6-api-design)
7. [AI Agent Design](#7-ai-agent-design)
8. [Phase-by-Phase Build Plan](#8-build-plan)
9. [Week-by-Week Sprint Plan](#9-sprint-plan)
10. [Repository Structure](#10-repo-structure)
11. [Deployment Architecture](#11-deployment)
12. [Monetization Strategy](#12-monetization)
13. [Risk Register](#13-risks)
14. [Resume Impact Assessment](#14-resume-impact)

---

# 1. PRODUCT VISION

## One-Liner
> CodeLens AI: Index any codebase → Search it semantically → Get AI-powered reviews, docs, and answers.

## Problem Statement
- Developers spend 60% of time **reading** code, not writing it
- Onboarding to a new codebase takes 3-6 months
- Code reviews are manual, inconsistent, and slow
- Documentation is always outdated or missing
- Existing tools (Sourcegraph, SonarQube) are expensive and don't have AI

## Solution
A **CLI-first, extension-powered** code intelligence tool that:
1. Indexes any codebase locally (Go binary — fast, zero infrastructure)
2. Makes it searchable (exact + semantic)
3. Auto-generates documentation
4. Reviews code for bugs, security issues, and code smells
5. Answers natural-language questions about the codebase

## Target Users
- Individual developers (CLI + VS Code extension)
- Small teams (shared knowledge base)
- Enterprise (self-hosted, custom models, CI/CD integration)

---

# 2. CORE FEATURES (MVP)

## Phase 1: Go CLI (Weeks 1-4)
```
$ codelens init                     # Initialize project config
$ codelens index .                  # Index all files
$ codelens search "redis lock"      # Keyword + semantic search
$ codelens review src/main.go       # AI code review
$ codelens docs src/auth/           # Generate documentation
$ codelens ask "how does auth work" # Q&A over codebase
$ codelens report --format html     # Generate analysis report
```

## Phase 2: VS Code Extension (Weeks 5-8)
```
Features:
├── Sidebar panel: Chat with your codebase
├── Inline decorations: Complexity score per function
├── Hover provider: AI-generated function summary
├── Command palette:
│   ├── "CodeLens: Review this file"
│   ├── "CodeLens: Generate docs"
│   ├── "CodeLens: Explain selection"
│   └── "CodeLens: Find similar code"
├── Status bar: Project health score
├── CodeLens (VS Code feature): Inline "Review | Docs | Explain" above functions
└── Webview panel: Full analysis dashboard
```

## Phase 3: Cloud Backend (Weeks 9-12)
```
Features:
├── GitHub/GitLab OAuth: Connect your repo
├── Auto-index on push: Webhook triggers re-indexing
├── Team knowledge base: Shared Q&A history
├── PR review bot: Auto-comment on pull requests
├── Dashboard: Code health metrics over time
├── Billing: Stripe integration, usage metering
└── Admin: Org management, SSO, audit logs
```

## Phase 4: Chrome Extension + CI/CD (Weeks 13-16)
```
Features:
├── Chrome extension: AI review button on GitHub PR pages
├── GitHub Action: codelens-review-action
├── Slack bot: /codelens ask "how does payment work"
└── API: Public REST/GraphQL for integrations
```

---

# 3. ARCHITECTURE DECISION RECORDS

## ADR-001: CLI-First Architecture
**Decision:** Build Go CLI as the core engine. All other interfaces (VS Code, Chrome, Web) wrap it.
**Rationale:**
- Single source of truth for all logic
- CLI runs offline — no internet dependency
- Binary is bundled inside extensions as a child process
- Users who don't want a GUI still get full functionality
- Easier to test (CLI is just stdin/stdout)

## ADR-002: Go for Core Engine (Not Java/Python)
**Decision:** Go for the CLI and indexer.
**Rationale:**
- Single binary distribution (no JVM/Python runtime needed)
- Goroutines for concurrent file crawling (1000s of files in parallel)
- Low memory footprint (~20MB vs ~200MB for JVM)
- Fast startup (<100ms vs ~2s for Spring Boot)
- tree-sitter bindings available in Go for AST parsing
**Trade-off:** Java has better enterprise ecosystem; Python has better AI ecosystem. Go is the sweet spot for the core engine.

## ADR-003: Local-First AI (Ollama for v1)
**Decision:** Use Ollama (local LLM) as default, OpenAI/Anthropic as optional upgrade.
**Rationale:**
- Zero cost for users (no API key required)
- No data leaves user's machine (privacy/security selling point)
- Works offline (airplane, air-gapped networks)
- Upgrade path: switch to GPT-4/Claude for higher quality
**Trade-off:** Local models (Llama 3, CodeLlama) are ~80% as good as GPT-4 for code tasks. Good enough for MVP.

## ADR-004: SQLite-vss for Local Vector Store
**Decision:** SQLite with virtual table extension for vector search (local mode).
**Rationale:**
- Zero infrastructure — single file on disk
- Ships with the Go binary
- 100K vectors in <50MB disk space
- Sufficient for single-repo indexing (most repos are <10K files)
**Trade-off:** Not suitable for multi-repo cloud mode → use pgvector/ChromaDB for cloud.

## ADR-005: GraphQL for Cloud API (Not REST)
**Decision:** GraphQL (Go gqlgen) for the cloud API layer.
**Rationale:**
- Dashboard needs counts only; code viewer needs full content + annotations
- One endpoint, flexible queries — avoids N+1 REST endpoints
- Type-safe schema generation with gqlgen
- Subscription support for real-time agent status
**Trade-off:** More complex than REST for simple CRUD. Worth it because read patterns vary widely.

## ADR-006: MongoDB for Analysis Storage
**Decision:** MongoDB for storing code analysis results and agent outputs.
**Rationale:**
- Each file type produces different analysis shapes (Java vs TS vs Go)
- Agent outputs are semi-structured (variable keys, nested objects)
- Schema evolves as we add new analysis types — no migrations needed
- Time-series analysis history (track code health over time)
**Trade-off:** No ACID transactions across documents. Not needed — each analysis is independent.

## ADR-007: Java/Spring Boot for Business Logic
**Decision:** Java for auth, billing, org management, and notification services.
**Rationale:**
- Spring Security for OAuth2 + JWT (battle-tested)
- Spring Data JPA for relational user/org/billing data (PostgreSQL)
- Kafka consumer for processing webhooks and notifications
- Your strongest backend skill — fastest to build
**Trade-off:** Heavier than Go for simple CRUD. Worth it for Spring ecosystem.

## ADR-008: OpenTelemetry from Day 1
**Decision:** Instrument every service with OTel from the first commit.
**Rationale:**
- Trace AI calls end-to-end (which agent, which model, how many tokens, how long)
- Token cost tracking (critical for pricing and profitability)
- Debugging multi-service flows without OTel is nightmare
- Demonstrates production mindset in interviews

---

# 4. TECH STACK JUSTIFICATION

## Per-Service Stack

### Go Service — Core Engine + API Gateway
```
Language:        Go 1.22+
GraphQL:         gqlgen (code-generated, type-safe)
AST Parsing:     tree-sitter-go (multi-language support)
Vector Store:    SQLite-vss (local), pgvector (cloud)
Search:          Elasticsearch 8.x (cloud mode)
Git Integration: go-git (pure Go git implementation)
HTTP:            chi router (lightweight)
WebSocket:       gorilla/websocket
OTel:            go.opentelemetry.io/otel
Testing:         go test + testify
Build:           goreleaser (cross-platform binary releases)
```

### Python Service — AI Agents
```
Language:        Python 3.11+
Framework:       FastAPI + uvicorn
AI Framework:    LangGraph 0.2+ (state machine agent orchestration)
LLM:             Ollama (local) / OpenAI / Anthropic (cloud)
Embeddings:      text-embedding-3-small (OpenAI) / nomic-embed (local)
Vector Store:    ChromaDB (agent-side semantic search)
OTel:            opentelemetry-python
Testing:         pytest + pytest-asyncio
```

### Java Service — Business Logic
```
Language:        Java 17+
Framework:       Spring Boot 3.2+
Auth:            Spring Security + OAuth2 (GitHub, Google)
Database:        PostgreSQL (users, orgs, billing)
ORM:             Spring Data JPA / Hibernate
Messaging:       Kafka (webhook events, notifications)
Caching:         Redis (session cache, rate limiting)
Billing:         Stripe Java SDK
Email:           Spring Mail (SendGrid)
OTel:            opentelemetry-java
Testing:         JUnit 5 + Mockito + Testcontainers
Build:           Maven / Gradle
```

### Angular — Web Dashboard
```
Framework:       Angular 17+ (standalone components)
State:           RxJS BehaviorSubject / NgRx (if grows)
UI:              PrimeNG (your existing knowledge)
GraphQL:         Apollo Angular
WebSocket:       RxJS WebSocketSubject
Charts:          ngx-charts / Chart.js
Code Viewer:     Monaco Editor (same as VS Code)
Markdown:        ngx-markdown (render AI-generated docs)
Build:           Nx monorepo (your existing knowledge)
```

### VS Code Extension
```
Language:        TypeScript
API:             VS Code Extension API
Webview:         Svelte or plain HTML (lightweight)
Communication:   Extension ↔ Go CLI via child_process.spawn()
State:           VS Code Memento (local persistence)
Publishing:      vsce (VS Code Extension CLI)
```

### Chrome Extension
```
Language:        TypeScript
UI:              Preact (3KB — tiny bundle size)
API:             Chrome Extension Manifest V3
Content Script:  Injects into github.com pages
Background:      Service Worker (API calls)
```

---

# 5. DATA MODELS

## MongoDB — Analysis Documents

```json
// Project document
{
  "_id": ObjectId,
  "name": "my-backend",
  "repoUrl": "github.com/user/repo",
  "language": "java",
  "fileCount": 342,
  "totalLOC": 45000,
  "lastIndexedAt": ISODate,
  "config": {
    "ignorePaths": ["node_modules", "build"],
    "reviewRules": ["security", "performance", "complexity"]
  }
}

// File analysis document (flexible schema per language)
{
  "_id": ObjectId,
  "projectId": ObjectId,
  "path": "src/main/java/DemandProcessingUtil.java",
  "language": "java",
  "loc": 4796,
  "hash": "sha256:abc123",
  "analysis": {
    "classes": [
      {
        "name": "DemandProcessingUtil",
        "methods": 47,
        "cyclomaticComplexity": 89,
        "annotations": ["@Service", "@Transactional"]
      }
    ],
    "issues": [
      {
        "type": "complexity",
        "severity": "high",
        "line": 1733,
        "message": "Method exceeds 500 LOC — extract sub-methods",
        "suggestion": "Split into processConfirmConfirm(), processConfirmReject(), ..."
      }
    ],
    "patterns": ["Strategy", "Factory", "State Machine"],
    "dependencies": ["LedgerService", "CaseFolder", "Redis"]
  },
  "documentation": {
    "summary": "Processes 12 financial scenarios for appeal order outcomes...",
    "methods": [
      { "name": "processSubsequentOrder", "doc": "..." }
    ]
  },
  "createdAt": ISODate
}

// Agent conversation document
{
  "_id": ObjectId,
  "projectId": ObjectId,
  "userId": ObjectId,
  "messages": [
    { "role": "user", "content": "How does the auth system work?", "ts": ISODate },
    { "role": "assistant", "content": "The auth system uses...", "ts": ISODate,
      "sources": ["src/auth/jwt.go:45", "src/middleware/auth.go:12"],
      "tokensUsed": 890, "model": "gpt-4", "latencyMs": 1200 }
  ]
}
```

## PostgreSQL — Business Data (Java/Spring Boot)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    github_id VARCHAR(100),
    plan VARCHAR(20) DEFAULT 'free',   -- free / pro / team / enterprise
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(id),
    plan VARCHAR(20) DEFAULT 'team',
    stripe_customer_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY,
    org_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    repo_url VARCHAR(500),
    webhook_secret VARCHAR(255),
    last_indexed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE usage_metrics (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    project_id UUID REFERENCES projects(id),
    action VARCHAR(50),  -- 'review', 'docs', 'ask', 'search'
    tokens_used INT,
    model VARCHAR(50),
    cost_usd DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    org_id UUID REFERENCES organizations(id),
    stripe_subscription_id VARCHAR(100),
    plan VARCHAR(20),
    status VARCHAR(20),  -- active / canceled / past_due
    current_period_end TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Elasticsearch — Code Index

```json
// Index mapping: code-chunks
{
  "mappings": {
    "properties": {
      "project_id":    { "type": "keyword" },
      "file_path":     { "type": "keyword" },
      "language":      { "type": "keyword" },
      "chunk_type":    { "type": "keyword" },     // "function", "class", "block"
      "name":          { "type": "text" },         // function/class name
      "content":       { "type": "text",           // actual code
                         "analyzer": "code_analyzer" },
      "documentation": { "type": "text" },         // AI-generated docs
      "line_start":    { "type": "integer" },
      "line_end":      { "type": "integer" },
      "complexity":    { "type": "integer" },
      "imports":       { "type": "keyword" },      // dependencies
      "indexed_at":    { "type": "date" }
    }
  },
  "settings": {
    "analysis": {
      "analyzer": {
        "code_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "camelcase_split", "snake_case_split"]
        }
      }
    }
  }
}
```

---

# 6. API DESIGN

## GraphQL Schema (Go gqlgen)

```graphql
type Query {
  # Projects
  project(id: ID!): Project
  projects(orgId: ID!, first: Int, after: String): ProjectConnection

  # Search
  search(projectId: ID!, query: String!, type: SearchType): SearchResults

  # File
  file(projectId: ID!, path: String!): FileAnalysis

  # Conversations
  conversations(projectId: ID!, first: Int): [Conversation]
}

type Mutation {
  # Project management
  createProject(input: CreateProjectInput!): Project
  indexProject(id: ID!): IndexJob
  deleteProject(id: ID!): Boolean

  # AI actions
  reviewFile(projectId: ID!, path: String!): ReviewResult
  generateDocs(projectId: ID!, path: String!): DocsResult
  askQuestion(projectId: ID!, question: String!): Answer

  # Billing
  createCheckoutSession(plan: Plan!): CheckoutSession
  cancelSubscription(orgId: ID!): Boolean
}

type Subscription {
  # Real-time agent status
  agentStatus(jobId: ID!): AgentStatusUpdate
  # Chat streaming
  chatStream(projectId: ID!, question: String!): ChatToken
}

type Project {
  id: ID!
  name: String!
  repoUrl: String
  fileCount: Int!
  totalLOC: Int!
  lastIndexedAt: DateTime
  healthScore: Float           # 0-100
  issues: IssuesSummary
  languages: [LanguageBreakdown!]!
}

type FileAnalysis {
  path: String!
  language: String!
  loc: Int!
  content: String!
  complexity: Int!
  issues: [Issue!]!
  documentation: FileDocumentation
  patterns: [String!]!
  dependencies: [String!]!
}

type SearchResults {
  hits: [SearchHit!]!
  total: Int!
  took: Int!                   # milliseconds
}

type SearchHit {
  filePath: String!
  lineStart: Int!
  lineEnd: Int!
  content: String!
  highlight: String!           # with <em> tags
  score: Float!
}

type Answer {
  text: String!
  sources: [SourceReference!]!
  tokensUsed: Int!
  model: String!
  latencyMs: Int!
}

enum SearchType { CODE, SEMANTIC, SYMBOL }
enum Plan { FREE, PRO, TEAM, ENTERPRISE }
```

## CLI Command Spec

```yaml
commands:
  init:
    description: Initialize CodeLens project
    flags:
      --language: Override auto-detected language
      --ignore: Paths to ignore (glob patterns)
    output: .codelens/config.yaml

  index:
    description: Index codebase into local vector store
    args: [path]
    flags:
      --force: Re-index all files (not just changed)
      --workers: Number of concurrent goroutines (default: CPU count)
    output: "Indexed 342 files (45,000 LOC) in 3.2s"

  search:
    description: Search code (keyword + semantic)
    args: [query]
    flags:
      --type: code | semantic | symbol (default: auto)
      --limit: Max results (default: 10)
      --language: Filter by language
    output: Matched code snippets with file:line references

  review:
    description: AI code review
    args: [file_or_directory]
    flags:
      --rules: security,performance,complexity (default: all)
      --model: ollama | openai | anthropic (default: ollama)
      --format: text | json | sarif | github (default: text)
    output: List of issues with severity, line, message, suggestion

  docs:
    description: Generate documentation
    args: [file_or_directory]
    flags:
      --output: Output directory (default: ./docs/)
      --format: markdown | html | json
    output: Generated documentation files

  ask:
    description: Ask a question about the codebase
    args: [question]
    flags:
      --model: ollama | openai | anthropic
      --context: Number of relevant chunks to include (default: 5)
    output: Answer with source references

  report:
    description: Generate full project analysis report
    flags:
      --format: html | json | pdf
      --output: Output file path
    output: Comprehensive code health report
```

---

# 7. AI AGENT DESIGN

## LangGraph State Machine

```
                    ┌─────────┐
                    │  START   │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │ CLASSIFY │ ← Determine intent
                    │  INTENT  │   (review/docs/search/ask)
                    └────┬────┘
                         │
            ┌────────────┼────────────┬──────────────┐
            ▼            ▼            ▼              ▼
     ┌──────────┐ ┌──────────┐ ┌──────────┐  ┌──────────┐
     │ REVIEW   │ │ DOC_GEN  │ │ SEARCH   │  │  Q&A     │
     │ AGENT    │ │ AGENT    │ │ AGENT    │  │  AGENT   │
     └────┬─────┘ └────┬─────┘ └────┬─────┘  └────┬─────┘
          │             │            │              │
          │        ┌────▼─────┐     │              │
          │        │ VALIDATE │     │              │
          │        │ OUTPUT   │     │              │
          │        └────┬─────┘     │              │
          │             │            │              │
          └─────────────┼────────────┴──────────────┘
                        │
                   ┌────▼────┐
                   │ FORMAT  │ ← Format for CLI/extension/web
                   │ OUTPUT  │
                   └────┬────┘
                        │
                   ┌────▼────┐
                   │  END    │
                   └─────────┘
```

## Agent Tool Definitions

```python
# Tools that agents can call

@tool
def read_file(path: str, start_line: int = None, end_line: int = None) -> str:
    """Read a file from the indexed project."""

@tool
def search_code(query: str, search_type: str = "semantic") -> list[SearchResult]:
    """Search the codebase using keyword or semantic search."""

@tool
def get_file_ast(path: str) -> dict:
    """Get the parsed AST (functions, classes, imports) of a file."""

@tool
def get_dependencies(path: str) -> list[str]:
    """Get files that this file imports/depends on."""

@tool
def get_dependents(path: str) -> list[str]:
    """Get files that import/depend on this file."""

@tool
def run_linter(path: str, rules: list[str]) -> list[Issue]:
    """Run static analysis rules on a file."""

@tool
def get_git_history(path: str, limit: int = 10) -> list[Commit]:
    """Get recent git commits that modified this file."""

@tool
def get_similar_code(code_snippet: str, limit: int = 5) -> list[SearchResult]:
    """Find similar code patterns in the codebase."""
```

## Agent Prompts (Simplified)

```python
REVIEW_AGENT_SYSTEM = """
You are a senior code reviewer. Analyze the provided code for:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues (N+1 queries, unnecessary allocations, blocking calls)
3. Code smells (long methods, deep nesting, magic numbers)
4. Design issues (SRP violations, tight coupling)

For each issue, provide:
- Severity: critical / high / medium / low
- Line number
- Description
- Suggested fix (code snippet)

Use tools to read related files and understand context before reviewing.
Do NOT report style issues or formatting.
"""

DOC_AGENT_SYSTEM = """
You are a technical writer generating documentation for code.
For each function/class/module, generate:
1. One-line summary
2. Detailed description (what it does, why it exists)
3. Parameters with types and descriptions
4. Return value description
5. Example usage
6. Related functions/classes

Use tools to read the actual implementation and understand context.
Write for a developer who has never seen this codebase.
"""

QA_AGENT_SYSTEM = """
You are a codebase expert. Answer questions about the project.
Always cite specific files and line numbers.
If you're not sure, say so — don't hallucinate.
Use tools to search the codebase and read relevant files.
Prefer showing actual code over describing it.
"""
```

---

# 8. PHASE-BY-PHASE BUILD PLAN

## Phase 1: Go CLI + Local Engine (Weeks 1-4)

### Week 1 — Project Setup + File Indexer
```
Tasks:
├── Initialize Go module, folder structure, CI/CD (GitHub Actions)
├── Implement file crawler with goroutines (concurrent directory walking)
├── Implement tree-sitter AST parser (extract functions, classes, imports)
├── Implement code chunker (split files into meaningful chunks)
├── Write unit tests for crawler and chunker
└── Deliverable: $ codelens index . works — crawls and parses files

Key Go concepts practiced:
- goroutines + WaitGroup for concurrent crawling
- channels for producer-consumer (crawler → parser → chunker)
- context.Context for cancellation
- embed for shipping tree-sitter grammars
```

### Week 2 — Embedding + Local Vector Store
```
Tasks:
├── Integrate Ollama API for local embeddings (nomic-embed-text)
├── Set up SQLite-vss for local vector storage
├── Implement embedding pipeline: chunk → embed → store
├── Implement semantic search: query → embed → vector search → rank
├── Implement keyword search: direct text matching with scoring
├── Write tests for search accuracy
└── Deliverable: $ codelens search "how does auth work" works

Key concepts practiced:
- Embedding generation and vector similarity (cosine distance)
- Hybrid search (keyword + semantic, reciprocal rank fusion)
- Batch processing (embed 100 chunks at once, not one-by-one)
```

### Week 3 — AI Review + Docs + Q&A
```
Tasks:
├── Integrate Ollama for local LLM inference
├── Implement review command: file → chunks → LLM → issues
├── Implement docs command: file → AST + code → LLM → documentation
├── Implement ask command: question → search → context → LLM → answer
├── Add --model flag for OpenAI/Anthropic as alternative
├── Implement SARIF output format (standard for code analysis)
└── Deliverable: $ codelens review, docs, ask all work

Key concepts practiced:
- Prompt engineering (system prompt, few-shot examples)
- RAG pipeline (retrieve → augment → generate)
- Output parsing (structured JSON from LLM)
```

### Week 4 — Polish, Config, Report
```
Tasks:
├── Implement .codelens/config.yaml (project configuration)
├── Implement $ codelens report --format html (full analysis report)
├── Incremental indexing (only re-index changed files based on hash)
├── Add OpenTelemetry instrumentation (traces for every operation)
├── Cross-platform build with goreleaser (Linux, Mac, Windows)
├── README with installation, usage, demo GIF
├── Write integration tests
└── Deliverable: Ship v0.1.0 to GitHub

Resume bullet earned:
"Built a cross-platform code intelligence CLI in Go with concurrent
file indexing (goroutines), hybrid search (keyword + semantic via
SQLite-vss), and local LLM integration (Ollama) — enabling offline
AI code review, documentation generation, and codebase Q&A."
```

---

## Phase 2: VS Code Extension (Weeks 5-8)

### Week 5 — Extension Scaffold + Sidebar Chat
```
Tasks:
├── Scaffold VS Code extension (yo code)
├── Bundle Go CLI binary inside extension
├── Implement sidebar webview (chat interface)
├── Extension spawns Go CLI as child process
├── Chat: user types question → Go CLI → answer displayed in sidebar
└── Deliverable: Extension installs, sidebar chat works

Key TypeScript concepts:
- VS Code Extension API (activate, commands, webview)
- child_process.spawn() for Go binary communication
- Message passing between extension host and webview
```

### Week 6 — Inline Features
```
Tasks:
├── CodeLens provider: "Review | Docs | Explain" above each function
├── Hover provider: Show AI summary on hover
├── Diagnostic provider: Show issues as squiggly underlines
├── Status bar: File complexity score
├── Tree view: Project issues organized by severity
└── Deliverable: Inline annotations work, issues show as diagnostics
```

### Week 7 — Commands + Productivity
```
Tasks:
├── Command palette: "Review this file", "Generate docs", "Explain selection"
├── Right-click context menu: "CodeLens: Explain this"
├── Auto-index on file save (debounced)
├── Settings UI: model selection, API key, ignore patterns
├── Progress notification for long-running operations
└── Deliverable: All commands work, settings configurable
```

### Week 8 — Polish + Publish
```
Tasks:
├── Extension icon, marketplace description, screenshots
├── Demo GIF / video for marketplace listing
├── Free tier logic (5 queries/day without API key)
├── Telemetry (anonymous usage stats, opt-in)
├── Publish to VS Code Marketplace
├── Write integration tests with @vscode/test-electron
└── Deliverable: Live on VS Code Marketplace

Resume bullet earned:
"Published a VS Code extension for AI-powered code intelligence —
featuring inline code review, auto-documentation, and codebase Q&A
with a bundled Go binary for local indexing and Ollama for offline
LLM inference."
```

---

## Phase 3: Cloud Backend (Weeks 9-12)

### Week 9 — Java/Spring Boot + Auth
```
Tasks:
├── Spring Boot project setup (Spring Initializr)
├── GitHub OAuth2 login (Spring Security)
├── User + Organization entities (PostgreSQL)
├── Project CRUD API
├── JWT token issuance for CLI/extension auth
└── Deliverable: Users can sign up via GitHub, create orgs/projects
```

### Week 10 — Kafka + Elasticsearch + MongoDB
```
Tasks:
├── Kafka: webhook events → code-index topic → Python consumer
├── Elasticsearch: code index, search API
├── MongoDB: analysis results, conversation history
├── Go service: GitHub webhook consumer → Kafka producer
├── Auto-index on git push
└── Deliverable: Push to GitHub → auto-index → searchable
```

### Week 11 — Python AI Service + LangGraph
```
Tasks:
├── FastAPI service with Kafka consumer
├── LangGraph agent orchestrator (review, docs, Q&A, search agents)
├── Multi-agent with tool calling (read file, search, get AST)
├── ChromaDB for cloud vector store
├── OpenTelemetry: trace every agent call, token cost
└── Deliverable: Full AI pipeline running in cloud mode
```

### Week 12 — Angular Dashboard + Billing
```
Tasks:
├── Angular app: project dashboard, code viewer, chat, reports
├── Apollo GraphQL integration
├── WebSocket for real-time agent status + chat streaming
├── Stripe billing integration (Java service)
├── Docker Compose for full stack local development
└── Deliverable: Full SaaS working end-to-end

Resume bullet earned:
"Designed a polyglot microservice architecture (Go + Java + Python)
with Kafka event-driven processing, Elasticsearch code search,
MongoDB flexible analysis storage, and LangGraph multi-agent
orchestration — deployed as a SaaS code intelligence platform
with Stripe billing and GitHub OAuth."
```

---

## Phase 4: Chrome Extension + CI/CD (Weeks 13-16)

### Week 13-14 — Chrome Extension
```
Tasks:
├── Manifest V3 extension scaffold
├── Content script: inject "Review with AI" button on GitHub PR pages
├── Popup: quick project search, recent conversations
├── Background service worker: API calls to cloud backend
├── Inline PR comments from AI review
└── Deliverable: Chrome extension on Chrome Web Store
```

### Week 15-16 — CI/CD + Launch
```
Tasks:
├── GitHub Action: codelens-review-action (SARIF upload)
├── Slack bot: /codelens ask "question"
├── Landing page (Next.js or static Angular)
├── Product Hunt launch preparation
├── Documentation site (Docusaurus or GitBook)
├── Public API documentation
└── Deliverable: Full product launched
```

---

# 9. WEEK-BY-WEEK SPRINT PLAN

| Week | Sprint | Focus | Deliverable |
|---|---|---|---|
| 1 | Go-1 | File crawler + AST parser | `codelens index .` works |
| 2 | Go-2 | Embeddings + search | `codelens search` works |
| 3 | Go-3 | AI review + docs + Q&A | `codelens review/docs/ask` work |
| 4 | Go-4 | Report + config + release | v0.1.0 on GitHub |
| 5 | VSC-1 | Extension scaffold + sidebar chat | Extension installs, chat works |
| 6 | VSC-2 | Inline features | CodeLens, hover, diagnostics |
| 7 | VSC-3 | Commands + settings | Full command palette |
| 8 | VSC-4 | Publish to marketplace | Live on VS Code Marketplace |
| 9 | Cloud-1 | Java auth + PostgreSQL | GitHub OAuth works |
| 10 | Cloud-2 | Kafka + ES + MongoDB | Auto-index pipeline |
| 11 | Cloud-3 | Python AI + LangGraph | Multi-agent running |
| 12 | Cloud-4 | Angular dashboard + Stripe | Full SaaS |
| 13 | Chrome-1 | Chrome extension MVP | PR review button works |
| 14 | Chrome-2 | Chrome polish + store | Live on Chrome Web Store |
| 15 | CI-1 | GitHub Action + Slack bot | CI/CD integration |
| 16 | Launch | Landing page + Product Hunt | Public launch |

---

# 10. REPOSITORY STRUCTURE

```
codelens/
├── cli/                          # Go CLI (core engine)
│   ├── cmd/
│   │   ├── root.go               # cobra CLI root
│   │   ├── index.go              # codelens index
│   │   ├── search.go             # codelens search
│   │   ├── review.go             # codelens review
│   │   ├── docs.go               # codelens docs
│   │   ├── ask.go                # codelens ask
│   │   └── report.go             # codelens report
│   ├── internal/
│   │   ├── crawler/              # file system crawler
│   │   ├── parser/               # tree-sitter AST parser
│   │   ├── chunker/              # code chunker
│   │   ├── embedder/             # embedding generation
│   │   ├── store/                # SQLite-vss vector store
│   │   ├── search/               # hybrid search engine
│   │   ├── llm/                  # Ollama/OpenAI/Anthropic client
│   │   ├── reviewer/             # code review logic
│   │   ├── docgen/               # documentation generator
│   │   └── telemetry/            # OpenTelemetry setup
│   ├── go.mod
│   ├── go.sum
│   └── Makefile
│
├── vscode-extension/             # VS Code Extension (TypeScript)
│   ├── src/
│   │   ├── extension.ts          # activation + command registration
│   │   ├── providers/
│   │   │   ├── codelens.ts       # CodeLens provider
│   │   │   ├── hover.ts          # hover provider
│   │   │   ├── diagnostics.ts    # issue diagnostics
│   │   │   └── tree.ts           # tree view provider
│   │   ├── webview/
│   │   │   └── chat/             # sidebar chat webview
│   │   ├── cli/
│   │   │   └── bridge.ts         # Go CLI child process communication
│   │   └── config.ts             # settings management
│   ├── package.json
│   └── tsconfig.json
│
├── chrome-extension/             # Chrome Extension (TypeScript + Preact)
│   ├── src/
│   │   ├── content/              # content scripts (inject into GitHub)
│   │   ├── popup/                # extension popup
│   │   ├── background/           # service worker
│   │   └── api/                  # backend API client
│   └── manifest.json
│
├── ai-service/                   # Python AI Agents
│   ├── app/
│   │   ├── main.py               # FastAPI app
│   │   ├── agents/
│   │   │   ├── orchestrator.py   # LangGraph state machine
│   │   │   ├── reviewer.py       # code review agent
│   │   │   ├── doc_writer.py     # documentation agent
│   │   │   ├── qa.py             # Q&A agent
│   │   │   └── tools.py          # agent tools
│   │   ├── rag/
│   │   │   ├── embedder.py       # embedding pipeline
│   │   │   ├── retriever.py      # vector search
│   │   │   └── chunker.py        # code chunking
│   │   └── telemetry.py          # OTel setup
│   ├── requirements.txt
│   └── Dockerfile
│
├── backend/                      # Java/Spring Boot Business Logic
│   ├── src/main/java/com/codelens/
│   │   ├── auth/                 # OAuth2 + JWT
│   │   ├── user/                 # user management
│   │   ├── org/                  # organization management
│   │   ├── project/              # project CRUD
│   │   ├── billing/              # Stripe integration
│   │   ├── webhook/              # GitHub webhook handler
│   │   ├── kafka/                # Kafka producer/consumer
│   │   └── notification/         # email/Slack notifications
│   ├── pom.xml
│   └── Dockerfile
│
├── gateway/                      # Go GraphQL Gateway
│   ├── graph/
│   │   ├── schema.graphql        # GraphQL schema
│   │   ├── resolver.go           # generated resolvers
│   │   └── model.go              # generated models
│   ├── main.go
│   └── Dockerfile
│
├── web-dashboard/                # Angular Web App
│   ├── src/app/
│   │   ├── dashboard/            # project dashboard
│   │   ├── code-viewer/          # Monaco editor + annotations
│   │   ├── chat/                 # Q&A chat interface
│   │   ├── reports/              # analysis reports
│   │   ├── settings/             # project/org settings
│   │   └── shared/               # shared components, services
│   ├── angular.json
│   └── package.json
│
├── docker-compose.yml            # Full stack local dev
├── docker-compose.prod.yml       # Production deployment
├── .github/workflows/            # CI/CD
│   ├── cli-build.yml
│   ├── extension-publish.yml
│   ├── backend-deploy.yml
│   └── ai-service-deploy.yml
├── docs/                         # Documentation site
├── landing-page/                 # Marketing landing page
└── README.md
```

---

# 11. DEPLOYMENT ARCHITECTURE

## Local Development (Docker Compose)

```yaml
# docker-compose.yml
services:
  cli:
    build: ./cli
    volumes: [./test-repo:/project]

  gateway:
    build: ./gateway
    ports: [4000:4000]
    depends_on: [elasticsearch, mongodb]

  backend:
    build: ./backend
    ports: [8080:8080]
    depends_on: [postgres, redis, kafka]
    environment:
      - SPRING_PROFILES_ACTIVE=local
      - GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID}

  ai-service:
    build: ./ai-service
    ports: [8000:8000]
    depends_on: [kafka, chromadb]
    environment:
      - OLLAMA_HOST=http://ollama:11434

  web-dashboard:
    build: ./web-dashboard
    ports: [4200:80]

  # Infrastructure
  postgres:
    image: postgres:16
    ports: [5432:5432]
  
  mongodb:
    image: mongo:7
    ports: [27017:27017]
  
  elasticsearch:
    image: elasticsearch:8.12.0
    ports: [9200:9200]
  
  redis:
    image: redis:7-alpine
    ports: [6379:6379]
  
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports: [9092:9092]
  
  chromadb:
    image: chromadb/chroma:latest
    ports: [8001:8000]
  
  ollama:
    image: ollama/ollama:latest
    ports: [11434:11434]

  # Observability
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports: [16686:16686]    # Jaeger UI
  
  grafana:
    image: grafana/grafana:latest
    ports: [3000:3000]
```

## Production (Cloud)
```
Option A: AWS
  - ECS Fargate for services
  - RDS PostgreSQL
  - ElastiCache Redis
  - Amazon OpenSearch (Elasticsearch)
  - MongoDB Atlas
  - MSK (Kafka)
  - S3 for report storage
  - CloudFront for web dashboard
  - Cost: ~$150-300/month at small scale

Option B: Railway / Render (Simpler)
  - Railway for Go, Java, Python services
  - Supabase for PostgreSQL
  - Upstash for Redis + Kafka
  - MongoDB Atlas free tier
  - Elastic Cloud free tier
  - Cost: ~$50-100/month at small scale
```

---

# 12. MONETIZATION STRATEGY

## Pricing Tiers

| Tier | Price | Features | Target |
|---|---|---|---|
| **Free** | $0 | CLI (local only), 5 VS Code queries/day, local LLM | Individual devs |
| **Pro** | $8/month | Unlimited queries, GPT-4/Claude, cloud sync, PR review | Serious devs |
| **Team** | $15/user/month | Shared knowledge base, org dashboard, GitHub Action | Small teams |
| **Enterprise** | $500+/month | Self-hosted, SSO, custom models, audit logs, SLA | Companies |

## Revenue Projections (Conservative)

| Month | Free Users | Pro | Team | MRR |
|---|---|---|---|---|
| 3 | 500 | 10 | 0 | $80 |
| 6 | 2,000 | 50 | 5 (25 users) | $775 |
| 12 | 10,000 | 200 | 20 (100 users) | $3,100 |
| 18 | 25,000 | 500 | 50 (250 users) | $7,750 |
| 24 | 50,000 | 1,000 | 100 (500 users) | $15,500 |

## Revenue Streams

```
1. Subscriptions (primary)      — recurring monthly
2. Usage-based (AI tokens)      — pay per heavy usage beyond tier limits
3. Marketplace (rule packs)     — community creates and sells code review rules
4. Enterprise contracts         — annual, custom pricing
5. GitHub Sponsors              — for the open-source CLI
```

---

# 13. RISK REGISTER

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| OpenAI/Anthropic API cost too high | Medium | High | Ollama local-first, cache responses in Redis, batch embeddings |
| Competitor launches similar tool | High | Medium | Ship fast, build community, niche down (specific language) |
| VS Code marketplace rejection | Low | High | Follow guidelines strictly, no telemetry without opt-in |
| Low adoption | Medium | High | Open-source CLI first (build trust), write blog posts, Product Hunt |
| LLM hallucinations in code review | High | Medium | Guardrails (validate issues against AST), confidence scores, user feedback loop |
| Scope creep (too many features) | High | Medium | Strict phase gates — ship each phase before starting next |
| Burnout (side project fatigue) | Medium | High | 2 hours/day max, weekends only for larger features, ship MVP fast |

---

# 14. RESUME IMPACT ASSESSMENT

## See separate section below — "What Are My Chances?"

---

*Last Updated: April 2026*
*Project: CodeLens AI — Code Intelligence Platform*
*Author: Jayanti Vishnoi*
