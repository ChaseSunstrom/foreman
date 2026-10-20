---
name: android
title: Android
area: jvm
tags: [android, kotlin, gradle, lifecycle, viewmodel, testing]
detect: [dep:androidx.core:core-ktx, dep:androidx.appcompat:appcompat, dep:androidx.lifecycle:lifecycle-viewmodel-ktx, dep:androidx.activity:activity-ktx, file:AndroidManifest.xml, file:gradle/libs.versions.toml]
related: [jetpack-compose, hilt, room, kotlin-coroutines, gradle, junit5]
---
Android apps in Kotlin: Gradle module setup, lifecycle-aware ViewModels, permissions, unit and instrumented tests.

## Verify
- `./gradlew testDebugUnitTest`: local JVM unit tests.
- `./gradlew lintDebug`: Android Lint, including API-level and manifest issues.
- `./gradlew assembleDebug`: the app compiles and resources merge.
- `./gradlew connectedDebugAndroidTest`: instrumented tests on a running emulator or device.

## Test first
Keep logic in ViewModels and plain classes so it tests on the JVM. Local tests in `src/test`, instrumented in `src/androidTest`.
```kotlin
class LoginViewModelTest {
  @get:Rule val main = MainDispatcherRule()

  @Test fun blankEmailShowsError() = runTest {
    val vm = LoginViewModel(FakeAuthRepo())
    vm.submit(email = "", password = "x")
    assertEquals("Email required", vm.state.value.error)
  }
}
```
`MainDispatcherRule` is a small rule that calls `Dispatchers.setMain(...)`.

## Do
- Set `compileSdk`, `targetSdk` and `minSdk` explicitly; keep dependencies in the version catalog.
- Hold UI state in a `ViewModel` exposed as `StateFlow`; collect with `collectAsStateWithLifecycle` or `repeatOnLifecycle`.
- Run IO on injected dispatchers; use `viewModelScope`.
- Request runtime permissions through the Activity Result API (`registerForActivityResult`).
- Declare components and permissions in `AndroidManifest.xml`; set `android:exported` explicitly on every component with an intent filter.
- Enable R8 (`isMinifyEnabled = true`) in release with keep rules for reflection-based libraries.
- Store secrets outside the repo; use EncryptedSharedPreferences or DataStore with the Keystore for sensitive values.

## Avoid
- `AsyncTask` and `startActivityForResult`/`onActivityResult`: deprecated. Use coroutines and the Activity Result API.
- Holding an `Activity` or `Context` in a ViewModel or singleton: memory leak. Use the application context or inject abstractions.
- Network or disk on the main thread: `NetworkOnMainThreadException` or ANRs.
- Kotlin synthetics and `findViewById` in new code: use view binding or Compose.
- Missing `android:exported` on components with intent filters: install fails on recent targets.
- Cleartext HTTP and `android:allowBackup="true"` by default for sensitive apps: set a network security config and review backup rules.
- Ignoring process death: state held only in memory is lost. Use `SavedStateHandle`.

## Review
- [ ] Unit tests cover ViewModels and domain logic without Android dependencies.
- [ ] Lint is clean or baselined with a reason.
- [ ] Permissions are minimal and requested at the point of use.
- [ ] Release build is minified and keep rules were tested on a release build.
- [ ] No hardcoded keys; no cleartext traffic unless declared.
