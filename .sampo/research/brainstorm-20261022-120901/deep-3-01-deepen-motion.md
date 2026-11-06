# Brainstorm — lens: deepen: motion

- **Compile one Motion Score to every surface** — FEATURE — value 5 — effort L — risk med — category: motion
  Why: pack lists "Motion Score file format that compiles to CSS, WAAPI, three.js tweens and the TUI clock" plus "one motion score into CSS and TUI clock" as separate ideas; merged they are the spine for the rest. fmcodetui.py already has shimmer/fades/glow/spinners with no shared timing source, and site/style.css has its own. Stdlib-only compiler `fm motion build`.
  Done when: one `motion.toml` with 3 named sequences produces CSS keyframes, a WAAPI JSON file and a TUI clock table, and a test asserts the same duration and easing id appear in all three.

- **Lint motion tokens in generated UI** — FEATURE — value 5 — effort M — risk low — category: motion lint
  Why: merges "lintable tokens", "Afterglow lint" and "native CSS default tier". A `fm check motion` verify command scans CSS/TSX for durations outside the token scale, animating layout properties (width, top, margin), missing `prefers-reduced-motion`, and traces over 600 ms. Gives playbooks a command Claude actually runs, which fits Foreman's "prove with commands" rule.
  Done when: a fixture with `transition: width 900ms` and no reduced-motion block fails with three named findings, and the clean fixture passes.

- **Verify motion from a filmstrip** — FEATURE — value 4 — effort L — risk med — category: motion verify
  Why: "Measure the motion from a filmstrip, not the CSS" and "assert reduced-motion equals final frame" need one harness. Assumption: a headless browser is available as a trusted tool; if not, the check reports skipped, not passed. It captures frames at fixed times, checks the first frame differs from the last, the reduced-motion render equals the last frame, and no frame is blank.
  Done when: `fm check filmstrip URL` writes N PNGs plus a verdict, and a page whose animation never runs fails with "frames identical".

- **Ship a motion choreography playbook family** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: only ui/terminal-ui.md (13 lines) exists as a UI playbook. Original writing, split into small files: stagger and hierarchy, weight by significance, loading and intro that never block LCP, game-feel with intensity caps, 3D camera and scene transitions. Each ends with the exact lint or filmstrip command from the ideas above.
  Done when: `/foreman:playbooks` lists ≥5 motion files in a ui stage, each naming a runnable check, and a test confirms each referenced command exists.

- **Add a motion preview in the TUI settings screen** — FEATURE — value 4 — effort M — risk low — category: tui config
  Why: the user asked for config inside the TUI, and there is no settings screen today (hand-edited TOML). Motion is the setting people can't judge from a number: a live preview box that loops the current shimmer, fade and spinner while you change speed, easing and intensity, then writes to tui.toml.
  Done when: changing "motion intensity" in the app updates the preview within one frame and the saved tui.toml round-trips through `fm code tui --print-config`.

- **Add a hush key with a motion budget** — FEATURE — value 3 — effort S — risk low — category: tui motion
  Why: merges "hush button" and "weight in proportion to significance". One key sets level 0–3 (off, state only, normal, full); each effect declares its level and a CPU cost, and the app respects `NO_MOTION`, reduced-motion, and slow SSH detection.
  Done when: at level 0 a recorded frame run shows no animated cells apart from required state changes, and at level 3 shows all.

- **Gate motion on frame-time budget** — PERFORMANCE — value 3 — effort M — risk low — category: motion perf
  Why: assumption: heavy glow/chart redraws can stall a terminal over a slow link. The animator measures its own frame cost and drops effects in priority order (decor first, state cues last) instead of lagging input. Pairs with `tests/bench_hooks.py`-style benchmarking.
  Done when: a test injecting 100 ms render delay shows decorative effects dropped while the keypress-to-paint latency stays under a stated bound.

- **Wild: Extract a Motion Score from a screen recording** — FEATURE — value 3 — effort L — risk high — category: motion wild
  Why: wild. Foreman already records demo/*.cast and mp4. Diff frames to detect regions that moved, fit durations and easings to curves, and emit a draft motion.toml, so "make it feel like this clip" becomes a file the lint then enforces.
  Done when: a recording of a known 300 ms ease-out fade yields a score with duration within ±50 ms and an ease-out curve class.

- **Wild: Motion lab page generated from the score** — FEATURE — value 3 — effort M — risk low — category: motion wild
  Why: wild. `fm page` artifacts already exist. Generate a single self-contained page showing every token as a playable swatch, with scrub, slow-mo, a reduced-motion toggle, and drag-to-edit curves that write back the score. It doubles as the site's design-system page.
  Done when: `fm motion lab` writes one HTML file with no external hosts (matches the T-24 site rule) and a test confirms every token in the score appears.

- **Wild: Sound-off "motion diff" in code review** — FEATURE — value 3 — effort M — risk med — category: motion review
  Why: wild. When a task changes animation, the close-out receipt shows before/after filmstrips side by side with changed durations, so a human reviews motion as motion. Fits the open close-out legibility work (T-0795).
  Done when: a task that changes a transition from 200 ms to 400 ms produces a receipt containing both filmstrips and the "200→400 ms" line.

- **Wild: Tempo that follows the agent's state** — FEATURE — value 3 — effort S — risk low — category: motion tui
  Why: wild. The fm code app's ambient pulse tracks the loop: slow breathing while the model thinks, a quickening when checks run, one settle when a task proves, and a single sharp cue only when the guard blocks. Motion becomes information, not decoration.
  Done when: a scripted event stream (think, check, prove, block) yields four distinct clock rates recorded in a test, and the block cue is the only one exceeding the intensity cap.

- **Teach 3D scene motion with a camera and easing playbook plus card checks** — FEATURE — value 3 — effort M — risk low — category: motion 3D
  Why: the library has three-js, react-three-fiber and postprocessing cards but none teaches choreography. Cover camera dolly paths, damped springs rather than linear lerps, frame-rate-independent updates, and idle-loop budgets; verified by a check that tweens use delta time rather than frame counts.
  Done when: a fixture scene using `+= 0.01` per frame is flagged by `fm check motion --3d`, and the delta-time version passes.

- **Record motion regressions as eval cases** — FEATURE — value 2 — effort M — risk low — category: evals
  Why: ties to the open `fm eval capture` (T-0035). A failing motion lint or filmstrip in a finished task becomes a redacted case, so playbook changes can be scored on whether Claude stops producing the same janky transitions.
  Done when: capturing a task that failed `fm check motion` yields an eval case that reproduces the failure and passes after the fix.
