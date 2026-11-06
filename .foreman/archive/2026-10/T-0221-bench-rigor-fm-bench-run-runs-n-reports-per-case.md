---
id: T-0221
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:59:37Z
updated: 2026-10-04T05:04:29Z
base: f5ab3dea93ce5f50a2b4889857f8da83db3c7149
base_tree: 92bdd7cf40140f88fcd43af07ab5344b64d0958e
verified: strong
---
# Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
## Raw request
> FEATURE: bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread, and fm bench gate A B says whether a candidate is no worse than live beyond noise (pass rate, cost +15%)
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
- [x] --runs 2 aggregates each case (pass rate, mean cost/turns), and fm bench gate passes an equal-or-better candidate and fails one that loses passes or costs >15% more — verify with `python3 plugin/tests/run.py -k test_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first, then --runs aggregation and fm bench gate; improve skill requires the gate
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/improve/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 9 tests in 8.0s (1 classes, 16 at a time; slowest: Bench 8s) / OK [ran] [tree f5b4c8e02399] (2026-10-04T05:03:21Z)
- `python3 plugin/tests/run.py -k test_bench` → ✗ exit 1 · Ran 9 tests in 7.7s (1 classes, 16 at a time; slowest: Bench 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f5b4c8e02399] (2026-10-04T05:03:37Z)
- `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 9 tests in 8.0s (1 classes, 16 at a time; slowest: Bench 8s) / OK [ran] [tree f5b4c8e02399] (2026-10-04T05:03:37Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 9 tests in 8.0s (1 classes, 16 at a time; slowest: Bench 8s) / OK [ran] [tree f5b4c8e02399] (2026-10-04T05:04:29Z)
- (audit self) `self checklist: gate compares only shared cases, treats old single-run results as 0/1 rates, fails on fewer total passes or >15% cost, warns on single runs; tests cover equal, worse, pricier` → pass [tree f5b4c8e02399] (2026-10-04T05:04:29Z)
## Log
- 2026-10-04T04:59:37Z created
- 2026-10-04T05:02:17Z set tier=S
- 2026-10-04T05:02:17Z focused
- 2026-10-04T05:04:29Z done
- 2026-10-04T05:04:29Z committed 41648c8 (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0220 [FEATURE S, done, 1 steps] Replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (t
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
- T-0212 [FEATURE L, done, 3 steps] Fm bench — Foreman's own SWE-bench: every finished task with a commit becomes a replayable — lesson: A benchmark made of your own finis…
- research T-0212-review: Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the cod…
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_bench.py
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/improve/SKILL.md
