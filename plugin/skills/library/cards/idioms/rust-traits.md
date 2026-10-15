---
name: rust-traits
title: Rust traits and generics
area: idioms
tags: [rust, traits, generics, dyn, impl-trait, dispatch]
detect: []
related: [rust, rust-lifetimes, clippy]
---
Rust traits and generics: static dispatch by default, `dyn` at plugin boundaries, small traits with std implementations.

## Verify
- `cargo check --all-targets`: trait bounds and coherence errors.
- `cargo clippy --all-targets -- -D warnings`: flags needless bounds, missing `Default` and derivable impls.
- `cargo test`: behavior, including doc tests that show trait usage.
- `cargo doc --no-deps`: public trait docs build and doc links resolve.

## Test first
Test the trait through a generic function with two implementations.
```rust
trait Clock { fn now(&self) -> u64; }
struct Fixed(u64);
impl Clock for Fixed { fn now(&self) -> u64 { self.0 } }

#[test]
fn expires_uses_injected_clock() {
    assert!(is_expired(&Fixed(100), 50));
    assert!(!is_expired(&Fixed(10), 50));
}
```
Write `is_expired<C: Clock>(c: &C, deadline: u64)` to make it pass. A hand-written fake beats a mocking crate for small traits.

## Do
- Accept generics (`fn f(x: impl AsRef<str>)`) or `&dyn Trait`, and return `impl Trait` when callers need only the behavior.
- Use `dyn Trait` when you need a heterogeneous collection or want to cut compile time and code size.
- Put bounds in a `where` clause when there are more than one or two.
- Implement std traits: `From`, `Display`, `Default`, `FromStr`, `Iterator`, `IntoIterator`. Derive `Debug`, `Clone`, `PartialEq` where sound.
- Use associated types when each implementor has exactly one such type (`Iterator::Item`), and generics when it may implement for many.
- Use a sealed trait (private supertrait) to keep a public trait closed to outside implementations.
- Implement `From<E>` for your error type so `?` converts automatically.

## Avoid
- `Box<dyn Trait>` everywhere out of habit: it costs an allocation and dynamic dispatch. Use generics unless you need runtime polymorphism.
- A trait with one implementor and no test double: a plain struct is enough.
- Returning `impl Trait` from a trait method on old toolchains: it needs a recent compiler. Check the repo's rust version, or return a boxed trait object.
- A trait that is not object safe used as `dyn`: generic methods and `Self` returns break it. Add `where Self: Sized` to those methods.
- Blanket impls like `impl<T> MyTrait for T`: they block every future impl by coherence rules. Bound them narrowly.
- `Clone` bounds added to dodge a borrow error: take a reference instead.

## Review
- [ ] Dispatch choice (generic or `dyn`) is deliberate.
- [ ] Traits are small and each method earns its place.
- [ ] Standard conversion traits are used instead of ad hoc `to_x` methods.
- [ ] Public traits have docs and a doc-test example.
- [ ] Object-safe traits are tested through `dyn` at least once if they are used that way.
