# BATTLE PLAN PART 2: Templates & Deep Dives

---

## System Design Template: WhatsApp/Chat System

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHAT SYSTEM DESIGN                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  REQUIREMENTS                                                   │
│  ├── 1:1 messaging                                             │
│  ├── Group chat (up to 256 members)                           │
│  ├── Online status                                             │
│  ├── Read receipts                                             │
│  ├── Media sharing                                             │
│  └── Message history                                           │
│                                                                 │
│  SCALE                                                          │
│  ├── 2B users, 500M DAU                                       │
│  ├── 65B messages/day                                         │
│  └── Average message size: 100 bytes                          │
│                                                                 │
│  ARCHITECTURE                                                   │
│                                                                 │
│  ┌──────────┐         ┌─────────────────────────────┐          │
│  │  Client  │◀───────▶│     WebSocket Gateway       │          │
│  └──────────┘         └────────────┬────────────────┘          │
│                                    │                            │
│              ┌─────────────────────┼─────────────────────┐      │
│              ▼                     ▼                     ▼      │
│       ┌──────────┐          ┌──────────┐          ┌──────────┐ │
│       │  Chat    │          │ Presence │          │  Group   │ │
│       │ Service  │          │ Service  │          │ Service  │ │
│       └────┬─────┘          └────┬─────┘          └────┬─────┘ │
│            │                     │                     │        │
│            ▼                     ▼                     ▼        │
│       ┌──────────┐          ┌──────────┐          ┌──────────┐ │
│       │Cassandra │          │  Redis   │          │PostgreSQL│ │
│       │(Messages)│          │ (Status) │          │ (Groups) │ │
│       └──────────┘          └──────────┘          └──────────┘ │
│                                                                 │
│  MESSAGE DELIVERY FLOW                                          │
│  1. User A sends message to User B                             │
│  2. Message stored in Cassandra                                │
│  3. If B is online: Push via WebSocket                        │
│  4. If B is offline: Store in queue + Push notification       │
│  5. When B comes online: Sync undelivered messages            │
│                                                                 │
│  DATA MODEL (Cassandra)                                         │
│  messages:                                                      │
│  ├── message_id: TIMEUUID                                      │
│  ├── conversation_id: UUID (partition key)                     │
│  ├── sender_id: UUID                                           │
│  ├── content: TEXT                                             │
│  ├── type: ENUM (text, image, video, audio)                   │
│  ├── status: ENUM (sent, delivered, read)                     │
│  └── created_at: TIMESTAMP (clustering key DESC)              │
│                                                                 │
│  WEBSOCKET CONNECTION MANAGEMENT (Redis)                        │
│  Key: user:{id}:connections                                    │
│  Value: Set of {gateway_id, connection_id}                     │
│                                                                 │
│  To send message to user:                                      │
│  1. Lookup user's connections                                  │
│  2. For each connection, route to gateway                      │
│  3. Gateway pushes to WebSocket                                │
└─────────────────────────────────────────────────────────────────┘
```

## System Design Template: Uber/Ride Sharing

```
┌─────────────────────────────────────────────────────────────────┐
│                   RIDE SHARING SYSTEM DESIGN                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  REQUIREMENTS                                                   │
│  ├── Real-time driver location tracking                       │
│  ├── Ride matching (rider ↔ driver)                           │
│  ├── ETA calculation                                          │
│  ├── Fare estimation & payment                                │
│  └── Trip history                                              │
│                                                                 │
│  SCALE                                                          │
│  ├── 500K concurrent drivers                                  │
│  ├── Location updates: 1M/sec (every 4 seconds)              │
│  ├── 20M rides/day                                            │
│  └── <5 sec to find driver                                    │
│                                                                 │
│  LOCATION TRACKING                                              │
│  QuadTree / Geohash for spatial indexing                       │
│                                                                 │
│  Redis GeoSpatial:                                              │
│  GEOADD drivers {longitude} {latitude} {driver_id}            │
│  GEORADIUS drivers {lng} {lat} 5 km                           │
│                                                                 │
│  Alternative: S2 Geometry (Google's approach)                  │
│  - Divide earth into cells at different levels                │
│  - Query nearby cells for drivers                              │
│                                                                 │
│  MATCHING ALGORITHM                                             │
│  1. Rider requests ride                                        │
│  2. Find drivers within radius (expand if needed)              │
│  3. Score drivers:                                             │
│     - Distance to rider                                        │
│     - Driver rating                                            │
│     - ETA                                                      │
│     - Supply/demand in area                                    │
│  4. Send request to top N drivers                              │
│  5. First to accept wins                                       │
│                                                                 │
│  ETA CALCULATION                                                │
│  ├── Real-time traffic data                                   │
│  ├── Historical patterns                                       │
│  ├── Road network graph (Dijkstra/A*)                         │
│  └── ML model for prediction                                   │
│                                                                 │
│  SURGE PRICING                                                  │
│  ├── Calculate supply/demand ratio per zone                   │
│  ├── Dynamic multiplier (1.0x - 3.0x)                        │
│  ├── Update every few minutes                                  │
│  └── Show surge before booking                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# LLD TEMPLATES IN JAVA

## LLD: Parking Lot System

```java
// ==================== ENUMS ====================
enum VehicleType { MOTORCYCLE, CAR, BUS }
enum SpotType { MOTORCYCLE, COMPACT, LARGE }
enum TicketStatus { ACTIVE, PAID, LOST }

// ==================== VEHICLE ====================
abstract class Vehicle {
    private String licensePlate;
    private VehicleType type;
    
    public Vehicle(String licensePlate) {
        this.licensePlate = licensePlate;
    }
    
    public abstract VehicleType getType();
    public String getLicensePlate() { return licensePlate; }
}

class Car extends Vehicle {
    public Car(String licensePlate) { super(licensePlate); }
    public VehicleType getType() { return VehicleType.CAR; }
}

class Motorcycle extends Vehicle {
    public Motorcycle(String licensePlate) { super(licensePlate); }
    public VehicleType getType() { return VehicleType.MOTORCYCLE; }
}

class Bus extends Vehicle {
    public Bus(String licensePlate) { super(licensePlate); }
    public VehicleType getType() { return VehicleType.BUS; }
}

// ==================== PARKING SPOT ====================
class ParkingSpot {
    private String spotId;
    private SpotType type;
    private boolean isAvailable;
    private Vehicle vehicle;
    
    public ParkingSpot(String spotId, SpotType type) {
        this.spotId = spotId;
        this.type = type;
        this.isAvailable = true;
    }
    
    public boolean canFitVehicle(Vehicle vehicle) {
        if (!isAvailable) return false;
        switch (vehicle.getType()) {
            case MOTORCYCLE: return true;
            case CAR: return type == SpotType.COMPACT || type == SpotType.LARGE;
            case BUS: return type == SpotType.LARGE;
            default: return false;
        }
    }
    
    public void parkVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
        this.isAvailable = false;
    }
    
    public void removeVehicle() {
        this.vehicle = null;
        this.isAvailable = true;
    }
    
    // Getters
    public String getSpotId() { return spotId; }
    public SpotType getType() { return type; }
    public boolean isAvailable() { return isAvailable; }
    public Vehicle getVehicle() { return vehicle; }
}

// ==================== PARKING FLOOR ====================
class ParkingFloor {
    private String floorId;
    private Map<SpotType, List<ParkingSpot>> spotsByType;
    
    public ParkingFloor(String floorId) {
        this.floorId = floorId;
        this.spotsByType = new HashMap<>();
        for (SpotType type : SpotType.values()) {
            spotsByType.put(type, new ArrayList<>());
        }
    }
    
    public void addSpot(ParkingSpot spot) {
        spotsByType.get(spot.getType()).add(spot);
    }
    
    public ParkingSpot findAvailableSpot(VehicleType vehicleType) {
        List<SpotType> suitableTypes = getSuitableSpotTypes(vehicleType);
        for (SpotType type : suitableTypes) {
            for (ParkingSpot spot : spotsByType.get(type)) {
                if (spot.isAvailable()) {
                    return spot;
                }
            }
        }
        return null;
    }
    
    private List<SpotType> getSuitableSpotTypes(VehicleType vehicleType) {
        switch (vehicleType) {
            case MOTORCYCLE: return Arrays.asList(SpotType.MOTORCYCLE, SpotType.COMPACT, SpotType.LARGE);
            case CAR: return Arrays.asList(SpotType.COMPACT, SpotType.LARGE);
            case BUS: return Arrays.asList(SpotType.LARGE);
            default: return Collections.emptyList();
        }
    }
}

// ==================== TICKET ====================
class Ticket {
    private String ticketId;
    private Vehicle vehicle;
    private ParkingSpot spot;
    private LocalDateTime entryTime;
    private LocalDateTime exitTime;
    private TicketStatus status;
    
    public Ticket(String ticketId, Vehicle vehicle, ParkingSpot spot) {
        this.ticketId = ticketId;
        this.vehicle = vehicle;
        this.spot = spot;
        this.entryTime = LocalDateTime.now();
        this.status = TicketStatus.ACTIVE;
    }
    
    public void markPaid() {
        this.exitTime = LocalDateTime.now();
        this.status = TicketStatus.PAID;
    }
    
    // Getters
    public String getTicketId() { return ticketId; }
    public Vehicle getVehicle() { return vehicle; }
    public ParkingSpot getSpot() { return spot; }
    public LocalDateTime getEntryTime() { return entryTime; }
    public TicketStatus getStatus() { return status; }
}

// ==================== FEE CALCULATOR (Strategy Pattern) ====================
interface FeeCalculationStrategy {
    double calculateFee(Ticket ticket);
}

class HourlyFeeStrategy implements FeeCalculationStrategy {
    private Map<VehicleType, Double> hourlyRates;
    
    public HourlyFeeStrategy() {
        hourlyRates = new HashMap<>();
        hourlyRates.put(VehicleType.MOTORCYCLE, 10.0);
        hourlyRates.put(VehicleType.CAR, 20.0);
        hourlyRates.put(VehicleType.BUS, 50.0);
    }
    
    public double calculateFee(Ticket ticket) {
        long hours = ChronoUnit.HOURS.between(
            ticket.getEntryTime(), 
            LocalDateTime.now()
        );
        hours = Math.max(1, hours); // Minimum 1 hour
        return hours * hourlyRates.get(ticket.getVehicle().getType());
    }
}

// ==================== PAYMENT (Strategy Pattern) ====================
interface PaymentStrategy {
    boolean processPayment(double amount);
}

class CashPayment implements PaymentStrategy {
    public boolean processPayment(double amount) {
        System.out.println("Processing cash payment: " + amount);
        return true;
    }
}

class CardPayment implements PaymentStrategy {
    private String cardNumber;
    
    public CardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
    }
    
    public boolean processPayment(double amount) {
        System.out.println("Processing card payment: " + amount);
        return true;
    }
}

// ==================== PARKING LOT (Singleton) ====================
class ParkingLot {
    private static ParkingLot instance;
    private String name;
    private List<ParkingFloor> floors;
    private Map<String, Ticket> activeTickets;
    private FeeCalculationStrategy feeStrategy;
    private AtomicInteger ticketCounter;
    
    private ParkingLot() {
        this.floors = new ArrayList<>();
        this.activeTickets = new ConcurrentHashMap<>();
        this.feeStrategy = new HourlyFeeStrategy();
        this.ticketCounter = new AtomicInteger(0);
    }
    
    public static synchronized ParkingLot getInstance() {
        if (instance == null) {
            instance = new ParkingLot();
        }
        return instance;
    }
    
    public void addFloor(ParkingFloor floor) {
        floors.add(floor);
    }
    
    public Ticket issueTicket(Vehicle vehicle) {
        ParkingSpot spot = findAvailableSpot(vehicle.getType());
        if (spot == null) {
            throw new RuntimeException("No available spot for " + vehicle.getType());
        }
        
        spot.parkVehicle(vehicle);
        String ticketId = "T" + ticketCounter.incrementAndGet();
        Ticket ticket = new Ticket(ticketId, vehicle, spot);
        activeTickets.put(ticketId, ticket);
        
        return ticket;
    }
    
    public double processExit(String ticketId, PaymentStrategy paymentStrategy) {
        Ticket ticket = activeTickets.get(ticketId);
        if (ticket == null) {
            throw new RuntimeException("Invalid ticket");
        }
        
        double fee = feeStrategy.calculateFee(ticket);
        if (paymentStrategy.processPayment(fee)) {
            ticket.markPaid();
            ticket.getSpot().removeVehicle();
            activeTickets.remove(ticketId);
            return fee;
        }
        throw new RuntimeException("Payment failed");
    }
    
    private ParkingSpot findAvailableSpot(VehicleType type) {
        for (ParkingFloor floor : floors) {
            ParkingSpot spot = floor.findAvailableSpot(type);
            if (spot != null) return spot;
        }
        return null;
    }
}
```

## LLD: LRU Cache

```java
class LRUCache {
    private int capacity;
    private Map<Integer, Node> cache;
    private Node head, tail;
    
    class Node {
        int key, value;
        Node prev, next;
        
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        
        // Dummy head and tail for easier operations
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    
    public int get(int key) {
        if (!cache.containsKey(key)) {
            return -1;
        }
        
        Node node = cache.get(key);
        // Move to front (most recently used)
        removeNode(node);
        addToFront(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            // Update existing
            Node node = cache.get(key);
            node.value = value;
            removeNode(node);
            addToFront(node);
        } else {
            // Check capacity
            if (cache.size() >= capacity) {
                // Remove LRU (from tail)
                Node lru = tail.prev;
                removeNode(lru);
                cache.remove(lru.key);
            }
            // Add new
            Node newNode = new Node(key, value);
            cache.put(key, newNode);
            addToFront(newNode);
        }
    }
    
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}
```

## LLD: Rate Limiter

```java
// Token Bucket Implementation
class TokenBucketRateLimiter {
    private final int capacity;
    private final int refillRate; // tokens per second
    private double tokens;
    private long lastRefillTime;
    
    public TokenBucketRateLimiter(int capacity, int refillRate) {
        this.capacity = capacity;
        this.refillRate = refillRate;
        this.tokens = capacity;
        this.lastRefillTime = System.currentTimeMillis();
    }
    
    public synchronized boolean allowRequest() {
        refill();
        if (tokens >= 1) {
            tokens -= 1;
            return true;
        }
        return false;
    }
    
    private void refill() {
        long now = System.currentTimeMillis();
        double elapsed = (now - lastRefillTime) / 1000.0;
        tokens = Math.min(capacity, tokens + elapsed * refillRate);
        lastRefillTime = now;
    }
}

// Sliding Window Counter Implementation
class SlidingWindowRateLimiter {
    private final int windowSizeMs;
    private final int maxRequests;
    private final Map<String, Deque<Long>> userRequests;
    
    public SlidingWindowRateLimiter(int windowSizeSeconds, int maxRequests) {
        this.windowSizeMs = windowSizeSeconds * 1000;
        this.maxRequests = maxRequests;
        this.userRequests = new ConcurrentHashMap<>();
    }
    
    public synchronized boolean allowRequest(String userId) {
        long now = System.currentTimeMillis();
        long windowStart = now - windowSizeMs;
        
        Deque<Long> requests = userRequests.computeIfAbsent(
            userId, k -> new LinkedList<>()
        );
        
        // Remove old requests outside window
        while (!requests.isEmpty() && requests.peekFirst() < windowStart) {
            requests.pollFirst();
        }
        
        if (requests.size() < maxRequests) {
            requests.addLast(now);
            return true;
        }
        return false;
    }
}

// Distributed Rate Limiter with Redis (Pseudo-code)
class RedisRateLimiter {
    private RedisTemplate<String, String> redis;
    private int windowSize;
    private int maxRequests;
    
    public boolean allowRequest(String userId) {
        String key = "rate_limit:" + userId;
        long now = System.currentTimeMillis();
        
        // Lua script for atomic operation
        String script = 
            "local key = KEYS[1] " +
            "local now = tonumber(ARGV[1]) " +
            "local window = tonumber(ARGV[2]) " +
            "local limit = tonumber(ARGV[3]) " +
            "redis.call('ZREMRANGEBYSCORE', key, 0, now - window) " +
            "local count = redis.call('ZCARD', key) " +
            "if count < limit then " +
            "  redis.call('ZADD', key, now, now) " +
            "  redis.call('EXPIRE', key, window / 1000) " +
            "  return 1 " +
            "end " +
            "return 0";
        
        Long result = redis.execute(/* script with args */);
        return result == 1;
    }
}
```

---

# ONLINE ASSESSMENT PATTERNS

## Most Common OA Problems by Company

### Amazon OA Most Asked
```
1. Merge K Sorted Lists (LeetCode 23)
2. LRU Cache (LeetCode 146)
3. Number of Islands (LeetCode 200)
4. Trapping Rain Water (LeetCode 42)
5. Two Sum (LeetCode 1)
6. Longest Substring Without Repeating (LeetCode 3)
7. Meeting Rooms II (LeetCode 253)
8. Product of Array Except Self (LeetCode 238)
9. Word Ladder (LeetCode 127)
10. Min Cost to Connect All Points (LeetCode 1584)
```

### Google OA Most Asked
```
1. Longest Increasing Path in Matrix (LeetCode 329)
2. Word Ladder II (LeetCode 126)
3. Minimum Window Substring (LeetCode 76)
4. Alien Dictionary (LeetCode 269)
5. Regular Expression Matching (LeetCode 10)
6. Serialize and Deserialize Binary Tree (LeetCode 297)
7. Word Search II (LeetCode 212)
8. Basic Calculator III (LeetCode 772)
9. Find Median from Data Stream (LeetCode 295)
10. Shortest Path in Binary Matrix (LeetCode 1091)
```

### Uber OA Most Asked
```
1. Design Hit Counter (LeetCode 362)
2. LRU Cache (LeetCode 146)
3. Meeting Scheduler (LeetCode 1229)
4. Task Scheduler (LeetCode 621)
5. Time Based Key-Value Store (LeetCode 981)
6. Course Schedule II (LeetCode 210)
7. Network Delay Time (LeetCode 743)
8. Word Ladder (LeetCode 127)
9. Find K Closest Elements (LeetCode 658)
10. Maximum Profit in Job Scheduling (LeetCode 1235)
```

### Atlassian OA Most Asked
```
1. Design In-Memory File System (LeetCode 588)
2. Find All Anagrams in a String (LeetCode 438)
3. Task Scheduler (LeetCode 621)
4. Design Search Autocomplete (LeetCode 642)
5. Implement Trie (LeetCode 208)
6. Binary Tree Level Order Traversal (LeetCode 102)
7. Merge Intervals (LeetCode 56)
8. Valid Parentheses (LeetCode 20)
9. Group Anagrams (LeetCode 49)
10. Time Based Key-Value Store (LeetCode 981)
```

### Indian Startups (Swiggy/Zomato/Flipkart) Most Asked
```
1. Number of Islands (LeetCode 200)
2. Merge Intervals (LeetCode 56)
3. LRU Cache (LeetCode 146)
4. Longest Substring Without Repeating (LeetCode 3)
5. Two Sum (LeetCode 1)
6. 3Sum (LeetCode 15)
7. Course Schedule (LeetCode 207)
8. Coin Change (LeetCode 322)
9. Binary Tree Level Order (LeetCode 102)
10. Rotate Array (LeetCode 189)
```

---

# GENAI DEEP DIVE TOPICS

## Vector Database Comparison

```
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Feature         │ Pinecone    │ Weaviate    │ Qdrant      │ pgvector    │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Type            │ Managed     │ Open Source │ Open Source │ Extension   │
│ Hosting         │ Cloud only  │ Cloud/Self  │ Cloud/Self  │ PostgreSQL  │
│ Hybrid Search   │ Yes         │ Yes         │ Yes         │ Limited     │
│ Filtering       │ Metadata    │ Rich        │ Rich        │ SQL         │
│ Scale           │ Excellent   │ Good        │ Good        │ Moderate    │
│ Free Tier       │ Yes         │ Yes         │ Yes         │ Yes         │
│ Best For        │ Quick Start │ Flexibility │ Performance │ Existing PG │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

## RAG Optimization Techniques

```
CHUNKING STRATEGIES
├── Fixed Size (Simple)
│   └── 500-1000 tokens per chunk
├── Sentence-Based
│   └── Natural boundaries, better context
├── Semantic Chunking
│   └── Based on topic shifts
└── Hierarchical
    └── Document → Section → Paragraph

RETRIEVAL IMPROVEMENTS
├── Hybrid Search
│   ├── Dense (embedding similarity)
│   └── Sparse (BM25 keyword)
├── Re-ranking
│   └── Cross-encoder for better relevance
├── Query Expansion
│   └── HyDE: Hypothetical Document Embeddings
└── Multi-Query
    └── Generate multiple search queries

GENERATION IMPROVEMENTS
├── Contextual Compression
│   └── Extract relevant parts only
├── Self-RAG
│   └── Retrieve-when-needed approach
└── Chain-of-Thought
    └── Step by step reasoning
```

## MCP Protocol Essentials

```
MCP COMPONENTS
├── Host (Client)
│   └── The LLM application (Claude, custom)
├── Server
│   └── Your tool implementation
├── Resources
│   └── Data exposed to LLM
├── Tools
│   └── Actions LLM can invoke
└── Prompts
    └── Pre-defined templates

MCP SERVER EXAMPLE (Python)
```python
from mcp import Server, Resource, Tool

server = Server("database-tool")

@server.resource("schema://{table_name}")
async def get_schema(table_name: str) -> str:
    """Expose table schema as a resource"""
    return get_table_schema(table_name)

@server.tool("query")
async def execute_query(sql: str) -> dict:
    """Execute SQL query"""
    return run_query(sql)

@server.tool("list_tables")
async def list_tables() -> list:
    """List all available tables"""
    return get_all_tables()

if __name__ == "__main__":
    server.run()
```

## AWS Bedrock Quick Reference

```
BEDROCK MODELS
├── Anthropic Claude (claude-3-sonnet, claude-3-haiku)
├── Amazon Titan (text, embeddings)
├── Meta Llama
├── Mistral
└── Stable Diffusion (images)

BEDROCK API EXAMPLE (Python)
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def invoke_claude(prompt):
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    return json.loads(response['body'].read())

KNOWLEDGE BASE SETUP
1. Create S3 bucket → Upload documents
2. Bedrock Console → Create Knowledge Base
3. Select embedding model (Titan Embeddings)
4. Choose vector store (OpenSearch/Pinecone)
5. Sync documents
6. Query via API:

def query_kb(kb_id, query):
    response = bedrock_agent.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kb_id,
                'modelArn': 'arn:aws:bedrock:...:claude-3-sonnet'
            }
        }
    )
    return response['output']['text']
```

---

# WEEKLY TRACKER TEMPLATES

## Daily Log Template

```
DATE: _______________
DAY: ___ / 90

MORNING SESSION (4:30 - 6:00 AM)
├── DSA Topic: _________________________
├── Problems Attempted: ____ / 3
├── Problems Solved: ____ / 3
├── Problem 1: _________________ [Easy/Med/Hard] ⬜ 
├── Problem 2: _________________ [Easy/Med/Hard] ⬜
├── Problem 3: _________________ [Easy/Med/Hard] ⬜
└── Key Pattern Learned: ________________

OFFICE SESSION (10:00 AM - 5:00 PM)
├── GenAI Topic: _________________________
├── Hands-on Completed: ⬜
├── Notes: _______________________________
└── Blockers: ____________________________

EVENING SESSION (5:30 - 7:30 PM)
├── System Design Topic: _________________
├── Design Completed: ⬜
├── Key Components: ______________________
└── Trade-offs Learned: __________________

NIGHT SESSION (8:00 - 9:00 PM)
├── LLD/Mock Topic: ______________________
├── Code Written: ⬜
├── Mock Interview: ⬜ (If applicable)
└── Feedback: ____________________________

DAILY SUMMARY
├── Total Hours: ____ / 8
├── Energy Level: ____/10
├── Confidence: ____/10
└── Tomorrow's Focus: ___________________
```

## Weekly Review Template

```
WEEK: ____ / 12
DATES: _____________ to _____________

DSA PROGRESS
├── Problems Solved: ____ / 25
├── Topics Covered: ___________________
├── Weak Areas Identified: ____________
├── Contest Participated: ⬜
└── Contest Score: ____________________

SYSTEM DESIGN PROGRESS
├── Designs Practiced: ____ / 5
├── New Patterns Learned: _____________
├── Mock SD Interviews: ____ / 2
└── Confidence Level: ____/10

LLD PROGRESS
├── Problems Completed: ____ / 3
├── Code Quality: ____/10
└── Patterns Mastered: ________________

GENAI PROGRESS
├── Topics Covered: ___________________
├── Hands-on Projects: ________________
├── Office Work Status: _______________
└── Blockers: _________________________

OVERALL METRICS
├── Total Hours Invested: ____ / 31.5
├── Schedule Adherence: ____%
├── Mock Interviews Done: ____
└── Week Rating: ____/10

KEY WINS THIS WEEK:
1. _________________________________
2. _________________________________
3. _________________________________

AREAS TO IMPROVE:
1. _________________________________
2. _________________________________

NEXT WEEK FOCUS:
_________________________________
```

---

# FINAL RESOURCES CHECKLIST

## Free Resources
- [ ] NeetCode.io (DSA patterns)
- [ ] LeetCode (Practice)
- [ ] System Design Primer (GitHub)
- [ ] ByteByteGo Newsletter
- [ ] Anthropic Documentation
- [ ] AWS Free Tier
- [ ] LangChain Documentation

## Your Subscriptions
- [ ] Programming Pathshala Renaissance
- [ ] KodeKloud (AWS, Docker, K8s)
- [ ] O'Reilly (Books)

## Books to Reference
- [ ] Designing Data-Intensive Applications
- [ ] System Design Interview (Alex Xu)
- [ ] Clean Code (Robert Martin)
- [ ] Head First Design Patterns

---

**REMEMBER:**
1. Quality over Quantity in DSA
2. Your GSTN experience is your SUPERPOWER
3. GenAI + Backend = Rare combination
4. Mock interviews from Week 4 onwards
5. Apply to companies starting Day 45

**YOU'VE GOT THIS! 🚀**
