---
name: junit5
title: JUnit 5
area: jvm
tags: [java, kotlin, junit, testing, jupiter, assertions]
detect: [dep:junit-jupiter, dep:junit-jupiter-api, dep:junit-jupiter-engine, dep:junit-jupiter-params]
related: [mockito, testcontainers, maven, gradle, spring-boot]
---
JUnit 5 (Jupiter) tests: lifecycle, parameterized tests, nested classes, extensions, assertions.

## Verify
- `./mvnw -q test` (or `./gradlew test`): the suite runs on the Jupiter engine.
- `./mvnw -q test -Dtest=PriceTest#negativeQuantityThrows`: one method runs (Gradle: `./gradlew test --tests 'PriceTest.negativeQuantityThrows'`).
- `./gradlew test --info | grep -c "PASSED"`: tests were discovered, not silently skipped.
- `./mvnw -q dependency:tree | grep -i junit`: no JUnit 4 vintage engine left unintentionally.

## Test first
Tests sit in `src/test/java` mirroring the package; name the behavior, not the method.
```java
import static org.junit.jupiter.api.Assertions.*;

class PriceTest {
  @Test void negativeQuantityThrows() {
    var ex = assertThrows(IllegalArgumentException.class, () -> Price.total(10, -1));
    assertEquals("quantity must be >= 0", ex.getMessage());
  }
}
```

## Do
- Import from `org.junit.jupiter.api` (`Test`, `BeforeEach`, `DisplayName`); package-private tests are fine.
- Use `@ParameterizedTest` with `@CsvSource`, `@ValueSource` or `@MethodSource` for table-style cases (needs `junit-jupiter-params`).
- Group cases with `@Nested` classes; share setup with `@BeforeEach`.
- Use `assertThrows`, `assertAll` for related checks, and `@TempDir` for files.
- Reuse logic with extensions (`@ExtendWith`), registered per class or programmatically with `@RegisterExtension`.
- Set `@Timeout` on tests that could hang.
- On Gradle, call `useJUnitPlatform()` in the `test` task; on Maven keep Surefire recent enough for the platform.

## Avoid
- `org.junit.Test` or `@RunWith`: JUnit 4, ignored by Jupiter. Use `org.junit.jupiter.api.Test` and `@ExtendWith`.
- Missing `useJUnitPlatform()` in Gradle: zero tests run and the build is green.
- `@BeforeClass`/`@AfterClass`: renamed `@BeforeAll`/`@AfterAll`, which must be `static` unless `@TestInstance(PER_CLASS)`.
- `@Ignore`: it is `@Disabled`, and give a reason.
- Asserting with `assertTrue(a.equals(b))`: failure messages are useless. Use `assertEquals`.
- Expected-exception try/catch with no `fail()`: the test passes when nothing throws. Use `assertThrows`.
- Tests sharing mutable static state: order is not guaranteed.

## Review
- [ ] Tests discovered by the Jupiter engine; the count is non-zero.
- [ ] Each test has one clear reason to fail and meaningful assertion messages.
- [ ] Parameterized cases cover edges (empty, null, boundary).
- [ ] No sleeps; time and randomness are injected.
- [ ] No leftover `@Disabled` without an issue reference.
