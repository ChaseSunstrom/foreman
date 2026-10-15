---
name: micronaut
title: Micronaut
area: jvm
tags: [java, kotlin, micronaut, aot, rest, di]
detect: [dep:micronaut-http-server-netty, dep:micronaut-inject, dep:micronaut-runtime, dep:micronaut-test-junit5, file:micronaut-cli.yml]
related: [junit5, mockito, gradle, maven, jackson, testcontainers]
---
Micronaut services: compile-time DI and AOP, declarative HTTP clients, typed config, `@MicronautTest`.

## Verify
- `./gradlew test` (or `./mvnw test`): the suite passes with annotation processing run at compile time.
- `./gradlew run` (or `./mvnw mn:run`): the app boots with DI wired at build time.
- `curl -fs localhost:8080/health`: the health endpoint answers (needs `management` and `endpoints.health` enabled).
- `./gradlew nativeCompile`: GraalVM native build succeeds if the project targets native.

## Test first
`@MicronautTest` starts the embedded server; inject an `HttpClient` annotated `@Client("/")`.
```java
@MicronautTest
class ItemControllerTest {
  @Inject @Client("/") HttpClient client;

  @Test void blankNameIsBadRequest() {
    var req = HttpRequest.POST("/items", Map.of("name", ""));
    var e = assertThrows(HttpClientResponseException.class,
        () -> client.toBlocking().exchange(req));
    assertEquals(HttpStatus.BAD_REQUEST, e.getStatus());
  }
}
```
Replace beans with `@MockBean(Service.class)` methods.

## Do
- Add the annotation processors (`micronaut-inject-java`, `micronaut-http-validation`) in the annotationProcessor scope, or kapt/ksp for Kotlin.
- Define beans with `@Singleton` and constructor injection.
- Bind config with `@ConfigurationProperties` or `@EachProperty`; override via env vars (`MY_PROP` maps to `my.prop`).
- Use declarative `@Client` interfaces for outbound HTTP, with `@Retryable` and `@CircuitBreaker` when needed.
- Validate with `@Valid` and `@Introspected` on request types so introspection works without reflection.
- Return `HttpResponse` with explicit status for non-200 outcomes.
- Mark blocking work `@ExecuteOn(TaskExecutors.BLOCKING)` (older code used `IO`).

## Avoid
- Blocking calls on the Netty event loop: annotate with `@ExecuteOn(TaskExecutors.BLOCKING)`.
- Missing annotation processor in a build: beans are silently absent and you get `NoSuchBeanException` at runtime.
- Runtime reflection and classpath scanning in application code: defeats AOT and breaks native. Use `@Introspected` or `@ReflectiveAccess`.
- Spring-style `@Autowired`/`@Value`: use `@Inject` and `@Value("${...}")` or typed config.
- JSON models without `@Serdeable` when using `micronaut-serde`: serialization fails at runtime.
- `@MockBean` for a type with no `@Replaces` semantic confusion: the mock must match the bean type exactly.

## Review
- [ ] Annotation processors are configured for every module that defines beans.
- [ ] Request and response types are `@Serdeable` or `@Introspected` as the serializer requires.
- [ ] No blocking calls on the event loop.
- [ ] Config lives in typed beans and `application.yml`; no secrets committed.
- [ ] Native build still passes where it ships.
