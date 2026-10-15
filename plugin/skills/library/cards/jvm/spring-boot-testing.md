---
name: spring-boot-testing
title: Spring Boot testing
area: jvm
tags: [java, kotlin, spring, testing, slices, mockmvc, testcontainers]
detect: [dep:spring-boot-starter-test, dep:spring-boot-testcontainers, dep:spring-security-test]
related: [spring-boot, junit5, mockito, testcontainers, spring-data-jpa, spring-security, assertj]
---
Spring Boot test slices over full contexts: `@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, with real databases via Testcontainers and cached contexts.

## Verify
- `./gradlew test` (or `mvn -q test`): all slices and integration tests pass.
- `./gradlew test --tests "*ControllerTest"`: web slice only, fast feedback.
- `grep -rc "@SpringBootTest" src/test`: count of full-context tests; keep it small.
- `./gradlew test -i | grep -c "Started .* in"`: number of contexts started; a high count means cache misses.

## Test first
Smallest slice that exercises the behavior.
```java
@WebMvcTest(ItemController.class)
class ItemControllerTest {
  @Autowired MockMvc mvc;
  @MockitoBean ItemService service;

  @Test void blankNameIs400() throws Exception {
    mvc.perform(post("/items").contentType("application/json")
          .content("{\"name\":\"\"}"))
       .andExpect(status().isBadRequest());
  }
}
```
`@MockitoBean` is Boot 3.4+ (`@MockBean` before). Tests live in `src/test/java`, mirroring main packages.

## Do
- Pick the slice: `@WebMvcTest` (controllers, advice, security filters), `@DataJpaTest` (repositories), `@JsonTest`, `@RestClientTest`; use `@SpringBootTest` only for wiring and end-to-end flows.
- Use a real database in repository tests via `@ServiceConnection` on a Testcontainers container, with `@AutoConfigureTestDatabase(replace = NONE)` when `@DataJpaTest` should not swap in H2.
- With Spring Security, add `spring-security-test` and use `@WithMockUser` or `SecurityMockMvcRequestPostProcessors.jwt()`; assert 401 and 403, not only success.
- Share one container and configuration across classes so the context cache is reused; avoid `@DirtiesContext`.
- Override properties with `@TestPropertySource` or `@DynamicPropertySource`.
- Use `@SpringBootTest(webEnvironment = RANDOM_PORT)` with `TestRestTemplate` or `WebTestClient` for real HTTP.
- Use Awaitility for async outcomes.

## Avoid
- `@SpringBootTest` for every test: slow suites. Use a slice.
- `@DirtiesContext` as a cleanup tool: kills context caching. Reset state in `@BeforeEach` or use `@Transactional` rollback.
- `@Transactional` on tests that hit a `RANDOM_PORT` server: the server runs in another thread and never sees the data. Insert and clean explicitly.
- H2 standing in for Postgres or MySQL: dialect drift hides bugs. Use Testcontainers.
- Varying `@MockitoBean`/`@MockBean` sets per class: each combination builds a new context. Centralize them in a base config.
- Hardcoded ports: use `@LocalServerPort`.

## Review
- [ ] Each test uses the narrowest slice that proves the behavior.
- [ ] Repository tests run against the production database engine.
- [ ] Security rules have negative tests.
- [ ] Context count stays low; no gratuitous `@DirtiesContext`.
- [ ] No sleeps; async waits use Awaitility.
