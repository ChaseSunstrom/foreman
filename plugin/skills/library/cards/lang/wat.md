---
name: wat
title: WebAssembly text format
area: lang
tags: [wasm, webassembly, wat, wabt, low-level, stack-machine]
detect: [ext:.wat, ext:.wast, ext:.wasm]
related: [rust, c]
---
WebAssembly text format (WAT): a typed stack machine, bounds-checked linear memory and tests that call exports from a host.

## Verify
- `wat2wasm module.wat -o module.wasm`: assembles the text, which validates types and structure.
- `wasm-validate module.wasm`: validates a binary against the spec.
- `wasm-objdump -d module.wasm`: disassembles the output to confirm the instructions.
- `wasm-interp module.wasm --run-all-exports`: runs exported functions in the interpreter, when the tool is installed.

## Test first
Load the module from a host test and assert on the exports.
```js
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const { instance } = await WebAssembly.instantiate(readFileSync("add.wasm"));
const { add } = instance.exports;
assert.equal(add(2, 3), 5);
assert.equal(add(2147483647, 1), -2147483648); // i32 wraps
```
Implement `(func (export "add") (param i32 i32) (result i32) ...)` in `add.wat` to make it pass.

## Do
- Write the module in folded form: `(i32.add (local.get $a) (local.get $b))`.
- Name locals, globals, functions and types with `$names`, and keep a comment for each export's signature.
- Declare memory with `(memory (export "mem") 1)` and use explicit offsets and alignment hints on loads and stores.
- Remember every value is `i32`, `i64`, `f32` or `f64` (plus reference and vector types), so convert with `i32.wrap_i64`, `i64.extend_i32_s` and similar.
- Use `block`, `loop` and `br_if` for control flow, where `br` to a loop label continues and to a block label exits.
- Check bounds yourself for host-supplied pointers, since out-of-range access traps.
- Use `i32.add` style wrapping arithmetic deliberately, and the `_s` or `_u` suffix for signedness.
- Define a small test host per module that instantiates and calls exports with edge values.

## Avoid
- Assuming signed integers: i32 is sign-agnostic, so division, shifts and comparisons need `_s` or `_u`. Pick one per operation.
- Forgetting that a branch to a `loop` label restarts it: infinite loops. Use `br_if` with a counter.
- Leaving values on the stack at function end: validation fails. Match the result type exactly.
- Writing past the memory size: it traps. Grow with `memory.grow` and check the result for -1.
- Passing strings across the boundary as host objects: Wasm sees only numbers. Pass pointer and length into linear memory.
- Using `unreachable` as error handling: it traps the whole instance. Return an error code instead.
- Hand-writing large programs: use a compiler from Rust or C for volume, and keep WAT for small kernels and inspection.

## Review
- [ ] The module validates with `wasm-validate`.
- [ ] Every export has a host test with edge values.
- [ ] Signedness is explicit on each integer operation.
- [ ] Memory accesses are bounds-safe and memory growth is checked.
- [ ] No leftover stack values or accidental traps.
