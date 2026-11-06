**Verdict: changes needed.** The default gate failure (finding 1) and the untested exit-code fix (finding 2) block approval. The rest are nits.

## lens: intent
- HIGH — `plugin/lib/smoke_web.cjs:212-219` and `plugin/lib/fmsmoke.py:201` — The default `fm smoke`, which `fm check` runs as a gate, now fails when the start page moves under reduced motion or overflows at 360 or 768 px. Both go through `add()` into `defects`, so the run exits 1. Any live page fails this: a polling telemetry panel, a video, a canvas. The only way out is `fm smoke set off`, which drops every check. `plugin/lib/fmoutcomes.py:71` also counts a `smoke` event with defects against every task closed in the previous 7 days ("smoke failed after"). Fix: send the frame-matrix findings (reduce stillness, 360/768 overflow) to `notes` unless `--strict` is passed or `smoke.strict` is set in meta. Alternatively log them as `smoke_profile`. Foreman's own habit points this way: `fmsmoke.py:192` says a missing browser "isn't a product defect... don't block". Confidence: high.
- LOW — `plugin/lib/smoke_web.cjs:20,190,191` — The frames fix the clock at 2026-01-15, which is nine months before today (2026-10-22), on the user's real running app. Client-side token expiry or "in 3 days" logic can then show a login or expired screen in the frames. Fix: freeze the clock only under `frozen`, or add a note in the visual-qa doc. Confidence: medium.

## lens: edge
- MEDIUM — `plugin/lib/fmsmoke.py:171-173` — Each run now writes to `smoke/<commit>/<name>`, where runs used to get unique timestamped folders. Two concurrent runs on the same commit therefore share one folder. The second run's `rmtree` deletes the first run's shots, and the folders end up mixed. A `-dirty` folder is overwritten by every later dirty state, so a receipt pointing at it can change underneath you. Fix: lock per folder (`c.lock`) or add a run suffix. Confidence: medium (read from the code, not run).
- LOW — `plugin/lib/smoke_web.cjs:360-361` — The `offline` profile waits 3 s per view and `slow3g` stretches the settle time. A viewport that exceeds its share of the deadline then reports "the page stopped responding (no answer for 30 s)". That message is wrong and counts as a defect. With stuck spinners, `offline` costs about 8 s per view, so a viewport with 12 or more tabs overruns its 100 s share. Fix: report budget exhaustion as a note with its own text. Confidence: plausible.
- LOW — `plugin/lib/smoke_web.cjs:30` — `\w` is ASCII-only, so tab names in non-Latin scripts all become `desktop-tab`, `-2`, `-3`. Those names depend on order, so they are not stable. Fix: allow Unicode letters (`\p{L}\p{N}` with the `u` flag) or hash the name. Confidence: high. Names are safe from traversal: the slug strips separators, `_rev` strips `\W`, and profile names come from argparse `choices`.
- LOW — `plugin/lib/fmsmoke.py:174-177,192-193` — When profile 2 reports "skipped" after profile 1 succeeded, the skipped message replaces profile 1's printed defects, but the exit code is still 1. Fix: print `texts` before the skipped line. Confidence: high.
- LOW — `plugin/lib/fmsmoke.py:195` — Pruning keeps 5 commits with no byte cap. `--profile all` with `motion` writes 5 PNGs per view, and the full-page frames can be very tall. Fix: cap the frame height or total bytes. Confidence: low.

## lens: maintainer
- MEDIUM — `plugin/lib/fmsmoke.py:201` — The exit-code fix is correct: the old early return at the missing-Playwright path ignored `bad`. It has no test. `test_a_profile_without_a_browser_is_skipped_with_a_reason` has no failing cmd or http check, and no test in `test_smoke.py` uses `smoke set cmd` or `set http`. Fix: add a test with `set cmd "false"`, no Playwright, and an expected exit of 1. Confidence: high.
- LOW — `plugin/lib/fmsmoke.py:63-75` — No test covers the `_kill` timeout path, such as a stub runner that sleeps. Fix: add one using `FOREMAN_SMOKE_RUNNER`.

## Acceptance criteria
- Profile flags accepted, applied, and skipped with a reason when no browser: met. `test_smoke_profiles.py:194,220` and the harness tests cover it.
- Frame matrix with stable names: met in code (`MATRIX` test), with the dirty-folder and concurrency caveats above.

## Implicit decisions
- Profile defects exit 1 although the docs say profiles aren't a gate.
- Folders are named per commit, plus `-dirty`.
- The profile list is imported eagerly in `fmcli`.
- `slow3g` is the DevTools preset.
- The colour-vision matrices come from Machado et al., severity 1.

## Not checked
- I ran no browser or tests.
- I did not check Playwright's `route.fetch` behaviour on streaming responses (it may stall `fetch`-based SSE under `empty`).
- I did not check hydration under the colour-vision SVG.
- I did not read the `fm check` plumbing.

## Timeout cleanup (question 5)
The cleanup is correct as read. SIGTERM to the process group runs the script's handler, `process.exit(143)`, and Playwright's exit hook then kills Chromium, which has its own process group. Chromium has no stdio of its own to hold the pipes, so `communicate()` does not block.

**Noticed:** none beyond the above. One small point: `fm smoke --profile all` can run past a Bash tool timeout, since it runs up to 10 crawls of 240 s each, so the docs should say to background it.
