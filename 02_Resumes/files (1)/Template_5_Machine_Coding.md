# MACHINE CODING - ANSWER TEMPLATE & EVALUATION GUIDE

## 🎯 STRONG HIRE SIGNALS (What Interviewers Score)

| Signal | Strong Hire | Hire | No Hire |
|--------|-------------|------|---------|
| **Completion** | Working code in 45-50 min | Core works | Incomplete |
| **Code Quality** | Clean, readable, modular | Reasonably organized | Messy |
| **Design** | Good OOP, clear abstractions | Some structure | No structure |
| **Edge Cases** | Handles gracefully | Handles main cases | Ignores |
| **Testing** | Tests with examples | Some testing | No testing |
| **Communication** | Talks through approach | Explains when asked | Silent |
| **Time Management** | Prioritizes well | Finishes core | Gets stuck |

---

## ⏱️ TIME MANAGEMENT (Critical!)

```
┌─────────────────────────────────────────────────────────────┐
│   60 MINUTE BREAKDOWN                                        │
├─────────────────────────────────────────────────────────────┤
│   0-5 min  │ CLARIFY: Scope, features, I/O format          │
│            │ ASK: "What's in scope? What's out?"            │
│            │ CONFIRM: Input/output examples                 │
├────────────┼────────────────────────────────────────────────┤
│   5-15 min │ DESIGN: Classes, relationships, key methods    │
│            │ DRAW: Quick class diagram on paper             │
│            │ PRIORITIZE: Which classes first?               │
├────────────┼────────────────────────────────────────────────┤
│  15-45 min │ CODE: Main functionality FIRST                 │
│            │ SKIP: Edge cases initially                     │
│            │ TALK: Explain as you write                     │
├────────────┼────────────────────────────────────────────────┤
│  45-55 min │ EDGE CASES: Add validation, error handling     │
│            │ CLEANUP: Remove debug code, add comments       │
├────────────┼────────────────────────────────────────────────┤
│  55-60 min │ TEST: Run through sample inputs                │
│            │ FIX: Any bugs found                            │
│            │ DEMO: Walkthrough for interviewer              │
└────────────┴────────────────────────────────────────────────┘
```

### ⚠️ TIME TRAPS TO AVOID

| Trap | Solution |
|------|----------|
| Overthinking design | 10 min max, then code |
| Perfect edge cases first | Core logic first |
| Debugging silently | Verbalize your thinking |
| Starting over | Fix forward |
| Fancy features | MVP first |

---

## 📝 CODE STRUCTURE TEMPLATE

```java
// STANDARD STRUCTURE FOR ANY MC PROBLEM

// 1. ENUMS (Define types/states)
enum Status { ACTIVE, INACTIVE, PENDING }
enum Type { TYPE_A, TYPE_B }

// 2. MODELS (Data classes)
class Entity {
    private final String id;
    private String name;
    private Status status;
    
    // Constructor
    // Getters (no setters if immutable)
}

// 3. EXCEPTIONS (Custom if needed)
class EntityNotFoundException extends RuntimeException {
    public EntityNotFoundException(String id) {
        super("Entity not found: " + id);
    }
}

// 4. INTERFACES (For strategies/extensibility)
interface Strategy {
    Result execute(Input input);
}

// 5. SERVICE (Business logic)
class EntityService {
    private final Map<String, Entity> store;
    
    public Entity create(String name) { }
    public Entity get(String id) { }
    public void update(String id, String name) { }
    public void delete(String id) { }
}

// 6. MAIN (Driver/Demo)
public class Main {
    public static void main(String[] args) {
        EntityService service = new EntityService();
        
        // Demo operations
        Entity e1 = service.create("test");
        System.out.println(service.get(e1.getId()));
    }
}
```

---

## 🔥 PROBLEM TEMPLATES

### 1. LRU CACHE (45 min)

