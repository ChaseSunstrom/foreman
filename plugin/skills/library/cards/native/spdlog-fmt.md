---
name: spdlog-fmt
title: spdlog and fmt
area: native
tags: [cpp, logging, spdlog, fmt, format, async, sinks]
detect: [dep:spdlog, dep:fmt, dep:fmtlib]
related: [cpp-modern, cmake, vcpkg, conan, cpp-concurrency]
---
Logging and formatting in C++: fmt compile-time checked format strings, spdlog loggers, sinks, async mode and flush policy.

## Verify
- `cmake --build build -j`: a bad format string or arg count fails at compile time with `FMT_STRING` or C++20 consteval.
- `ctest --test-dir build --output-on-failure`: log-capturing tests pass.
- `grep -rn "spdlog::set_level\|set_pattern\|flush_on" src`: confirm level, pattern and flush policy are set once at startup.
- `grep -rn "SPDLOG_ACTIVE_LEVEL" CMakeLists.txt src`: compile-time level matches the build type.

## Test first
Log to an in-memory ostream sink and assert on the text.
```cpp
#include <spdlog/spdlog.h>
#include <spdlog/sinks/ostream_sink.h>

TEST(Log, WarnIncludesPort) {
    std::ostringstream os;
    auto sink = std::make_shared<spdlog::sinks::ostream_sink_mt>(os);
    spdlog::logger lg("t", sink);
    lg.warn("port {} busy", 8080);
    lg.flush();
    EXPECT_NE(os.str().find("port 8080 busy"), std::string::npos);
}
```

## Do
- Use `{}` placeholders and pass values as args: `spdlog::info("user {} took {:.2f}ms", id, ms);`. Format specs follow fmt (`{:>8}`, `{:#x}`).
- Create named loggers once at startup (`spdlog::stdout_color_mt("net")`); fetch by name with `spdlog::get`.
- Set the pattern once: `spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%l] [%t] %v");`.
- Use rotating or daily file sinks for services: `spdlog::rotating_logger_mt("app", "logs/app.log", 5*1024*1024, 3);`.
- For hot paths use async: `spdlog::init_thread_pool(8192, 1)` then `spdlog::async_logger`; call `spdlog::shutdown()` before exit.
- Set `flush_on(spdlog::level::err)` so crashes keep error lines, and `flush_every` for periodic flush.
- Use `SPDLOG_INFO` macros (with `SPDLOG_ACTIVE_LEVEL`) when you need compiled-out levels and source locations.
- Format custom types with a `fmt::formatter<T>` specialization (or `operator<<` plus `fmt/ostream.h`).

## Avoid
- Building strings before logging (`info("x" + std::to_string(n))`): costs even when the level is off. Pass args.
- Runtime-built format strings without `fmt::runtime(...)`: compile error in C++20 mode. Fix the string or wrap deliberately.
- Mixing bundled and external fmt (`SPDLOG_FMT_EXTERNAL` mismatch): duplicate symbols. Use one fmt and link `spdlog::spdlog` consistently.
- Async loggers still alive at static destruction: crashes at exit. Call `spdlog::shutdown()` explicitly.
- Logging secrets, tokens or whole request bodies: redact first.
- Using `_st` single-thread sinks from several threads: data race. Use `_mt` variants.

## Review
- [ ] No string concatenation in log calls; args passed as format parameters.
- [ ] Level, pattern and flush policy are configured in one place.
- [ ] Async logging has an explicit shutdown, and the queue-full policy is chosen.
- [ ] No sensitive data in log output.
- [ ] One fmt library is used across the whole build.
