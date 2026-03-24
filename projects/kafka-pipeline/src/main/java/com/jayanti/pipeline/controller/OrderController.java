package com.jayanti.pipeline.controller;

import com.jayanti.pipeline.model.OrderEvent;
import com.jayanti.pipeline.producer.OrderEventProducer;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Map;

/**
 * REST entry point for publishing order events.
 * In production this would come from an upstream service or message bus.
 * Here it's a simple HTTP endpoint for demo and testing.
 */
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);

    private final OrderEventProducer producer;

    public OrderController(OrderEventProducer producer) {
        this.producer = producer;
    }

    @PostMapping
    public ResponseEntity<Map<String, String>> publishOrder(
            @Valid @RequestBody OrderRequest request) {

        OrderEvent event = new OrderEvent(
                request.orderId(),
                request.userId(),
                request.amount(),
                request.eventType(),
                Instant.now()
        );

        producer.sendAsync(event);
        log.info("Order event queued: orderId={}", request.orderId());

        return ResponseEntity.accepted()
                .body(Map.of(
                        "status", "QUEUED",
                        "orderId", request.orderId(),
                        "message", "Event published to Kafka"
                ));
    }

    // ──────────────────────────────────────────
    // Request DTO (Java 16+ record)
    // ──────────────────────────────────────────
    public record OrderRequest(
            @NotBlank String orderId,
            @NotBlank String userId,
            @NotNull  BigDecimal amount,
            @NotBlank String eventType
    ) {}
}
