package com.jayanti.pipeline.producer;

import com.jayanti.pipeline.model.OrderEvent;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

/**
 * Idempotent Kafka producer.
 *
 * Config: enable.idempotence=true, acks=all, retries=Integer.MAX_VALUE
 * This guarantees exactly-once delivery to the broker (producer side).
 *
 * Interview talking point: "Idempotent producer + acks=all + manual consumer
 * offset commit gives us at-least-once end-to-end with dedup via Redis."
 */
@Slf4j
@Service
public class OrderEventProducer {

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;
    private final Counter sentCounter;
    private final Counter failCounter;

    @Value("${app.kafka.topics.order-events}")
    private String ordersTopic;

    public OrderEventProducer(KafkaTemplate<String, OrderEvent> kafkaTemplate,
                               MeterRegistry registry) {
        this.kafkaTemplate = kafkaTemplate;
        this.sentCounter  = Counter.builder("kafka.producer.sent")
                .tag("topic", "order-events")
                .description("Total order events sent to Kafka")
                .register(registry);
        this.failCounter  = Counter.builder("kafka.producer.failed")
                .tag("topic", "order-events")
                .description("Total send failures")
                .register(registry);
    }

    /**
     * Send event to Kafka using orderId as partition key.
     * Same orderId always goes to same partition → ordering guaranteed per order.
     */
    public CompletableFuture<SendResult<String, OrderEvent>> send(OrderEvent event) {
        log.info("Sending event: orderId={} type={}", event.orderId(), event.eventType());

        CompletableFuture<SendResult<String, OrderEvent>> future =
                kafkaTemplate.send(ordersTopic, event.orderId(), event);

        future.whenComplete((result, ex) -> {
            if (ex != null) {
                failCounter.increment();
                log.error("Failed to send event orderId={}: {}", event.orderId(), ex.getMessage());
            } else {
                sentCounter.increment();
                log.debug("Sent orderId={} to partition={} offset={}",
                        event.orderId(),
                        result.getRecordMetadata().partition(),
                        result.getRecordMetadata().offset());
            }
        });

        return future;
    }
}
