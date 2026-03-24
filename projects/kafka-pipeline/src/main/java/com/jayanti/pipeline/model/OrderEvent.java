package com.jayanti.pipeline.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.math.BigDecimal;
import java.time.Instant;

/**
 * OrderEvent is used both as a Kafka message payload (JSON) and a JPA entity.
 *
 * Design note: Java records cannot be JPA entities (no default constructor,
 * immutable). We use a standard class with both bean-style getters (required
 * by Jackson + JPA) and record-style accessor aliases so callers can use either
 * convention. In a production codebase you would separate the DTO from the entity.
 *
 * Interview talking point: "At GSTN we had a similar dual-use model for invoice
 * events — the Kafka payload and the DB entity were the same class. We later
 * separated them as the schema diverged, but for smaller services this works fine."
 */
@Entity
@Table(name = "order_events")
public class OrderEvent {

    @Id
    @Column(name = "order_id", nullable = false, unique = true, length = 64)
    private String orderId;

    @Column(name = "user_id", nullable = false, length = 64)
    private String userId;

    @Column(name = "amount", nullable = false, precision = 19, scale = 4)
    private BigDecimal amount;

    @Column(name = "event_type", nullable = false, length = 64)
    private String eventType;

    @Column(name = "event_timestamp", nullable = false)
    private Instant timestamp;

    @Column(name = "processed_at")
    private Instant processedAt;

    // Default constructor required by JPA + Jackson deserialization
    public OrderEvent() {}

    public OrderEvent(String orderId, String userId, BigDecimal amount,
                      String eventType, Instant timestamp) {
        this.orderId = orderId;
        this.userId = userId;
        this.amount = amount;
        this.eventType = eventType;
        this.timestamp = timestamp;
    }

    // Bean-style getters (required by Jackson + JPA)
    public String getOrderId()      { return orderId; }
    public String getUserId()       { return userId; }
    public BigDecimal getAmount()   { return amount; }
    public String getEventType()    { return eventType; }
    public Instant getTimestamp()   { return timestamp; }
    public Instant getProcessedAt() { return processedAt; }

    // Record-style accessor aliases (convenience — matches Java record convention)
    public String orderId()      { return orderId; }
    public String userId()       { return userId; }
    public BigDecimal amount()   { return amount; }
    public String eventType()    { return eventType; }
    public Instant timestamp()   { return timestamp; }

    // Setters (for JPA and Jackson deserialization)
    public void setOrderId(String orderId)      { this.orderId = orderId; }
    public void setUserId(String userId)        { this.userId = userId; }
    public void setAmount(BigDecimal amount)    { this.amount = amount; }
    public void setEventType(String eventType)  { this.eventType = eventType; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }
    public void setProcessedAt(Instant t)       { this.processedAt = t; }

    @Override
    public String toString() {
        return "OrderEvent{orderId='%s', userId='%s', amount=%s, eventType='%s', timestamp=%s}"
                .formatted(orderId, userId, amount, eventType, timestamp);
    }
}
