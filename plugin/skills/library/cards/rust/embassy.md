---
name: embassy
title: Embassy (embedded async)
area: rust
tags: [rust, embedded, embassy, async, no-std, microcontroller]
detect: [dep:embassy-executor, dep:embassy-time, dep:embassy-sync, dep:embassy-futures]
related: [rust-unsafe, cargo, clippy, tokio]
---
Embassy async firmware: executor and tasks, timers, channels, HAL peripherals, probe-rs flashing and host-side tests.

## Verify
- `cargo build --release --target thumbv7em-none-eabihf`: firmware builds for your target (use the target in `.cargo/config.toml`).
- `cargo clippy --target thumbv7em-none-eabihf -- -D warnings`: lints for the real target.
- `cargo run --release`: with a `probe-rs` runner configured, flashes and streams `defmt` logs.
- `cargo test --lib` on the host: logic factored into a `no_std`-compatible crate runs on the dev machine.
- `cargo size --release`: flash and RAM stay inside the chip's budget (needs cargo-binutils).

## Test first
Keep pure logic (state machines, parsers, protocol framing) in a lib that compiles on host, and test it there.
```rust
#[test]
fn debounce_ignores_glitch() {
    let mut d = Debounce::new(3);
    assert!(!d.update(true));
    assert!(!d.update(false));
    assert!(!d.update(true));
    assert!(d.update(true) == false);
}
```
Hardware behavior is verified on a board with `defmt-test` or manual probe runs; say so in the task evidence.

## Do
- Spawn tasks with `#[embassy_executor::task]` and `spawner.spawn(...)`; each task fn is statically allocated, so pool size is part of its signature.
- Await `Timer::after_millis(..)` / `Ticker`, never busy-wait.
- Share data between tasks with `embassy_sync::channel::Channel`, `Signal` or `Mutex` using a raw mutex type matching your context (`CriticalSectionRawMutex` for interrupts, `NoopRawMutex` single executor).
- Put statics in `StaticCell`/`static_cell::make_static!` rather than `static mut`.
- Log with `defmt`; set `DEFMT_LOG` level and use `defmt::unwrap!` instead of `unwrap`.
- Set a panic handler (`panic-probe`) and a watchdog for production.
- Pin the chip feature of the HAL crate and the time driver feature (`embassy-time` tick rate must match).

## Avoid
- Blocking calls (long loops, `cortex_m::asm::delay` for ms) inside a task: starves other tasks. Await a timer.
- Holding a `Mutex` guard across an `.await` with a blocking raw mutex: deadlock or priority issues. Scope it tightly.
- `static mut` for shared state: UB risk. Use `StaticCell` or sync primitives.
- Mismatched executor and interrupt priorities, using `InterruptExecutor` for high-priority work without matching NVIC setup.
- Enabling `std` or `alloc` crates by accident: link errors. Check `default-features = false`.
- Copying examples from a different chip family: pins and clocks differ. Check the HAL's own examples.
- Unbounded stack in tasks: size via `memory.x` and keep large buffers static.

## Review
- [ ] Builds for the real target with clippy clean.
- [ ] No blocking waits in tasks; timers are awaited.
- [ ] Raw mutex types match where data is touched (interrupt vs thread).
- [ ] Logic is host-tested; hardware checks are listed in evidence.
- [ ] Panic and watchdog behavior are decided.
