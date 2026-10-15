---
name: clojure
title: Clojure
area: lang
tags: [clojure, jvm, functional, repl, deps-edn, leiningen]
detect: [ext:.clj, ext:.cljc, ext:.cljs, file:deps.edn, file:project.clj, file:bb.edn]
related: [groovy]
---
Clojure projects: deps.edn or Leiningen, clojure.test, clj-kondo lint, REPL-driven development.

## Verify
- `clj-kondo --lint src test`: static lint (unused bindings, wrong arity, unresolved symbols).
- `cljfmt check`: formatting, if cljfmt is configured (`lein cljfmt check` under Leiningen).
- `clojure -M:test` (alias name varies; see `deps.edn`), or `lein test`: runs the suite.
- `clojure -M -e "(require 'my.ns) (println :ok)"`: the namespace loads with no reflection or missing-require error.

## Test first
Tests mirror source namespaces: `src/my/core.clj` has `test/my/core_test.clj` (underscore in file, hyphen in ns).
```clojure
(ns my.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [my.core :as core]))

(deftest parse-amount
  (testing "blank input is rejected"
    (is (nil? (core/parse-amount "")))
    (is (thrown? clojure.lang.ExceptionInfo (core/parse-amount! "")))))
```
Use `clojure.test.check` for properties and `with-redefs` only for impure edges.

## Do
- Keep functions pure and data-first; push I/O to the edges and pass dependencies in a map (or use Integrant, Component, or Mount).
- Validate boundaries with `clojure.spec.alpha` or Malli, not scattered `assert`.
- Throw `ex-info` with a data map so callers can dispatch on `ex-data`.
- Use `(set! *warn-on-reflection* true)` in hot or interop code and add type hints where it warns.
- Prefer `reduce`, `into` with transducers and `update`/`assoc-in` over loops and atoms.
- Use `:refer`-free `:as` requires and keep one namespace per file; `clj-kondo` config in `.clj-kondo/config.edn`.

## Avoid
- Lazy sequences escaping a `with-open` or `binding` scope: they realize after the resource closes. Wrap in `doall` or `vec` inside.
- `def` inside a function: creates a global. Use `let`.
- `(use ...)` or `(:use ...)` and `:refer :all`: name collisions and unreadable provenance. Use `:as`.
- Nested atoms or `swap!` with side effects: the function may retry. Keep `swap!` functions pure.
- `read-string` or `eval` on untrusted input: code execution. Use `clojure.edn/read-string`.
- Forgetting AOT or classpath changes need a REPL restart after editing `deps.edn`.

## Review
- [ ] clj-kondo reports no new warnings and no unresolved symbols.
- [ ] Side effects sit in clearly named functions (`!` suffix) and not inside `swap!` or `map` bodies.
- [ ] Lazy results are realized before the scope that backs them ends.
- [ ] Error paths use `ex-info` with data, and tests assert the data.
- [ ] No reflection warnings in changed interop code.
