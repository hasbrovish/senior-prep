import { useState, useEffect, useCallback } from "react";

/* ═══════════════════════════════════════════════════════════════
   CONFIGURABLE 360° INTERVIEW PREP SYSTEM
   - All data from: V4 Tracker, Garima Sheet, Battle Plans, GenAI Guide
   - Every section has ADD CUSTOM capability
   - Persistent storage + Obsidian/GitHub export
   ═══════════════════════════════════════════════════════════════ */

const K = "prep-ultimate-v5";

// ─── DSA: NeetCode 150 + Garima + Company OA extras (200+) ───
const DSA_INIT = [
  // Arrays & Hashing
  ...[["Two Sum","Arrays",1,"E","HashMap",["Google","Amazon","Meta"]],["Contains Duplicate","Arrays",217,"E","HashSet",["Amazon"]],["Valid Anagram","Arrays",242,"E","Count",["Google"]],["Group Anagrams","Arrays",49,"M","HashMap",["Amazon","Meta"]],["Top K Frequent","Arrays",347,"M","Bucket/Heap",["Amazon","Meta"]],["Product Except Self","Arrays",238,"M","Prefix",["Amazon","Apple"]],["Valid Sudoku","Arrays",36,"M","HashSet",["Uber"]],["Longest Consecutive","Arrays",128,"M","HashSet",["Google","Amazon"]],["Encode Decode Strings","Arrays",271,"M","Delimit",["Google"]],["Longest Common Prefix","Arrays",14,"E","String",["Apple"]],["First Missing Positive","Arrays",41,"H","Index Hash",["Amazon"]],["Subarray Sum = K","Arrays",560,"M","Prefix+Map",["Amazon","Google"]],["Majority Element","Arrays",169,"E","Boyer-Moore",["Amazon"]],["Sort Colors","Arrays",75,"M","Dutch Flag",["Amazon"]],["Next Permutation","Arrays",31,"M","Pattern",["Google"]],["Rotate Array","Arrays",189,"M","Reverse",["Amazon"]]],
  // Two Pointers
  ...[["Valid Palindrome","2Ptr",125,"E","Two Ptr",["Meta"]],["Two Sum II Sorted","2Ptr",167,"M","Two Ptr",["Amazon"]],["3Sum","2Ptr",15,"M","Sort+2Ptr",["Amazon","Google","Meta"]],["Container Most Water","2Ptr",11,"M","Two Ptr",["Oracle","Google"]],["Trapping Rain Water","2Ptr",42,"H","Two Ptr",["Amazon","Google","Microsoft"]]],
  // Sliding Window
  ...[["Buy Sell Stock","SlideWin",121,"E","Kadane",["Amazon","Google"]],["Longest No Repeat","SlideWin",3,"M","HashMap",["Amazon","Google","Meta","Microsoft"]],["Longest Repeat Replace","SlideWin",424,"M","Freq Count",["Google"]],["Permutation in String","SlideWin",567,"M","Fixed Win",["Microsoft"]],["Min Window Substring","SlideWin",76,"H","HashMap",["Meta","Google","Uber"]],["Sliding Window Max","SlideWin",239,"H","Mono Deque",["Google","Amazon"]],["Find All Anagrams","SlideWin",438,"M","Fixed Win",["Amazon"]],["Max Consecutive Ones III","SlideWin",1004,"M","Binary Cnt",["Microsoft"]]],
  // Stack
  ...[["Valid Parentheses","Stack",20,"E","Stack",["Amazon"]],["Min Stack","Stack",155,"M","Aux Stack",["Amazon"]],["Eval Reverse Polish","Stack",150,"M","Stack",["Amazon"]],["Generate Parentheses","Stack",22,"M","Backtrack",["Google"]],["Daily Temperatures","Stack",739,"M","Mono Stack",["Meta"]],["Car Fleet","Stack",853,"M","Mono Stack",["Google"]],["Largest Rect Histogram","Stack",84,"H","Mono Stack",["Google","Amazon"]]],
  // Binary Search
  ...[["Binary Search","BinSearch",704,"E","Template",["Common"]],["Search 2D Matrix","BinSearch",74,"M","2D BS",["Amazon"]],["Koko Eating Bananas","BinSearch",875,"M","BS Answer",["Oracle"]],["Find Min Rotated","BinSearch",153,"M","Modified BS",["Meta"]],["Search Rotated Array","BinSearch",33,"M","Modified BS",["Meta","Amazon"]],["Time Based KV Store","BinSearch",981,"M","BS + Map",["Google"]],["Median Two Sorted","BinSearch",4,"H","BS",["Google","Amazon"]],["Find Peak Element","BinSearch",162,"M","BS",["Meta"]],["Capacity Ship Packages","BinSearch",1011,"M","BS Answer",["Amazon"]],["Split Array Largest","BinSearch",410,"H","BS+Greedy",["Google"]]],
  // Linked List
  ...[["Reverse LL","LinkedList",206,"E","Iterate",["Amazon","Google"]],["Merge Two Sorted","LinkedList",21,"E","Dummy",["Amazon"]],["LL Cycle","LinkedList",141,"E","Fast-Slow",["Amazon"]],["Reorder List","LinkedList",143,"M","Multi",["Meta"]],["Remove Nth End","LinkedList",19,"M","Gap Ptr",["Meta"]],["Copy Random Pointer","LinkedList",138,"M","HashMap",["Amazon","Meta"]],["Add Two Numbers","LinkedList",2,"M","Carry",["Amazon"]],["Find Duplicate","LinkedList",287,"M","Floyd",["Amazon"]],["LRU Cache","LinkedList",146,"M","Map+DLL",["Apple","Amazon","Google","Meta"]],["Merge K Sorted","LinkedList",23,"H","Heap",["Amazon","Google"]],["Reverse K-Group","LinkedList",25,"H","Count+Rev",["Amazon"]],["LL Cycle II","LinkedList",142,"M","Math",["Amazon"]],["Reverse LL II","LinkedList",92,"M","Range",["Google"]]],
  // Trees
  ...[["Invert Tree","Trees",226,"E","DFS",["Google"]],["Max Depth","Trees",104,"E","DFS",["Amazon"]],["Diameter","Trees",543,"E","DFS",["Meta"]],["Same Tree","Trees",100,"E","DFS",["Amazon"]],["Subtree of Another","Trees",572,"E","DFS",["Amazon"]],["LCA BST","Trees",235,"M","BST",["Meta"]],["Level Order","Trees",102,"M","BFS",["Amazon","Meta"]],["Validate BST","Trees",98,"M","Inorder",["Amazon"]],["Kth Smallest BST","Trees",230,"M","Inorder",["Amazon"]],["Pre+Inorder Build","Trees",105,"M","Recursion",["Google"]],["Right Side View","Trees",199,"M","BFS",["Meta"]],["Good Nodes","Trees",1448,"M","DFS",["Microsoft"]],["Max Path Sum","Trees",124,"H","DFS",["DoorDash","Meta"]],["Serialize/Deserialize","Trees",297,"H","BFS/DFS",["Amazon","Google"]],["Word Search II","Trees",212,"H","Trie+BT",["Amazon"]],["Binary Tree Zigzag","Trees",103,"M","BFS",["Amazon"]],["Path Sum II","Trees",113,"M","DFS+BT",["Amazon"]],["Flatten to LL","Trees",114,"M","DFS",["Meta"]]],
  // Heap
  ...[["Kth Largest Stream","Heap",703,"E","Min Heap",["Amazon"]],["Last Stone Weight","Heap",1046,"E","Max Heap",["Common"]],["K Closest Points","Heap",973,"M","Max Heap",["Amazon","Meta"]],["Kth Largest Element","Heap",215,"M","QuickSelect",["Meta"]],["Task Scheduler","Heap",621,"M","Greedy+Heap",["Oracle","Meta"]],["Design Twitter","Heap",355,"M","Heap+Map",["Common"]],["Median Data Stream","Heap",295,"H","2 Heaps",["Amazon","Google"]]],
  // Backtracking
  ...[["Subsets","Backtrack",78,"M","BT",["Amazon"]],["Combination Sum","Backtrack",39,"M","BT",["Amazon"]],["Permutations","Backtrack",46,"M","BT",["Meta"]],["Subsets II","Backtrack",90,"M","BT+Skip",["Amazon"]],["Combo Sum II","Backtrack",40,"M","BT+Skip",["Amazon"]],["Word Search","Backtrack",79,"M","DFS+BT",["Amazon"]],["Palindrome Partition","Backtrack",131,"M","BT",["Amazon"]],["Letter Combos Phone","Backtrack",17,"M","BT",["Google","Meta"]],["N-Queens","Backtrack",51,"H","BT",["Google"]]],
  // Tries
  ...[["Implement Trie","Trie",208,"M","Trie",["Amazon"]],["Add Search Word","Trie",211,"M","Trie+DFS",["Meta"]],["Search Suggestions","Trie",1268,"M","Trie",["Amazon"]]],
  // Graphs
  ...[["Num Islands","Graphs",200,"M","BFS/DFS",["Amazon","Google","Meta"]],["Clone Graph","Graphs",133,"M","DFS+Map",["Meta"]],["Max Area Island","Graphs",695,"M","DFS",["DoorDash"]],["Pacific Atlantic","Graphs",417,"M","DFS",["Google"]],["Rotten Oranges","Graphs",994,"M","Multi BFS",["DoorDash","Amazon"]],["Walls and Gates","Graphs",286,"M","Multi BFS",["DoorDash"]],["Course Schedule","Graphs",207,"M","Topo Sort",["Amazon","Google"]],["Course Schedule II","Graphs",210,"M","Topo Sort",["Amazon"]],["Graph Valid Tree","Graphs",261,"M","Union Find",["Google"]],["Redundant Conn","Graphs",684,"M","Union Find",["Google"]],["Word Ladder","Graphs",127,"H","BFS",["Amazon"]],["Alien Dictionary","Graphs",269,"H","Topo Sort",["Meta","Google"]],["Longest Path Matrix","Graphs",329,"H","DFS+Memo",["Google"]],["Num Connected","Graphs",323,"M","Union Find",["Google"]]],
  // 1D DP
  ...[["Climbing Stairs","1D-DP",70,"E","DP",["Amazon"]],["Min Cost Stairs","1D-DP",746,"E","DP",["Amazon"]],["House Robber","1D-DP",198,"M","DP",["Amazon"]],["House Robber II","1D-DP",213,"M","Circular DP",["Amazon"]],["Longest Palindrome Str","1D-DP",5,"M","Expand",["Amazon"]],["Palindromic Substrings","1D-DP",647,"M","Expand",["Meta"]],["Decode Ways","1D-DP",91,"M","DP",["Meta","Amazon"]],["Coin Change","1D-DP",322,"M","DP",["Amazon","Google"]],["Max Product Subarray","1D-DP",152,"M","DP",["Amazon"]],["Word Break","1D-DP",139,"M","DP+Set",["Amazon","Meta"]],["Longest Increasing Sub","1D-DP",300,"M","DP/BS",["Amazon"]],["Partition Equal Subset","1D-DP",416,"M","0/1 Knapsack",["Amazon"]]],
  // 2D DP
  ...[["Unique Paths","2D-DP",62,"M","Grid DP",["Google"]],["Longest Common Subseq","2D-DP",1143,"M","LCS",["Amazon"]],["Buy Sell Cooldown","2D-DP",309,"M","State DP",["Goldman"]],["Coin Change II","2D-DP",518,"M","DP",["Amazon"]],["Target Sum","2D-DP",494,"M","DP",["Meta"]],["Interleaving String","2D-DP",97,"M","2D DP",["Google"]],["Edit Distance","2D-DP",72,"M","DP",["Amazon","Google"]]],
  // Greedy + Intervals + Math + Bit
  ...[["Max Subarray","Greedy",53,"M","Kadane",["Amazon"]],["Jump Game","Greedy",55,"M","Greedy",["Amazon"]],["Jump Game II","Greedy",45,"M","BFS",["Amazon"]],["Gas Station","Greedy",134,"M","Greedy",["Amazon"]],["Partition Labels","Greedy",763,"M","Greedy",["Amazon"]],["Merge Intervals","Intervals",56,"M","Sort",["Google","Amazon","Meta"]],["Insert Interval","Intervals",57,"M","Scan",["Google"]],["Meeting Rooms","Intervals",252,"E","Sort",["Meta"]],["Meeting Rooms II","Intervals",253,"M","Heap",["Google","Amazon"]],["Non-Overlapping","Intervals",435,"M","Greedy",["Amazon"]],["Rotate Image","Math",48,"M","Transpose",["Amazon"]],["Spiral Matrix","Math",54,"M","Bounds",["Amazon"]],["Set Matrix Zeroes","Math",73,"M","In-place",["Amazon"]],["Pow(x,n)","Math",50,"M","Binary Exp",["Meta"]],["Single Number","Bits",136,"E","XOR",["Amazon"]],["Missing Number","Bits",268,"E","XOR",["Amazon"]]],
].map(([n,p,lc,d,pat,co])=>({n,p,lc,d,pat,co,s:"todo",notes:""}));

