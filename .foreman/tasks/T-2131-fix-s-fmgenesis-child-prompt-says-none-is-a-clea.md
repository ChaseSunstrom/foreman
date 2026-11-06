---
id: T-2131
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T09:33:17Z
updated: 2026-10-30T11:37:20Z
base: ff13889197f0a4155bacbb79fbfd66f598933c6a
base_tree: 5d58acf778d705fb2fbbfd87205c989e46f24cb0
plan0_at: 2026-10-30T11:34:18Z
plan0_scope: []
verified: strong
---
# FIX S: fmgenesis CHILD prompt says '"none" is a clean repo' and KIND_WORDS maps 'clean…
## Raw request
> FIX S: fmgenesis CHILD prompt says '"none" is a clean repo' and KIND_WORDS maps 'clean repo|calibrat' to none, but fmexam now has a 'clean' kind (none = no request, planted defects); reword the prompt and map clean/rank words, without moving GEN_DEFECTS (T-2126 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Genesis maps none (unasked defects), clean (nothing planted) and rank to fmexam's kinds in CHILD, KIND_WORDS and FALLBACK — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: _kinds and FALLBACK map clean/none/rank; reword CHILD
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.Genesis.test_clean_none_and_rank_map_to_their_own_exam_kinds` → red as expected (exit 1) · run.py: no test matches test_genesis.Genesis.test_clean_none_and_rank_map_to_their_own_exam_kinds [ran] [tree e050a65de0d2] (2026-10-30T11:34:29Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_clean_none_and_rank_map_to_their_own_exam_kinds` → red as expected (exit 1) · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes) [ran] [tree e050a65de0d2] (2026-10-30T11:34:36Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam` → ✗ exit 1 · Ran 93 tests in 22.7s (21 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 17s, GenesisLive 15s) / FAILED (1 classes) [ran] [tree f71f68f1822b] (2026-10-30T11:35:03Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 93 tests in 22.6s (21 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 17s, GenesisLive 15s) / OK [ran] [tree 59a236f8d01d] (2026-10-30T11:36:01Z)
- `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_clean_none_and_rank_map_to_their_own_exam_kinds` → ✗ exit 1 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2a377850b811] (2026-10-30T11:36:25Z)
- `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_clean_none_and_rank_map_to_their_own_exam_kinds` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / OK [ran] [tree 2a377850b811] (2026-10-30T11:36:25Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 69 tests in 4.0s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 2a377850b811] (2026-10-30T11:37:17Z)
- (audit edge) `self: diffed fmgenesis; rank/none/clean regexes run against every FALLBACK text and the test fixtures (no stray hits; 'on its own' dropped as too broad); GEN_DEFECTS untouched; old 'Initiative unmapped' fixture now uses Taste` → 'Prioritizes security fixes' maps to rank + vuln, both right; \brank keeps 'frank' out [tree 2a377850b811] (2026-10-30T11:37:17Z)
- (audit self) `self: diffed fmgenesis; rank/none/clean regexes run against every FALLBACK text and the test fixtures (no stray hits; 'on its own' dropped as too broad); GEN_DEFECTS untouched; old 'Initiative unmapped' fixture now uses Taste` → no findings [tree 2a377850b811] (2026-10-30T11:37:17Z)
## Log
- 2026-10-30T09:33:17Z created
- 2026-10-30T09:33:22Z set type=FIX, tier=S
- 2026-10-30T11:34:16Z planned: it has criteria and steps
- 2026-10-30T11:34:17Z focused
- 2026-10-30T11:37:19Z done
- 2026-10-30T11:37:20Z committed f30000da (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- T-2126 [FEATURE M, done, 2 steps] #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7) — lesson: a module-…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
