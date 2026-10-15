---
name: serde
title: Serde
area: rust
tags: [rust, serde, json, serialization, derive, deserialization]
detect: [dep:serde, dep:serde_json]
related: [axum, actix-web, clippy, cargo, sqlx]
---
Serde: derive Serialize and Deserialize, control the wire format with attributes, and round-trip test it.

## Verify
- `cargo test`: round-trip and fixture tests pass.
- `cargo check --features serde`: optional derive features compile (only if the crate gates serde behind a feature).
- `cargo clippy --all-targets -- -D warnings`: lint.
- `cargo tree -i serde -e features`: whether `derive` comes from the right place.

## Test first
Pin the exact wire format with a literal, not just a round trip.
```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, PartialEq, Debug)]
#[serde(rename_all = "camelCase")]
struct User { user_id: u32, #[serde(default)] nick: Option<String> }

#[test]
fn reads_camel_case_and_defaults() {
    let u: User = serde_json::from_str(r#"{"userId":7}"#).unwrap();
    assert_eq!(u, User { user_id: 7, nick: None });
}
```
Put wire fixtures in `tests/fixtures/` and compare against them.

## Do
- Enable the derive macros with `serde = { version = "1", features = ["derive"] }`.
- Use `#[serde(rename_all = "...")]` at container level rather than renaming each field.
- Use `#[serde(default)]` and `skip_serializing_if = "Option::is_none"` for optional fields.
- Tag enums explicitly: `#[serde(tag = "type")]`, or `tag` with `content`. Choose it before the format ships.
- Use `#[serde(deny_unknown_fields)]` on strict config structs, not on forward-compatible API payloads.
- Use `#[serde(with = "module")]` or `deserialize_with` for dates and special encodings, and keep the helper in one module.
- Validate after deserializing (a `TryFrom` or `#[serde(try_from = "Raw")]`) so invalid states are unrepresentable.

## Avoid
- Forgetting the `derive` feature: the derive macro is not found. Add the feature.
- `#[serde(untagged)]` enums for large types: errors read "data did not match any variant" and ordering matters. Prefer a tag.
- `serde_json::Value` throughout: type safety is lost. Parse into structs at the boundary.
- Deserializing untrusted input with no limits: cap body size and nesting depth before parsing.
- `#[serde(flatten)]` with `deny_unknown_fields`: they conflict. Pick one.
- Serializing `f64` NaN or `u64` beyond 2^53 for JavaScript clients: they lose precision. Send as strings.
- Using `unwrap()` on `from_str` in handlers: map the error to a 4xx.

## Review
- [ ] The wire format is pinned by a test against a literal, not only a round trip.
- [ ] Optional and missing fields have explicit defaults.
- [ ] Enum representation is deliberate and documented.
- [ ] Untrusted input is size-limited and validated after parse.
- [ ] Renames are consistent across the container.
