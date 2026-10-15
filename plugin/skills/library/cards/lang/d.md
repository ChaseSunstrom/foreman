---
name: d
title: D
area: lang
tags: [d, dlang, dub, systems, ranges, templates]
detect: [ext:.d, file:dub.json, file:dub.sdl]
related: [cpp, rust]
---
D: `@safe` code by default, ranges and templates for generic code, `unittest` blocks and dub for the build.

## Verify
- `dub build`: compiles the package with its dependencies.
- `dub test`: builds with `-unittest` and runs every `unittest` block.
- `dub build --build=release`: the optimized build still compiles, since release mode removes contracts and asserts.
- `dub lint`: static analysis, when dscanner is available.

## Test first
`unittest` blocks live next to the code they test.
```d
int clamp(int x, int lo, int hi) @safe pure
{
    return x < lo ? lo : (x > hi ? hi : x);
}

unittest
{
    assert(clamp(5, 0, 3) == 3);
    assert(clamp(-1, 0, 3) == 0);
    import std.exception : assertThrown;
    assertThrown!Error(assert(false));
}
```

## Do
- Mark functions `@safe`, `pure` and `nothrow` where true, and `@trusted` only on small audited wrappers.
- Use ranges and `std.algorithm` and `std.range` pipelines (`map`, `filter`, `array`) with UFCS for readable chains.
- Use `in` and `out` contracts and `invariant` for classes and structs.
- Prefer `struct` for values and `class` for polymorphic reference types, with `scope` or `RAII` for lifetime.
- Use `enum` for compile-time constants and `static if`, `static foreach` for compile-time branches.
- Use templates with constraints: `T foo(T)(T x) if (isNumeric!T)`.
- Use slices (`T[]`) for views and `.dup` or `.idup` when ownership is needed.
- Use `scope(exit)` and `scope(failure)` for cleanup near the allocation.

## Avoid
- Relying on `assert` and contracts in release builds: `-release` removes them. Use `enforce` for checks that must stay.
- Returning a slice of a stack array: it dangles. Return `.dup` or use `@safe` and `return scope` checks.
- Appending to a slice in a loop with no reserve: repeated reallocation. Use `Appender` or `reserve`.
- `@trusted` over large bodies: it disables safety checks wholesale. Keep it to the minimal expression.
- Unconstrained templates: error messages come from deep inside. Add signature constraints.
- Garbage collector allocations in a hot `@nogc` path: use `@nogc` annotations to enforce and manage memory explicitly.
- Mutating a range while iterating it: invalid. Collect first or use indexes.

## Review
- [ ] Functions carry the strongest attributes they honestly can.
- [ ] Every public function has a `unittest` including a failure case.
- [ ] Checks that must survive `-release` use `enforce`.
- [ ] No dangling slices or oversized `@trusted` blocks.
- [ ] `dub test` passes.
