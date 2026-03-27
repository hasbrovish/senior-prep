# Company Questions — Phase 1 (Mid-Tier Product Companies)

## Razorpay
- Payment gateway architecture, idempotency keys, reconciliation
- "Design a payment retry system" — Saga pattern, DLQ, exponential backoff
- GSTN angle: Both handle financial data with zero-loss guarantees

## Juspay
- Payment orchestration, card vault, PCI compliance
- "How do you handle distributed transactions?" — XA vs Saga, your Atomikos experience
- Focus on low-latency decision making (route payment to best processor)

## CRED
- Reward systems, credit card bill payments, gamification
- "Design a rewards/cashback system" — Event-driven, eventually consistent
- GSTN angle: Large user base, event-driven architecture

## MakeMyTrip
- Booking systems, inventory management, search + ranking
- "Design a hotel booking system" — Distributed locks, double-booking prevention
- GSTN angle: High concurrency during peak (deadlines ≈ holiday seasons)

## Meesho / Paytm
- E-commerce at scale, logistics, notification systems
- "Design a notification system" — Your exact GSTN experience
- GSTN angle: Multi-channel notifications, regional language support

## Common Phase 1 Questions
1. Explain microservices vs monolith tradeoffs
2. How do you handle API versioning?
3. Design a rate limiter (you've built this at GSTN)
4. Explain your caching strategy
5. How do you ensure zero downtime deployments?
