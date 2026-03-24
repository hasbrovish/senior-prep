package com.jayanti.pipeline.service;

import com.jayanti.pipeline.model.DeadLetter;
import com.jayanti.pipeline.repository.DeadLetterRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Service for managing dead letter entries.
 * Used by DlqConsumer to persist failed events, and by ops endpoints for review.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class DeadLetterService {

    private final DeadLetterRepository deadLetterRepository;

    public void save(DeadLetter deadLetter) {
        deadLetterRepository.save(deadLetter);
        log.error("Dead letter persisted: orderId={} reason={}",
                deadLetter.getOrderId(), deadLetter.getFailureReason());
    }

    public List<DeadLetter> findUnresolved() {
        return deadLetterRepository.findByResolvedFalseOrderByReceivedAtDesc();
    }

    public void markResolved(Long id) {
        deadLetterRepository.findById(id).ifPresent(dl -> {
            dl.setResolved(true);
            deadLetterRepository.save(dl);
            log.info("Dead letter resolved: id={} orderId={}", id, dl.getOrderId());
        });
    }
}
