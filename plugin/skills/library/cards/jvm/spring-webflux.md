---
name: spring-webflux
title: Spring WebFlux
area: jvm
tags: [java, kotlin, spring, reactive, webflux, reactor, netty]
detect: [dep:spring-boot-starter-webflux, dep:spring-webflux, dep:reactor-core, dep:reactor-test]
related: [spring-boot, kotlin-coroutines, spring-boot-testing, resilience4j, micrometer, testcontainers]
---
Reactive Spring on Reactor and Netty: Mono/Flux pipelines, WebClient, functional or annotated endpoints, no blocking on event-loop threads.

## Verify
- `./gradlew test` (or `mvn -q test`): the suite, including StepVerifier and WebTestClient tests.
- `./gradlew dependencies --configuration runtimeClasspath | grep -E "spring-boot-starter-web( |$)"`: spring-web (servlet) is not also on the classpath, or Boot silently picks MVC.
- `grep -rnE "\.block\(|Thread\.sleep|\.toFuture\(\)\.get" src/main`: no blocking calls in reactive code.
- `./gradlew test -Dreactor.schedulers.defaultPoolSize=1`: still passes when a single scheduler thread is available (exposes hidden blocking).

## Test first
`StepVerifier` for publishers, `WebTestClient` for endpoints. Tests live in `src/test`.
```java
@WebFluxTest(ItemController.class)
class ItemControllerTest {
  @Autowired WebTestClient client;
  @MockitoBean ItemService service;

  @Test void missingItemIs404() {
    when(service.find("x")).thenReturn(Mono.empty());
    client.get().uri("/items/x").exchange().expectStatus().isNotFound();
  }
}
```
`@MockitoBean` replaced `@MockBean` in Boot 3.4+. Use `@MockBean` on older versions.

## Do
- Return `Mono`/`Flux` from every layer and let the framework subscribe. Compose with `map`, `flatMap`, `zip`, `switchIfEmpty`.
- Set timeouts on every `WebClient` call (`.timeout(Duration)` plus connect and response timeouts on the Reactor Netty `HttpClient`) and build one `WebClient` from the injected `WebClient.Builder`.
- Wrap unavoidable blocking calls (JDBC, files) in `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())`.
- Use `Mono.defer` for work that must happen per subscription, not at assembly time.
- Handle errors with `onErrorResume`, `onErrorMap`, `retryWhen(Retry.backoff(...))`; map domain errors in `@ControllerAdvice` or `WebExceptionHandler`.
- Kotlin: prefer `suspend` controllers and `Flow`; they bridge to Reactor automatically.
- Use `StepVerifier.withVirtualTime` for delays and retries instead of real sleeps.

## Avoid
- `.block()` or `.blockFirst()` in a handler: it throws `IllegalStateException` on a Netty thread (or deadlocks elsewhere). Chain with `flatMap`.
- Subscribing inside a `map` or `doOnNext`: errors and cancellation are lost. Use `flatMap`.
- Calling `.subscribe()` in a request path to "fire and forget": no backpressure, no error handling. Return the publisher, or use `.subscribe(ok, err)` deliberately.
- Mixing `spring-boot-starter-web` and webflux starters expecting reactive: MVC wins. Remove the servlet starter.
- Storing request state in `ThreadLocal`/MDC: threads hop. Use the Reactor `Context` and `contextWrite`.
- Reading `WebClient` bodies you never consume (`retrieve()` without `bodyToMono`): connection leaks. Always consume or `releaseBody()`.

## Review
- [ ] No blocking call on event-loop threads; blocking work is isolated on `boundedElastic`.
- [ ] Every outbound call has a timeout and a bounded retry.
- [ ] Nothing is subscribed manually inside the pipeline.
- [ ] Tests assert completion, errors and empty cases with `StepVerifier` or `WebTestClient`.
- [ ] Streaming endpoints respect backpressure and cap buffering (`limitRate`, `bufferTimeout`).
