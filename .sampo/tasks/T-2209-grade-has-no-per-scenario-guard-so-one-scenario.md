---
id: T-2209
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T20:15:44Z
updated: 2026-10-31T03:26:26Z
group: exam grading robustness
base: fbafd8f27bf5279d65d12ddf6e61bab145da1b49
base_tree: fe8d0466506cb49c30f39b7cca4bc9ac74a965c5
plan0_at: 2026-10-31T03:10:42Z
plan0_scope: []
verified: strong
---
# fm exam grade survives one scenario's exception: it grades the rest and names the broken one
## Raw request
> grade() has no per-scenario guard, so one scenario's exception aborts the run's grade (out of scope)
> (noticed by an agent; research T-2203-review)
## Interpretation
fmexam.grade loops over a run's scenarios; one exception (a damaged key.json, a repo git can't read) aborts the whole grade, so the end-of-run exam on the production model could lose every result to one bad scenario.
## Assumptions (confidence)
## Acceptance criteria
- [x] a run where one scenario's grading raises still grades every other scenario, records the broken one as ungraded with the exception's type and message (plain'd), and exits non-zero naming it — verify with `cd plugin/tests && python3 -m unittest -q test_exam`
## Non-goals
## Approach (options → choice → why)
Options: (1) try/except per scenario in grade, an ungraded line with the error, exit non-zero naming it (chosen: smallest, keeps every other result); (2) validate all scenarios before grading (misses runtime failures); (3) let it abort (loses results). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a run dir with one scenario whose key or repo makes grade raise; grade wraps each scenario, records an ungraded line with the error, continues, and the summary names it
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_one_scenario_that_raises_is_ungraded_and_named_while_the_rest_grade` → ✗ exit 1 · Ran 1 test in 0.588s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree b0fca6729cdc] (2026-10-31T03:18:34Z)
- `cd plugin/tests && python3 -m unittest -q test_exam.ExamGen.test_one_scenario_that_raises_is_ungraded_and_named_while_the_rest_grade` → exit 0 · Ran 1 test in 0.555s / OK [ran] [tree b0fca6729cdc] (2026-10-31T03:18:34Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_exam` → exit 0 · Ran 35 tests in 184.220s / OK [ran] [tree b0fca6729cdc] (2026-10-31T03:21:58Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_exam` → exit 0 · Ran 35 tests in 182.946s / OK [ran] [tree f2006e4ec926] (2026-10-31T03:25:02Z)
- (audit edge) `self: grade wraps each scenario in safe() catching Exception only (Ctrl-C and SystemExit still stop it); a broken one adds a plain'd, 200-character ungraded entry and counts as neither found nor fixed; summary lists it; exam run and exam grade exit 1 when any is ungraded; test_exam 35 green; red-to-green proven` → a damaged key.json grades the other scenarios and names the broken one; an ungraded held-out scenario counts as not closed in the scorecard [tree f2006e4ec926] (2026-10-31T03:25:02Z)
- (audit self) `self: grade wraps each scenario in safe() catching Exception only (Ctrl-C and SystemExit still stop it); a broken one adds a plain'd, 200-character ungraded entry and counts as neither found nor fixed; summary lists it; exam run and exam grade exit 1 when any is ungraded; test_exam 35 green; red-to-green proven` → no findings [tree f2006e4ec926] (2026-10-31T03:25:02Z)
## Log
- 2026-10-30T20:15:44Z created
- 2026-10-31T03:10:22Z planned from capture
- 2026-10-31T03:10:22Z set approved=True
- 2026-10-31T03:10:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2209.builder.md
- 2026-10-31T03:10:41Z focused
- 2026-10-31T03:18:30Z merged worktree-agent-af22fc08d52f09b4f (2 file(s))
- 2026-10-31T03:18:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af22fc08d52f09b4f
- 2026-10-31T03:18:31Z focused
- 2026-10-31T03:21:58Z scope: plugin/lib/fmexam.py (grade, summary, CLI exits), plugin/tests/test_exam.py, CHANGELOG.md
- 2026-10-31T03:26:24Z done
- 2026-10-31T03:26:26Z committed 458f5e0a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- research T-2097-review: Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test. …
- decision 2026-10-30: fm genesis select keeps reading Haiku-graded lines and names the model on its provisional line; fm exam scorecard (the done gate) skips them
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
## Lessons
- A batch grader needs a per-item guard, or one bad input erases every good result
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
