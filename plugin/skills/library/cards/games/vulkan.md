---
name: vulkan
title: Vulkan
area: games
tags: [vulkan, graphics, gpu, spirv, rendering, validation]
detect: [dep:ash, dep:vulkano, dep:vulkan, file:*.spv, ext:.spv, ext:.vert, ext:.frag, ext:.comp]
related: [glsl, opengl, wgpu, cmake]
---
Vulkan renderers: explicit synchronization and memory, validation layers, SPIR-V shaders compiled offline.

## Verify
- `vulkaninfo --summary`: a loader and at least one device are present on this machine.
- `glslc shader.frag -o shader.frag.spv`: the shader compiles to SPIR-V (or `glslangValidator -V shader.frag -o shader.frag.spv`).
- `spirv-val shader.frag.spv`: the SPIR-V is valid for the target environment.
- `VK_LOADER_DEBUG=error ./app`: loader and layer problems print instead of failing silently.

## Test first
Run headless with the validation layer on, and make zero validation messages the failing check. Use a software device (lavapipe) in CI.
```bash
# fails until the app produces zero validation errors
VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.x86_64.json \
./app --frames 10 --headless 2>&1 | tee run.log
! grep -E "VUID-|Validation Error" run.log
```
For image output, render one frame offscreen and compare against a stored reference with a tolerance.

## Do
- Enable `VK_LAYER_KHRONOS_validation` in debug builds and install a debug messenger; treat errors as test failures.
- Request only the features and extensions you use, after checking the physical device supports them.
- Allocate memory through VMA (or a sub-allocator), not one `vkAllocateMemory` per resource.
- Use frames in flight (2 typical) with a fence and semaphores per frame; wait on the fence before reusing resources.
- Insert barriers with the narrowest stage and access masks; prefer synchronization2 (`vkCmdPipelineBarrier2`) where available.
- Recreate the swapchain on `VK_ERROR_OUT_OF_DATE_KHR` and on resize; handle `VK_SUBOPTIMAL_KHR`.
- Compile shaders at build time and load SPIR-V; use specialization constants for variants.
- Destroy objects in reverse creation order and `vkDeviceWaitIdle` before teardown.

## Avoid
- Testing only on one vendor's driver: lenient drivers hide bugs. Validate with the layers and test a second device or lavapipe.
- Ignoring `VkResult`: a swallowed `VK_ERROR_DEVICE_LOST` looks like a hang later. Check every call.
- Over-broad barriers (`ALL_COMMANDS` everywhere): serialize the GPU. Scope them.
- Wrong image layouts: transition explicitly and track the layout; validation flags it.
- Updating a descriptor set or buffer still in use by an in-flight frame: use per-frame copies or update-after-bind.
- Per-draw `vkCreate*` of pipelines: stall. Build up front or use a pipeline cache.
- Forgetting buffer alignment (`minUniformBufferOffsetAlignment`, std140/std430 layout): garbled data.

## Review
- [ ] Validation is clean over a multi-frame run including a resize.
- [ ] Every created object has a matching destroy in the right order.
- [ ] Synchronization is per frame in flight, with minimal stage and access masks.
- [ ] Shaders are validated SPIR-V built in the build, not hand-edited binaries.
- [ ] Device feature and extension requests are checked before use.
