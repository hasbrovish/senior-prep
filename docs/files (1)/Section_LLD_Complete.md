# LLD (Low Level Design) Complete

## Approach Framework

1. **Clarify requirements** — Functional + non-functional. Don't assume.
2. **Identify core entities** — Nouns in the problem become classes.
3. **Define relationships** — Has-a, is-a, uses.
4. **Apply SOLID principles** — Single Responsibility, Open-Closed, Liskov, Interface Segregation, Dependency Inversion.
5. **Choose design patterns** — Strategy, Factory, Observer, State, etc.
6. **Write code** — Clean, extensible, testable.

---

## Problem 1: Parking Lot

### Entities
- ParkingLot (floors, entry/exit points)
- ParkingFloor (spots)
- ParkingSpot (type: compact/regular/large, status: free/occupied)
- Vehicle (type: motorcycle/car/bus, licensePlate)
- Ticket (entryTime, spot, vehicle)
- Payment (amount, method)

### Key Design Decisions
- **Strategy Pattern** for pricing: HourlyPricing, FlatRatePricing, WeekendPricing. Swap without changing core logic.
- **Factory Pattern** for spot allocation: allocate by vehicle type.
- **Observer Pattern** for display boards: spot availability updates notify all display boards.

### SOLID Application
- **SRP:** ParkingSpot only manages its state. PricingStrategy only calculates cost.
- **OCP:** New vehicle type = new VehicleType enum + new allocation rule. No existing code changes.
- **DIP:** ParkingLot depends on SpotAllocationStrategy interface, not concrete allocation.

---

## Problem 2: Elevator System

### Entities
- Building, Elevator, Floor, Request (floor, direction)
- ElevatorController (scheduling algorithm)

### Key Design Decisions
- **State Pattern** for elevator: Idle, MovingUp, MovingDown, DoorOpen. Each state defines valid transitions.
- **Strategy Pattern** for scheduling: SCAN (elevator continues in one direction), LOOK (reverses when no more requests ahead), ShortestSeekFirst.
- GSTN parallel: Similar to our Golang FSM — states in config, transitions validated at compile/runtime.

### Concurrency
Multiple elevators = multiple threads. Request queue is shared → ConcurrentLinkedQueue or BlockingQueue. Each elevator runs its own loop, picks requests from queue.

---

## Problem 3: Chess Game

### Entities
- Board (8x8 grid of Cells), Cell (row, col, Piece)
- Piece (abstract): King, Queen, Rook, Bishop, Knight, Pawn
- Player (white/black), Move (from, to, piece)
- Game (board, players, turn, status)

### Key Design Decisions
- **Template Method** in Piece: `isValidMove()` defined per piece type, but all share `move()` template (validate → execute → check game state).
- **Command Pattern** for moves: MoveCommand stores before/after state → enables undo.
- Each Piece subclass implements `getPossibleMoves(Board board)` — polymorphism.

---

## Problem 4: Rate Limiter (Built at GSTN)

### Entities
- RateLimiter (interface), TokenBucketLimiter, SlidingWindowLimiter
- RateLimitConfig (maxRequests, windowSize, burstAllowed)
- RateLimitStore (interface): InMemoryStore, RedisStore

### Key Design Decisions
- **Strategy Pattern**: Different algorithms (token bucket, sliding window) behind same interface.
- **DIP**: RateLimiter depends on RateLimitStore interface. Swap InMemory (dev) for Redis (prod) without changing limiter logic.
- **Decorator Pattern**: `LoggingRateLimiter` wraps any `RateLimiter` to add logging without modifying core.

### GSTN Implementation
```java
public interface RateLimiter {
    boolean allowRequest(String clientId);
}

public class SlidingWindowRateLimiter implements RateLimiter {
    private final RateLimitStore store;
    private final RateLimitConfig config;

    public boolean allowRequest(String clientId) {
        long currentWindow = System.currentTimeMillis() / config.windowMs();
        long currentCount = store.incrementAndGet(clientId, currentWindow);
        long prevCount = store.getCount(clientId, currentWindow - 1);
        double overlap = 1.0 - (System.currentTimeMillis() % config.windowMs()) / (double) config.windowMs();
        double weighted = prevCount * overlap + currentCount;
        return weighted <= config.maxRequests();
    }
}
```

---

## Problem 5: Notification Service (Built at GSTN)

### Entities
- Notification, NotificationChannel (interface): SMSChannel, EmailChannel, PushChannel
- NotificationTemplate, UserPreference
- NotificationQueue, DeliveryTracker

### Patterns Used
- **Strategy** for channels: same interface, different delivery mechanism.
- **Observer** for delivery tracking: channels notify DeliveryTracker on success/failure.
- **Builder** for NotificationBuilder: complex object with many optional fields.
- **Factory Method** for channel selection based on notification type + user preference.

---

## Problem 6: Cache (LRU)

### Implementation
```java
public class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> map;
    private final DoublyLinkedList<K, V> list;

    public V get(K key) {
        Node<K, V> node = map.get(key);
        if (node == null) return null;
        list.moveToHead(node);
        return node.value;
    }

    public void put(K key, V value) {
        if (map.containsKey(key)) {
            Node<K, V> node = map.get(key);
            node.value = value;
            list.moveToHead(node);
        } else {
            if (map.size() >= capacity) {
                Node<K, V> tail = list.removeTail();
                map.remove(tail.key);
            }
            Node<K, V> newNode = new Node<>(key, value);
            list.addToHead(newNode);
            map.put(key, newNode);
        }
    }
}
```
O(1) get and put via HashMap + DoublyLinkedList combination.

---

## SOLID Principles Quick Reference

| Principle | Meaning | GSTN Example |
|-----------|---------|--------------|
| **S**ingle Responsibility | One class, one reason to change | FilingValidator only validates. FilingRepository only persists. |
| **O**pen-Closed | Open for extension, closed for modification | New tax return type = new validator class, not editing existing |
| **L**iskov Substitution | Subtypes must be substitutable for base types | Any RateLimiter implementation works where RateLimiter is expected |
| **I**nterface Segregation | No client forced to depend on methods it doesn't use | Separate ReadRepository and WriteRepository interfaces |
| **D**ependency Inversion | Depend on abstractions, not concretions | Service depends on CacheStore interface, not Redis directly |

---

## Design Patterns Quick Reference

| Pattern | When to Use | GSTN Example |
|---------|-------------|--------------|
| Strategy | Multiple algorithms, swap at runtime | Pricing, rate limiting, caching strategy |
| Factory | Object creation logic varies | Filing validator per return type |
| Observer | One-to-many notification | Cache invalidation via Kafka events |
| State | Object behavior changes with state | Filing lifecycle (Draft→Submitted→Validated) |
| Builder | Complex object construction | NotificationBuilder, QueryBuilder |
| Decorator | Add behavior without modifying class | LoggingRateLimiter wrapping SlidingWindowRateLimiter |
| Template Method | Common algorithm, varying steps | Piece.move() in chess, AbstractValidator.validate() |
| Command | Encapsulate request as object | Undo/redo, audit logging |
| Singleton | One instance globally | ConfigManager, ConnectionPool (use sparingly) |
