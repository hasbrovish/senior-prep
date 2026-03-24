import { useState, useEffect, useCallback } from "react";

const INITIAL_STATE = {
  dailyLogs: [],
  concepts: {
    os: [
      { name: "Process vs Thread", done: false, confident: false },
      { name: "Deadlock — 4 conditions, detection, prevention", done: false, confident: false },
      { name: "Race condition — examples and fixes", done: false, confident: false },
      { name: "Mutex vs Semaphore vs Monitor", done: false, confident: false },
      { name: "Virtual memory, Page tables, TLB", done: false, confident: false },
      { name: "Blocking vs Non-blocking I/O, epoll", done: false, confident: false },
      { name: "Producer-Consumer problem", done: false, confident: false },
      { name: "Context switching cost", done: false, confident: false },
    ],
    networking: [
      { name: "TCP vs UDP — handshake, reliability", done: false, confident: false },
      { name: "HTTP/1.1 vs HTTP/2 vs HTTP/3", done: false, confident: false },
      { name: "TLS/HTTPS handshake", done: false, confident: false },
      { name: "DNS resolution flow", done: false, confident: false },
      { name: "WebSocket vs SSE vs Long Polling", done: false, confident: false },
      { name: "REST vs gRPC vs GraphQL", done: false, confident: false },
      { name: "L4 vs L7 Load Balancers", done: false, confident: false },
      { name: "CDN — how it works, anycast", done: false, confident: false },
    ],
    db: [
      { name: "B-tree internals — pages, splitting", done: false, confident: false },
      { name: "LSM tree — memtable, WAL, SSTables, compaction", done: false, confident: false },
      { name: "SQL vs NoSQL — decision framework", done: false, confident: false },
      { name: "ACID properties", done: false, confident: false },
      { name: "Isolation levels (Read Committed → Serializable)", done: false, confident: false },
      { name: "MVCC — how PostgreSQL handles it", done: false, confident: false },
      { name: "Indexing — composite, covering, hash", done: false, confident: false },
      { name: "N+1 query problem", done: false, confident: false },
      { name: "Window functions (ROW_NUMBER, RANK, LAG, LEAD)", done: false, confident: false },
      { name: "Sharding strategies", done: false, confident: false },
      { name: "DB Design 5-step framework", done: false, confident: false },
    ],
    distributed: [
      { name: "CAP Theorem", done: false, confident: false },
      { name: "Eventual vs Strong vs Causal Consistency", done: false, confident: false },
      { name: "Consistent Hashing — virtual nodes", done: false, confident: false },
      { name: "Replication: Leader, Multi-leader, Leaderless", done: false, confident: false },
      { name: "Quorum: W + R > N", done: false, confident: false },
      { name: "Bloom Filters", done: false, confident: false },
      { name: "Leader Election (Raft high level)", done: false, confident: false },
      { name: "SAGA pattern", done: false, confident: false },
      { name: "CQRS pattern", done: false, confident: false },
      { name: "Rate Limiting — Token Bucket, Sliding Window", done: false, confident: false },
      { name: "Circuit Breaker pattern", done: false, confident: false },
    ],
    jvm: [
      { name: "JVM Architecture — class loading, runtime areas", done: false, confident: false },
      { name: "Heap: Young Gen, Old Gen, Metaspace", done: false, confident: false },
      { name: "String Pool and intern()", done: false, confident: false },
      { name: "synchronized vs volatile vs Lock", done: false, confident: false },
      { name: "Double-checked locking Singleton", done: false, confident: false },
      { name: "ThreadPool / ExecutorService", done: false, confident: false },
      { name: "CompletableFuture", done: false, confident: false },
      { name: "Virtual Threads (Java 21)", done: false, confident: false },
      { name: "G1GC internals", done: false, confident: false },
      { name: "ZGC — sub-ms pauses", done: false, confident: false },
      { name: "GC tuning parameters", done: false, confident: false },
      { name: "Thread dump analysis (jstack)", done: false, confident: false },
      { name: "Heap dump analysis (VisualVM/MAT)", done: false, confident: false },
      { name: "p50, p95, p99 latency metrics", done: false, confident: false },
    ],
    spring: [
      { name: "Bean lifecycle and scopes", done: false, confident: false },
      { name: "@Bean, @Qualifier, @Primary", done: false, confident: false },
      { name: "@Transactional — propagation, isolation", done: false, confident: false },
      { name: "@ControllerAdvice exception handling", done: false, confident: false },
      { name: "Actuator + Micrometer for monitoring", done: false, confident: false },
    ],
    solid: [
      { name: "Single Responsibility Principle", done: false, confident: false },
      { name: "Open/Closed Principle", done: false, confident: false },
      { name: "Liskov Substitution Principle", done: false, confident: false },
      { name: "Interface Segregation Principle", done: false, confident: false },
      { name: "Dependency Inversion Principle", done: false, confident: false },
    ],
    patterns: [
      { name: "Singleton (all 5 variants)", done: false, confident: false },
      { name: "Factory & Abstract Factory", done: false, confident: false },
      { name: "Builder", done: false, confident: false },
      { name: "Strategy", done: false, confident: false },
      { name: "Observer", done: false, confident: false },
      { name: "Decorator", done: false, confident: false },
      { name: "State", done: false, confident: false },
      { name: "Template Method", done: false, confident: false },
      { name: "Chain of Responsibility", done: false, confident: false },
    ],
  },
  dsaProblems: [
    { name: "Container With Most Water", pattern: "Two Pointers", difficulty: "M", company: "Oracle", status: "todo" },
    { name: "Trapping Rain Water", pattern: "Two Pointers", difficulty: "H", company: "Amazon", status: "todo" },
    { name: "3Sum", pattern: "Two Pointers", difficulty: "M", company: "Common", status: "todo" },
    { name: "Longest Substring No Repeat", pattern: "Sliding Window", difficulty: "M", company: "Common", status: "todo" },
    { name: "Min Window Substring", pattern: "Sliding Window", difficulty: "H", company: "Common", status: "todo" },
    { name: "Eval Reverse Polish Notation", pattern: "Stack", difficulty: "M", company: "Amazon", status: "todo" },
    { name: "Daily Temperatures", pattern: "Monotonic Stack", difficulty: "M", company: "Common", status: "todo" },
    { name: "LRU Cache", pattern: "HashMap+DLL", difficulty: "M", company: "Apple", status: "todo" },
    { name: "Merge K Sorted Lists", pattern: "Heap+LL", difficulty: "H", company: "Common", status: "todo" },
    { name: "Search Rotated Array", pattern: "Binary Search", difficulty: "M", company: "Common", status: "todo" },
    { name: "Koko Eating Bananas", pattern: "BS on Answer", difficulty: "M", company: "Oracle", status: "todo" },
    { name: "First Missing Positive", pattern: "Array", difficulty: "H", company: "Amazon", status: "todo" },
    { name: "Rotten Oranges", pattern: "BFS", difficulty: "M", company: "DoorDash", status: "todo" },
    { name: "File System Shortest Path", pattern: "BFS+HashMap", difficulty: "M", company: "Amazon", status: "todo" },
    { name: "Binary Tree Max Path Sum", pattern: "Tree DFS", difficulty: "H", company: "DoorDash", status: "todo" },
    { name: "Diameter of Binary Tree", pattern: "Tree DFS", difficulty: "E", company: "Common", status: "todo" },
    { name: "Lowest Common Ancestor", pattern: "Tree DFS", difficulty: "M", company: "Common", status: "todo" },
    { name: "Task Scheduler", pattern: "Greedy+Heap", difficulty: "M", company: "Oracle", status: "todo" },
    { name: "Longest Common Prefix", pattern: "String", difficulty: "E", company: "Apple", status: "todo" },
    { name: "Group Anagrams", pattern: "HashMap", difficulty: "M", company: "Common", status: "todo" },
    { name: "Coin Change", pattern: "DP", difficulty: "M", company: "Common", status: "todo" },
    { name: "Edit Distance", pattern: "DP", difficulty: "M", company: "Common", status: "todo" },
  ],
  lldProblems: [
    { name: "Parking Lot System", patterns: "Strategy, Factory, State", status: "todo" },
    { name: "Elevator System", patterns: "State, Strategy, Observer", status: "todo" },
    { name: "Movie Ticket Booking", patterns: "Observer, State, Concurrency", status: "todo" },
    { name: "Vending Machine", patterns: "State, Strategy", status: "todo" },
    { name: "LRU Cache (Thread-safe)", patterns: "HashMap+DLL, Lock", status: "todo" },
    { name: "Splitwise / Expense Sharing", patterns: "Strategy, Observer, Graph", status: "todo" },
    { name: "Rate Limiter", patterns: "Strategy, Thread safety", status: "todo" },
    { name: "In-Memory Key-Value Store", patterns: "HashMap, TTL, Thread safety", status: "todo" },
    { name: "In-Memory File System", patterns: "Composite, Tree", status: "todo" },
    { name: "Logging Framework", patterns: "Singleton, Observer, Strategy", status: "todo" },
    { name: "Pub-Sub Messaging System", patterns: "Observer, Queue, Thread safety", status: "todo" },
    { name: "Chess Game", patterns: "State, Strategy, Factory", status: "todo" },
  ],
  systemDesigns: [
    { name: "URL Shortener", company: "Apple", status: "todo", rating: 0 },
    { name: "Distributed Cache", company: "Oracle", status: "todo", rating: 0 },
    { name: "Key-Value Store", company: "Oracle", status: "todo", rating: 0 },
    { name: "Apple Music", company: "Apple", status: "todo", rating: 0 },
    { name: "Order Management System", company: "Apple", status: "todo", rating: 0 },
    { name: "Multi-Broker Portfolio", company: "Amazon", status: "todo", rating: 0 },
    { name: "Monitoring & Alerting", company: "DoorDash", status: "todo", rating: 0 },
    { name: "Rate Limiter", company: "Common", status: "todo", rating: 0 },
    { name: "Notification System", company: "Common", status: "todo", rating: 0 },
    { name: "Chat / Messaging", company: "Common", status: "todo", rating: 0 },
    { name: "News Feed", company: "Common", status: "todo", rating: 0 },
    { name: "Payment System", company: "Common", status: "todo", rating: 0 },
    { name: "Video Streaming", company: "Common", status: "todo", rating: 0 },
    { name: "Ride Sharing (Uber)", company: "Common", status: "todo", rating: 0 },
  ],
  weeklyNotes: [],
  streak: 0,
  bestStreak: 0,
};

