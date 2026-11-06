# Brainstorm — lens: bold bets

- **Write the missing language and domain playbook wave** — FEATURE — value 5 — effort L — risk low — category: playbooks
  Why: The pack lists playbooks only for rust, ts, cpp and python, while the library has cards for jvm, games, ml, mobile, data and ops with verify commands and no playbook on top. Assumption: the 15 stages can take sibling files without a format change.
  Done when: `fm playbooks` lists go, jvm, swift/kotlin, C#, shell, SQL, game-loop and ML-training playbooks. Each names a verify command that its linked lib card also lists, and a routing test sends a matching request to the right one.

- **Build a shader Rosetta so one GLSL-subset recipe runs in browser and TUI** — FEATURE — value 4 — effort L — risk med — category: 3D / shader
  Why: The pack has `fm code app` motion (shimmer, glow) and a request for 3D and non-generic looks, but shader looks and cell shaders would be written twice. Assumption: a small stdlib interpreter or transpiler for a GLSL ES subset (uv, time, noise, mix, sdf primitives) is enough for backdrops and materials.
  Done when: one `.glsl` recipe renders as a WebGL fragment shader and as a per-cell colour function in the TUI. A test compares the two outputs at 5 sample points to within a stated tolerance.

- **Guard against the user's own look repeating across projects** — FEATURE — value 4 — effort M — risk low — category: design memory
  Why: Models converge on one look, and the user wants "non generic". Existing ideas measure distance from generic defaults, not from what this user's last projects already used. Assumption: a local fingerprint of palette, type pairing and motif per closed UI task is enough.
  Done when: starting a UI task in a second project prints the fingerprints of the previous five looks and `fm check design` fails if the new DESIGN.md is within a set distance of any of them.

- **Crawl a generated web app into a UI state graph** — FEATURE — value 4 — effort L — risk med — category: visual QA
  Why: Screenshot proof and a settings-screen monkey test are planned, but nothing explores a generated app as a whole. Assumption: headless Chromium is detected, with `fm shot` as the fallback.
  Done when: `fm shot crawl URL` writes a graph of reachable states with a screenshot per node. It reports dead ends, focus traps and overflow at 3 viewports, and a seeded run produces the same graph twice.

- **Write the test-craft playbook family (property, fuzz, golden, load)** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: The verify stage has only tdd and verification-loop. The team's own work leans on fuzz and golden-frame ideas, but no playbook teaches Claude to write them.
  Done when: four playbooks each ship a runnable template that passes in `plugin/tests`. Each template's check goes red when a planted bug is inserted.

- **Breed playbooks overnight against held-out UI briefs (wild)** — FEATURE — value 4 — effort L — risk med — category: evals / evolve
  Why: Wild. `test_evolve` exists in the bench, the plan is "every playbook earns its place", and there is a USD cap. Assumption: mutating one playbook's wording and scoring it with the slop detector plus a critic panel gives a usable signal.
  Done when: `fm bench breed ui/design-direction --budget 5` writes a Pareto set of variants. The winner beats the current playbook on at least 3 of 5 held-out briefs and nothing is merged without a human `accept`.

- **Extract a Motion Score from a screen recording (wild)** — FEATURE — value 4 — effort L — risk high — category: motion
  Why: Wild. Reference-to-tokens ideas cover screenshots only, and the "feel" the user wants is in the timing. Assumption: ffmpeg is optional and frame-differencing finds element timings well enough.
  Done when: given a 10-second clip of a known CSS animation, the extracted durations and easing land within 15% of the source. The result is written as a Motion Score file that the motion playbook consumes.

- **Spike before any L-size feature** — FEATURE — value 3 — effort M — risk low — category: process
  Why: Many tasks sit deferred as "Later from T-07xx" and L-size items such as T-0034 and T-1207 are blocked or deferred. A 20-minute spike with a measured result would show which are worth building. Assumption: a throwaway worktree plus a one-page result fits the existing task flow.
  Done when: `fm task spike T-NNNN` creates a time-boxed branch and ends with a result card of measured numbers. Closing an L feature without a spike card or an explicit waiver is refused.

- **Write deliverable playbooks for decks, reports and spreadsheet models** — FEATURE — value 3 — effort M — risk low — category: playbooks
  Why: `fm check office` is in the queue, but nothing teaches Claude to build a good xlsx or docx. Assumption: users hand Foreman non-code deliverables too.
  Done when: three playbooks each name an `fm check office` assertion set. A fixture task built by following each playbook passes the check, and a flawed copy fails it.

- **Bring `fm code app` to macOS and Windows** — FEATURE — value 3 — effort L — risk med — category: platform
  Why: The pack shows Linux-only evidence (a libappindicator blocker, Arch commands, an `/run/user` path). Assumption: wider users matter for "fully featured" and ConPTY plus VT enabling is stdlib-reachable.
  Done when: CI runs the golden-frame suite on macOS and Windows runners. `fm code app` starts, resizes and exits cleanly on both, with config paths resolved per OS.

- **Let panels be springy bodies you drag into layout (wild)** — FEATURE — value 3 — effort M — risk med — category: TUI config
  Why: Wild. The request wants config inside the TUI, and hand-edited TOML is the pain. Dragging a panel border with the mouse stretches its neighbours on damped springs. Releasing snaps to a grid and writes the layout to `tui.toml`.
  Done when: a scripted mouse drag in a pty test changes the layout and the saved `tui.toml` reproduces the same frame on reload. Under reduced motion the change is instant.
