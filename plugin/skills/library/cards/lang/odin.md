---
name: odin
title: Odin
area: lang
tags: [odin, systems, manual-memory, allocators, data-oriented, gamedev]
detect: [ext:.odin, file:ols.json]
related: [c, zig]
---
Odin: explicit allocators, `defer` for cleanup, tagged unions and data-oriented structs, tested with the built-in test runner.

## Verify
- `odin check .`: type checks the package without producing a binary.
- `odin build . -vet -strict-style`: builds with extra checks for unused variables and imports plus style rules.
- `odin test .`: runs procedures marked `@(test)` in the package.
- `odin test . -sanitize:address`: tests under the address sanitizer, where the toolchain supports it.

## Test first
A procedure with the `@(test)` attribute and the `testing` package.
```odin
package clamp_test

import "core:testing"

clamp_int :: proc(x, lo, hi: int) -> int {
	return min(hi, max(lo, x))
}

@(test)
test_clamp :: proc(t: ^testing.T) {
	testing.expect_value(t, clamp_int(5, 0, 3), 3)
	testing.expect_value(t, clamp_int(-1, 0, 3), 0)
}
```
The test runner also reports leaked tracked allocations from `context.allocator` in tests.

## Do
- Pass an `allocator` parameter (default `context.allocator`) to procedures that allocate, and use `context.temp_allocator` with `free_all` for per-frame data.
- Pair every allocation with `defer delete(...)` or `defer free(...)` on the next line.
- Use tagged `union` for variants and `switch v in value` for exhaustive handling.
- Return multiple values and an `ok` boolean or an error enum, and check them with `or_return` and `or_else`.
- Use `#soa` arrays and plain structs for data-oriented layouts.
- Use `distinct` types for ids and units to avoid mix-ups.
- Use `when ODIN_DEBUG` and `#assert` for debug and compile-time checks.
- Use `core:mem` tracking allocator in tests and debug builds to find leaks and bad frees.

## Avoid
- Forgetting `defer delete`: leaks. Add it directly after the `make` or `new` call.
- Deleting with a different allocator than the one that allocated: corrupt frees. Keep the allocator with the owning data.
- Holding pointers into a dynamic array across appends: it may move. Use indices or handles.
- Keeping `context.temp_allocator` data past `free_all`: dangling. Copy it to a long-lived allocator first.
- Ignoring returned errors and `ok` values: failures are silent. Use `or_return` or handle them.
- Assuming slices own memory: they are views. Free the backing array, not the slice.
- Large by-value structs passed everywhere: copying costs. Pass pointers or slices.

## Review
- [ ] Every allocation has a matching `defer` free on the same allocator.
- [ ] Procedures that allocate accept an allocator.
- [ ] Error returns are checked.
- [ ] No pointers or slices outlive the data they view.
- [ ] `odin test` and `odin build -vet` pass.
