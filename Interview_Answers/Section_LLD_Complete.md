# LLD (Low-Level Design) — Complete Interview Guide
# Java Backend Engineer | SDE-2/SDE-3 Prep
# Companies: Razorpay, CRED, Juspay, Flipkart, Amazon, Swiggy, Stripe, Google

---

## SECTION 1: The 45-Minute LLD Interview Framework

### Minute-by-Minute Structure

```
0–5 min   → Clarify Requirements
5–10 min  → Identify Entities + Relationships (talk aloud)
10–15 min → Define Core Interfaces + Class Hierarchy
15–35 min → Implement Core Classes + Key Methods
35–42 min → Handle Edge Cases + Concurrency
42–45 min → Extensibility Discussion + Trade-offs
```

### Requirements Clarification (What to Ask)
1. **Actors**: Who uses this system? (Users, Admins, etc.)
2. **Core actions**: What are the 3–5 main operations?
3. **Scale**: Single machine or distributed? (LLD = single machine, usually)
4. **Concurrency**: Multiple threads? (Almost always yes — ask explicitly)
5. **Constraints**: Any performance requirements?

### How to Identify Entities
- Nouns in the problem = Entities (classes)
- Verbs = Methods
- Adjectives describing nouns = Fields or subclasses

### Common Candidate Mistakes
- Writing code before clarifying (big red flag)
- Making everything concrete — use interfaces for extensibility
- Forgetting thread safety when concurrency is implied
- Over-engineering: 15 classes for a 45-min problem is too many
- Under-engineering: flat classes with no abstraction

---

## SECTION 2: SOLID Principles — Java Code Examples

### S — Single Responsibility Principle
> A class should have only one reason to change.

**BAD:**
```java
public class UserService {
    public User getUser(int id) { /* DB logic */ }
    public void sendWelcomeEmail(User user) { /* email logic */ }
    public String generateReport(User user) { /* report logic */ }
}
// Problem: 3 reasons to change — DB, email service, reporting format
```

**GOOD:**
```java
public class UserRepository {
    public User findById(int id) { /* DB logic only */ }
}
public class EmailService {
    public void sendWelcomeEmail(User user) { /* email logic only */ }
}
public class UserReportGenerator {
    public String generate(User user) { /* report logic only */ }
}
```

---

### O — Open/Closed Principle
> Open for extension, closed for modification.

**BAD:**
```java
public class PaymentProcessor {
    public void process(String type, double amount) {
        if (type.equals("CREDIT")) { /* credit logic */ }
        else if (type.equals("UPI")) { /* UPI logic */ }
        // Adding new payment = modify this class (BAD)
    }
}
```

**GOOD:**
```java
public interface PaymentStrategy {
    void process(double amount);
}
public class CreditCardPayment implements PaymentStrategy {
    public void process(double amount) { /* credit logic */ }
}
public class UpiPayment implements PaymentStrategy {
    public void process(double amount) { /* UPI logic */ }
}
public class PaymentProcessor {
    private final PaymentStrategy strategy;
    public PaymentProcessor(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    public void process(double amount) { strategy.process(amount); }
    // Adding new payment = new class, no modification here
}
```

**GSTN context:** `CaseCustomizerFactory` selects the right `ICaseCustomizer` implementation — open/closed in action.

---

### L — Liskov Substitution Principle
> Subclasses must be substitutable for their base class.

**BAD:**
```java
public class Rectangle {
    protected int width, height;
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int area() { return width * height; }
}
public class Square extends Rectangle {
    @Override
    public void setWidth(int w) { this.width = w; this.height = w; } // Breaks LSP!
    @Override
    public void setHeight(int h) { this.width = h; this.height = h; } // Breaks LSP!
}
// Code that works for Rectangle breaks when Square is substituted
```

**GOOD:**
```java
public interface Shape {
    int area();
}
public class Rectangle implements Shape {
    private int width, height;
    public Rectangle(int w, int h) { this.width = w; this.height = h; }
    public int area() { return width * height; }
}
public class Square implements Shape {
    private int side;
    public Square(int s) { this.side = s; }
    public int area() { return side * side; }
}
```

---

### I — Interface Segregation Principle
> Don't force clients to implement interfaces they don't use.

**BAD:**
```java
public interface Worker {
    void work();
    void eat();
    void sleep();
}
public class Robot implements Worker {
    public void work() { /* ok */ }
    public void eat() { throw new UnsupportedOperationException(); } // Robot doesn't eat!
    public void sleep() { throw new UnsupportedOperationException(); }
}
```

**GOOD:**
```java
public interface Workable { void work(); }
public interface Eatable { void eat(); }
public interface Sleepable { void sleep(); }

public class Human implements Workable, Eatable, Sleepable {
    public void work() { /* ok */ }
    public void eat() { /* ok */ }
    public void sleep() { /* ok */ }
}
public class Robot implements Workable {
    public void work() { /* ok */ }
}
```