const CATEGORY_LABELS = {
  os: "Operating Systems",
  networking: "Networking",
  db: "Databases",
  distributed: "Distributed Systems",
  jvm: "JVM & Java Internals",
  spring: "Spring Boot",
  solid: "SOLID Principles",
  patterns: "Design Patterns",
};

const WEEK_PLAN = [
  { week: 1, month: 1, title: "Operating Systems", focus: "Processes, Threads, Deadlocks, Memory, I/O" },
  { week: 2, month: 1, title: "Computer Networking", focus: "TCP/UDP, HTTP, TLS, WebSocket, gRPC, LB" },
  { week: 3, month: 1, title: "Database Internals", focus: "B-tree, LSM, Indexing, MVCC, Advanced SQL" },
  { week: 4, month: 1, title: "DSA Patterns Start", focus: "Two Pointers, Sliding Window, Binary Search, Stack" },
  { week: 5, month: 2, title: "JVM Architecture", focus: "Class loading, Heap/Stack, Memory model, Leaks" },
  { week: 6, month: 2, title: "Concurrency", focus: "synchronized, Locks, ThreadPool, CompletableFuture" },
  { week: 7, month: 2, title: "GC + Performance", focus: "G1GC, ZGC, Profiling, Metrics, Optimization" },
  { week: 8, month: 2, title: "System Design Blocks", focus: "Caching, CDN, Load Balancing, Message Queues" },
  { week: 9, month: 3, title: "Clean Code + SOLID", focus: "Naming, Functions, SOLID, Design Patterns" },
  { week: 10, month: 3, title: "LLD / Machine Coding", focus: "Parking Lot, Elevator, LRU Cache, Vending Machine" },
  { week: 11, month: 3, title: "Distributed Systems", focus: "Replication, Consistency, CAP, Quorum, Bloom Filters" },
  { week: 12, month: 3, title: "System Design Framework", focus: "7-step framework, Estimation, API design" },
  { week: 13, month: 4, title: "Interview Designs 1", focus: "Apple Music, Distributed Cache, KV Store" },
  { week: 14, month: 4, title: "Interview Designs 2", focus: "Order Mgmt, Portfolio Platform, Monitoring" },
  { week: 15, month: 4, title: "Go Language", focus: "Goroutines, Channels, net/http, Context" },
  { week: 16, month: 4, title: "Python + AI Tools", focus: "FastAPI, LangChain basics, LLM APIs" },
  { week: 17, month: 5, title: "DB + Kafka Deep Dive", focus: "LSM internals, Kafka partitions, Redis" },
  { week: 18, month: 5, title: "AI-Augmented Eng", focus: "Claude Code, Cursor, Copilot workflows" },
  { week: 19, month: 5, title: "Communication", focus: "Requirement gathering, Tradeoffs, STAR stories" },
  { week: 20, month: 5, title: "Profile Building", focus: "GitHub repos, LinkedIn, Blog, Networking" },
  { week: 21, month: 6, title: "Integration Practice", focus: "Mix DSA + LLD + System Design + Behavioral" },
  { week: 22, month: 6, title: "Mock Interviews", focus: "Pramp, Interviewing.io, Exponent" },
  { week: 23, month: 6, title: "Mocks + Weak Areas", focus: "Target weak spots from mocks" },
  { week: 24, month: 6, title: "Final Polish", focus: "Light review, STAR stories, confidence" },
];

