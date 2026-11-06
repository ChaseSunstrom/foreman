---
id: T-0222
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:59:37Z
updated: 2026-10-04T05:06:47Z
base: 41648c8a5a31c1efc15121210c20d837466da487
base_tree: f5b4c8e02399cbf56fab0675f0b101ddb40af716
verified: strong
---
# Fm bench build --commits RANGE --verify CMD — bench cases from any repo's history (commits
## Raw request
> FEATURE: fm bench build --commits RANGE --verify CMD — bench cases from any repo's history (commits touching tests and source, prompt from the commit message), validated fail-to-pass like brief cases
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
- [x] a commit with a test and a fix (no brief) becomes a valid case via --commits/--verify; a tests-only commit is skipped; brief cases stay — verify with `python3 plugin/tests/run.py -k test_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then commit mining in fmbench.build
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 10 tests in 8.7s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree 1201e0ec0f7b] (2026-10-04T05:05:37Z)
- `python3 plugin/tests/run.py -k test_bench` → ✗ exit 1 · Ran 10 tests in 8.6s (1 classes, 16 at a time; slowest: Bench 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1201e0ec0f7b] (2026-10-04T05:05:54Z)
- `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 10 tests in 8.7s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree 1201e0ec0f7b] (2026-10-04T05:05:54Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 10 tests in 8.8s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree 1201e0ec0f7b] (2026-10-04T05:06:47Z)
- (audit self) `self checklist: test paths are shell-quoted into the user's own verify template; docs-only and tests-only commits skipped; same fail-to-pass validation; merging keeps the other kind of case` → pass [tree 1201e0ec0f7b] (2026-10-04T05:06:47Z)
## Log
- 2026-10-04T04:59:37Z created
- 2026-10-04T05:04:43Z set tier=S
- 2026-10-04T05:04:43Z focused
- 2026-10-04T05:06:47Z done
- 2026-10-04T05:06:47Z committed 6ba4e6e (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0221 [FEATURE S, done, 1 steps] Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
- T-0220 [FEATURE S, done, 1 steps] Replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (t
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
- T-0212 [FEATURE L, done, 3 steps] Fm bench — Foreman's own SWE-bench: every finished task with a commit becomes a replayable — lesson: A benchmark made of your own finis…
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_bench.py
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
