---
name: opengl
title: OpenGL
area: games
tags: [opengl, graphics, gpu, glsl, rendering, c]
detect: [dep:gl, dep:glow, dep:glium, dep:glad, dep:PyOpenGL, dep:moderngl, dep:glfw]
related: [glsl, vulkan, wgpu]
---
OpenGL renderers: core profile, VAOs/VBOs/UBOs, GLSL shaders, state discipline and debug output.

## Verify
- `glxinfo -B`: the context, driver and GL version this machine provides.
- `glslangValidator shader.frag`: the shader compiles standalone.
- `LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a ./app --frames 5`: runs headless on Mesa software rendering (CI-friendly).
- `MESA_DEBUG=1 ./app`: Mesa prints more GL error detail.

## Test first
Create a hidden window or EGL context, render one frame, and read pixels back. Fail on any GL error or wrong pixel.
```python
import moderngl
def test_fill_color_renders_red():
    ctx = moderngl.create_standalone_context()
    fbo = ctx.simple_framebuffer((4, 4))
    fbo.use(); fbo.clear(1.0, 0.0, 0.0, 1.0)
    assert fbo.read(components=3)[:3] == b"\xff\x00\x00"
    assert ctx.error == "GL_NO_ERROR"
```
In C or C++ use `glGetError` in a loop after setup or enable `glDebugMessageCallback` and assert none arrive.

## Do
- Request a core profile context explicitly (for example 3.3 or 4.1 core, forward-compatible on macOS).
- Enable `GL_DEBUG_OUTPUT` and `glDebugMessageCallback` in debug builds (4.3+ or `KHR_debug`).
- Check `glGetShaderiv(..., GL_COMPILE_STATUS)` and `glGetProgramiv(..., GL_LINK_STATUS)` and print the info log.
- Use VAOs for all vertex state and set `layout(location = N)` in shaders, not name lookups per frame.
- Use uniform buffer objects with `std140` for shared data; query offsets or pad to 16 bytes.
- Batch draws and bind state by group (program, texture, VAO); avoid redundant binds.
- Delete buffers, textures and programs you create, and unbind on teardown.
- Load functions through GLAD, GLEW or the windowing library loader, after making the context current.

## Avoid
- Legacy fixed-function calls (`glBegin`/`glEnd`, `glMatrixMode`, `gl_ModelViewMatrix`): absent in core. Use buffers and shaders.
- Calling GL from a thread without the context current: undefined behavior. One thread per context.
- `glGetUniformLocation` or `glGetError` every frame in release: syncs the driver. Cache locations and use debug output.
- Reading back (`glReadPixels`, `glGetBufferSubData`) mid-frame: stalls the pipeline. Use PBOs or fences.
- Non-power-of-two or unaligned texture uploads with default unpack alignment: skewed images. Set `glPixelStorei(GL_UNPACK_ALIGNMENT, 1)` for tightly packed rows.
- Missing `GL_FRAMEBUFFER_COMPLETE` check after attaching: black output. Check `glCheckFramebufferStatus`.
- Forgetting sRGB handling: wrong gamma. Use `GL_SRGB8_ALPHA8` and `GL_FRAMEBUFFER_SRGB` deliberately.

## Review
- [ ] Context version and profile are requested explicitly and the code uses only that API.
- [ ] Shader and link logs are surfaced on failure.
- [ ] No GL errors or debug messages over a full frame loop.
- [ ] Resources are created once and released on teardown, not per frame.
- [ ] GL calls stay on the context's thread.