const DB_DESIGN_REF = {
  steps: [
    { num: 1, title: "List the Nouns", desc: "Read requirements → underline every noun → those are your tables" },
    { num: 2, title: "Define Columns", desc: "For each noun ask: \"What do I need to know about this thing?\"" },
    { num: 3, title: "Define Relationships", desc: "Ask: \"Can ONE of X have MANY of Y?\" → FK goes on the MANY side" },
    { num: 4, title: "Think About Queries", desc: "What queries run most? → Add indexes. Read-heavy? → Consider denormalize" },
    { num: 5, title: "Think About Edge Cases", desc: "Concurrent access? Deletions? Data that changes after reference?" },
  ],
  sqlVsNosql: {
    sql: ["Relational data (lots of JOINs)", "ACID needed (money, orders)", "Stable schema", "Complex queries"],
    nosql: ["Document-shaped data", "Massive write throughput", "Varying schema per record", "Key-based access only"],
  },
};

export default function PrepTracker() {
  const [state, setState] = useState(null);
  const [tab, setTab] = useState("dashboard");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const result = await window.storage.get("prep-tracker-state");
        if (result && result.value) {
          const parsed = JSON.parse(result.value);
          const merged = { ...INITIAL_STATE, ...parsed };
          if (!merged.concepts.patterns) merged.concepts = INITIAL_STATE.concepts;
          setState(merged);
        } else {
          setState(INITIAL_STATE);
        }
      } catch {
        setState(INITIAL_STATE);
      }
      setLoading(false);
    };
    load();
  }, []);

  const save = useCallback(async (newState) => {
    setState(newState);
    try {
      await window.storage.set("prep-tracker-state", JSON.stringify(newState));
    } catch (e) {
      console.error("Save failed", e);
    }
  }, []);

  if (loading || !state) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", background: "#0a0e17", color: "#e2e8f0", fontFamily: "'JetBrains Mono', 'Fira Code', monospace" }}>
        Loading...
      </div>
    );
  }

  const totalConcepts = Object.values(state.concepts).flat().length;
  const doneConcepts = Object.values(state.concepts).flat().filter(c => c.done).length;
  const confidentConcepts = Object.values(state.concepts).flat().filter(c => c.confident).length;
  const dsaDone = state.dsaProblems.filter(p => p.status === "done").length;
  const lldDone = state.lldProblems.filter(p => p.status === "done").length;
  const sdDone = state.systemDesigns.filter(p => p.status === "done").length;
  const totalDays = state.dailyLogs.length;
  const totalHours = state.dailyLogs.reduce((s, l) => s + (l.hours || 0), 0);

  const today = new Date().toISOString().split("T")[0];
  const loggedToday = state.dailyLogs.some(l => l.date === today);

  const tabs = [
    { id: "dashboard", label: "Dashboard", icon: "◉" },
    { id: "daily", label: "Daily Log", icon: "✎" },
    { id: "concepts", label: "Concepts", icon: "◆" },
    { id: "dsa", label: "DSA", icon: "⟐" },
    { id: "lld", label: "LLD", icon: "⬡" },
    { id: "sysdesign", label: "Sys Design", icon: "⊞" },
    { id: "dbref", label: "DB Design", icon: "⊟" },
    { id: "roadmap", label: "Roadmap", icon: "▸" },
    { id: "notes", label: "Notes", icon: "≡" },
  ];

  return (
    <div style={{ minHeight: "100vh", background: "#0a0e17", color: "#c9d1d9", fontFamily: "'JetBrains Mono', 'Fira Code', 'SF Mono', monospace", fontSize: 13 }}>
      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0d1117 0%, #161b22 100%)", borderBottom: "1px solid #21262d", padding: "16px 24px", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
        <div>
          <div style={{ fontSize: 18, fontWeight: 700, color: "#58a6ff", letterSpacing: 1 }}>⟨/⟩ BACKEND MASTERY</div>
          <div style={{ fontSize: 11, color: "#484f58", marginTop: 2 }}>6-Month Prep Tracker</div>
        </div>
        <div style={{ display: "flex", gap: 20, alignItems: "center", flexWrap: "wrap" }}>
          <Stat label="Days Logged" value={totalDays} color="#58a6ff" />
          <Stat label="Hours" value={totalHours.toFixed(1)} color="#3fb950" />
          <Stat label="Streak" value={state.streak} color="#d29922" />
          <Stat label="Concepts" value={`${doneConcepts}/${totalConcepts}`} color="#bc8cff" />
          {!loggedToday && <div style={{ background: "#da3633", color: "#fff", padding: "4px 12px", borderRadius: 4, fontSize: 11, fontWeight: 600, animation: "pulse 2s infinite" }}>LOG TODAY</div>}
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 0, borderBottom: "1px solid #21262d", overflowX: "auto", background: "#0d1117" }}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{
            background: tab === t.id ? "#161b22" : "transparent",
            color: tab === t.id ? "#58a6ff" : "#484f58",
            border: "none",
            borderBottom: tab === t.id ? "2px solid #58a6ff" : "2px solid transparent",
            padding: "10px 16px",
            cursor: "pointer",
            fontFamily: "inherit",
            fontSize: 12,
            fontWeight: tab === t.id ? 600 : 400,
            whiteSpace: "nowrap",
            transition: "all 0.15s",
          }}>
            {t.icon} {t.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ padding: "20px 24px", maxWidth: 1100, margin: "0 auto" }}>
        {tab === "dashboard" && <Dashboard state={state} dsaDone={dsaDone} lldDone={lldDone} sdDone={sdDone} doneConcepts={doneConcepts} confidentConcepts={confidentConcepts} totalConcepts={totalConcepts} totalDays={totalDays} totalHours={totalHours} />}
        {tab === "daily" && <DailyLog state={state} save={save} today={today} />}
        {tab === "concepts" && <Concepts state={state} save={save} />}
        {tab === "dsa" && <DSATracker state={state} save={save} />}
        {tab === "lld" && <LLDTracker state={state} save={save} />}
        {tab === "sysdesign" && <SysDesignTracker state={state} save={save} />}
        {tab === "dbref" && <DBDesignRef />}
        {tab === "roadmap" && <Roadmap />}
        {tab === "notes" && <Notes state={state} save={save} />}
      </div>

      <style>{`
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
        input, textarea, select { font-family: inherit; font-size: 13px; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0d1117; }
        ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
      `}</style>
    </div>
  );
}

