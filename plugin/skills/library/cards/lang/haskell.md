---
name: haskell
title: Haskell
area: lang
tags: [haskell, ghc, cabal, stack, hspec, hlint]
detect: [ext:.hs, ext:.lhs, file:*.cabal, file:cabal.project, file:stack.yaml, file:package.yaml]
related: [scala]
---
Haskell baseline: cabal or stack builds, -Wall in CI, hlint and a formatter, hspec or tasty with QuickCheck, total functions and strict where it counts.

## Verify
- `cabal build all`: everything compiles (or `stack build`).
- `cabal test all --test-show-details=direct`: test suites with output (or `stack test`).
- `hlint .`: idiom and redundancy hints.
- `cabal check`: package description problems before publishing.
- `ormolu --mode check $(git ls-files '*.hs')`: formatting, when Ormolu is the project formatter (or `fourmolu`).

## Test first
hspec (or tasty) in `test/Spec.hs`, with QuickCheck properties for invariants. Declare a `test-suite` in the cabal file.
```haskell
import Test.Hspec
import PortParser (parsePort)

main :: IO ()
main = hspec $
  describe "parsePort" $
    it "rejects empty input" $
      parsePort "" `shouldBe` Left "invalid"
```

## Do
- Set `ghc-options: -Wall -Wcompat -Widentities -Wincomplete-record-updates` (and `-Werror` in CI); fix incomplete-pattern warnings.
- Keep a tight `build-depends` with bounds; commit `cabal.project.freeze` or the stack resolver for applications.
- Return `Maybe` or `Either e` for partial results; use `case` and total functions.
- Use `newtype` wrappers for domain values (ports, ids) to stop argument mix-ups.
- Use `Data.Text` and `Data.ByteString` instead of `String` for real text and bytes.
- Use strict fields (`!Int`) and `foldl'` for accumulators.
- Wrap resources in `bracket` or `withFile`; use `Control.Exception.try` with a specific exception type.

## Avoid
- Partial functions (`head`, `tail`, `fromJust`, `!!`, `read`): runtime crashes. Use pattern matching, `listToMaybe`, `readMaybe`.
- `foldl` and lazy accumulators over big inputs: thunk build-up and stack or memory blowups. Use `foldl'` and bang patterns.
- `String` for large text: linked list of Char. Use `Text`.
- Lazy IO (`getContents`, `readFile` then late use): handle closed or held open unexpectedly. Use strict reads or streaming libraries.
- `catch` with a bare `SomeException` handler that swallows async exceptions like `ThreadKilled`: breaks cancellation. Catch specific types, or rethrow async ones.
- `unsafePerformIO` for convenience: breaks purity and sharing. Move effects to IO.
- Orphan instances and blanket `{-# LANGUAGE ... #-}` piles: confusing resolution. Define instances with the type or class; enable extensions per module.
- Leaving `-Wall` warnings (unused, incomplete patterns): real bugs hide among them.

## Review
- [ ] No new partial functions; incomplete-pattern warnings resolved.
- [ ] Accumulators and fields are strict where data is large.
- [ ] Text and bytes use Text and ByteString, not String.
- [ ] Exceptions caught by specific type; resources released with bracket.
- [ ] `-Wall` clean, hlint clean and tests run in CI.
