---
name: proptest
title: proptest
area: rust
tags: [rust, testing, property-based, proptest, fuzz, shrinking]
detect: [dep:proptest, dep:proptest-derive]
related: [criterion, serde, cargo, clippy]
---
Property-based tests with proptest: strategies, round-trip and invariant properties, shrinking and regression files.

## Verify
- `cargo test`: properties run (256 cases each by default).
- `PROPTEST_CASES=5000 cargo test`: a deeper run before merging risky logic.
- `git status proptest-regressions`: new failure seeds were saved and are committed.
- `cargo clippy --all-targets -- -D warnings`: lints on test code.

## Test first
State the property, run it, watch it fail with a shrunk counterexample.
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn encode_decode_roundtrip(s in "\\PC{0,64}") {
        let enc = encode(&s);
        prop_assert_eq!(decode(&enc).unwrap(), s);
    }
}
```

## Do
- Pick properties: round trip (`decode(encode(x)) == x`), idempotence, invariants (sorted, length preserved), oracle (compare to a simple slow version), no panic on any input.
- Compose strategies: `prop::collection::vec(any::<u8>(), 0..100)`, `prop_oneof!`, `.prop_map`, `.prop_filter`, `.prop_flat_map`.
- Derive with `#[derive(Arbitrary)]` (proptest-derive) for plain types, or write a strategy fn returning `impl Strategy<Value = T>`.
- Use `prop_assert!`/`prop_assert_eq!` inside `proptest!` so shrinking works; `prop_assume!` to discard.
- Commit the `proptest-regressions/` files: they replay past failures first.
- Configure with `#![proptest_config(ProptestConfig::with_cases(1000))]` inside the block.
- Keep the fixed example tests too: a failing seed becomes a plain `#[test]`.

## Avoid
- `assert!` in the body: panics shrink worse and lose context. Use `prop_assert!`.
- Over-filtering with `prop_filter`: "too many local rejects" aborts. Build valid values with `prop_map` or a constrained strategy.
- Non-deterministic bodies (clock, RNG, network): shrinking and replay break. Inject them.
- Unbounded sizes (`any::<String>()` into a heavy fn): slow runs. Bound collections and ranges.
- Reimplementing the code under test as the oracle: the same bug passes. Use a simpler model.
- Ignoring `proptest-regressions` in .gitignore: failures are lost on CI.

## Review
- [ ] Each property names a real invariant, not a restated implementation.
- [ ] Inputs are bounded and valid by construction.
- [ ] Regression files are committed.
- [ ] `prop_assert*` is used inside `proptest!`.
- [ ] Case counts are reasonable for CI runtime.
