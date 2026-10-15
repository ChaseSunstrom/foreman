---
name: leptos
title: Leptos
area: rust
tags: [rust, web, leptos, wasm, ssr, signals]
detect: [dep:leptos, dep:leptos_axum, dep:leptos_router, file:Leptos.toml]
related: [axum, wasm-bindgen, tokio, serde]
---
Leptos full-stack Rust UI: fine-grained signals, components, server functions, SSR and hydration.

## Verify
- `cargo leptos build`: server and wasm bundles both build (needs cargo-leptos).
- `cargo leptos test`: unit and end-to-end tests as configured.
- `cargo clippy --all-targets --features ssr -- -D warnings` and again with `--features hydrate`: both feature sets compile clean.
- `cargo test`: pure logic and server fns.
- `cargo leptos watch`: no hydration warnings in the browser console on first load.

## Test first
Test logic outside the view; test server functions directly.
```rust
#[test]
fn total_sums_items() {
    let items = vec![Item { price: 2 }, Item { price: 3 }];
    assert_eq!(total(&items), 5);
}
```
For UI, use wasm-bindgen-test or Playwright through cargo-leptos `end2end` config.

## Do
- Separate features: `ssr` for server deps (axum, tokio, DB), `hydrate` for the wasm client. Gate server-only code with `#[cfg(feature = "ssr")]`.
- Components are fns marked `#[component]` returning `impl IntoView`; state lives in signals (`signal(0)` or `RwSignal`).
- Read signals inside the view closure (`move || count.get()`) so updates are fine-grained.
- Use `#[server]` functions for DB and secrets; they return `Result<T, ServerFnError>` and run only on the server.
- Load async data with `Resource`/`Suspense` (or `Transition`) and handle errors with `ErrorBoundary`.
- Use `Callback`/`StoredValue` for non-reactive shared state.
- Keep SSR and client render output identical for first paint.

## Avoid
- Reading a signal outside a reactive scope and expecting updates: it's a one-time read. Wrap in a closure.
- Browser-only APIs (`window()`, `localStorage`) during SSR: panics. Use `Effect::new` or `cfg` guards.
- Differing server and client markup (random values, `Date::now`): hydration mismatch. Seed on the server and pass down.
- Server-only crates compiled for wasm: build errors. Keep them behind `ssr`.
- Secrets or DB handles in code that can reach the client: put them in `#[server]` fns.
- Following older API names from tutorials (`create_signal`, `create_effect`): verify the names against your version's docs.
- Unwrapping in server fns: propagate `ServerFnError`.

## Review
- [ ] `ssr` and `hydrate` builds both pass.
- [ ] No server-only code is reachable from client features.
- [ ] Reactive reads sit inside closures; effects don't loop on their own writes.
- [ ] Resources have loading and error states.
- [ ] No hydration mismatch warnings.
