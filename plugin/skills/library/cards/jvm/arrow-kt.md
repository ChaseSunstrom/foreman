---
name: arrow-kt
title: Arrow
area: jvm
tags: [kotlin, functional, either, raise, error-handling, resilience, optics]
detect: [dep:arrow-core, dep:arrow-fx-coroutines, dep:arrow-resilience, dep:arrow-optics]
related: [kotlin-coroutines, kotest, mockk, ktor, detekt]
---
Arrow for Kotlin: typed errors with `Either` and the `Raise` DSL, parallel and resource-safe coroutines, resilience policies, without leaking exceptions.

## Verify
- `./gradlew test`: error paths and success paths both covered.
- `./gradlew dependencies --configuration runtimeClasspath | grep arrow`: all Arrow artifacts share one version.
- `grep -rnE "arrow\.core\.computations|Either\.catch \{|\.getOrHandle" src`: no removed or deprecated APIs from Arrow 1.x tutorials.
- `./gradlew compileKotlin`: no deprecation errors after an upgrade.

## Test first
Assert the typed error, not an exception.
```kotlin
class ParseTest {
    @Test fun `negative age is a typed error`() {
        val r = either { parseAge("-3") }
        assertEquals(AgeError.Negative(-3).left(), r)
    }
}

fun Raise<AgeError>.parseAge(s: String): Int {
    val n = s.toIntOrNull() ?: raise(AgeError.NotANumber(s))
    ensure(n >= 0) { AgeError.Negative(n) }
    return n
}
```

## Do
- Model domain failures as a sealed error type and return `Either<Error, A>`, or use `context(Raise<Error>)`-style functions with `Raise<E>` receivers.
- Use `either { ... }` and `bind()` (or `.bind()` on `Either`) to sequence; use `ensure` and `ensureNotNull` for guards.
- Convert exceptions at the boundary: `Either.catch { }` or `catch { }` inside `Raise`, rethrow `CancellationException`.
- Use `parMap`, `parZip`, `raceN` from `arrow-fx-coroutines` for structured parallelism.
- Use `Resource` and `resourceScope { install(...) }` for acquire/release; `Schedule` and `Resilience` modules for retry and circuit breaker.
- Use `accumulate` or `zipOrAccumulate` for validation that reports all errors.
- Use `arrow-optics` with `@optics` and KSP for nested immutable updates.
- At HTTP or CLI edges, fold the `Either` into a response once.

## Avoid
- `arrow.core.computations.either.eager`, `getOrHandle`, and `Validated` from 0.x/1.1 tutorials: deprecated or removed. Use `either { }`, `getOrElse`, `Either` with `zipOrAccumulate`.
- `catch (e: Throwable)` around suspend code: swallows cancellation. Rethrow `CancellationException` or use Arrow's `catch`.
- Mixing thrown exceptions and `Either` for the same failure: callers cannot know. Pick `Either` for domain errors, exceptions for bugs.
- `Either<Throwable, A>` as the error type everywhere: loses meaning. Use sealed domain errors.
- Calling `.getOrNull()` on every result: discards the error. Fold or map the error.
- Version skew between `arrow-core` and `arrow-fx-coroutines`: link errors. Use the Arrow BOM.

## Review
- [ ] Domain errors are a sealed hierarchy, not strings or `Throwable`.
- [ ] Exceptions are caught only at boundaries and never swallow cancellation.
- [ ] Validation that should report many errors accumulates them.
- [ ] Resources use `Resource`/`resourceScope`, not manual try/finally.
- [ ] No deprecated Arrow APIs; versions aligned through one BOM.
