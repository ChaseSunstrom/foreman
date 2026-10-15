---
name: java
title: Java
area: lang
tags: [java, jvm, maven, gradle, junit, records]
detect: [ext:.java, file:pom.xml, file:build.gradle, file:build.gradle.kts, file:mvnw, file:gradlew]
related: [kotlin, scala, spring-boot, junit]
---
Java baseline: build via the Maven or Gradle wrapper, JUnit 5, modern language features, and null and resource discipline.

## Verify
- `./mvnw -q verify` (or `./gradlew build`): compile, tests and packaging through the repo wrapper.
- `./mvnw -q test -Dtest=ClassNameTest` (or `./gradlew test --tests ClassNameTest`): one class while iterating.
- `java -version`: the JDK matches the project's configured release.

## Test first
JUnit 5 under `src/test/java`, mirroring the package, class `FooTest`. Use `assertThrows` for failures.
```java
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;

class PortParserTest {
    @Test
    void rejectsEmpty() {
        assertThrows(IllegalArgumentException.class, () -> PortParser.parse(""));
    }
}
```

## Do
- Use the wrapper (`mvnw` or `gradlew`), not a global install; set `maven.compiler.release` or the Gradle toolchain.
- Use records for data carriers, `sealed` types with pattern-matching `switch` where the JDK allows, and `var` only when the type is obvious.
- Return `Optional` from lookups that may be empty; never as a field or parameter.
- Use try-with-resources for every `AutoCloseable`.
- Make classes immutable by default (`final` fields, `List.of`, `Map.copyOf`).
- Use `java.time` (`Instant`, `LocalDate`, `Clock` injected for tests).
- Use SLF4J with parameterized messages: `log.info("saved {}", id)`.

## Avoid
- `catch (Exception e) {}` or `e.printStackTrace()`: swallowed or unstructured errors. Log with the logger and rethrow or handle.
- `==` on strings and boxed values: compares references. Use `equals` or `Objects.equals`.
- `Date`, `Calendar` and `SimpleDateFormat`: mutable and not thread-safe. Use `java.time`.
- String concatenation into SQL: injection. Use `PreparedStatement` parameters.
- Overriding `equals` without `hashCode`: broken in hash collections. Use a record or both.
- Returning null collections: callers NPE. Return empty collections.
- Unbounded `parallelStream()` on blocking work: starves the common pool. Use an explicit executor.
- Mutating a collection while iterating it: `ConcurrentModificationException`. Use `removeIf` or iterate a copy.

## Review
- [ ] Resources use try-with-resources; no swallowed exceptions.
- [ ] No string-built SQL; inputs validated at boundaries.
- [ ] Immutable types where possible; `equals`/`hashCode` consistent.
- [ ] Time handled via `java.time` with an injectable `Clock`.
- [ ] Tests run in the wrapper build and cover a failure path.
