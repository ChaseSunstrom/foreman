# Brainstorm — lens: reliability

- **Make every check answer pass, fail or unable** — FIX — value 5 — effort M — risk low — category: verification
  Why: `fm shot`, `fm check ui`/`design`, the WebGL survival contract and the browser ladder all depend on a browser or GPU that may be absent. assumption: today a missing dependency can read as a skip or a pass.
  Done when: with the browser removed, `fm check ui` exits with a distinct "unable" status. A UI task cannot close on "unable" unless the user signs it off, and a test covers this.

- **Run each checker against a known-bad zoo every release** — FEATURE — value 5 — effort M — risk low — category: gate integrity
  Why: many new gates are proposed (slop detector, layout, a11y, motion lint, contrast). Only the slop detector has a precision corpus. A checker that quietly stops flagging is the worst failure. (wild-adjacent: it self-tests the gates.)
  Done when: `fm check --selftest` feeds 10+ deliberately broken pages, frames and configs to every checker. A checker that passes any of them fails the release.

- **Keep one ratchet ledger with a raise protocol** — CLEAN — value 4 — effort M — risk low — category: governance
  Why: the ideas propose ratchets for lines, tokens, `--help` length, swallowed errors, TUI cost and skill descriptions. Scattered one-way ratchets eventually wedge a legitimate change.
  Done when: all ratchets live in one file with owner, current value and reason. Raising one needs a recorded justification and expires after N releases. `fm doctor` lists ratchets that are about to bind.

- **Probe real glyph widths with a cursor-position query** — FEATURE — value 4 — effort M — risk med — category: TUI correctness
  Why: T-1468 shows `len()` padding broke on wide glyphs. A static width table still disagrees with some terminals on emoji and ambiguous-width characters. assumption: the terminal answers the CPR query.
  Done when: at launch, a timed broker prints each ambiguous glyph class and reads back the cursor column. Results are cached per `$TERM` and terminal. A test with a fake terminal that lies about widths shows layout following the probe.

- **Calibrate each visual baseline's noise floor** — FEATURE — value 4 — effort M — risk low — category: visual regression
  Why: the golden-frame, `fm shot` and baseline-inbox ideas all need a diff tolerance. A fixed threshold is either flaky or blind.
  Done when: approving a baseline renders it N times. The measured max jitter becomes that baseline's tolerance. A one-pixel shift of real content still fails, and re-rendering on a loaded machine does not.

- **Fail `fm shot` on a fallback font** — FIX — value 4 — effort S — risk low — category: visual proof
  Why: a proof screenshot taken before webfonts load, or with a missing face, looks plausible but is wrong. The site now self-hosts fonts (S24), so a mismatch is detectable.
  Done when: `fm shot` waits for `document.fonts.ready` and compares used faces to the declared tokens. A test page with a broken font URL fails with the face named.

- **Run a weekly scaffold bit-rot canary with latest dependencies** — FEATURE — value 4 — effort M — risk low — category: templates
  Why: 3D, shader and web scaffolds pin versions. Upstream three.js, R3F and Tailwind drift, and templates rot silently between releases. assumption: lockfiles ship with the templates.
  Done when: a scheduled job builds and smoke-tests each template against unpinned latest. Breakage files a task naming the dependency and version.

- **Lint that every atomic write syncs the file and its directory** — SECURITY — value 3 — effort S — risk low — category: durability
  Why: atomic settings, last-good copies and journals are proposed repeatedly. A rename without fsync of the file and directory can still lose the file on power loss.
  Done when: one `atomic_write()` helper is the only allowed writer, with a lint to enforce it. A fault-injecting `os` shim shows the old or new content survives a kill at every step.

- **Promote new gates from advisory to blocking by measured false-positive rate** — FEATURE — value 4 — effort M — risk low — category: gate rollout
  Why: the design, a11y, motion and layout gates risk blocking real work on opinion. T-0828 mentions shadow mode only for compact output.
  Done when: a new gate starts advisory and logs would-block events. It becomes blocking only after N runs at under X% overridden, and a demotion rule reverses it. The status shows the rate.

- **Register every seed in generative visuals and lint unseeded randomness** — FIX — value 3 — effort S — risk low — category: determinism
  Why: noise fields, particles, reaction-diffusion and shader recipes feed screenshots, goldens and demos. Unseeded randomness makes proofs unreproducible.
  Done when: recipes take a seed from one registry. A lint rejects `Math.random` and `random.random()` in recipe code, and two renders with the same seed are byte-identical.

- **Wild: Run a twin-run determinism diff** — CLEAN — value 4 — effort S — risk low — category: determinism
  Why: assumption: dict-order, hash-seed and thread-timing leaks cause the flaky canaries that keep getting dropped (T-1380, T-1435).
  Done when: CI replays one recorded event log twice with different `PYTHONHASHSEED` and `TZ`. Any frame-byte difference fails with the first differing frame.

- **Wild: Run `fm drill` for compound fault days** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: faults are proposed one at a time (full disk, clock jump, resize storm, SIGSTOP, stale login). Real failures compound.
  Done when: `fm drill --seed N` replays a run while injecting 3+ random overlapping faults. The terminal ends restored, the journal resumes, and the same seed reproduces any failure.

- **Wild: Add a locale and environment matrix to golden frames** — FIX — value 3 — effort M — risk low — category: portability
  Why: assumption: goldens are recorded only under the developer's locale. Turkish-i casing, RTL text, `LANG=C` and CJK width would differ.
  Done when: each golden view renders under a matrix of `LANG`, `TZ`, `TERM` and `COLORTERM`. Any divergence is either an approved variant or a bug.

- **Wild: Replay old bug fixtures after every playbook edit** — FEATURE — value 3 — effort M — risk low — category: playbook regression
  Why: the pack proposes A/B playbook evals and ablation. A single edit can silently re-break a past failure the playbook once fixed.
  Done when: each playbook carries the past failure cases it fixed as eval fixtures. Editing a playbook reruns them, and a regression names the edit.
