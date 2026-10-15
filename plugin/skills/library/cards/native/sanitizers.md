---
name: sanitizers
title: Sanitizers (ASan, UBSan, TSan, MSan)
area: native
tags: [sanitizers, asan, ubsan, tsan, clang, gcc, memory]
detect: []
related: [valgrind, cmake, meson, bazel, googletest, catch2]
---
Compiler sanitizers for C/C++: build instrumented, run the real tests, treat any report as a failure.

## Verify
- `cmake -S . -B build-asan -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer" && cmake --build build-asan`: an instrumented build exists (use `meson setup -Db_sanitize=address,undefined` for Meson).
- `ASAN_OPTIONS=detect_leaks=1:abort_on_error=1 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 ctest --test-dir build-asan --output-on-failure`: tests abort on the first memory or undefined-behaviour report.
- `cmake -S . -B build-tsan -DCMAKE_CXX_FLAGS="-fsanitize=thread"`: a separate build for data-race checks.
- `ldd build-asan/mytests | grep -i asan`: the binary links the runtime.

## Test first
Reproduce the bug as a test that triggers the report, then fix. The failing result is the sanitizer message with a non-zero exit.
```cpp
TEST(Buffer, CopyDoesNotOverrun) {
  std::vector<char> v(4);
  copy_into(v.data(), "hello world", v.size());   // ASan: heap-buffer-overflow
  SUCCEED();
}
```
Run it in the ASan build: it must fail there before the fix and pass after.

## Do
- Use separate build directories per sanitizer: ASan+UBSan together, TSan alone, MSan alone (Clang, Linux only).
- Build with `-g -O1 -fno-omit-frame-pointer` for readable stacks at usable speed.
- Pass the same flags at link time (`-fsanitize=...` in linker flags, or `CMAKE_EXE_LINKER_FLAGS`/`target_link_options`).
- Set `halt_on_error=1` (UBSan needs `-fno-sanitize-recover=undefined` at compile time to be fatal) so CI fails.
- Run the unit, integration and fuzz tests in the sanitizer build in CI.
- Symbolize reports: install `llvm-symbolizer` or set `ASAN_SYMBOLIZER_PATH`.
- Use `-fsanitize=address,undefined,float-divide-by-zero` or add `integer` checks deliberately when wanted.

## Avoid
- Combining `-fsanitize=address` with `-fsanitize=thread` or `memory`: incompatible. Separate builds.
- Applying flags to the app but not to dependencies you built (MSan especially needs an instrumented libc++): false positives. Rebuild deps or use ASan.
- Suppressing reports with `__attribute__((no_sanitize(...)))` or a suppression file to get green: fix the bug; record any suppression with a reason.
- Running the instrumented binary under Valgrind: ASan and Valgrind conflict. Choose one per run.
- Static linking the libc with ASan, or `-static` generally: the runtime needs dynamic linking on most setups.
- Reading a leak report as noise: `detect_leaks` is on by default for Linux ASan; it often points at a real missing `delete` or ownership cycle.

## Review
- [ ] A CI job runs tests under ASan+UBSan, and another under TSan if threads exist.
- [ ] Reports fail the run; no blanket suppressions.
- [ ] Flags are on both compile and link lines.
- [ ] Bug fixes come with a test that failed under the sanitizer.
- [ ] Sanitizer builds are not shipped.
