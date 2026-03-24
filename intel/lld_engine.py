"""
LLD (Low-Level Design) Practice Engine.

20 standard problems with:
  - Requirements, constraints, evaluation rubric
  - SOLID compliance scoring
  - AI-powered design evaluation
  - Score tracking in DB

Usage:
  from intel.lld_engine import get_lld_problem, print_lld_problems, evaluate_lld_design
"""

from datetime import date
import json

LLD_PROBLEMS = {
    "parking-lot": {
        "name":        "Parking Lot System",
        "difficulty":  "easy",
        "companies":   ["amazon", "adobe", "flipkart", "phonepe"],
        "time_mins":   45,
        "requirements": [
            "Multiple levels, multiple types of spots (compact, large, handicapped, motorcycle)",
            "Park/unpark vehicles, assign nearest available spot",
            "Track occupied/free spots, generate ticket with entry time",
            "Calculate parking fee based on duration and vehicle type",
            "Handle concurrent access (multiple entry/exit gates)",
        ],
        "key_classes": ["ParkingLot", "ParkingFloor", "ParkingSpot", "Vehicle", "Ticket", "FeeCalculator"],
        "patterns":    ["Singleton (ParkingLot)", "Strategy (FeeCalculator)", "Factory (VehicleFactory)"],
        "solid_checks": [
            "S: FeeCalculator separate from ParkingLot",
            "O: Add new vehicle types without changing existing",
            "L: Car, Truck, Motorcycle all substitutable for Vehicle",
            "I: Separate interfaces: Parkable, Chargeable",
            "D: ParkingLot depends on SpotAssignment interface, not concrete",
        ],
        "hire_signals": [
            "Uses Strategy pattern for fee calculation (hourly, flat, etc.)",
            "Thread-safe spot assignment (synchronized or ConcurrentHashMap)",
            "Extensible: adding EV charging spots without breaking existing code",
            "Generates receipt with ticket number, timestamps",
        ],
        "no_hire": "Single ParkingLot class with switch/if-else for vehicle types",
    },

    "lru-cache": {
        "name":        "LRU Cache",
        "difficulty":  "easy",
        "companies":   ["amazon", "google", "flipkart", "goldman"],
        "time_mins":   30,
        "requirements": [
            "get(key): return value or -1",
            "put(key, value): insert/update. Evict LRU if capacity exceeded",
            "Both operations O(1)",
        ],
        "key_classes": ["LRUCache", "Node (doubly linked list)", "HashMap"],
        "patterns":    ["Doubly Linked List + HashMap", "OR LinkedHashMap (Java shortcut)"],
        "solid_checks": [
            "S: Cache logic + eviction policy are separate concerns",
            "O: Eviction policy swappable (LRU/LFU/FIFO) via interface",
        ],
        "hire_signals": [
            "Implements from scratch: DLL + HashMap (shows understanding)",
            "OR mentions LinkedHashMap with accessOrder=true as production shortcut",
            "Discusses Thread safety: ConcurrentHashMap or ReentrantReadWriteLock",
            "Mentions distributed cache (Redis) for production extension",
        ],
        "no_hire": "Uses LinkedList scan to find LRU — O(n)",
    },

    "elevator": {
        "name":        "Elevator System",
        "difficulty":  "medium",
        "companies":   ["amazon", "microsoft", "adobe", "flipkart"],
        "time_mins":   45,
        "requirements": [
            "Multiple elevators, multiple floors",
            "Request elevator from any floor (UP/DOWN)",
            "Elevator dispatching algorithm (nearest car, SCAN/LOOK)",
            "Handle concurrent requests",
            "Emergency stop, door open/close sensors",
        ],
        "key_classes": ["ElevatorSystem", "Elevator", "ElevatorController", "Request", "Door"],
        "patterns":    ["State (elevator: IDLE, MOVING_UP, MOVING_DOWN)", "Observer (floor request → controller)", "Strategy (dispatch algorithm)"],
        "solid_checks": [
            "S: Elevator state machine separate from dispatching logic",
            "O: New dispatch algorithms via Strategy interface",
            "D: ElevatorController depends on DispatchStrategy interface",
        ],
        "hire_signals": [
            "State machine for elevator (not raw if/else)",
            "SCAN algorithm: service requests in direction of travel",
            "Thread per elevator with blocking queue for requests",
            "Discussion of real-world: weighted dispatching, VIP floors",
        ],
        "no_hire": "Single class with if (floor > currentFloor) go up",
    },

    "chess": {
        "name":        "Chess Game",
        "difficulty":  "medium",
        "companies":   ["amazon", "google", "microsoft", "goldman"],
        "time_mins":   45,
        "requirements": [
            "All pieces: Pawn, Rook, Knight, Bishop, Queen, King",
            "Move validation for each piece type",
            "Check and Checkmate detection",
            "Turn management, game state",
            "Optional: castling, en passant",
        ],
        "key_classes": ["Board", "Piece (abstract)", "Player", "GameManager", "Move"],
        "patterns":    ["Template Method (Piece.isValidMove())", "Observer (Board state changes)", "Command (Move history for undo)"],
        "solid_checks": [
            "S: Move validation in each Piece class, not Board",
            "O: Add new piece types by extending Piece",
            "L: All Piece subclasses substitutable in Board",
        ],
        "hire_signals": [
            "Abstract Piece class with abstract isValidMove()",
            "Board passes itself to isValidMove for path checking",
            "Check detection: simulate king movement",
            "Move history (Command pattern) for undo/replay",
        ],
        "no_hire": "All move logic in Board.move() with instanceof checks",
    },

    "bookmyshow": {
        "name":        "Movie Booking System (BookMyShow)",
        "difficulty":  "medium",
        "companies":   ["amazon", "flipkart", "phonepe", "swiggy"],
        "time_mins":   45,
        "requirements": [
            "Search movies by city, theater, showtime",
            "Book seats (concurrent — seat should not be double-booked)",
            "Payment processing, booking confirmation",
            "Cancellation with refund policy",
            "Notification: booking confirmation, show reminder",
        ],
        "key_classes": ["Movie", "Theater", "Screen", "Show", "Seat", "Booking", "Payment"],
        "patterns":    ["Observer (booking → notification)", "Strategy (payment methods)", "Template (refund calculation)"],
        "solid_checks": [
            "S: Booking, Payment, Notification separate classes",
            "O: New payment methods without changing BookingService",
            "D: BookingService depends on NotificationPort interface",
        ],
        "hire_signals": [
            "Optimistic locking or pessimistic lock for seat booking",
            "Seat status: AVAILABLE, RESERVED, BOOKED (reserved for payment hold)",
            "Eventual consistency discussion: booking held 10 min during payment",
            "Microservice decomposition: movie-service, booking-service, payment-service",
        ],
        "no_hire": "No concurrency handling — multiple users can book same seat",
    },

    "splitwise": {
        "name":        "Expense Sharing App (Splitwise)",
        "difficulty":  "medium",
        "companies":   ["amazon", "google", "flipkart"],
        "time_mins":   45,
        "requirements": [
            "Add expense, split EQUAL/EXACT/PERCENT/SHARES",
            "Show balance: who owes whom",
            "Settle up between two users",
            "Group expenses",
            "Transaction history",
        ],
        "key_classes": ["User", "Expense", "Split", "Group", "Balance", "SplitCalculator"],
        "patterns":    ["Strategy (EqualSplit, ExactSplit, PercentSplit, ShareSplit)", "Observer (balance update on new expense)"],
        "solid_checks": [
            "O: New split types by implementing SplitStrategy interface",
            "S: SplitCalculator separate from Expense",
        ],
        "hire_signals": [
            "Strategy pattern for split types — interviewer loves this",
            "Simplify balances: A→B 100, B→A 60 → net A→B 40",
            "Heap-based minimum transactions algorithm",
            "Thread safety for concurrent expense additions",
        ],
        "no_hire": "if/else for split types in Expense class",
    },

    "hotel-booking": {
        "name":        "Hotel Booking System",
        "difficulty":  "medium",
        "companies":   ["amazon", "microsoft", "flipkart"],
        "time_mins":   45,
        "requirements": [
            "Search rooms by date range, type, amenities",
            "Book room (prevent double booking for same dates)",
            "Pricing: base + seasonal + occupancy-based",
            "Cancellation with refund tiers",
            "Review and rating system",
        ],
        "key_classes": ["Hotel", "Room", "Booking", "RoomAvailability", "PricingEngine"],
        "patterns":    ["Strategy (PricingStrategy: seasonal, occupancy)", "Observer (booking confirmation, reminder)"],
        "solid_checks": [
            "O: New pricing strategies without changing Room class",
            "S: Availability management separate from Booking",
        ],
        "hire_signals": [
            "Interval overlap detection for date-range booking",
            "Pricing engine with strategy pattern",
            "Discuss read-heavy: cache room availability in Redis",
        ],
        "no_hire": "No overlap check — can double book same room",
    },

    "snake-ladder": {
        "name":        "Snake and Ladder Game",
        "difficulty":  "easy",
        "companies":   ["amazon", "microsoft", "adobe"],
        "time_mins":   30,
        "requirements": [
            "N players, configurable board size",
            "Snakes and ladders at configurable positions",
            "Dice roll (1-6), player movement",
            "Win condition, turn management",
            "Support for multiple dice",
        ],
        "key_classes": ["Board", "Player", "Dice", "Snake", "Ladder", "Game"],
        "patterns":    ["Strategy (dice rolling strategy)", "Observer (turn management)", "Command (move history)"],
        "solid_checks": [
            "S: Board setup, game loop, player state — separate classes",
            "O: Add new special cells (portal, teleporter) without changing Board",
        ],
        "hire_signals": [
            "Extensible: Snake and Ladder both implement Jump interface",
            "Board cells as HashMap<position, Jump> instead of sparse array",
            "Multi-dice support via varargs or list",
        ],
        "no_hire": "Single main() with switch/case for snakes and ladders",
    },

    "notification-system": {
        "name":        "Notification System",
        "difficulty":  "medium",
        "companies":   ["amazon", "flipkart", "phonepe", "swiggy"],
        "time_mins":   45,
        "requirements": [
            "Send notifications: Email, SMS, Push, In-App",
            "User preferences: which channels are enabled",
            "Templates with variable substitution",
            "Rate limiting per user/channel",
            "Retry failed notifications with exponential backoff",
            "Priority queue: critical alerts vs marketing",
        ],
        "key_classes": ["NotificationService", "NotificationChannel", "Template", "UserPreference", "NotificationQueue"],
        "patterns":    ["Strategy (Email/SMS/Push channels)", "Observer (events → notifications)", "Chain of Responsibility (rate limiting → send → retry)"],
        "solid_checks": [
            "O: New channel type by implementing NotificationChannel",
            "D: NotificationService depends on NotificationChannel interface",
            "I: Don't force all channels to implement unused methods",
        ],
        "hire_signals": [
            "Strategy for channels — extensible to WhatsApp, Slack etc.",
            "Discusses Kafka for async, reliable delivery",
            "Rate limiting: token bucket per user per channel",
            "Template engine for personalisation at scale",
            "GSTN CommunicationService reference — your strongest example here",
        ],
        "no_hire": "if(type==EMAIL) emailClient.send() else if(SMS)...",
    },

    "library-management": {
        "name":        "Library Management System",
        "difficulty":  "easy",
        "companies":   ["amazon", "microsoft", "adobe"],
        "time_mins":   45,
        "requirements": [
            "Add/remove books, search by title/author/ISBN",
            "Issue and return books",
            "Multiple copies of same book",
            "Fine calculation for overdue books",
            "Member management, reservation queue",
        ],
        "key_classes": ["Library", "Book", "BookCopy", "Member", "Loan", "FineCalculator"],
        "patterns":    ["Observer (due date reminder)", "Strategy (FineCalculator)", "Repository (BookRepository)"],
        "solid_checks": [
            "S: FineCalculator separate from Loan",
            "O: New book types (ebook, magazine) by extending BookItem",
        ],
        "hire_signals": [
            "Book vs BookCopy distinction (multiple copies of same book)",
            "Reservation queue for waitlisted members",
            "Fine calculation with configurable policy",
        ],
        "no_hire": "Library class with direct ArrayList management, no abstraction",
    },

    "food-delivery": {
        "name":        "Food Delivery App (Zomato/Swiggy)",
        "difficulty":  "hard",
        "companies":   ["swiggy", "amazon", "flipkart", "phonepe"],
        "time_mins":   60,
        "requirements": [
            "Browse restaurants, menus, items",
            "Cart management, order placement",
            "Restaurant matching and delivery partner assignment",
            "Real-time order tracking (status updates)",
            "Payment, refunds",
            "Ratings and reviews",
        ],
        "key_classes": ["Order", "Restaurant", "DeliveryPartner", "CartItem", "Location", "OrderTracker"],
        "patterns":    ["Observer (order status updates)", "Strategy (delivery partner assignment)", "State (order states)"],
        "solid_checks": [
            "S: Separate: order management, delivery management, payment",
            "O: New delivery partner assignment strategies without changing core",
            "D: OrderService depends on PaymentPort, NotificationPort interfaces",
        ],
        "hire_signals": [
            "Order state machine: PLACED → CONFIRMED → PREPARING → PICKED_UP → DELIVERED",
            "Geospatial partner assignment (nearest partner within X km)",
            "Discuss microservices: order-service, delivery-service, restaurant-service",
            "Eventual consistency in order status propagation",
        ],
        "no_hire": "Single OrderManager class handling all concerns",
    },

    "rate-limiter": {
        "name":        "Rate Limiter",
        "difficulty":  "medium",
        "companies":   ["google", "amazon", "goldman", "phonepe"],
        "time_mins":   45,
        "requirements": [
            "Rate limit per IP, user, API key",
            "Configurable limits per endpoint",
            "Algorithms: token bucket, sliding window, fixed window",
            "Return rate limit headers (X-RateLimit-Remaining)",
            "Distributed rate limiting (multiple nodes)",
        ],
        "key_classes": ["RateLimiter", "TokenBucketLimiter", "SlidingWindowLimiter", "RateLimitConfig"],
        "patterns":    ["Strategy (algorithm selection)", "Chain of Responsibility (middleware stack)"],
        "solid_checks": [
            "O: New algorithms by implementing RateLimiterStrategy",
            "S: Config management separate from enforcement logic",
        ],
        "hire_signals": [
            "Token Bucket: tokens += rate * elapsed, min(tokens, capacity)",
            "Sliding Window: count requests in rolling window",
            "Redis-based distributed: Lua script for atomic increment + check",
            "Return proper HTTP 429 with Retry-After header",
        ],
        "no_hire": "Simple counter without time window awareness",
    },

    "design-patterns-ood": {
        "name":        "Vending Machine",
        "difficulty":  "medium",
        "companies":   ["amazon", "microsoft", "adobe", "goldman"],
        "time_mins":   45,
        "requirements": [
            "Multiple products, multiple quantities",
            "Accept coins/notes, return change",
            "Select product, dispense if available and paid",
            "Refund on cancel",
            "Admin: restock, collect cash",
        ],
        "key_classes": ["VendingMachine", "Product", "Coin", "State", "ItemDispenser"],
        "patterns":    ["State (IDLE, HAS_MONEY, DISPENSING, RETURN_CHANGE)", "Singleton (VendingMachine)", "Strategy (payment methods)"],
        "solid_checks": [
            "S: State management separate from UI/IO",
            "O: Add new states without changing VendingMachine",
        ],
        "hire_signals": [
            "State pattern — clean transitions without if/else explosion",
            "Proper change calculation (greedy coin algorithm)",
            "Thread safety for concurrent users",
        ],
        "no_hire": "Multiple if-else for machine state in main class",
    },

    "linkedin": {
        "name":        "LinkedIn / Professional Network",
        "difficulty":  "hard",
        "companies":   ["microsoft", "amazon", "flipkart"],
        "time_mins":   60,
        "requirements": [
            "User profiles, connections (1st/2nd degree)",
            "News feed with posts, likes, comments",
            "Job postings and applications",
            "Search: people, companies, jobs",
            "Notifications: connection request, post like",
        ],
        "key_classes": ["User", "Connection", "Post", "FeedService", "NotificationService", "SearchService"],
        "patterns":    ["Observer (notification on connection/post)", "Strategy (feed ranking)", "Repository (UserRepository, PostRepository)"],
        "solid_checks": [
            "D: FeedService depends on FeedRanking interface",
            "S: Feed generation, connection management, notifications — all separate",
        ],
        "hire_signals": [
            "Graph-based connections (BFS for 2nd degree)",
            "Feed: pull vs push model tradeoff discussion",
            "Search: inverted index or Elasticsearch mention",
            "Scale: 900M users — horizontal sharding strategy",
        ],
        "no_hire": "All methods on User class",
    },

    "atm": {
        "name":        "ATM System",
        "difficulty":  "medium",
        "companies":   ["goldman", "amazon", "microsoft"],
        "time_mins":   45,
        "requirements": [
            "Card insertion, PIN validation",
            "Cash withdrawal (check balance, sufficient cash)",
            "Balance enquiry, mini statement",
            "Multiple accounts: savings, current",
            "Transaction logging, receipt printing",
        ],
        "key_classes": ["ATM", "Card", "Account", "Transaction", "CashDispenser", "BankingService"],
        "patterns":    ["State (IDLE, HAS_CARD, PIN_ENTERED, TRANSACTION)", "Strategy (account type: savings vs current)"],
        "solid_checks": [
            "S: PIN validation, cash dispensing, account management — separate",
            "O: New transaction types by implementing Transaction interface",
        ],
        "hire_signals": [
            "State machine for ATM flow",
            "Secure PIN handling (don't store plain text)",
            "Transaction atomicity: debit account AND dispense cash atomically",
            "Network timeout handling: auto-rollback if cash not dispensed",
        ],
        "no_hire": "if(state==CARD_INSERTED) then PIN prompt, all in one class",
    },

    "cab-booking": {
        "name":        "Cab Booking System (Uber/Ola)",
        "difficulty":  "hard",
        "companies":   ["amazon", "flipkart", "swiggy", "phonepe"],
        "time_mins":   60,
        "requirements": [
            "Match rider to nearest driver",
            "Real-time location tracking",
            "Pricing: base fare + per km + surge",
            "Trip states: requested, accepted, arrived, in_trip, completed",
            "Payment, rating, cancellation",
        ],
        "key_classes": ["Trip", "Driver", "Rider", "DriverMatcher", "PricingEngine", "LocationService"],
        "patterns":    ["State (trip states)", "Strategy (DriverMatcher, PricingEngine)", "Observer (trip status notifications)"],
        "solid_checks": [
            "D: TripService depends on DriverMatchingStrategy, PricingStrategy",
            "S: Location tracking, pricing, matching — separate services",
        ],
        "hire_signals": [
            "Geospatial indexing: QuadTree or geohash for nearby drivers",
            "Surge pricing: Strategy pattern with real-time demand/supply ratio",
            "Trip state machine with valid transitions",
            "Dispatch timeout: if no driver in 30s, expand search radius",
        ],
        "no_hire": "Linear scan of all drivers to find nearest",
    },

    "inventory": {
        "name":        "Inventory Management System",
        "difficulty":  "medium",
        "companies":   ["amazon", "flipkart", "adobe"],
        "time_mins":   45,
        "requirements": [
            "Add/remove products, track quantities",
            "Low stock alerts",
            "Multiple warehouses",
            "Order fulfillment: pick from nearest/cheapest warehouse",
            "Reporting: stock levels, movements",
        ],
        "key_classes": ["Product", "Warehouse", "Inventory", "StockAlert", "FulfillmentEngine"],
        "patterns":    ["Observer (low stock alert)", "Strategy (fulfillment: nearest, cheapest)", "Repository pattern"],
        "solid_checks": [
            "O: New fulfillment strategies without changing InventoryService",
            "D: InventoryService depends on FulfillmentStrategy interface",
        ],
        "hire_signals": [
            "Observer for low stock threshold",
            "Multi-warehouse fulfillment with optimisation criteria",
            "Concurrent stock deduction: optimistic locking",
        ],
        "no_hire": "Single warehouse, no concurrency handling",
    },

    "task-management": {
        "name":        "Task Management System (Jira-lite)",
        "difficulty":  "medium",
        "companies":   ["amazon", "microsoft", "adobe"],
        "time_mins":   45,
        "requirements": [
            "Create tasks, assign to users, set priority/due date",
            "Task states: TODO, IN_PROGRESS, REVIEW, DONE",
            "Subtasks, dependencies (task A blocks task B)",
            "Comments, attachments",
            "Board view: Kanban columns",
        ],
        "key_classes": ["Task", "User", "Board", "Sprint", "Comment", "TaskDependency"],
        "patterns":    ["Observer (task status change → notification)", "State (task workflow)", "Composite (task + subtasks)"],
        "solid_checks": [
            "O: New task types (bug, story, epic) by extending Task",
            "Composite pattern: Task contains List<Task> subtasks",
        ],
        "hire_signals": [
            "State pattern for task workflow with valid transitions",
            "Composite for task hierarchy",
            "Dependency cycle detection (topological sort)",
        ],
        "no_hire": "String-based state with no validation of transitions",
    },

    "search-autocomplete": {
        "name":        "Search Autocomplete / Typeahead",
        "difficulty":  "medium",
        "companies":   ["google", "amazon", "microsoft", "flipkart"],
        "time_mins":   45,
        "requirements": [
            "Return top K suggestions for prefix",
            "Rank by frequency/recency",
            "Support add/remove suggestions",
            "Handle concurrent reads/writes",
            "Optional: fuzzy matching",
        ],
        "key_classes": ["TrieNode", "Trie", "AutocompleteService", "SuggestionRanker"],
        "patterns":    ["Trie data structure", "Observer (frequency update on search)", "Strategy (ranking algorithm)"],
        "solid_checks": [
            "O: New ranking strategies without changing Trie",
            "D: AutocompleteService depends on RankingStrategy interface",
        ],
        "hire_signals": [
            "Trie with top-K cache at each node for O(1) retrieval",
            "Thread-safe with ReadWriteLock (many reads, few writes)",
            "Discuss distributed: separate trie per first-char range",
        ],
        "no_hire": "Linear scan of all entries for prefix match",
    },

    "message-queue": {
        "name":        "Message Queue (Kafka-lite)",
        "difficulty":  "hard",
        "companies":   ["amazon", "google", "goldman", "phonepe"],
        "time_mins":   60,
        "requirements": [
            "Topics with partitions",
            "Producer: publish messages to topic",
            "Consumer groups: each group gets all messages, load balanced within group",
            "Offset management: consumer tracks position",
            "Retention policy: delete messages older than N days",
            "At-least-once delivery guarantee",
        ],
        "key_classes": ["MessageQueue", "Topic", "Partition", "Producer", "Consumer", "ConsumerGroup", "Offset"],
        "patterns":    ["Observer (publisher-subscriber)", "Iterator (offset-based message consumption)"],
        "solid_checks": [
            "S: Message storage, consumer offset tracking, retention — separate",
            "O: New retention policies by implementing RetentionPolicy interface",
        ],
        "hire_signals": [
            "Partition-based parallelism for consumer group",
            "Offset stored per (consumer_group, partition)",
            "At-least-once: commit offset AFTER processing",
            "GSTN Kafka DLQ pattern — your strongest example here",
        ],
        "no_hire": "Simple in-memory queue with no partition/consumer group concept",
    },
}