function Stat({ label, value, color }) {
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ fontSize: 18, fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: 10, color: "#484f58", textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
    </div>
  );
}

function ProgressBar({ value, max, color = "#58a6ff", height = 6 }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div style={{ background: "#21262d", borderRadius: height / 2, height, width: "100%", overflow: "hidden" }}>
      <div style={{ background: color, height: "100%", width: `${pct}%`, borderRadius: height / 2, transition: "width 0.4s ease" }} />
    </div>
  );
}

function Card({ children, title, style = {} }) {
  return (
    <div style={{ background: "#0d1117", border: "1px solid #21262d", borderRadius: 8, padding: 16, marginBottom: 16, ...style }}>
      {title && <div style={{ fontSize: 13, fontWeight: 600, color: "#e6edf3", marginBottom: 12, borderBottom: "1px solid #21262d", paddingBottom: 8 }}>{title}</div>}
      {children}
    </div>
  );
}

function Dashboard({ state, dsaDone, lldDone, sdDone, doneConcepts, confidentConcepts, totalConcepts, totalDays, totalHours }) {
  const weekNum = Math.min(24, Math.max(1, Math.ceil(totalDays / 7) || 1));
  const currentWeek = WEEK_PLAN[Math.min(weekNum - 1, 23)];

  return (
    <div>
      <Card title={`◉ CURRENT FOCUS — Week ${currentWeek.week}: ${currentWeek.title}`}>
        <div style={{ color: "#8b949e", marginBottom: 8 }}>{currentWeek.focus}</div>
        <ProgressBar value={weekNum} max={24} color="#58a6ff" height={8} />
        <div style={{ fontSize: 11, color: "#484f58", marginTop: 6 }}>Week {weekNum} of 24 · Month {currentWeek.month} of 6</div>
      </Card>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 12 }}>
        <Card>
          <div style={{ color: "#484f58", fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }}>DSA Problems</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: "#3fb950", margin: "4px 0" }}>{dsaDone}<span style={{ fontSize: 14, color: "#484f58" }}>/{state.dsaProblems.length}</span></div>
          <ProgressBar value={dsaDone} max={state.dsaProblems.length} color="#3fb950" />
        </Card>
        <Card>
          <div style={{ color: "#484f58", fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }}>LLD Problems</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: "#d29922", margin: "4px 0" }}>{lldDone}<span style={{ fontSize: 14, color: "#484f58" }}>/{state.lldProblems.length}</span></div>
          <ProgressBar value={lldDone} max={state.lldProblems.length} color="#d29922" />
        </Card>
        <Card>
          <div style={{ color: "#484f58", fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }}>System Designs</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: "#bc8cff", margin: "4px 0" }}>{sdDone}<span style={{ fontSize: 14, color: "#484f58" }}>/{state.systemDesigns.length}</span></div>
          <ProgressBar value={sdDone} max={state.systemDesigns.length} color="#bc8cff" />
        </Card>
        <Card>
          <div style={{ color: "#484f58", fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }}>Concepts Confident</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: "#f778ba", margin: "4px 0" }}>{confidentConcepts}<span style={{ fontSize: 14, color: "#484f58" }}>/{totalConcepts}</span></div>
          <ProgressBar value={confidentConcepts} max={totalConcepts} color="#f778ba" />
        </Card>
      </div>

      <Card title="⟐ CATEGORY BREAKDOWN">
        {Object.entries(state.concepts).map(([key, items]) => {
          const done = items.filter(i => i.done).length;
          return (
            <div key={key} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
              <div style={{ width: 160, fontSize: 12, color: "#8b949e" }}>{CATEGORY_LABELS[key]}</div>
              <div style={{ flex: 1 }}><ProgressBar value={done} max={items.length} color="#58a6ff" /></div>
              <div style={{ fontSize: 11, color: "#484f58", width: 40, textAlign: "right" }}>{done}/{items.length}</div>
            </div>
          );
        })}
      </Card>

      {state.dailyLogs.length > 0 && (
        <Card title="≡ RECENT LOGS">
          {state.dailyLogs.slice(-5).reverse().map((log, i) => (
            <div key={i} style={{ display: "flex", gap: 12, padding: "6px 0", borderBottom: "1px solid #161b22", fontSize: 12 }}>
              <span style={{ color: "#58a6ff", width: 80 }}>{log.date}</span>
              <span style={{ color: "#3fb950", width: 30 }}>{log.hours}h</span>
              <span style={{ color: "#8b949e", flex: 1 }}>{log.takeaway || "—"}</span>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
}

function DailyLog({ state, save, today }) {
  const [form, setForm] = useState({ date: today, dsaProblems: "", mainTopic: "", hours: "", takeaway: "" });
  const existing = state.dailyLogs.find(l => l.date === today);

  const submit = () => {
    if (!form.hours) return;
    const logs = [...state.dailyLogs.filter(l => l.date !== form.date), { ...form, hours: parseFloat(form.hours) || 0 }].sort((a, b) => a.date.localeCompare(b.date));
    let streak = 0;
    const d = new Date(today);
    for (let i = 0; i < 365; i++) {
      const ds = d.toISOString().split("T")[0];
      if (logs.some(l => l.date === ds)) { streak++; d.setDate(d.getDate() - 1); } else break;
    }
    save({ ...state, dailyLogs: logs, streak, bestStreak: Math.max(state.bestStreak, streak) });
    setForm({ date: today, dsaProblems: "", mainTopic: "", hours: "", takeaway: "" });
  };

  const inputStyle = { background: "#0d1117", border: "1px solid #30363d", borderRadius: 6, padding: "8px 12px", color: "#c9d1d9", width: "100%", outline: "none", boxSizing: "border-box" };

  return (
    <div>
      <Card title={`✎ LOG TODAY — ${today}`}>
        {existing && <div style={{ background: "#0b3d1c", border: "1px solid #238636", borderRadius: 6, padding: 10, marginBottom: 12, fontSize: 12, color: "#3fb950" }}>✓ Already logged today: {existing.hours}h — {existing.takeaway}</div>}
        <div style={{ display: "grid", gap: 12 }}>
          <div>
            <label style={{ fontSize: 11, color: "#484f58", display: "block", marginBottom: 4 }}>DSA Problem(s) Solved</label>
            <input style={inputStyle} value={form.dsaProblems} onChange={e => setForm({ ...form, dsaProblems: e.target.value })} placeholder="e.g. Two Sum, Container With Most Water" />
          </div>
          <div>
            <label style={{ fontSize: 11, color: "#484f58", display: "block", marginBottom: 4 }}>Main Topic Studied</label>
            <input style={inputStyle} value={form.mainTopic} onChange={e => setForm({ ...form, mainTopic: e.target.value })} placeholder="e.g. B-tree internals, G1GC" />
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: 12 }}>
            <div>
              <label style={{ fontSize: 11, color: "#484f58", display: "block", marginBottom: 4 }}>Total Hours</label>
              <input style={inputStyle} type="number" step="0.5" min="0" max="12" value={form.hours} onChange={e => setForm({ ...form, hours: e.target.value })} placeholder="2.5" />
            </div>
            <div>
              <label style={{ fontSize: 11, color: "#484f58", display: "block", marginBottom: 4 }}>Key Takeaway (1 sentence)</label>
              <input style={inputStyle} value={form.takeaway} onChange={e => setForm({ ...form, takeaway: e.target.value })} placeholder="What's the ONE thing you learned today?" />
            </div>
          </div>
          <button onClick={submit} style={{ background: "#238636", color: "#fff", border: "none", borderRadius: 6, padding: "10px 20px", cursor: "pointer", fontFamily: "inherit", fontWeight: 600, fontSize: 13 }}>
            {existing ? "Update Today's Log" : "Log Today"}
          </button>
        </div>
      </Card>

      <Card title="≡ ALL LOGS">
        <div style={{ maxHeight: 400, overflow: "auto" }}>
          {state.dailyLogs.slice().reverse().map((log, i) => (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "80px 40px 1fr 1fr", gap: 8, padding: "8px 0", borderBottom: "1px solid #161b22", fontSize: 12, alignItems: "start" }}>
              <span style={{ color: "#58a6ff" }}>{log.date}</span>
              <span style={{ color: "#3fb950", fontWeight: 600 }}>{log.hours}h</span>
              <span style={{ color: "#c9d1d9" }}>{log.mainTopic || log.dsaProblems || "—"}</span>
              <span style={{ color: "#8b949e", fontStyle: "italic" }}>{log.takeaway || ""}</span>
            </div>
          ))}
          {state.dailyLogs.length === 0 && <div style={{ color: "#484f58", textAlign: "center", padding: 20 }}>No logs yet. Start today.</div>}
        </div>
      </Card>
    </div>
  );
}

