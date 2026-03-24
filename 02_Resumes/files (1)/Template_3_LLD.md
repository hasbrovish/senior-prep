# LOW-LEVEL DESIGN (LLD) - ANSWER TEMPLATE & EVALUATION GUIDE

## 🎯 STRONG HIRE SIGNALS (What Interviewers Score)

| Signal | Strong Hire | Hire | No Hire |
|--------|-------------|------|---------|
| **Class Design** | Clean, follows SOLID | Good structure | Monolithic |
| **Design Patterns** | Identifies & applies correctly | Uses some | None/wrong |
| **Extensibility** | Anticipates future needs | Extensible with guidance | Rigid |
| **Code Quality** | Production-ready | Clean, readable | Messy |
| **Trade-offs** | Discusses proactively | When prompted | Doesn't recognize |
| **Abstraction** | Right level | Some abstraction | Over/under engineered |

---

## 📝 LLD ANSWER TEMPLATE (45-60 minutes)

### STEP 1: CLARIFY REQUIREMENTS (5 minutes)

```
"Before I start designing, let me understand the scope..."

ASK THESE:
□ What are the core entities? (Users, Products, Orders?)
□ What operations need to be supported?
□ Any constraints? (Single-threaded or concurrent?)
□ Scale considerations? (In-memory or persistent?)
□ What might change in the future? (Extensibility hints)

EXAMPLE - Parking Lot:
- "What types of vehicles? Car, Bike, Truck?"
- "Multiple floors or single level?"
- "Payment required?"
- "Hourly or flat rate pricing?"
- "Multiple entry/exit points?"
```

### STEP 2: IDENTIFY CORE ENTITIES (5 minutes)

```
"The main entities I see are..."

TECHNIQUE: Noun Extraction
┌─────────────────────────────────────────────────────┐
│ Read requirements → Circle all NOUNS               │
│                                                     │
│ "A parking lot has multiple floors, each floor    │
│  has spots for different vehicles. Users can      │
│  park their vehicle and pay at exit."            │
│                                                     │
│ Entities: ParkingLot, Floor, Spot, Vehicle, User  │
│ Actions: park(), exit(), pay() → become methods   │
└─────────────────────────────────────────────────────┘

DRAW CLASS BOXES:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  ParkingLot  │  │    Floor     │  │    Spot      │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ - floors     │  │ - spots      │  │ - type       │
│ - capacity   │  │ - floorNum   │  │ - isOccupied │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ + park()     │  │ + findSpot() │  │ + occupy()   │
│ + exit()     │  │ + getAvail() │  │ + release()  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### STEP 3: DEFINE RELATIONSHIPS (5 minutes)

```
"Let me define how these classes interact..."

RELATIONSHIP TYPES:
┌──────────────────────────────────────────────────────┐
│ IS-A (Inheritance):                                  │
│   Car IS-A Vehicle                                   │
│   Bike IS-A Vehicle                                  │
│                                                      │
│ HAS-A (Composition):                                │
│   ParkingLot HAS-A List<Floor>                      │
│   Floor HAS-A List<Spot>                            │
│                                                      │
│ USES (Dependency):                                   │
│   ParkingService USES ParkingLot                    │
│   PaymentService USES PricingStrategy               │
└──────────────────────────────────────────────────────┘

SAY:
"ParkingLot contains Floors (composition), and each Floor
contains Spots. Vehicle is an abstract class with Car, Bike
as concrete implementations (inheritance)."
```

### STEP 4: APPLY DESIGN PATTERNS (5 minutes)

```
"I'll use [PATTERN] here because..."

COMMON PATTERNS FOR LLD:

┌─────────────────┬─────────────────────────────────────┐
│ Factory         │ Creating different vehicle/spot     │
│                 │ types without if-else chains       │
├─────────────────┼─────────────────────────────────────┤
│ Strategy        │ Different pricing algorithms       │
│                 │ Different allocation strategies    │
├─────────────────┼─────────────────────────────────────┤
│ Observer        │ Notify display boards on change    │
│                 │ Notify on booking confirmation     │
├─────────────────┼─────────────────────────────────────┤
│ Singleton       │ ParkingLot instance                │
│                 │ Database connection                │
├─────────────────┼─────────────────────────────────────┤
│ State           │ Booking states (pending→confirmed) │
│                 │ Vending machine states             │
├─────────────────┼─────────────────────────────────────┤
│ Command         │ Undo/Redo operations               │
│                 │ Request queuing                    │
└─────────────────┴─────────────────────────────────────┘

SAY:
"I'm using Strategy pattern for pricing so we can easily 
add new pricing models (hourly, daily, weekend) without 
modifying existing code - this follows Open-Closed principle."
```

### STEP 5: CODE KEY CLASSES (25-30 minutes)

```java
// EXAMPLE: Parking Lot

// 1. ENUMS (Define types first)
enum VehicleType { CAR, BIKE, TRUCK }
enum SpotType { COMPACT, REGULAR, LARGE }

// 2. ABSTRACT BASE (If inheritance needed)
abstract class Vehicle {
    private String licensePlate;
    private VehicleType type;
    
    public abstract SpotType getRequiredSpotType();
}

// 3. CONCRETE IMPLEMENTATIONS
class Car extends Vehicle {
    @Override
    public SpotType getRequiredSpotType() {
        return SpotType.REGULAR;
    }
}

// 4. CORE ENTITIES
class Spot {
    private final String spotId;
    private final SpotType type;
    private Vehicle currentVehicle;
    
    public boolean isAvailable() {
        return currentVehicle == null;
    }
    
    public boolean canFit(Vehicle vehicle) {
        return this.type.ordinal() >= 
               vehicle.getRequiredSpotType().ordinal();
    }
    
