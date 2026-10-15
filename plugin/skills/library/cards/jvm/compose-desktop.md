---
name: compose-desktop
title: Compose Multiplatform Desktop
area: jvm
tags: [kotlin, compose, desktop, jvm, packaging, ui, gradle]
detect: []
related: [jetpack-compose, kotlin-multiplatform, kotlin-coroutines, gradle, kotest]
---
Compose Multiplatform for Desktop: a JVM app window with the JetBrains Compose Gradle plugin, state hoisting, and native packaging per OS.

## Verify
- `./gradlew run`: the app launches from the main class set in the `compose.desktop` block.
- `./gradlew test`: UI and state tests pass (headless unit tests; `compose.desktop.uiTestJUnit4` for UI tests).
- `./gradlew packageDistributionForCurrentOS`: builds the native installer for the host OS.
- `./gradlew createDistributable`: builds an app image without an installer, quick packaging smoke test.

## Test first
State holders are plain Kotlin and test without UI; UI tests use the Compose test rule.
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
Add `testImplementation(compose.desktop.uiTestJUnit4)` and `compose.desktop.currentOs` to dependencies.

## Do
- Entry point: `fun main() = application { Window(onCloseRequest = ::exitApplication, title = "App") { App() } }`.
- Configure `compose.desktop.application { mainClass = "..."; nativeDistributions { targetFormats(Dmg, Msi, Deb); packageName; packageVersion } }`; `packageVersion` must be numeric (`MAJOR.MINOR.PATCH`), and macOS needs MAJOR above 0.
- Hoist state into a ViewModel-like class and expose `StateFlow`; collect with `collectAsState()`.
- Run IO off the UI with `rememberCoroutineScope` and `Dispatchers.IO`; update state on the main dispatcher.
- Use `rememberSaveable` sparingly (desktop has no process-death restore); persist user settings to disk explicitly.
- Add icons per OS in `nativeDistributions` (`macOS { iconFile.set(...) }`, `windows`, `linux`).
- Declare needed JDK modules with `modules("java.sql")` since the packaged runtime is trimmed; use `./gradlew suggestRuntimeModules`.
- Enable ProGuard release builds with `./gradlew packageReleaseDistributionForCurrentOS` and keep rules in a file.

## Avoid
- Blocking calls in composables or `onClick`: the window freezes. Launch a coroutine.
- Starting work in composition without `LaunchedEffect`/`DisposableEffect`: it repeats on every recomposition.
- Missing JDK modules in the packaged app: works under `run`, `NoClassDefFoundError` when installed. Run `suggestRuntimeModules` and list `modules(...)`.
- Hardcoded Android-isms (`Context`, `R.drawable`): not on desktop. Use `painterResource` from compose resources.
- Mutable collections as state: no recomposition. Use `mutableStateListOf` or immutable copies.
- Cross-compiling installers: packages build only for the host OS; use CI runners per OS.

## Review
- [ ] App runs with `./gradlew run` and packages with `packageDistributionForCurrentOS`.
- [ ] State holders are separate from composables and unit tested.
- [ ] No blocking I/O on the UI thread; effects are keyed correctly.
- [ ] Packaged runtime includes required JDK modules.
- [ ] Version, icons and target formats are set for each OS shipped.