---

### D — Dependency Inversion Principle
> Depend on abstractions, not concretions.

**BAD:**
```java
public class OrderService {
    private MySQLOrderRepository repo = new MySQLOrderRepository(); // Hardcoded!
    public void placeOrder(Order order) { repo.save(order); }
}
```

**GOOD:**
```java
public interface OrderRepository {
    void save(Order order);
    Order findById(long id);
}
public class MySQLOrderRepository implements OrderRepository { /* MySQL impl */ }
public class MongoOrderRepository implements OrderRepository { /* Mongo impl */ }

public class OrderService {
    private final OrderRepository repo; // Depends on abstraction
    public OrderService(OrderRepository repo) { this.repo = repo; } // Injected
    public void placeOrder(Order order) { repo.save(order); }
}
```

---

## SECTION 3: Five Full LLD Problems with Java Code

---

### Problem 1: Parking Lot

**Clarification questions to ask:**
- How many floors? How many spots per floor?
- Vehicle types? (Motorcycle, Car, Bus/Truck)
- Fee calculation? (Hourly? Per vehicle type?)
- Multiple entry/exit gates?
- Do we need to find nearest available spot?

**Class diagram:**
```
ParkingLot
  └── ParkingFloor[]
        └── ParkingSpot[]
              └── Vehicle (parked)

Vehicle (abstract)
  ├── Motorcycle
  ├── Car
  └── Truck

ParkingTicket
FeeCalculator (interface)
  └── HourlyFeeCalculator
SpotAssignmentStrategy (interface)
  └── NearestSpotStrategy
```

**Complete Java Code:**

