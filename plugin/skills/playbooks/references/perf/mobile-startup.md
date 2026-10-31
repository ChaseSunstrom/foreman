<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Phone app cold start and frame drops

Use when an Android, iOS, Expo or Compose app has a slow cold start or dropped frames on a phone.

Built on the cards `fm lib show android-macrobenchmark`, `fm lib show compose-performance`, `fm lib show expo` and `fm lib show swiftui`.

1. **Measure on a release-type build on a real device.** Debug builds and simulators report numbers nobody will see.
2. **Android:** a macrobenchmark module measures startup and jank:
   ```bash
   ./gradlew assembleBenchmark
   ./gradlew :macrobenchmark:connectedBenchmarkAndroidTest
   ```
   Compose: look for unstable parameters and recomposition counts before adding `remember`.
3. **Expo or RN:** run `npx expo run:android --variant release`, trace JS with the Hermes sampler, and fix re-render storms (memoize, stable keys, a virtualised list) before anything native.
4. **iOS:** trace with Instruments (Time Profiler template) and the App Launch template; work off the main thread.
5. **Startup:** list what runs before first frame (SDK init, disk reads, network); defer all that is not needed to draw.
6. **One change, remeasure** with at least ten runs; report median and p90 before and after.

Pass: a measured startup or frame-time delta outside noise on the same device, with the suite (`npx jest`, `./gradlew testReleaseUnitTest`) green.
