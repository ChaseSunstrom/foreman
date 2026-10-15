---
name: imgui
title: Dear ImGui
area: native
tags: [cpp, imgui, gui, immediate-mode, tools, backends, overlay]
detect: [dep:imgui, dep:imgui-sfml, file:imgui.ini, file:imgui_demo.cpp]
related: [sdl, raylib, cmake, cpp-modern, vcpkg]
---
Dear ImGui: immediate-mode UI with platform and renderer backends, ID stacks, frame structure and docking setup.

## Verify
- `cmake --build build -j`: backend sources (`imgui_impl_*`) compile with matching platform and renderer.
- `grep -rn "NewFrame\|Render()\|RenderDrawData" src`: each frame has NewFrame calls for the renderer, the platform, then `ImGui::NewFrame`, and ends with `ImGui::Render` plus draw data submission.
- `grep -rn "ImGui::PushID\|##" src | head`: loops over widgets have unique IDs.
- `ctest --test-dir build --output-on-failure`: logic tests pass (UI state kept in plain structs).

## Test first
Keep UI state in plain data and test it; for widget logic, run the context with no backend.
```cpp
TEST(Ui, ListSelectionClamps) {
    ListModel m{ .items = {"a","b"}, .selected = 5 };
    m.clamp();
    EXPECT_EQ(m.selected, 1);
}
```
For UI code, create `ImGui::CreateContext()`, set `io.DisplaySize` and `io.Fonts->Build()` / `GetTexDataAsRGBA32`, call `NewFrame`, `EndFrame`, then `DestroyContext`. Assert it does not trip `IM_ASSERT`.

## Do
- Order each frame: poll events (forward to `ImGui_ImplSDL2_ProcessEvent` or the GLFW callbacks), backend `NewFrame` calls, `ImGui::NewFrame()`, widgets, `ImGui::Render()`, clear, backend `RenderDrawData`, present.
- Enable keyboard nav or docking explicitly: `io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard | ImGuiConfigFlags_DockingEnable;` (docking and viewports live on the docking branch).
- Give identical labels unique IDs: `"Delete##%d"` or `ImGui::PushID(id)` / `PopID()` in loops.
- Match each `Begin`/`End`, `BeginChild`/`EndChild`, `Push*`/`Pop*`; `End` is required even if `Begin` returned false, but `EndPopup`/`EndTable`/`EndMenu` are called only when the matching `Begin*` returned true.
- Keep app state outside widgets; widgets edit it by pointer (`ImGui::SliderFloat("gain", &s.gain, 0, 1)`).
- Check `io.WantCaptureMouse` and `io.WantCaptureKeyboard` before passing input to the game.
- Set `io.IniFilename = nullptr` for tools that should not persist layout, or point it at a user-data directory.
- Compile Dear ImGui into your own target with the same defines in every translation unit (`IMGUI_USER_CONFIG`).

## Avoid
- Calling widgets outside `NewFrame`/`Render`: assertion failures. Keep all UI in the frame function.
- Same label twice without IDs: clicks hit the wrong widget. Add `##id`.
- Mismatched Begin/End: crashes with asserts. Use scope guards in a debug build.
- Holding `ImGuiIO&` or `ImFont*` across a context change or font rebuild: stale. Re-fetch each frame.
- Creating or destroying textures during `RenderDrawData`: do it between frames.
- Per-frame `std::string` allocation for labels in large lists: use `ImGuiListClipper` for long lists.
- Mixing backend sources from a different Dear ImGui revision: struct mismatches. Take them together.

## Review
- [ ] Frame call order matches the backend's documented sequence.
- [ ] Every Begin and Push has its End and Pop on all paths.
- [ ] Repeated widgets have unique IDs.
- [ ] Input capture flags gate game input.
- [ ] `imgui.ini` and layout persistence is a decision, not an accident.
