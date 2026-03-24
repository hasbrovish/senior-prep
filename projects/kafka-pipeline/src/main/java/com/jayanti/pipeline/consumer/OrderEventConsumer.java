package com.jayanti.pipeline.consumer;

import com.jayanti.pipeline.model.OrderEvent;
import com.jayanti.pipeline.service.IdempotencyService;
import com.jayanti.pipeline.service.OrderProcessingService;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

/**
 * Main Kafka consumer with DLQ routing after 3 failures.
 *
 * Pattern: at-least-once delivery + Redis idempotency = exactly-once business outcome.
 *
 * Interview talking point: "This is the same pattern from my GSTN Kafka framework —
 * base Consumer class with Template Method, DLQ after N retries, Redis dedup.
 * At GSTN we processed 2M+ events/day with zero data loss."
 */
@Slf4j
@Component
public class OrderEventConsumer {

    private static final int MAX_RETRY_ATTEMPTS = 3;

    private final OrderProcessingService processingService;
    private final IdempotencyService idempotencyService;
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;
    private final Counter processedCounter;
    private final Counter dlqCounter;
    private final Counter duplicateCounter;

    @Value("${app.kafka.topics.order-events-dlq}")
    private String dlqTopic;

    public OrderEventConsumer(OrderProcessingService processingService,
                               IdempotencyService idempotencyService,
                               KafkaTemplate<String, OrderEvent> kafkaTemplate,
                               MeterRegistry registry) {
        this.processingService  = processingService;
        this.idempotencyService = idempotencyService;
        this.kafkaTemplate      = kafkaTemplate;
        this.processedCounter   = Counter.builder("kafka.consumer.processed").register(registry);
        this.dlqCounter         = Counter.builder("kafka.consumer.dlq.sent").register(registry);
        this.duplicateCounter   = Counter.builder("kafka.consumer.duplicates").register(registry);
    }

    @KafkaListener(
            topics      = "${app.kafka.topics.order-events}",
            groupId     = "${spring.kafka.consumer.group-id}",
            concurrency = "3"
    )
    public void consume(ConsumerRecord<String, OrderEvent> record, Acknowledgment ack) {
        OrderEvent event = record.value();
        log.info("Received: orderId={} partition={} offset={}",
                event.orderId(), record.partition(), record.offset());

        // Idempotency check — skip if already processed (Redis SET NX)
        if (!idempotencyService.markAsProcessing(event.orderId())) {
            log.warn("Duplicate event skipped: orderId={}", event.orderId());
            duplicateCounter.increment();
            ack.acknowledge(); // still commit offset
            return;
        }

        int attempts = 0;
        while (attempts < MAX_RETRY_ATTEMPTS) {
            try {
                processingService.process(event);
                processedCounter.increment();
                idempotencyService.markAsCompleted(event.orderId());
                ack.acknowledge(); // manual commit only on success
                log.info("Processed: orderId={}", event.orderId());
                return;
            } catch (Exception e) {
                attempts++;
                log.warn("Processing failed (attempt {}/{}): orderId={} error={}",
                        attempts, MAX_RETRY_ATTEMPTS, event.orderId(), e.getMessage());
                if (attempts < MAX_RETRY_ATTEMPTS) {
                    sleep(attempts * 1000L); // backoff: 1s, 2s
                }
            }
        }

        // All retries exhausted — send to DLQ
        log.error("Sending to DLQ after {} failures: orderId={}", MAX_RETRY_ATTEMPTS, event.orderId());
        kafkaTemplate.send(dlqTopic, event.orderId(), event);
        dlqCounter.increment();
        idempotencyService.markAsFailed(event.orderId());
        ack.acknowledge(); // commit offset so we don't re-process indefinitely
    }

    private void sleep(long millis) {
        try { Thread.sleep(millis); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }
}
