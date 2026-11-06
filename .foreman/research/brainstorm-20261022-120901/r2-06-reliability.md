# Brainstorm — lens: reliability

- **Add a content-torture fixture to every UI gate** — FEATURE — value 5 — effort M — risk low — category: design QA
  Why: assumption: generated UI breaks on real data, not on the lorem-ipsum the model writes. The pack shows `fm shot`/`fm check ui` proposals but no hostile-data pass.
  Done when: `fm check ui` renders a page against a fixture of 300-character names, RTL text, emoji ZWJ sequences, empty lists, 10k rows and a 0-byte image, and fails on overflow, clipped text or a layout shift over a set threshold.

- **Freeze time for screenshot proofs** — FIX — value 5 — effort M — risk med — category: visual QA
  Why: assumption: animated pages never produce the same screenshot twice, so visual proof is flaky and will be dropped. The pack has the screenshot proof loop and golden frames, but nothing makes the page itself deterministic.
  Done when: `fm shot --freeze` injects virtual time, a seeded `Math.random` and paused CSS/WAAPI animations, and two runs on one commit give byte-identical PNGs at t=0, t=mid and t=end.

- **Require a WebGL survival contract in the 3D playbook** — FEATURE — value 4 — effort M — risk low — category: 3D
  Why: the pack has a 3D playbook with a perf budget and leak soak, but nothing on losing the GPU. Phones and driver resets fire `webglcontextlost`.
  Done when: a lint on the 3D scaffold fails unless the scene has context-lost/restored handlers, a DPR cap, visibility-based pause and a static poster fallback. A headless test forces context loss and the page recovers or shows the poster.

- **Gate the slop detector with a precision corpus** — FEATURE — value 4 — effort M — risk low — category: design QA
  Why: the pack has many "slop detector" and "generic-UI tell" lint ideas. A lint that flags good, distinctive designs gets switched off.
  Done when: `fm check design` ships with 15+ original, deliberately distinctive reference pages that must pass, plus a generic corpus that must fail. CI breaks if either rate regresses.

- **Check playbooks for contradictory directives** — CLEAN — value 3 — effort M — risk low — category: playbooks
  Why: the pack proposes dozens of new playbooks (motion, a11y, anti-generic, 3D). They will clash, e.g. "always animate entrances" against "honour reduced-motion with no movement".
  Done when: playbooks declare checkable directives in frontmatter (`requires`/`forbids` tokens). `fm doctor` fails when two playbooks that load for one task conflict, and names both.

- **Run a routing eval for every new design playbook** — FEATURE — value 4 — effort M — risk low — category: skills
  Why: the pack has 1,161 skill files and a proposed trigger-overlap constellation, but no test that a request like "make it feel less like a template" loads the right playbook.
  Done when: each playbook carries 8 positive and 4 negative sample requests. The routing test passes at ≥90% recall with zero negatives loading, and runs in CI.

- **Add a browser-less fallback chain to `fm shot`** — FIX — value 4 — effort M — risk low — category: visual QA
  Why: assumption: many machines, including this hardened-kernel Arch box, lack a headless browser. A silent skip would count as a pass.
  Done when: with no browser, `fm shot` degrades to a stdlib SVG/DOM-snapshot render. It records the evidence as `unverified-visual` and refuses to close a UI task as "proved".

- **Make A/B playbook evals report variance** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: the pack has "A/B every playbook" and `fm eval capture` run N times, but a lift measured on a single run is noise. T-1380 shows load-dependent flake is already a live problem.
  Done when: `fm eval` reports paired-seed results with an interval and a minimum-detectable-effect line, and marks "no lift shown" when the interval spans zero.

- **Wild: Render with a canary palette that exposes hardcoded colours** — TEST — FIX — value 3 — effort S — risk low — category: TUI
  Why: wild. The pack has theme engines and contrast checks, but hardcoded ANSI colours in panels and extensions quietly escape them.
  Done when: `fm code tui --canary-palette` maps every theme role to loud magenta variants. A frame snapshot test fails if any painted cell uses a colour outside the role table.

- **Wild: Bisect tui.toml to find the setting that breaks the screen** — FEATURE — value 3 — effort M — risk low — category: config
  Why: wild. Hand-edited TOML plus a new settings screen means "something's off" bugs. The pack has last-good fallback but no way to isolate the cause.
  Done when: `fm code tui --bisect` replays the config key by key against a smoke render and names the first key whose frame fails an invariant (overflow, unreadable text, a crash).

- **Wild: Use integer-only maths in the TUI 3D rasteriser** — FEATURE — value 3 — effort L — risk med — category: 3D
  Why: wild. The pack proposes a stdlib software rasteriser. Float differences across Python builds and architectures would break golden frames.
  Done when: the rasteriser uses fixed-point maths, and a golden frame of a rotating cube hashes identically on the oldest and newest supported Python.

- **Test generated pages under offline and slow-3G profiles** — FEATURE — value 3 — effort M — risk low — category: web QA
  Why: assumption: the web-UI playbooks assume fast networks. The pack's "no third-party loads" rule is only enforced on Foreman's own site.
  Done when: `fm shot --net slow3g|offline` loads the page. It fails if the first meaningful paint takes over a set budget or if an offline state shows a blank screen instead of a designed error face.