```java
// ── Enums ──────────────────────────────────────────────────────────────────

public enum VehicleType { MOTORCYCLE, CAR, TRUCK }
public enum SpotType    { SMALL, MEDIUM, LARGE }
public enum SpotStatus  { AVAILABLE, OCCUPIED }

// ── Vehicle Hierarchy ──────────────────────────────────────────────────────

public abstract class Vehicle {
    private final String licensePlate;
    private final VehicleType type;
    public Vehicle(String licensePlate, VehicleType type) {
        this.licensePlate = licensePlate;
        this.type = type;
    }
    public String getLicensePlate() { return licensePlate; }
    public VehicleType getType()    { return type; }
}

public class Motorcycle extends Vehicle {
    public Motorcycle(String plate) { super(plate, VehicleType.MOTORCYCLE); }
}
public class Car extends Vehicle {
    public Car(String plate) { super(plate, VehicleType.CAR); }
}
public class Truck extends Vehicle {
    public Truck(String plate) { super(plate, VehicleType.TRUCK); }
}

// ── Parking Spot ───────────────────────────────────────────────────────────

public class ParkingSpot {
    private final int spotId;
    private final SpotType type;
    private volatile SpotStatus status;
    private Vehicle parkedVehicle;

    public ParkingSpot(int spotId, SpotType type) {
        this.spotId = spotId;
        this.type = type;
        this.status = SpotStatus.AVAILABLE;
    }

    public synchronized boolean park(Vehicle vehicle) {
        if (status == SpotStatus.OCCUPIED) return false;
        this.parkedVehicle = vehicle;
        this.status = SpotStatus.OCCUPIED;
        return true;
    }

    public synchronized Vehicle unpark() {
        Vehicle v = this.parkedVehicle;
        this.parkedVehicle = null;
        this.status = SpotStatus.AVAILABLE;
        return v;
    }

    public boolean isAvailable()  { return status == SpotStatus.AVAILABLE; }
    public SpotType getType()     { return type; }
    public int getSpotId()        { return spotId; }
}

// ── Parking Ticket ─────────────────────────────────────────────────────────

public class ParkingTicket {
    private static final AtomicLong counter = new AtomicLong(0);
    private final long ticketId;
    private final Vehicle vehicle;
    private final ParkingSpot spot;
    private final int floorNumber;
    private final LocalDateTime entryTime;
    private LocalDateTime exitTime;
    private double totalFee;

    public ParkingTicket(Vehicle vehicle, ParkingSpot spot, int floor) {
        this.ticketId   = counter.incrementAndGet();
        this.vehicle    = vehicle;
        this.spot       = spot;
        this.floorNumber = floor;
        this.entryTime  = LocalDateTime.now();
    }

    public void close(double fee) {
        this.exitTime = LocalDateTime.now();
        this.totalFee = fee;
    }

    public long getTicketId()           { return ticketId; }
    public Vehicle getVehicle()         { return vehicle; }
    public ParkingSpot getSpot()        { return spot; }
    public int getFloor()               { return floorNumber; }
    public LocalDateTime getEntryTime() { return entryTime; }
    public LocalDateTime getExitTime()  { return exitTime; }
    public double getTotalFee()         { return totalFee; }
}

// ── Fee Calculator (Strategy pattern) ─────────────────────────────────────

public interface FeeCalculator {
    double calculate(ParkingTicket ticket);
}

public class HourlyFeeCalculator implements FeeCalculator {
    private static final Map<VehicleType, Double> RATES = Map.of(
        VehicleType.MOTORCYCLE, 20.0,
        VehicleType.CAR,        40.0,
        VehicleType.TRUCK,      80.0
    );

    @Override
    public double calculate(ParkingTicket ticket) {
        long minutes = ChronoUnit.MINUTES.between(ticket.getEntryTime(), LocalDateTime.now());
        long hours   = Math.max(1, (long) Math.ceil(minutes / 60.0));
        double rate  = RATES.getOrDefault(ticket.getVehicle().getType(), 40.0);
        return hours * rate;
    }
}

// ── Spot Assignment Strategy (Strategy pattern) ────────────────────────────

public interface SpotAssignmentStrategy {
    Optional<ParkingSpot> findSpot(List<ParkingFloor> floors, VehicleType vehicleType);
}

public class NearestSpotStrategy implements SpotAssignmentStrategy {
    private static final Map<VehicleType, SpotType> TYPE_MAP = Map.of(
        VehicleType.MOTORCYCLE, SpotType.SMALL,
        VehicleType.CAR,        SpotType.MEDIUM,
        VehicleType.TRUCK,      SpotType.LARGE
    );

    @Override
    public Optional<ParkingSpot> findSpot(List<ParkingFloor> floors, VehicleType vehicleType) {
        SpotType required = TYPE_MAP.get(vehicleType);
        return floors.stream()
            .flatMap(f -> f.getSpots().stream())
            .filter(s -> s.getType() == required && s.isAvailable())
            .findFirst();
    }
}

// ── Parking Floor ──────────────────────────────────────────────────────────

public class ParkingFloor {
    private final int floorNumber;
    private final List<ParkingSpot> spots;

    public ParkingFloor(int floorNumber, int small, int medium, int large) {
        this.floorNumber = floorNumber;
        this.spots = new ArrayList<>();
        int id = floorNumber * 1000;
        for (int i = 0; i < small;  i++) spots.add(new ParkingSpot(id++, SpotType.SMALL));
        for (int i = 0; i < medium; i++) spots.add(new ParkingSpot(id++, SpotType.MEDIUM));
        for (int i = 0; i < large;  i++) spots.add(new ParkingSpot(id++, SpotType.LARGE));
    }

    public List<ParkingSpot> getSpots() { return spots; }
    public int getFloorNumber()         { return floorNumber; }

    public long availableCount(SpotType type) {
        return spots.stream().filter(s -> s.getType() == type && s.isAvailable()).count();
    }
}

// ── Parking Lot ────────────────────────────────────────────────────────────

public class ParkingLot {
    private static volatile ParkingLot instance;
    private final List<ParkingFloor> floors;
    private final FeeCalculator feeCalculator;
    private final SpotAssignmentStrategy assignmentStrategy;
    private final Map<Long, ParkingTicket> activeTickets = new ConcurrentHashMap<>();

    private ParkingLot(List<ParkingFloor> floors,
                       FeeCalculator feeCalculator,
                       SpotAssignmentStrategy strategy) {
        this.floors              = floors;
        this.feeCalculator       = feeCalculator;
        this.assignmentStrategy  = strategy;
    }

    // Bill Pugh Singleton
    public static ParkingLot getInstance(List<ParkingFloor> floors,
                                          FeeCalculator calc,
                                          SpotAssignmentStrategy strategy) {
        if (instance == null) {
            synchronized (ParkingLot.class) {
                if (instance == null) {
                    instance = new ParkingLot(floors, calc, strategy);
                }
            }
        }
        return instance;
    }

    public ParkingTicket parkVehicle(Vehicle vehicle) {
        Optional<ParkingSpot> spot = assignmentStrategy.findSpot(floors, vehicle.getType());
        if (spot.isEmpty()) throw new RuntimeException("No spot available for " + vehicle.getType());

        int floorNum = findFloor(spot.get());
        spot.get().park(vehicle);

        ParkingTicket ticket = new ParkingTicket(vehicle, spot.get(), floorNum);
        activeTickets.put(ticket.getTicketId(), ticket);
        return ticket;
    }

    public double exitVehicle(long ticketId) {
        ParkingTicket ticket = activeTickets.remove(ticketId);
        if (ticket == null) throw new RuntimeException("Invalid ticket: " + ticketId);

        double fee = feeCalculator.calculate(ticket);
        ticket.close(fee);
        ticket.getSpot().unpark();
        return fee;
    }

    private int findFloor(ParkingSpot spot) {
        for (ParkingFloor floor : floors) {
            if (floor.getSpots().contains(spot)) return floor.getFloorNumber();
        }
        return -1;
    }

    public Map<SpotType, Long> getAvailability() {
        Map<SpotType, Long> result = new HashMap<>();
        for (SpotType type : SpotType.values()) {
            result.put(type, floors.stream()
                .mapToLong(f -> f.availableCount(type)).sum());
        }
        return result;
    }
}
```

