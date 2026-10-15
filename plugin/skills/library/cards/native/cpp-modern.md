---
name: cpp-modern
title: Modern C++ (17/20/23)
area: native
tags: [cpp, c++20, c++17, stl, ranges, types, safety]
detect: [ext:.cpp, ext:.cc, ext:.hpp, file:CMakeLists.txt]
related: [cmake, clang-tidy, clang-format, sanitizers, googletest, cpp-raii]
---
Modern C++ idioms: value semantics, std::span/string_view/optional/variant/expected, ranges, constexpr, warnings as errors.

## Verify
- `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror"`: configure with strict warnings.
- `cmake --build build -j && ctest --test-dir build --output-on-failure`: builds clean and tests pass.
- `clang-tidy -p build src/*.cpp`: modernize, bugprone and cppcoreguidelines checks.
- `cmake -B build-asan -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"`: sanitizer build for UB and lifetime bugs.

## Test first
Use GoogleTest or Catch2 from `tests/`. Test the edge that raw pointers and C arrays get wrong.
```cpp
#include <gtest/gtest.h>
#include "parse.hpp"

TEST(Parse, EmptyInputYieldsNullopt) {
    EXPECT_EQ(parse_port(""), std::nullopt);
    EXPECT_EQ(parse_port("70000"), std::nullopt);
    EXPECT_EQ(parse_port("8080"), std::optional<int>{8080});
}
```

## Do
- Set `CMAKE_CXX_STANDARD`, `CMAKE_CXX_STANDARD_REQUIRED ON` and `CMAKE_CXX_EXTENSIONS OFF` explicitly.
- Pass non-owning views as `std::span<const T>` and `std::string_view`; return owning types by value (copy elision, move).
- Model absence with `std::optional`, closed alternatives with `std::variant` + `std::visit`, fallible results with `std::expected` (C++23) or a project Result type.
- Mark `[[nodiscard]]` on functions whose result must be checked; `explicit` on single-arg constructors; `noexcept` on moves.
- Use `constexpr`/`consteval` for tables and validation; use `static_assert` for layout assumptions.
- Prefer `std::ranges` algorithms and views over index loops; use `enum class`.
- Use structured bindings, `if` with initializer, and `std::format` (C++20) over printf or stream chains.

## Avoid
- `new`/`delete` or `malloc` in app code: use `std::make_unique`/`make_shared` and containers.
- `std::string_view` stored past the owner's life, or built from a temporary `std::string`: dangling. Store `std::string` when owning.
- `using namespace std;` in headers: pollutes every includer. Qualify names.
- C-style casts: use `static_cast`, and treat `reinterpret_cast` as a review flag.
- `std::move` on a `const` object or on a return local: it copies or blocks elision. Just `return x;`.
- Signed/unsigned comparisons and `int` for sizes: use `std::size_t` or `std::ssize`, and compile with `-Wconversion`.
- `std::endl` in loops: it flushes; use `'\n'`.

## Review
- [ ] No owning raw pointers; ownership is visible in types.
- [ ] Views and references never outlive what they point to.
- [ ] Every switch over an enum handles all cases with no `default` hiding new ones.
- [ ] Warnings clean at `-Wall -Wextra`; sanitizer run passes.
- [ ] Headers are self-contained and carry include guards or `#pragma once`.
