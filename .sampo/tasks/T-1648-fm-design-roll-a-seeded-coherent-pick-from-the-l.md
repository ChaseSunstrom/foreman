---
id: T-1648
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_looks_gallery.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:58:23Z
updated: 2026-10-23T02:40:42Z
base: 1f2da113b6dbfc9d01b98903e821cd198209fa7f
base_tree: 4b4608d8fdac2f628f318ce4537cf1275b4bb555
plan0_at: 2026-10-23T02:08:26Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_looks_gallery.py, CHANGELOG.md]
verified: strong
---
# fm design roll: a seeded, coherent pick from the look cards, applied as one reversible patch
## Raw request
> fm design roll: a seeded, coherent pick from the look cards, applied as one reversible patch
## Interpretation
fm design roll [--seed N] [--apply] picks a coherent look from the look cards (plugin/skills/library/cards/looks: palette, type, motion and texture that belong together), deterministic for a seed; --apply writes it into DESIGN.md as one patch with an undo file, and fm design roll --undo restores the exact bytes.
## Assumptions (confidence)
## Acceptance criteria
- [x] the same seed gives the same look; applying then undoing restores DESIGN.md byte for byte — verify with `python3 plugin/tests/run.py test_looks_gallery.Roll`
## Non-goals
## Approach (options → choice → why)
Options: random mixing of tokens (incoherent); picking a whole card (coherent, few options); seeded picks within a card's allowed variations. Choice: seeded picks within a card: varied but coherent, reproducible, and reversible.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] card front-matter reader
3. [x] patch plus undo file
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_looks_gallery.Roll` → ✗ exit 1 · Ran 4 tests in 2.7s (1 classes, 16 at a time; slowest: Roll 1s) / FAILED (1 classes) [ran] [tree d98cf5c3ac79] (2026-10-23T02:10:27Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery.Roll 2>&1 | tail -30` → exit 0 · Ran 4 tests in 17.4s (1 classes, 16 at a time; slowest: Roll 17s) / OK [ran] [tree 1b9e5b51e0d3] (2026-10-23T02:12:24Z)
- (step 2) `python3 plugin/tests/run.py test_looks_gallery` → exit 0 · Ran 9 tests in 14.0s (2 classes, 16 at a time; slowest: Roll 13s, Gallery 8s) / OK [ran] [tree 6ed19feea313] (2026-10-23T02:13:34Z)
- (step 3) `python3 plugin/tests/run.py test_looks_gallery.Roll` → exit 0 · Ran 4 tests in 14.4s (1 classes, 16 at a time; slowest: Roll 13s) / OK [ran] [tree 6ed19feea313] (2026-10-23T02:13:51Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery.Roll 2>&1 | grep -E "^(FAIL|ERROR)|Error|assert" | head -20` → ✗ exit 1 · FAILED (failures=2) / FAILED (1 classes) [ran] [tree 0fc5e01a1da9] (2026-10-23T02:25:22Z)
- (step 3) `python3 plugin/tests/run.py test_looks_gallery.Roll` → ✗ exit 1 · Ran 7 tests in 7.6s (1 classes, 16 at a time; slowest: Roll 7s) / FAILED (1 classes) [ran] [tree 0fc5e01a1da9] (2026-10-23T02:25:32Z)
- (step 3) `python3 plugin/tests/run.py test_looks_gallery.Roll` → exit 0 · Ran 7 tests in 5.8s (1 classes, 16 at a time; slowest: Roll 5s) / OK [ran] [tree b6ca91092173] (2026-10-23T02:27:02Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery.Roll` → exit 0 · Ran 7 tests in 6.9s (1 classes, 16 at a time; slowest: Roll 7s) / OK [ran] [tree fcce3a810dc1] (2026-10-23T02:39:59Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery.Roll` → exit 0 · Ran 7 tests in 3.7s (1 classes, 16 at a time; slowest: Roll 3s) / OK [ran] [tree fcce3a810dc1] (2026-10-23T02:40:10Z)
- (audit intent) `fm-reviewer pass (shared with T-1639); MEDIUM fixed test-first: a failed write restores the prior undo record, a half-done roll counts as the same run so the original bytes survive (failed-write + crash tests); LOWs: before read inside write_section's design-md lock (keep=), a plain .orig beside the JSON, a golden seed→card test, card name written beside the seed` → fm design roll picks one look card by seed (palette, a non-generic lead face, motion), writes DESIGN.md's ## Look, and --undo restores the file byte for byte [tree fcce3a810dc1] (2026-10-23T02:40:10Z)
- (audit adversary) `fm-reviewer pass (shared with T-1639); MEDIUM fixed test-first: a failed write restores the prior undo record, a half-done roll counts as the same run so the original bytes survive (failed-write + crash tests); LOWs: before read inside write_section's design-md lock (keep=), a plain .orig beside the JSON, a golden seed→card test, card name written beside the seed` → a symlinked DESIGN.md, non-UTF-8 and oversized files refused before any write; the read happens under the same lock as the write [tree fcce3a810dc1] (2026-10-23T02:40:10Z)
- (audit edge) `fm-reviewer pass (shared with T-1639); MEDIUM fixed test-first: a failed write restores the prior undo record, a half-done roll counts as the same run so the original bytes survive (failed-write + crash tests); LOWs: before read inside write_section's design-md lock (keep=), a plain .orig beside the JSON, a golden seed→card test, card name written beside the seed` → a failed or crashed roll never loses the original bytes; a roll on a missing file undoes by deleting it [tree fcce3a810dc1] (2026-10-23T02:40:10Z)
- (audit design) `fm-reviewer pass (shared with T-1639); MEDIUM fixed test-first: a failed write restores the prior undo record, a half-done roll counts as the same run so the original bytes survive (failed-write + crash tests); LOWs: before read inside write_section's design-md lock (keep=), a plain .orig beside the JSON, a golden seed→card test, card name written beside the seed` → generic faces (Inter, Roboto, Arial…) never lead a stack; one card owns palette, type and motion [tree fcce3a810dc1] (2026-10-23T02:40:10Z)
## Log
- 2026-10-22T20:58:23Z created
- 2026-10-22T20:58:24Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_looks_gallery.py', 'CHANGELOG.md']
- 2026-10-22T20:58:25Z split from T-1539 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:58Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_looks_gallery.Roll`
- 2026-10-22T21:30:21Z criterion 1 text: the same seed gives the same look; applying then undoing restores DESIGN.md byte for byte — verify with python3 plugin/tests/run.py test_looks_gallery.Roll → the same seed gives the same look; applying then undoing restores DESIGN.md byte for byte
- 2026-10-23T02:08:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1648.builder.md
- 2026-10-23T02:08:26Z focused
- 2026-10-23T02:39:10Z merged worktree-agent-a73bea39aa37a5a51 (6 file(s))
- 2026-10-23T02:39:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a73bea39aa37a5a51
- 2026-10-23T02:39:51Z focused
- 2026-10-23T02:40:06Z scope: plugin/lib/fmroll.py (own module, keeps fmcli/fmdesign edits small) and MASTER.md
- 2026-10-23T02:40:42Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1498 [FEATURE M, done, 2 steps] Style shelf: twelve original named looks as library cards — lesson: Name taste cards with a prefix (look-) so a single everyday word in…
- T-1539 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second po
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/tests/test_looks_gallery.py; re-ground the plan against them before editing
## Lessons
- An undo record must be written as one step with the change, or restored when the change fails; a half-written record is the bug
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_looks_gallery.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- plugin/lib/fmroll.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmshot.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/fixtures/design-surfaces/DESIGN.md
- plugin/tests/test_design_gates.py
- plugin/tests/test_design_surfaces.py
- plugin/tests/test_doctor.py
- plugin/tests/test_fmshot.py
- plugin/tests/test_design_tokens.py
- plugin/tests/test_docs.py