**Extension — EV Charging:**
```java
// Add without modifying existing code (Open/Closed)
public enum SpotType { SMALL, MEDIUM, LARGE, EV_CHARGING }

public class EvVehicle extends Vehicle {
    public EvVehicle(String plate) { super(plate, VehicleType.CAR); }
}
// NearestSpotStrategy updated to prefer EV_CHARGING for EvVehicle
// HourlyFeeCalculator adds EV surcharge
```

**Follow-up interview questions:**
- Q: "How do you handle two threads parking simultaneously?" → `synchronized` on `ParkingSpot.park()` + `ConcurrentHashMap` for tickets
- Q: "How would you scale this to 1000 floors?" → Shard by floor, keep availability summary in Redis
- Q: "How would you add reservations?" → Add `ReservedStatus`, `Reservation` class, expiry with scheduled cleanup

---

### Problem 2: Vending Machine

**Clarification questions:**
- Does it support multiple payment methods?
- What happens if money inserted > item price?
- Can admin restock without power cycling?
- Does it need a display/UI state?

**State machine:**
```
IDLE → SELECT_PRODUCT → INSERT_MONEY → DISPENSE → IDLE
                                     ↘ CANCEL → IDLE
```

**Complete Java Code:**

```java
// ── State Interface ────────────────────────────────────────────────────────

public interface VendingMachineState {
    void selectProduct(VendingMachine machine, String productCode);
    void insertMoney(VendingMachine machine, double amount);
    void dispense(VendingMachine machine);
    void cancel(VendingMachine machine);
}

// ── Product ────────────────────────────────────────────────────────────────

public class Product {
    private final String code;
    private final String name;
    private final double price;
    private int quantity;

    public Product(String code, String name, double price, int quantity) {
        this.code = code; this.name = name;
        this.price = price; this.quantity = quantity;
    }

    public boolean isAvailable()   { return quantity > 0; }
    public void decrementStock()   { quantity--; }
    public String getCode()        { return code; }
    public String getName()        { return name; }
    public double getPrice()       { return price; }
    public int getQuantity()       { return quantity; }
    public void restock(int qty)   { this.quantity += qty; }
}

// ── Vending Machine ────────────────────────────────────────────────────────

public class VendingMachine {
    private VendingMachineState currentState;
    private final Map<String, Product> inventory = new HashMap<>();
    private Product selectedProduct;
    private double insertedAmount;

    // States (flyweight — single instances)
    private final VendingMachineState idleState     = new IdleState();
    private final VendingMachineState selectState   = new SelectProductState();
    private final VendingMachineState insertState   = new InsertMoneyState();
    private final VendingMachineState dispenseState = new DispenseState();

    public VendingMachine() {
        this.currentState = idleState;
    }

    public void addProduct(Product p)  { inventory.put(p.getCode(), p); }
    public Product getProduct(String code) { return inventory.get(code); }

    public void setState(VendingMachineState state) { this.currentState = state; }
    public VendingMachineState getIdleState()     { return idleState; }
    public VendingMachineState getSelectState()   { return selectState; }
    public VendingMachineState getInsertState()   { return insertState; }
    public VendingMachineState getDispenseState() { return dispenseState; }

    public void setSelectedProduct(Product p)    { this.selectedProduct = p; }
    public Product getSelectedProduct()          { return selectedProduct; }

    public void addAmount(double amount)         { this.insertedAmount += amount; }
    public double getInsertedAmount()            { return insertedAmount; }
    public void resetAmount()                    { this.insertedAmount = 0; }

    // Delegate to current state
    public void selectProduct(String code)       { currentState.selectProduct(this, code); }
    public void insertMoney(double amount)       { currentState.insertMoney(this, amount); }
    public void dispense()                       { currentState.dispense(this); }
    public void cancel()                         { currentState.cancel(this); }
}

// ── Concrete States ────────────────────────────────────────────────────────

public class IdleState implements VendingMachineState {
    @Override
    public void selectProduct(VendingMachine machine, String code) {
        Product p = machine.getProduct(code);
        if (p == null || !p.isAvailable()) {
            System.out.println("Product unavailable: " + code);
            return;
        }
        machine.setSelectedProduct(p);
        machine.setState(machine.getSelectState());
        System.out.println("Selected: " + p.getName() + " — Price: ₹" + p.getPrice());
    }
    @Override public void insertMoney(VendingMachine m, double a) { System.out.println("Select a product first."); }
    @Override public void dispense(VendingMachine m)              { System.out.println("Select a product first."); }
    @Override public void cancel(VendingMachine m)                { System.out.println("Nothing to cancel."); }
}

public class SelectProductState implements VendingMachineState {
    @Override public void selectProduct(VendingMachine m, String c) { System.out.println("Already selected. Insert money."); }
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addAmount(amount);
        machine.setState(machine.getInsertState());
        System.out.printf("Inserted: ₹%.2f. Total: ₹%.2f%n", amount, machine.getInsertedAmount());
        if (machine.getInsertedAmount() >= machine.getSelectedProduct().getPrice()) {
            machine.dispense();
        }
    }
    @Override public void dispense(VendingMachine m) { System.out.println("Insert money first."); }
    @Override
    public void cancel(VendingMachine machine) {
        machine.setSelectedProduct(null);
        machine.setState(machine.getIdleState());
        System.out.println("Cancelled. Returning to idle.");
    }
}

public class InsertMoneyState implements VendingMachineState {
    @Override public void selectProduct(VendingMachine m, String c) { System.out.println("Already inserting money."); }
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addAmount(amount);
        System.out.printf("Total inserted: ₹%.2f%n", machine.getInsertedAmount());
    }
    @Override
    public void dispense(VendingMachine machine) {
        Product p = machine.getSelectedProduct();
        if (machine.getInsertedAmount() < p.getPrice()) {
            System.out.printf("Insufficient: need ₹%.2f more%n", p.getPrice() - machine.getInsertedAmount());
            return;
        }
        machine.setState(machine.getDispenseState());
        machine.dispense();
    }
    @Override
    public void cancel(VendingMachine machine) {
        System.out.printf("Returning ₹%.2f%n", machine.getInsertedAmount());
        machine.resetAmount();
        machine.setSelectedProduct(null);
        machine.setState(machine.getIdleState());
    }
}

public class DispenseState implements VendingMachineState {
    @Override public void selectProduct(VendingMachine m, String c) { System.out.println("Dispensing in progress."); }
    @Override public void insertMoney(VendingMachine m, double a)   { System.out.println("Dispensing in progress."); }
    @Override
    public void dispense(VendingMachine machine) {
        Product p = machine.getSelectedProduct();
        double change = machine.getInsertedAmount() - p.getPrice();
        p.decrementStock();
        System.out.println("Dispensing: " + p.getName());
        if (change > 0) System.out.printf("Change: ₹%.2f%n", change);
        machine.resetAmount();
        machine.setSelectedProduct(null);
        machine.setState(machine.getIdleState());
    }
    @Override public void cancel(VendingMachine m) { System.out.println("Cannot cancel — dispensing."); }
}
```

