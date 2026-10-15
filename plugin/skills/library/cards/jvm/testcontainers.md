---
name: testcontainers
title: Testcontainers
area: jvm
tags: [java, kotlin, testing, docker, integration, database]
detect: [dep:testcontainers, dep:postgresql, dep:junit-jupiter, dep:spring-boot-testcontainers]
related: [junit5, spring-boot, spring-data-jpa, flyway, liquibase, quarkus]
---
Testcontainers: real databases and brokers in Docker for integration tests, with reuse, wait strategies and dynamic properties.

## Verify
- `docker info`: the Docker daemon the tests need is reachable.
- `./mvnw -q verify` (or `./gradlew integrationTest`): container-backed tests start, run and clean up.
- `docker ps -a --filter label=org.testcontainers=true`: no leaked containers after the run (Ryuk reaps them).
- `./mvnw -q dependency:tree | grep -i testcontainers`: module versions match the core artifact.

## Test first
Start the container once per class and inject its coordinates into the app. Use the JUnit 5 extension.
```java
@Testcontainers
@SpringBootTest
class ItemRepositoryIT {
  @Container @ServiceConnection
  static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");

  @Autowired ItemRepository repo;

  @Test void persistsAndReads() {
    var saved = repo.save(new Item("a"));
    assertTrue(repo.findById(saved.getId()).isPresent());
  }
}
```
Outside Spring Boot use `@DynamicPropertySource` to register `pg::getJdbcUrl`.

## Do
- Pin an exact image tag matching production's major version.
- Declare containers `static` for one start per class; share across classes with a singleton holder.
- Use `@ServiceConnection` (Spring Boot 3.1 and later) or `@DynamicPropertySource`; never hardcode ports.
- Apply real migrations (Flyway or Liquibase) to the container, not `create-drop`.
- Use wait strategies (`Wait.forListeningPort()`, `Wait.forLogMessage`) for custom images.
- Name integration tests `*IT` so the build runs them in the right phase.
- Use `GenericContainer` and `withExposedPorts` for services without a module; read the mapped port with `getMappedPort`.

## Avoid
- Non-static `@Container` fields: a fresh container per test method, very slow.
- Hardcoded `localhost:5432` in properties: the host port is random. Read it from the container.
- `latest` image tags: unreproducible failures.
- Using H2 as a stand-in for Postgres semantics: dialect gaps hide bugs. Test against the real engine.
- Disabling Ryuk to make CI work without understanding the cause: containers then leak.
- Sleeping until a service is ready: use a wait strategy.
- Assuming Docker in every environment: gate with `@Testcontainers(disabledWithoutDocker = true)` where that is intended.

## Review
- [ ] Image tags are pinned and match production.
- [ ] Container lifecycle is per class or shared deliberately.
- [ ] Connection details are injected, not hardcoded.
- [ ] Schema comes from real migrations.
- [ ] CI has Docker available and runs the integration tests.
