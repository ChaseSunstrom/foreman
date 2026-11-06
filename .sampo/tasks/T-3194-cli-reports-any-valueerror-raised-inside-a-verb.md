---
id: T-3194
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T11:01:22Z
updated: 2026-11-05T11:32:14Z
base: 738524a9c4ac31577c74e91d10937fd038be7a6a
base_tree: 08df4c345a1890516547bbcf4fe9dbb705f29265
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T11:26:53Z
plan0_scope: []
verified: strong
---
# Cli reports any ValueError raised inside a verb as 'state looks corrupt … sampo fsck',…
## Raw request
> cli reports any ValueError raised inside a verb as 'state looks corrupt … sampo fsck', sending the user to repair state that isn't broken (seen with an ElementTree serialisation error in works); only state-load errors should say that
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a ValueError inside a verb that isn't a parse error prints 'fm: <verb> failed: ValueError: …' with no corrupt-state claim, exits 1 and names one Next; CorruptState, JSONDecodeError and UnicodeDecodeError keep the corrupt-state line and exit 4 — verify with `python3 plugin/tests/run.py test_exit_next`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a plain ValueError is not reported as corrupt state
2. [x] narrow cli.py's ValueError handler to parse errors
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exit_next` → ✗ exit 1 · Ran 7 tests in 1.4s (1 classes, 16 at a time; slowest: ExitNext 0s) / FAILED (1 classes: test_exit_next.ExitNext) [ran] [tree 8c19412c18bc] [world 2f1906870a] (2026-11-05T11:27:08Z)
- (step 2) `python3 plugin/tests/run.py test_exit_next test_drill test_task_bulk` → exit 0 · Ran 24 tests in 36.2s (6 classes, 16 at a time; slowest: Drill 35s, Bulk 16s, StateErrors 5s) / OK [ran] [tree cc5d1a05e454] [world 2f1906870a] (2026-11-05T11:28:02Z)
- `test_exit_next` → ✗ exit 127 · bash: line 1: test_exit_next: command not found (start tree + this task's tests) [ran] [tree 774a3d633254] [world 2f1906870a] (2026-11-05T11:28:24Z)
- `test_exit_next` → ✗ exit 127 · bash: line 1: test_exit_next: command not found [ran] [tree 774a3d633254] [world 2f1906870a] (2026-11-05T11:28:24Z)
- `python3 plugin/tests/run.py test_exit_next` → ✗ exit 1 · Ran 7 tests in 3.5s (1 classes, 16 at a time; slowest: ExitNext 0s) / FAILED (1 classes: test_exit_next.ExitNext) (start tree + this task's tests) [ran] [tree 774a3d633254] [world 2f1906870a] (2026-11-05T11:28:33Z)
- `python3 plugin/tests/run.py test_exit_next` → exit 0 · Ran 7 tests in 0.8s (1 classes, 16 at a time; slowest: ExitNext 0s) / OK [ran] [tree 774a3d633254] [world 2f1906870a] (2026-11-05T11:28:33Z)
- (step 2) `python3 plugin/tests/run.py test_exit_next test_drill test_task_bulk test_cost_forecast test_portability test_ledger_index test_core test_unattended test_lanes` → exit 0 · Ran 379 tests in 82.6s (57 classes, 16 at a time; slowest: Lanes 82s, LaneRecovery 60s, Unattended 41s) / OK [ran] [tree f4fa30f77285] [world 2f1906870a] (2026-11-05T11:30:31Z)
- (ac 1) `python3 plugin/tests/run.py test_exit_next` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: ExitNext 0s) / OK [ran] [tree f4fa30f77285] [world 2f1906870a] (2026-11-05T11:30:45Z)
- (audit edge) `self: read every raise ValueError in core.py; brief frontmatter errors are state and now raise CorruptState (a ValueError subclass, so callers that catch ValueError are unchanged); argument ValueErrors (audit lens, rule pattern, --revisit) now say '<verb> failed' and point at --help instead of fsck` → JSONDecodeError and UnicodeDecodeError keep exit 4 and the fsck Next; a plain ValueError exits 1 with one Next line (T-2653 contract held: test_exit_next asserts exactly one); meta.json and brief parse failures are CorruptState, so a truly corrupt state still reaches fsck [tree f4fa30f77285] (2026-11-05T11:30:45Z)
- (audit self) `self: read every raise ValueError in core.py; brief frontmatter errors are state and now raise CorruptState (a ValueError subclass, so callers that catch ValueError are unchanged); argument ValueErrors (audit lens, rule pattern, --revisit) now say '<verb> failed' and point at --help instead of fsck` → no findings [tree f4fa30f77285] (2026-11-05T11:30:45Z)
## Log
- 2026-11-05T11:01:22Z created
- 2026-11-05T11:26:42Z planned: it has criteria and steps
- 2026-11-05T11:26:52Z focused
- 2026-11-05T11:26:53Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T11:32:10Z done
- 2026-11-05T11:32:14Z committed ac225cad (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-1667 [FEATURE M, done, 3 steps] fm fsck: a read-only report of broken worktrees, stale locks and torn journals, --fix for the safe repairs — lesson: A dead-pid check i…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-11-03: [outward] [revisited: Kirjokansi fused with Ilmarinen's forge] [cites: user steer 2026-11-03: super improve the fuse completely, combined/animated l…
## Lessons
- A catch-all ValueError handler names one cause for every subclass; map the cause by type (parse errors, the module's own CorruptState) and give the rest a neutral line
## Plan gaps
- failed first: step 1 failing test: a plain ValueError is not reported as corrupt state
## Files touched
- plugin/tests/test_exit_next.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- plugin/lib/sampo/core.py
