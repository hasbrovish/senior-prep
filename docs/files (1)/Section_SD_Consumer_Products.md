# System Design — Consumer Products

## Design: Twitter/X Feed
- **Write path:** Tweet → Kafka → Fan-out service → Write to each follower's timeline (Redis sorted set)
- **Read path:** Get timeline from Redis sorted set. Pre-computed for most users.
- **Celebrity problem:** Don't fan-out for users with 10M+ followers. Mix at read time instead.
- **Scale:** Tweets/day: ~500M. Timelines: pre-computed for active users, on-demand for inactive.

## Design: Instagram/Photo Sharing
- **Upload:** Client → API → S3 (photos) + MySQL (metadata). CDN for serving.
- **Feed:** Similar to Twitter fan-out. Ranked by ML model (engagement prediction).
- **Stories:** Separate storage (24hr TTL). Redis sorted set for ordering.

## Design: Uber/Ride-Matching
- **Geospatial indexing:** GeoHash or QuadTree for nearby driver lookup.
- **Matching:** Score drivers by distance + ETA + rating. Greedy matching with timeout.
- **Real-time tracking:** Driver location updates every 3s → Kafka → consumer updates Redis GeoHash → client polls or WebSocket push.
- **GSTN parallel:** High concurrency (riders = taxpayers), event-driven architecture, real-time status updates.

## Design: YouTube/Video Streaming
- **Upload:** Chunked upload → transcoding pipeline (multiple resolutions) → CDN distribution.
- **Streaming:** Adaptive bitrate (HLS/DASH). CDN edge servers. Prefetch next chunks.
- **Search:** Elasticsearch for video metadata. ML ranking for recommendations.

## Design: WhatsApp Messaging
- **1:1 messaging:** WebSocket connection per device. Messages stored in Cassandra (write-optimized).
- **Group messaging:** Fan-out on write for small groups (<256). Each member gets a copy.
- **End-to-end encryption:** Signal Protocol. Server never sees plaintext.
- **Delivery receipts:** Sent (server received) → Delivered (device received) → Read (user opened).
- **Offline delivery:** Messages queued. Delivered when device reconnects.

## Design: Google Docs (Collaborative Editing)
- **Conflict resolution:** Operational Transformation (OT) or CRDT (Conflict-free Replicated Data Types).
- **OT:** Transform concurrent operations to maintain consistency. Complex but well-proven.
- **CRDT:** Mathematically guaranteed convergence. Simpler logic, potentially more bandwidth.
- **Architecture:** WebSocket for real-time sync. Operation log in DB. Periodic snapshots for fast loading.
