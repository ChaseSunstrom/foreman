---
name: webassembly
title: WebAssembly
area: native
tags: [webassembly, wasm, emscripten, wasi, wasm-bindgen, browser]
detect: [ext:.wasm, ext:.wat, dep:wasm-bindgen, dep:wasm-pack, file:wasm-pack.toml, file:Emscripten.cmake]
related: [cmake, rust-cargo, sanitizers]
---
WebAssembly modules from C/C++ (Emscripten) or Rust (wasm-bindgen), run in browsers, Node or WASI runtimes.

## Verify
- `emcmake cmake -S . -B build-wasm && cmake --build build-wasm`: C/C++ builds through Emscripten's toolchain file.
- `wasm-pack build --target web` (Rust): the package builds with JS glue in `pkg/`.
- `wasm-tools validate out.wasm`: the binary is valid (when wasm-tools is installed).
- `wasm-pack test --node`: Rust wasm tests run under Node (use `--headless --firefox` for browser tests).

## Test first
Test logic natively first (it is plain C/C++/Rust), then test the boundary in a JS or wasm test runner. A failing boundary test:
```rust
use wasm_bindgen_test::*;
wasm_bindgen_test_configure!(run_in_node);

#[wasm_bindgen_test]
fn parse_rejects_empty() {
    assert!(my_crate::parse("").is_err());
}
```
For Emscripten, build with `-sEXPORTED_FUNCTIONS` and call the export from a Node script that asserts on the result.

## Do
- Keep the boundary small: pass numbers, pointers plus lengths, or typed arrays; avoid chatty calls across the JS/wasm edge.
- Export explicitly: `EMSCRIPTEN_KEEPALIVE` or `-sEXPORTED_FUNCTIONS=_name` with `-sEXPORTED_RUNTIME_METHODS=ccall,cwrap`; `#[wasm_bindgen]` for Rust.
- Build release with optimisation (`-O2`/`-Oz`, `wasm-opt -O`, Rust `opt-level = "s"` or `"z"`, `lto = true`) and measure the `.wasm` size.
- Serve with `Content-Type: application/wasm` and load with `WebAssembly.instantiateStreaming` (or the generated loader).
- Free what you allocate across the boundary (`free`, wasm-bindgen `.free()`).
- Use WASI targets (`wasm32-wasip1`, or `wasm32-wasi` on older toolchains) for server-side, with explicit capability grants (`--dir`).
- Run heavy work in a Web Worker so the main thread stays responsive.

## Avoid
- Assuming threads, sockets or a filesystem exist: browsers need `-pthread`, SharedArrayBuffer and cross-origin isolation headers (COOP/COEP) for threads; WASI needs preopened dirs.
- Copying large strings and arrays per call: share memory views (`HEAPU8`, `Uint8Array` on `memory.buffer`).
- Holding a typed-array view across a call that may grow memory: the buffer is detached. Re-create the view.
- Mixing `usize`/`size_t` expectations: wasm32 pointers are 32-bit, so sizes over 4 GiB fail.
- Shipping debug builds or unstripped names: large and slow. Use release profile and strip.
- Using `eval`/`Function`-style loaders or disabling CSP to make the module load: allow `wasm-unsafe-eval` narrowly if required.
- Trusting input from JS inside wasm: validate lengths and ranges at the boundary; memory safety inside the module does not stop logic bugs.

## Review
- [ ] The core logic has native tests plus at least one boundary test.
- [ ] Exports are explicit and minimal; ownership across the boundary is documented.
- [ ] Release build is optimised; size is measured and bounded.
- [ ] Server sends the correct MIME type and isolation headers if threads are used.
- [ ] Inputs from JS are validated.
