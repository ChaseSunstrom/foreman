---
name: kotlin-coroutines
title: Kotlin Coroutines
area: jvm
tags: [kotlin, coroutines, async, flow, concurrency, testing]
detect: [dep:kotlinx-coroutines-core, dep:kotlinx-coroutines-test, dep:kotlinx-coroutines-android, dep:kotlinx-coroutines-reactor]
related: [ktor, android, jetpack-compose, kotlinx-serialization, mockito]
---
Kotlin coroutines and Flow: structured concurrency, dispatchers, cancellation, `runTest` with virtual time.

## Verify
- `./gradlew test`: coroutine tests pass under `runTest`.
- `./gradlew dependencies --configuration testRuntimeClasspath | grep coroutines`: core and test artifacts share a version.
- `./gradlew detekt` (if configured): no `GlobalScope` or `runBlocking` in production code.
- `./gradlew test -Dkotlinx.coroutines.debug`: coroutine names appear in thread names while debugging.

## Test first
Use `runTest` from `kotlinx-coroutines-test`; delays advance virtually.
```kotlin
class RetryTest {
  @Test fun retriesThreeTimesWithBackoff() = runTest {
    var calls = 0
    val result = retry(times = 3, delayMs = 1_000) {
      if (++calls < 3) error("boom") else "ok"
    }
    assertEquals("ok", result)
    assertEquals(3_000, currentTime)
  }
}
```
Inject the dispatcher (`StandardTestDispatcher(testScheduler)`) into classes under test.

## Do
- Launch in a scope tied to a lifecycle (`viewModelScope`, `coroutineScope { }`, a server scope); children cancel with the parent.
- Run parallel work with `coroutineScope { val a = async { ... }; val b = async { ... } }`.
- Make `suspend` functions main-safe: `withContext(Dispatchers.IO)` for blocking calls, inside the function that blocks.
- Inject `CoroutineDispatcher` as a constructor parameter for testing.
- Use `Flow` for streams, `stateIn` and `shareIn` with `SharingStarted.WhileSubscribed(5_000)` for hot state.
- Rethrow `CancellationException` when catching `Exception`.
- Use `SupervisorJob` or `supervisorScope` when one child's failure must not cancel siblings.
- Replace `Dispatchers.Main` in JVM tests with `Dispatchers.setMain(...)` and reset it after.

## Avoid
- `GlobalScope.launch`: leaks and ignores cancellation. Use a lifecycle-bound scope.
- `runBlocking` inside a coroutine or on an event-loop thread: deadlocks and stalls. Keep it for `main` and tests only.
- `catch (e: Exception)` around suspend calls without rethrowing cancellation: the coroutine keeps running after cancel.
- `Thread.sleep` in a coroutine: blocks the thread. Use `delay`.
- Real `delay` in tests with `runBlocking`: slow and flaky. Use `runTest`.
- `async { }.await()` immediately: pointless; call the function directly.
- Collecting a `Flow` in a loop on `Dispatchers.Default` and touching UI state: collect on the right dispatcher or use `flowOn` upstream only.

## Review
- [ ] Every coroutine has an owner scope and a cancellation story.
- [ ] Blocking calls are wrapped in `withContext(Dispatchers.IO)`.
- [ ] Dispatchers are injected, not hardcoded in classes under test.
- [ ] Tests use `runTest` and assert on virtual time where relevant.
- [ ] Exceptions are handled without swallowing `CancellationException`.
