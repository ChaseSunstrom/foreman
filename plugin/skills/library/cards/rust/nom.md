---
name: nom
title: nom parser combinators
area: rust
tags: [rust, parsing, nom, combinators, binary, text]
detect: [dep:nom, dep:winnow]
related: [proptest, serde, thiserror-anyhow, criterion]
---
nom parsers: small combinator functions returning IResult, full-input checks, bounded recursion and readable errors.

## Verify
- `cargo test`: every parser has accept and reject cases, including trailing garbage.
- `cargo clippy --all-targets -- -D warnings`: lints.
- `cargo test --release`: deep-recursion inputs don't overflow (run once with a hostile nested sample).
- `cargo bench` (if criterion is present): parsers don't allocate in the hot path.

## Test first
Assert full consumption and the exact remainder.
```rust
#[test]
fn kv_parses_and_leaves_rest() {
    let (rest, (k, v)) = kv("name=bob;x").unwrap();
    assert_eq!((k, v, rest), ("name", "bob", ";x"));
}
#[test]
fn kv_rejects_missing_equals() {
    assert!(kv("name").is_err());
}
```

## Do
- Write each parser as `fn name(i: &str) -> IResult<&str, T>`; build from `tag`, `take_while1`, `alt`, `tuple`, `delimited`, `preceded`, `separated_list0`, `map`, `map_res`, `opt`.
- Use the `complete` variants for whole-buffer text and `streaming` for incremental input; do not mix.
- Finish with `all_consuming(parser)(input)` (or check `rest.is_empty()`) at the top level.
- Return richer errors with `nom::error::VerboseError` or a custom `ParseError`; add `context("field", p)`.
- Use `Parser::parse` and the `Parser` trait style (`tag("a").map(..)`) if on a version that has it; check your version's docs for the exact names.
- Prefer borrowing (`&str`/`&[u8]` slices) and convert to owned types only at the edge.
- Cap recursion depth for nested formats by threading a depth counter.
- Fuzz or property test the top-level parser: it must never panic.

## Avoid
- Forgetting `all_consuming`: `"123abc"` parses as 123 and silently drops the tail. Require full input.
- `many0` over a parser that can succeed consuming nothing: infinite loop (nom errors out, but it's a bug). Ensure progress.
- `alt` order that puts a prefix first (`tag("a")` before `tag("ab")`): shorter branch wins. Longest first.
- `.unwrap()` on parse results of untrusted input: panics. Map to your error type.
- Mixing `&[u8]` and `&str` helpers or `streaming`/`complete` modules: confusing `Incomplete` results.
- Unbounded recursion on nested input: stack overflow. Limit depth.
- Copying nom 4/5 macros (`named!`, `do_parse!`): removed in current versions. Use functions.

## Review
- [ ] Top-level parse requires full input consumption.
- [ ] Every alt branch is ordered so longer matches come first.
- [ ] Errors carry context and convert to the crate's error type.
- [ ] Recursion depth and input length are bounded.
- [ ] Tests include malformed and trailing-garbage input.
