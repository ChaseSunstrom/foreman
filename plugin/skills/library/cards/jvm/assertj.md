---
name: assertj
title: AssertJ
area: jvm
tags: [java, kotlin, testing, assertions, fluent, collections, exceptions]
detect: [dep:assertj-core, dep:assertj-db, dep:assertj-guava]
related: [junit5, mockito, spring-boot-testing, archunit, kotest]
---
AssertJ fluent assertions: one `assertThat` entry point, precise collection, exception and object-graph checks, soft assertions for grouped failures.

## Verify
- `./gradlew test`: assertions hold.
- `mvn -q test`: same on Maven.
- `grep -rnE "assertTrue\(.*(equals|contains|isEmpty|size)" src/test`: JUnit boolean assertions that lose failure detail.
- `grep -rn "org.junit.Assert\." src/test`: old JUnit 4 asserts mixed into an AssertJ suite.

## Test first
```java
import static org.assertj.core.api.Assertions.*;

class CartTest {
  @Test void totalsAndRejectsNegativeQuantity() {
    var cart = new Cart();
    cart.add("apple", 2);
    assertThat(cart.items())
        .extracting(Item::name, Item::qty)
        .containsExactly(tuple("apple", 2));
    assertThatThrownBy(() -> cart.add("pear", -1))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining("quantity");
  }
}
```
Import from `org.assertj.core.api.Assertions` (or `BDDAssertions`).

## Do
- Use typed assertions: `assertThat(list).hasSize(3).contains(x)`, `containsExactly` for order, `containsExactlyInAnyOrder` for sets, `isEqualTo` for objects.
- Extract fields with `extracting("name")`, or method refs, then assert; `filteredOn` to select first.
- Compare objects by fields with `usingRecursiveComparison().ignoringFields("id", "createdAt").isEqualTo(expected)`.
- Use `assertThatThrownBy` or `assertThatExceptionOfType(...).isThrownBy(...)` and also check message and cause (`hasCauseInstanceOf`).
- Group independent checks with `SoftAssertions.assertSoftly(s -> { ... })` or the JUnit 5 `SoftAssertionsExtension`.
- Doubles: `isCloseTo(x, within(0.01))`; dates: `isBefore`, `isCloseTo`, with a fixed `Clock` rather than now.
- Custom `Condition` or `as("description")` and `describedAs` so failure messages explain intent.
- Async: pair with Awaitility `await().untilAsserted(() -> assertThat(...))`.
- Optionals and futures: `assertThat(opt).isPresent().get()`, `assertThat(future).succeedsWithin(Duration)`.

## Avoid
- `assertThat(x)` with no assertion call: the check never runs and passes. Static analysis (`assertj-errorprone`) can catch it; add an assertion.
- `assertTrue(list.contains(x))`: failure says only "expected true". Use `assertThat(list).contains(x)`.
- `assertThat(a.equals(b)).isTrue()`: no diff output. Use `isEqualTo`.
- `isEqualTo` on objects without `equals`: compares identity. Use recursive comparison.
- `usingRecursiveComparison()` ignoring many fields to force a pass: hides defects. Ignore only generated values.
- Catching exceptions manually with try/fail/catch: use `assertThatThrownBy`.
- Mixing Hamcrest `assertThat` and AssertJ imports: wrong overload, confusing messages.

## Review
- [ ] Every `assertThat` is followed by an assertion method.
- [ ] Failure messages would identify the problem without a debugger.
- [ ] Time and randomness are controlled; floating point uses tolerances.
- [ ] Exception tests check type and message.
- [ ] Only one assertion library style per test class.
