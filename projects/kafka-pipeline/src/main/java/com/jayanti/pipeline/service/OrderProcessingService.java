package com.jayanti.pipeline.service;

import com.jayanti.pipeline.model.OrderEvent;
import com.jayanti.pipeline.repository.OrderEventRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Random;

/**
 * Core business logic for processing order events.
 *
 * Interview talking point: "Processing is @Transactional — DB write and any
 * downstream calls happen atomically. If the method throws, the transaction
 * rolls back, the consumer does NOT acknowledge the offset, and Kafka redelivers.
 * The Redis idempotency check in the consumer layer prevents double-processing
 * after a successful commit."
 *
 * Simulated failure: negative amounts trigger a RuntimeException to demonstrate
 * the retry + DLQ flow without needing real infrastructure failures.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class OrderProcessingService {

    private final OrderEventRepository orderEventRepository;
    private final Random random = new Random();

    @Transactional
    public void process(OrderEvent event) {
        // Demo: negative amounts always fail to trigger the DLQ path
        if (event.amount().compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException(
                    "Invalid negative amount for orderId=" + event.orderId());
        }

        // Demo: simulate occasional transient failures (10% chance) to show retry
        if (random.nextInt(10) == 0) {
            throw new RuntimeException(
                    "Simulated transient failure for orderId=" + event.orderId());
        }

        // Stamp processed time and persist
        event.setProcessedAt(Instant.now());
        orderEventRepository.save(event);

        log.info("Order persisted: orderId={} type={} amount={}",
                event.orderId(), event.eventType(), event.amount());
    }
}
