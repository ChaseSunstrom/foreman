---
name: cpp-concurrency
title: C++ Concurrency
area: native
tags: [cpp, threads, mutex, atomics, memory-order, tsan, jthread]
detect: []
related: [cpp-modern, cpp-raii, sanitizers, cpp-coroutines, googletest]
---
C++ threading: std::jthread, scoped locks, condition variables, atomics and memory orders, verified under ThreadSanitizer.

## Verify
- `cmake -B build-tsan -DCMAKE_CXX_FLAGS="-fsanitize=thread -g -O1" && cmake --build build-tsan`: ThreadSanitizer build (do not combine with ASan).
- `ctest --test-dir build-tsan --output-on-failure`: any data race fails the run with a report.
- `ctest --test-dir build --repeat until-fail:50`: flaky interleavings surface.
- `clang-tidy -p build --checks='concurrency-*' src/*.cpp`: concurrency checks such as thread-canceltype and mt-unsafe.

## Test first
Write a stress test that hammers the shared state; it fails under TSan before the fix.
```cpp
TEST(Counter, ConcurrentIncrements) {
    Counter c;
    {
        std::vector<std::jthread> ts;
        for (int i = 0; i < 8; ++i)
            ts.emplace_back([&] { for (int j = 0; j < 10000; ++j) c.inc(); });
    }  // jthreads join here
    EXPECT_EQ(c.value(), 80000);
}
```

## Do
- Use `std::jthread` (joins on destruction, carries a `std::stop_token`) over `std::thread`.
- Lock with `std::scoped_lock lk{m1, m2}` (deadlock-free multi-lock) or `std::lock_guard`; keep critical sections tiny and call no user callbacks while holding.
- Pair every `std::condition_variable` wait with a predicate: `cv.wait(lk, [&]{ return ready; });`. Change the predicate state under the same mutex.
- Default to `std::memory_order_seq_cst`; relax to acquire/release only with a written reason and a TSan run.
- Use `std::atomic<T>` only for independent flags and counters; guard multi-field invariants with a mutex.
- Pass data between threads by move through a queue or `std::promise`/`std::future`; avoid shared mutable state.
- Use `std::shared_mutex` only for read-heavy data measured to contend.

## Avoid
- `std::thread` left joinable at scope exit: it calls `std::terminate`. Use `jthread` or join in RAII.
- `cv.wait(lk)` with no predicate: spurious wakeups and lost notifications. Always loop or pass a predicate.
- Capturing locals by reference in a detached thread: dangling after return. Capture by value or join.
- `volatile` as a sync tool: it gives no atomicity or ordering. Use `std::atomic`.
- Double-checked locking with a plain bool: a race. Use `std::call_once` or a function-local static.
- Locking two mutexes in differing order across call sites: deadlock. Use `std::scoped_lock`.
- `std::async` without keeping the future: the destructor blocks, serializing work. Hold the future.

## Review
- [ ] Each shared variable has one documented guard (mutex or atomic).
- [ ] No lock held across I/O, user callbacks, or a `join`.
- [ ] Shutdown path tested: stop requested, threads joined, no hang.
- [ ] TSan run clean on the concurrent tests.
- [ ] Non-seq_cst orderings carry a comment explaining the happens-before edge.
