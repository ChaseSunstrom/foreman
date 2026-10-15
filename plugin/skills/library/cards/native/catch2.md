---
name: catch2
title: Catch2
area: native
tags: [catch2, cpp, testing, bdd, unit-tests, matchers]
detect: [dep:catch2, dep:Catch2, file:*.test.cpp]
related: [cmake, googletest, sanitizers, conan, vcpkg]
---
Catch2 v3 C++ tests: TEST_CASE with SECTIONs, REQUIRE/CHECK, generators and matchers, linked as a library.

## Verify
- `ctest --test-dir build --output-on-failure`: tests run (CMake with `catch_discover_tests`).
- `./build/tests/mytests --list-tests`: the new test case is registered.
- `./build/tests/mytests "[parser]" --order rand --rng-seed time`: tests tagged `[parser]` run in random order and pass.
- `./build/tests/mytests -s`: passing assertions are printed too, for debugging.

## Test first
Tests live in `tests/*.cpp`, linked to `Catch2::Catch2WithMain`.
```cpp
#include <catch2/catch_test_macros.hpp>
#include "parser.h"

TEST_CASE("parser rejects empty input", "[parser]") {
  auto r = Parse("");
  REQUIRE_FALSE(r.ok());
  CHECK(r.error() == "empty");
}
```
```cmake
find_package(Catch2 3 REQUIRED)
add_executable(mytests tests/parser.cpp)
target_link_libraries(mytests PRIVATE mylib Catch2::Catch2WithMain)
include(Catch)
catch_discover_tests(mytests)
```

## Do
- Include the narrow headers (`<catch2/catch_test_macros.hpp>`, `<catch2/matchers/catch_matchers_string.hpp>`, `<catch2/generators/catch_generators.hpp>`) to keep compile times down.
- Use `REQUIRE` when later lines depend on the check, `CHECK` to continue and collect failures.
- Share setup with `SECTION`s: the test case is re-run once per leaf section, so each starts from fresh state.
- Use `GENERATE(values(...))`/`table<...>` for data-driven cases, and `TEMPLATE_TEST_CASE` for types.
- Use `REQUIRE_THAT(x, Catch::Matchers::ContainsSubstring("..."))` and `REQUIRE_THROWS_AS`/`REQUIRE_THROWS_WITH` for errors.
- Compare floats with `Catch::Approx` (`x == Approx(1.0).margin(1e-9)`), or `WithinAbs`/`WithinRel` matchers.
- Tag test cases (`"[slow]"`, `"[.]"` to hide by default) and filter by tag in CI.

## Avoid
- The v2 single header `#include <catch2/catch.hpp>` and `#define CATCH_CONFIG_MAIN` in v3 projects: v3 is a compiled library, use `Catch2::Catch2WithMain`. Check which major the project pins before copying snippets.
- `Matchers::Contains` for strings (v2 name): v3 uses `ContainsSubstring`, `StartsWith`, `EndsWith`.
- `REQUIRE(a == b)` on complex expressions with side effects or `&&`/`||`: Catch decomposes only simple comparisons. Compute into variables first.
- Mutable state shared between SECTIONs outside the test case: sections re-run the case, so put state inside.
- Assertions from other threads: Catch assertions are not thread safe in the older releases; collect results and assert on the main thread.
- Forgetting `catch_discover_tests`: CTest runs one opaque executable.

## Review
- [ ] Test names state the behaviour and carry a tag.
- [ ] REQUIRE vs CHECK chosen so failures cannot crash later lines.
- [ ] Sections do not depend on each other's side effects.
- [ ] Only needed Catch2 headers are included.
- [ ] Random order passes (`--order rand`).
