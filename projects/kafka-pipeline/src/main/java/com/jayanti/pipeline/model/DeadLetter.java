package com.jayanti.pipeline.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;

/**
 * Persists events that exhausted all retries and landed in the DLQ.
 * Ops teams use this table to inspect failures, fix root causes, and replay.
 */
@Entity
@Table(name = "dead_letters")
public class DeadLetter {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "order_id", nullable = false, length = 64)
    private String orderId;

    @Column(name = "payload", nullable = false, columnDefinition = "TEXT")
    private String payload;     // Raw JSON of the failed OrderEvent

    @Column(name = "failure_reason", columnDefinition = "TEXT")
    private String failureReason;

    @Column(name = "retry_count")
    private int retryCount;

    @Column(name = "received_at", nullable = false)
    private Instant receivedAt;

    @Column(name = "resolved")
    private boolean resolved = false;

    protected DeadLetter() {}

    public DeadLetter(String orderId, String payload, String failureReason, int retryCount) {
        this.orderId = orderId;
        this.payload = payload;
        this.failureReason = failureReason;
        this.retryCount = retryCount;
        this.receivedAt = Instant.now();
        this.resolved = false;
    }

    public Long getId()              { return id; }
    public String getOrderId()       { return orderId; }
    public String getPayload()       { return payload; }
    public String getFailureReason() { return failureReason; }
    public int getRetryCount()       { return retryCount; }
    public Instant getReceivedAt()   { return receivedAt; }
    public boolean isResolved()      { return resolved; }
    public void setResolved(boolean resolved) { this.resolved = resolved; }
}
