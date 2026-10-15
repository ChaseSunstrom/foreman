---
name: rust-unsafe
title: Rust unsafe code
area: rust
tags: [rust, unsafe, ffi, miri, soundness, safety]
detect: [dep:libc, dep:bindgen, dep:cbindgen, file:build.rs]
related: [clippy, cargo, wasm-bindgen, tokio]
---
Writing unsafe Rust: smallest possible blocks, documented invariants, a safe wrapper, and Miri to check.

## Verify
- `cargo +nightly miri test`: runs tests under Miri to catch UB (out-of-bounds, aliasing, uninitialised reads). Needs the nightly toolchain with the miri component.
- `cargo clippy --all-targets -- -D warnings -W clippy::undocumented_unsafe_blocks`: every unsafe block needs a SAFETY comment.
- `grep -rn "unsafe" src | wc -l`: the unsafe surface is small and tracked.
- `cargo test --release`: UB sometimes only shows with optimisations.

## Test first
Test the safe wrapper with the inputs that would break the invariant.
```rust
pub struct Buf { ptr: *mut u8, len: usize }

impl Buf {
    pub fn get(&self, i: usize) -> Option<u8> {
        if i < self.len {
            // SAFETY: ptr is valid for len bytes (see `new`) and i < len.
            Some(unsafe { *self.ptr.add(i) })
        } else { None }
    }
}

#[test]
fn out_of_range_is_none() {
    let b = Buf::new(4);
    assert_eq!(b.get(4), None);
}
```
Run it under Miri as the real check.

## Do
- Keep each `unsafe` block to one operation, and put a `// SAFETY:` comment stating why the preconditions hold.
- Document the caller's obligations in a `# Safety` section on every `unsafe fn`.
- Hide unsafe behind a safe API whose type invariants make misuse impossible (private fields, newtypes, lifetimes).
- Use `#![forbid(unsafe_code)]` in crates that don't need it, and `#![deny(unsafe_op_in_unsafe_fn)]` in ones that do.
- Prefer `MaybeUninit`, `NonNull`, `slice::from_raw_parts` with checked lengths, and `std::ptr::addr_of!` over raw casts.
- For FFI: `#[repr(C)]`, check for null, never unwind across the boundary (`extern "C"` with catch_unwind), and free memory with the allocator that made it.
- Implement `Send`/`Sync` manually only with a written argument.

## Avoid
- `mem::uninitialized` and `mem::zeroed` for types with invalid zero patterns: instant UB. Use `MaybeUninit`.
- Creating `&mut` aliases to the same data via raw pointers: aliasing UB even if it works. Keep one live mutable path.
- Transmuting between types of unequal layout or with `#[repr(Rust)]` assumptions: use `#[repr(C)]` or `from_ne_bytes`.
- `unsafe` to dodge the borrow checker: restructure, or use `RefCell`, indices or split borrows.
- Dereferencing pointers from C without a null and alignment check.
- Treating "tests pass" as proof: UB passes tests. Run Miri and sanitizers.
- `static mut`: use atomics, `OnceLock` or a `Mutex`.

## Review
- [ ] Every unsafe block has a SAFETY comment that names the invariant and who upholds it.
- [ ] The public API is safe to call in any order with any input.
- [ ] Miri passes on the tests covering the unsafe code.
- [ ] FFI boundaries check nulls, ownership and panics.
- [ ] Unsafe is not used where a safe alternative has the same cost.
