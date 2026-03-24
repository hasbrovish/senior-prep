package com.jayanti.pipeline.repository;

import com.jayanti.pipeline.model.OrderEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface OrderEventRepository extends JpaRepository<OrderEvent, String> {
}
