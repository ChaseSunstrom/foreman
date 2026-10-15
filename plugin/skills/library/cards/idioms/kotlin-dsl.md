---
name: kotlin-dsl
title: Kotlin DSLs
area: idioms
tags: [kotlin, dsl, lambdas, receivers, builders, gradle]
detect: [file:build.gradle.kts, file:settings.gradle.kts]
related: [kotlin, gradle, junit]
---
Kotlin DSLs: lambdas with receivers, `@DslMarker` scoping, and builders that produce immutable results.

## Verify
- `./gradlew build`: compile, test and check, including the build scripts themselves.
- `./gradlew test`: the DSL's behavior tests.
- `./gradlew tasks`: a Kotlin build script still configures without errors.

## Test first
Test the DSL by the structure it builds, not its internals.
```kotlin
import kotlin.test.Test
import kotlin.test.assertEquals

class HtmlDslTest {
    @Test
    fun nestedTagsRender() {
        val out = html { body { p { +"hi" } } }.render()
        assertEquals("<html><body><p>hi</p></body></html>", out)
    }
}
```

## Do
- Write builders as `fun html(init: Html.() -> Unit): Html = Html().apply(init)`.
- Put the receiver on the lambda type (`Tag.() -> Unit`) so members read without a prefix.
- Mark DSL receivers with an annotation class marked `@DslMarker` to stop inner scopes from calling outer builders implicitly.
- Keep the builder mutable and private, and return an immutable model from `build()`.
- Use `operator fun String.unaryPlus()` for text nodes and `infix` for readable pairs.
- Use `inline` for lambda-taking functions so lambdas cost nothing and allow non-local returns where wanted.
- Use `@PublishedApi internal` when a public inline function needs internal state.
- In Gradle scripts use typed accessors and `tasks.register`, not eager `tasks.create`.

## Avoid
- A DSL for something a function call with named arguments expresses: more machinery, no gain. Use named and default parameters.
- Missing `@DslMarker`: nested lambdas silently resolve to the outer receiver. Add the marker annotation to the builder classes.
- Exposing mutable builders to callers after `build()`: later edits change finished objects. Copy on build.
- Overusing operator overloading with unexpected meaning: readers cannot guess it. Keep to widely understood operators.
- `lateinit` fields in builders for required values: failures appear late. Validate in `build()` with `require` and a clear message.
- Gradle `tasks.create` and configuration-time work that runs on every build: use `register` and lazy `Provider` properties.

## Review
- [ ] Builder scopes are protected by a `@DslMarker`.
- [ ] `build()` validates required fields and returns immutable data.
- [ ] Tests assert on the produced structure for nested and empty cases.
- [ ] Inline and receiver lambdas are used so call sites read declaratively.
- [ ] Gradle logic is lazy and typed.
