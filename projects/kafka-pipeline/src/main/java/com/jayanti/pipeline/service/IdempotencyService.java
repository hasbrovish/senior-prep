package com.jayanti.pipeline.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;

/**
 * Redis-based idempotency guard.
 *
 * Uses Redis SET NX (set if not exists) for atomic check-and-set.
 * TTL = 24 hours — covers Kafka retention window.
 *
 * States per orderId:
 *   "PROCESSING" → currently being handled
 *   "COMPLETED"  → successfully processed
 *   "FAILED"     → sent to DLQ
 *
 * Interview talking point: "This is the same dedup pattern used at GSTN for
 * return filing — filing the same GSTIN+period twice must be idempotent.
 * Redis SETNX gives atomic check-and-set without distributed locks."
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class IdempotencyService {

    private static final String KEY_PREFIX = "order:idempotency:";
    private static final Duration TTL = Duration.ofHours(24);

    private final StringRedisTemplate redisTemplate;

    /**
     * Atomically mark orderId as processing.
     * Returns true if this is the first time (not a duplicate).
     * Returns false if already seen (duplicate — skip).
     */
    public boolean markAsProcessing(String orderId) {
        Boolean set = redisTemplate.opsForValue()
                .setIfAbsent(KEY_PREFIX + orderId, "PROCESSING", TTL);
        return Boolean.TRUE.equals(set);
    }

    public void markAsCompleted(String orderId) {
        redisTemplate.opsForValue().set(KEY_PREFIX + orderId, "COMPLETED", TTL);
    }

    public void markAsFailed(String orderId) {
        redisTemplate.opsForValue().set(KEY_PREFIX + orderId, "FAILED", TTL);
    }

    public String getStatus(String orderId) {
        return redisTemplate.opsForValue().get(KEY_PREFIX + orderId);
    }
}
