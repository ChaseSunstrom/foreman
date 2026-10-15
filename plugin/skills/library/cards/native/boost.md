---
name: boost
title: Boost C++ Libraries
area: native
tags: [cpp, boost, asio, beast, program-options, filesystem, json]
detect: [dep:boost*, dep:boost-asio, dep:boost-beast]
related: [cpp-modern, cmake, vcpkg, conan, cpp-coroutines]
---
Boost usage: find_package components, Asio io_context and strands, Beast, Program_options, and when std has already replaced it.

## Verify
- `cmake -S . -B build && cmake --build build -j`: configure finds Boost and links only declared components.
- `cmake --build build --target help | grep -i boost`: confirm targets exist when using the superproject.
- `ctest --test-dir build --output-on-failure`: suite passes.
- `ldd build/app | grep -i boost`: shared Boost libs resolve at runtime (skip for static links).

## Test first
Test through Asio with a real `io_context`; run it to completion so a handler that never fires fails.
```cpp
TEST(Timer, FiresOnce) {
    boost::asio::io_context io;
    boost::asio::steady_timer t{io, std::chrono::milliseconds(5)};
    int fired = 0;
    t.async_wait([&](boost::system::error_code ec) { if (!ec) ++fired; });
    io.run();
    EXPECT_EQ(fired, 1);
}
```

## Do
- Use `find_package(Boost REQUIRED COMPONENTS system filesystem)` and link `Boost::filesystem`, not raw paths. Header-only libraries link `Boost::headers`.
- Keep one `io_context` per process and one thread pool via `boost::asio::thread_pool` or N threads calling `io.run()`.
- Use `boost::asio::strand` (or `make_strand(executor)`) for objects whose handlers can run on several threads.
- Prefer `co_spawn` with `use_awaitable` over callback chains when C++20 is available.
- Hold the I/O object alive in handlers with `shared_from_this` and bind lifetime to the completion handler.
- Check `boost::system::error_code` first in every handler; treat `operation_aborted` as normal cancellation.
- Reach for `std::filesystem`, `std::optional`, `std::variant`, `std::thread` first; use Boost where std lacks the feature (Asio, Beast, Program_options, Multi_index, Unordered flat maps).

## Avoid
- `find_package(Boost)` with no components while linking compiled libs: link errors. List components.
- Old `FindBoost` module assumptions: modern CMake ships `BoostConfig`; set `CMP0167` policy as needed, not hand edits.
- Destroying the `io_context` or a socket with pending handlers: use-after-free. Cancel and run until drained.
- Calling `io.run()` on a stopped context: it returns at once. Call `io.restart()` first.
- Mixing Boost and std versions of one facility (`boost::thread` plus `std::mutex`): pick one.
- Assuming `async_*` completes in the calling thread: handlers run inside `run()` on any of its threads.
- Blocking calls inside a handler: stalls every other handler on that thread.

## Review
- [ ] Only needed components appear in `find_package` and `target_link_libraries`.
- [ ] Every async operation has a defined cancellation and error path.
- [ ] Shared state touched by handlers is under a strand or mutex.
- [ ] A Boost type is not used where a standard type exists.
- [ ] Pinned Boost version matches in vcpkg or conan and CI.
