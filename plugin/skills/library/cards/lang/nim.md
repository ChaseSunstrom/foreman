---
name: nim
title: Nim
area: lang
tags: [nim, nimble, unittest, compiled, gc, metaprogramming]
detect: [ext:.nim, ext:.nims, ext:.nimble, file:*.nimble, file:nim.cfg]
related: [bash]
---
Nim projects: Nimble packages, `unittest`, ORC memory management, style-insensitive identifiers.

## Verify
- `nim check src/mypkg.nim`: parse and type-check with no codegen.
- `nimble build`: compiles the binaries declared in the `.nimble` file.
- `nimble test`: runs every `tests/t*.nim` (files starting with `t`).
- `nim c -r --hints:off tests/test_parse.nim`: compiles and runs a single test file.
- `nimpretty --backup:off src/mypkg.nim`: formats in place.

## Test first
Tests live in `tests/`, with a `tests/config.nims` adding `--path:"../src"` so imports resolve.
```nim
import unittest
import mypkg/parse

suite "parse":
  test "rejects empty input":
    expect ValueError:
      discard parseAmount("")

  test "returns none on junk when lenient":
    check parseAmountOpt("x").isNone
```

## Do
- Declare `requires "nim >= X"` and package dependencies in the `.nimble` file; set `srcDir` and `bin`.
- Use `Option[T]` (`std/options`) or exceptions with specific types (`raise newException(ValueError, "...")`) at boundaries, and one convention per module.
- Mark exported symbols with `*` and keep the rest private; split into `src/pkg/` modules.
- Use `let` over `var`, and `proc` parameters as `openArray` for read-only sequences or strings.
- Use `defer` for cleanup and `try/finally` around resources; wrap files with `open` plus `defer: close(f)`.
- Compile with `-d:release` for speed measurements and `-d:danger` only after tests pass in both default and release.
- Use `--mm:orc` (the default in current releases) and avoid `{.gcsafe.}` casts to silence thread warnings.

## Avoid
- Relying on global `var` from threaded code: not gcsafe. Pass data via channels or `Isolated`/`Atomic`.
- Using `cast[...]` or unsafe pointer arithmetic when `ptr`/`ref` types and `seq` indexing suffice: memory bugs. Keep casts in one audited place.
- Forgetting `discard` for results you ignore: compile error, and `discard` hides `Result`-like errors. Check or log them.
- Assuming identifier case matters: `fooBar` and `foo_bar` are the same name (first letter is case-sensitive). Don't define lookalikes.
- `import` of whole modules with colliding names in big projects: use `from x import nil` or qualified `x.foo`.
- String building with `&=` in hot loops over a shared seq of strings with copies: use `strutils.join` or `newStringOfCap`.
- Swallowing `CatchableError` with an empty `except:`: catch specific types.

## Review
- [ ] `nimble test` passes and a new test fails without the change.
- [ ] Exported (`*`) surface is intentional, and docs comments (`##`) exist for it.
- [ ] No `cast`, `unsafeAddr` or `{.gcsafe.}` overrides without a comment on why.
- [ ] Dependencies and the Nim version floor are in the `.nimble` file.
- [ ] Resources are closed via `defer` or `finally`.