    public void occupy(Vehicle vehicle) {
        if (!canFit(vehicle)) {
            throw new IllegalArgumentException("Vehicle too large");
        }
        this.currentVehicle = vehicle;
    }
    
    public void release() {
        this.currentVehicle = null;
    }
}

// 5. STRATEGY PATTERN (For extensibility)
interface PricingStrategy {
    double calculatePrice(Duration duration);
}

class HourlyPricing implements PricingStrategy {
    private final double hourlyRate;
    
    @Override
    public double calculatePrice(Duration duration) {
        long hours = Math.max(1, duration.toHours());
        return hours * hourlyRate;
    }
}

// 6. SERVICE LAYER
class ParkingService {
    private final ParkingLot parkingLot;
    private final PricingStrategy pricingStrategy;
    
    public Ticket park(Vehicle vehicle) {
        Spot spot = parkingLot.findAvailableSpot(vehicle);
        if (spot == null) {
            throw new ParkingFullException();
        }
        spot.occupy(vehicle);
        return new Ticket(vehicle, spot, Instant.now());
    }
    
    public Receipt exit(Ticket ticket) {
        Duration parked = Duration.between(
            ticket.getEntryTime(), Instant.now());
        double amount = pricingStrategy.calculatePrice(parked);
        ticket.getSpot().release();
        return new Receipt(ticket, amount);
    }
}
```

### STEP 6: DISCUSS EXTENSIBILITY (5 minutes)

```
"If we needed to add [new feature], we would..."

COMMON EXTENSIONS:
┌────────────────────────────────────────────────────────┐
│ "Add new vehicle type (Bus)?"                          │
│ → Just create new Bus class extending Vehicle          │
│ → No changes to existing code (Open-Closed)           │
├────────────────────────────────────────────────────────┤
│ "Add new pricing model (Weekend pricing)?"             │
│ → Create WeekendPricing implementing PricingStrategy   │
│ → Inject different strategy based on day              │
├────────────────────────────────────────────────────────┤
│ "Add reservation feature?"                             │
│ → Add ReservationService                               │
│ → Spot gets reservedUntil timestamp                   │
│ → findAvailableSpot checks reservation status         │
└────────────────────────────────────────────────────────┘

SAY:
"Because I used Strategy pattern, adding new pricing is just
creating a new class. No existing code needs to change."
```

---

## 🔥 STRONG HIRE PHRASES

### Starting:
- "Let me first identify the core entities and their relationships..."
- "I'll design this to be extensible for..."

### While Designing:
- "I'm using [Pattern] here to follow [SOLID principle]..."
- "This abstraction allows us to easily add..."
- "The trade-off with this approach is..."

### Code Quality:
- "I'm making this private to encapsulate..."
- "I'll inject this dependency for testability..."
- "This validation prevents invalid state..."

### Extensibility:
- "If requirements change to add X, we would just..."
- "This follows Open-Closed - extend without modifying..."

---

## 📊 SOLID QUICK REFERENCE

| Principle | One-liner | Code Smell if Violated |
|-----------|-----------|------------------------|
| **S**ingle Responsibility | One reason to change | God class, 500+ line class |
| **O**pen/Closed | Extend, don't modify | if-else chains for types |
| **L**iskov Substitution | Subtypes are substitutable | Square extends Rectangle breaks |
| **I**nterface Segregation | Specific > general interfaces | Empty method implementations |
| **D**ependency Inversion | Depend on abstractions | new ConcreteClass() everywhere |

---

## 📊 PATTERN SELECTION GUIDE

| Scenario | Pattern | Why |
|----------|---------|-----|
| Multiple types of same thing | Factory | Encapsulate creation logic |
| Different algorithms | Strategy | Swap behavior at runtime |
| Object state changes behavior | State | Cleaner than if-else chains |
| Notify multiple objects | Observer | Decouple notifier and listeners |
| Complex object construction | Builder | Step-by-step, immutable result |
| One instance globally | Singleton | Controlled access |
| Wrap additional behavior | Decorator | Add features without inheritance |
| Simplify complex subsystem | Facade | Single entry point |

---

## 📝 LLD PROBLEMS QUICK TEMPLATES

### Parking Lot
```
Entities: ParkingLot, Floor, Spot, Vehicle, Ticket
Patterns: Factory (Vehicle), Strategy (Pricing), Singleton (Lot)
Key methods: park(), exit(), findSpot()
```

### Elevator System
```
Entities: Elevator, Floor, Request, Controller
Patterns: State (elevator state), Observer (floor display), Strategy (scheduling)
Key methods: requestElevator(), moveToFloor()
```

### BookMyShow
```
Entities: Movie, Theatre, Show, Seat, Booking, User
Patterns: Factory (Seat types), Observer (notifications), Strategy (pricing)
Key methods: searchMovies(), bookSeats(), cancelBooking()
```

### Splitwise
```
Entities: User, Group, Expense, Split
Patterns: Strategy (split types: equal, exact, percentage), Observer (balance updates)
Key methods: addExpense(), settleUp(), getBalance()
```

---

## 📝 SELF-ASSESSMENT CHECKLIST

```
□ Did I clarify all requirements before designing?
□ Did I identify all core entities?
□ Did I define relationships (IS-A, HAS-A)?
□ Did I apply at least 2 design patterns appropriately?
□ Does my design follow SOLID principles?
□ Is my code clean and readable?
□ Can I extend without modifying existing code?
□ Did I discuss trade-offs?
□ Did I handle edge cases/validation?
□ Is my design testable (dependencies injected)?
```

**Score: ___/10**

- 9-10: Strong Hire level
- 7-8: Hire level  
- 5-6: Lean Hire
- 0-4: Need more practice
