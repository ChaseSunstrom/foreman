---
name: cpp-raii
title: C++ RAII and Ownership
area: native
tags: [cpp, raii, smart-pointers, ownership, lifetime, rule-of-zero, exceptions]
detect: []
related: [cpp-modern, cpp-concurrency, sanitizers, valgrind, clang-tidy]
---
C++ resource ownership: RAII wrappers, unique_ptr custom deleters, rule of zero/five, exception safety.

## Verify
- `cmake -B build-asan -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer -g" && cmake --build build-asan`: leak, use-after-free and double-free detection.
- `ctest --test-dir build-asan --output-on-failure`: runs tests under ASan with LeakSanitizer.
- `clang-tidy -p build --checks='cppcoreguidelines-special-member-functions,cppcoreguidelines-owning-memory,bugprone-use-after-move' src/*.cpp`: special-member, raw ownership and moved-from use.

## Test first
Count acquisitions and releases with a fake resource; the test fails on a leak or double release.
```cpp
struct Probe { static inline int live = 0; Probe(){++live;} ~Probe(){--live;} };

TEST(Handle, ReleasesOnException) {
    Probe::live = 0;
    EXPECT_THROW({ Scoped<Probe> p; throw std::runtime_error("x"); }, std::runtime_error);
    EXPECT_EQ(Probe::live, 0);
}
TEST(Handle, MoveTransfersOwnership) {
    Scoped<Probe> a; auto b = std::move(a);
    EXPECT_EQ(Probe::live, 1);
}
```

## Do
- Follow the rule of zero: hold members that manage themselves (`std::vector`, `std::string`, `unique_ptr`) and write no special members.
- When a class owns a raw handle, define or delete all five: destructor, copy ctor/assign, move ctor/assign. Delete copy for unique handles.
- Wrap C handles with `std::unique_ptr<T, Deleter>` or a small class: `std::unique_ptr<FILE, decltype(&fclose)> f{fopen(p, "r"), &fclose};`.
- Declare move operations `noexcept` so containers move instead of copy on reallocation.
- Create with `std::make_unique`/`std::make_shared`; pass `T&` or `T*` for non-owning use, `unique_ptr` by value to transfer.
- Use `std::shared_ptr` only for real shared ownership; break cycles with `weak_ptr`.
- Keep destructors `noexcept`; log instead of throwing.

## Avoid
- Passing `shared_ptr` by value everywhere: atomic refcount cost and unclear ownership. Pass `const T&`.
- `shared_ptr` from `this` via a second `shared_ptr<T>(this)`: double delete. Inherit `enable_shared_from_this`.
- `unique_ptr<T>` of an incomplete type in a header (pimpl): destructor needed where T is complete. Declare it in the header, define it in the .cpp.
- `new` inside a function-call argument list with other throwing args: leak risk. Use `make_unique`.
- Using an object after `std::move`: only assign or destroy. Reset it explicitly.
- Throwing from a destructor: `std::terminate` during unwinding. Swallow and log.
- Returning `.get()` of a local `unique_ptr`: dangles. Return the `unique_ptr`.

## Review
- [ ] Each resource has exactly one owner, visible from the type.
- [ ] No naked `new`/`delete`, `fopen` without a wrapper, or manual lock/unlock pairs.
- [ ] Special members are all-default (rule of zero) or all-explicit.
- [ ] Move constructor and assignment are `noexcept`.
- [ ] A test throws mid-construction and shows nothing leaks.
