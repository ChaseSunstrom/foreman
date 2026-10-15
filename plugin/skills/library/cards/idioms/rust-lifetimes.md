---
name: rust-lifetimes
title: Rust lifetimes and borrowing
area: idioms
tags: [rust, lifetimes, borrowing, ownership, references, clippy]
detect: []
related: [rust, rust-traits, clippy]
---
Rust ownership and lifetimes: let elision and owned data do the work, annotate only when a signature ties inputs to outputs.

## Verify
- `cargo check --all-targets`: borrow and lifetime errors surface here fast.
- `cargo clippy --all-targets -- -D warnings`: catches needless clones, needless lifetimes and borrow smells.
- `cargo test`: behavior holds.
- `cargo miri test`: undefined behavior in `unsafe` code, when the nightly toolchain with miri is installed.

## Test first
A test that fails to compile is a valid red. Express the intended borrow in a test.
```rust
#[test]
fn longest_borrows_from_inputs() {
    let a = String::from("hello");
    let out;
    {
        let b = String::from("hi");
        out = longest(&a, &b).len();
    }
    assert_eq!(out, 5);
}
```
For compile-fail guarantees use the `trybuild` crate, or a `compile_fail` doc test.

## Do
- Rely on elision first: one input reference gives the output its lifetime, and `&self` methods give outputs the lifetime of `self`.
- Add `'a` only when a function returns a reference tied to specific inputs: `fn pick<'a>(x: &'a str, y: &str) -> &'a str`.
- Take `&str` and `&[T]` in parameters, not `&String` or `&Vec<T>`.
- Return owned data (`String`, `Vec`) when a lifetime would infect the whole call chain.
- Use `Cow<'a, str>` when a function sometimes allocates and sometimes borrows.
- Structs that hold references need a lifetime parameter. Prefer owning fields unless profiling says otherwise.
- Use `'static` bounds only for data that truly lives forever, or when spawning threads, where owned or `Arc` data is the usual answer.
- Narrow a borrow with a block or a small function so a later mutable use compiles.

## Avoid
- Fighting the borrow checker with `.clone()` everywhere: it hides the design problem. Restructure ownership or pass references.
- `&'static str` fields to silence an error: it forces leaks or literals. Use `String` or a lifetime parameter.
- Self-referential structs: they cannot be expressed safely. Store indices, use `Rc` or `Arc`, or split the struct.
- `Box::leak` to get `'static`: it leaks memory. Use `Arc` or scoped threads (`std::thread::scope`).
- Returning a reference to a local: it dangles. Return the owned value.
- Holding a `RefCell` borrow across a call that borrows again: it panics at runtime. Scope the borrow tightly.

## Review
- [ ] Explicit lifetimes appear only where elision cannot express the relationship.
- [ ] Parameters accept the most general borrowed type (`&str`, `&[T]`, `impl AsRef<Path>`).
- [ ] No gratuitous `.clone()` added only to pass the borrow checker.
- [ ] Every `unsafe` block has a comment stating the invariant it relies on.
- [ ] Public APIs avoid leaking lifetime parameters when an owned type would do.
