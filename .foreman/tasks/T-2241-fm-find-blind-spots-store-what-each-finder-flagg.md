---
id: T-2241
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:06:09Z
updated: 2026-10-31T02:35:15Z
inferred_deps: [T-2185]
inferred_why: T-2185: named in its request
base: fc8134c1f597091c06ca1637d5fbf397935de0a8
base_tree: fa0f47b49100bd53668529dde5a70c472942ee72
plan0_at: 2026-10-31T02:02:06Z
plan0_scope: []
verified: strong
---
# fm find blind spots: a closed FIX whose lines no finder flagged becomes a record and, at most once a day, a rule/tool/check task
## Raw request
> fm find blind spots: store what each finder flagged at capture time, map a closed FIX's lines to it, and file at most one rule/tool/check task a day for a miss (T-2185 rung e)
## Interpretation
T-2185 rung e. Recall only grows if misses are seen: a bug someone fixed that no finder flagged is the measured gap. Record it from data (what finders flagged vs the lines a FIX changed), never a hand list, and turn it into one improvement task a day so the queue isn't flooded.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find --capture and fm prove --capture save which lines each finder flagged per file (state find-flags.json, bounded); when a FIX task closes, its changed lines (git diff from its start point, its own files) that no saved flag sits within 3 lines of become a blind-spot record (state blindspots.jsonl: task, file, lines, finders that ran); fm find --blindspots lists them and files at most one 'fm find missed …: add a rule, tool or check' task a day; a finish never fails because of it — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots`
## Non-goals
## Approach (options → choice → why)
Options: (1) snapshot flags at capture, diff a closed FIX's hunks against them (chosen: cheap, local, no model; ±3 lines tolerance); (2) re-run fm find on the FIX's start tree at close (exact but slow, runs on every close); (3) ask a model whether a finder should have caught it (costly, untestable). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (FindBlindSpots): flags saved at capture; a FIX touching an unflagged line records a blind spot, a flagged one doesn't; one task a day; a broken state file never fails the finish
2. [x] save flags at capture; record at FIX close (fm task finish hook, best effort); fm find --blindspots
3. [x] docs (MASTER fmfind, CHANGELOG)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots 2>&1 | tail -8` → ✗ exit 1 · Ran 5 tests in 6.338s / FAILED (failures=3, errors=1) [ran] [tree 7705f0615c3f] (2026-10-31T02:03:31Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots 2>&1 | tail -20` → exit 0 · Ran 5 tests in 7.898s / OK [ran] [tree 5bcb8db66caa] (2026-10-31T02:04:12Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots 2>&1 | tail -20` → exit 0 · Ran 5 tests in 7.898s / OK [ran] [tree 5bcb8db66caa] (2026-10-31T02:04:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots 2>&1 | tail -30` → ✗ exit 1 · Ran 11 tests in 30.945s / FAILED (failures=3) [ran] [tree 5ced4addeac9] (2026-10-31T02:12:28Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots` → ✗ exit 1 · Ran 11 tests in 10.207s / FAILED (failures=4, errors=5) (start tree + this task's tests) [ran] [tree 4c0b26be16ff] (2026-10-31T02:31:05Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots` → exit 0 · Ran 11 tests in 16.357s / OK [ran] [tree 4c0b26be16ff] (2026-10-31T02:31:05Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find test_execution test_close_gates` → exit 0 · Ran 110 tests in 65.455s / OK [ran] [tree 4c0b26be16ff] (2026-10-31T02:32:37Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find test_execution test_close_gates` → exit 0 · Ran 110 tests in 71.268s / OK [ran] [tree 4c0b26be16ff] (2026-10-31T02:33:48Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find test_execution test_close_gates` → exit 0 · Ran 110 tests in 45.288s / OK [ran] [tree 4c0b26be16ff] (2026-10-31T02:34:34Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBlindSpots` → exit 0 · Ran 11 tests in 6.522s / OK [ran] [tree 4c0b26be16ff] (2026-10-31T02:34:41Z)
- (audit intent) `fm-reviewer five lenses on the branch: changes needed, fixed in 00af4b22: a filed record is marked and the newest unfiled one is picked (no daily refile of the same miss), flags carry each file's blob hash and a stale file is skipped, a capture replaces a file's flags, the hook builds its own guarded diff with --no-textconv, reads flags first and has a 10 s budget, a reopened FIX replaces its records, --relative and a TAB-safe name parse, per-file finders, '..' keys skipped, Filed 0 lines; test_find test_execution test_close_gates green; red-to-green proven` → a fix no finder flagged becomes a blind-spot record and at most one improvement task a day [tree 4c0b26be16ff] (2026-10-31T02:34:41Z)
- (audit adversary) `fm-reviewer five lenses on the branch: changes needed, fixed in 00af4b22: a filed record is marked and the newest unfiled one is picked (no daily refile of the same miss), flags carry each file's blob hash and a stale file is skipped, a capture replaces a file's flags, the hook builds its own guarded diff with --no-textconv, reads flags first and has a 10 s budget, a reopened FIX replaces its records, --relative and a TAB-safe name parse, per-file finders, '..' keys skipped, Filed 0 lines; test_find test_execution test_close_gates green; red-to-green proven` → every git call in the hook runs with fsmonitor and hooks off and --no-textconv; text is plain'd and defanged; nothing runs repo code [tree 4c0b26be16ff] (2026-10-31T02:34:41Z)
- (audit edge) `fm-reviewer five lenses on the branch: changes needed, fixed in 00af4b22: a filed record is marked and the newest unfiled one is picked (no daily refile of the same miss), flags carry each file's blob hash and a stale file is skipped, a capture replaces a file's flags, the hook builds its own guarded diff with --no-textconv, reads flags first and has a 10 s budget, a reopened FIX replaces its records, --relative and a TAB-safe name parse, per-file finders, '..' keys skipped, Filed 0 lines; test_find test_execution test_close_gates green; red-to-green proven` → stale flags, reopened FIXes, names with spaces, subdirectory roots (untested: noted), a corrupt state file [tree 4c0b26be16ff] (2026-10-31T02:34:41Z)
- (audit operator) `fm-reviewer five lenses on the branch: changes needed, fixed in 00af4b22: a filed record is marked and the newest unfiled one is picked (no daily refile of the same miss), flags carry each file's blob hash and a stale file is skipped, a capture replaces a file's flags, the hook builds its own guarded diff with --no-textconv, reads flags first and has a 10 s budget, a reopened FIX replaces its records, --relative and a TAB-safe name parse, per-file finders, '..' keys skipped, Filed 0 lines; test_find test_execution test_close_gates green; red-to-green proven` → no flags means no work at finish; the hook is budgeted and best-effort, never failing the close [tree 4c0b26be16ff] (2026-10-31T02:34:41Z)
- (audit maintainer) `fm-reviewer five lenses on the branch: changes needed, fixed in 00af4b22: a filed record is marked and the newest unfiled one is picked (no daily refile of the same miss), flags carry each file's blob hash and a stale file is skipped, a capture replaces a file's flags, the hook builds its own guarded diff with --no-textconv, reads flags first and has a 10 s budget, a reopened FIX replaces its records, --relative and a TAB-safe name parse, per-file finders, '..' keys skipped, Filed 0 lines; test_find test_execution test_close_gates green; red-to-green proven` → the hook reuses fmfind's _git helper and the finder OPEN_CAP [tree 4c0b26be16ff] (2026-10-31T02:34:41Z)
## Log
- 2026-10-31T00:06:09Z created
- 2026-10-31T02:01:41Z planned from capture
- 2026-10-31T02:01:41Z set approved=True
- 2026-10-31T02:01:42Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2241.builder.md
- 2026-10-31T02:02:06Z focused
- 2026-10-31T02:30:32Z merged worktree-agent-aa673c10b6a1b42dc (6 file(s))
- 2026-10-31T02:30:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa673c10b6a1b42dc
- 2026-10-31T02:30:37Z focused
- 2026-10-31T02:34:34Z scope: plugin/lib/fmfind.py (save_flags, blindspots), plugin/lib/fmcli.py (finish hook, --blindspots), plugin/lib/fmprove.py (save flags at capture), plugin/tests/test_find.py, MASTER.md, CHANGELOG.md
- 2026-10-31T02:35:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2185 [FEATURE L, planned, 7 steps] Initiative detection ladder (steer 2026-10-30 #4, capability #1): fm find stays the free…
- T-2076 [FEATURE M, done, 2 steps] Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next — l…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- the similar finished task took 2 steps
## Lessons
- A snapshot keyed by line numbers must carry the content hash it was taken from, or any later edit turns its absence into a false miss
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmprove.py
- plugin/lib/fmfind.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
