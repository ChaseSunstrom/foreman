---
name: clang-tidy
title: clang-tidy
area: native
tags: [cpp, c, static-analysis, lint, clang, compile-commands, checks]
detect: [file:.clang-tidy]
related: [clang-format, cmake, cpp-modern, sanitizers, llvm-tooling, ccache]
---
clang-tidy: a .clang-tidy check set driven by compile_commands.json, with warnings-as-errors and header filters.

## Verify
- `cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`: writes `build/compile_commands.json`, which clang-tidy needs.
- `clang-tidy -p build src/foo.cpp`: lint one file with the repo's `.clang-tidy`.
- `clang-tidy -p build --list-checks`: shows the checks actually enabled.
- `run-clang-tidy -p build -quiet`: lint the whole compile database in parallel.
- `clang-tidy -p build --warnings-as-errors='*' src/foo.cpp`: non-zero exit on any finding (CI gate).

## Test first
For a new check set, add a file that must trigger it; the lint fails first.
```cpp
// tests/lint/bad.cpp
int* make() { return new int(3); }   // cppcoreguidelines-owning-memory
void f(std::vector<int> v) { (void)v.size(); } // performance-unnecessary-value-param
```
Run `clang-tidy -p build tests/lint/bad.cpp --warnings-as-errors='*'` and expect a non-zero exit; fix the config or code until the intended checks fire, then remove the file.

## Do
- Commit `.clang-tidy` with `Checks: 'bugprone-*,performance-*,modernize-*,readability-*,-modernize-use-trailing-return-type'` and `WarningsAsErrors: ''` locally, `'*'` in CI.
- Set `HeaderFilterRegex: '^(src|include)/'` so project headers are checked and third-party ones are not.
- Create the compile database through CMake (`CMAKE_EXPORT_COMPILE_COMMANDS`), or `bear -- make` for Make builds.
- Enable in CMake with `set(CMAKE_CXX_CLANG_TIDY clang-tidy)` for per-build linting, or run `run-clang-tidy` in CI.
- Apply mechanical fixes with `clang-tidy -p build --fix` or `run-clang-tidy -fix`, then review the diff and rebuild.
- Silence a justified finding on one line with `// NOLINT(check-name)` or `// NOLINTNEXTLINE(check-name)` and a reason.
- Pin the clang-tidy version in CI; check names and behavior change between releases.

## Avoid
- Enabling `*` wholesale: thousands of style findings that bury bugs. Start with bugprone, performance and a short modernize list.
- Bare `// NOLINT` without a check name: hides future findings. Name the check.
- Running with a stale `compile_commands.json`: wrong flags and missing includes. Regenerate after CMake changes.
- Running `--fix` over generated code or on a dirty tree: unreviewable diffs. Commit first and exclude generated paths.
- GCC-only flags in the compile database: clang-tidy errors out. Use `--extra-arg=-Wno-unknown-warning-option` or the same compiler family.
- Treating `clang-diagnostic-error` as a lint finding: it is a compile error, fix the build.

## Review
- [ ] `.clang-tidy` is committed, and its check list has a reason for each exclusion.
- [ ] CI runs it with warnings as errors on changed or all files.
- [ ] Each NOLINT names its check and explains why.
- [ ] Automated fixes were reviewed and tests still pass.
