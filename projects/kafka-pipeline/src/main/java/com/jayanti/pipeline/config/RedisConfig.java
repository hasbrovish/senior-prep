package com.jayanti.pipeline.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * Redis configuration for idempotency checks.
 *
 * We use StringRedisTemplate (not the generic RedisTemplate) because our
 * idempotency keys and values are plain strings. This avoids Java serialization
 * overhead and makes keys human-readable in Redis CLI.
 *
 * Key pattern: "idempotency:order:{orderId}"
 * TTL: 86400 seconds (24 hours) — configurable via app.idempotency.ttl-seconds
 */
@Configuration
public class RedisConfig {

    /**
     * StringRedisTemplate is sufficient for idempotency key/value operations.
     * Uses StringRedisSerializer for both key and value.
     */
    @Bean
    public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory connectionFactory) {
        StringRedisTemplate template = new StringRedisTemplate();
        template.setConnectionFactory(connectionFactory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new StringRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
