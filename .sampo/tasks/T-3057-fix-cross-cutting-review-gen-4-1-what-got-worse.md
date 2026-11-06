---
id: T-3057
type: FIX
tier: M
status: planned
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:07Z
updated: 2026-11-06T03:53:13Z
trigger: genesis-review
trigger_key: c290705280a2d241
---
# Sampo's own arm stops claiming done falsely in Louhi's long exams: find why every foreman run says done while the hidden checks fail (6 of 6 false, plain arm 1 of 6 true), then fix the cause
## Raw request
> FIX: cross-cutting review gen-4 #1 (what got worse): Sampo's own arm reports done falsely on every scenario (l001/l002 foreman: true done 0/6, false done 6, gens 2 and 3) while the plain arm manages 1/6; the discipline layer scores below no layer at all and nothing in the diff touches it. [false done 6]
> genesis-review 4:1
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
Reading 1 (chosen): gen-4's review found the foreman arm of the long exams (l001, l002; gens 2 and 3) reporting done on all 6 scenarios with 0 true, while the plain arm manages 1 of 6: Sampo's discipline layer (evidence, criteria checks, finish) is meant to prevent exactly this, so either its criteria checks pass vacuously on those scenarios, the close accepts evidence that doesn't run the hidden behaviour, or the grader reads done from a field Sampo writes early; read each run's journal and the grade, name the cause per run, fix it in Sampo, and rerun one long scenario per arm. Reading 2: a grader bug only; possible, ruled in or out by step 1.
## Assumptions (confidence)
## Acceptance criteria
- [ ] for each of the 6 false-done runs, the cause is named in research (which check passed without testing the goal, or where done was read too early) — verify with `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/T-3057-false-done.md`
- [ ] the cause is fixed in Sampo with a test that reproduces one of the runs' shapes (red before, green after) — verify with `python3 plugin/tests/run.py test_exam`
- [ ] one long scenario rerun per arm after the fix: the foreman arm no longer reports done where the hidden check fails — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: sampo exam long's run.json, key.json and the foreman arm's journals and task files, sampo task prove --vacuous for each run's criteria; likely outcome: a named cause per run (vacuous checks or premature done) and a fix with a test. 2. Do less: tighten the grader; fails if: the arm really closes on vacuous checks. 3. Rerun all long exams first; fails if: hours of runs before any cause is known. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] read the 6 runs' journals, task files and grades; name each cause  <- CURRENT
2. [ ] failing test of the cause
3. [ ] the fix
4. [ ] rerun one long scenario per arm
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:31:07Z created
- 2026-11-05T03:54:12Z planned from capture
- 2026-11-05T03:54:14Z set approved=True
- 2026-11-05T03:54:14Z blocked: approved; waits for a builder slot (investigation-heavy: a sonnet builder with the long exam paths)
- 2026-11-06T03:53:13Z unblocked
## Follow-ups captured