```java
// KEY INSIGHT: HashMap + Doubly Linked List for O(1) operations

class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> map;
    private final Node<K, V> head, tail; // Dummy nodes
    
    class Node<K, V> {
        K key;
        V value;
        Node<K, V> prev, next;
        
        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        this.head = new Node<>(null, null);
        this.tail = new Node<>(null, null);
        head.next = tail;
        tail.prev = head;
    }
    
    public V get(K key) {
        if (!map.containsKey(key)) return null;
        Node<K, V> node = map.get(key);
        moveToHead(node);
        return node.value;
    }
    
    public void put(K key, V value) {
        if (map.containsKey(key)) {
            Node<K, V> node = map.get(key);
            node.value = value;
            moveToHead(node);
        } else {
            if (map.size() >= capacity) {
                evict();
            }
            Node<K, V> newNode = new Node<>(key, value);
            map.put(key, newNode);
            addToHead(newNode);
        }
    }
    
    private void moveToHead(Node<K, V> node) {
        removeNode(node);
        addToHead(node);
    }
    
    private void removeNode(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void addToHead(Node<K, V> node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    private void evict() {
        Node<K, V> lru = tail.prev;
        removeNode(lru);
        map.remove(lru.key);
    }
}
```

### 2. RATE LIMITER (45 min)

```java
// KEY INSIGHT: Token Bucket or Sliding Window

// SLIDING WINDOW APPROACH
class RateLimiter {
    private final int maxRequests;
    private final long windowSizeMs;
    private final Map<String, Deque<Long>> userRequests;
    
    public RateLimiter(int maxRequests, long windowSizeMs) {
        this.maxRequests = maxRequests;
        this.windowSizeMs = windowSizeMs;
        this.userRequests = new ConcurrentHashMap<>();
    }
    
    public synchronized boolean allowRequest(String userId) {
        long now = System.currentTimeMillis();
        long windowStart = now - windowSizeMs;
        
        userRequests.putIfAbsent(userId, new LinkedList<>());
        Deque<Long> requests = userRequests.get(userId);
        
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

// TOKEN BUCKET APPROACH
class TokenBucketRateLimiter {
    private final int maxTokens;
    private final double refillRate; // tokens per second
    private double currentTokens;
    private long lastRefillTime;
    
    public TokenBucketRateLimiter(int maxTokens, double refillRate) {
        this.maxTokens = maxTokens;
        this.refillRate = refillRate;
        this.currentTokens = maxTokens;
        this.lastRefillTime = System.nanoTime();
    }
    
    public synchronized boolean allowRequest() {
        refill();
        if (currentTokens >= 1) {
            currentTokens--;
            return true;
        }
        return false;
    }
    
    private void refill() {
        long now = System.nanoTime();
        double elapsedSeconds = (now - lastRefillTime) / 1e9;
        currentTokens = Math.min(maxTokens, 
                                 currentTokens + elapsedSeconds * refillRate);
        lastRefillTime = now;
    }
}
```

### 3. PARKING LOT (60 min)

```java
// ENTITIES
enum VehicleType { BIKE, CAR, TRUCK }
enum SpotType { SMALL, MEDIUM, LARGE }

class Vehicle {
    private final String licensePlate;
    private final VehicleType type;
}

class ParkingSpot {
    private final String spotId;
    private final SpotType type;
    private Vehicle parkedVehicle;
    
    public boolean isAvailable() { return parkedVehicle == null; }
    
    public boolean canFit(Vehicle vehicle) {
        return this.type.ordinal() >= vehicle.getType().ordinal();
    }
    
    public void park(Vehicle vehicle) {
        if (!canFit(vehicle)) throw new IllegalArgumentException();
        this.parkedVehicle = vehicle;
    }
    
    public void vacate() { this.parkedVehicle = null; }
}

class Floor {
    private final int floorNumber;
    private final List<ParkingSpot> spots;
    
    public ParkingSpot findAvailableSpot(Vehicle vehicle) {
        return spots.stream()
            .filter(s -> s.isAvailable() && s.canFit(vehicle))
            .findFirst()
            .orElse(null);
    }
}

class ParkingLot {
    private final List<Floor> floors;
    private final Map<String, Ticket> activeTickets;
    
    public Ticket park(Vehicle vehicle) {
        for (Floor floor : floors) {
            ParkingSpot spot = floor.findAvailableSpot(vehicle);
            if (spot != null) {
                spot.park(vehicle);
                Ticket ticket = new Ticket(vehicle, spot, LocalDateTime.now());
                activeTickets.put(ticket.getId(), ticket);
                return ticket;
            }
        }
        throw new ParkingFullException();
    }
    
    public double exit(String ticketId) {
        Ticket ticket = activeTickets.remove(ticketId);
        Duration parked = Duration.between(ticket.getEntryTime(), LocalDateTime.now());
        ticket.getSpot().vacate();
        return calculateFee(parked);
    }
}
```

