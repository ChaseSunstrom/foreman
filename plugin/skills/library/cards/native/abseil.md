---
name: abseil
title: Abseil (absl)
area: native
tags: [cpp, abseil, absl, status, containers, strings, flags]
detect: [dep:abseil, dep:absl*, dep:abseil-cpp]
related: [cpp-modern, cmake, bazel, googletest, vcpkg]
---
Abseil C++: absl::Status/StatusOr, flat_hash_map, string utilities, time, flags and logging, with correct CMake linking.

## Verify
- `cmake --build build -j`: link errors reveal missing `absl::` targets.
- `ctest --test-dir build --output-on-failure`: suite passes.
- `grep -rn "std::unordered_map" src | head`: spot containers worth moving to `absl::flat_hash_map`.
- `clang-tidy -p build --checks='abseil-*' src/*.cpp`: Abseil-specific modernizations (string-find-startswith, duration arithmetic).

## Test first
Test the error path through `absl::StatusOr` with gMock matchers.
```cpp
#include "gmock/gmock.h"
#include "absl/status/statusor.h"

TEST(Config, MissingKeyIsNotFound) {
    absl::StatusOr<int> r = GetInt(cfg, "port");
    ASSERT_FALSE(r.ok());
    EXPECT_EQ(r.status().code(), absl::StatusCode::kNotFound);
}
```

## Do
- Link per-target: `target_link_libraries(app PRIVATE absl::status absl::statusor absl::flat_hash_map absl::strings)`; use `find_package(absl CONFIG REQUIRED)`.
- Return `absl::Status` or `absl::StatusOr<T>` for fallible calls; check `.ok()` before `.value()` or `*`.
- Build errors with `absl::InvalidArgumentError(absl::StrCat("bad port: ", p))`; use `absl::StrFormat` for printf-style typing.
- Use `absl::flat_hash_map`/`flat_hash_set` for hot lookups; use `node_hash_map` when pointer stability is required.
- Use `absl::string_view`-style APIs via `std::string_view`; split with `absl::StrSplit`, join with `absl::StrJoin`, trim with `absl::StripAsciiWhitespace`.
- Use `absl::Duration` and `absl::Time` instead of raw integers for time.
- Mark guarded data with `ABSL_GUARDED_BY(mu_)` and use `absl::Mutex` with `absl::MutexLock`; compile with `-Wthread-safety` on Clang.

## Avoid
- `.value()` on an error `StatusOr`: aborts the process. Check `ok()` or propagate.
- Depending on `flat_hash_map` iteration order or on pointer/reference stability across inserts: both unspecified. Copy keys out or use node maps.
- Mixing Abseil built with a different C++ standard than the app: ODR and ABI breaks (`absl::string_view` vs `std::string_view`). Use one standard everywhere.
- Linking the monolithic `absl::absl` target when specific targets exist: slow builds, larger binaries.
- Ignoring a returned `Status`: it is `[[nodiscard]]`. Handle it or call `.IgnoreError()` with a comment.
- `absl::Mutex` unlock-before-lock mismatches via manual `Lock()`/`Unlock()`: use `MutexLock`.

## Review
- [ ] Every Status or StatusOr is propagated or handled; none dropped.
- [ ] Error codes match semantics (`kNotFound`, `kInvalidArgument`, `kInternal`).
- [ ] No reliance on hash container ordering.
- [ ] Targets linked are specific, and one C++ standard is used across Abseil and the app.
- [ ] Guarded fields carry thread-safety annotations.
