---
name: cpp-coroutines
title: C++20 Coroutines
area: native
tags: [cpp, coroutines, c++20, async, asio, generator, lifetime]
detect: []
related: [cpp-modern, cpp-concurrency, boost, sanitizers, cmake]
---
C++20 coroutines: promise types, awaiters, frame lifetime, Asio awaitable or a task library, and the dangling-reference traps.

## Verify
- `cmake -B build -DCMAKE_CXX_STANDARD=20 -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -g" && cmake --build build -j`: coroutine frames are heap objects, so ASan catches use-after-free of them.
- `ctest --test-dir build --output-on-failure`: suite passes.
- `clang-tidy -p build --checks='cppcoreguidelines-avoid-reference-coroutine-parameters,cppcoreguidelines-avoid-capturing-lambda-coroutines' src/*.cpp`: the two classic lifetime bugs.
- `grep -n "fcoroutines" CMakeLists.txt`: GCC 10 needs `-fcoroutines`; later versions with C++20 enable it.

## Test first
Drive the coroutine to completion and assert on the value; run it under ASan.
```cpp
TEST(Task, ReturnsValueAfterSuspend) {
    boost::asio::io_context io;
    int out = 0;
    boost::asio::co_spawn(io, [&]() -> boost::asio::awaitable<void> {
        out = co_await compute_later(io);
    }, boost::asio::detached);
    io.run();
    EXPECT_EQ(out, 42);
}
```

## Do
- Use a library: Asio `awaitable<T>` with `co_spawn`, or a vetted `task<T>`/`generator<T>` (C++23 has `std::generator`). Hand-written promise types are for library authors.
- Take coroutine parameters by value (or `shared_ptr`), since the frame outlives the caller's arguments.
- Make lambda coroutines capture nothing: pass state as parameters, or the closure dies while the frame still points at it.
- Define `initial_suspend`/`final_suspend` deliberately: lazy start with `suspend_always`; final suspend `suspend_always` so the result stays readable until the owner destroys the frame.
- Implement `unhandled_exception()` to store `std::current_exception()` and rethrow on `await_resume`/`get`.
- Resume on a known executor; transfer with symmetric transfer (`await_suspend` returning a `coroutine_handle`) to avoid stack growth in chains.
- Own the frame in an RAII handle that calls `handle.destroy()`.

## Avoid
- `const std::string&` or `std::string_view` parameters on a coroutine: dangle after the first suspension. Take by value.
- Capturing lambda coroutines `[&]{ co_await ...; }` that outlive the enclosing scope: use-after-free. Pass args or keep the lambda alive.
- Resuming one handle from two threads, or resuming a destroyed frame: undefined behavior. Serialize via a strand.
- `co_await` while holding a `std::mutex` lock: the lock is held across suspension and may unlock on another thread. Release first, or use an async mutex.
- Forgetting `co_return` in a `Task<void>` path: falls off the end. Return explicitly.
- Fire-and-forget without error handling: exceptions vanish. Use `co_spawn` with a completion handler that logs.
- Assuming `generator` copying works: it is move-only.

## Review
- [ ] No reference or view parameters on coroutines.
- [ ] No captures in coroutine lambdas, or documented lifetime guarantees.
- [ ] Every coroutine frame has a single owner that destroys it.
- [ ] Exceptions propagate to an awaiter or a logged handler.
- [ ] Tests run under ASan and exercise a suspend plus an error path.
