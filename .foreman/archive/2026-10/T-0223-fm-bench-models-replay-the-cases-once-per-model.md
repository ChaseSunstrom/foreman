---
id: T-0223
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:59:37Z
updated: 2026-10-04T05:10:04Z
base: 6ba4e6ea1940be5b2033ea176f487ee5f21dbeea
base_tree: 7a8f9d4f2cb25922646843b33e09e6aa45eb0a76
verified: strong
---
# Fm bench models — replay the cases once per model and recommend the cheapest model that pa
## Raw request
> FEATURE: fm bench models — replay the cases once per model and recommend the cheapest model that passes per tier, saved for fm run --models on a yes
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
fm run --models S=…,M=…,L=… is chosen by hand. Measure instead: replay the bench cases once per model and recommend, per tier, the cheapest model that reaches the best pass rate — usage saved on the user's own work.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a stub where only some models solve, fm bench models recommends per tier the cheapest model with the best pass rate, and --save stores it for fm run — verify with `python3 plugin/tests/run.py -k test_bench`
## Non-goals
## Approach (options → choice → why)
A) a static table (haiku for S…): ignores what this project needs. B) fm bench models: run_case_n per model over the cases, then per tier pick the model with the best pass total and, among ties, the lowest measured mean cost; --save writes meta run_models like fm run --save. Choice: B.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then models runner + recommendation + --save
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 11 tests in 10.2s (1 classes, 16 at a time; slowest: Bench 10s) / OK [ran] [tree 4fa707bb11ed] (2026-10-04T05:08:24Z)
- `python3 plugin/tests/run.py -k test_bench` → ✗ exit 1 · Ran 11 tests in 9.4s (1 classes, 16 at a time; slowest: Bench 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4fa707bb11ed] (2026-10-04T05:08:44Z)
- `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 11 tests in 10.3s (1 classes, 16 at a time; slowest: Bench 10s) / OK [ran] [tree 4fa707bb11ed] (2026-10-04T05:08:44Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 11 tests in 10.4s (1 classes, 16 at a time; slowest: Bench 10s) / OK [ran] [tree 4fa707bb11ed] (2026-10-04T05:10:04Z)
- (audit intent) `self review` → per-tier model choice for fm run now comes from the project's own replayed work; saves usage when a cheaper model passes [tree 4fa707bb11ed] (2026-10-04T05:10:04Z)
- (audit edge) `self review` → a tier no model passed keeps its current model; a crashing model run is recorded per case; model names validated before use as argv; --save merges into existing run_models (tested) [tree 4fa707bb11ed] (2026-10-04T05:10:04Z)
## Log
- 2026-10-04T04:59:37Z created
- 2026-10-04T05:07:17Z focused
- 2026-10-04T05:07:17Z scope: the test edit above was written just before the focus succeeded (plan gaps); it belongs to this task
- 2026-10-04T05:10:04Z done
- 2026-10-04T05:10:04Z committed 263266b (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0221 [FEATURE S, done, 1 steps] Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
- T-0220 [FEATURE S, done, 1 steps] Replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (t
- T-0222 [FEATURE S, done, 1 steps] Fm bench build --commits RANGE --verify CMD — bench cases from any repo's history (commits
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
- similar finished tasks took 1–1 steps
## Lessons
- Recommend from measured pass totals first and measured cost second: an order-of-models assumption ('haiku is cheapest') breaks the moment pricing or a model's verbosity changes
## Files touched
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/tests/test_bench.py
- CHANGELOG.md
- MASTER.md