function Concepts({ state, save }) {
  const toggle = (cat, idx, field) => {
    const newConcepts = { ...state.concepts };
    newConcepts[cat] = [...newConcepts[cat]];
    newConcepts[cat][idx] = { ...newConcepts[cat][idx], [field]: !newConcepts[cat][idx][field] };
    if (field === "confident" && !newConcepts[cat][idx].done && newConcepts[cat][idx].confident) {
      newConcepts[cat][idx].done = true;
    }
    save({ ...state, concepts: newConcepts });
  };

  return (
    <div>
      {Object.entries(state.concepts).map(([cat, items]) => {
        const done = items.filter(i => i.done).length;
        const conf = items.filter(i => i.confident).length;
        return (
          <Card key={cat} title={`${CATEGORY_LABELS[cat]} — ${done}/${items.length} studied · ${conf} confident`}>
            {items.map((item, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "6px 0", borderBottom: "1px solid #161b22" }}>
                <button onClick={() => toggle(cat, i, "done")} style={{ background: item.done ? "#238636" : "#21262d", border: "1px solid " + (item.done ? "#238636" : "#30363d"), borderRadius: 4, width: 22, height: 22, cursor: "pointer", color: "#fff", fontSize: 12, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                  {item.done ? "✓" : ""}
                </button>
                <span style={{ flex: 1, color: item.done ? "#8b949e" : "#c9d1d9", textDecoration: item.done ? "none" : "none", fontSize: 12 }}>{item.name}</span>
                <button onClick={() => toggle(cat, i, "confident")} style={{ background: item.confident ? "#58a6ff" : "transparent", border: "1px solid " + (item.confident ? "#58a6ff" : "#30363d"), borderRadius: 4, padding: "2px 8px", cursor: "pointer", color: item.confident ? "#fff" : "#484f58", fontSize: 10, fontFamily: "inherit" }}>
                  {item.confident ? "CONFIDENT" : "not yet"}
                </button>
              </div>
            ))}
          </Card>
        );
      })}
    </div>
  );
}

