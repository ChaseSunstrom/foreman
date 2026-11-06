---
id: T-2130
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/tests/test_genesis.py]
depends_on: []
source: discovered
created: 2026-10-30T09:31:47Z
updated: 2026-10-30T13:03:12Z
base: 54a116dac0d300a613e38050c666928617be03f7
base_tree: 2cfee3053adfb1255566c421bf9ced80dd86f725
plan0_at: 2026-10-30T13:02:23Z
plan0_scope: [plugin/tests/test_genesis.py]
verified: strong
---
# plugin/tests/test_genesis.py:1325 slices `fmexam.KINDS[i::3]`, so the genesis test's…
## Raw request
> plugin/tests/test_genesis.py:1325 slices `fmexam.KINDS[i::3]`, so the genesis test's capability sets shift with every kind added. Pin it to an explicit list
> (noticed by an agent; research T-2126-review)
## Interpretation
test_genesis.py:1374 builds three capabilities from fmgenesis.GEN_DEFECTS[i::3], so adding a defect kind reshuffles which kinds each capability holds and can flip the test for no reason. Pin the three lists to the kinds they hold today.
## Assumptions (confidence)
## Acceptance criteria
- [x] the genesis exam test passes with explicit capability lists — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] replace the stride slice with the three explicit lists
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 74 tests in 4.7s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 3a4df354cff5] (2026-10-30T13:02:35Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 74 tests in 4.2s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 3a4df354cff5] (2026-10-30T13:02:39Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 74 tests in 4.4s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree d384cff80e8d] (2026-10-30T13:02:57Z)
- (audit intent) `diff vs the raw request` → the three groups are exactly today's GEN_DEFECTS[i::3]; the unused import went with it [tree d384cff80e8d] (2026-10-30T13:02:57Z)
- (audit maintainer) `a new defect kind added to GEN_DEFECTS` → no longer reshuffles this test's capabilities [tree d384cff80e8d] (2026-10-30T13:02:57Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 74 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree d384cff80e8d] (2026-10-30T13:03:09Z)
- (audit self) `self: the pinned groups equal today's slices; test_genesis green` → no findings [tree d384cff80e8d] (2026-10-30T13:03:09Z)
## Log
- 2026-10-30T09:31:47Z created
- 2026-10-30T13:02:06Z set type=CLEAN, tier=S
- 2026-10-30T13:02:06Z planned: it has criteria and steps
- 2026-10-30T13:02:06Z set scope=['plugin/tests/test_genesis.py']
- 2026-10-30T13:02:22Z focused
- 2026-10-30T13:02:24Z set approved=True
- 2026-10-30T13:03:11Z done
- 2026-10-30T13:03:12Z committed 9027c9d5 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- T-2131 [FIX S, done, 1 steps] FIX S: fmgenesis CHILD prompt says '"none" is a clean repo' and KIND_WORDS maps 'clean…
- T-2126 [FEATURE M, done, 2 steps] #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7) — lesson: a module-…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- similar finished tasks took 1–2 steps
## Preflight
Changed in scope since this was planned (2026-10-30): plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Behaviour lock
none: test-only; the test's own assertions are the lock and pass unchanged
## Lessons
- Pin a test's inputs to explicit values; a stride slice over a growing tuple silently changes what the test checks
## Files touched
- plugin/tests/test_genesis.py
