package com.jayanti.pipeline.consumer;

import com.jayanti.pipeline.model.DeadLetter;
import com.jayanti.pipeline.model.OrderEvent;
import com.jayanti.pipeline.service.DeadLetterService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

/**
 * Dead Letter Queue consumer.
 * Reads from order-events-dlq, persists each failed event to the dead_letters
 * table for ops review, alerting, and eventual manual replay.
 *
 * Interview talking point: "DLQ consumers are completely separate from main consumers.
 * The ops team reviews the dead_letters table daily via a dashboard. We alert when
 * DLQ lag exceeds 100 messages — that means something systemic is wrong.
 * At GSTN we had the same pattern: GSTN-DLQ topic consumed by a separate pod."
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DlqConsumer {

    private final DeadLetterService deadLetterService;

    @KafkaListener(
            topics  = "${app.kafka.topics.order-events-dlq}",
            groupId = "order-processing-group-dlq"
    )
    public void consume(ConsumerRecord<String, OrderEvent> record, Acknowledgment ack) {
        OrderEvent event = record.value();
        log.error("DLQ message received: orderId={} eventType={} partition={} offset={}",
                event.orderId(), event.eventType(), record.partition(), record.offset());

        // Persist to dead_letters table for ops review
        // retryCount is not tracked in the DLQ payload in this design,
        // so we use MAX_RETRY_ATTEMPTS as the default.
        DeadLetter dl = new DeadLetter(
                event.orderId(),
                event.toString(),
                "MAX_RETRIES_EXCEEDED",
                3
        );
        deadLetterService.save(dl);

        ack.acknowledge(); // always commit from DLQ — we have persisted it
    }
}
