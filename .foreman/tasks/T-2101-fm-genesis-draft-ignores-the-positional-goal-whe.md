---
id: T-2101
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T05:27:22Z
updated: 2026-10-30T11:39:18Z
base: f30000da6197261f32695e4ba7408aa46c539af4
base_tree: 2a377850b8115a8a966c659bda9a81c5f9150bf9
plan0_at: 2026-10-30T11:37:35Z
plan0_scope: []
verified: strong
---
# fm genesis draft` ignores the positional goal when `--file` is also given, and…
## Raw request
> fm genesis draft` ignores the positional goal when `--file` is also given, and `--per-kind` is accepted by every genesis action
> (noticed by an agent; research T-2099-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis draft refuses a goal line plus --file, and --per-kind is refused outside spec/exam — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: usage errors for both; per-kind default None, 9 in spec/exam
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_draft_refuses_a_goal_twice_and_per_kind_is_only_for_spec_and_exam` → red as expected (exit 1) · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes) [ran] [tree e5b1126e0065] (2026-10-30T11:38:03Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 94 tests in 19.6s (21 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamAuthors 12s) / OK [ran] [tree a148caf6e783] (2026-10-30T11:38:27Z)
- `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_draft_refuses_a_goal_twice_and_per_kind_is_only_for_spec_and_exam` → ✗ exit 1 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9ab101e0418d] (2026-10-30T11:38:38Z)
- `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_draft_refuses_a_goal_twice_and_per_kind_is_only_for_spec_and_exam` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / OK [ran] [tree 9ab101e0418d] (2026-10-30T11:38:38Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 70 tests in 4.1s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 9ab101e0418d] (2026-10-30T11:38:55Z)
- (audit edge) `self: diffed; every caller (fmexam GENESIS prompt, scout hint, skills, site) passes the goal one way only; no-action status with --per-kind is refused; spec/exam keep 9 by default and still reject under 3` → --per-kind 0 reaches spec's own 'at least 3' error instead of becoming 9 [tree 9ab101e0418d] (2026-10-30T11:38:55Z)
- (audit self) `self: diffed; every caller (fmexam GENESIS prompt, scout hint, skills, site) passes the goal one way only; no-action status with --per-kind is refused; spec/exam keep 9 by default and still reject under 3` → no findings [tree 9ab101e0418d] (2026-10-30T11:38:55Z)
## Log
- 2026-10-30T05:27:22Z created
- 2026-10-30T11:37:34Z set tier=S, type=FIX
- 2026-10-30T11:37:34Z planned: it has criteria and steps
- 2026-10-30T11:37:34Z focused
- 2026-10-30T11:39:17Z done
- 2026-10-30T11:39:18Z committed cf6037b1 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research T-2099-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** There are no HIGH findings. Two MEDIUM is…
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
