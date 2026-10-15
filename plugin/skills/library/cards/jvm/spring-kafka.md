---
name: spring-kafka
title: Spring for Apache Kafka
area: jvm
tags: [java, spring, kafka, messaging, consumers, producers, retries]
detect: [dep:spring-kafka, dep:spring-kafka-test]
related: [spring-boot, testcontainers, jackson, micrometer, resilience4j, spring-boot-testing]
---
Spring Kafka producers and listeners: explicit serialization, offset and ack semantics, bounded retries with dead-letter topics, idempotent handlers.

## Verify
- `./gradlew test`: listener and producer tests pass against an embedded or containerized broker.
- `grep -rnE "enable-auto-commit|enable.auto.commit" src/main/resources`: auto-commit is off or deliberately on.
- `grep -rn "trusted.packages" src/main`: JSON deserializer trusted packages are narrow, not `*`.
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group GROUP`: lag and assignments on a real broker.

## Test first
`@EmbeddedKafka` (spring-kafka-test) or a Testcontainers `KafkaContainer`. Wait on the outcome, not on sleep.
```java
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = "orders")
class OrderListenerTest {
  @Autowired KafkaTemplate<String, String> template;
  @Autowired OrderRepo repo;

  @Test void duplicateMessageIsAppliedOnce() {
    template.send("orders", "k1", "{\"id\":\"o1\"}");
    template.send("orders", "k1", "{\"id\":\"o1\"}");
    await().atMost(Duration.ofSeconds(10)).untilAsserted(
        () -> assertThat(repo.countById("o1")).isEqualTo(1));
  }
}
```

## Do
- Set serializers explicitly (`StringSerializer`, `JsonSerializer`, or Avro) and `auto.offset.reset` knowingly.
- Handle failures with `DefaultErrorHandler` plus `DeadLetterPublishingRecoverer` and a `BackOff` (`FixedBackOff` or `ExponentialBackOff` with a max); mark non-retryable exceptions with `addNotRetryableExceptions`.
- Make handlers idempotent (dedupe by business key) since delivery is at least once.
- Use `ErrorHandlingDeserializer` wrapping the real deserializer so one poison record does not loop forever.
- Set `max.poll.interval.ms` and `max.poll.records` to cover handler time; keep handlers short.
- Producers: `acks=all` and `enable.idempotence=true`; key by entity id for ordering.
- Use `ContainerProperties.AckMode.MANUAL` only when acking after the side effect is needed.
- Use `@RetryableTopic` for non-blocking retries when ordering is not required.

## Avoid
- `JsonDeserializer` with `spring.json.trusted.packages=*`: remote type injection. List exact packages or use a type mapping.
- Swallowing exceptions in `@KafkaListener`: the offset advances and the record is lost. Rethrow so the error handler runs.
- Blocking retry with a long `BackOff` in the listener thread: rebalance via `max.poll.interval.ms`. Use retry topics.
- Sending without checking the future: `template.send(...)` is async; failures vanish. Handle the `CompletableFuture` result (the return type is `CompletableFuture` in recent versions, `ListenableFuture` in old ones).
- Deserialization failures without `ErrorHandlingDeserializer`: infinite redelivery loop.
- Tests with `Thread.sleep`: flaky. Use Awaitility.

## Review
- [ ] Failure path ends in a dead-letter topic with bounded retries.
- [ ] Handlers are idempotent and tested with duplicates.
- [ ] Trusted packages and serializers are explicit.
- [ ] Consumer timeouts fit worst-case handler time.
- [ ] Producer durability settings (`acks`, idempotence) are set.
