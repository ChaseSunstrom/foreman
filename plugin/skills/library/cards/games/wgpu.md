---
name: wgpu
title: wgpu and WGSL
area: games
tags: [wgpu, wgsl, rust, graphics, gpu, webgpu]
detect: [dep:wgpu, dep:naga, ext:.wgsl]
related: [rust, vulkan, glsl, cargo]
---
wgpu in Rust: portable GPU access over Vulkan, Metal, D3D12 and WebGPU, with WGSL shaders validated by naga.

## Verify
- `cargo clippy --all-targets -- -D warnings`: lints, including misuse of descriptors.
- `cargo test`: tests pass (headless, using a fallback adapter where needed).
- `naga shader.wgsl`: the WGSL parses and validates (naga-cli).
- `cargo check --target wasm32-unknown-unknown`: the WebGPU build target still compiles.

## Test first
Create a device without a surface, render or compute to a texture or buffer, map it, and assert on bytes.
```rust
#[test]
fn compute_doubles_values() {
    let (device, queue) = pollster::block_on(test_device()); // force_fallback_adapter in CI
    let out = run_double_shader(&device, &queue, &[1.0f32, 2.0, 3.0]);
    assert_eq!(out, vec![2.0, 4.0, 6.0]);
}
```
Write `test_device()` once with `RequestAdapterOptions { force_fallback_adapter: true, .. }` so CI works without a GPU.

## Do
- Validate every WGSL file with naga in tests (`naga::front::wgsl::parse_str` plus the validator) so errors surface without a device.
- Bring up Instance, Adapter, Device, Queue once; request only needed `Features` and `Limits`.
- Configure the surface from `surface.get_capabilities(&adapter)` and reconfigure on resize.
- Match WGSL and Rust struct layouts: use `bytemuck::Pod` with `#[repr(C)]` and respect alignment (vec3 pads to 16 bytes in uniform blocks).
- Install an error handler or push and pop error scopes; do not rely on panics from the default handler alone.
- Reuse bind group layouts and pipelines; create them at load time, not per frame.
- Get frames with `surface.get_current_texture()` and handle `Lost`, `Outdated` and `Timeout` by reconfiguring.
- Map buffers with `map_async` then `device.poll(...)` before reading.

## Avoid
- Copying examples from an older wgpu release verbatim: descriptor fields and function signatures change between versions. Read the version in `Cargo.lock` and its docs.
- Blocking the browser main thread on native-style `pollster::block_on` for wasm: use async with `wasm-bindgen-futures`.
- Writing a uniform buffer every frame by creating a new buffer: use `queue.write_buffer`.
- Unaligned buffer copy sizes or `bytes_per_row` not a multiple of 256 for texture to buffer copies: validation error. Pad rows.
- Ignoring surface texture lifetime: present by dropping `SurfaceTexture` after `present()`.
- Missing `device.poll` in tests: mapped data never arrives.
- Using `unwrap` on adapter requests: no GPU yields `None`. Handle it and fall back.

## Review
- [ ] Shaders pass naga validation in a unit test.
- [ ] Struct layouts match between Rust (`bytemuck`) and WGSL.
- [ ] Surface errors are handled by reconfigure, not panic.
- [ ] Pipelines and bind groups are not rebuilt per frame.
- [ ] The wasm32 build still compiles when the project targets the web.
