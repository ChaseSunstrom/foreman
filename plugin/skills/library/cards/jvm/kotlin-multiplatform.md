---
name: kotlin-multiplatform
title: Kotlin Multiplatform
area: jvm
tags: [kotlin, multiplatform, kmp, gradle, ios, shared]
detect: [dep:org.jetbrains.kotlin.multiplatform, dep:kotlin-multiplatform, file:shared/build.gradle.kts, file:*.podspec]
related: [gradle, kotlin-coroutines, kotlinx-serialization, ktor, android, jetpack-compose]
---
Kotlin Multiplatform: shared code in `commonMain`, per-target source sets, `expect`/`actual`, and per-target test tasks.

## Verify
- `./gradlew allTests`: tests run for every configured target.
- `./gradlew jvmTest`: fast JVM run of `commonTest` while iterating (use the target your project has).
- `./gradlew iosSimulatorArm64Test`: native tests on the iOS simulator target (macOS only).
- `./gradlew build`: all targets compile, catching platform APIs leaked into common code.

## Test first
Write the test in `commonTest` with `kotlin.test`; it runs on every target.
```kotlin
// src/commonTest/kotlin/PriceTest.kt
import kotlin.test.*

class PriceTest {
  @Test fun negativeQuantityThrows() {
    assertFailsWith<IllegalArgumentException> { total(10, -1) }
  }
}
```
Dependency: `commonTest.dependencies { implementation(kotlin("test")) }`. For suspend code add `kotlinx-coroutines-test` and `runTest`.

## Do
- Keep business logic in `commonMain`; put platform code in `androidMain`, `iosMain`, `jvmMain`.
- Declare an `expect` in common and an `actual` per target, or prefer a plain interface injected from the platform when it is enough.
- Use multiplatform libraries (`kotlinx-coroutines`, `kotlinx-serialization`, `kotlinx-datetime`, Ktor client with per-platform engines, SQLDelight).
- Configure targets in `kotlin { ... }` with `androidTarget()`, `jvm()`, `iosArm64()`, `iosSimulatorArm64()`, and use the default hierarchy template so `iosMain` exists.
- Store versions in the Gradle version catalog; keep the Kotlin version aligned with plugins.
- Expose shared code to iOS as a framework with `binaries.framework { baseName = "Shared" }`.
- Design shared APIs with Swift in mind: avoid generics-heavy signatures and suspend functions without wrappers.

## Avoid
- Importing `java.*` or `android.*` in `commonMain`: fails on other targets. Use common APIs or `expect`/`actual`.
- Using `System.currentTimeMillis()` or `String.format` in common code: use `kotlinx-datetime` or `Clock.System`, and string templates.
- Old `kotlin("multiplatform")` with `android()` target and the legacy hierarchy: use `androidTarget()` and the default hierarchy.
- Mutable global state under the legacy native memory model assumptions: the new memory manager is the default now; still avoid shared mutable singletons.
- Platform libraries only available on JVM (Gson, Retrofit, Room's older versions) in common: use multiplatform replacements.
- Testing only on JVM and shipping iOS untested: run each target's test task in CI.

## Review
- [ ] `commonMain` has no platform imports; build passes for all targets.
- [ ] Every shared behavior has a `commonTest` test.
- [ ] `expect`/`actual` pairs are small and tested per target.
- [ ] iOS framework API is idiomatic from Swift.
- [ ] CI runs `allTests` on suitable runners (macOS for Apple targets).
