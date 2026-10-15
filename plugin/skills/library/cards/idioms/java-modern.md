---
name: java-modern
title: Modern Java
area: idioms
tags: [java, records, sealed, pattern-matching, streams, optional]
detect: []
related: [java, java-virtual-threads, junit, maven]
---
Modern Java idioms: records for data, sealed types with pattern matching, immutable collections, `var` where the type is obvious.

## Verify
- `mvn -q verify`: compile, test and package for Maven projects (or `./gradlew check` for Gradle).
- `java -version`: the runtime matches the `release` or toolchain the build targets.
- `mvn -q test-compile`: sources and tests compile at the configured release.

## Test first
JUnit 5 with `assertThrows` and a record-based fixture.
```java
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class MoneyTest {
    @Test
    void rejectsNegativeAmounts() {
        assertThrows(IllegalArgumentException.class,
            () -> new Money(-1, "USD"));
    }
}
```
Put the check in the record's compact constructor to make it pass.

## Do
- Model immutable data as `record`, with validation in the compact constructor.
- Model closed alternatives as `sealed interface` plus records, and consume them with `switch` pattern matching, which the compiler checks for exhaustiveness.
- Use `instanceof` pattern matching: `if (o instanceof Circle c)`.
- Use text blocks for multi-line strings and `var` for obvious local types.
- Use `List.of`, `Map.of` and `Stream.toList()` for immutable results.
- Return `Optional` from lookups that may find nothing, and compose with `map` and `orElseThrow`.
- Use `try-with-resources` for everything `AutoCloseable`.
- Use `java.time` for dates and `Objects.requireNonNull` at API boundaries.

## Avoid
- `Optional` as a field, parameter or collection element: it adds noise and null risk. Use it for return values only.
- `Optional.get()` without a check: it throws. Use `orElseThrow()` with a message, or `ifPresent`.
- `java.util.Date` and `SimpleDateFormat`: mutable and not thread-safe. Use `java.time` and `DateTimeFormatter`.
- Raw types and unchecked casts: they defeat generics. Parameterize them.
- Long stream pipelines with side effects: hard to debug. Use a loop when mutation is the point.
- `==` on boxed values or strings: compares references. Use `equals`.
- Mutable getters returning internal collections: wrap in `List.copyOf` or return an unmodifiable view.

## Review
- [ ] Data carriers are records and alternatives are sealed with exhaustive switches.
- [ ] No `null` returned where a collection or `Optional` fits.
- [ ] Resources close through try-with-resources.
- [ ] Public APIs validate arguments.
- [ ] Language features used exist at the project's target release.
