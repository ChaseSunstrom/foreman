---
name: cpp-templates
title: C++ templates and concepts
area: idioms
tags: [cpp, templates, concepts, constexpr, metaprogramming, generics]
detect: [file:CMakeLists.txt]
related: [cpp, cmake, googletest]
---
Modern C++ templates: concepts for constraints, `constexpr` for compile-time work, and small templates with clear errors.

## Verify
- `cmake -S . -B build && cmake --build build`: configure and compile; template errors appear at instantiation.
- `ctest --test-dir build --output-on-failure`: the suite, run from the build tree.
- `clang-tidy -p build FILE.cpp`: when configured, flags template and modernization issues.

## Test first
Use `static_assert` for compile-time contracts and a normal test for runtime ones.
```cpp
#include <concepts>
#include <gtest/gtest.h>
#include "sum.hpp"

static_assert(std::same_as<decltype(sum(1, 2)), int>);
static_assert(!requires { sum("a", 1); });  // constraint rejects it

TEST(Sum, AddsMixedIntegers) {
    EXPECT_EQ(sum(2, 3), 5);
}
```

## Do
- Constrain templates with concepts: `template <std::integral T> T sum(T a, T b)`, or a named `concept` with a `requires` expression.
- Use abbreviated templates (`auto` parameters with a concept) for short functions.
- Use `constexpr` and `consteval` functions, and verify with `static_assert`.
- Use `if constexpr` instead of tag dispatch or SFINAE.
- Perfect-forward with `std::forward<T>(x)` only when `T` is a forwarding reference.
- Put template definitions in headers, and use explicit instantiation (`extern template`) when compile time matters.
- Prefer variadic templates with fold expressions over recursion: `(args + ...)`.
- Use standard type traits (`std::is_same_v`, `std::remove_cvref_t`) before writing your own.

## Avoid
- SFINAE with `enable_if` in new code: unreadable errors. Use concepts or `if constexpr`.
- Unconstrained templates: errors surface deep in the instantiation. Add a concept at the interface.
- `std::forward` on a non-forwarding parameter (a `const T&` or a concrete type): it is meaningless. Use `std::move` only when you intend to.
- Template bloat from large bodies in generic code: move type-independent logic into a non-template function.
- Specializing function templates: it interacts badly with overloads. Overload, or specialize a class template.
- Defining templates in a `.cpp` and calling from another: link errors. Keep them in the header.
- `typename` omission for dependent types: add `typename` or use `_t` aliases.

## Review
- [ ] Every public template has a concept or documented requirements.
- [ ] Compile-time contracts are asserted with `static_assert`.
- [ ] Forwarding is used only with forwarding references.
- [ ] No SFINAE tricks where concepts are available at the project's language standard.
- [ ] Error messages for a wrong type were checked and are readable.
