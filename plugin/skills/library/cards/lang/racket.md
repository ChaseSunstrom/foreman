---
name: racket
title: Racket
area: lang
tags: [racket, scheme, lisp, functional, macros, rackunit]
detect: [ext:.rkt, ext:.scrbl, file:info.rkt]
related: [common-lisp, prolog]
---
Racket: modules with `#lang racket`, contracts at module boundaries, immutable data and rackunit tests in `test` submodules.

## Verify
- `raco make main.rkt`: compiles the module and its dependencies, surfacing unbound identifiers and syntax errors.
- `raco test .`: runs rackunit tests in the `test` submodules of every file under the directory.
- `raco fmt --help`: only if the formatter is installed; otherwise rely on editor indentation.
- `raco pkg install --auto --name my-pkg`: installs the package in development mode, when it has an `info.rkt`.

## Test first
Tests sit in a `module+ test` at the bottom of the file under test.
```racket
#lang racket

(provide (contract-out [clamp (-> real? real? real? real?)]))

(define (clamp x lo hi) (min hi (max lo x)))

(module+ test
  (require rackunit)
  (check-equal? (clamp 5 0 3) 3)
  (check-equal? (clamp -1 0 3) 0)
  (check-exn exn:fail:contract? (lambda () (clamp "a" 0 3))))
```

## Do
- Start each file with a `#lang` line and use `provide` with `contract-out` for exported functions.
- Prefer immutable data: lists, vectors via `vector-immutable`, hashes via `hash`, and structs without `#:mutable`.
- Define data with `struct`, and use `match` for destructuring and dispatch.
- Use `for` loops and comprehensions (`for/list`, `for/fold`, `for/hash`) instead of manual recursion where clearer.
- Write `define-syntax-rule` or `syntax-parse` macros only when a function cannot express it.
- Use `parameterize` for dynamic context and `raise-argument-error` for bad inputs.
- Use `#lang typed/racket` where static types are wanted, in the modules that need them.

## Avoid
- `set!` on shared variables: mutation breaks reasoning. Thread state through function arguments or `for/fold`.
- Macros for what a higher-order function does: hard to debug. Use functions first.
- Mixing `racket/base` and `racket` indiscriminately: load times and name clashes. Pick `racket/base` for libraries and require what you use.
- `eval` at runtime on built strings: unsafe and hard to trace. Use data and `match`.
- Using `equal?` on huge structures in hot loops: slow. Compare keys, or use `eq?` for symbols.
- Forgetting that `cond` without `else` can return void: add an `else` branch.
- `list-ref` and `length` in loops: quadratic. Use vectors or iterate once.

## Review
- [ ] Exports have contracts and errors name the argument.
- [ ] Data is immutable except where documented.
- [ ] Macros are justified and have tests for the expansion behavior.
- [ ] `raco test` passes and each module has a test submodule.
- [ ] No quadratic list access in loops.