// ─── HLD: 35 problems (from V4 + Garima + my additions) ───
const HLD_INIT = [
  ["URL Shortener","Encoding, Base62, DB sharding, Analytics",["Apple","Google","Stripe"],"Fundamental"],
  ["Rate Limiter","Token Bucket, Sliding Window, Distributed, Redis",["Stripe","Uber","DoorDash"],"Fundamental"],
  ["Key-Value Store","LSM tree, Compaction, Replication, Partitioning",["Oracle","Amazon"],"Fundamental"],
  ["Distributed Cache (Redis)","Consistent Hashing, Eviction, Cluster, Replication",["Oracle","Amazon"],"Fundamental"],
  ["Pastebin","S3 storage, TTL, Expiry, Content-addressable",["Common"],"Fundamental"],
  ["Notification Service","Push/Email/SMS, Priority routing, Dedup, Templates",["Amazon","Meta"],"Core"],
  ["News Feed / Timeline","Fan-out write/read, Ranking, Cache, Pagination",["Meta","LinkedIn"],"Core"],
  ["Chat / WhatsApp","WebSocket, Delivery receipts, E2E, Cassandra",["Meta","Slack"],"Core"],
  ["Twitter","Timeline, Trending, Cache, Fanout",["Meta","Twitter"],"Core"],
  ["Instagram","Photo upload, CDN, Feed, Stories",["Meta"],"Core"],
  ["Search Autocomplete","Trie, Prefix search, Ranking, Personalization",["Google","Amazon"],"Core"],
  ["Apple Music / Spotify","Streaming, Adaptive bitrate, CDN, Playlists, Recs",["Apple","Spotify"],"Core"],
  ["E-commerce (Amazon)","Inventory, Payments, Cart, Catalog, Search",["Amazon"],"Core"],
  ["Ticket Booking","Seat selection, Concurrency, Locking, Calendar",["Common"],"Core"],
  ["Hotel Booking (Airbnb)","Search, Booking, Calendar, Pricing, Reviews",["Airbnb"],"Core"],
  ["Order Management","State machine, SAGA, Eventual consistency, Payments",["Apple","Amazon","DoorDash"],"Advanced"],
  ["Multi-Broker Portfolio","Multi-tenancy, Aggregation, Real-time, Schema",["Amazon","Goldman"],"Advanced"],
  ["Monitoring & Alerting","Event ingestion, Pipeline, Rules engine, SLA",["DoorDash","Netflix"],"Advanced"],
  ["Video Streaming (Netflix)","CDN, Transcoding, ABR, DRM, Recommendations",["Netflix","Google"],"Advanced"],
  ["Uber / Ride Sharing","Matching, Geospatial, ETA, Surge, Real-time",["Uber","DoorDash"],"Advanced"],
  ["Payment System","Idempotency, Reconciliation, Ledger, Audit trail",["Stripe","Amazon","Goldman"],"Advanced"],
  ["Distributed Task Scheduler","Cron, Priority Queue, Retries, Distributed",["Uber","Netflix"],"Advanced"],
  ["Web Crawler","BFS, URL frontier, Robots.txt, Dedup, Politeness",["Google","Amazon"],"Advanced"],
  ["Dropbox / Google Drive","Chunking, Sync, Dedup, Versioning, Conflict",["Google","Dropbox"],"Advanced"],
  ["Google Docs","CRDT, Operational Transform, Real-time collab",["Google","Microsoft"],"Expert"],
  ["Design Kafka","Log-structured, Partitions, Consumer groups, Exactly-once",["Meta","LinkedIn"],"Expert"],
  ["Design Redis","Data structures, Persistence, Clustering, Pub/Sub",["Meta","Amazon"],"Expert"],
  ["Location Service (Yelp)","Geospatial, QuadTree, Geo-hashing",["Google","Uber"],"Expert"],
  ["Google Maps","Graph algorithms, ETA, Real-time updates",["Google"],"Expert"],
  ["Zoom (Video Calling)","WebRTC, SFU vs MCU, Quality adaptation",["Common"],"Expert"],
  ["Top K Heavy Hitter","Count-Min Sketch, HyperLogLog, Stream",["Meta","Amazon"],"Expert"],
  ["Aggregation System","Stream processing, Lambda architecture, Dashboards",["Netflix","Uber"],"Expert"],
  ["Distributed Search","Elasticsearch, Inverted Index, Sharding",["Google","Amazon"],"Expert"],
  ["Distributed Queue","Kafka design, Topics, Partitions, Consumer groups",["LinkedIn","Uber"],"Expert"],
  ["YouTube","Upload pipeline, Transcoding, CDN, Search, Recommendations",["Google"],"Core"],
  ["Job Scheduler","Cron, Priority Queue, Retries, Exactly-once, Distributed",["Google","Amazon"],"Advanced"],
  ["GenAI RAG System","Vector DB, Embeddings, Chunking, LLM orchestration",["GenAI"],"Advanced"],
].map(([n,f,co,tier])=>({n,f,co,tier,s:"todo",rating:0,notes:""}));

// ─── LLD: 25 problems ───
const LLD_INIT = [
  ["Parking Lot","Factory, Strategy, Observer","Flipkart/Amazon/Uber","Multi-level, vehicle types, pricing"],
  ["LRU Cache","HashMap + DLL","All companies","O(1) operations, thread-safe"],
  ["Rate Limiter","Strategy Pattern","Uber/Amazon","Token Bucket, Sliding Window"],
  ["Tic Tac Toe","State Pattern","Amazon/Google","N×N board, win detection"],
  ["Snake and Ladder","State, Observer","Flipkart/Amazon","Board gen, player turns"],
  ["BookMyShow","Observer, Strategy","Flipkart","Seat locking, concurrency"],
  ["Splitwise","Observer, Graph","Flipkart/PhonePe","Debt simplification"],
  ["Elevator System","State, Strategy, Observer","Uber/Amazon","Multi-elevator coordination"],
  ["LFU Cache","HashMap + Min Heap","Google/Amazon","Frequency eviction"],
  ["Chess Game","Strategy, Observer","Amazon/Google","Piece rules, check/checkmate"],
  ["Hotel Management","Factory, Strategy","MakeMyTrip/Airbnb","Room booking, pricing"],
  ["ATM Machine","State, Chain of Resp","Banks/Fintech","Auth, dispensing, transactions"],
  ["File System","Composite Pattern","Google/Dropbox","Hierarchy, permissions"],
  ["Vending Machine","State Pattern","Amazon/Flipkart","Coin handling, inventory"],
  ["Logger System","Singleton, Chain","All companies","Levels, sinks, async"],
  ["Car Rental","Factory, Strategy","Uber/Zoomcar","Availability, pricing"],
  ["Library Management","Factory Pattern","Common","Checkout, fines, reservations"],
  ["Food Ordering (Swiggy)","Strategy, Observer","Swiggy/Zomato","Cart, orders, delivery"],
  ["Cricket Scorecard","Observer","Flipkart","Innings, overs, statistics"],
  ["Stock Exchange","Observer, Mediator","Trading firms","Order matching, bid/ask"],
  ["Meeting Scheduler","Strategy","Google/Microsoft","Conflict detection, rooms"],
  ["Ride Sharing (Uber)","Strategy, Observer","Uber/Ola","Matching, fare, tracking"],
  ["URL Shortener (LLD)","Factory","All companies","Base62, collision handling"],
  ["Task Scheduler","Strategy, Queue","Google/Amazon","Priority, distributed"],
  ["Pub-Sub System","Observer, Queue","LinkedIn/Uber","Topics, subscribers, ordering"],
].map(([n,patterns,co,focus])=>({n,patterns,co,focus,s:"todo",notes:""}));