---

### Problem 3: Elevator System

**Clarification questions:**
- How many elevators? How many floors?
- Direction: up/down only, or can it go either way from anywhere?
- Algorithm: FCFS, LOOK, or SCAN?
- Is there a priority for emergency/VIP floors?
- Multi-threaded? (Elevators run concurrently)

**Class diagram:**
```
ElevatorSystem
  └── Elevator[]  (each runs in its own thread)
  └── Scheduler (interface)
        └── LOOKScheduler

Request (external: from floor button, internal: inside elevator)
Direction enum (UP, DOWN)
ElevatorState enum (IDLE, MOVING_UP, MOVING_DOWN)
```

**Complete Java Code:**

```java
public enum Direction   { UP, DOWN }
public enum ElevatorState { IDLE, MOVING_UP, MOVING_DOWN }

public class Request {
    private final int floor;
    private final Direction direction; // null for internal requests
    public Request(int floor, Direction direction) {
        this.floor = floor; this.direction = direction;
    }
    public int getFloor()           { return floor; }
    public Direction getDirection() { return direction; }
}

public class Elevator implements Runnable {
    private final int id;
    private int currentFloor;
    private ElevatorState state;
    // TreeSet keeps floors sorted; split into up/down queues (LOOK algorithm)
    private final TreeSet<Integer> upQueue   = new TreeSet<>();
    private final TreeSet<Integer> downQueue = new TreeSet<>(Collections.reverseOrder());
    private final Object lock = new Object();

    public Elevator(int id, int startFloor) {
        this.id = id; this.currentFloor = startFloor; this.state = ElevatorState.IDLE;
    }

    public void addRequest(int floor) {
        synchronized (lock) {
            if (floor > currentFloor || state == ElevatorState.MOVING_UP) {
                upQueue.add(floor);
            } else {
                downQueue.add(floor);
            }
            lock.notifyAll();
        }
    }

    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            synchronized (lock) {
                while (upQueue.isEmpty() && downQueue.isEmpty()) {
                    try { lock.wait(); } catch (InterruptedException e) { return; }
                }
            }
            processRequests();
        }
    }

    private void processRequests() {
        // LOOK: serve up queue first, then down queue
        while (!upQueue.isEmpty()) {
            int nextFloor = upQueue.first();
            moveTo(nextFloor);
            synchronized (lock) { upQueue.remove(nextFloor); }
        }
        state = ElevatorState.MOVING_DOWN;
        while (!downQueue.isEmpty()) {
            int nextFloor = downQueue.first();
            moveTo(nextFloor);
            synchronized (lock) { downQueue.remove(nextFloor); }
        }
        state = ElevatorState.IDLE;
    }

    private void moveTo(int targetFloor) {
        System.out.printf("Elevator %d: floor %d → %d%n", id, currentFloor, targetFloor);
        // Simulate movement (1 sec per floor in real system)
        currentFloor = targetFloor;
        System.out.printf("Elevator %d: arrived at floor %d%n", id, currentFloor);
    }

    public int getCurrentFloor() { return currentFloor; }
    public ElevatorState getState()  { return state; }
    public int getId()           { return id; }
}

public interface ElevatorScheduler {
    Elevator selectElevator(List<Elevator> elevators, Request request);
}

public class NearestIdleScheduler implements ElevatorScheduler {
    @Override
    public Elevator selectElevator(List<Elevator> elevators, Request request) {
        return elevators.stream()
            .min(Comparator.comparingInt(e ->
                Math.abs(e.getCurrentFloor() - request.getFloor())))
            .orElseThrow();
    }
}

public class ElevatorSystem {
    private final List<Elevator> elevators;
    private final ElevatorScheduler scheduler;
    private final List<Thread> threads = new ArrayList<>();

    public ElevatorSystem(int numElevators, int startFloor, ElevatorScheduler scheduler) {
        this.scheduler = scheduler;
        this.elevators = new ArrayList<>();
        for (int i = 0; i < numElevators; i++) {
            Elevator e = new Elevator(i + 1, startFloor);
            elevators.add(e);
            Thread t = new Thread(e, "Elevator-" + (i + 1));
            threads.add(t);
            t.start();
        }
    }

    public void requestElevator(int floor, Direction direction) {
        Request req      = new Request(floor, direction);
        Elevator chosen  = scheduler.selectElevator(elevators, req);
        System.out.printf("Dispatching Elevator %d to floor %d%n", chosen.getId(), floor);
        chosen.addRequest(floor);
    }

    public void shutdown() {
        threads.forEach(Thread::interrupt);
    }
}
```

