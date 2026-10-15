---
name: dioxus
title: Dioxus
area: rust
tags: [rust, ui, dioxus, wasm, desktop, signals]
detect: [dep:dioxus, dep:dioxus-web, dep:dioxus-desktop, file:Dioxus.toml]
related: [leptos, wasm-bindgen, tokio, serde]
---
Dioxus cross-platform UI: rsx components, signals, hooks, router and fullstack server functions.

## Verify
- `dx build`: the app builds for the configured platform (needs the dioxus CLI).
- `dx serve`: dev server runs with hot reload and no console panics.
- `cargo clippy --all-targets -- -D warnings`: lints; also run with each platform feature you ship.
- `cargo test`: non-UI logic and state reducers.
- `dx check`: rsx lint for common mistakes (when your CLI version provides it).

## Test first
Keep state transitions in plain functions and test those.
```rust
#[test]
fn toggle_flips_done() {
    let mut t = Todo { done: false };
    t.toggle();
    assert!(t.done);
}
```
For rendering, `VirtualDom::new(App)` plus `rebuild_in_place()` and `dioxus_ssr::render(&dom)` can assert on HTML output.

## Do
- Write components as fns with `#[component]` returning `Element`; props are owned, `PartialEq + Clone` types.
- Hold state with `use_signal(|| init)`; read with `signal()` or `.read()`, write with `.set(..)` or `.write()`.
- Derive values with `use_memo`, run effects with `use_effect`, async work with `use_resource`.
- Provide shared state with `use_context_provider` and read with `use_context`.
- Give list items a stable `key` in `for` loops inside rsx.
- Use `dioxus-router` `Routable` enums for typed routes.
- Put server-only code in `#[server]` functions (fullstack) behind the `server` feature; keep the `web`/`desktop` feature client-only.

## Avoid
- Hooks called conditionally or in loops: order must be stable across renders. Call them at the top of the component.
- Holding a `.read()`/`.write()` borrow across `.await`: runtime borrow panics. Clone the value out first.
- Mutating a signal inside the render body: infinite re-render. Do it in handlers or effects.
- Missing list `key`s: wrong DOM reuse and stale state.
- Blocking work in event handlers: freezes the UI. Use `spawn` or `use_resource`.
- Old 0.4/0.5 API names (`cx: Scope`, `use_state`, `use_ref`): replaced by signals; check your installed version.
- Platform crates enabled together by accident (web and desktop): build failures. Select via features.

## Review
- [ ] Hooks are unconditional and top-level.
- [ ] No signal borrow held across an await.
- [ ] Lists have stable keys.
- [ ] Platform features are selected explicitly and each shipped target builds.
- [ ] Logic is tested outside the view layer.