// ─── Concepts: 10 categories, 160+ items ───
const CONCEPTS_INIT = {
  os:["Process vs Thread (PCB, TCB, context switch cost)","Process States (New→Ready→Running→Waiting→Terminated)","CPU Scheduling (FCFS, SJF, RR, Priority, MLFQ)","Process Synchronization (Critical section, Peterson's)","Deadlock (4 conditions, Detection, Prevention, Avoidance)","Mutex vs Semaphore vs Monitor","Virtual Memory, Paging, Page tables, TLB","Blocking vs Non-blocking I/O, epoll, select","Producer-Consumer, Reader-Writer problems","Memory Management (Fragmentation, Paging, Segmentation)"],
  networking:["TCP 3-way handshake, Flow control, Congestion","UDP — when to use, use cases","HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)","TLS/HTTPS handshake flow","DNS resolution (recursive vs iterative)","WebSocket vs SSE vs Long Polling","REST vs gRPC vs GraphQL","L4 vs L7 Load Balancers","CDN — anycast, edge caching","API Gateway pattern","Sticky Sessions vs Stateless","CORS, OAuth2 flow","Rate Limiting at network level"],
  database:["B-tree internals (pages, splitting)","LSM tree (memtable, WAL, SSTables, compaction)","SQL vs NoSQL decision framework","ACID properties (explain each)","BASE properties","Isolation levels (Read Uncommitted → Serializable)","MVCC — how PostgreSQL does it","Indexing: composite, covering, partial, hash","N+1 query problem — detection and fix","Window functions (ROW_NUMBER, RANK, LAG, LEAD)","CTEs and recursive queries","Normalization (1NF→3NF→BCNF)","Denormalization — when and why","Sharding: hash vs range vs directory","Connection pooling (HikariCP)","DB Design 5-step framework","Query optimization (EXPLAIN ANALYZE)","Redis data structures deep dive"],
  distributed:["CAP Theorem (CP vs AP examples)","PACELC Theorem","Eventual vs Strong vs Causal Consistency","Consistent Hashing (virtual nodes)","Replication: Leader, Multi-leader, Leaderless","Quorum: W + R > N","Bloom Filters (false positives, use cases)","Merkle Trees (anti-entropy, sync)","Leader Election (Raft high level)","Gossip Protocol","Vector Clocks / Lamport Timestamps","SAGA (choreography vs orchestration)","CQRS pattern","Event Sourcing","Rate Limiting (Token Bucket, Leaky Bucket, Sliding Window)","Circuit Breaker, Bulkhead, Sidecar","Strangler Fig (migration)","2PC, 3PC (distributed transactions)","Distributed Locks (Redlock)","Retries, Exponential backoff, Jitter"],
  jvm:["JVM Architecture (class loading, JIT, runtime areas)","Heap: Young Gen, Old Gen, Metaspace","synchronized vs volatile vs Lock","ReentrantLock, ReadWriteLock","Double-checked locking Singleton","ThreadPool / ExecutorService / ForkJoinPool","CompletableFuture (thenApply, thenCompose, allOf)","ConcurrentHashMap (segments, CAS)","CountDownLatch, CyclicBarrier, Semaphore","G1GC (regions, mixed collections)","ZGC (colored pointers, sub-ms)","GC tuning (-Xmx, -XX:MaxGCPauseMillis)","Thread dump (jstack), Heap dump (VisualVM)","JIT compilation (C1, C2, tiered)","Collections internals (HashMap bucket, resize, collision)","Java 8+ (Streams, Optional, Lambda, Method refs)","Generics (type erasure, wildcards, bounds)"],
  spring:["Bean lifecycle and scopes","@Bean, @Qualifier, @Primary","Constructor vs Setter vs Field DI","@Transactional (propagation, isolation)","@ControllerAdvice + @ExceptionHandler","Spring AOP (cross-cutting concerns)","Actuator + Micrometer monitoring","Spring Data JPA (repos, JPQL, pagination)","Spring Security (JWT, OAuth 2.0, OIDC, API Security)","Auto-configuration mechanism","Spring WebFlux (reactive)","Caching with @Cacheable","Kafka Architecture (topics, partitions, consumer groups, ISR)"],
  microservices:["Monolith vs Microservices tradeoffs","Service Discovery (Eureka, Consul)","API Gateway pattern","Circuit Breaker (Resilience4j)","Distributed Tracing (Zipkin, Jaeger)","Event-Driven Architecture","SAGA pattern implementation","12-Factor App","Docker, Containers, Dockerfile","ECS/EKS/Kubernetes basics","CI/CD pipelines (GitHub Actions, CodePipeline)","RabbitMQ vs Kafka (when to use which)","Golang basics (goroutines, channels, concurrency model)"],
  patterns:["Singleton (5 variants)","Factory & Abstract Factory","Builder","Strategy","Observer","Decorator","State","Template Method","Chain of Responsibility","Proxy","Adapter","Facade","Command","SOLID principles (all 5)"],
  aws:["IAM (Users, Groups, Roles, Policies)","EC2 (Instance types, AMI, SG, EBS)","VPC (Subnets, Route tables, NAT, NACL)","S3 (Buckets, Lifecycle, Versioning, Glacier)","Lambda (Triggers, Layers, Concurrency)","API Gateway (REST, WebSocket, Throttling)","DynamoDB (GSI, LSI, Streams, DAX)","RDS/Aurora (Multi-AZ, Read replicas)","CloudWatch (Logs, Metrics, Alarms)","SNS/SQS (Pub/Sub, DLQ, FIFO, Fanout)","CloudFront CDN","Route 53 (DNS, Health checks)","Secrets Manager + KMS","Bedrock (Foundation models, Knowledge Bases)","SageMaker basics","Terraform / IaC basics","AWS↔Azure mapping (Lambda↔Functions, S3↔Blob, DynamoDB↔CosmosDB)","Azure OpenAI vs AWS Bedrock (when to use which)"],
  genai:["How LLMs work (tokens, context, temperature)","Prompt Engineering (system, few-shot, CoT)","Embeddings (vectors, cosine similarity)","RAG pipeline (chunk→embed→store→retrieve→generate)","Chunking strategies (fixed, recursive, semantic)","Vector DBs (FAISS, pgvector, Pinecone, Chroma)","LangChain (chains, tools, memory, agents)","LangGraph (nodes, edges, state, routing)","ReAct pattern (Reasoning + Acting)","Function calling / Tool use","Multi-agent orchestration","MCP Protocol (Model Context Protocol)","MCP Servers + Clients","Agent memory (short-term vs long-term)","AWS Bedrock (Claude, Titan, Knowledge Bases)","Evaluation (faithfulness, relevance, hallucination)","Guardrails (PII, output validation, prompt injection)","Hybrid search (BM25 + Vector, Reranking)","Cost optimization (caching, smaller models, batching)","RAG vs Fine-tuning decision framework"],
};

// ─── STAR Stories (14) ───
const STAR_INIT = [
  {lp:"Ownership",pr:"Went beyond your role",s:""},{lp:"Dive Deep",pr:"Dug into data for root cause",s:""},{lp:"Bias for Action",pr:"Decided with incomplete info",s:""},{lp:"Disagree & Commit",pr:"Disagreed but committed",s:""},{lp:"Customer Obsession",pr:"Prioritized the customer",s:""},{lp:"Deliver Results",pr:"Met a tight deadline",s:""},{lp:"Earn Trust",pr:"Admitted a mistake",s:""},{lp:"Invent & Simplify",pr:"Simplified something complex",s:""},{lp:"Think Big",pr:"Proposed something ambitious",s:""},{lp:"Have Backbone",pr:"Pushed back on leadership",s:""},{lp:"Production Incident",pr:"Handled critical outage",s:""},{lp:"Mentoring",pr:"Helped junior engineer grow",s:""},{lp:"Ambiguity",pr:"Handled unclear requirements",s:""},{lp:"Conflict",pr:"Resolved team disagreement",s:""},
];