function StatusButton({ status, onChange }) {
  const colors = { todo: { bg: "#21262d", border: "#30363d", text: "#484f58", label: "TODO" }, doing: { bg: "#2a1f00", border: "#d29922", text: "#d29922", label: "DOING" }, done: { bg: "#0b3d1c", border: "#238636", text: "#3fb950", label: "DONE" }, revisit: { bg: "#3d1a1a", border: "#da3633", text: "#f85149", label: "REVISIT" } };
  const order = ["todo", "doing", "done", "revisit"];
  const c = colors[status] || colors.todo;
  const next = () => { const idx = order.indexOf(status); onChange(order[(idx + 1) % order.length]); };
  return <button onClick={next} style={{ background: c.bg, border: `1px solid ${c.border}`, color: c.text, borderRadius: 4, padding: "2px 10px", cursor: "pointer", fontSize: 10, fontFamily: "inherit", fontWeight: 600, minWidth: 60 }}>{c.label}</button>;
}

function DSATracker({ state, save }) {
  const updateStatus = (idx, status) => {
    const problems = [...state.dsaProblems];
    problems[idx] = { ...problems[idx], status };
    save({ ...state, dsaProblems: problems });
  };

  const patterns = [...new Set(state.dsaProblems.map(p => p.pattern))];
  const diffColors = { E: "#3fb950", M: "#d29922", H: "#f85149" };

  return (
    <div>
      <Card>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
          {patterns.map(p => {
            const count = state.dsaProblems.filter(pr => pr.pattern === p && pr.status === "done").length;
            const total = state.dsaProblems.filter(pr => pr.pattern === p).length;
            return <span key={p} style={{ background: "#161b22", border: "1px solid #21262d", borderRadius: 4, padding: "4px 10px", fontSize: 11, color: count === total ? "#3fb950" : "#8b949e" }}>{p}: {count}/{total}</span>;
          })}
        </div>
      </Card>
      <Card title="⟐ ALL PROBLEMS">
        <div style={{ display: "grid", gridTemplateColumns: "1fr 120px 30px 70px 70px", gap: "0", fontSize: 12 }}>
          <div style={{ color: "#484f58", padding: "4px 0", borderBottom: "1px solid #21262d", fontWeight: 600 }}>Problem</div>
          <div style={{ color: "#484f58", padding: "4px 0", borderBottom: "1px solid #21262d", fontWeight: 600 }}>Pattern</div>
          <div style={{ color: "#484f58", padding: "4px 0", borderBottom: "1px solid #21262d", fontWeight: 600 }}>D</div>
          <div style={{ color: "#484f58", padding: "4px 0", borderBottom: "1px solid #21262d", fontWeight: 600 }}>Company</div>
          <div style={{ color: "#484f58", padding: "4px 0", borderBottom: "1px solid #21262d", fontWeight: 600 }}>Status</div>
          {state.dsaProblems.map((p, i) => (
            <React.Fragment key={i}>
              <div style={{ padding: "6px 0", borderBottom: "1px solid #161b22", color: p.status === "done" ? "#484f58" : "#c9d1d9" }}>{p.name}</div>
              <div style={{ padding: "6px 0", borderBottom: "1px solid #161b22", color: "#8b949e" }}>{p.pattern}</div>
              <div style={{ padding: "6px 0", borderBottom: "1px solid #161b22", color: diffColors[p.difficulty], fontWeight: 700 }}>{p.difficulty}</div>
              <div style={{ padding: "6px 0", borderBottom: "1px solid #161b22", color: "#58a6ff" }}>{p.company}</div>
              <div style={{ padding: "4px 0", borderBottom: "1px solid #161b22" }}><StatusButton status={p.status} onChange={s => updateStatus(i, s)} /></div>
            </React.Fragment>
          ))}
        </div>
      </Card>
    </div>
  );
}

