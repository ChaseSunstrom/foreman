---
id: T-1886
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-29T00:53:41Z
updated: 2026-10-29T01:15:54Z
base: 53c501087397f6f50e20464612138c126b0eb6c4
base_tree: 6c86fb3ee6bf4bbaf44c91a0dabf383b53afeaf7
plan0_at: 2026-10-29T01:05:06Z
plan0_scope: []
verified: strong
---
# A capture filled by fm task set, ac add or step add becomes planned, so the drive stops offering it for planning
## Raw request
> Stop-hook drive asks to plan inbox tasks whose briefs already have criteria and steps (T-1876, T-1881) while gates run on the tree; it should say 'all planned, gates running: wait for the notification' and let the turn end
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a captured task given criteria and steps by set/ac/step is planned; a status set by hand is kept — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] regression test: test_a_capture_given_criteria_and_steps_is_planned (red)
2. [x] _filled() in fmcli task_set, task ac add, task step add (green)
3. [x] docs: CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-10-29T01:14:02Z steps 3/3 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py
- touched since last checkpoint: plugin/tests/test_cli.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1889t.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1889i.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1888t.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1888i.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/apply.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake.test_a_capture_given_criteria_and_steps_is_planned` → red as expected (exit 1) · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / FAILED (1 classes) [ran] [tree c8d0e50bb1e0] (2026-10-29T01:05:13Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 125 tests in 39.5s (37 classes, 16 at a time; slowest: TaskLifecycle 39s, Checks 16s, AuditPrep 16s) / OK [ran] [tree 16629f29ba44] (2026-10-29T01:05:57Z)
- (step 3) `grep -q 'T-1886' CHANGELOG.md && grep -q 'T-1886' MASTER.md` → exit 0 · (no output) [ran] [tree c7718c6089a5] (2026-10-29T01:06:07Z)
- `python3 plugin/tests/run.py test_cli.CaptureAndIntake.test_a_capture_given_criteria_and_steps_is_planned` → ✗ exit 1 · Ran 1 tests in 2.6s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c7718c6089a5] (2026-10-29T01:06:17Z)
- `python3 plugin/tests/run.py test_cli.CaptureAndIntake.test_a_capture_given_criteria_and_steps_is_planned` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: CaptureAndIntake 2s) / OK [ran] [tree c7718c6089a5] (2026-10-29T01:06:17Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.9    44.8     150  [0] / SessionEnd                  36.3    40.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree c7718c6089a5] (2026-10-29T01:13:31Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 125 tests in 23.6s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, Checks 8s) / OK [ran] [tree c7718c6089a5] (2026-10-29T01:15:51Z)
- (audit intent) `S: lenses only; red→green test plus full gates` → a captured task filled by set/ac add/step add turns planned [tree c7718c6089a5] (2026-10-29T01:15:51Z)
- (audit adversary) `S: lenses only; red→green test plus full gates` → none — local brief state only [tree c7718c6089a5] (2026-10-29T01:15:51Z)
- (audit edge) `S: lenses only; red→green test plus full gates` → criteria alone stay captured; status=captured set by hand is kept [tree c7718c6089a5] (2026-10-29T01:15:51Z)
- (audit self) `S: lenses only; red→green test plus full gates` → no findings [tree c7718c6089a5] (2026-10-29T01:15:51Z)
## Log
- 2026-10-29T00:53:41Z created
- 2026-10-29T00:53:57Z cause: briefs filled with fm task set --section 'Acceptance criteria' stay status=captured, so the drive offers them for planning again; fm task set filling criteria+steps on a captured task could promote it to planned (as unblock does)
- 2026-10-29T01:00:51Z planned from capture
- 2026-10-29T01:05:06Z focused
- 2026-10-29T01:15:52Z done
- 2026-10-29T01:15:54Z committed b50f1dfe (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- T-1400 [FEATURE M, done, 1 steps] A standing mandate: a sweeping request becomes one record (its text, its clauses from fm c — lesson: parse_ts returns a datetime, not e…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- A status that follows from the brief's contents should be derived where the contents change, not left to the caller
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
