---
name: spring-boot
title: Spring Boot
area: jvm
tags: [java, kotlin, spring, web, api, actuator]
detect: [dep:spring-boot-starter-web, dep:spring-boot-starter, dep:spring-boot-starter-webflux, dep:spring-boot-starter-actuator]
related: [spring-security, spring-data-jpa, junit5, mockito, testcontainers, maven, gradle, jackson]
---
Spring Boot services: auto-configured starters, constructor injection, typed configuration, actuator, slice tests.

## Verify
- `./mvnw -q verify` (or `./gradlew check`): compile, unit and integration tests through the wrapper.
- `./mvnw -q dependency:tree -Dverbose` (or `./gradlew dependencies`): no conflicting starters (for example web and webflux together).
- `curl -fs localhost:8080/actuator/health`: the app boots and the health endpoint answers after `spring-boot:run` or `bootRun`.
- `./mvnw -q spring-boot:build-image` (or `./gradlew bootBuildImage`): the layered image builds.

## Test first
Use the narrowest slice: `@WebMvcTest` for controllers, `@DataJpaTest` for repositories, `@SpringBootTest` only for wiring. Tests live in `src/test/java` mirroring the main package.
```java
@WebMvcTest(ItemController.class)
class ItemControllerTest {
  @Autowired MockMvc mvc;
  @MockitoBean ItemService service;

  @Test void rejectsBlankName() throws Exception {
    mvc.perform(post("/items").contentType(APPLICATION_JSON).content("{\"name\":\"\"}"))
       .andExpect(status().isBadRequest());
  }
}
```

## Do
- Inject through constructors (a single constructor needs no `@Autowired`); keep fields `final`.
- Bind settings with `@ConfigurationProperties` records plus `@Validated`, not scattered `@Value`.
- Use profiles and `application-{profile}.yml`; keep secrets in environment variables.
- Validate request bodies with `@Valid` and Jakarta Bean Validation; map errors in one `@RestControllerAdvice` (or `ProblemDetail`).
- Put `@Transactional` on service methods, not controllers.
- Expose only needed actuator endpoints: `management.endpoints.web.exposure.include`.
- Return DTOs, not entities, from controllers.

## Avoid
- Field injection with `@Autowired`: hides dependencies and breaks plain unit tests. Use constructors.
- `javax.*` imports on Boot 3 and later: the namespace is `jakarta.*`.
- `@SpringBootTest` for every test: slow context start. Use slices and `@MockitoBean` (Boot 3.4 and later; `@MockBean` is deprecated there).
- `spring.jpa.hibernate.ddl-auto=update` in production: use Flyway or Liquibase migrations.
- `WebSecurityConfigurerAdapter`: removed; declare a `SecurityFilterChain` bean.
- Exposing `management.endpoints.web.exposure.include=*` publicly: leaks env and heap dumps.
- Catching exceptions in controllers to return 200: let the advice map them to status codes.

## Review
- [ ] No secrets or credentials in committed `application*.yml`.
- [ ] Each endpoint validates input and has a test for the failure path.
- [ ] Transactions are scoped on services; no lazy-loading entities leave the service layer.
- [ ] Actuator exposure and CORS are deliberate.
- [ ] Schema changes arrive as migrations, not `ddl-auto`.
