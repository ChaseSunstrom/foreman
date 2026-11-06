---
id: T-1164
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:43:10Z
base: 847e9d388a542a90ebf882500e3d91d17d9c17bc
base_tree: 97d841afc3f28d2d5cf395da654bfe8e9ec1b895
plan0_at: 2026-10-16T11:36:14Z
plan0_scope: []
verified: strong
---
# Feed a task's brief with the defect classes confirmed by reviewers in the last 30 days (`f
## Raw request
> FEATURE: Feed a task's brief with the defect classes confirmed by reviewers in the last 30 days (`fm lane brief` section "Defects this project keeps shipping").
> DONE-WHEN: a test with two confirmed findings of one class in the finding records makes `fm lane brief` print that class once with its count, and no section appears when there are none
## Interpretation
Builders keep shipping the same kinds of defect reviewers then find (hot-path cost, cwd vs root paths, duplicated output, counting events instead of actors, untested branches, unbounded input). Put the project's recent confirmed reviewer findings in every builder brief, grouped into a few named classes with a count and one example each, so the builder checks for them before reporting.
## Assumptions (confidence)
## Acceptance criteria
- [x] with two confirmed findings of one class in the last 30 days fm lane brief prints that class once with count 2 and an example; rejected or older findings are ignored; no section when there are none — verify with `python3 plugin/tests/run.py test_defect_classes`
## Non-goals
## Approach (options → choice → why)
Options: (a) read confirmed findings of the last 30 days (fm task finding records; find where they are stored) and bucket them with a small keyword table into classes (hot path/cost, paths/cwd, duplicate/redundant output, counting/dedupe, untested branch, limits/unbounded, untrusted input/injection, race/lock, other), printed in fm lane brief under 'Defects this project keeps shipping' (top 5 classes, count + one 100-char example); (b) ask a model to classify (cost, nondeterminism; rejected); (c) free-text last N findings (no grouping; noisy). Choice: (a). No section when there are none.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_defect_classes.py): two confirmed of one class -> one line count 2; rejected/old ignored; none -> no section
2. [x] The classifier table and the brief section in fmlanes.builder_brief
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_defect_classes` → ✗ exit 1 · Ran 3 tests in 0.9s (1 classes, 16 at a time; slowest: DefectClasses 1s) / FAILED (1 classes) [ran] [tree 09eceb022448] (2026-10-16T11:36:35Z)
- (step 2) `python3 plugin/tests/run.py test_defect_classes test_lanes test_conflict_history` → exit 0 · Ran 36 tests in 11.4s (7 classes, 16 at a time; slowest: Lanes 11s, ConflictHistory 2s, DefectClasses 1s) / OK [ran] [tree b3aa3733f749] (2026-10-16T11:36:55Z)
- (ac 1) `python3 plugin/tests/run.py test_defect_classes test_lanes` → exit 0 · Ran 33 tests in 41.7s (6 classes, 16 at a time; slowest: Lanes 41s, BoardLanes 5s, DefectClasses 4s) / OK [ran] [tree 7941f64a2ebf] (2026-10-16T11:40:16Z)
- (ac 1) `python3 plugin/tests/run.py test_defect_classes` → exit 0 · Ran 3 tests in 4.1s (1 classes, 16 at a time; slowest: DefectClasses 4s) / OK [ran] [tree 02a67b54769a] (2026-10-16T11:40:37Z)
- (step 1) `python3 plugin/tests/run.py test_defect_classes` → exit 0 · Ran 3 tests in 4.1s (1 classes, 16 at a time; slowest: DefectClasses 4s) / OK [ran] [tree 02a67b54769a] (2026-10-16T11:40:37Z)
- (audit intent) `self: reviewed merged diff; backfilled today's 15 confirmed reviewer findings with fm task finding and previewed the section on the real ledger; 'other' was the largest class, so three classes were added from the real wording; now 'other' drops out of the top 5` → builders see this project's recurring defect kinds before they report [tree 02a67b54769a] (2026-10-16T11:40:37Z)
- (audit adversary) `self: reviewed merged diff; backfilled today's 15 confirmed reviewer findings with fm task finding and previewed the section on the real ledger; 'other' was the largest class, so three classes were added from the real wording; now 'other' drops out of the top 5` → finding text is redacted at record time and the brief is redacted on write [tree 02a67b54769a] (2026-10-16T11:40:37Z)
- (audit edge) `self: reviewed merged diff; backfilled today's 15 confirmed reviewer findings with fm task finding and previewed the section on the real ledger; 'other' was the largest class, so three classes were added from the real wording; now 'other' drops out of the top 5` → rejected and older-than-30-day findings ignored; no section with none [tree 02a67b54769a] (2026-10-16T11:40:37Z)
- (audit operator) `self: reviewed merged diff; backfilled today's 15 confirmed reviewer findings with fm task finding and previewed the section on the real ledger; 'other' was the largest class, so three classes were added from the real wording; now 'other' drops out of the top 5` → five lines at most, newest example each [tree 02a67b54769a] (2026-10-16T11:40:37Z)
- (audit maintainer) `self: reviewed merged diff; backfilled today's 15 confirmed reviewer findings with fm task finding and previewed the section on the real ledger; 'other' was the largest class, so three classes were added from the real wording; now 'other' drops out of the top 5` → one keyword table, first match wins; tune it as findings accumulate [tree 02a67b54769a] (2026-10-16T11:40:37Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:36:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1164.builder.md
- 2026-10-16T11:36:13Z focused
- 2026-10-16T11:38:57Z merged worktree-agent-a0d65828bde6f858a (2 file(s))
- 2026-10-16T11:39:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0d65828bde6f858a
- 2026-10-16T11:39:08Z focused
- 2026-10-16T11:40:31Z scope: MASTER.md and CHANGELOG.md lines; three keyword classes added after previewing on today's 15 backfilled findings (5 of 12 were 'other')
- 2026-10-16T11:43:09Z done
- 2026-10-16T11:43:10Z committed cc278756 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261016-round2: Format per cluster: ideas, grounding (code or fm command), Status (queued / done / partial / new / false), Score (value 1-5, effort …
- T-1161 [FEATURE M, done, 2 steps] Record files that conflicted at `fm lane merge` and warn in `fm lane brief` when a new lan — lesson: count distinct actors, not events,…
- research T-1076-review: Verdict: approve with nits.** The code is correct on the paths I traced. None of these findings is HIGH. I did not run the tests, and I could not…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Lessons
- preview a classifier on the real data before shipping it: the table built from imagined wording put 5 of 12 real findings in 'other'
## Plan gaps
- failed first: step 1 Failing tests (test_defect_classes.py): two confirmed of one class -> one line count 2; rejected/ol…
## Files touched
- plugin/tests/test_defect_classes.py
- plugin/lib/fmlanes.py
- MASTER.md
- CHANGELOG.md
