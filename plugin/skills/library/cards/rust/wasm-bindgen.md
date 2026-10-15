---
name: wasm-bindgen
title: wasm-bindgen
area: rust
tags: [rust, wasm, webassembly, javascript, browser, bindgen]
detect: [dep:wasm-bindgen, dep:wasm-bindgen-futures, dep:web-sys, dep:js-sys]
related: [cargo, clippy, serde, rust-unsafe]
---
Rust to WebAssembly with wasm-bindgen: exported APIs, JS interop, build targets, and browser-run tests.

## Verify
- `cargo check --target wasm32-unknown-unknown`: the crate compiles for the wasm target.
- `wasm-pack build --target web`: builds and generates the JS glue and `.d.ts` (use `bundler` or `nodejs` for those targets).
- `wasm-pack test --headless --chrome`: runs `wasm_bindgen_test` tests in a real browser (or `--node`).
- `cargo clippy --target wasm32-unknown-unknown -- -D warnings`: lint for the wasm cfg.

## Test first
Use `wasm-bindgen-test` and drive the exported function as JS would.
```rust
use wasm_bindgen_test::*;
wasm_bindgen_test_configure!(run_in_browser);

#[wasm_bindgen_test]
fn greet_rejects_empty() {
    assert!(crate::greet("").is_err());
}
```
Keep core logic in plain Rust with ordinary `#[test]`s. Test only the glue in wasm tests. Add `wasm-bindgen-test` as a dev-dependency.

## Do
- Set `crate-type = ["cdylib", "rlib"]` in `[lib]` so both wasm and native tests build.
- Export with `#[wasm_bindgen]` on functions, structs and impls. Return `Result<T, JsError>` (or `JsValue`) so failures become JS exceptions.
- Pass complex data with `serde-wasm-bindgen` or `tsify` instead of hand-built `JsValue` objects.
- Enable only the `web-sys` features you call (each type is behind a feature flag).
- Use `wasm-bindgen-futures` (`spawn_local`, `JsFuture`) for async. Export `async fn` directly for promises.
- Install the panic hook in start code (`console_error_panic_hook::set_once()`).
- Keep the `wasm-bindgen` crate version identical to the CLI that processes the output.
- Size-optimise the release profile (`opt-level = "s"`, `lto = true`) and run `wasm-opt`.

## Avoid
- CLI and crate `wasm-bindgen` version mismatch: a schema-version error at glue-generation time. Pin both to the same version.
- `std::time::Instant`, threads, or file and network access on wasm32-unknown-unknown: they panic or are unsupported. Use `web-sys` Performance and `fetch`.
- Missing `web-sys` feature flags: "no such type or method" compile errors. Add the feature named in the docs.
- Holding Rust references across the boundary: pass owned values or exported structs, which JS must `.free()`.
- `getrandom` without the `js` backend config for wasm: a compile error or runtime failure. Enable the wasm backend your getrandom version documents.
- Copying large buffers per call: share a view into `memory` or pass `&[u8]` once.

## Review
- [ ] Public exports return `Result` and never panic on JS input.
- [ ] Only needed `web-sys` features are enabled.
- [ ] Core logic is testable natively, with a minimal wasm test layer.
- [ ] Generated TypeScript types match the intended API.
- [ ] Bundle size was checked after the change.
