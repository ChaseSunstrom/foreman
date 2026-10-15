---
name: glsl
title: GLSL
area: games
tags: [glsl, shader, graphics, gpu, spirv, opengl]
detect: [ext:.glsl, ext:.vert, ext:.frag, ext:.comp, ext:.geom, ext:.tesc, ext:.tese]
related: [opengl, vulkan, wgpu]
---
GLSL shaders for OpenGL and Vulkan: stage entry points, layouts, precision and validation with glslang.

## Verify
- `glslangValidator shader.frag`: the shader compiles for its stage (stage from the extension).
- `glslangValidator -V shader.frag -o shader.frag.spv`: it compiles to Vulkan SPIR-V (or `glslc shader.frag -o shader.frag.spv`).
- `spirv-val shader.frag.spv`: the SPIR-V is valid.
- `glslangValidator -G shader.frag -o shader.gl.spv`: the OpenGL SPIR-V target compiles, when you use `GL_ARB_gl_spirv`.

## Test first
A shader test is a compile gate plus a rendered pixel check. Start with the compile failing on the missing symbol or version.
```bash
# fails until the shader exists and compiles for every stage
for f in shaders/*.vert shaders/*.frag shaders/*.comp; do
  glslangValidator "$f" || exit 1
done
```
Then render one offscreen frame with known inputs and compare a few pixels (or an image with tolerance) in the host project's test suite.

## Do
- Begin every file with `#version` on the first line (for example `#version 450` for Vulkan, `#version 330 core` for GL 3.3).
- Declare `layout(location = N)` on every in and out; use `layout(set = S, binding = B)` for Vulkan descriptors.
- Pack uniform blocks for `std140` (vec3 aligns to 16 bytes) or `std430` for storage blocks; mirror the layout in host structs.
- Give fragment shaders explicit precision on GLES (`precision mediump float;`).
- Use `#include` only through a loader or `GL_GOOGLE_include_directive`, and pass include paths to the compiler.
- Keep compute `local_size_x/y/z` a multiple of the hardware wave size (64 is a safe default) and bounds-check against buffer size.
- Use `specialization constants` (`layout(constant_id = N)`) for compile-time variants in Vulkan.
- Normalize vectors you assume are unit length and guard `pow`, `sqrt`, `log` and divisions against bad inputs.

## Avoid
- `vec3` members in `std140` blocks next to scalars: host and shader offsets diverge. Add padding or use `vec4`.
- Branching on non-uniform values around `texture()` with implicit derivatives: undefined. Use `textureLod` or `textureGrad`.
- `gl_FragColor` and `varying`/`attribute`: removed in core. Use `out` and `in`.
- Uninitialized locals and outputs: garbage on some drivers. Assign every output on every path.
- Comparing floats with `==`: use an epsilon.
- Different `#version` than the host context: compile errors at runtime. Match the context.
- Relying on one vendor's leniency: validate with glslang before committing.

## Review
- [ ] Each shader compiles with glslang for its stage and, for Vulkan, passes `spirv-val`.
- [ ] Host struct layouts match the block layout (`std140` or `std430`) field by field.
- [ ] Every in and out has an explicit location; the stages' interfaces match.
- [ ] No derivative functions inside non-uniform control flow.
- [ ] Outputs are written on all code paths.
