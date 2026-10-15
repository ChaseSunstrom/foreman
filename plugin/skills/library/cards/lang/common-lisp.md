---
name: common-lisp
title: Common Lisp
area: lang
tags: [lisp, common-lisp, sbcl, asdf, clos, repl]
detect: [ext:.lisp, ext:.asd, ext:.cl]
related: [racket, prolog]
---
Common Lisp (SBCL and ASDF): systems with packages, CLOS and conditions, tests run non-interactively in batch.

## Verify
- `sbcl --noinform --non-interactive --eval '(asdf:load-system :my-system)'`: the system loads, surfacing compile warnings and undefined functions.
- `sbcl --noinform --non-interactive --eval '(asdf:test-system :my-system)'`: runs the tests the system declares, and exits.
- `sbcl --noinform --non-interactive --load file.lisp`: loads a single file in a clean image.

## Test first
FiveAM (or the repo's framework) with a suite wired to ASDF.
```lisp
(defpackage :my-system/tests (:use :cl :fiveam))
(in-package :my-system/tests)

(def-suite main)
(in-suite main)

(test clamp
  (is (= 3 (my-system:clamp 5 0 3)))
  (is (= 0 (my-system:clamp -1 0 3)))
  (signals type-error (my-system:clamp "a" 0 3)))
```
Declare `:perform (test-op ...)` in the `.asd` so `asdf:test-system` runs it.

## Do
- Define one package per module with an explicit `:export` list and `(in-package ...)` at the top of each file.
- Describe the build in an `.asd` file, with `:depends-on` and `:components` in order.
- Use `defstruct` for plain records and `defclass` with generic functions for polymorphism.
- Use `let`, `let*` and `destructuring-bind` for bindings, and `loop` or `iterate` for iteration.
- Signal and handle errors with conditions: `define-condition`, `handler-case`, `restart-case`, and `unwind-protect` for cleanup.
- Use `with-open-file` and other `with-` macros for resources.
- Declare types and `(declaim (optimize ...))` only in profiled hot paths.
- Keep macros small, generate gensyms with `gensym` or `with-gensyms`, and evaluate arguments once.

## Avoid
- Macros for what a function can do: hard to debug and compose. Write a function and add a macro only for syntax.
- Variable capture in macros: a local name collides with caller code. Use gensyms.
- Evaluating a macro argument more than once: duplicate side effects. Bind it in a `let` first.
- Destructive operations (`sort`, `nreverse`, `delete`) on literal or shared lists: undefined behavior. Use `copy-list` or the non-destructive forms.
- Modifying quoted constants: undefined. Build with `list` or `copy-tree`.
- `eval` and `read-from-string` on untrusted input: code execution. Use `*read-eval*` nil or a parser.
- Global `defvar` state without earmuffs and reset in tests: hidden coupling. Name them `*like-this*` and rebind with `let`.

## Review
- [ ] Packages export only the public API.
- [ ] The system loads clean in a fresh image with no warnings.
- [ ] Macros bind arguments once and use gensyms.
- [ ] No destructive operations on shared or literal data.
- [ ] Tests run through `asdf:test-system`.
