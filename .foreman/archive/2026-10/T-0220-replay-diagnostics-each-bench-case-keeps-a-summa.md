---
id: T-0220
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:59:37Z
updated: 2026-10-04T05:02:06Z
base: 64b3600c03a657a0b680b2d649928f52a319a525
base_tree: dce046da99fa661fb6081001aad0da43867ff4a4
verified: strong
---
# Replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (t
## Raw request
> FEATURE: replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (tasks made, steps, evidence runs, gates, guard blocks) and fm bench show LABEL prints it, so a failure can be pinned to a stage
> CONTEXT: plugin/lib/fmbench.py run_case keeps only pass/cost/turns; the replay's FOREMAN_STATE folder is deleted with the worktree
> CONTEXT: fmbench.py; /foreman:improve should require fm bench gate before proposing a merge
> CONTEXT: fmbench.build needs finished briefs today; commits with tests exist in every repo the user works on
> CONTEXT: fm run --models S=…,M=…,L=… is manual today (fmserve._models)
> CONTEXT: /foreman:improve is manual today; fm bench + gate are the referee; merging Foreman changes is always the user's call
> DONE-WHEN: a stubbed replay that writes Foreman events shows them summarized in its result and in fm bench show
> DONE-WHEN: tests show --runs 2 aggregates and fm bench gate passes an equal candidate and fails a worse one
> DONE-WHEN: a test repo's commit with a test and a fix becomes a valid case without any brief
> DONE-WHEN: a stubbed run where the cheap model passes recommends it and --save stores it
> DONE-WHEN: with stubbed claude, one evolve generation builds a candidate worktree with the proposed edit, benches both, and reports keep/drop from the gate
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a stubbed replay that makes a Foreman task and hits a guard block has both in its result's diag and in fm bench show — verify with `python3 plugin/tests/run.py -k test_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then _diagnose over the replay state before the worktree goes, and fm bench show
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 7 tests in 6.4s (1 classes, 16 at a time; slowest: Bench 6s) / OK [ran] [tree 92bdd7cf4014] (2026-10-04T05:01:03Z)
- `python3 plugin/tests/run.py -k test_bench` → ✗ exit 1 · Ran 7 tests in 6.4s (1 classes, 16 at a time; slowest: Bench 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 92bdd7cf4014] (2026-10-04T05:01:16Z)
- `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 7 tests in 6.3s (1 classes, 16 at a time; slowest: Bench 6s) / OK [ran] [tree 92bdd7cf4014] (2026-10-04T05:01:16Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 7 tests in 6.3s (1 classes, 16 at a time; slowest: Bench 6s) / OK [ran] [tree 92bdd7cf4014] (2026-10-04T05:02:06Z)
- (audit self) `self checklist: read-only summary of the replay's own temp state taken before cleanup; tolerant of missing files; show handles old results without diag` → pass [tree 92bdd7cf4014] (2026-10-04T05:02:06Z)
## Log
- 2026-10-04T04:59:37Z created
- 2026-10-04T04:59:43Z set tier=S
- 2026-10-04T05:00:19Z focused
- 2026-10-04T05:00:19Z scope: the test edit above was written just before the focus succeeded (plan gaps); it belongs to this task
- 2026-10-04T05:02:06Z done
- 2026-10-04T05:02:06Z committed f5ab3de (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
- research T-0212-review: Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the cod…
- T-0212 [FEATURE L, done, 3 steps] Fm bench — Foreman's own SWE-bench: every finished task with a commit becomes a replayable — lesson: A benchmark made of your own finis…
- research t0023-grounding: Ledger events (this project, ~700 events): step_done 66, step_add 64, task_set 61, ac_check 58, audit 37, subagent 35,
- similar past tasks were L: consider --tier L
## Files touched
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/tests/test_bench.py
- CHANGELOG.md
- MASTER.md