function LLDTracker({ state, save }) {
  const updateStatus = (idx, status) => {
    const problems = [...state.lldProblems];
    problems[idx] = { ...problems[idx], status };
    save({ ...state, lldProblems: problems });
  };

  return (
    <Card title="⬡ LOW-LEVEL DESIGN / MACHINE CODING">
      {state.lldProblems.map((p, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 0", borderBottom: "1px solid #161b22" }}>
          <StatusButton status={p.status} onChange={s => updateStatus(i, s)} />
          <div style={{ flex: 1 }}>
            <div style={{ color: p.status === "done" ? "#484f58" : "#c9d1d9", fontSize: 13, fontWeight: 500 }}>{p.name}</div>
            <div style={{ color: "#484f58", fontSize: 11, marginTop: 2 }}>Patterns: {p.patterns}</div>
          </div>
        </div>
      ))}
    </Card>
  );
}

function SysDesignTracker({ state, save }) {
  const updateStatus = (idx, status) => {
    const designs = [...state.systemDesigns];
    designs[idx] = { ...designs[idx], status };
    save({ ...state, systemDesigns: designs });
  };
  const updateRating = (idx, rating) => {
    const designs = [...state.systemDesigns];
    designs[idx] = { ...designs[idx], rating };
    save({ ...state, systemDesigns: designs });
  };

  return (
    <Card title="⊞ SYSTEM DESIGN PRACTICE">
      {state.systemDesigns.map((sd, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 0", borderBottom: "1px solid #161b22" }}>
          <StatusButton status={sd.status} onChange={s => updateStatus(i, s)} />
          <div style={{ flex: 1 }}>
            <span style={{ color: "#c9d1d9", fontWeight: 500 }}>{sd.name}</span>
            <span style={{ color: "#58a6ff", fontSize: 11, marginLeft: 8 }}>({sd.company})</span>
          </div>
          <div style={{ display: "flex", gap: 2 }}>
            {[1, 2, 3, 4, 5].map(n => (
              <button key={n} onClick={() => updateRating(i, n)} style={{ background: "none", border: "none", cursor: "pointer", color: n <= sd.rating ? "#d29922" : "#21262d", fontSize: 16 }}>●</button>
            ))}
          </div>
        </div>
      ))}
    </Card>
  );
}

