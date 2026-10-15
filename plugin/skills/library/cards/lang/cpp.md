---
name: cpp
title: C++
area: lang
tags: [cpp, cmake, clang-tidy, raii, sanitizers, googletest]
detect: [ext:.cpp, ext:.cc, ext:.cxx, ext:.hpp, file:CMakeLists.txt, file:conanfile.txt, file:vcpkg.json]
related: [c, cmake, rust]
---
Modern C++ baseline: CMake build, RAII and smart pointers, warnings as errors, sanitizers, clang-tidy, GoogleTest or Catch2.

## Verify
- `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug && cmake --build build`: configure and compile.
- `ctest --test-dir build --output-on-failure`: registered tests.
- `cmake -S . -B build-asan -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined"`: a sanitizer build for the test run.
- `clang-tidy -p build src/foo.cpp`: static checks using the compile database (needs `CMAKE_EXPORT_COMPILE_COMMANDS=ON`).
- `clang-format --dry-run -Werror src/foo.cpp`: formatting.

## Test first
GoogleTest (or Catch2), tests in `tests/`, linked via `gtest_discover_tests`.
```cpp
#include <gtest/gtest.h>
#include "port.hpp"

TEST(ParsePort, RejectsEmpty) {
  EXPECT_FALSE(parse_port("").has_value());
}
```

## Do
- Set `CMAKE_CXX_STANDARD`, `CMAKE_CXX_STANDARD_REQUIRED ON` and `CMAKE_EXPORT_COMPILE_COMMANDS ON`; use target-based CMake (`target_link_libraries`, `target_include_directories`).
- Compile with `-Wall -Wextra -Wpedantic -Werror` per target.
- Own resources with RAII: `std::unique_ptr`, `std::vector`, `std::string`, lock guards; create with `std::make_unique`.
- Pass by `const T&` or `std::span`/`std::string_view` for non-owning views; mark single-arg constructors `explicit`.
- Return `std::optional` or `std::expected` (when the standard allows) for expected failures.
- Use `const`, `constexpr`, `[[nodiscard]]` and `override` liberally.
- Follow the rule of zero; if one special member is needed, define all five.

## Avoid
- Raw `new`/`delete` and `malloc` in application code: leaks on exceptions. Use smart pointers and containers.
- `std::string_view` or `span` outliving the owner (including from temporaries): dangling. Keep the owner alive.
- Iterating while inserting or erasing in a container: invalidated iterators. Use erase-remove or save the returned iterator.
- Catching exceptions by value: slicing. Catch by `const&`.
- `using namespace std;` in headers: leaks names into every includer.
- Missing `virtual` destructor on a polymorphic base: undefined behavior on delete. Declare it.
- `shared_ptr` everywhere: cycles and cost. Default to `unique_ptr`, and break cycles with `weak_ptr`.
- Data races on non-atomic shared state: undefined behavior. Use `std::mutex` or `std::atomic` and a TSan run.

## Review
- [ ] No owning raw pointers or manual `delete`; resources are RAII.
- [ ] Views do not outlive their owners.
- [ ] Warnings clean at `-Werror`; sanitizers pass.
- [ ] Polymorphic bases have virtual destructors and `override` is used.
- [ ] Tests registered with CTest and covering an error path.
