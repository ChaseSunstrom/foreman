# Brainstorm — lens: reliability

- **Gate every settings write with a render-before-commit dry run** — FEATURE — value 5 — effort M — risk low — category: config reliability
  Why: the request wants live TUI config saved back to tui.toml/code.toml, and the pack has no settings screen today (all hand-edited TOML). Earlier ideas cover last-good copies and confirm-or-revert, but not proving the candidate renders. Assumption: fmcodetui.py can be driven headless with a fake event stream.
  Done when: a test writes a tui.toml with an unreadable theme (fg equals bg) and a zero-width layout; the settings screen refuses to apply both, names the failing check, and the live frame is unchanged.

- **Record every TUI crash as a replayable fixture automatically** — FEATURE — value 4 — effort M — risk low — category: crash capture
  Why: recent commits fix wide-glyph padding (T-1468) and paste (T-1316) after the fact; each was found by eye. Assumption: the event log is deterministic enough to replay.
  Done when: forcing an exception in a panel's render writes `crash-<ts>.json` (event slice, size, theme, tui.toml hash); `fm code tui --replay` reproduces the same exception in a test, and the fixture is picked up by the golden-frame suite.

- **Add a display-width oracle test that sweeps every panel with hostile strings** — FIX — value 4 — effort S — risk low — category: layout correctness
  Why: T-1468 shows `len()` used as width and padded wrong. Assumption: other panels share the pattern. A corpus (CJK, emoji ZWJ, combining marks, bidi, tabs) catches the class, not one instance.
  Done when: a test renders each panel at 20/40/80/200 columns with the corpus and asserts every output row is exactly the target column width and no row wraps.

- **Bench-gate every new design playbook with a headless-render failure budget** — FEATURE — value 4 — effort L — risk med — category: design verification
  Why: the user wants far more UI/3D/motion skills, but nothing in the pack proves generated output works (blank WebGL canvas, context loss, 0-height hero). Assumption: a headless browser may be missing, so the check must degrade to a static lint with a stated reason.
  Done when: `fm check ui` on a deliberately broken 3D page (shader compile error) fails with the console error quoted, and on a fixed page passes; with no browser installed it prints "not verified: no browser" and exits non-zero under `--strict`.

- **Make skill and playbook edits atomic and index-consistent** — FIX — value 3 — effort S — risk low — category: library integrity
  Why: with 1161 skill files and T-0 style "fm lib source add killed at any step" asks, a mass authoring round (the user's "way more playbooks") multiplies partial-write risk. Assumption: the index is rebuilt non-atomically for local playbooks.
  Done when: a test kills the writer at each of N syscalls during a playbook add and afterwards the index either lists the old set or the new set, never a mix, and `fm doctor` is green.

- **Add a round-convergence stop so "super recursive" cannot loop forever** — FEATURE — value 5 — effort M — risk low — category: loop safety
  Why: the user asked for recursive brainstorm "etc. etc.", and this is round 3 with hundreds of near-duplicate ideas. Assumption: duplicates can be detected by title-token overlap.
  Done when: a round whose new ideas overlap prior titles above a threshold (default 70%) halts with "converged: N of M duplicate" and files one decision card instead of tasks; a test feeds a repeated list and sees the halt.

- **Pin golden frames to a terminal-emulator oracle, not just stored text** — FEATURE — value 3 — effort M — risk med — category: test fidelity
  Why: golden frames alone can bless a wrong frame. Assumption: a small stdlib VT interpreter fits in a test helper.
  Done when: frames are fed through the interpreter and the resulting screen grid (not the raw escapes) is compared; a test with an unbalanced SGR or cursor-move overflow fails.

- **Flap-proof the canary: classify load-induced failures before filing tasks** — FIX — value 4 — effort S — risk low — category: canary noise
  Why: dropped items T-1380 and the 1.2.47/1.2.50 canaries were transient failures under side-by-side load and cost reviewed tasks. Assumption: load average at failure time is recoverable.
  Done when: a red canary reruns once after load drops below a threshold; only a second red files a task, and the first red is logged as "transient, load=X".

- **Wild: Run a "chaos twin" of the TUI that fuzzes keys, resizes and event floods nightly** — FEATURE — value 4 — effort M — risk low — category: fuzzing
  Why: assumption: the app's pty tests are scripted, not randomized. wild.
  Done when: a seeded 10-minute run exits with terminal restored and no exception; any failure prints its seed, and rerunning the seed reproduces it.

- **Wild: Keep a "last known good" copy of the whole TUI config that boots if the new one misrenders three times** — FEATURE — value 3 — effort M — risk med — category: self-heal
  Why: assumption: a misrendering config can pass validation yet look broken. wild.
  Done when: after three consecutive frame-budget or render failures with a new tui.toml, the app restarts on the last-good file and shows a one-line banner naming the bad key.

- **Wild: Bisect a regressed look across the theme/layout/key settings automatically** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: assumption: with many settings, a user can't tell which one broke the screen. wild.
  Done when: given a config and a failing render check, `fm code tui --bisect` outputs the minimal single key whose removal fixes the check, verified by a test with a seeded bad key.

- **Detect stale shader and 3D template drift by compiling them in CI** — CLEAN — value 3 — effort M — risk med — category: template rot
  Why: the user wants runnable 3D scene templates; library versions (three.js, R3F) change. Assumption: a pinned version plus a compile check is feasible offline.
  Done when: CI builds each scene template against its pinned versions headlessly and fails with the shader/log error on any break; the template card records the tested version.

- **Fail the release when any doc'd fence or demo command no longer runs** — CLEAN — value 3 — effort M — risk low — category: doc drift
  Why: the README leans on demo/live.svg and many new playbooks will embed commands. Assumption: not all fences are runnable today.
  Done when: `fm release` executes all fences marked runnable in a scratch copy and a deliberately broken fence blocks it with file and line.
