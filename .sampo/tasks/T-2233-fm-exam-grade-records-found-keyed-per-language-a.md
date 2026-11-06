---
id: T-2233
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T23:45:16Z
updated: 2026-10-30T23:59:16Z
base: 1aba532b724e9ac5eb7d7f6f7aa527e01c7c85fe
base_tree: 86491dac5be590a909fd723fe400b47237277037
plan0_at: 2026-10-30T23:47:34Z
plan0_scope: []
paused_tree: 89a32e6234bf043c6c92938a38f20f2a849e5fea
verified: strong
---
# fm exam grade records found/keyed per language and per defect kind, and fm exam summary…
## Raw request
> fm exam grade records found/keyed per language and per defect kind, and fm exam summary prints them, so #1's recall is reported per language and bug type (T-2185 piece 1; re-grading s0-001's saved finders answers gives the numbers at no model cost)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam grade records found/keyed per language and per defect kind (overall and held out) and summary prints them — verify with `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in ExamGen, then grade aggregates per-scenario (lang, kind, hit) and summary prints it
## Resume here
## Docs impact
MASTER.md fmexam entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → red as expected (exit 1) · Ran 1 test in 0.111s / FAILED (failures=1) [ran] [tree 03275356e637] (2026-10-30T23:47:46Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → red as expected (exit 1) · Ran 1 test in 0.111s / FAILED (failures=1) [ran] [tree 03275356e637] (2026-10-30T23:47:58Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → red as expected (exit 1) · Ran 1 test in 0.205s / FAILED (errors=1) [ran] [tree 4c8bdba1b75a] (2026-10-30T23:48:08Z)
- `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → ✗ exit 1 · Ran 1 test in 0.383s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree 8f3f8016c0e3] (2026-10-30T23:48:59Z)
- `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → exit 0 · Ran 1 test in 0.325s / OK [ran] [tree 8f3f8016c0e3] (2026-10-30T23:48:59Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → exit 0 · Ran 1 test in 0.340s / OK [ran] [tree 8f3f8016c0e3] (2026-10-30T23:52:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → exit 0 · Ran 1 test in 0.350s / OK [ran] [tree 8f3f8016c0e3] (2026-10-30T23:52:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_recall_is_reported_per_language_and_per_defect_kind` → exit 0 · Ran 1 test in 0.336s / OK [ran] [tree 89a32e6234bf] (2026-10-30T23:52:32Z)
- (audit edge) `self: diff read twice; recall is returned beside the int counts (never summed into them), so every consumer of the COUNTS dicts is unchanged; keys are the generator's own lang and defect kind; summary plain's and cuts them; test_exam green` → goal kinds keep nothing keyed, so they add no recall; each axis splits the same found/keyed totals (asserted); held-out recall asserted non-empty [tree 89a32e6234bf] (2026-10-30T23:52:32Z)
- (audit self) `self: diff read twice; recall is returned beside the int counts (never summed into them), so every consumer of the COUNTS dicts is unchanged; keys are the generator's own lang and defect kind; summary plain's and cuts them; test_exam green` → no findings [tree 89a32e6234bf] (2026-10-30T23:52:32Z)
## Log
- 2026-10-30T23:45:16Z created
- 2026-10-30T23:47:32Z set tier=S
- 2026-10-30T23:47:33Z planned: it has criteria and steps
- 2026-10-30T23:47:33Z focused
- 2026-10-30T23:53:08Z paused: focus moved to T-2221
- 2026-10-30T23:53:55Z done
- 2026-10-30T23:53:57Z committed 496c0c47 (4 files)
- 2026-10-30T23:56:23Z guard authorization added: publish
- 2026-10-30T23:59:16Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule: exam recall for #1 is reported …
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Lessons
- A total hides a blind spot: report a detector's recall along every axis a steer names, from the same tally
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
