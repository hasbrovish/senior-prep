# Company Questions — Phase 2 (Top-Tier Companies)

## Amazon / Flipkart
- LP-heavy behavioral rounds (see Amazon_LP_STAR_Bank.md)
- "Design Amazon's order processing system" — Event sourcing, Saga, exactly-once
- Bar Raiser round: deep dive into one topic, cross-examine tradeoffs
- GSTN angle: Similar scale (14M users), compliance requirements

## Goldman Sachs
- Financial systems, low-latency trading, risk management
- "Design a real-time risk assessment system" — Streaming (Kafka Streams), in-memory computation
- Strong emphasis on data consistency and correctness
- GSTN angle: Financial data, XA transactions, audit trails

## Google
- Googleyness: ambiguity comfort, doing the right thing, collaboration
- 2 coding + 1 system design + 1 behavioral (Googleyness & Leadership)
- Code on Google Docs (no autocomplete)
- GSTN angle: Scale, technical leadership, polyglot (Go + Java)

## Stripe / Anthropic
- Code quality > speed. Production-grade code in interviews.
- "Design an idempotent API" — Your rate limiter + Kafka idempotent consumer experience
- Anthropic: AI safety thinking, intellectual honesty, first-principles
- GSTN angle: Financial compliance (Stripe), AI POC experience (Anthropic)

## PhonePe / Swiggy
- UPI payments, hyperlocal delivery, real-time systems
- "Design UPI payment flow" — Similar to GSTN filing flow (multi-step, state machine)
- "Design real-time delivery tracking" — WebSocket + Kafka + Redis pub/sub
- GSTN angle: Event-driven architecture, state machine (Golang FSM)
