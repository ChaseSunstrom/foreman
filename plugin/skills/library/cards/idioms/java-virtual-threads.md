---
name: java-virtual-threads
title: Java virtual threads
area: idioms
tags: [java, virtual-threads, concurrency, executors, loom, structured]
detect: []
related: [java, java-modern, junit]
---
Virtual threads: one cheap thread per blocking task, no pools for them, and care around pinning and limits.

## Verify
- `java -version`: virtual threads are final from Java 21 onward, so confirm the runtime.
- `mvn -q verify`: build and tests (or `./gradlew check`).
- `java -Djdk.tracePinnedThreads=full -jar app.jar`: prints stack traces when a virtual thread pins its carrier.
- `jcmd PID Thread.dump_to_file -format=json out.json`: thread dump that includes virtual threads.

## Test first
Prove the task count scales with blocking calls.
```java
@Test
void handlesTenThousandBlockingTasks() throws Exception {
    try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
        var futures = IntStream.range(0, 10_000)
            .mapToObj(i -> ex.submit(() -> { Thread.sleep(100); return i; }))
            .toList();
        long sum = 0;
        for (var f : futures) sum += f.get();
        assertEquals(49_995_000L, sum);
    }
}
```

## Do
- Use `Executors.newVirtualThreadPerTaskExecutor()` in try-with-resources, one task per unit of work.
- Start single threads with `Thread.ofVirtual().start(runnable)` or `Thread.startVirtualThread`.
- Write plain blocking code. Virtual threads make it scale, so avoid callback chains.
- Limit access to scarce resources (a database, a rate-limited API) with a `Semaphore`.
- Prefer `ReentrantLock` over `synchronized` around blocking calls on versions where pinning matters.
- Use `ThreadLocal` sparingly, and prefer passing values explicitly.
- Keep platform-thread pools for CPU-bound work.

## Avoid
- Pooling virtual threads (`newFixedThreadPool` with a virtual factory): they are cheap, so a pool only caps throughput. Create one per task and use a `Semaphore` to bound.
- Blocking inside `synchronized` for long: on some versions this pins the carrier thread and starves others. Use `ReentrantLock`.
- CPU-bound loops on virtual threads: they gain nothing. Use `ForkJoinPool` or a platform pool.
- Large per-thread caches in `ThreadLocal`: with millions of threads memory explodes. Share or pass state.
- Assuming `Thread.sleep` or I/O is the same everywhere: native calls and file I/O may still pin. Measure with `jdk.tracePinnedThreads`.
- Ignoring interrupts: cancel with `Future.cancel(true)` and honor `InterruptedException`.

## Review
- [ ] A virtual-thread executor is closed through try-with-resources.
- [ ] Concurrency limits are enforced with semaphores, not pool size.
- [ ] No long blocking work inside `synchronized` blocks.
- [ ] Interrupts are propagated, not swallowed.
- [ ] CPU-bound work stays off virtual threads.
