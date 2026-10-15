---
name: bevy
title: Bevy
area: rust
tags: [rust, game, bevy, ecs, graphics, systems]
detect: [dep:bevy]
related: [cargo, clippy, serde, rust-unsafe]
---
Bevy game engine: ECS components, systems, plugins and resources, with logic tested through a headless App.

## Verify
- `cargo check --all-targets`: systems and queries type-check (bad system parameters fail here).
- `cargo test`: headless App tests.
- `cargo clippy --all-targets -- -D warnings`: lint (disable `clippy::type_complexity` and `too_many_arguments` for system signatures in `Cargo.toml` if noisy).
- `cargo run --features bevy/dynamic_linking`: fast dev iteration (dev only, never ship it).

## Test first
Build a minimal `App` without a window, run `update()`, and assert on the World.
```rust
use bevy::prelude::*;

#[derive(Component)] struct Health(i32);

fn damage(mut q: Query<&mut Health>) { for mut h in &mut q { h.0 -= 1; } }

#[test]
fn damage_system_reduces_health() {
    let mut app = App::new();
    app.add_systems(Update, damage);
    let e = app.world_mut().spawn(Health(3)).id();
    app.update();
    assert_eq!(app.world().get::<Health>(e).unwrap().0, 2);
}
```
Use `MinimalPlugins`, not `DefaultPlugins`, in tests.

## Do
- Keep systems small and single-purpose. Group them in a `Plugin` per feature.
- Model state with components and resources, and sequencing with schedules, `.chain()`, `.before()`/`.after()` and system sets.
- Use `States` (`in_state`, `OnEnter`, `OnExit`) for menus, loading and gameplay phases.
- Use `Commands` for spawn and despawn, and `Query` filters (`With`, `Without`, `Changed`) to narrow iteration.
- Communicate between systems with events or messages, depending on the pinned version's API.
- Load assets through `AssetServer` and check load state before using them.
- Pin the exact bevy version in `Cargo.toml`, and read its migration guide before bumping.

## Avoid
- Copying tutorials across Bevy versions: APIs rename every release (bundles to required components, `Query::single` return types, event APIs). Check the pinned version's docs.
- Conflicting query access in one system (`&mut T` twice): a runtime panic. Use `Without`, or `ParamSet`.
- Doing heavy work in `Update` every frame: use change detection, timers or a task pool (`AsyncComputeTaskPool`).
- Unordered systems that depend on each other's results: nondeterministic bugs. Add ordering.
- `DefaultPlugins` in unit tests: it needs a window and GPU. Use `MinimalPlugins`.
- Shipping `dynamic_linking`: the binary needs the shared library. Remove the feature for release.
- Unwrapping `Query::single()`: it errors with zero or many entities. Handle the result.

## Review
- [ ] Systems have narrow queries and explicit ordering where they depend on each other.
- [ ] Gameplay logic has headless tests.
- [ ] Dev-only features are not on in release builds.
- [ ] Assets are loaded asynchronously and their load state is handled.
- [ ] The Bevy version is pinned and APIs match its docs.
