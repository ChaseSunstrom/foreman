---
name: mojo
title: Mojo
area: lang
tags: [mojo, python, ml, simd, performance, systems]
detect: [ext:.mojo, file:mojoproject.toml, file:pixi.toml]
related: [python, python-performance]
---
Mojo: Python-like syntax with `fn`, typed values, ownership conventions and SIMD, tested with the standard testing module.

## Verify
- `mojo build main.mojo`: compiles to a native binary and reports type and ownership errors.
- `mojo run main.mojo`: compiles and runs once.
- `mojo test`: runs functions whose names start with `test_` in the given files or directories.
- `mojo format .`: formats the sources.

## Test first
Test functions are named `test_*`, use `testing` asserts and live in files named `test_*.mojo`.
```mojo
from testing import assert_equal, assert_raises

fn clamp(x: Int, lo: Int, hi: Int) -> Int:
    return min(hi, max(lo, x))

def test_clamp():
    assert_equal(clamp(5, 0, 3), 3)
    assert_equal(clamp(-1, 0, 3), 0)

def test_raises():
    with assert_raises():
        raise Error("boom")

def main():
    test_clamp()
    test_raises()
```
Mojo changes quickly, so check the installed version's release notes for syntax before relying on a feature.

## Do
- Use `fn` with typed parameters and return types for performance-sensitive code, and `def` for dynamic, Python-style code.
- Declare mutation and ownership through argument conventions: default read-only borrow, `mut` for mutable access and `owned` or `var` to take ownership, per the installed version's docs.
- Use `struct` for static data layouts and `trait` for shared interfaces, with `@value` or explicit lifecycle methods where the toolchain supports them.
- Use `SIMD[DType.float32, width]` and `vectorize` or `parallelize` for data-parallel loops, with the width from `simdwidthof`.
- Mark compile-time parameters in square brackets (`fn f[N: Int]()`) and use `alias` for compile-time constants, per version.
- Use `raises` on functions that throw and handle errors with `try` and `except`.
- Import Python modules through `python` interop only at the edges.
- Benchmark with the `benchmark` module and keep `keep()` on results so work is not optimized away.

## Avoid
- Assuming Python semantics inside `fn`: types, ownership and mutability are enforced. Annotate and pass by the right convention.
- Copying large structs by accident: pass by borrow. Take ownership only when needed.
- Calling Python objects in a hot loop: interop is slow. Move data into typed Mojo structures first.
- Using syntax from old blog posts: keywords such as `inout` and `borrowed` have been renamed across releases. Check the current docs for the installed version.
- Benchmarking a loop whose result is unused: the compiler removes it. Use `keep`.
- Over-wide SIMD or unaligned loads with no tail handling: wrong results at the end. Handle the remainder.

## Review
- [ ] Hot paths use `fn`, typed values and SIMD where it pays off.
- [ ] Ownership conventions are explicit and no needless copies remain.
- [ ] Python interop stays at the boundary.
- [ ] Syntax matches the installed toolchain version.
- [ ] `mojo test` passes.
