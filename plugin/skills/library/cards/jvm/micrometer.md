---
name: micrometer
title: Micrometer
area: jvm
tags: [java, kotlin, metrics, observability, prometheus, tracing, spring]
detect: [dep:micrometer-core, dep:micrometer-registry-prometheus, dep:micrometer-tracing, dep:micrometer-observation]
related: [spring-boot, spring-webflux, resilience4j, spring-kafka, spring-cloud]
---
Micrometer metrics and observations: bounded-cardinality tags, the right meter type, a registry per backend, and tests against `SimpleMeterRegistry`.

## Verify
- `./gradlew test`: metric tests pass.
- `curl -s localhost:8080/actuator/metrics`: lists meter names (the `metrics` endpoint must be exposed).
- `curl -s localhost:8080/actuator/prometheus`: scrape output with expected names and tags (needs `micrometer-registry-prometheus`).
- `curl -s "localhost:8080/actuator/metrics/http.server.requests?tag=status:500"`: tag drill-down on a real meter.

## Test first
Use `SimpleMeterRegistry` and assert the meter, name, tags and value.
```java
class CheckoutMetricsTest {
  @Test void failureIncrementsTaggedCounter() {
    var registry = new SimpleMeterRegistry();
    var svc = new Checkout(registry);
    assertThrows(PaymentException.class, () -> svc.pay("card", -1));
    assertEquals(1.0, registry.get("checkout.failures").tag("reason", "invalid").counter().count());
  }
}
```
For Spring, `@SpringBootTest` with `@AutoConfigureObservability` when metrics are disabled in tests.

## Do
- Pick the meter type: `Counter` for events, `Timer` for durations and rates, `DistributionSummary` for sizes, `Gauge` for current values from a held reference.
- Name with dots and lowercase (`orders.created`); the registry converts per backend. Put units in base units or `baseUnit(...)`.
- Keep tags low-cardinality (status, outcome, type); never user ids, URLs with ids or raw error messages.
- Build meters once and reuse (`Counter.builder(...).register(registry)`), not on every call, or use the builder with a bounded tag set.
- Add common tags via `management.metrics.tags.application=...` and a `MeterFilter` for renames or caps (`MeterFilter.maximumAllowableTags`).
- Enable timer percentiles/histograms deliberately: `management.metrics.distribution.percentiles-histogram.http.server.requests=true`.
- Use the Observation API (`Observation.createNotStarted(...).observe(...)`) to get metrics and traces from one instrumentation point.
- Bound exposure: `management.endpoints.web.exposure.include=health,info,prometheus` and secure the management port.

## Avoid
- High-cardinality tags (user id, request path with id): memory blowup and a huge scrape. Use templated URIs and enumerations.
- `Gauge` over a temporary object: it is held weakly and reads `NaN` once collected. Keep a strong reference or use `registry.gauge(name, obj, fn)` with a long-lived obj.
- Registering the same name with different tag keys: the registry rejects or drops. Keep tag key sets identical.
- Creating `new SimpleMeterRegistry()` in production code: metrics never reach the backend. Inject the application registry.
- Timing with `System.currentTimeMillis` and a counter: lose percentiles. Use `Timer.record` or `@Timed` with `TimedAspect`.
- Exposing all actuator endpoints publicly: leaks internals.

## Review
- [ ] Tags come from bounded sets and are identical per meter name.
- [ ] Meter types and base units match what is measured.
- [ ] Meters are created once and the injected registry is used.
- [ ] Tests assert names, tags and values with `SimpleMeterRegistry`.
- [ ] Actuator exposure is minimal and secured.
