---
name: kotlin
title: Kotlin
area: lang
tags: [kotlin, gradle, coroutines, junit, ktlint, detekt]
detect: [ext:.kt, ext:.kts, file:build.gradle.kts, dep:kotlin-stdlib, dep:org.jetbrains.kotlin.jvm]
related: [java, spring-boot, android]
---
Kotlin baseline: Gradle wrapper builds, null safety, data classes and sealed types, structured coroutines, kotlin.test or JUnit 5.

## Verify
- `./gradlew build`: compile, tests and checks through the wrapper.
- `./gradlew test --tests "pkg.FooTest"`: a single class while iterating.
- `./gradlew ktlintCheck detekt`: style and static analysis, when those plugins are configured.

## Test first
Tests in `src/test/kotlin`, class `FooTest`. Use `runTest` from kotlinx-coroutines-test for suspend code.
```kotlin
import kotlin.test.Test
import kotlin.test.assertFailsWith

class PortParserTest {
    @Test
    fun rejectsEmpty() {
        assertFailsWith<IllegalArgumentException> { parsePort("") }
    }
}
```

## Do
- Use `val` by default; model state with `data class` and closed hierarchies with `sealed interface` plus exhaustive `when`.
- Express absence as `T?` and handle it with `?.`, `?:` and `let`; validate input with `require` and `check`.
- Launch coroutines in a scope tied to a lifecycle (`coroutineScope`, `viewModelScope`); make suspend functions main-safe with `withContext(Dispatchers.IO)`.
- Use `Flow` for streams; collect with lifecycle awareness.
- Inject `CoroutineDispatcher` so tests can pass a test dispatcher.
- Use extension functions and scope functions sparingly and readably.
- Keep Java interop explicit with `@JvmStatic`, `@JvmOverloads` and `@Throws` where Java callers need them.

## Avoid
- `!!`: an NPE with no message. Use `?:` with `error(...)` or a safe call.
- `GlobalScope.launch`: leaks and ignores cancellation. Use a structured scope.
- Swallowing `CancellationException` in a broad `catch (e: Exception)`: breaks cancellation. Rethrow it.
- Blocking calls (`Thread.sleep`, `runBlocking`) inside coroutines: stalls the dispatcher. Use `delay` and suspend APIs.
- `lateinit` for values that may never be set: `UninitializedPropertyAccessException`. Use nullable types or constructor injection.
- Platform types from Java (`String!`) treated as non-null: runtime NPE. Annotate or declare nullable.
- Mutable collections exposed from a class: callers mutate state. Expose `List` and copy.

## Review
- [ ] No `!!`, `GlobalScope`, or `runBlocking` in production paths.
- [ ] `CancellationException` is rethrown wherever exceptions are caught broadly.
- [ ] `when` over sealed types is exhaustive without an `else`.
- [ ] Dispatchers are injected, not hard-coded, in testable code.
- [ ] Gradle wrapper build and tests pass.
