---
id: T-2401
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:16:30Z
updated: 2026-10-31T15:07:30Z
base: d4a33b4f400f26f667f8bcc1fe502705ae2ff625
base_tree: 0ed24519fdbd763e950ccad61f8f5b68a3297bba
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-10-31T14:17:12Z
plan0_scope: []
verified: strong
---
# #4 exam defect: the oracle misses test-first on goal-rust-860eab (s0-011), so it closes 17/18 and a #4 held-out scenario no arm can close
## Raw request
> #4 exam defect: the oracle misses test-first on goal-rust-860eab (s0-011), so it closes 17/18 and a #4 held-out scenario no arm can close
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the oracle closes every s0-011 scenario, goal-rust-860eab included — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce: put the scenario's tf defect back into the oracle's work and run its suite; find why the suite doesn't catch it or fails on loading (LOAD); red test in test_exam with a rust goal render; fix the template or the putback
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 43 tests in 96.1s (11 classes, 16 at a time; slowest: ExamAuthors 96s, ExamGen 75s, ExamRust 23s) / OK [ran] [tree a4f12e8d1bb3] (2026-10-31T14:23:24Z)
- `python3 plugin/tests/run.py test_exam -k merges_two_regions` → ✗ exit 1 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: ExamGen 0s) / FAILED (1 classes: test_exam.ExamGen) (start tree + this task's tests) [ran] [tree a4f12e8d1bb3] (2026-10-31T14:23:29Z)
- `python3 plugin/tests/run.py test_exam -k merges_two_regions` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: ExamGen 0s) / OK [ran] [tree a4f12e8d1bb3] (2026-10-31T14:23:29Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 43 tests in 89.1s (11 classes, 16 at a time; slowest: ExamAuthors 88s, ExamGen 70s, ExamRust 28s) / OK [ran] [tree f459fc2dd761] (2026-10-31T14:25:31Z)
- (audit edge) `self-review: putback merges adjacent changed regions when either's widened anchor reaches the other (the equal lines between are the same in clean and planted, so the merged planted slice is exact); red→green on a two-region page() fixture shaped like goal-rust-860eab; all 43 exam tests pass` → regions far apart are applied as before (the existing two-region test still passes); a merge never widens past either region's own lines [tree f459fc2dd761] (2026-10-31T14:25:31Z)
- (audit self) `self-review: putback merges adjacent changed regions when either's widened anchor reaches the other (the equal lines between are the same in clean and planted, so the merged planted slice is exact); red→green on a two-region page() fixture shaped like goal-rust-860eab; all 43 exam tests pass` → no findings [tree f459fc2dd761] (2026-10-31T14:25:31Z)
## Log
- 2026-10-31T14:16:30Z created
- 2026-10-31T14:17:09Z focused
- 2026-10-31T14:17:12Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-10-31T14:23:58Z scope: plugin/lib/fmexam.py, plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:27:47Z done
- 2026-10-31T14:27:50Z committed e65edbb8 (4 files)
- 2026-10-31T15:07:30Z verified on s70-010 (zero-token oracle rerun): test-first 194/203 -> 201/203; the 2 left are held-out slow-c-18f793 and slow-c-6bc211, a different defect (a slow C defect put back doesn't make the suite fail), filed apart
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- decision 2026-10-30: [revisited: free arm beats the session arm] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3 plugin/tests/ru…
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–4 steps
## Lessons
- Anchors computed on the original text break once a neighbouring edit lands: merge regions that share context before applying
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
