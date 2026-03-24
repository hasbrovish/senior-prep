package com.jayanti.pipeline.repository;

import com.jayanti.pipeline.model.DeadLetter;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DeadLetterRepository extends JpaRepository<DeadLetter, Long> {

    List<DeadLetter> findByResolvedFalseOrderByReceivedAtDesc();

    List<DeadLetter> findByOrderId(String orderId);
}
