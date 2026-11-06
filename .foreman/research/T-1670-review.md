**Verdict:** changes needed. The fixes are small, and I found no HIGH findings.

## lens: intent
- MEDIUM — mods/foreman-ui/tools/pane_replay.py:91 — `golden --update` cannot bootstrap or recover. `drawn()` stages a copy whose `replay.test.tsx` imports `./fixtures/golden`. If `golden.ts` is missing, or holds merge-conflict markers (a one-line 30 KB file that every parallel pane change rewrites), the staged test fails to resolve or compile. That raises `RuntimeError` before the write at :92. The "none committed yet → written" branch (:92) is therefore unreachable, and `read_golden()` evaluated beside `drawn()` raises `JSONDecodeError` on a corrupt file even for `--update`. I did not run it, so the missing-import behaviour is inferred (PLAUSIBLE). — Fix: have `stage()` write a stub `golden.ts` into the copy, and under `--update` have `read_golden` treat a bad file as None. — medium
- LOW — mods/foreman-ui/tools/pane_replay.py:312 — With no golden committed, `golden` (without `--update`) writes the file and exits 0 printing "the pane draws it". That wrongly blesses a missing golden. — Fix: print "written" whenever it wrote, and exit 1 unless `--update`. — high

## lens: edge
- LOW — mods/foreman-ui/tools/pane_replay.py:119 — Only a lowercase `.png` triggers rsvg-convert. `--out x.PNG`, `.jpg` or `.pdf` silently gets SVG text. — Fix: `path.lower().endswith(".png")`, and reject other extensions. — high
- LOW — mods/foreman-ui/tools/pane_replay.py:125 — `check=True` with `capture_output` raises `CalledProcessError`, which `main` does not catch (:328 catches only ValueError, RuntimeError and TimeoutExpired). A malformed frame gives a traceback, and rsvg-convert's stderr is lost. — Fix: catch it and `sys.exit` with `e.stderr`. — medium

## lens: maintainer
- MEDIUM — mods/foreman-ui/tools/pane_replay.py:100 — The golden drift diff dumps both trees as indent=1 JSON. Raster cells are single-line base64, so a pane change prints whole 30 KB lines and not the text rows that moved. The existing `diff()` (:336) already prefers text frames and falls back to trees. — Fix: `return False, diff([("golden", old, text(json.loads(old), *GOLDEN_SIZE)), ("drawn now", line, text(json.loads(line), *GOLDEN_SIZE))])`. — high
- MEDIUM — plugin/tests/test_ui_replay.py:208-215 — The golden-wiring test greps the kit file for strings. It would pass if the comparison were broken, such as `toBe(GOLDEN)` against the wrong value. The real proof is the `claude plugin test mods/foreman-ui` gate, not the AC command. — Fix: name that gate in the test comment, or add a Run-style test that stages a modified golden and expects the kit to fail. — medium
- LOW — plugin/tests/test_ui_replay.py:181 — The PNG branch (rsvg-convert present or absent) has no test. — Fix: mock `shutil.which` and `subprocess.run`. — high

## Acceptance criteria
- The SVG writer, and `golden` compare and rewrite, are met. The unit tests in `test_ui_replay` exercise them with `drawn` mocked.
- PNG output is not verifiable: the rsvg-convert path is untested.
- "The mod's replay test fails when the pane drifts" is not verifiable from the named command. `test_ui_replay` never runs the kit, and the `toBe(GOLDEN)` at replay.test.tsx:73 only runs under `claude plugin test`.
- Files vs steps: CHANGELOG.md, MASTER.md, replay.test.tsx, pane_replay.py and test_ui_replay.py are named by no step. They are the feature itself, so I count it as plan bookkeeping and not scope creep.

## Implicit decisions
- The golden is the whole drawn-tree JSON string, stored as a `.ts` default export.
- The golden uses the synthetic `pane-busy` view at 80x40.
- The SVG uses a fixed 8.4 px cell, DejaVu Sans Mono, a dark ground and a single text colour (no pane colours).
- The first run auto-writes the golden.

## Not checked
- I did not run `claude plugin test` or rsvg-convert (read-only), so the golden's currency is unverified.
- `golden.ts` content is omitted from the diff.
- The other asked items (the fm page replay, the kit clock set to the view's time, forked-skill visual QA) are outside this diff. The request's remaining items, the clock and the visual QA, have no hunk here.
- CHANGELOG.md and MASTER.md: the two inserted lines look fine.

**Noticed:** `ptyline.splitlines()` in `drawn()` (pane_replay.py:101) splits on U+0085 and U+2028/2029, which JSON.stringify leaves raw. A title containing one would truncate the captured tree line.
