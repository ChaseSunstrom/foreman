<!-- Foreman's own playbook (written for Foreman, not ported). -->
# A game runs below 60 fps: find the CPU or GPU bound

Use when a game runs below 60 fps or hitches as the entity count grows.

Built on the cards `fm lib show game-loop`, `fm lib show shader-performance`, `fm lib show opengl`, `fm lib show vulkan`, `fm lib show unity` and `fm lib show godot`.

1. **Set the budget:** 16.6 ms for 60 fps, 8.3 ms for 120. Measure frame time in milliseconds, never fps.
2. **Find the bound:** CPU (simulation, draw-call submission) or GPU (fill rate, shaders, overdraw). Shrinking the resolution and seeing frame time fall means GPU-bound; it staying flat means CPU-bound.
3. **Profile with the engine's tool** (Godot profiler, Unity Profiler, RenderDoc for a GPU frame) and take the biggest bar first, in a release build, not the editor.
4. **Typical causes, by bound:** CPU: per-frame allocation, per-entity scripts, too many draw calls (batch, instance). GPU: expensive fragment work, overdraw, uncompressed textures, shader branches.
5. **Validate shader edits:** `glslangValidator -V shader.frag -o /dev/null`.
6. **One change, one measurement**, same scene, same camera path, several runs; keep the numbers (see the benchmark loop).

Pass: p95 frame time under budget over a scripted run, before and after numbers recorded.

Stop when the fix changes the look of the game; that is a design decision.
