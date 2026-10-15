---
name: gleam
title: Gleam
area: lang
tags: [gleam, beam, functional, gleeunit, hex, types]
detect: [ext:.gleam, file:gleam.toml, dep:gleam_stdlib, dep:gleeunit]
related: [erlang]
---
Gleam on the BEAM (or JavaScript): statically typed, immutable, `Result` errors, gleeunit tests, Hex packages.

## Verify
- `gleam format --check src test`: formatting is canonical.
- `gleam check`: type-checks without producing output.
- `gleam test`: runs gleeunit over `test/`.
- `gleam build --warnings-as-errors`: compiles and fails on warnings such as unused values or unreachable patterns.

## Test first
Tests live in `test/<pkg>_test.gleam`; any public function whose name ends `_test` runs.
```gleam
import gleeunit
import gleeunit/should
import mypkg/parse

pub fn main() {
  gleeunit.main()
}

pub fn parse_rejects_empty_test() {
  parse.int("")
  |> should.equal(Error(parse.Empty))
}
```
Dependencies for tests go under `[dev-dependencies]` in `gleam.toml` (`gleeunit`).

## Do
- Model failure as `Result(a, MyError)` with a custom error type; chain with `use x <- result.try(...)`.
- Model states as custom types and match exhaustively, with no catch-all `_` on types you own.
- Keep modules small and mark only the API `pub`; use `pub opaque type` to hide constructors.
- Use the pipe `|>` and labelled arguments (`name: value`) for readable calls.
- Choose a target in `gleam.toml` (`target = "erlang"` or `"javascript"`) and avoid `@external` unless a package is missing.
- Add dependencies with `gleam add <pkg>` so `manifest.toml` stays in sync; commit `manifest.toml`.
- For concurrency on Erlang, use `gleam_otp` actors and supervisors instead of ad hoc processes.

## Avoid
- `let assert` and `panic`/`todo` in library paths: crash at runtime. Return a `Result` and use `let assert` only in tests or true invariants (with a message `as "..."`).
- Ignoring a `Result` with `let _ =`: errors vanish. Handle or propagate.
- `dynamic` decoding by hand with old `decode` APIs from memory: they changed across releases. Use `gleam/dynamic/decode` per the installed version's docs.
- Misusing `@external` FFI with wrong arity or types: the compiler can't check it. Keep externals tiny and tested.
- Deep recursion without tail calls on large lists: Gleam optimizes tail calls only. Use an accumulator or `list.fold`.
- Treating `Int` division by zero as an error: `x / 0` returns `0`. Check explicitly.
- Relying on APIs from memory: the stdlib has renamed and removed functions between releases. Check the compiler error and the package docs.

## Review
- [ ] `gleam format --check`, `gleam check` and `gleam test` pass with no warnings.
- [ ] No `let assert`, `panic` or `todo` outside tests without a justification.
- [ ] Public API is minimal and types are opaque where invariants exist.
- [ ] Every `Result` is handled or propagated.
- [ ] Target-specific code is isolated, and tests run for each declared target.
