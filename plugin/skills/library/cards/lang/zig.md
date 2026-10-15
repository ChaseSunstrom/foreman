---
name: zig
title: Zig
area: lang
tags: [zig, systems, allocators, comptime, build-zig, testing]
detect: [ext:.zig, file:build.zig, file:build.zig.zon]
related: [bash]
---
Zig code: explicit allocators, error unions, comptime, `build.zig`, built-in `test` blocks.

## Verify
- `zig fmt --check .`: formatting is canonical.
- `zig build`: compiles per `build.zig` (default Debug mode keeps safety checks).
- `zig build test`: runs the `test` step wired in `build.zig`.
- `zig test src/foo.zig`: runs one file's test blocks quickly, when the file has no module imports.
- `zig build -Doptimize=ReleaseSafe test`: tests also pass with optimizations while safety checks stay on.

## Test first
Tests are `test "name" { ... }` blocks inside the source file; use `std.testing`.
```zig
const std = @import("std");
const parse = @import("parse.zig");

test "parseInt rejects empty input" {
    try std.testing.expectError(error.Empty, parse.parseInt(""));
}

test "join frees what it allocates" {
    const s = try parse.join(std.testing.allocator, &.{ "a", "b" });
    defer std.testing.allocator.free(s);
    try std.testing.expectEqualStrings("a,b", s);
}
```
`std.testing.allocator` fails the test on leaks and double frees.

## Do
- Take an `std.mem.Allocator` parameter in any function that allocates; the caller owns the lifetime and the docs say who frees.
- Pair every allocation with `defer` (or `errdefer` on error paths) on the next line.
- Return error unions (`!T`) with named error sets and propagate with `try`; handle with `catch |err| switch (err)`.
- Use arena allocators (`std.heap.ArenaAllocator`) for request or batch lifetimes, and a debug or leak-checking allocator in `main` for development.
- Use slices and sentinel-terminated pointers deliberately; prefer `[]const u8` for strings.
- Keep comptime for types and tables; avoid it where a plain runtime function is clearer.
- Pin the Zig version in the repo (README or CI) and check `std` docs for that version.

## Avoid
- `catch unreachable` or `.?` on fallible or optional values from outside input: safety panic in Debug, undefined behavior in ReleaseFast. Handle the error.
- Returning a slice of a stack buffer or a freed allocation: dangling pointer. Allocate, or take a caller buffer.
- Copying a struct that owns an `ArrayList` or allocator-backed field by value and using both: double free. Move ownership explicitly.
- Using `std` APIs from memory: they change between releases (allocator, `ArrayList`, I/O interfaces, build API). Check the compiler's docs and error messages.
- Ignoring errors with `_ = try ...` patterns that discard results meant to be checked.
- Testing only in ReleaseFast: integer overflow and bounds bugs stay silent.

## Review
- [ ] Each allocation has a matching `defer`/`errdefer` free, and tests use `std.testing.allocator`.
- [ ] No `unreachable`, `.?` or `@intCast` on unvalidated input.
- [ ] Public functions document ownership of returned memory.
- [ ] `zig fmt --check` and `zig build test` pass in Debug and ReleaseSafe.
- [ ] `build.zig.zon` dependencies carry a hash and a pinned source.
