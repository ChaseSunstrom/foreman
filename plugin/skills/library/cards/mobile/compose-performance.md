---
name: compose-performance
title: Compose Performance
area: mobile
tags: [android, kotlin, compose, performance, recomposition, jank]
detect: [dep:androidx.compose.ui:ui, dep:androidx.compose.runtime:runtime, file:*.gradle.kts]
related: [kotlin, android, kotlin-coroutines]
---
Jetpack Compose performance: cut unnecessary recomposition with stable inputs, deferred reads and keyed lazy lists, then confirm with metrics.

## Verify
- `./gradlew :app:assembleRelease`: performance is judged on a release (R8 and baseline-profile) build, so it must build.
- `./gradlew :app:testDebugUnitTest`: unit tests for state holders pass.
- `./gradlew :app:connectedDebugAndroidTest`: Compose UI tests (and recomposition-count tests) pass on a device or emulator.
- `./gradlew :benchmark:connectedBenchmarkAndroidTest`: Macrobenchmark startup and scroll timing, if a benchmark module exists.

## Test first
Prove a composable does not recompose when unrelated state changes, using a counter in a test.
```kotlin
class RecompositionTest {
    @get:Rule val rule = createComposeRule()

    @Test fun rowSkipsWhenOtherStateChanges() {
        var compositions = 0
        var other by mutableStateOf(0)
        rule.setContent {
            Text("other $other")
            Row(item = Item(1, "a")) { compositions++ }
        }
        rule.runOnIdle { other++ }
        rule.waitForIdle()
        assertEquals(1, compositions)
    }
}
```

## Do
- Give every `LazyColumn` item a `key = { it.id }` and a `contentType`, so rows are reused and moved correctly.
- Pass stable parameters: immutable data classes, `ImmutableList` or `@Immutable` and `@Stable` annotations when a type holds read-only collections.
- Check the stability of types in the Compose compiler reports (`-P plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=...`) and fix unstable params in hot composables.
- Read fast-changing state as late as possible: pass lambdas (`offset = { scroll.value }`) and use `Modifier.graphicsLayer { }` or `drawBehind { }`, so only layout or draw reruns.
- Hoist expensive work into `remember(key) { }`, and use `derivedStateOf { }` for values derived from frequently changing state.
- Keep state in a ViewModel or state holder, and collect with `collectAsStateWithLifecycle()`.
- Hold lambdas stable via `remember` when they capture changing values, if the compiler's strong skipping is not enabled in your setup.
- Ship a baseline profile and measure with Macrobenchmark on a release build.

## Avoid
- Measuring jank in a debug build: it is much slower, with no R8 or AOT. Test release.
- Reading `State.value` in the composable body for scroll or animation values: it recomposes every frame. Defer the read to the layout or draw phase.
- Missing keys in lazy lists: state and animations jump to the wrong row after inserts. Add `key`.
- Allocating objects, lists and `Modifier` chains with new state per recomposition: `remember` them.
- Sorting or filtering inside the composable body: it reruns on every recomposition. Do it in the ViewModel or `remember`.
- Unstable `List<T>` params from `kotlin.collections`: Compose treats them as unstable. Use an immutable wrapper or enable the strong-skipping mode your compiler version supports.
- Nested scrollables of unbounded height (a `LazyColumn` inside a `verticalScroll`): it crashes or composes everything.

## Review
- [ ] Lazy items have keys and content types.
- [ ] Hot composables take stable parameters per the compiler report.
- [ ] Animated or scroll-driven values are read in layout or draw lambdas.
- [ ] Derived values use `remember` or `derivedStateOf`.
- [ ] A release-build benchmark or recomposition test backs the claim.