---

### Problem 4: BookMyShow (Ticket Booking)

**Clarification questions:**
- Multiple shows/screens at same time?
- Seat selection: user picks specific seat or system assigns?
- Payment: sync or async?
- Concurrent booking of same seat — how to handle?
- Cancellation and refund policy?

**The critical challenge: preventing double-booking under concurrency**

```java
public enum SeatStatus { AVAILABLE, LOCKED, BOOKED }

public class Seat {
    private final String seatId; // e.g., "A1", "B12"
    private final String row;
    private final int number;
    private volatile SeatStatus status;
    private final ReentrantLock seatLock = new ReentrantLock();

    public Seat(String row, int number) {
        this.row = row; this.number = number;
        this.seatId = row + number;
        this.status = SeatStatus.AVAILABLE;
    }

    // Returns true if successfully locked (temp hold during payment)
    public boolean tryLock() {
        if (seatLock.tryLock()) {
            try {
                if (status == SeatStatus.AVAILABLE) {
                    status = SeatStatus.LOCKED;
                    return true;
                }
            } finally {
                seatLock.unlock();
            }
        }
        return false;
    }

    public synchronized boolean confirmBooking() {
        if (status == SeatStatus.LOCKED) { status = SeatStatus.BOOKED; return true; }
        return false;
    }

    public synchronized void releaseLock() {
        if (status == SeatStatus.LOCKED) status = SeatStatus.AVAILABLE;
    }

    public SeatStatus getStatus() { return status; }
    public String getSeatId()     { return seatId; }
}

public class Show {
    private final long showId;
    private final String movieName;
    private final LocalDateTime showTime;
    private final Screen screen;

    public Show(long showId, String movieName, LocalDateTime time, Screen screen) {
        this.showId = showId; this.movieName = movieName;
        this.showTime = showTime; this.screen = screen;
    }
    public Screen getScreen() { return screen; }
    public long getShowId()   { return showId; }
}

public class Screen {
    private final int screenId;
    private final List<Seat> seats;

    public Screen(int screenId, int rows, int seatsPerRow) {
        this.screenId = screenId;
        this.seats = new ArrayList<>();
        for (int r = 0; r < rows; r++) {
            char rowChar = (char)('A' + r);
            for (int s = 1; s <= seatsPerRow; s++) {
                seats.add(new Seat(String.valueOf(rowChar), s));
            }
        }
    }

    public Optional<Seat> findSeat(String seatId) {
        return seats.stream().filter(s -> s.getSeatId().equals(seatId)).findFirst();
    }

    public List<Seat> getAvailableSeats() {
        return seats.stream()
            .filter(s -> s.getStatus() == SeatStatus.AVAILABLE)
            .collect(Collectors.toList());
    }
}

public class Booking {
    private static final AtomicLong counter = new AtomicLong(0);
    private final long bookingId;
    private final Show show;
    private final List<Seat> seats;
    private final String userId;
    private BookingStatus status;
    private double totalAmount;

    public Booking(Show show, List<Seat> seats, String userId, double amount) {
        this.bookingId   = counter.incrementAndGet();
        this.show = show; this.seats = seats;
        this.userId = userId; this.totalAmount = amount;
        this.status = BookingStatus.PENDING;
    }
    public void confirm() { this.status = BookingStatus.CONFIRMED; }
    public long getBookingId() { return bookingId; }
}

public enum BookingStatus { PENDING, CONFIRMED, CANCELLED }

public class BookingService {
    private final Map<Long, Show> shows = new ConcurrentHashMap<>();
    // Locks per show to minimize contention
    private final ConcurrentHashMap<Long, ReentrantLock> showLocks = new ConcurrentHashMap<>();
    private static final int LOCK_TIMEOUT_SECONDS = 5;

    public Booking bookSeats(String userId, long showId, List<String> seatIds)
            throws InterruptedException {
        Show show = shows.get(showId);
        if (show == null) throw new IllegalArgumentException("Show not found: " + showId);

        ReentrantLock lock = showLocks.computeIfAbsent(showId, k -> new ReentrantLock());

        // Try to acquire show-level lock within timeout
        if (!lock.tryLock(LOCK_TIMEOUT_SECONDS, TimeUnit.SECONDS)) {
            throw new RuntimeException("System busy, please retry");
        }

        List<Seat> lockedSeats = new ArrayList<>();
        try {
            Screen screen = show.getScreen();
            // Validate and lock all seats atomically
            for (String seatId : seatIds) {
                Seat seat = screen.findSeat(seatId)
                    .orElseThrow(() -> new IllegalArgumentException("Seat not found: " + seatId));
                if (!seat.tryLock()) {
                    // Release all already-locked seats and fail
                    lockedSeats.forEach(Seat::releaseLock);
                    throw new RuntimeException("Seat " + seatId + " is no longer available");
                }
                lockedSeats.add(seat);
            }

            // All seats locked — process payment (simulated)
            double amount = processPayment(userId, lockedSeats.size() * 250.0);

            // Confirm booking
            lockedSeats.forEach(Seat::confirmBooking);
            Booking booking = new Booking(show, lockedSeats, userId, amount);
            booking.confirm();
            return booking;

        } finally {
            lock.unlock();
        }
    }

    private double processPayment(String userId, double amount) {
        // Payment gateway integration — simplified
        System.out.printf("Payment of ₹%.2f processed for user %s%n", amount, userId);
        return amount;
    }

    public void addShow(Show show) {
        shows.put(show.getShowId(), show);
    }
}
```

