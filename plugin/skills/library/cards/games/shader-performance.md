---
name: shader-performance
title: Shader performance
area: games
tags: [shader, gpu, performance, overdraw, branching, bandwidth]
detect: [ext:.wgsl, ext:.hlsl, ext:.frag, ext:.vert, ext:.shader, ext:.glsl]
related: [glsl, opengl, vulkan, wgpu]
---
GPU shader cost: reduce per-fragment math, texture bandwidth, overdraw and divergent branches; measure on target hardware before and after.

## Verify
- `glslangValidator -V shader.frag -o /dev/null`: the GLSL compiles to SPIR-V with no errors.
- `spirv-val shader.spv`: the SPIR-V module is valid.
- `naga shader.wgsl`: the WGSL module parses and validates (when naga-cli is installed).
- `grep -rnE "discard|for *\(|while *\(" shaders`: lists loops and discards to check against the review points.

## Test first
Shaders rarely have unit tests. Set a measurable budget and a reference-image check first.
```python
def test_frame_time_budget():
    t = render_benchmark(scene="heavy", frames=300, resolution=(1920, 1080))
    assert t.p95_ms < 8.0

def test_output_matches_reference():
    img = render_frame(scene="lit_sphere", seed=1)
    assert mean_abs_diff(img, load("ref/lit_sphere.png")) < 2.0
```

## Do
- Profile first with the GPU vendor or engine tool (frame debugger, GPU capture) and find the bound: ALU, texture fetch, bandwidth or overdraw.
- Move work up the pipeline: compute per-vertex or per-draw on the CPU what does not vary per pixel. Precompute into textures or LUTs.
- Use the lowest precision that looks right (`mediump` or half) on mobile, and keep `highp` for positions and depth.
- Use mipmapped, compressed textures, and pack channels (roughness, metallic, AO into one texture).
- Replace `pow`, `sin`, `normalize` chains with cheaper forms (multiplication, `rsqrt`, polynomial approximations) where the error is invisible.
- Sort opaque draws front to back for early-z, and draw transparency last with as few layers as possible.
- Cut overdraw with tight quads and alpha-tested cutouts instead of large transparent sprites.
- Use specialization constants or `#define` variants instead of runtime flags.

## Avoid
- Per-pixel branches on varying data: divergent lanes execute both paths. Use `mix`, `step` or `select`, or branch on uniforms.
- Dependent texture reads (UV computed from another sample) in hot paths: they stall latency hiding. Precompute UVs in the vertex stage.
- Large loops with dynamic bounds in fragment shaders: unrolling fails and the cost is hidden. Fix the bound or move to compute.
- `discard` in an opaque pass: it disables early-z. Use alpha-to-coverage or a separate cutout pass.
- Optimising by feel on a desktop GPU: mobile and integrated GPUs differ greatly. Measure on the weakest target.
- Full-resolution post effects each frame: render at half resolution or merge passes.

## Review
- [ ] A recorded before and after GPU timing exists on the weakest target device.
- [ ] No per-pixel dynamic branches or loops with unknown bounds.
- [ ] Texture count, size and format are justified, with mipmaps enabled.
- [ ] Overdraw and transparency layers are checked in a frame capture.
- [ ] Shader variants are bounded and compile at load, not at first draw.
