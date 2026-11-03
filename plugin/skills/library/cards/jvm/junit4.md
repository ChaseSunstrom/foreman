---
name: junit4
title: JUnit 4
area: jvm
tags: [java, kotlin, junit, testing, assertions, rules]
detect: [dep:junit:junit]
related: [junit5, mockito, maven, gradle, android]
---
JUnit 4 tests (`org.junit.Test`): runners, rules, assertions and the vintage style that JUnit 5 replaces.

## Verify
- `./gradlew test` (or `./mvnw -q test`): the suite runs and reports its test count.
- `./gradlew test --tests 'PriceTest.negativeQuantityThrows'`: one method runs (Maven: `./mvnw -q test -Dtest=PriceTest#negativeQuantityThrows`).
- `./gradlew dependencies --configuration testRuntimeClasspath | grep junit`: one JUnit 4 version resolves.
- `./mvnw -q dependency:tree | grep -i junit`: no second JUnit copy comes in through another library.

## Test first
Tests sit in `src/test/java` mirroring the package. Name the behavior.
```java
import static org.junit.Assert.*;
import org.junit.Test;

public class PriceTest {
  @Test public void negativeQuantityThrows() {
    try {
      Price.total(10, -1);
      fail("expected IllegalArgumentException");
    } catch (IllegalArgumentException e) {
      assertEquals("quantity must be >= 0", e.getMessage());
    }
  }
}
```

## Do
- Put the expected value first: `assertEquals(expected, actual)`.
- Give assertions a message as the first argument when the failure would be unclear.
- Create shared fixtures in `@Before` and release them in `@After`.
- Use a `@Rule` such as `TemporaryFolder` for files, so cleanup runs even on failure.
- Use `@Category` to split slow or integration tests from the unit suite.
- Use `Assume` to skip a test when its environment is missing, instead of passing silently.
- Migrate with `junit-vintage-engine` only as a bridge; new tests use JUnit 5 (see the junit5 card).

## Avoid
- `@Test(expected = X.class)`: it passes if the exception comes from any line in the test. Use a `try`/`fail()` block or the `assertThrows` method if your version has it.
- `assertEquals(actual, expected)`: the failure message reads backwards. Put expected first.
- `@Ignore` with no reason: it is silent skipping. Give the reason in the annotation.
- `@BeforeClass` state that tests mutate: each test method runs on a fresh instance, but static state is shared.
- `assertTrue(a.equals(b))`: failures print `false`. Use `assertEquals`.
- Mixing `org.junit.Test` with JUnit 5 `@Test` in one class: the wrong annotation is ignored.
- Sleeping to wait for a background task: inject a clock or latch.

## Review
- [ ] The test count is non-zero; no test is silently ignored.
- [ ] Exception tests fail when nothing is thrown.
- [ ] Assertions state expected before actual, with messages where useful.
- [ ] Rules or `@After` release files and sockets on failure.
- [ ] `@Ignore` carries a reason.
