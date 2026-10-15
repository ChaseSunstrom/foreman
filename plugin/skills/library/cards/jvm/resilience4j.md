---
name: resilience4j
title: Resilience4j
area: jvm
tags: [java, kotlin, resilience, circuit-breaker, retry, bulkhead, rate-limiter]
detect: [dep:resilience4j-circuitbreaker, dep:resilience4j-retry, dep:resilience4j-spring-boot3, dep:resilience4j-bulkhead, dep:resilience4j-ratelimiter, dep:resilience4j-timelimiter]
related: [spring-boot, spring-cloud, micrometer, spring-webflux, spring-kafka]
---
Resilience4j fault tolerance: circuit breaker, retry, bulkhead, rate limiter and time limiter composed in a deliberate order, with fallbacks and metrics.

## Verify
- `./gradlew test`: policy behavior tests pass.
- `curl -s localhost:8080/actuator/circuitbreakers`: breaker state per instance (needs actuator and the `circuitbreakers` endpoint exposed).
- `curl -s localhost:8080/actuator/health`: breaker health indicators appear when `registerHealthIndicator: true`.
- `curl -s localhost:8080/actuator/retryevents`: recent retry events.

## Test first
Drive the breaker through its transitions in a unit test with a small window.
```java
class BreakerTest {
  @Test void opensAfterFailureRate() {
    var cb = CircuitBreaker.of("x", CircuitBreakerConfig.custom()
        .slidingWindowSize(4).minimumNumberOfCalls(4)
        .failureRateThreshold(50).build());
    for (int i = 0; i < 4; i++) {
      try { cb.executeSupplier(() -> { throw new IllegalStateException(); }); }
      catch (IllegalStateException ignored) {}
    }
    assertEquals(CircuitBreaker.State.OPEN, cb.getState());
    assertThrows(CallNotPermittedException.class, () -> cb.executeSupplier(() -> "ok"));
  }
}
```

## Do
- Configure instances in `application.yml` under `resilience4j.circuitbreaker.instances.NAME` (`slidingWindowSize`, `minimumNumberOfCalls`, `failureRateThreshold`, `waitDurationInOpenState`, `permittedNumberOfCallsInHalfOpenState`), and reference them with `@CircuitBreaker(name = "NAME", fallbackMethod = "...")`.
- Compose in this order outside-in: Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( call ))))), which is the annotation aspect default order.
- Retry: set `maxAttempts`, `waitDuration` with `enableExponentialBackoff`, and `retryExceptions`/`ignoreExceptions` explicitly; retry only idempotent calls.
- Set `recordExceptions`/`ignoreExceptions` so business errors (404, validation) do not trip the breaker.
- Fallback methods must have the same return type and an extra last parameter of the exception type.
- Use `Bulkhead` (semaphore or thread-pool) to cap concurrency per dependency.
- Reactive: use the `resilience4j-reactor` operators (`transformDeferred(CircuitBreakerOperator.of(cb))`).
- Export metrics through Micrometer and alert on open state.

## Avoid
- Retry around a non-idempotent POST: duplicate side effects. Add idempotency keys or skip retry.
- Self-invocation of an annotated method inside the same class: the proxy is bypassed and no policy applies. Call through another bean.
- Breaker counting every exception, including 4xx: opens on client mistakes. Set `ignoreExceptions`.
- `@TimeLimiter` on a non-async method: needs a `CompletableFuture` or reactive return. Return async types.
- Unbounded retries or `maxAttempts` large with long waits: ties up threads. Cap attempts and total time.
- Fallbacks that hide failure by returning stale data silently: log and meter fallback use.
- Using `resilience4j-spring-boot2` artifacts on Boot 3: use `resilience4j-spring-boot3`.

## Review
- [ ] Each remote call has timeout, bounded retry and breaker with explicit exception lists.
- [ ] Retried operations are idempotent.
- [ ] Annotations are invoked through proxies; aspect order is understood.
- [ ] Fallbacks are typed, logged and metered.
- [ ] State transitions are covered by a test.