**Follow-up: What if two users book same seat simultaneously?**
- `ReentrantLock` per show + `tryLock` on individual `Seat` ensures atomicity
- If seat is taken mid-booking, all locked seats are released (no partial booking)

---

### Problem 5: LRU Cache

**Approach 1 — LinkedHashMap (simple, interview-fast)**

```java
public class LRUCache {
    private final int capacity;
    // accessOrder=true: get() moves element to end (most recently used)
    private final LinkedHashMap<Integer, Integer> cache;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
                return size() > LRUCache.this.capacity;
            }
        };
    }

    public int get(int key) {
        return cache.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        cache.put(key, value);
    }
}
// Time: O(1) for both get and put. Space: O(capacity)
```

**Approach 2 — Doubly Linked List + HashMap (explains internals)**

```java
public class LRUCacheManual {
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    // Dummy head (LRU end) and tail (MRU end)
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    static class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }

    public LRUCacheManual(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToTail(node); // Most recently used
        return node.val;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.val = value;
            moveToTail(node);
        } else {
            if (map.size() == capacity) {
                Node lru = head.next; // Least recently used
                removeNode(lru);
                map.remove(lru.key);
            }
            Node newNode = new Node(key, value);
            insertAtTail(newNode);
            map.put(key, newNode);
        }
    }

    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertAtTail(Node node) {
        node.prev = tail.prev;
        node.next = tail;
        tail.prev.next = node;
        tail.prev = node;
    }

    private void moveToTail(Node node) {
        removeNode(node);
        insertAtTail(node);
    }
}
// Time: O(1) for both. Space: O(capacity)
```

