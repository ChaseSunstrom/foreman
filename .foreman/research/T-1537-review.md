**Verdict: changes needed.** The acceptance criteria are met. The three named features that were not built are the main gap, and the ledger can be flooded. I did not run the tests; I judged from the code and the recorded evidence.

## lens: intent
- MEDIUM — T-1537 task brief, Steps and Non-goals — "roll looks while idle", "bisect taste across history" and "a style séance" are in the request but not built. They are not under Non-goals and "Follow-ups captured" is empty — build them, or capture them as tasks and list them as Non-goals — high
- MEDIUM — plugin/lib/fmtaste.py:76 — `kept` and `reverted` are only manual verbs. Nothing watches DESIGN.md, so a real revert never reaches the ledger unless the model remembers to run `fm looks revert` — name this in the docs, or add a hook note — medium
- LOW — plugin/skills/directions/SKILL.md:23-25 — "never one below 0" contradicts the skill's four-option menu once a few looks are negative — "else the least negative"

## lens: adversary
- MEDIUM — plugin/lib/fmtaste.py:174 (`pick`) — modified arrows or Home send escape sequences that contain digits. `"\x1b[1;2A"` records `a` then `b`, and `"\x1b[1~"` records `a`, so the docstring's claim is wrong — drain the escape sequence after Esc, and add a test
- LOW — plugin/lib/fmtaste.py:201 — `os.open` follows symlinks, so a named link reads its target. It is not a folder or a URL, and only votes and the link's name are kept — add `O_NOFOLLOW`, or record this as a decision
- LOW — plugin/commands/looks.md:45 — `--why "<their words>"` sits in double quotes, so `$(…)` expands. settings.md guards its paste with a regex — use single quotes and refuse a quote character
- LOW — plugin/commands/looks.md and plugin/skills/directions/SKILL.md:25 — the full-autonomy rule is prose only, and the test checks only that `fm looks` appears. `fm looks keep` or `calibrate --answers` run by the model cannot be told from the user's — assert the "Record nothing" sentence in the test, and say "AskUserQuestion denied → record nothing" in the command

## lens: edge
- MEDIUM — plugin/lib/fmtaste.py:14,16,287 — each learned file adds +1, with no dedupe. `fm looks learn *.css` over 50 files gives one look +50 against kept +3. Repeat runs add up, and `EVENTS_KEEP=500` then drops kept, reverted and calibration events first — count at most one `learned` per file name and look, and cap its total (for example at 3 per look)
- LOW — plugin/lib/fmtaste.py:65-73 — a corrupt or unexpected-shape ledger is silently wiped on the next write — write a `.bak` first
- LOW — plugin/lib/fmtaste.py:251 — `learn` exits 0 when every file was skipped, so scripts cannot tell

## lens: maintainer
- MEDIUM — plugin/tests/test_taste_ledger.py:762 — only the no-Pillow branch is tested. `_image_colours` (fmtaste.py:217-230) and the 40-megapixel bomb check have no test — add a stdlib-built PNG that declares 10000×10000, under `skipUnless(PIL)`
- LOW — CHANGELOG.md — it is in the task's scope but not in the diff

## lens: design (fm code app)
- LOW — plugin/lib/fmcodetui.py:1908 — an answer cannot be undone (only Esc, which loses everything). Enter on the default highlight silently records A. The rows are text only, with no palette swatch — add Backspace to go back, and start with no row highlighted

## Acceptance criteria
- A kept and a reverted look update the ledger: met (Ledger test).
- The picker records 12 answers: met (CLI and app tests).
- Nothing reads a file the user did not name: met (the `Opens` test: only the named page was read, the linked stylesheet was not).

## Judged
- Named files only: URLs, folders, FIFOs and devices are refused. The cap is 8 MiB, with `LEARN_MAX` 50.
- Decompression bomb: handled by the 40-megapixel check before decoding. It is untested.
- Pillow is detected and never installed.
- Ledger: written through `fmcore.lock` and `write_atomic`, and only the file's basename is kept.
- `/foreman:looks` is user-only. Under full autonomy nothing is recorded, but only by prose.
- fm code: Esc and q stop with nothing kept, and L opens the picker only from the main screen.
- fmcodetui.py merge with T-1543: no textual conflict is expected. Its edits are at lines ~1581, 1725, 2037-2100, 2580 and 2810-2852, while ours are at 101, 1130, 1146, 1459, 1591, 1645 and ~1888. The nearest pair is `self.tui = None` (line 1581) against the commands dict (line 1589), 7 lines apart.

## Implicit decisions
- `n` (neither) gives both looks −1.
- The ledger is global, not per project.
- Calibration pairs repeat after 5 rounds.
- Plain RGB distance of 48 for colour matching.

## Not checked
- Running the tests.
- The `fm help` width test.
- Rendering of the picker.
- Whether AskUserQuestion is auto-answered under full autonomy.

Noticed: `fm looks lido` fails with a confusing argparse "invalid choice" error (plugin/lib/fmcli.py:63).
