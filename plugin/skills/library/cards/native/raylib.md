---
name: raylib
title: raylib
area: native
tags: [c, cpp, raylib, game, graphics, audio, 2d, 3d]
detect: [dep:raylib, file:raylib.h]
related: [sdl, imgui, cmake, cpp-modern, sanitizers]
---
raylib: init and main loop, resource load/unload pairing, frame timing, and keeping game logic testable without a window.

## Verify
- `cmake --build build -j`: links `raylib` via `find_package(raylib REQUIRED)` or FetchContent.
- `ctest --test-dir build --output-on-failure`: logic tests run with no window.
- `cmake -B build-asan -DCMAKE_C_FLAGS="-fsanitize=address -g" -DCMAKE_CXX_FLAGS="-fsanitize=address -g" && cmake --build build-asan`: catches use-after-unload.
- `grep -c "Load" src/*.c* ; grep -c "Unload" src/*.c*`: every `Load*` call has a matching `Unload*`.

## Test first
Separate pure game logic from drawing and test that.
```c
// tests/test_player.c
#include <assert.h>
#include "player.h"

int main(void) {
    Player p = {.x = 0, .vx = 10};
    player_step(&p, 0.5f);          // pure math, no raylib window
    assert(p.x == 5.0f);
    return 0;
}
```
Keep `raylib` calls such as `DrawRectangle` in a thin render layer so no test needs `InitWindow`.

## Do
- Open with `InitWindow(w, h, title)`, set `SetTargetFPS(60)`, loop on `while (!WindowShouldClose())`, and close with `CloseWindow()`.
- Wrap drawing: `BeginDrawing(); ClearBackground(RAYWHITE); ... EndDrawing();` and use `BeginMode2D(camera)`/`EndMode2D()` for camera space.
- Use `GetFrameTime()` for delta time; move by `speed * dt`.
- Pair every `LoadTexture`/`LoadSound`/`LoadFont`/`LoadModel` with `UnloadTexture`/`UnloadSound`/`UnloadFont`/`UnloadModel`, and unload before `CloseWindow()`.
- Call `InitAudioDevice()` before loading sounds, and `CloseAudioDevice()` at the end.
- Load assets after `InitWindow` (textures need the GL context) and check validity: `IsTextureValid(tex)` or `tex.id == 0` in older releases.
- Use `SetConfigFlags(FLAG_VSYNC_HINT | FLAG_WINDOW_RESIZABLE)` before `InitWindow`.
- Resolve asset paths from `GetApplicationDirectory()` so launching from another cwd works.

## Avoid
- Loading textures or models inside the frame loop: leaks and hitches. Load once.
- Forgetting `UnloadTexture` on reload: GPU memory leak. Unload the old handle first.
- Calling `LoadTexture` before `InitWindow`: crash or blank texture. Order matters.
- Using `GetTime()` deltas ad hoc instead of `GetFrameTime()`: jitter. Use frame time or a fixed step.
- Using raylib types (`Vector2`) in core logic that tests link without raylib: extra link. Own small math types or link raylib's math header only.
- `SetTargetFPS` plus vsync flag together giving uneven frame pacing: choose one.
- Hard-coded relative asset paths like `"assets/x.png"`: break when cwd differs. Resolve a base path.

## Review
- [ ] Every Load has a matching Unload on exit and on reload.
- [ ] Movement uses delta time, not a per-frame constant.
- [ ] Game logic is separate from draw code and has tests.
- [ ] Window, audio and resource init order is correct, and teardown reverses it.
- [ ] Assets resolve from a known base path.