**Thread-Safe LRU Cache:**

```java
public class ThreadSafeLRUCache {
    private final LRUCacheManual cache;
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();

    public ThreadSafeLRUCache(int capacity) {
        this.cache = new LRUCacheManual(capacity);
    }

    public int get(int key) {
        // get() modifies order (MRU), so needs write lock
        rwLock.writeLock().lock();
        try { return cache.get(key); }
        finally { rwLock.writeLock().unlock(); }
    }

    public void put(int key, int value) {
        rwLock.writeLock().lock();
        try { cache.put(key, value); }
        finally { rwLock.writeLock().unlock(); }
    }
}
```

**Extension — LFU Cache:**
```
Instead of recency, track frequency.
Data structure: HashMap<key, freq> + HashMap<freq, LinkedHashSet<key>>
minFreq variable tracks current minimum frequency.
get: update freq, move key to freq+1 bucket
put: if capacity full, evict from minFreq bucket (LRU among least frequent)
```

---

## SECTION 4: Design Patterns Quick Reference

| Pattern | Trigger phrase | Java in 5 lines | Your GSTN example |
|---|---|---|---|
| **Strategy** | "multiple algorithms for same task" | Interface + implementations, inject via constructor | `CaseCustomizerFactory` selecting `ICaseCustomizer` |
| **Factory** | "create object without exposing creation logic" | Static method returns interface type | `KafkaConsumerFactory` |
| **Observer** | "notify multiple listeners of an event" | `List<Observer>` + `notifyAll()` | Kafka consumer listeners |
| **Builder** | "construct complex object step by step" | Inner static Builder class with chained setters | Request object construction |
| **Singleton** | "only one instance needed globally" | Private constructor + static volatile instance | Spring beans, config singletons |
| **Decorator** | "add behavior without modifying class" | Wraps original object, implements same interface | `BufferedReader` wraps `FileReader` |
| **Template Method** | "algorithm skeleton, subclasses fill steps" | Abstract class with `templateMethod()` calling abstract steps | Your `Consumer.java` base class |
| **Command** | "encapsulate a request as an object" | `Command` interface with `execute()` | Undo/redo, task queues |
| **Composite** | "tree structures, treat leaf and composite uniformly" | `Component` interface, `Leaf` and `Composite` both implement it | File system, org charts |
| **Proxy** | "control access to an object" | Same interface as real object, add cross-cutting concerns | Spring AOP, lazy loading |

---

## SECTION 5: SDE-3 LLD Bar — What's Different

### SDE-2 vs SDE-3 Expectations

| Aspect | SDE-2 | SDE-3 |
|---|---|---|
| Correctness | Working solution | Working + handles edge cases gracefully |
| Design | Reasonable class hierarchy | Justifies every design choice |
| Extensibility | Mentions it | Demonstrates it with concrete examples |
| Patterns | Uses appropriate patterns | Explains *why* this pattern over alternatives |
| Trade-offs | Basic trade-offs | Quantifies trade-offs, knows when NOT to apply pattern |
| Concurrency | Adds locks when asked | Proactively identifies race conditions |

### How to Signal SDE-3 Level

1. **Lead with the interface, not the implementation**
   - "First I'll define the contracts, then we can discuss implementations"

2. **Justify every design decision**
   - Not: "I'll use Strategy pattern here"
   - Yes: "I'll use Strategy here because we'll likely add new fee types without changing the core parking logic — keeps it Open/Closed"

3. **Identify extensibility points proactively**
   - "Right now this handles cars only. If we add EVs, we'd add a new SpotType enum value and update the strategy — no existing code changes"

4. **Discuss concurrency without being asked**
   - "Parking is highly concurrent — two threads could try to park in the same spot. I'll use synchronized on the spot itself to prevent this, rather than locking the whole lot which would kill throughput"

5. **Know when NOT to use patterns**
   - "I'm not using a full Observer pattern here because we only have one listener — adding that abstraction would be over-engineering for this problem"

### Sample SDE-3 LLD Questions

1. "Design a distributed LRU cache" → Consistent hashing + per-node LRU + cache invalidation
2. "Design a rate limiter that works across multiple servers" → Redis sliding window counter
3. "Design a task scheduler with priorities and dependencies" → Priority queue + DAG for dependency resolution
4. "Design a plugin system for your application" → ServiceLoader, reflection, interface contracts
5. "Design an undo/redo system" → Command pattern + two stacks (undo/redo history)
