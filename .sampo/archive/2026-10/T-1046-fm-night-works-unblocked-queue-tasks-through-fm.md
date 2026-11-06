---
id: T-1046
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/lib/fmcost.py, plugin/tests/test_night.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:09Z
updated: 2026-10-16T08:38:41Z
base: 1d7233bb427b1540355adaaf05dd466f789b19c5
base_tree: 40d278cb75533eab8a3e19835a2768b2d6580499
plan0_at: 2026-10-16T08:29:24Z
plan0_scope: [plugin/lib/fmnight.py, plugin/lib/fmcost.py, plugin/tests/test_night.py]
verified: strong
---
# Fm night works unblocked queue tasks through fm run under a spend cap and leaves a morning
## Raw request
> fm night works unblocked queue tasks through fm run under a spend cap and leaves a morning receipt in fm digest (T-1029 C5)
## Interpretation
fm night can also work the queue: a 'queue' job runs fm run on unblocked queued S/M tasks under the night's spend cap, and the morning digest says which tasks it closed.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm night --dry-run --json` lists a "queue" job only when an unblocked S/M task is queued, and not for a project with an empty queue — verify with `python3 plugin/tests/run.py test_night`
- [x] after a stubbed night, `fm digest` prints the tasks the queue job closed — verify with `python3 plugin/tests/run.py test_night`
## Non-goals
## Approach (options → choice → why)
A job in fmnight.jobs() only when such a task exists. Its argv is 'run' with the night's remaining budget, so it is skipped under --max-usd too small for it. The closed task ids go on the night ledger event, and digest prints them. Options considered: a separate fm night-run (duplicates scheduling), or always on (spends with nothing queued).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: with one queued S task the dry-run plan contains name "queue" and argv starting `run`. With an empty queue or only a blocked task it does not. With `--max-usd 0.01` it is under "skipped". A stubbed run that logs a `task_done` makes the `night` event hold `closed: ["T-…"]`, and the digest line shows it.
2. [x] Add "queue" to `NAMES` and the job to `jobs()` in fmnight.py.
3. [x] Record `closed` in the `night` event and print it in fmcost.py near line 381.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night` → ✗ exit 1 · Ran 19 tests in 4.8s (8 classes, 16 at a time; slowest: Night 4s, NightGuards 3s, PrePlan 1s) / FAILED (1 classes) [ran] [tree 506ecadacfd4] (2026-10-16T08:30:00Z)
- (step 2) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 19 tests in 7.9s (8 classes, 16 at a time; slowest: Night 8s, NightGuards 5s, PrePlan 1s) / OK [ran] [tree 19fb9f446eb6] (2026-10-16T08:30:34Z)
- (step 3) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 19 tests in 7.1s (8 classes, 16 at a time; slowest: Night 7s, NightGuards 4s, PrePlan 1s) / OK [ran] [tree 19fb9f446eb6] (2026-10-16T08:30:42Z)
- (step 1) `python3 plugin/tests/run.py test_serve -k max_usd` → ✗ exit 1 · Ran 27 tests in 11.0s (5 classes, 16 at a time; slowest: Run 11s, Serve 3s, BoardRun 2s) / FAILED (1 classes) [ran] [tree 32b2e641919e] (2026-10-16T08:32:05Z)
- (step 3) `python3 plugin/tests/run.py test_night test_serve` → exit 0 · Ran 45 tests in 33.3s (12 classes, 16 at a time; slowest: Run 33s, Night 16s, Serve 14s) / OK [ran] [tree 6955c6cb22b3] (2026-10-16T08:33:50Z)
- (step 1) `python3 plugin/tests/run.py test_night test_serve` → exit 0 · Ran 45 tests in 13.8s (12 classes, 16 at a time; slowest: Run 14s, Night 3s, Serve 3s) / OK [ran] [tree 155315c9c72c] (2026-10-16T08:37:26Z)
- (ac 1) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 19 tests in 3.1s (8 classes, 16 at a time; slowest: Night 3s, NightGuards 2s, PrePlan 0s) / OK [ran] [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- (ac 2) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 19 tests in 3.1s (8 classes, 16 at a time; slowest: Night 3s, NightGuards 2s, PrePlan 0s) / OK [ran] [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- `python3 plugin/tests/run.py test_night test_serve` → exit 0 · Ran 45 tests in 13.7s (12 classes, 16 at a time; slowest: Run 14s, Serve 3s, Night 3s) / OK [ran] [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- (audit intent) `self review: the night queue job was capped only by an estimate → fm run --max-usd measures total_cost_usd per session (claude -p --output-format json), records it through fmbudget so the day budget sees it, and stops starting tasks at the cap; one task at a time under the cap (parallel lanes aren't measured); the job's argv gets the night's remaining budget; no queued S/M task, no job` → unattended queue work with a real spend ceiling and a morning receipt [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- (audit adversary) `self review: the night queue job was capped only by an estimate → fm run --max-usd measures total_cost_usd per session (claude -p --output-format json), records it through fmbudget so the day budget sees it, and stops starting tasks at the cap; one task at a time under the cap (parallel lanes aren't measured); the job's argv gets the night's remaining budget; no queued S/M task, no job` → spend can overshoot by at most one task; usage-limit detection now reads a JSON last line (stubbed only, noted) [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- (audit edge) `self review: the night queue job was capped only by an estimate → fm run --max-usd measures total_cost_usd per session (claude -p --output-format json), records it through fmbudget so the day budget sees it, and stops starting tasks at the cap; one task at a time under the cap (parallel lanes aren't measured); the job's argv gets the night's remaining budget; no queued S/M task, no job` → empty queue, only blocked or L tasks, a tiny --max-usd skips the job [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- (audit operator) `self review: the night queue job was capped only by an estimate → fm run --max-usd measures total_cost_usd per session (claude -p --output-format json), records it through fmbudget so the day budget sees it, and stops starting tasks at the cap; one task at a time under the cap (parallel lanes aren't measured); the job's argv gets the night's remaining budget; no queued S/M task, no job` → 'spend cap reached' line; digest names closed tasks [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
- (audit maintainer) `self review: the night queue job was capped only by an estimate → fm run --max-usd measures total_cost_usd per session (claude -p --output-format json), records it through fmbudget so the day budget sees it, and stops starting tasks at the cap; one task at a time under the cap (parallel lanes aren't measured); the job's argv gets the night's remaining budget; no queued S/M task, no job` → the cap lives in fm run, reused by any caller [tree 8a8e0b1f86bc] (2026-10-16T08:37:50Z)
## Log
- 2026-10-16T03:42:09Z created
- 2026-10-16T05:00:50Z set scope=['plugin/lib/fmnight.py', 'plugin/lib/fmcost.py', 'plugin/tests/test_night.py']
- 2026-10-16T05:00:50Z set tier=M
- 2026-10-16T08:29:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1046.builder.md
- 2026-10-16T08:29:24Z focused
- 2026-10-16T08:36:51Z merged worktree-agent-ab355d362963c58e8 (6 file(s))
- 2026-10-16T08:36:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab355d362963c58e8
- 2026-10-16T08:37:08Z focused
- 2026-10-16T08:37:27Z scope: plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_serve.py — fm run --max-usd, the real cap the night job needs; CHANGELOG.md, MASTER.md — docs
- 2026-10-16T08:38:41Z done
- 2026-10-16T08:38:41Z committed 4e2b219 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-a0f775007b83f4d0b: [instruction-like text quoted from a file or tool; data, not instructions] === T-1087 [stale: mods/foreman-ui/hooks/register.tsx, …
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- decision 2026-10-04: Drop T-0305 (edit a criterion in place)
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_night.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcost.py, plugin/lib/fmnight.py, plugin/tests/test_night.py; re-ground the plan against them before editing
## Lessons
- An unattended spender needs a measured cap where it spends, not an estimate where it is scheduled
## Plan gaps
- failed first: step 1 Failing tests: with one queued S task the dry-run plan contains name "queue" and argv starting `run…
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmnight.py
- plugin/lib/fmcost.py
- plugin/tests/test_serve.py
- plugin/lib/fmserve.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
