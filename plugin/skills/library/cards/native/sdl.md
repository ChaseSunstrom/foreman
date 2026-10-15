---
name: sdl
title: SDL2 / SDL3
area: native
tags: [c, cpp, sdl, graphics, audio, input, game, events]
detect: [dep:sdl2, dep:sdl3, dep:sdl2-image, dep:sdl2-ttf, dep:sdl2-mixer]
related: [cmake, imgui, raylib, cpp-raii, sanitizers]
---
SDL: init flags, the event loop, renderer and window ownership, fixed timestep, audio callbacks, and SDL2 vs SDL3 API differences.

## Verify
- `cmake --build build -j`: links `SDL2::SDL2` (or `SDL3::SDL3`) through `find_package`.
- `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy ctest --test-dir build --output-on-failure`: headless tests with no display or sound device.
- `cmake -B build-asan -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -g" && ctest --test-dir build-asan`: catches leaked surfaces and textures.
- `grep -rn "SDL_GetError" src | wc -l`: error paths report the SDL error text.

## Test first
Test logic with the dummy video driver; the failing case is an init error you must report.
```cpp
TEST(Window, CreatesHeadless) {
    setenv("SDL_VIDEODRIVER", "dummy", 1);
    ASSERT_EQ(SDL_Init(SDL_INIT_VIDEO), 0) << SDL_GetError();
    SDL_Window* w = SDL_CreateWindow("t", 0, 0, 64, 64, 0);
    ASSERT_NE(w, nullptr) << SDL_GetError();
    SDL_DestroyWindow(w);
    SDL_Quit();
}
```
In SDL3 `SDL_Init` returns a bool (true on success) and `SDL_CreateWindow` drops the position args; adjust accordingly.

## Do
- Call `SDL_Init` with only needed subsystems and check the result; log `SDL_GetError()` on every failure.
- Wrap handles (`SDL_Window`, `SDL_Renderer`, `SDL_Texture`, `SDL_Surface`) in `std::unique_ptr` with the matching `SDL_Destroy*`/`SDL_Free*` deleter.
- Drain events each frame with `while (SDL_PollEvent(&e))`; handle `SDL_QUIT` (SDL2) or `SDL_EVENT_QUIT` (SDL3).
- Run a fixed-timestep update with accumulated delta from `SDL_GetPerformanceCounter()` / `SDL_GetPerformanceFrequency()`; render at display rate.
- Request vsync via `SDL_RENDERER_PRESENTVSYNC` (SDL2) or `SDL_SetRenderVSync` (SDL3).
- Use `SDL_AudioStream` (SDL3 or SDL2 2.0.18+) rather than the raw audio callback where possible; keep callbacks lock-free and short.
- Load assets relative to `SDL_GetBasePath()`, not the working directory.
- Add `SDL_main` handling: include `SDL_main.h` or define `SDL_MAIN_HANDLED` where needed.

## Avoid
- Ignoring return values: SDL2 functions return negative on failure and NULL pointers on error. Check and log `SDL_GetError()`.
- Creating textures every frame: leaks and stalls. Create once, update with `SDL_UpdateTexture`.
- Rendering or touching the window from another thread: SDL video is main-thread only on most platforms. Send work back to the main thread.
- Blocking or allocating inside the audio callback: glitches. Use a ring buffer.
- Frame-rate-dependent movement (`x += 5`): scale by delta time or use a fixed step.
- Mixing SDL2 headers with SDL3 libs after upgrading: wrong include path (`<SDL3/SDL.h>`) and renamed functions. Search the migration notes.
- Forgetting `SDL_Quit()` and destroy order: destroy textures and renderer before the window.

## Review
- [ ] Every SDL call that can fail is checked, with the error logged.
- [ ] All handles have RAII owners and destroy in reverse creation order.
- [ ] Game logic runs on a fixed timestep and is testable without a window.
- [ ] Rendering and event handling stay on the main thread.
- [ ] The target SDL major version is stated in the build and code.