// ─── Companies (12) ───
const COS = {
  apple:{nm:"Apple",rnds:"Phone→3T+1M",tip:"Deep JVM/concurrency. Double-checked locking, GC tuning, Spring @Bean/@Qualifier."},
  oracle:{nm:"Oracle",rnds:"Phone→3-4T",tip:"Distributed theory: quorum, bloom filters, consistent hashing, LSM trees."},
  amazon:{nm:"Amazon",rnds:"Phone→4-5L(2LP each)",tip:"12 STAR stories mapped to LPs. Ownership, Dive Deep most frequent."},
  doordash:{nm:"DoorDash",rnds:"Phone→3-4T+1C",tip:"Graph-heavy DSA. Multi-source BFS, tree paths. DoorDash eng blog."},
  google:{nm:"Google",rnds:"Phone→3C+1-2SD+1B",tip:"3 coding rounds! More DSA practice needed. Follow-ups push to Hard."},
  meta:{nm:"Meta",rnds:"Phone→2C+1SD+1B",tip:"AI-assisted coding in 2026. E6+: Design Redis/Kafka. Data model weighted."},
  microsoft:{nm:"Microsoft",rnds:"Phone→C+LLD+SD+B",tip:"LLD decides offer. AI awareness growing. Code quality > speed."},
  stripe:{nm:"Stripe",rnds:"Phone→C+Bug+Int+SD+B",tip:"NOT LeetCode-style. Integration with real GitHub repos. Clean tested code."},
  netflix:{nm:"Netflix",rnds:"Phone→4-5T+Culture",tip:"System design heavy. Independent decision-making. Freedom & responsibility."},
  uber:{nm:"Uber",rnds:"Phone→3-4T",tip:"Real-time systems. Geospatial (geohash, quadtree). Event-driven."},
  linkedin:{nm:"LinkedIn",rnds:"Phone→3C+1SD+1B",tip:"LinkedIn invented Kafka. Social graph problems. Feed ranking."},
  goldman:{nm:"Goldman Sachs",rnds:"Phone→4-5(C+SD+Math+B)",tip:"Financial domain. Strong SQL. ACID deeply. Transactions, ledgers."},
};

// ─── Roadmap (20 weeks) ───
const ROAD = [
  {w:1,ph:"Found",t:"OS + Arrays/Hashing",tasks:["OSTEP Ch 4-7","NeetCode: Arrays (16)","Prompt Engineering course","Setup workspace","Get DDIA"]},
  {w:2,ph:"Found",t:"Networking + TwoPtr/SlideWin",tasks:["OSTEP Ch 26-33","NeetCode: 2Ptr(5)+SlideWin(8)","Hussein Nasser videos","LangChain for LLM Apps","DB Schema: E-commerce"]},
  {w:3,ph:"Found",t:"DB Internals + Stack/BS",tasks:["DDIA Ch 3+7","NeetCode: Stack(7)+BS(10)","Chat with Your Data (RAG)","5 SQL problems","Activeloop RAG start"]},
  {w:4,ph:"Found",t:"Java Concurrency + LinkedList",tasks:["Concurrency in Practice Ch1-5","NeetCode: LinkedList(13)","Code: Producer-Consumer, Deadlock","LangChain Academy M0-2","5 SQL problems"]},
  {w:5,ph:"Found",t:"Advanced JVM + Trees",tasks:["Concurrency Ch8,10","NeetCode: Trees(18)","ThreadPool, CompletableFuture","LangChain Academy M3-4","AI Agents in LangGraph"]},
  {w:6,ph:"Found",t:"Spring Boot + Heap/Backtrack",tasks:["Build REST API (Spring Boot)","NeetCode: Heap(7)+Backtrack(9)","DDIA Ch5 Replication","LangChain Academy M5-6","DB Schema: Food Delivery"]},
  {w:7,ph:"Found",t:"Graphs + Tries + GenAI Project #1",tasks:["NeetCode: Graphs(14)+Tries(3)","DDIA Ch6 Partitioning","BUILD: Document Q&A (RAG)","Push Project #1 to GitHub","Start AWS: IAM, EC2, VPC"]},
  {w:8,ph:"Found",t:"DP + Complete NeetCode 150!",tasks:["NeetCode: DP(19)+Greedy(5)+Intervals(5)+Math+Bits","DDIA Ch9 Consistency","AWS: S3, Lambda, DynamoDB","5 SQL problems","Activeloop RAG complete"]},
  {w:9,ph:"Depth",t:"System Design Start",tasks:["Alex Xu Vol1 Ch1-4","SD: URL Shortener (record 35min)","SD: Rate Limiter","Re-solve weak DSA problems","Udemy LangChain course start"]},
  {w:10,ph:"Depth",t:"SD Core + LLD Start",tasks:["SD: Key-Value Store, Distributed Cache","LLD: Parking Lot, LRU Cache","DDIA Ch11 Stream Processing","AWS: API GW, RDS, CloudWatch","Design Patterns: 5 coded"]},
  {w:11,ph:"Depth",t:"SD + LLD + GenAI Project #2",tasks:["SD: Chat System, News Feed","LLD: Elevator, Rate Limiter","Start Interview Coach project","pgvector + MCP Protocol","Write 4 STAR stories"]},
  {w:12,ph:"Depth",t:"Advanced SD",tasks:["SD: Apple Music, Order Mgmt, Netflix","LLD: BookMyShow, Splitwise","Interview Coach continued","AWS: SNS/SQS, CloudFront","4 more STAR stories"]},
  {w:13,ph:"Depth",t:"Expert SD + Deploy",tasks:["SD: Payment System, Uber","LLD: Chess, Food Ordering","Deploy Interview Coach","SD: Task Scheduler, Web Crawler","Read 3 eng blogs"]},
  {w:14,ph:"Depth",t:"Company-Specific Prep",tasks:["SD: Kafka, Redis (E6 level)","LLD: Stock Exchange, Meeting Scheduler","DDIA Ch5-9 review","Company research (Glassdoor, Blind)","Polish all 14 STAR stories"]},
  {w:15,ph:"Polish",t:"Mocks Begin",tasks:["2 DSA mocks (Pramp)","1 SD mock (self-record)","Docker + monitoring on GenAI projects","Write blog post","AWS: Bedrock, SageMaker basics"]},
  {w:16,ph:"Polish",t:"Intensive Mocks",tasks:["3 mocks (alternate DSA/SD/Behavioral)","Timed DSA (25min M, 40min H)","Target company DSA problems","Clean GitHub + READMEs","OA practice (timed)"]},
  {w:17,ph:"Polish",t:"Full Simulations",tasks:["Full mock days (DSA+SD+Behavioral)","Practice designs to camera","Fill concept gaps","Update LinkedIn","Start applying"]},
  {w:18,ph:"Polish",t:"Applications Sprint",tasks:["Apply 5-10 companies/week","1 mock/day","Fix weak spots from feedback","Company-specific prep before each","STAR stories natural delivery"]},
  {w:19,ph:"Polish",t:"Active Interviewing",tasks:["Continue interviews","Morning: review for specific company","After each: write debrief","Stay sharp: 2-3 DSA/day","Adjust prep from real feedback"]},
  {w:20,ph:"Polish",t:"Final Push",tasks:["Continue interviews + negotiate","Use levels.fyi data","Review offers holistically","Trust your preparation","You earned this"]},
];

// ─── GenAI Courses ───
const GENAI_C = [
  {n:"Prompt Engineering",p:"DeepLearning.AI",h:"1.5h",u:"https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",w:1,f:true},
  {n:"LangChain for LLM Apps",p:"DeepLearning.AI",h:"1h",u:"https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/",w:2,f:true},
  {n:"Chat with Your Data (RAG)",p:"DeepLearning.AI",h:"1h",u:"https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/",w:3,f:true},
  {n:"Functions, Tools & Agents",p:"DeepLearning.AI",h:"1h",u:"https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/",w:4,f:true},
  {n:"AI Agents in LangGraph",p:"DeepLearning.AI",h:"1h",u:"https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/",w:5,f:true},
  {n:"Intro to LangGraph (Full)",p:"LangChain Academy",h:"5+h",u:"https://academy.langchain.com/courses/intro-to-langgraph",w:5,f:true},
  {n:"RAG Course (Advanced)",p:"Activeloop",h:"10+h",u:"https://learn.activeloop.ai/courses/rag",w:7,f:true},
  {n:"LangChain & LangGraph",p:"Udemy (Eden Marco)",h:"19h",u:"https://www.udemy.com/course/langchain/",w:9,f:false},
];

