# Brainstorm — lens: user value

- **Export the theme to everything around the TUI** — FEATURE — value 4 — effort M — risk low — category: themes
  Why: themes live only in tui.toml, and T-1217 shows the docked pane's colours already clash with its surroundings. Import is covered in the list above; export is not.
  Done when: `fm code theme export --to kitty,alacritty,wezterm,tmux,fzf` writes files whose colours match the theme's role table (a test compares each hex), and prints the include line without editing any user file.

- **Swipe through the deferred backlog** — FEATURE — value 4 — effort S — risk low — category: triage
  Why: the pack lists about 25 "Later from T-07xx/08xx" tasks sitting deferred. A "Later from" expiry is already proposed, but nothing lets the user clear them quickly.
  Done when: `fm triage` shows one deferred task at a time, one key each for do now, keep, or drop. Drops and keeps are recorded with a reason, and a test shows 10 decisions update the ledger with no other file changes.

- **Write the Go, JVM, Swift, C# and shell build playbooks** — FEATURE — value 4 — effort L — risk low — category: playbooks
  Why: the build stage covers only rust, ts and cpp, and the lang stage only python, rust and cpp, yet the ask is "way more playbooks". Library cards exist for jvm, native and mobile but no playbook uses them.
  Done when: each new playbook ships an original-text file plus a seeded-bug eval that fails without it. `fm playbooks` lists them under build/lang and the evals pass.

- **Generate a consistent icon and empty-state illustration set** — FEATURE — value 4 — effort M — risk low — category: ui assets
  Why: stock icon sets are one of the loudest generic-UI tells, and the pack shows svg-canvas cards but no generator. Assumption: a stdlib SVG emitter on a shared grid is enough.
  Done when: `fm icons build` turns a grid and stroke spec into 24 named SVG icons plus 3 empty-state illustrations. `fm check` fails an icon off the grid or with mismatched stroke weight, and the output is byte-reproducible.

- **Direct the camera with a recorded path** — FEATURE — value 3 — effort M — risk med — category: 3d
  Why: the list has scene recipes and scroll-linked scenes, but nobody authors camera moves. Hand-tuned camera numbers are where 3D heroes go generic. Assumption: users prefer dragging to typing keyframes.
  Done when: a dev-page helper records a drag-and-scroll camera path to `camera.json` (keyframes, easing, scroll mapping). A headless test replays it and gets the same camera matrix at frames 0, 30 and 60.

- **Write a game-feel ("juice") playbook with intensity caps** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: motion and interaction playbooks are covered, but hit-stop, screen shake, squash-and-stretch and anticipation are not. The guard refusal that "shakes the frame" is already proposed as an effect and needs safe limits.
  Done when: the playbook gives each technique a magnitude, duration and a flash-safe cap. A lint on a sample page flags a shake over the cap, and the TUI guard flash cites the playbook's numbers.

- **Port with a differential parity oracle** — FEATURE — value 3 — effort M — risk med — category: migration
  Why: migration and codemod playbooks are proposed, but "rewrite this in X" is its own hard case: recorded inputs run through old and new code with outputs diffed.
  Done when: `fm port record` captures inputs and outputs from the original, and `fm port check` runs them against the new code, listing each diverging case. It can be used as a task's verify command, and a test with one planted divergence turns red.

- **Write an experiment and ML playbook with a metric evidence kind** — FEATURE — value 3 — effort M — risk low — category: ml
  Why: ml cards exist, but no playbook covers seeds, baselines or "is 0.3% better real". The noise-aware perf evidence kind is already proposed and could be reused here. Assumption: the user trains models sometimes.
  Done when: the playbook requires a pinned seed, a baseline run and N repeats. `fm task prove` accepts a metric claim only when the gain exceeds the measured spread, and a test rejects a within-noise improvement.

- **Write a web loading and intro choreography playbook that never blocks LCP** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: TUI empty and loading states are covered, but not web splash, font swap and first-reveal sequences, which are where "good animation" often ruins performance.
  Done when: the playbook's template page keeps its LCP within budget in a headless run while playing a 1.2-second staged reveal, and the check fails a variant that hides content behind the animation.

- **Walk through a 3D lookbook gallery room (wild)** — FEATURE — value 3 — effort L — risk med — category: design showcase
  Why: wild. The lookbook and style-recipe shelf are proposed as flat pages. A small browsable room, one framed plinth per look, would make the 40 styles feel like something shown to friends. Assumption: the zero-dependency 3D scaffold exists first.
  Done when: `fm page lookbook --room` writes one HTML file, with no network access, that renders every look on its own plinth. A headless run visits each one and screenshots it, and the page still works with keyboard only.

- **Sketch a TUI layout with the mouse (wild)** — FEATURE — value 3 — effort M — risk med — category: tui config
  Why: wild. Layout is hand-edited TOML and the settings-screen ideas centre on forms. A canvas where the user drags panel borders in box-drawing characters, then saves, matches how people picture a layout. It is also one possible shape for the layout builder.
  Done when: in the app, dragging a divider updates a live layout and `Save` writes the matching `tui.toml` layout block. A pty test replays drag events and the round trip reproduces the same frame.

- **Pull a grade preset out of a photo (wild)** — FEATURE — value 2 — effort M — risk low — category: 3d look
  Why: wild. Palette extraction from screenshots is covered. Turning a photo's contrast curve, grain and bloom into a postprocessing preset for a 3D scene is not, and it makes a distinctive look from something personal.
  Done when: `fm design grade photo.jpg` writes a preset JSON of tint curve, grain amount and bloom threshold. A fixture photo gives stable values, and the 3D template loads the preset with no code changes.

- **Add a sonic UI recipe set, off by default (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The list has terminal bells but nothing for the web. Tiny synthesized WebAudio sounds with no audio files fit the "non-generic" ask. They would mute on reduced motion and never autoplay.
  Done when: the playbook ships 6 oscillator recipes (tick, confirm, error, whoosh). The template plays nothing before a user gesture, and a lint fails any page that autoplays audio.
