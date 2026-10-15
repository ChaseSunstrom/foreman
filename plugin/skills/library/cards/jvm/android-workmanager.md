---
name: android-workmanager
title: Android WorkManager
area: jvm
tags: [android, kotlin, workmanager, background, constraints, hilt, testing]
detect: [dep:work-runtime-ktx, dep:work-runtime, dep:work-testing, dep:hilt-work]
related: [android, hilt, room, kotlin-coroutines, espresso, jetpack-compose]
---
WorkManager for deferrable, guaranteed Android background work: unique, constrained, idempotent workers with correct retry and result handling.

## Verify
- `./gradlew testDebugUnitTest`: worker logic and `TestListenableWorkerBuilder` tests pass.
- `./gradlew connectedDebugAndroidTest`: `WorkManagerTestInitHelper` tests pass on a device or emulator.
- `adb shell dumpsys jobscheduler | grep -i <your.package>`: the scheduled job exists on a device.
- `./gradlew lintDebug`: lint flags missing `foregroundServiceType` and notification issues.

## Test first
`work-testing` provides `TestListenableWorkerBuilder` for a single worker.
```kotlin
@RunWith(AndroidJUnit4::class)
class SyncWorkerTest {
    @Test fun failedNetworkRetries() = runTest {
        val ctx = ApplicationProvider.getApplicationContext<Context>()
        val worker = TestListenableWorkerBuilder<SyncWorker>(ctx)
            .setInputData(workDataOf("id" to "bad")).build()
        assertEquals(ListenableWorker.Result.retry(), worker.doWork())
    }
}
```
For chains, constraints and periodic work use `WorkManagerTestInitHelper.initializeTestWorkManager` and `getTestDriver()`.

## Do
- Extend `CoroutineWorker` and implement `doWork()` returning `Result.success()`, `retry()`, or `failure()`.
- Make work idempotent; it may run more than once.
- Use `enqueueUniqueWork(name, ExistingWorkPolicy.KEEP, request)` and `enqueueUniquePeriodicWork(..., ExistingPeriodicWorkPolicy.KEEP, ...)` to avoid duplicates.
- Declare `Constraints` (`setRequiredNetworkType`, `setRequiresCharging`) rather than checking inside the worker.
- Set backoff: `setBackoffCriteria(BackoffPolicy.EXPONENTIAL, ...)`; cap attempts with `runAttemptCount`.
- Keep input and output `Data` small; pass IDs and read from the database.
- Use `setForeground`/`getForegroundInfo` for long expedited work, with the right foreground service type in the manifest.
- Hilt: `@HiltWorker` with `@AssistedInject`, and a `Configuration.Provider` using `HiltWorkerFactory` (remove the default initializer from the manifest).
- Observe with `getWorkInfosForUniqueWorkFlow`.

## Avoid
- Periodic work with an interval under 15 minutes: it is clamped. Use a foreground service or alarm if timing matters.
- Calling `enqueue` on every launch: duplicates stack up. Use unique work with `KEEP`.
- Returning `Result.retry()` unconditionally: infinite retry. Check `runAttemptCount` and return `failure()`.
- Blocking calls on the main thread in a plain `Worker` subclass assumptions: workers run on a background executor, but heavy CPU work should use `CoroutineWorker` with the right dispatcher.
- Large payloads in `Data` (limit is about 10 KB): throws. Persist and pass a key.
- Hilt workers without disabling default `WorkManagerInitializer`: factory is ignored and instantiation fails.
- Assuming exact timing: work is deferrable and Doze-aware.

## Review
- [ ] Workers are idempotent and use unique work names.
- [ ] Constraints, backoff and attempt caps are explicit.
- [ ] Results (`success`/`retry`/`failure`) map to real outcomes.
- [ ] Foreground work declares its service type and notification.
- [ ] Tests cover success, retry and failure paths.