function DBDesignRef() {
  return (
    <div>
      <Card title="⊟ DB DESIGN — 5-STEP FRAMEWORK (Reference)">
        {DB_DESIGN_REF.steps.map(s => (
          <div key={s.num} style={{ display: "flex", gap: 12, padding: "10px 0", borderBottom: "1px solid #161b22" }}>
            <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#58a6ff", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700, fontSize: 13, flexShrink: 0 }}>{s.num}</div>
            <div>
              <div style={{ color: "#e6edf3", fontWeight: 600, fontSize: 13 }}>{s.title}</div>
              <div style={{ color: "#8b949e", fontSize: 12, marginTop: 2 }}>{s.desc}</div>
            </div>
          </div>
        ))}
      </Card>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <Card title="✓ Choose SQL When">
          {DB_DESIGN_REF.sqlVsNosql.sql.map((item, i) => (
            <div key={i} style={{ padding: "4px 0", color: "#3fb950", fontSize: 12 }}>→ {item}</div>
          ))}
        </Card>
        <Card title="✓ Choose NoSQL When">
          {DB_DESIGN_REF.sqlVsNosql.nosql.map((item, i) => (
            <div key={i} style={{ padding: "4px 0", color: "#d29922", fontSize: 12 }}>→ {item}</div>
          ))}
        </Card>
      </div>

      <Card title="⟐ RELATIONSHIP RULES (Quick Reference)">
        <div style={{ fontSize: 12, lineHeight: 1.8, color: "#8b949e" }}>
          <div><span style={{ color: "#58a6ff", fontWeight: 600 }}>One-to-Many:</span> FK goes on the MANY side. (User → Orders: user_id in Orders table)</div>
          <div><span style={{ color: "#d29922", fontWeight: 600 }}>Many-to-Many:</span> Create junction table with both FKs. (Students ↔ Courses: Enrollments table)</div>
          <div><span style={{ color: "#3fb950", fontWeight: 600 }}>One-to-One:</span> FK on either side, add UNIQUE constraint. (User → Profile: user_id in Profile)</div>
          <div style={{ marginTop: 8, color: "#bc8cff" }}><strong>Key insight:</strong> Always ask "Can ONE of X have MANY of Y?" — the answer tells you where the FK goes.</div>
          <div style={{ marginTop: 4, color: "#f778ba" }}><strong>Edge cases to always check:</strong> What if referenced data changes? (snapshot it) · What if it's deleted? (soft delete) · Concurrent access? (locking strategy)</div>
        </div>
      </Card>
    </div>
  );
}

function Roadmap() {
  const monthColors = ["#58a6ff", "#3fb950", "#d29922", "#bc8cff", "#f778ba", "#f85149"];
  return (
    <Card title="▸ 24-WEEK ROADMAP">
      {WEEK_PLAN.map((w, i) => (
        <div key={i} style={{ display: "flex", gap: 12, padding: "8px 0", borderBottom: "1px solid #161b22", alignItems: "center" }}>
          <div style={{ width: 50, textAlign: "center" }}>
            <div style={{ fontSize: 11, color: monthColors[w.month - 1], fontWeight: 700 }}>M{w.month}</div>
            <div style={{ fontSize: 13, color: "#e6edf3", fontWeight: 600 }}>W{w.week}</div>
          </div>
          <div style={{ width: 3, height: 30, background: monthColors[w.month - 1], borderRadius: 2, flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <div style={{ color: "#e6edf3", fontWeight: 500, fontSize: 13 }}>{w.title}</div>
            <div style={{ color: "#484f58", fontSize: 11 }}>{w.focus}</div>
          </div>
        </div>
      ))}
    </Card>
  );
}

function Notes({ state, save }) {
  const [note, setNote] = useState("");
  const inputStyle = { background: "#0d1117", border: "1px solid #30363d", borderRadius: 6, padding: "10px 12px", color: "#c9d1d9", width: "100%", outline: "none", resize: "vertical", minHeight: 80, boxSizing: "border-box", fontFamily: "inherit" };

  const addNote = () => {
    if (!note.trim()) return;
    const notes = [...(state.weeklyNotes || []), { date: new Date().toISOString().split("T")[0], text: note.trim() }];
    save({ ...state, weeklyNotes: notes });
    setNote("");
  };

  const deleteNote = (idx) => {
    const notes = [...state.weeklyNotes];
    notes.splice(idx, 1);
    save({ ...state, weeklyNotes: notes });
  };

  return (
    <div>
      <Card title="≡ ADD NOTE / REFLECTION">
        <textarea style={inputStyle} value={note} onChange={e => setNote(e.target.value)} placeholder="What did you learn? What are you struggling with? What's the plan for next week?" />
        <button onClick={addNote} style={{ background: "#238636", color: "#fff", border: "none", borderRadius: 6, padding: "8px 16px", cursor: "pointer", fontFamily: "inherit", fontWeight: 600, fontSize: 12, marginTop: 8 }}>Add Note</button>
      </Card>
      <Card title="≡ ALL NOTES">
        {(state.weeklyNotes || []).slice().reverse().map((n, i) => (
          <div key={i} style={{ padding: "10px 0", borderBottom: "1px solid #161b22", display: "flex", gap: 12 }}>
            <div style={{ color: "#58a6ff", fontSize: 11, width: 80, flexShrink: 0 }}>{n.date}</div>
            <div style={{ color: "#c9d1d9", fontSize: 12, flex: 1, whiteSpace: "pre-wrap" }}>{n.text}</div>
            <button onClick={() => deleteNote((state.weeklyNotes || []).length - 1 - i)} style={{ background: "none", border: "none", color: "#484f58", cursor: "pointer", fontSize: 14, flexShrink: 0 }}>×</button>
          </div>
        ))}
        {(!state.weeklyNotes || state.weeklyNotes.length === 0) && <div style={{ color: "#484f58", textAlign: "center", padding: 20 }}>No notes yet.</div>}
      </Card>
    </div>
  );
}
