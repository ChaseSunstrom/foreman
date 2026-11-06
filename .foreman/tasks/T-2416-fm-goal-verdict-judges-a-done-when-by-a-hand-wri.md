---
id: T-2416
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T14:56:39Z
updated: 2026-10-31T18:06:01Z
builder_model: sonnet
base: c9b0eebf92b3f046b61ca532435717bd6b943a55
base_tree: 07dd4619cbf37567f15599f3b347e02d50018531
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-10-31T17:52:26Z
plan0_scope: []
lane_stop: merged 2026-10-31T18:03:02Z
verified: strong
---
# fm goal verdict judges a done-when by a hand-written list of command forms (_VACUOUS,…
## Raw request
> fm goal verdict judges a done-when by a hand-written list of command forms (_VACUOUS, lint_verify in fmcore.py), a format check: test 1 -eq 1 still reads finished. Replace it with a red check: a done-when counts only if it fails on the tree as it was before the item's work (from gen-1/critique-finish.md; T-2333 is the ls/cat overreach of the same list)
## Interpretation
Reading 1: fm goal verdict counts an item's done-when only if it fails on the tree from before the item's work (the earliest start commit, c.task_base, of the item's tasks), run guarded with fmcli._run_at as fm task prove --vacuous does; a check that passes there (test 1 -eq 1, a grep for text that already existed) reads 'item N check passes before the work: it proves nothing'. The red result is cached per (done-when, base sha), since a base never changes. Reading 2: widen the _VACUOUS list. Ruled out: a list is a format check, any form outside it passes (the critique's point; T-2333 was its overreach).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal verdict reads an item whose done-when passes on its tasks' start tree as not finished ('passes before the work'), and one that fails there and passes now as proven; the start-tree result is cached per done-when and base — verify with `python3 plugin/tests/run.py test_goal -k RedBefore`
## Non-goals
## Approach (options → choice → why)
1) red check on the item's start tree via _run_at, cached per (done-when, base); lint_verify kept only where no start commit exists (fails if: an item's tasks have no base, which the fallback names as unproven rather than finished). 2) use what exists: run fm task prove --vacuous on each item task's criteria; fails if: the goal's done-when is not a task criterion, so the item check itself stays unproven. 3) do less: add test/[ to _VACUOUS; fails if: the next form (python3 -c 1, grep for existing text) passes again. Choice 1 (80%): the done-when itself is judged by running it where the work isn't.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: test 1 -eq 1 and a grep for existing text read hollow; a real check reads proven; cached on a rerun; no base falls back to lint_verify and says unproven
2. [x] the red check in fmmandate.verdict via fmcli._run_at and c.task_base, with the cache
3. [x] docs: MASTER fmmandate line, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_goal -k RedBefore` → ✗ exit 1 · Ran 5 tests in 8.6s (1 classes, 16 at a time; slowest: GoalRedBefore 5s) / FAILED (1 classes: test_goal.GoalRedBefore) [ran] [tree 80338b4c62a4] (2026-10-31T17:55:02Z)
- (step 2) `python3 plugin/tests/run.py test_goal -k RedBefore` → exit 0 · Ran 5 tests in 6.3s (1 classes, 16 at a time; slowest: GoalRedBefore 6s) / OK [ran] [tree d2552b6e60d3] (2026-10-31T17:56:21Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs test_goal test_mandate && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.28s] [ran] [tree c3ef863d7bce] (2026-10-31T17:57:06Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mandate test_docs` → exit 0 · Ran 141 tests in 21.3s (32 classes, 16 at a time; slowest: GoalReview 21s, GoalAcrossDays 18s, Fences 16s) / OK [ran] [tree fb7f9d17e482] (2026-10-31T18:04:10Z)
- (step 3) `grep -q T-2416 MASTER.md CHANGELOG.md` → exit 0 · (no output) [ran] [tree 60009de834c0] (2026-10-31T18:04:36Z)
- (ac 1) `python3 plugin/tests/run.py test_goal -k RedBefore` → exit 0 · Ran 5 tests in 13.7s (1 classes, 16 at a time; slowest: GoalRedBefore 12s) / OK [ran] [tree 60009de834c0] (2026-10-31T18:04:52Z)
- (audit intent) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; one finding fixed (deadline-skipped items no longer run under the task's grants)` → a done-when counts only if it fails on the item's start tree; no base reads unproven [tree 60009de834c0] (2026-10-31T18:04:52Z)
- (audit adversary) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; one finding fixed (deadline-skipped items no longer run under the task's grants)` → checks run guarded on a scratch tree; drift-refused and unreached items never run here [tree 60009de834c0] (2026-10-31T18:04:52Z)
- (audit edge) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; one finding fixed (deadline-skipped items no longer run under the task's grants)` → timeouts and scratch failures uncached; earliest base wins; cache capped [tree 60009de834c0] (2026-10-31T18:04:52Z)
- (audit operator) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; one finding fixed (deadline-skipped items no longer run under the task's grants)` → only fm goal verdict runs it; 300 s per check, 900 s per verdict [tree 60009de834c0] (2026-10-31T18:04:52Z)
## Log
- 2026-10-31T14:56:39Z created
- 2026-10-31T17:52:08Z planned: it has criteria and steps
- 2026-10-31T17:52:09Z set tier=M
- 2026-10-31T17:52:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2416.builder.md
- 2026-10-31T17:52:25Z focused
- 2026-10-31T17:52:26Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-10-31T18:03:02Z merged worktree-agent-a58b74fd2a0ed056b (3 file(s))
- 2026-10-31T18:03:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a58b74fd2a0ed056b
- 2026-10-31T18:03:25Z focused
- 2026-10-31T18:04:25Z scope: files outside the globs came from the lane merge and the changelog line
- 2026-10-31T18:05:56Z done
- 2026-10-31T18:06:01Z committed 28e96faa (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2332-review: I found no HIGH issues. The change is small and the diff matches the two acceptance criteria. I read the code but did not run any tests. The adve…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
## Why not caught
none: the format list was the design (T-2332); the Mission 4 critique found its gap
## Lessons
- Judge a check by running it where the work isn't, not by matching its shape: any shape list has a next form it misses
## Plan gaps
- failed first: step 1 red tests: test 1 -eq 1 and a grep for existing text read hollow; a real check reads proven; cached…
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmmandate.py
- MASTER.md
- CHANGELOG.md
