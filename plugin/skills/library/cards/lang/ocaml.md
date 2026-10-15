---
name: ocaml
title: OCaml
area: lang
tags: [ocaml, dune, opam, functional, ocamlformat, alcotest]
detect: [ext:.ml, ext:.mli, file:dune-project, file:*.opam, file:.ocamlformat]
related: [bash]
---
OCaml projects: dune builds, opam switches, ocamlformat, Alcotest or ppx_expect tests, explicit interfaces.

## Verify
- `dune build 2>&1 | head -50`: compiles with the dune profile's warnings (dev profile makes many warnings errors).
- `dune build @fmt`: ocamlformat diff is empty (needs a `.ocamlformat` file; apply with `dune fmt`).
- `dune test`: runs every `(test ...)` stanza and expect-test diff.
- `opam install . --deps-only --with-test`: the opam file lists every dependency the code uses.

## Test first
Tests live in `test/` with a `dune` stanza `(test (name test_foo) (libraries mylib alcotest))`.
```ocaml
let test_parse_rejects_empty () =
  Alcotest.(check (result int string))
    "empty input" (Error "empty") (Mylib.Parse.int "")

let () =
  Alcotest.run "parse"
    [ "parse", [ Alcotest.test_case "empty" `Quick test_parse_rejects_empty ] ]
```
Run `dune test`; it fails until `Parse.int` returns `Error "empty"`.

## Do
- Write a `.mli` for every public module; export abstract types and keep constructors private.
- Return `result` or `option` for expected failures; reserve exceptions for bugs and use `Fun.protect ~finally` for cleanup.
- Pattern match exhaustively and avoid wildcard `_` on variants you own, so new cases break the build.
- Use `(libraries ...)` in dune and keep `dune-project` `(generate_opam_files true)` so the opam file never drifts.
- Pin the ocamlformat version in `.ocamlformat` (`version=...`) so CI and editors agree.
- Use `Stdlib` modules (`List`, `Option`, `Result`, `Seq`, `Hashtbl`) before adding Base or Core.

## Avoid
- `List.hd`, `List.nth`, `Option.get`, `Hashtbl.find` on unchecked input: they raise. Match, or use `List.nth_opt`, `Hashtbl.find_opt`.
- Polymorphic `=` and `compare` on functional values, cyclic data or abstract types: runtime exception or wrong order. Use a typed `equal`/`compare`.
- Silencing warnings with `-w -a` or `[@@@warning "-32"]` blanket: the unused-value and fragile-match warnings find real bugs. Delete the dead code.
- `Str` or hand-rolled string parsing for structured input: use a real parser (Angstrom, Menhir) or `Scanf` for trivial formats.
- Mutating a global `ref` for state: pass state explicitly or hide it behind an `.mli`.
- Mixing `open Core` and Stdlib in one file: shadowed names change semantics silently.

## Review
- [ ] Each new module has an `.mli` and exposes only what callers need.
- [ ] No partial functions on user input; every `match` is exhaustive without a catch-all.
- [ ] `dune build @fmt` and `dune test` pass with no `dune promote` of unreviewed output.
- [ ] Dependencies are declared in `dune-project` or the opam file, not only installed locally.
- [ ] Resources are closed on every path (`Fun.protect`, `In_channel.with_open_bin`).
