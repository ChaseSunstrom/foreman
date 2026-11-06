---
id: T-1925
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T06:33:10Z
updated: 2026-10-29T07:06:43Z
base: ba96df933ce0d1a6257ee68df7d2c1439582cb77
base_tree: c85dcbc4e1266a7197e6a843ee31d0be996fa5d1
plan0_at: 2026-10-29T07:05:18Z
plan0_scope: []
verified: strong
---
# fm task set: a refused field naming a brief section says --section <Name>; fm which finds it
## Raw request
> fm task set: a refused field that names a brief section (interpretation, approach) should say --section <Name> --text; fm which didn't find it either
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task set ID interpretation=x names --section 'Interpretation'; fm which interpretation finds task set — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Hint in the refusal, section names in --section help; test red then green
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping.FinishGaps.test_a_refused_field_naming_a_section_says_how_to_fill_it` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: FinishGaps 1s) / FAILED (1 classes) [ran] [tree f1963ebea9cb] (2026-10-29T07:05:35Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 18 tests in 7.9s (8 classes, 16 at a time; slowest: CommitOwnFiles 8s, StepEvidence 7s, FinishGaps 7s) / OK [ran] [tree 8fd19550517a] (2026-10-29T07:05:57Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 18 tests in 3.7s (8 classes, 16 at a time; slowest: FinishGaps 3s, StepEvidence 3s, CommitOwnFiles 3s) / OK [ran] [tree 8fd19550517a] (2026-10-29T07:06:12Z)
- (audit intent) `self review of the diff; test red then green; manual run of the refusal` → interpretation=x and approach=x now name --section with the exact heading; fm which interpretation lists fm task set [tree 8fd19550517a] (2026-10-29T07:06:12Z)
- (audit edge) `self review of the diff; test red then green; manual run of the refusal` → unknown fields (colour=x) keep the old message; risks_and_rollback maps to 'Risks and rollback' [tree 8fd19550517a] (2026-10-29T07:06:12Z)
- (audit self) `self review of the diff; test red then green; manual run of the refusal` → no findings [tree 8fd19550517a] (2026-10-29T07:06:12Z)
## Log
- 2026-10-29T06:33:10Z created
- 2026-10-29T07:05:17Z planned from capture
- 2026-10-29T07:05:17Z focused
- 2026-10-29T07:06:41Z done
- 2026-10-29T07:06:43Z committed b0d49b3c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1624-review: Verdict:** approve with nits. I couldn't run anything (no Bash in this session), so every finding below comes from reading the code. No finding i…
- T-1805 [FEATURE S, done, 2 steps] Before a push to main or a release, run the suite once under the oldest supported Python w — lesson: A flag that re-runs a command unde…
- research T-1652-review: Verdict: changes needed.** Three MEDIUM findings: the worker write guard, release versioning, and the DTCG importer silently dropping tokens. I r…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 2 steps
## Plan gaps
- failed first: step 1 Hint in the refusal, section names in --section help; test red then green
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
- CHANGELOG.md