### 4. SPLITWISE (60 min)

```java
// ENTITIES
class User {
    private final String id;
    private final String name;
}

enum SplitType { EQUAL, EXACT, PERCENTAGE }

// STRATEGY PATTERN for split calculation
interface SplitStrategy {
    Map<User, Double> split(double amount, List<User> users, List<Double> values);
}

class EqualSplit implements SplitStrategy {
    public Map<User, Double> split(double amount, List<User> users, List<Double> values) {
        double each = amount / users.size();
        return users.stream().collect(Collectors.toMap(u -> u, u -> each));
    }
}

class ExactSplit implements SplitStrategy {
    public Map<User, Double> split(double amount, List<User> users, List<Double> values) {
        Map<User, Double> result = new HashMap<>();
        for (int i = 0; i < users.size(); i++) {
            result.put(users.get(i), values.get(i));
        }
        return result;
    }
}

// CORE SERVICE
class ExpenseService {
    private final Map<String, Map<String, Double>> balances; // user -> (other user -> amount owed)
    
    public void addExpense(User paidBy, double amount, List<User> splitAmong, 
                          SplitStrategy strategy, List<Double> values) {
        Map<User, Double> splits = strategy.split(amount, splitAmong, values);
        
        for (Map.Entry<User, Double> entry : splits.entrySet()) {
            User user = entry.getKey();
            double share = entry.getValue();
            
            if (!user.equals(paidBy)) {
                updateBalance(user.getId(), paidBy.getId(), share);
            }
        }
    }
    
    private void updateBalance(String fromUser, String toUser, double amount) {
        balances.computeIfAbsent(fromUser, k -> new HashMap<>())
                .merge(toUser, amount, Double::sum);
    }
    
    public Map<String, Double> getBalances(String userId) {
        return balances.getOrDefault(userId, Collections.emptyMap());
    }
}
```

---

## 🔥 STRONG HIRE PHRASES

### While Clarifying:
- "Let me confirm the scope..."
- "What's the expected input size?"
- "Should I handle concurrent access?"

### While Designing:
- "I'll start with the core classes..."
- "The key data structure here is..."
- "I'm using [pattern] because..."

### While Coding:
- "I'm implementing [method] which..."
- "This handles the case where..."
- "Let me skip validation for now and add it later..."

### When Stuck:
- "Let me think about this for a second..."
- "I think the issue is..."
- "Let me try a different approach..."

### While Testing:
- "Let me trace through with this example..."
- "Edge case: what if the input is empty?"

---

## ⚠️ RED FLAGS TO AVOID

| Red Flag | Solution |
|----------|----------|
| No talking for 5+ minutes | Verbalize your thinking |
| Starting without design | Spend 5-10 min on design |
| Trying to be perfect | Get working code first |
| Ignoring edge cases entirely | Handle after core works |
| Complex code when simple works | Keep it simple |
| Not testing at all | Always demo with examples |

---

## 📝 SELF-ASSESSMENT CHECKLIST

```
□ Did I clarify requirements before coding?
□ Did I spend 5-10 min on design?
□ Is my code working for happy path?
□ Did I handle major edge cases?
□ Is my code clean and readable?
□ Did I talk through my approach?
□ Did I finish in time?
□ Did I demo with examples?
```

**Score: ___/8**

- 7-8: Strong Hire
- 5-6: Hire
- 3-4: Lean Hire
- 0-2: Need more practice
