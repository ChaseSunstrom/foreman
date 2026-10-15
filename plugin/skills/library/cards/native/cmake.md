---
name: cmake
title: CMake
area: native
tags: [cmake, c, cpp, build, ctest, targets]
detect: [file:CMakeLists.txt, file:CMakePresets.json, file:*.cmake]
related: [googletest, catch2, conan, vcpkg, sanitizers, meson]
---
Target-based CMake builds: presets, modern target_* commands, CTest for tests.

## Verify
- `cmake --preset default && cmake --build --preset default -j`: configure and build from a preset (needs CMakePresets.json).
- `cmake -S . -B build -Wdev -Werror=dev`: configure with CMake's own warnings treated as errors.
- `ctest --test-dir build --output-on-failure`: the registered tests run and print failures.
- `cmake --build build --target help`: the expected targets exist.

## Test first
Tests are registered with `enable_testing()` and `add_test`/`gtest_discover_tests`, usually under `tests/`. Write the failing test, then add it to the build.
```cmake
enable_testing()
add_executable(parser_test tests/parser_test.cpp)
target_link_libraries(parser_test PRIVATE mylib)
add_test(NAME parser_rejects_empty COMMAND parser_test)
```
The test exits non-zero until the behaviour exists; `ctest -R parser_rejects_empty` must fail first.

## Do
- Start with `cmake_minimum_required(VERSION ...)` then `project(... LANGUAGES CXX)`. Set `CMAKE_CXX_STANDARD`, `CMAKE_CXX_STANDARD_REQUIRED ON` and `CMAKE_CXX_EXTENSIONS OFF`, or use `target_compile_features(t PUBLIC cxx_std_20)`.
- Declare everything per target: `target_include_directories`, `target_link_libraries`, `target_compile_definitions`, each with `PUBLIC`/`PRIVATE`/`INTERFACE` chosen deliberately.
- Use `$<BUILD_INTERFACE:...>` and `$<INSTALL_INTERFACE:...>` for include dirs of installable libraries.
- Keep options in CMakePresets.json (generator, build type, toolchain file, cache vars) so CI and developers run the same command.
- Export `compile_commands.json` with `CMAKE_EXPORT_COMPILE_COMMANDS ON` for clang-tidy and IDEs.
- Find dependencies with `find_package(Foo CONFIG REQUIRED)` and link imported targets (`Foo::Foo`).
- Set `CMAKE_BUILD_TYPE` only for single-config generators; use `--config` with Visual Studio or Ninja Multi-Config.

## Avoid
- Global `include_directories`, `link_libraries`, `add_definitions`: they leak into every target. Use the `target_*` forms.
- `file(GLOB ...)` for sources: new files do not trigger a reconfigure. List sources explicitly (or add `CONFIGURE_DEPENDS` knowingly).
- Setting `CMAKE_CXX_FLAGS` by hand for warnings: use `target_compile_options` with `$<$<CXX_COMPILER_ID:GNU,Clang>:-Wall>`-style generator expressions, or `/W4` for MSVC.
- Linking by raw path or `-lfoo`: use imported or alias targets so usage requirements propagate.
- `FetchContent` of a dependency without pinning a `GIT_TAG` hash or `URL_HASH`: builds stop being reproducible.
- Putting `project()` after `add_subdirectory` or omitting it: compiler variables are unset.
- Editing generated files in the build dir: re-run configure instead.

## Review
- [ ] No directory-scope `include_directories`/`add_definitions`; visibility keywords on every `target_link_libraries`.
- [ ] Sources are listed explicitly, tests registered with `add_test` or discovery.
- [ ] A preset or documented command configures, builds and tests from clean.
- [ ] Installable targets have `install(TARGETS ... EXPORT ...)` and a config file if consumed by others.
- [ ] Third-party fetches are pinned.
