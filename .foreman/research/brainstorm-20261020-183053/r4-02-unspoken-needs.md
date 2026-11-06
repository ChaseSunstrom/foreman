# Brainstorm — lens: unspoken needs

- **Turn "super improve X" into a scorecard before work starts** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: the last three asks were open-ended ("super improve foreman", "super improve the foreman code tui, better animations/looks…", "keep going"). Nothing says when such an ask is done. This turns the ask into 4–6 measurable targets (text-per-screen ratio, frame-time budget, theme count, golden-frame coverage) with a stop condition, and shows the progress in the TUI.
  Done when: `fm task new` on a vague "improve" request writes a scorecard file with numeric targets, and `fm task prove` refuses to close the umbrella task until each target is met or explicitly waived.

- **Gate releases on a standing policy** — FEATURE — value 5 — effort M — risk med — category: release
  Why: the user said "no need to ask me, feel free to release at any time" and has sent six near-identical "Release 1.2.N and push" requests. Record that as a durable authorization with guards: CI green, no bench regression beyond the noise band, changelog drafted from closed task ids. Foreman can then release unprompted and stop itself when a guard fails.
  Done when: `fm release --auto` exits without prompting if every guard passes. It refuses and names the failing guard otherwise. A test covers one passing and one failing case.

- **Reproduce GitHub-runner slowness locally** — FIX — value 4 — effort S — risk low — category: CI
  Why: CI went red on Linux 3.12 twice for timing reasons (only 4 of 8 tasks queued inside the hook's 5 s; CPU-time bounds). Both passed on the dev box. A `fm ci-sim` that runs the suite under CPU quota (cgroup/`taskset` plus `nice`) would catch these before the push.
  Done when: `fm ci-sim` runs the timing-sensitive tests at a quarter of the CPU, and a deliberately slowed hook fails there but passes unthrottled.

- **Make the README demo regenerate and fail on drift** — CLEAN — value 4 — effort M — risk low — category: docs
  Why: `demo/live.svg` names Claude Code 2.1.301, while the project is adapting to 2.1.304 and the TUI keeps changing. Assumption: the demo is recorded by hand. Re-record it from a scripted fake run and compare it against the last render when the TUI or the tested version changes.
  Done when: the release check fails if the demo's recorded Claude Code version or TUI frame hash differs from the current ones, and `fm demo --record` regenerates it.

- **Turn the user's look complaints into checks** — FEATURE — value 5 — effort M — risk low — category: taste memory
  Why: "the TUI looked like crap with all the text" produced one redesign. The same complaint will come back on the next view unless it's stored as a rule. Save visual steers as lessons that become frame lints: text cells per screen, a minimum count of non-text glyphs, and color roles that aren't all one hue. Builders then run these before they show anything.
  Done when: a lint reads a golden frame and fails when its text-cell ratio is over the stored limit, and the limit came from a recorded steer.

- **Attach a before/after frame pair as evidence for UI tasks** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: Foreman's core claim is proof by commands that actually ran. A TUI task today can only prove that tests pass, not that the screen got better, and the user judges by eye. The close-out should carry two rendered frames (old commit and new commit, same fixture run) and a diff summary the user can skim after an unattended run.
  Done when: closing a task that touches TUI files stores `before.txt` and `after.txt` frames in the task record, and `fm task show` displays them side by side.

- **Show cost per proved task live** — FEATURE — value 4 — effort S — risk low — category: metrics
  Why: the user's benchmark ask was "cost per fully-correct session", and they want Foreman cheaper and faster than Claude Code. The TUI header should carry that same number: running dollars divided by tasks closed with proof, next to the last bench figure for plain Claude Code. This is different from a burn gauge, because it divides by delivered work.
  Done when: the header shows `$/proved` once one task has closed, and an integration test with a fake run asserts the value equals total cost divided by proved tasks.

- **Wild: Pick between two looks and let it learn** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: assumption: the user is the only judge of looks, and writing a style brief is harder than choosing. Show two renderings of the same live frame, one dense and one airy or one theme against another, and ask for a key press. Store the pick as the default for that view, and keep the previous pick one key away.
  Done when: `fm code tui --compare` shows two variants of one frame and writes the chosen variant's settings to the user config. wild

- **Wild: Hand the TUI a reference app to imitate** — FEATURE — value 3 — effort L — risk med — category: design input
  Why: "better looks" is hard to specify, but the user knows tools whose screens they like. Capture a run of that tool in a pty, reduce each frame to structure (panel boxes, density, color count, motion rate), and give those numbers to the builder as a target the TUI's golden frames are measured against.
  Done when: `fm look capture CMD` produces a structure profile file, and a lint reports how far a TUI frame is from it on density, panel count and color count. wild

- **Wild: Print a shift-change note at the top of every new session** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: the user's habit is "continue" and "keep going" across sessions, with CI failures and releases landing in between. Open each session with 5 lines: what was released, what's red, what's blocked on them (T-0325 needs a pacman package, T-0352 needs a publish decision), and the one task to do next. Keep it short, since context tax is already a tracked cost.
  Done when: session start emits a digest of at most 5 lines under a byte budget enforced by the context-tax test, and it lists every blocked task that needs the user's action. wild

- **Count a "taste regression" when a look gets worse** — FIX — value 3 — effort M — risk low — category: regression
  Why: an unattended polish pass could add animation that quietly raises text density or CPU cost. Record per-view metrics (text ratio, colors, frame ms) each release and report any view that moves the wrong way. This is separate from golden frames, which flag any change, good or bad.
  Done when: `fm code tui --metrics` prints per-view numbers, and the release check names a view whose text ratio or frame time grew by more than its band against the last release.

- **Split `register.tsx` so the pane and TUI share one source of truth** — CLEAN — value 3 — effort M — risk med — category: structure
  Why: T-0166 is deferred, and the foreman-ui pane and `fm code` TUI both need the same station, check and Gantt pictures. Without a shared module, each polish round is built twice and the two drift, which the user will see as one of them looking worse.
  Done when: the band and pane render through a shared module, with one test that renders the same fixture event log through both and gets identical station-track output.
