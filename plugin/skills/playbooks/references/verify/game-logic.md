<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Verify game logic without a window

Use when you change game rules, physics, pathfinding, or a simulation step and need proof that does not depend on someone playing it.

Built on the cards `fm lib show game-loop`, `fm lib show game-physics`, `fm lib show pathfinding`, `fm lib show godot-gdscript` and `fm lib show unity-testing`.

1. **Separate simulation from rendering.** If logic cannot run with no window or GPU, the first change is that split; do it test-first.
2. **Fixed timestep, seeded randomness.** A test steps the simulation N ticks with a fixed seed and compares state, so a failure reproduces exactly.
3. **Run the engine's headless tests:**
   ```bash
   godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
   Unity -batchmode -nographics -projectPath . -runTests -testPlatform EditMode -testResults editmode.xml
   pytest -q
   ```
4. **Hunt the usual causes of flake:** `grep -rniE "random\(|rand\(|Date\.now|time\.time" src` inside simulation code, and frame pacing done by sleeping (`grep -rn "sleep(\|setTimeout(" src`).
5. **Edge cases that break games:** zero and huge delta time, a fast body through a thin wall, an unreachable goal, the same input twice.
6. **Feel is not testable here.** Say what a human must still play.

Pass: the headless suite exits non-zero before the fix and 0 after, twice in a row with the same seed.