// ─── MAIN APP ───
export default function App(){
  const[d,setD]=useState(null);const[tab,setTab]=useState("dash");const[ld,setLd]=useState(true);
  useEffect(()=>{(async()=>{try{const r=await window.storage.get(K);setD(r?.value?{...mk(),...JSON.parse(r.value)}:mk())}catch{setD(mk())}setLd(false)})()},[]);
  const sv=useCallback(async nd=>{setD(nd);try{await window.storage.set(K,JSON.stringify(nd))}catch(e){console.error(e)}},[]);
  if(ld||!d)return<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100vh",background:"#080c14",color:"#484f58",fontFamily:"monospace"}}>Loading...</div>;

  const tabs=[{id:"dash",l:"◉ Dash"},{id:"road",l:"▸ Roadmap"},{id:"dsa",l:"⟐ DSA"},{id:"hld",l:"⊞ HLD"},{id:"lld",l:"⬡ LLD"},{id:"con",l:"◆ Concepts"},{id:"co",l:"⎈ Companies"},{id:"gen",l:"⚡ GenAI"},{id:"star",l:"★ STAR"},{id:"mock",l:"◎ Mocks"},{id:"app",l:"📋 Apply"},{id:"notes",l:"≡ Notes"},{id:"exp",l:"⇧ Export"}];
  const dsaDone=d.dsa.filter(p=>p.s==="done").length;const totalC=Object.values(d.concepts).flat();

  return(<div style={{minHeight:"100vh",background:"#080c14",color:"#c9d1d9",fontFamily:"'SF Mono',monospace",fontSize:12}}>
    <header style={{background:"linear-gradient(135deg,#0a1628,#0d1117,#121a2b)",borderBottom:"1px solid #1a2332",padding:"10px 14px",display:"flex",justifyContent:"space-between",alignItems:"center",flexWrap:"wrap",gap:6}}>
      <div><div style={{fontSize:16,fontWeight:800,background:"linear-gradient(90deg,#58a6ff,#bc8cff)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>⟨/⟩ 360° INTERVIEW HQ</div><div style={{fontSize:9,color:"#484f58"}}>SDE-2/Senior · 12 Companies · 200+ DSA · 35 HLD · 25 LLD · 20 Weeks</div></div>
      <div style={{display:"flex",gap:14}}>{[["Day",d.logs.length,"#58a6ff"],["Hrs",d.logs.reduce((s,l)=>s+(l.hours||0),0).toFixed(0),"#3fb950"],["DSA",`${dsaDone}/${d.dsa.length}`,"#d29922"],["🔥",calcStreak(d.logs),"#f778ba"]].map(([l,v,c],i)=><div key={i} style={{textAlign:"center"}}><div style={{fontSize:16,fontWeight:700,color:c}}>{v}</div><div style={{fontSize:8,color:"#484f58"}}>{l}</div></div>)}</div>
    </header>
    <div style={{display:"flex",borderBottom:"1px solid #1a2332",overflowX:"auto",background:"#0a0f1a"}}>{tabs.map(t=><button key={t.id} onClick={()=>setTab(t.id)} style={{background:tab===t.id?"#121a2b":"transparent",color:tab===t.id?"#58a6ff":"#3d444d",border:"none",borderBottom:tab===t.id?"2px solid #58a6ff":"2px solid transparent",padding:"7px 10px",cursor:"pointer",fontFamily:"inherit",fontSize:10,whiteSpace:"nowrap",fontWeight:tab===t.id?700:400}}>{t.l}</button>)}</div>
    <main style={{padding:"10px 12px",maxWidth:1200,margin:"0 auto"}}>
      {tab==="dash"&&<Dash d={d} sv={sv}/>}{tab==="road"&&<Road d={d} sv={sv}/>}{tab==="dsa"&&<DSATab d={d} sv={sv}/>}{tab==="hld"&&<HLDTab d={d} sv={sv}/>}{tab==="lld"&&<LLDTab d={d} sv={sv}/>}{tab==="con"&&<ConTab d={d} sv={sv}/>}{tab==="co"&&<CoTab/>}{tab==="gen"&&<GenTab d={d} sv={sv}/>}{tab==="star"&&<StarTab d={d} sv={sv}/>}{tab==="mock"&&<MockTab d={d} sv={sv}/>}{tab==="app"&&<AppTab d={d} sv={sv}/>}{tab==="notes"&&<NoteTab d={d} sv={sv}/>}{tab==="exp"&&<ExpTab d={d}/>}
    </main>
    <style>{`button:hover{filter:brightness(1.15)}::-webkit-scrollbar{width:4px}::-webkit-scrollbar-thumb{background:#1a2332;border-radius:2px}input,textarea,select{font-family:inherit;font-size:11px}`}</style>
  </div>);
}

function mk(){return{dsa:DSA_INIT.map(x=>({...x})),hld:HLD_INIT.map(x=>({...x})),lld:LLD_INIT.map(x=>({...x})),concepts:Object.fromEntries(Object.entries(CONCEPTS_INIT).map(([k,v])=>[k,v.map(c=>({n:c,s:false,c:false}))])),genDone:GENAI_C.map(()=>false),star:STAR_INIT.map(s=>({...s})),logs:[],notes:[],mocks:[],apps:[],weekChecks:{},currentWeek:1}}
function calcStreak(logs){if(!logs.length)return 0;let s=0,dt=new Date();for(let i=0;i<365;i++){if(logs.some(l=>l.date===dt.toISOString().split("T")[0])){s++;dt.setDate(dt.getDate()-1)}else break}return s}

// ─── UI ───
const X={card:{background:"#0d1320",border:"1px solid #1a2332",borderRadius:6,padding:10,marginBottom:8},ct:{fontSize:12,fontWeight:600,color:"#e6edf3",marginBottom:6,borderBottom:"1px solid #1a2332",paddingBottom:5},inp:{background:"#080c14",border:"1px solid #1a2332",borderRadius:3,padding:"5px 7px",color:"#c9d1d9",outline:"none",fontFamily:"inherit"},btn:{background:"#238636",color:"#fff",border:"none",borderRadius:3,padding:"5px 12px",cursor:"pointer",fontFamily:"inherit",fontWeight:600,fontSize:10},fb:{background:"transparent",border:"1px solid #1a2332",borderRadius:3,padding:"2px 7px",cursor:"pointer",color:"#484f58",fontSize:9,fontFamily:"inherit"},addBtn:{background:"#1a2332",color:"#58a6ff",border:"1px dashed #30363d",borderRadius:4,padding:"6px 12px",cursor:"pointer",fontFamily:"inherit",fontSize:10,width:"100%",marginTop:6}};
function C({children,title,style={}}){return<div style={{...X.card,...style}}>{title&&<div style={X.ct}>{title}</div>}{children}</div>}
function Bar({v,mx,c="#58a6ff",h=4}){return<div style={{background:"#151d2e",borderRadius:h/2,height:h,width:"100%",overflow:"hidden"}}><div style={{background:c,height:"100%",width:`${mx>0?(v/mx)*100:0}%`,borderRadius:h/2,transition:"width .3s"}}/></div>}
function SB({status,onChange}){const m={todo:{b:"#151d2e",d:"#1a2332",c:"#484f58",l:"TODO"},doing:{b:"#2a1f00",d:"#d29922",c:"#d29922",l:"WIP"},done:{b:"#0b3d1c",d:"#238636",c:"#3fb950",l:"DONE"},redo:{b:"#3d1a1a",d:"#da3633",c:"#f85149",l:"REDO"}};const o=["todo","doing","done","redo"];const s=m[status]||m.todo;return<button onClick={()=>onChange(o[(o.indexOf(status)+1)%4])} style={{background:s.b,border:`1px solid ${s.d}`,color:s.c,borderRadius:3,padding:"1px 6px",cursor:"pointer",fontSize:8,fontFamily:"inherit",fontWeight:700,minWidth:34}}>{s.l}</button>}
const DC={E:"#3fb950",M:"#d29922",H:"#f85149"};

// ─── DASHBOARD ───
function Dash({d,sv}){
  const today=new Date().toISOString().split("T")[0];const logged=d.logs.some(l=>l.date===today);
  const[f,sF]=useState({hours:"",topic:"",takeaway:""});
  const log=()=>{if(!f.hours)return;sv({...d,logs:[...d.logs.filter(l=>l.date!==today),{date:today,...f,hours:parseFloat(f.hours)}].sort((a,b)=>a.date.localeCompare(b.date))});sF({hours:"",topic:"",takeaway:""})};
  const tc=Object.values(d.concepts).flat();
  return<div>
    {!logged&&<C style={{border:"1px solid #f85149"}}><div style={{color:"#f85149",fontWeight:600,fontSize:11,marginBottom:6}}>⚠ LOG TODAY</div><div style={{display:"flex",gap:4,flexWrap:"wrap"}}><input style={{...X.inp,width:50}} type="number" step="0.5" placeholder="Hrs" value={f.hours} onChange={e=>sF({...f,hours:e.target.value})}/><input style={{...X.inp,flex:1,minWidth:100}} placeholder="Topic" value={f.topic} onChange={e=>sF({...f,topic:e.target.value})}/><input style={{...X.inp,flex:1,minWidth:100}} placeholder="Takeaway" value={f.takeaway} onChange={e=>sF({...f,takeaway:e.target.value})}/><button onClick={log} style={X.btn}>Log</button></div></C>}
    {logged&&<C style={{border:"1px solid #238636"}}><span style={{color:"#3fb950",fontSize:11}}>✓ Logged — {d.logs.find(l=>l.date===today)?.hours}h</span></C>}
    <C title={`Week ${d.currentWeek}/20: ${ROAD[Math.min(d.currentWeek-1,19)].t}`}><Bar v={d.currentWeek} mx={20} c="#58a6ff" h={6}/><div style={{display:"flex",justifyContent:"space-between",marginTop:3}}><span style={{fontSize:9,color:"#484f58"}}>{ROAD[Math.min(d.currentWeek-1,19)].ph}</span><div style={{display:"flex",gap:3}}><button onClick={()=>sv({...d,currentWeek:Math.max(1,d.currentWeek-1)})} style={X.fb}>←</button><button onClick={()=>sv({...d,currentWeek:Math.min(20,d.currentWeek+1)})} style={X.fb}>→</button></div></div></C>
    <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(130px,1fr))",gap:6}}>
      {[["DSA",d.dsa.filter(p=>p.s==="done").length,d.dsa.length,"#3fb950"],["HLD",d.hld.filter(p=>p.s==="done").length,d.hld.length,"#bc8cff"],["LLD",d.lld.filter(p=>p.s==="done").length,d.lld.length,"#d29922"],["Concepts",tc.filter(c=>c.c).length,tc.length,"#f778ba"],["GenAI",d.genDone.filter(Boolean).length,d.genDone.length,"#58a6ff"],["STAR",d.star.filter(s=>s.s.length>20).length,14,"#f85149"],["Mocks",d.mocks.length,20,"#79c0ff"],["Apps",d.apps.length,0,"#7ee787"]].map(([l,v,mx,c],i)=><C key={i}><div style={{fontSize:8,color:"#484f58",textTransform:"uppercase",letterSpacing:1}}>{l}</div><div style={{fontSize:18,fontWeight:700,color:c}}>{v}{mx>0&&<span style={{fontSize:10,color:"#484f58"}}>/{mx}</span>}</div><Bar v={v} mx={mx||v||1} c={c}/></C>)}
    </div>
    <C title="Recent">{d.logs.slice(-5).reverse().map((l,i)=><div key={i} style={{display:"flex",gap:4,padding:"2px 0",borderBottom:"1px solid #0d1320",fontSize:10}}><span style={{color:"#58a6ff",width:65}}>{l.date}</span><span style={{color:"#3fb950",width:20}}>{l.hours}h</span><span style={{color:"#c9d1d9",flex:1}}>{l.topic}</span></div>)}{!d.logs.length&&<div style={{color:"#484f58",textAlign:"center",padding:8,fontSize:11}}>No logs yet</div>}</C>
  </div>;
}

// ─── ROADMAP ───
function Road({d,sv}){
  const toggle=(w,i)=>{const k=`w${w}-${i}`;sv({...d,weekChecks:{...d.weekChecks,[k]:!d.weekChecks[k]}})};
  return<div>{ROAD.map((w,wi)=>{const dn=w.tasks.filter((_,i)=>d.weekChecks[`w${w.w}-${i}`]).length;
    return<C key={wi} style={d.currentWeek===w.w?{border:"1px solid #58a6ff"}:{}} title={<div style={{display:"flex",justifyContent:"space-between"}}><span><span style={{color:{Found:"#58a6ff",Depth:"#d29922",Polish:"#3fb950"}[w.ph],fontSize:8,marginRight:4}}>{w.ph.toUpperCase()}</span>W{w.w}: {w.t}</span><span style={{fontSize:9,color:dn===w.tasks.length?"#3fb950":"#484f58"}}>{dn}/{w.tasks.length}</span></div>}>
      {w.tasks.map((t,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:5,padding:"2px 0"}}><button onClick={()=>toggle(w.w,i)} style={{width:14,height:14,borderRadius:2,border:"1px solid "+(d.weekChecks[`w${w.w}-${i}`]?"#238636":"#1a2332"),background:d.weekChecks[`w${w.w}-${i}`]?"#238636":"transparent",color:"#fff",cursor:"pointer",fontSize:8,display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>{d.weekChecks[`w${w.w}-${i}`]?"✓":""}</button><span style={{fontSize:10,color:d.weekChecks[`w${w.w}-${i}`]?"#484f58":"#c9d1d9"}}>{t}</span></div>)}
    </C>})}</div>;
}

// ─── DSA (200+, filterable, configurable) ───
function DSATab({d,sv}){
  const[fp,sFp]=useState("all");const[fc,sFc]=useState("all");const[fd,sFd]=useState("all");const[adding,setAdding]=useState(false);const[nf,setNf]=useState({n:"",p:"Arrays",lc:0,d:"M",pat:"",co:""});
  const up=(i,f,v)=>{const a=[...d.dsa];a[i]={...a[i],[f]:v};sv({...d,dsa:a})};
  const addCustom=()=>{if(!nf.n)return;sv({...d,dsa:[...d.dsa,{...nf,co:nf.co.split(",").map(s=>s.trim()),s:"todo",notes:""}]});setNf({n:"",p:"Arrays",lc:0,d:"M",pat:"",co:""});setAdding(false)};
  const pats=[...new Set(d.dsa.map(p=>p.p))];const cos=[...new Set(d.dsa.flatMap(p=>p.co))].sort();
  let list=d.dsa;if(fp!=="all")list=list.filter(p=>p.p===fp);if(fc!=="all")list=list.filter(p=>p.co.includes(fc));if(fd!=="all")list=list.filter(p=>p.d===fd);
  const done=d.dsa.filter(p=>p.s==="done").length;

  return<div>
    <C><div style={{display:"flex",justifyContent:"space-between"}}><span style={{fontWeight:600,color:"#e6edf3"}}>DSA: {done}/{d.dsa.length}</span><span style={{fontSize:10,color:"#484f58"}}>NeetCode 150 + Garima + OA</span></div><Bar v={done} mx={d.dsa.length} c="#3fb950" h={6}/></C>
    <C>
      <div style={{fontSize:9,color:"#484f58",marginBottom:3}}>PATTERN</div>
      <div style={{display:"flex",gap:3,flexWrap:"wrap",marginBottom:6}}><button onClick={()=>sFp("all")} style={{...X.fb,...(fp==="all"?{borderColor:"#58a6ff",color:"#58a6ff"}:{})}}>All</button>{pats.map(p=><button key={p} onClick={()=>sFp(p)} style={{...X.fb,...(fp===p?{borderColor:"#58a6ff",color:"#58a6ff"}:{})}}>{p}</button>)}</div>
      <div style={{fontSize:9,color:"#484f58",marginBottom:3}}>COMPANY</div>
      <div style={{display:"flex",gap:3,flexWrap:"wrap",marginBottom:6}}><button onClick={()=>sFc("all")} style={{...X.fb,...(fc==="all"?{borderColor:"#58a6ff",color:"#58a6ff"}:{})}}>All</button>{cos.map(c=><button key={c} onClick={()=>sFc(c)} style={{...X.fb,...(fc===c?{borderColor:"#58a6ff",color:"#58a6ff"}:{})}}>{c}</button>)}</div>
      <div style={{display:"flex",gap:3}}>{["all","E","M","H"].map(x=><button key={x} onClick={()=>sFd(x)} style={{...X.fb,...(fd===x?{borderColor:DC[x]||"#58a6ff",color:DC[x]||"#58a6ff"}:{})}}>{x==="all"?"All":x}</button>)}</div>
    </C>
    <div style={{background:"#0d1320",border:"1px solid #1a2332",borderRadius:6,overflow:"hidden"}}>{list.map(p=>{const i=d.dsa.indexOf(p);return<div key={i} style={{display:"flex",alignItems:"center",gap:4,padding:"4px 8px",borderBottom:"1px solid #0d1825",fontSize:10}}>
      <SB status={p.s} onChange={s=>up(i,"s",s)}/>
      <span style={{color:DC[p.d],fontWeight:700,width:12}}>{p.d}</span>
      {p.lc?<a href={`https://leetcode.com/problems/`} target="_blank" rel="noreferrer" style={{color:p.s==="done"?"#484f58":"#c9d1d9",flex:1,textDecoration:"none"}}>{p.n}</a>:<span style={{flex:1,color:"#c9d1d9"}}>{p.n}</span>}
      <span style={{color:"#3d444d",fontSize:9,width:70,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{p.pat}</span>
      <span style={{color:"#58a6ff",fontSize:8}}>{p.co?.slice(0,2).join(",")}</span>
    </div>})}</div>
    {adding?<C style={{border:"1px dashed #58a6ff"}}><div style={{fontSize:10,color:"#58a6ff",marginBottom:6}}>+ ADD CUSTOM PROBLEM</div><div style={{display:"flex",gap:4,flexWrap:"wrap"}}><input style={{...X.inp,flex:1}} placeholder="Problem name" value={nf.n} onChange={e=>setNf({...nf,n:e.target.value})}/><select style={X.inp} value={nf.d} onChange={e=>setNf({...nf,d:e.target.value})}><option>E</option><option>M</option><option>H</option></select><input style={{...X.inp,width:80}} placeholder="Pattern" value={nf.pat} onChange={e=>setNf({...nf,pat:e.target.value})}/><input style={{...X.inp,width:100}} placeholder="Companies (,)" value={nf.co} onChange={e=>setNf({...nf,co:e.target.value})}/><button onClick={addCustom} style={X.btn}>Add</button><button onClick={()=>setAdding(false)} style={{...X.fb,color:"#f85149"}}>Cancel</button></div></C>:<button onClick={()=>setAdding(true)} style={X.addBtn}>+ Add Custom DSA Problem</button>}
  </div>;
}

// ─── HLD (35, configurable) ───
function HLDTab({d,sv}){
  const[ft,sFt]=useState("all");const[adding,setAdding]=useState(false);const[nf,setNf]=useState({n:"",f:"",co:"",tier:"Core"});
  const up=(i,f,v)=>{const a=[...d.hld];a[i]={...a[i],[f]:v};sv({...d,hld:a})};
  const add=()=>{if(!nf.n)return;sv({...d,hld:[...d.hld,{...nf,co:nf.co.split(",").map(s=>s.trim()),s:"todo",rating:0,notes:""}]});setNf({n:"",f:"",co:"",tier:"Core"});setAdding(false)};
  const tiers=["Fundamental","Core","Advanced","Expert"];const list=ft==="all"?d.hld:d.hld.filter(s=>s.tier===ft);
  return<div>
    <C title="7-STEP FRAMEWORK"><div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(100px,1fr))",gap:3,fontSize:9,color:"#8b949e"}}>{["1.Requirements","2.Estimation","3.API","4.Data Model","5.Architecture","6.Deep Dives","7.Tradeoffs"].map((s,i)=><div key={i} style={{background:"#0a1628",padding:"3px 6px",borderRadius:2,borderLeft:"2px solid #58a6ff"}}>{s}</div>)}</div></C>
    <div style={{display:"flex",gap:3,marginBottom:6}}><button onClick={()=>sFt("all")} style={{...X.fb,...(ft==="all"?{borderColor:"#58a6ff",color:"#58a6ff"}:{})}}>All ({d.hld.length})</button>{tiers.map(t=><button key={t} onClick={()=>sFt(t)} style={{...X.fb,...(ft===t?{borderColor:"#bc8cff",color:"#bc8cff"}:{})}}>{t}</button>)}</div>
    {list.map(sd=>{const i=d.hld.indexOf(sd);return<C key={i}><div style={{display:"flex",alignItems:"center",gap:6,marginBottom:3}}>
      <SB status={sd.s} onChange={s=>up(i,"s",s)}/>
      <span style={{color:"#e6edf3",fontWeight:600,flex:1,fontSize:11}}>{sd.n}</span>
      <span style={{fontSize:8,color:{Fundamental:"#3fb950",Core:"#58a6ff",Advanced:"#d29922",Expert:"#f85149"}[sd.tier],background:"#0a1628",padding:"1px 5px",borderRadius:2}}>{sd.tier}</span>
    </div><div style={{fontSize:9,color:"#484f58"}}>{sd.f}</div>
    <textarea style={{...X.inp,minHeight:24,width:"100%",boxSizing:"border-box",marginTop:3}} placeholder="Notes..." value={sd.notes} onChange={e=>up(i,"notes",e.target.value)}/></C>})}
    {adding?<C style={{border:"1px dashed #58a6ff"}}><div style={{display:"flex",gap:4,flexWrap:"wrap"}}><input style={{...X.inp,flex:1}} placeholder="System name" value={nf.n} onChange={e=>setNf({...nf,n:e.target.value})}/><input style={{...X.inp,flex:1}} placeholder="Key concepts" value={nf.f} onChange={e=>setNf({...nf,f:e.target.value})}/><select style={X.inp} value={nf.tier} onChange={e=>setNf({...nf,tier:e.target.value})}>{tiers.map(t=><option key={t}>{t}</option>)}</select><button onClick={add} style={X.btn}>Add</button></div></C>:<button onClick={()=>setAdding(true)} style={X.addBtn}>+ Add Custom System Design</button>}
  </div>;
}

// ─── LLD (25, configurable) ───
function LLDTab({d,sv}){
  const[adding,setAdding]=useState(false);const[nf,setNf]=useState({n:"",patterns:"",co:"",focus:""});
  const up=(i,f,v)=>{const a=[...d.lld];a[i]={...a[i],[f]:v};sv({...d,lld:a})};
  const add=()=>{if(!nf.n)return;sv({...d,lld:[...d.lld,{...nf,s:"todo",notes:""}]});setNf({n:"",patterns:"",co:"",focus:""});setAdding(false)};
  return<div><C title="LLD · Machine Coding · 45min"><div style={{fontSize:10,color:"#8b949e"}}>Classes → Interfaces → SOLID → Code → Test</div></C>
    {d.lld.map((p,i)=><C key={i}><div style={{display:"flex",alignItems:"center",gap:6,marginBottom:3}}><SB status={p.s} onChange={s=>up(i,"s",s)}/><span style={{color:"#e6edf3",fontWeight:500,flex:1,fontSize:11}}>{p.n}</span><span style={{fontSize:9,color:"#484f58"}}>{p.co}</span></div><div style={{fontSize:9,color:"#d29922"}}>{p.patterns}</div><textarea style={{...X.inp,minHeight:20,width:"100%",boxSizing:"border-box",marginTop:2}} placeholder="Notes..." value={p.notes} onChange={e=>up(i,"notes",e.target.value)}/></C>)}
    {adding?<C style={{border:"1px dashed #58a6ff"}}><div style={{display:"flex",gap:4,flexWrap:"wrap"}}><input style={{...X.inp,flex:1}} placeholder="Problem" value={nf.n} onChange={e=>setNf({...nf,n:e.target.value})}/><input style={{...X.inp,flex:1}} placeholder="Patterns" value={nf.patterns} onChange={e=>setNf({...nf,patterns:e.target.value})}/><button onClick={add} style={X.btn}>Add</button></div></C>:<button onClick={()=>setAdding(true)} style={X.addBtn}>+ Add Custom LLD</button>}
  </div>;
}

// ─── CONCEPTS (160+, configurable) ───
function ConTab({d,sv}){
  const labels={os:"Operating Systems",networking:"Networking",database:"Databases",distributed:"Distributed Systems",jvm:"JVM & Java",spring:"Spring Boot",microservices:"Microservices",patterns:"Design Patterns",aws:"AWS Cloud",genai:"GenAI / AI Engineering"};
  const[adding,setAdding]=useState(null);const[nv,setNv]=useState("");
  const toggle=(cat,idx,field)=>{const c={...d.concepts};c[cat]=[...c[cat]];c[cat][idx]={...c[cat][idx],[field]:!c[cat][idx][field]};if(field==="c"&&!c[cat][idx].s)c[cat][idx].s=true;sv({...d,concepts:c})};
  const addConcept=(cat)=>{if(!nv.trim())return;const c={...d.concepts};c[cat]=[...c[cat],{n:nv.trim(),s:false,c:false}];sv({...d,concepts:c});setNv("");setAdding(null)};
  return<div>{Object.entries(d.concepts).map(([cat,items])=>{const dn=items.filter(i=>i.s).length;const cf=items.filter(i=>i.c).length;
    return<C key={cat} title={<span>{labels[cat]||cat} <span style={{color:"#484f58",fontWeight:400}}>— {dn}/{items.length} studied · {cf} confident</span></span>}>
      {items.map((item,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:5,padding:"2px 0",borderBottom:"1px solid #0d1320"}}>
        <button onClick={()=>toggle(cat,i,"s")} style={{width:14,height:14,borderRadius:2,border:"1px solid "+(item.s?"#238636":"#1a2332"),background:item.s?"#238636":"transparent",color:"#fff",cursor:"pointer",fontSize:7,display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>{item.s?"✓":""}</button>
        <span style={{flex:1,fontSize:10,color:item.s?"#484f58":"#c9d1d9"}}>{item.n}</span>
        <button onClick={()=>toggle(cat,i,"c")} style={{background:item.c?"#0a1929":"transparent",border:"1px solid "+(item.c?"#58a6ff":"#1a2332"),borderRadius:2,padding:"1px 5px",cursor:"pointer",color:item.c?"#58a6ff":"#3d444d",fontSize:8,fontFamily:"inherit"}}>{item.c?"✓":""}</button>
      </div>)}
      {adding===cat?<div style={{display:"flex",gap:3,marginTop:4}}><input style={{...X.inp,flex:1}} placeholder="New concept..." value={nv} onChange={e=>setNv(e.target.value)} onKeyDown={e=>e.key==="Enter"&&addConcept(cat)}/><button onClick={()=>addConcept(cat)} style={X.btn}>+</button></div>:<button onClick={()=>setAdding(cat)} style={{...X.addBtn,fontSize:9}}>+ Add to {labels[cat]||cat}</button>}
    </C>})}</div>;
}

// ─── COMPANIES ───
function CoTab(){return<div>{Object.entries(COS).map(([k,co])=><C key={k} title={co.nm}><div style={{fontSize:10}}><span style={{color:"#484f58"}}>Rounds: </span><span style={{color:"#c9d1d9"}}>{co.rnds}</span></div><div style={{fontSize:10,color:"#d29922",marginTop:3,background:"#0a1628",padding:4,borderRadius:3,borderLeft:"2px solid #3fb950"}}>💡 {co.tip}</div></C>)}</div>}

// ─── GENAI ───
function GenTab({d,sv}){
  const toggle=i=>{const g=[...d.genDone];g[i]=!g[i];sv({...d,genDone:g})};
  return<div><C title="⚡ GenAI Learning Path">{GENAI_C.map((c,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:6,padding:"4px 0",borderBottom:"1px solid #0d1320"}}><button onClick={()=>toggle(i)} style={{width:16,height:16,borderRadius:"50%",border:"2px solid "+(d.genDone[i]?"#3fb950":"#1a2332"),background:d.genDone[i]?"#3fb950":"transparent",color:"#fff",cursor:"pointer",fontSize:9,display:"flex",alignItems:"center",justifyContent:"center"}}>{d.genDone[i]?"✓":""}</button><div style={{flex:1}}><div style={{color:d.genDone[i]?"#484f58":"#e6edf3",fontSize:11}}>{c.n}</div><div style={{fontSize:9,color:"#484f58"}}>{c.p} · {c.h} · W{c.w} · {c.f?<span style={{color:"#3fb950"}}>FREE</span>:<span style={{color:"#d29922"}}>Paid</span>}</div></div><a href={c.u} target="_blank" rel="noreferrer" style={{color:"#58a6ff",fontSize:9}}>→</a></div>)}</C>
    <C title="Portfolio Projects"><div style={{background:"#0a1628",padding:8,borderRadius:4,borderLeft:"3px solid #3fb950",marginBottom:6}}><div style={{color:"#e6edf3",fontWeight:600,fontSize:11}}>P1: Document Q&A (RAG) — Week 7</div><div style={{fontSize:10,color:"#8b949e"}}>Python + FastAPI + LangChain + FAISS + Streamlit</div></div><div style={{background:"#0a1628",padding:8,borderRadius:4,borderLeft:"3px solid #bc8cff"}}><div style={{color:"#e6edf3",fontWeight:600,fontSize:11}}>P2: Interview Coach (Agent) — Week 12</div><div style={{fontSize:10,color:"#8b949e"}}>Python + FastAPI + LangGraph + pgvector + React</div></div></C>
  </div>;
}

// ─── STAR ───
function StarTab({d,sv}){
  const up=(i,s)=>{const a=[...d.star];a[i]={...a[i],s};sv({...d,star:a})};
  return<div><C title={`★ STAR Stories — ${d.star.filter(s=>s.s.length>20).length}/14`}><Bar v={d.star.filter(s=>s.s.length>20).length} mx={14} c="#f85149" h={5}/></C>
    {d.star.map((s,i)=><C key={i} title={<span><span style={{color:"#d29922"}}>{s.lp}</span> — {s.pr}</span>}><textarea style={{...X.inp,minHeight:60,width:"100%",boxSizing:"border-box"}} placeholder="S: ... T: ... A: ... R: ..." value={s.s} onChange={e=>up(i,e.target.value)}/></C>)}
  </div>;
}

// ─── MOCKS ───
function MockTab({d,sv}){
  const[f,sF]=useState({date:new Date().toISOString().split("T")[0],type:"DSA",platform:"Pramp",rating:"",feedback:"",weak:""});
  const add=()=>{if(!f.rating)return;sv({...d,mocks:[...d.mocks,{...f,rating:parseInt(f.rating)}]});sF({...f,rating:"",feedback:"",weak:""})};
  return<div><C title="Log Mock"><div style={{display:"flex",gap:3,flexWrap:"wrap",marginBottom:4}}><input style={{...X.inp,width:90}} type="date" value={f.date} onChange={e=>sF({...f,date:e.target.value})}/><select style={X.inp} value={f.type} onChange={e=>sF({...f,type:e.target.value})}>{["DSA","System Design","LLD","Behavioral","Full Loop"].map(t=><option key={t}>{t}</option>)}</select><select style={X.inp} value={f.platform} onChange={e=>sF({...f,platform:e.target.value})}>{["Pramp","Interviewing.io","Exponent","Self","Friend"].map(t=><option key={t}>{t}</option>)}</select><input style={{...X.inp,width:35}} type="number" min="1" max="5" placeholder="1-5" value={f.rating} onChange={e=>sF({...f,rating:e.target.value})}/></div><input style={{...X.inp,width:"100%",boxSizing:"border-box",marginBottom:3}} placeholder="Feedback" value={f.feedback} onChange={e=>sF({...f,feedback:e.target.value})}/><button onClick={add} style={X.btn}>Log</button></C>
    {d.mocks.slice().reverse().map((m,i)=><C key={i}><div style={{display:"flex",gap:4,fontSize:10}}><span style={{color:"#58a6ff"}}>{m.date}</span><span>{m.type}</span><span style={{color:m.rating>=4?"#3fb950":m.rating>=3?"#d29922":"#f85149"}}>{"●".repeat(m.rating)}{"○".repeat(5-m.rating)}</span></div>{m.feedback&&<div style={{fontSize:10,color:"#8b949e"}}>💬 {m.feedback}</div>}</C>)}
  </div>;
}

// ─── APPLICATION TRACKER ───
function AppTab({d,sv}){
  const[f,sF]=useState({company:"",role:"SDE-2",status:"Applied",date:new Date().toISOString().split("T")[0],notes:""});
  const add=()=>{if(!f.company)return;sv({...d,apps:[...d.apps,{...f,id:Date.now()}]});sF({...f,company:"",notes:""})};
  const up=(id,field,val)=>{sv({...d,apps:d.apps.map(a=>a.id===id?{...a,[field]:val}:a)})};
  const del=id=>sv({...d,apps:d.apps.filter(a=>a.id!==id)});
  const statuses=["Wishlist","Applied","Phone Screen","Technical","Onsite","Offer","Rejected"];
  const sc={Wishlist:"#484f58",Applied:"#58a6ff","Phone Screen":"#d29922",Technical:"#bc8cff",Onsite:"#f778ba",Offer:"#3fb950",Rejected:"#f85149"};
  return<div><C title="📋 Track Applications"><div style={{display:"flex",gap:3,flexWrap:"wrap",marginBottom:4}}><input style={{...X.inp,flex:1}} placeholder="Company" value={f.company} onChange={e=>sF({...f,company:e.target.value})}/><input style={{...X.inp,width:80}} placeholder="Role" value={f.role} onChange={e=>sF({...f,role:e.target.value})}/><select style={X.inp} value={f.status} onChange={e=>sF({...f,status:e.target.value})}>{statuses.map(s=><option key={s}>{s}</option>)}</select><button onClick={add} style={X.btn}>Add</button></div></C>
    {d.apps.map(a=><C key={a.id}><div style={{display:"flex",alignItems:"center",gap:6}}>
      <span style={{fontWeight:600,color:"#e6edf3",flex:1,fontSize:11}}>{a.company}</span><span style={{fontSize:10,color:"#484f58"}}>{a.role}</span>
      <select style={{...X.inp,color:sc[a.status]}} value={a.status} onChange={e=>up(a.id,"status",e.target.value)}>{statuses.map(s=><option key={s}>{s}</option>)}</select>
      <button onClick={()=>del(a.id)} style={{background:"none",border:"none",color:"#484f58",cursor:"pointer"}}>×</button>
    </div><input style={{...X.inp,width:"100%",boxSizing:"border-box",marginTop:3}} placeholder="Notes (referral, interview dates...)" value={a.notes} onChange={e=>up(a.id,"notes",e.target.value)}/></C>)}
  </div>;
}

// ─── NOTES ───
function NoteTab({d,sv}){
  const[f,sF]=useState({title:"",tag:"general",body:""});const[ft,sFt]=useState("all");
  const add=()=>{if(!f.body.trim())return;sv({...d,notes:[...d.notes,{...f,date:new Date().toISOString().split("T")[0],id:Date.now()}]});sF({title:"",tag:"general",body:""})};
  const del=id=>sv({...d,notes:d.notes.filter(n=>n.id!==id)});
  const tags=["all",...new Set(d.notes.map(n=>n.tag))];
  return<div><C title="New Note"><div style={{display:"flex",gap:4,marginBottom:4}}><input style={{...X.inp,flex:1}} placeholder="Title" value={f.title} onChange={e=>sF({...f,title:e.target.value})}/><select style={X.inp} value={f.tag} onChange={e=>sF({...f,tag:e.target.value})}>{["general","dsa","system-design","lld","java","db","distributed","genai","behavioral","insight","aws","company"].map(t=><option key={t}>{t}</option>)}</select></div><textarea style={{...X.inp,minHeight:60,width:"100%",boxSizing:"border-box"}} placeholder="What did you learn?" value={f.body} onChange={e=>sF({...f,body:e.target.value})}/><button onClick={add} style={{...X.btn,marginTop:4}}>Save</button></C>
    <div style={{display:"flex",gap:3,marginBottom:6,flexWrap:"wrap"}}>{tags.map(t=><button key={t} onClick={()=>sFt(t)} style={{...X.fb,...(ft===t?{borderColor:"#58a6ff",color:"#58a6ff"}:{})}}>{t}</button>)}</div>
    {(ft==="all"?d.notes:d.notes.filter(n=>n.tag===ft)).slice().reverse().map(n=><C key={n.id}><div style={{display:"flex",justifyContent:"space-between"}}><div><span style={{color:"#58a6ff",fontSize:9}}>{n.date}</span><span style={{background:"#0a1628",padding:"1px 4px",borderRadius:2,fontSize:8,color:"#484f58",marginLeft:3}}>{n.tag}</span>{n.title&&<span style={{color:"#e6edf3",marginLeft:3,fontSize:10}}>{n.title}</span>}</div><button onClick={()=>del(n.id)} style={{background:"none",border:"none",color:"#484f58",cursor:"pointer"}}>×</button></div><div style={{fontSize:10,color:"#c9d1d9",whiteSpace:"pre-wrap",marginTop:2}}>{n.body}</div></C>)}
  </div>;
}

// ─── EXPORT ───
function ExpTab({d}){
  const gen=()=>{let m=`# 360° Prep Export\n> ${new Date().toISOString().split("T")[0]} | Days:${d.logs.length} | Hours:${d.logs.reduce((s,l)=>s+(l.hours||0),0).toFixed(1)}\n\n`;
    m+=`## DSA (${d.dsa.filter(p=>p.s==="done").length}/${d.dsa.length})\n|#|Problem|Pattern|D|Status|Companies|\n|-|-|-|-|-|-|\n`;
    d.dsa.forEach((p,i)=>m+=`|${i+1}|${p.n}|${p.pat}|${p.d}|${p.s}|${p.co?.join(",")}|\n`);
    m+=`\n## HLD (${d.hld.filter(s=>s.s==="done").length}/${d.hld.length})\n`;d.hld.forEach(s=>m+=`### ${s.n} [${s.tier}] — ${s.s}\n${s.f}\n${s.notes?`Notes: ${s.notes}\n`:""}\n`);
    m+=`## LLD (${d.lld.filter(l=>l.s==="done").length}/${d.lld.length})\n`;d.lld.forEach(l=>m+=`### ${l.n} — ${l.s}\n${l.patterns}\n${l.notes?`Notes: ${l.notes}\n`:""}\n`);
    m+=`## Concepts\n`;Object.entries(d.concepts).forEach(([k,its])=>{m+=`### ${k}\n`;its.forEach(i=>m+=`- [${i.c?"x":i.s?"~":" "}] ${i.n}\n`);m+="\n"});
    m+=`## STAR\n`;d.star.forEach(s=>m+=`### ${s.lp}\n${s.s||"_Not written_"}\n\n`);
    m+=`## Mocks (${d.mocks.length})\n`;d.mocks.forEach(m2=>m+=`- ${m2.date} ${m2.type} ${m2.rating}/5 ${m2.feedback||""}\n`);
    m+=`## Applications\n`;d.apps.forEach(a=>m+=`- ${a.company} | ${a.role} | ${a.status} | ${a.notes||""}\n`);
    m+=`\n## Notes\n`;d.notes.forEach(n=>m+=`### ${n.date} [${n.tag}] ${n.title||""}\n${n.body}\n\n`);
    m+=`## Logs\n|Date|Hrs|Topic|Takeaway|\n|-|-|-|-|\n`;d.logs.forEach(l=>m+=`|${l.date}|${l.hours}|${l.topic||""}|${l.takeaway||""}|\n`);
    return m;};
  const copy=t=>navigator.clipboard.writeText(t).catch(()=>{});
  return<div><C title="⇧ Export"><div style={{fontSize:10,color:"#8b949e",marginBottom:8}}>Markdown → Obsidian/Notion/GitHub | JSON → Full backup</div><div style={{display:"flex",gap:4}}><button onClick={()=>copy(gen())} style={{...X.btn,background:"#58a6ff"}}>📋 Markdown</button><button onClick={()=>copy(JSON.stringify(d,null,2))} style={{...X.btn,background:"#3fb950"}}>📋 JSON</button></div></C>
    <C title="Obsidian Setup"><div style={{fontSize:10,color:"#8b949e",lineHeight:1.7}}>1. Create: Interview-Prep/ in vault<br/>2. Paste markdown → progress.md<br/>3. Tags: #dsa #system-design #lld #genai #aws<br/>4. Push vault to private GitHub repo<br/><span style={{color:"#58a6ff"}}>💡 Export weekly → git commit → full history</span></div></C>
  </div>;
}
