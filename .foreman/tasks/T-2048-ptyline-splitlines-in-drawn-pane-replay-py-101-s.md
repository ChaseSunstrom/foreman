---
id: T-2048
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T20:24:10Z
updated: 2026-10-29T23:25:58Z
base: e6c9c4bf4e3f200c4aca8d93c8b64fae662a6f43
base_tree: ac3d3e9eecff1cf1e45568dbe287accdeba9b1fa
plan0_at: 2026-10-29T23:20:44Z
plan0_scope: []
verified: strong
---
# Pane replay SVG keeps a title with U+2028 on its row
## Raw request
> ptyline.splitlines()` in `drawn()` (pane_replay.py:101) splits on U+0085 and U+2028/2029, which JSON.stringify leaves raw. A title containing one would truncate the captured tree line
> (noticed by an agent; research T-1670-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] svg() splits frames only on newlines — verify with `cd plugin/tests && python3 -m unittest test_ui_replay.Frames.test_a_line_separator_in_a_title_stays_on_its_row`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] split on newline
## Resume here
<!-- auto -->
- 2026-10-29T23:20:51Z step 1/2: failing test
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_ui_replay.Frames.test_a_line_separator_in_a_title_stays_on_its_row` → ✗ exit 1 · Ran 1 test in 0.003s / FAILED (failures=1) [ran] [tree 86603725d383] (2026-10-29T23:22:07Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_ui_replay` → exit 0 · Ran 21 tests in 1.022s / OK [ran] [tree 3076ff7e11d1] (2026-10-29T23:22:14Z)
- `cd plugin/tests && python3 -m unittest test_ui_replay.Frames.test_a_line_separator_in_a_title_stays_on_its_row` → ✗ exit 1 · Ran 1 test in 0.007s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 3076ff7e11d1] (2026-10-29T23:22:14Z)
- `cd plugin/tests && python3 -m unittest test_ui_replay.Frames.test_a_line_separator_in_a_title_stays_on_its_row` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree 3076ff7e11d1] (2026-10-29T23:22:14Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 23:20 UTC; claude plugin test mods/foreman-ui → [ran] [tree f98ed591e075] (2026-10-29T23:25:29Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_ui_replay.Frames.test_a_line_separator_in_a_title_stays_on_its_row` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree f98ed591e075] (2026-10-29T23:25:39Z)
- (audit intent) `self-review of the one-line diff: svg() now splits frames on \n only, matching drawn() since T-1670; swept mods/foreman-ui/tools for other splitlines calls` → a title holding U+2028 renders as one SVG text row; the new test pins it [tree f98ed591e075] (2026-10-29T23:25:39Z)
- (audit adversary) `self-review of the one-line diff: svg() now splits frames on \n only, matching drawn() since T-1670; swept mods/foreman-ui/tools for other splitlines calls` → the frame text is escaped as before; only the row split changed, no new input path [tree f98ed591e075] (2026-10-29T23:25:39Z)
- (audit edge) `self-review of the one-line diff: svg() now splits frames on \n only, matching drawn() since T-1670; swept mods/foreman-ui/tools for other splitlines calls` → \r is not stripped here, but drawn() already strips it before frames reach svg(); empty rows still skipped by ln.strip() [tree f98ed591e075] (2026-10-29T23:25:39Z)
- (audit operator) `self-review of the one-line diff: svg() now splits frames on \n only, matching drawn() since T-1670; swept mods/foreman-ui/tools for other splitlines calls` → no behaviour change for ordinary frames: test_ui_replay 21/21 and the golden frame pass [tree f98ed591e075] (2026-10-29T23:25:39Z)
- (audit maintainer) `self-review of the one-line diff: svg() now splits frames on \n only, matching drawn() since T-1670; swept mods/foreman-ui/tools for other splitlines calls` → comment names T-2048 at the split; the golden diff at line 355 splits both sides alike, so it stays [tree f98ed591e075] (2026-10-29T23:25:39Z)
- (audit self) `self-review of the one-line diff: svg() now splits frames on \n only, matching drawn() since T-1670; swept mods/foreman-ui/tools for other splitlines calls` → no findings [tree f98ed591e075] (2026-10-29T23:25:39Z)
## Log
- 2026-10-29T20:24:10Z created
- 2026-10-29T23:20:43Z planned from capture
- 2026-10-29T23:20:43Z focused
- 2026-10-29T23:22:04Z criterion 1 verify: `cd plugin/tests && python3 -m unittest test_ui_replay.UiReplayTools.test_a_line_separator_in_a_title_stays_on_its_row` → `cd plugin/tests && python3 -m unittest test_ui_replay.Frames.test_a_line_separator_in_a_title_stays_on_its_row`
- 2026-10-29T23:25:57Z done
- 2026-10-29T23:25:58Z committed ac5d8565 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1670-review: Verdict:** changes needed. The fixes are small, and I found no HIGH findings. [stale: mods/foreman-ui/tools/pane_replay.py, plugin/tests/test_ui_…
- T-1670 [FEATURE M, done, 4 steps] Pane replay follow-ups (T-1534): replay beside the task timeline in fm page, SVG/PNG outpu — lesson: a golden tool must bootstrap itsel…
- research T-1534-review: Verdict:** changes needed (one MEDIUM, easy to fix). The data-not-code question comes out clean. [stale: plugin/tests/test_ui_replay.py changed s…
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
- similar past tasks were M: consider --tier M
## Why not caught
T-1670 fixed drawn() but svg() kept splitlines; no test fed a line separator to svg()
## Lessons
- Fixing one splitlines call means grepping the same file for its siblings; T-1670 fixed drawn() and left svg()
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_ui_replay.py
- mods/foreman-ui/tools/pane_replay.py
- CHANGELOG.md
