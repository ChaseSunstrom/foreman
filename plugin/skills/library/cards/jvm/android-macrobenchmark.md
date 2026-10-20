---
name: android-macrobenchmark
title: Android Macrobenchmark
area: jvm
tags: [android, benchmark, performance, startup, baseline-profile, testing]
detect: [dep:androidx.benchmark:benchmark-macro-junit4, dep:androidx.benchmark:benchmark-macro]
related: [android, jetpack-compose, gradle, espresso]
---
Jetpack Macrobenchmark: measure app startup and scrolling jank from a separate test module, and generate baseline profiles.

## Verify
- `./gradlew assembleBenchmark`: the benchmarkable build variant compiles.
- `./gradlew :macrobenchmark:connectedBenchmarkAndroidTest`: runs the benchmarks on a physical device (module name varies).
- `./gradlew lintDebug`: the benchmark module is lint-clean.

## Test first
Write the benchmark in its own `com.android.test` module that targets the app.
```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
  @get:Rule val rule = MacrobenchmarkRule()

  @Test fun startup() = rule.measureRepeated(
    packageName = "com.example.app",
    metrics = listOf(StartupTimingMetric()),
    iterations = 5,
    startupMode = StartupMode.COLD,
  ) {
    pressHome()
    startActivityAndWait()
  }
}
```

## Do
- Keep benchmarks in a separate `com.android.test` module with `targetProjectPath` set to the app.
- Add a non-debuggable `benchmark` build type that matches release, signed with the debug key.
- Run on a real device: emulators give misleading numbers.
- Use `StartupMode.COLD` for startup, `FrameTimingMetric` for scrolling.
- Use at least five iterations and compare medians, not single runs.
- Generate baseline profiles with `BaselineProfileRule` and ship them in the app.
- Pick stable targets via `UiAutomator` selectors or `contentDescription`.
- Keep each benchmark single-purpose.

## Avoid
- Benchmarking a debuggable build: results are not representative. Use the non-debuggable benchmark variant.
- Running on an emulator and trusting the numbers: use hardware.
- One iteration: noise dominates. Use several and look at the distribution.
- Leaving the app installed in an odd state: call `pressHome()` and kill the process in setup.
- Minification disabled on the benchmark variant: differs from release. Match release R8 settings.
- Treating baseline profiles as a one-time job: regenerate when startup paths change.

## Review
- [ ] Benchmarks live in a separate test module targeting a non-debuggable variant.
- [ ] Run on a physical device with several iterations.
- [ ] Startup and scroll metrics are both covered.
- [ ] Baseline profile generation is wired up.
