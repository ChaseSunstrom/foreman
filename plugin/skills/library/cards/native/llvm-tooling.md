---
name: llvm-tooling
title: LLVM and Clang Tooling
area: native
tags: [llvm, clang, ir, opt, lld, compiler, lldb, sanitizers]
detect: [dep:llvm, dep:llvm*, dep:clang, file:*.ll, ext:.ll]
related: [clang-tidy, clang-format, sanitizers, cmake, cpp-modern]
---
LLVM and Clang tools: inspecting IR, optimizer passes, lld, llvm-cov coverage, symbolizing and LLDB, with version-matched toolchains.

## Verify
- `clang --version && llvm-config --version`: compiler and libraries share one version.
- `clang -S -emit-llvm -O2 foo.c -o foo.ll`: emit textual IR to inspect.
- `opt -passes='default<O2>' -S foo.ll -o out.ll`: new pass manager syntax; `opt --print-passes` lists names.
- `llvm-lit -v test/`: run LLVM-style lit tests with FileCheck.
- `clang -fprofile-instr-generate -fcoverage-mapping foo.c -o foo && LLVM_PROFILE_FILE=foo.profraw ./foo && llvm-profdata merge -sparse foo.profraw -o foo.profdata && llvm-cov report ./foo -instr-profile=foo.profdata`: coverage report.

## Test first
LLVM code is tested with lit plus FileCheck; the test fails until the pass or codegen produces the expected IR.
```llvm
; RUN: opt -passes=instcombine -S %s | FileCheck %s
define i32 @f(i32 %x) {
; CHECK-LABEL: @f(
; CHECK-NEXT: ret i32 %x
  %a = add i32 %x, 0
  ret i32 %a
}
```
Run `llvm-lit -v path/to/test.ll`.

## Do
- Configure LLVM builds with `-DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_ASSERTIONS=ON -DLLVM_ENABLE_PROJECTS="clang;lld" -G Ninja`; build out-of-tree.
- Use the new pass manager with `opt -passes=...`; legacy `-instcombine` style flags are removed.
- Link out-of-tree tools with `find_package(LLVM REQUIRED CONFIG)`, `llvm_map_components_to_libnames`, and `separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})`.
- Use `lld` with `-fuse-ld=lld` for faster links; use `-flto=thin` for ThinLTO.
- Symbolize crashes with `llvm-symbolizer`; set `ASAN_SYMBOLIZER_PATH` or `LLVM_SYMBOLIZER_PATH`.
- Debug with `lldb ./app`, `breakpoint set -n main`, `bt`, `frame variable`; build with `-g` and `-O0` for readable state.
- Use `llvm-objdump -d --no-show-raw-insn` and `llvm-nm -C` to inspect binaries.
- Use `FileCheck` directives (`CHECK`, `CHECK-NEXT`, `CHECK-NOT`, `CHECK-LABEL`) rather than diffing whole IR.

## Avoid
- Mixing a distro clang with libLLVM of another version: ABI crashes. Use one install and its `llvm-config`.
- Assertions off in a development build of LLVM-based tools: silent bad IR. Enable `LLVM_ENABLE_ASSERTIONS`.
- Legacy pass manager flags such as `opt -O2 -instcombine`: removed in recent releases. Use `-passes=`.
- Hard-coding LLVM component lists: breaks across versions. Use `llvm_map_components_to_libnames`.
- Matching whole IR text with exact value names in tests: brittle. Use FileCheck captures like `%[[V:.*]]`.
- Running `opt` on unverified IR: add `-verify-each` or run `opt -passes=verify`.
- Building LLVM with default (all) targets and RTTI on without need: huge builds. Set `LLVM_TARGETS_TO_BUILD`.

## Review
- [ ] One LLVM version across compiler, libraries and tools.
- [ ] Tests use FileCheck, with positive and negative checks.
- [ ] Pass pipelines use the new pass manager string syntax.
- [ ] Verifier runs on generated IR.
