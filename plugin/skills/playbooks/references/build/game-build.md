<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Game project build and import errors

Use when a game project will not load, import or export headless: Godot, Unity, Unreal, or a shader or GPU pipeline that fails to compile.

Built on the cards `fm lib show godot`, `fm lib show godot-gdscript`, `fm lib show unity`, `fm lib show unreal`, `fm lib show glsl` and `fm lib show wgpu`.

1. **Run the engine headless and read the log**, not the editor window:
   ```bash
   godot --headless --path . --quit
   Unity -batchmode -nographics -projectPath . -logFile - -quit
   glslangValidator -V shader.frag -o /dev/null
   ```
2. **First script or shader error only.** One parse error cascades into dozens of missing-type errors; fix the earliest and rerun.
3. **Import errors** (missing resource, stale `.import` or `Library/` cache): fix the reference or the asset. Deleting the cache is a last step and goes in the report, since it hides which asset was broken.
4. **Shader errors:** note the GLSL or WGSL version the target needs (`#version`, WebGL, Vulkan). A shader that compiles on one driver can fail on another; validate with `glslangValidator` or `naga`.
5. **Export or player builds:** run the exact export preset or `BuildPipeline` method CI uses, once, and keep its log.

Pass: the headless command exits 0 with no `ERROR` or `error CS` lines in the log.

Stop when a fix needs an engine version bump or an asset the repo does not hold.
