---
name: jetpack-compose
title: Jetpack Compose
area: jvm
tags: [android, kotlin, compose, ui, state, testing]
detect: [dep:androidx.compose.ui:ui, dep:androidx.compose.material3:material3, dep:androidx.compose:compose-bom, dep:androidx.activity:activity-compose, dep:androidx.compose.foundation:foundation, dep:androidx.compose.ui:ui-test-junit4, dep:androidx.compose.ui:ui-test-manifest]
related: [android, kotlin-coroutines, hilt, kotlin-multiplatform]
---
Jetpack Compose UI: stateless composables, state hoisting, recomposition control, semantic UI tests.

## Verify
- `./gradlew testDebugUnitTest`: ViewModel and state-holder tests on the JVM.
- `./gradlew connectedDebugAndroidTest`: `createComposeRule` UI tests on a device or emulator.
- `./gradlew lintDebug`: Compose lint checks (modifier ordering, remember misuse) are clean.
- `./gradlew assembleRelease`: R8 does not strip what the UI needs.

## Test first
Test through semantics, not view IDs. Put tests in `src/androidTest` (or Robolectric in `src/test`).
```kotlin
class CounterTest {
  @get:Rule val rule = createComposeRule()

  @Test fun clickIncrements() {
    rule.setContent { Counter() }
    rule.onNodeWithText("Count: 0").performClick()
    rule.onNodeWithText("Count: 1").assertExists()
  }
}
```

## Do
- Hoist state: a composable takes `value` and `onValueChange`; the caller owns state.
- Keep screen state in a `ViewModel` as `StateFlow`; read with `collectAsStateWithLifecycle()`.
- Take a `modifier: Modifier = Modifier` as the first optional parameter and apply it to the root element.
- Use `remember` and `rememberSaveable` for local state that survives recomposition or configuration change.
- Give `LazyColumn` items stable `key = { it.id }`.
- Run side effects in `LaunchedEffect(key)`, `DisposableEffect` or `rememberCoroutineScope`, never in the composable body.
- Import the Compose BOM (`platform(libs.compose.bom)`) so artifact versions align.
- Use `@Preview` on stateless composables with fake data.

## Avoid
- Mutable collections or `var` objects as state: changes are not observed. Use `mutableStateOf`, `mutableStateListOf` or immutable data replaced with `copy`.
- Doing IO or launching coroutines in the composable body: it reruns on every recomposition. Use effects.
- Passing a `ViewModel` deep into child composables: pass state and lambdas instead.
- `collectAsState()` for lifecycle-bound flows on Android: keeps collecting in background. Use `collectAsStateWithLifecycle()`.
- Unstable lambdas or classes causing broad recomposition: mark data classes `@Immutable` or `@Stable` only when true; verify with compiler reports.
- Missing `modifier` parameter on reusable composables.
- `remember` without keys when its value depends on inputs: stale values. Add the keys.

## Review
- [ ] Composables are stateless where possible, with state hoisted to the owner.
- [ ] No side effects outside effect APIs.
- [ ] Lists use stable keys.
- [ ] UI tests assert behavior via semantics and accessibility labels exist.
- [ ] Previews exist for key states (empty, loading, error).
