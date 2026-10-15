---
name: googletest
title: GoogleTest and GoogleMock
area: native
tags: [googletest, gtest, gmock, cpp, testing, unit-tests]
detect: [dep:gtest, dep:googletest, dep:GTest, file:*_test.cc, file:*_test.cpp]
related: [cmake, bazel, catch2, sanitizers, valgrind]
---
GoogleTest C++ unit tests: TEST/TEST_F, EXPECT vs ASSERT, GoogleMock for interfaces, CTest discovery.

## Verify
- `ctest --test-dir build --output-on-failure`: discovered tests run (CMake with `gtest_discover_tests`).
- `./build/tests/mytests --gtest_filter='Parser.*' --gtest_repeat=50 --gtest_shuffle`: order dependence and flakiness show.
- `./build/tests/mytests --gtest_list_tests`: the test you wrote is registered.
- `./build/tests/mytests --gtest_brief=1`: only failures are printed.

## Test first
Tests live in `tests/*_test.cc`, linked to `GTest::gtest_main` (or `gtest_main` with `gmock`).
```cpp
#include <gtest/gtest.h>
#include "parser.h"

TEST(Parser, RejectsEmptyInput) {
  auto r = Parse("");
  ASSERT_FALSE(r.ok());
  EXPECT_EQ(r.error(), "empty");
}
```
```cmake
find_package(GTest CONFIG REQUIRED)
add_executable(mytests tests/parser_test.cc)
target_link_libraries(mytests PRIVATE mylib GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(mytests)
```

## Do
- Name tests `TEST(Suite, Behaviour)` with no underscores in either name.
- Use `ASSERT_*` when later lines would crash if the check fails (null pointers, size before indexing); use `EXPECT_*` otherwise to report more failures.
- Use `TEST_F` with a fixture class for shared setup (`SetUp`/`TearDown`), and `TEST_P` with `INSTANTIATE_TEST_SUITE_P` for table-driven cases.
- Use `EXPECT_THAT(x, matcher)` with gmock matchers (`ElementsAre`, `HasSubstr`, `Pair`) for containers and strings.
- Mock only interfaces you own: `MOCK_METHOD(ReturnType, Name, (Args), (override));` then `EXPECT_CALL(mock, Name(_)).WillOnce(Return(...))`.
- Use `EXPECT_DEATH`/`ASSERT_DEATH` with a regex for fatal paths, in a suite named `*DeathTest`.
- Use `SCOPED_TRACE` inside helper functions so failures point to the caller.

## Avoid
- Old macro names (`INSTANTIATE_TEST_CASE_P`, `TYPED_TEST_CASE`): deprecated. Use `INSTANTIATE_TEST_SUITE_P`, `TYPED_TEST_SUITE`.
- Old gmock syntax `MOCK_METHOD1(name, ret(arg))`: use `MOCK_METHOD`.
- `ASSERT_*` in a helper that returns a value: it only returns from that function; wrap with `ASSERT_NO_FATAL_FAILURE` or use `EXPECT`.
- `EXPECT_EQ(ptr, NULL)` or `EXPECT_EQ(str.c_str(), "x")`: compares pointers. Use `EXPECT_EQ(ptr, nullptr)` and compare `std::string`/`EXPECT_STREQ`.
- `EXPECT_EQ(1.0/3, x)` on floats: use `EXPECT_NEAR` or `EXPECT_DOUBLE_EQ`.
- Mock expectations set after the call under test, or `Mock::VerifyAndClearExpectations` forgotten on a leaked mock: expectations never run.
- Tests that share global state or rely on order: shuffle will expose them; reset state in `SetUp`.

## Review
- [ ] Each test checks one behaviour with a name that states it.
- [ ] ASSERT vs EXPECT is chosen so a failure cannot cause a crash.
- [ ] Mocks have explicit `EXPECT_CALL` counts; no uninteresting-call warnings ignored.
- [ ] Tests pass with `--gtest_shuffle --gtest_repeat`.
- [ ] CTest discovers the tests (no manual `add_test` per case).
