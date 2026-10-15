---
name: quarkus
title: Quarkus
area: jvm
tags: [java, kotlin, quarkus, rest, native, cdi]
detect: [dep:quarkus-rest, dep:quarkus-resteasy-reactive, dep:quarkus-resteasy, dep:quarkus-arc, dep:quarkus-junit5]
related: [junit5, testcontainers, maven, gradle, hibernate, jackson]
---
Quarkus services: CDI beans, REST endpoints, config via `application.properties`, dev mode, `@QuarkusTest`, native builds.

## Verify
- `./mvnw -q verify` (or `./gradlew build`): compile and tests, including `@QuarkusTest`.
- `./mvnw quarkus:dev`: dev mode boots with live reload and Dev Services.
- `./mvnw -q package -Dnative`: the native image builds (reflection and resource gaps appear here).
- `curl -fs localhost:8080/q/health`: SmallRye Health answers (needs `quarkus-smallrye-health`).

## Test first
`@QuarkusTest` boots the app once; REST Assured drives HTTP. Tests live in `src/test/java`.
```java
@QuarkusTest
class GreetingResourceTest {
  @Test void rejectsBlankName() {
    given().contentType("application/json").body("{\"name\":\"\"}")
      .when().post("/items")
      .then().statusCode(400);
  }
}
```
Use `@InjectMock` (quarkus-junit5-mockito) to mock beans.

## Do
- Use `quarkus-rest` (the current REST stack) with Jakarta REST annotations; return `Uni` or `Multi` only when the stack is reactive end to end.
- Inject with constructors or `@Inject`; scope beans explicitly (`@ApplicationScoped`).
- Bind settings with `@ConfigMapping` interfaces; override per profile with `%dev.`, `%test.`, `%prod.` prefixes.
- Rely on Dev Services for databases in dev and test instead of hand-started containers.
- Validate with `quarkus-hibernate-validator` and `@Valid`; map errors with `@ServerExceptionMapper`.
- Register reflection with `@RegisterForReflection` for classes used only through serialization in native builds.
- Keep startup work out of constructors; use `@Observes StartupEvent`.

## Avoid
- Blocking calls on an event-loop thread in reactive endpoints: add `@Blocking` or run on a worker.
- `private` injected fields: Quarkus ArC removes the reflection needed; use package-private or constructors.
- Spring-style assumptions (`@Autowired`, `@Value`): use CDI `@Inject` and `@ConfigProperty`.
- Old `quarkus-resteasy-reactive` artifact names in new code: the extension was renamed `quarkus-rest`.
- Reading `System.getenv` directly: bypasses config profiles. Use config injection.
- Dynamic classpath scanning or reflection in native-bound code: it fails at runtime. Declare it at build time.
- Mixing `quarkus-bom` versions with plugin versions: set `quarkus.platform.version` once.

## Review
- [ ] Tests run with `@QuarkusTest` and cover a failure path per endpoint.
- [ ] Native build still passes if the project ships native.
- [ ] Profile-specific config uses `%prod.` for production values; no secrets committed.
- [ ] No blocking I/O on event-loop threads.
- [ ] Health, readiness and metrics extensions are present for deployments.