def get_lld_problem(name: str):
    """Get a specific LLD problem by name/key."""
    key = name.lower().replace(" ", "-")
    # Fuzzy match
    for k, v in LLD_PROBLEMS.items():
        if k == key or key in k or k in key:
            return {"key": k, **v}
    return None


def list_lld_problems(company: str = None, difficulty: str = None) -> list[dict]:
    """List LLD problems with optional filters."""
    result = []
    for k, v in LLD_PROBLEMS.items():
        if company and company.lower() not in [c.lower() for c in v.get("companies", [])]:
            continue
        if difficulty and v.get("difficulty") != difficulty:
            continue
        result.append({"key": k, **v})
    return sorted(result, key=lambda x: {"easy": 0, "medium": 1, "hard": 2}[x["difficulty"]])


def print_lld_problems(company: str = None, difficulty: str = None):
    """Print available LLD problems."""
    problems = list_lld_problems(company=company, difficulty=difficulty)
    label = f"{company or 'All Companies'}"

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  LLD PRACTICE PROBLEMS — {label:<30}║
  ╚══════════════════════════════════════════════════════════╝
""")
    diff_icon = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    for p in problems:
        companies_str = ", ".join(p["companies"][:3])
        print(f"  {diff_icon[p['difficulty']]} {p['name']:<35} [{p['time_mins']} min]  {companies_str}")
        print(f"     Key: prep lld \"{p['key']}\"")

    print()
    print(f"  Total: {len(problems)} problems | prep lld <name>  to practice")
    print()


def print_lld_session(key: str):
    """Print a full LLD practice session for a problem."""
    problem = get_lld_problem(key)
    if not problem:
        print(f"\n  ❌ Problem '{key}' not found.")
        print(f"  Available: {', '.join(LLD_PROBLEMS.keys())}\n")
        return

    diff_icon = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  LLD PRACTICE — {problem['name']:<40}║
  ║  {diff_icon[problem['difficulty']]} {problem['difficulty'].upper():<8} │ ⏱ {problem['time_mins']} min │ {', '.join(problem['companies'][:3]):<18}  ║
  ╚══════════════════════════════════════════════════════════╝

  APPROACH:
    1. Gather requirements (5 min) — ask clarifying questions
    2. Identify entities and their relationships (5 min)
    3. Draw class diagram (10 min)
    4. Code the core classes (20-25 min)
    5. Discuss extensibility and SOLID compliance (5 min)

  REQUIREMENTS:""")

    for i, req in enumerate(problem["requirements"], 1):
        print(f"    {i}. {req}")

    print(f"\n  KEY CLASSES TO IMPLEMENT:")
    for cls in problem["key_classes"]:
        print(f"    • {cls}")

    print(f"\n  DESIGN PATTERNS TO USE:")
    for pat in problem["patterns"]:
        print(f"    • {pat}")

    print(f"\n  SOLID COMPLIANCE CHECKLIST:")
    for check in problem["solid_checks"]:
        print(f"    □ {check}")

    print(f"\n  ── START TIMER: {problem['time_mins']} MINUTES ────────────────────────────")
    print(f"  Open IntelliJ / VS Code. Start coding. Think aloud.")
    print()

    try:
        input("  [Press Enter when done — then self-evaluate]")
    except (EOFError, KeyboardInterrupt):
        pass

    print(f"\n  ── HIRE SIGNALS (did you include these?): ─────────────────")
    all_good = True
    for signal in problem["hire_signals"]:
        try:
            ans = input(f"  {'□'} {signal[:65]}  (y/n): ").strip().lower()
            icon = "✅" if ans == "y" else "❌"
            print(f"  {icon} {signal[:65]}")
            if ans != "y":
                all_good = False
        except (EOFError, KeyboardInterrupt):
            break

    print(f"\n  ── NO HIRE IF: ─────────────────────────────────────────────")
    print(f"  ❌ {problem['no_hire']}")

    # Score and save
    try:
        score_raw = input("\n  Self-score (1=bad design  3=decent  5=hire level): ").strip()
        score = int(score_raw) if score_raw.isdigit() and 1 <= int(score_raw) <= 5 else 3
    except (EOFError, KeyboardInterrupt):
        score = 3

    save_lld_score(problem["key"], score)

    verdict = "HIRE" if score >= 4 else ("LEAN HIRE" if score >= 3 else "NO HIRE")
    print(f"\n  Verdict: {verdict}  (score {score}/5)")
    print(f"  Logged to DB. Run: prep lld-scores  to see your trend.")
    print()


