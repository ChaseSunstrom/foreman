---
id: T-2150
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-30T11:11:35Z
updated: 2026-10-30T11:12:44Z
baseline: true
base: e626873d29cde3784f88f8992b959cd28ca04862
base_tree: 35c8297912cb8be766e0bd1da815636bb1ee4a1e
plan0_at: 2026-10-30T11:12:10Z
plan0_scope: []
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_find.FindRenders.test_clean_renders_find_nothing_and_planted_ones_find_their_key. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_find passes with resume's done items skipped — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] skip done key items in the find coverage test
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find` → red as expected (exit 1) · Ran 30 tests in 5.9s (14 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, FindLearns 1s) / FAILED (1 classes) [ran] [tree 35c8297912cb] (2026-10-30T11:12:21Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 30 tests in 5.9s (14 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 1dd235411049] (2026-10-30T11:12:27Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 30 tests in 5.9s (14 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 1dd235411049] (2026-10-30T11:12:40Z)
- (audit edge) `self-review: a resume key's done item is met on the planted repo by design (T-2140), so the coverage test skips it; the clean-render and no-unkeyed-finding asserts still cover it` → only done items are skipped; every planted item of every kind and language is still asserted found [tree 1dd235411049] (2026-10-30T11:12:40Z)
- (audit self) `self-review: a resume key's done item is met on the planted repo by design (T-2140), so the coverage test skips it; the clean-render and no-unkeyed-finding asserts still cover it` → no findings [tree 1dd235411049] (2026-10-30T11:12:40Z)
## Log
- 2026-10-30T11:11:35Z created
- 2026-10-30T11:12:09Z set tier=S
- 2026-10-30T11:12:09Z planned: it has criteria and steps
- 2026-10-30T11:12:09Z focused
- 2026-10-30T11:12:43Z done
- 2026-10-30T11:12:44Z committed 467794d6 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2085 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-2021 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-2147 [FIX M, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: a new MASTER note bumps its group's map-table count; run test_docs after any M…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- the similar finished task took 1 steps
## Lessons
- a new key field (done) needs a sweep of every test that iterates fmexam.KINDS, not just test_exam
## Files touched
- plugin/tests/test_find.py