def save_lld_score(problem_key: str, score: int, time_mins: int = 0, notes: str = ""):
    """Save an LLD session score to DB."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        conn.execute("""
            INSERT INTO lld_sessions (date_done, problem_key, score, time_mins, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (str(date.today()), problem_key, score, time_mins, notes))
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_lld_scores(limit: int = 20) -> list[dict]:
    """Get recent LLD practice history."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        rows = conn.execute("""
            SELECT * FROM lld_sessions ORDER BY date_done DESC LIMIT ?
        """, (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def evaluate_lld_with_ai(problem_key: str, design_description: str) -> str:
    """Use AI to evaluate an LLD design description."""
    try:
        from intel.coach import _call_claude, _profile_context
        problem = get_lld_problem(problem_key)
        if not problem:
            return "Problem not found"

        system = f"""You are a senior SDE-3 evaluating an LLD interview answer.
{_profile_context()}

PROBLEM: {problem['name']}
REQUIREMENTS: {json.dumps(problem['requirements'])}
EXPECTED PATTERNS: {', '.join(problem['patterns'])}
SOLID CHECKS: {json.dumps(problem['solid_checks'])}
HIRE SIGNALS: {json.dumps(problem['hire_signals'])}
NO-HIRE IF: {problem['no_hire']}

Evaluate the candidate's design. Return:
1. SCORE: X/10 (with breakdown: SOLID, extensibility, correctness, patterns, production-readiness)
2. VERDICT: Strong Hire / Hire / Lean Hire / Lean No Hire / No Hire
3. WHAT'S GOOD: 2-3 specific strengths
4. CRITICAL GAPS: 2-3 things missing that would cause a rejection
5. HIRE-LEVEL DESIGN: Show what a 9/10 design looks like in bullet points
6. FOLLOW-UP QUESTIONS: 3 questions an interviewer would probe deeper"""

        return _call_claude(system, f"CANDIDATE'S DESIGN:\n{design_description}")
    except Exception as e:
        return f"[AI evaluation unavailable: {e}]"
