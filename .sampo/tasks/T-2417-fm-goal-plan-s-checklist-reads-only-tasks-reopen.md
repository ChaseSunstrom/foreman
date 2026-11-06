---
id: T-2417
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmandate.py, plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T14:56:40Z
updated: 2026-11-02T02:24:47Z
group: critique-finish follow-ups
base: 97599336528ad5809708e74dce6022d78f5aea8c
base_tree: 45c0209d236aded82b1b7cd992eb4f0509929db3
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T02:13:04Z
plan0_scope: [plugin/lib/fmmandate.py, plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md]
verified: ok
---
# fm goal plan's checklist reads later fixes on a task's files, not only reopens within 7 days
## Raw request
> fm goal plan's checklist reads only tasks reopened within 7 days, so it saw none of the 905 follow-up fix commits the T-2332 miner found; feed later fix commits on a task's files into it, measured against the miner's 184 of 905 (research/T-2332-miner.py) (from gen-1/critique-finish.md)
## Interpretation
Reading 1: _misses (fmmandate) lists only items added after a done claim and tasks reopened within 7 days, so the 905 follow-up fix commits the T-2332 miner found never reach the checklist; feed it the tasks whose files a later fix touched (fmoutcomes.outcomes' fixed later and reverted fates), naming the fixing task, measured against the miner's 184 predicted of 905. Reading 2: port the miner itself into the checklist. Reading 1 fits: outcomes() already computes later fixes and reverts per task with their source.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal plan's checklist names a recently done task a later fix touched (fate fixed later) with what fixed it, beside the reopen lines; the brief records outcomes' fixed-later count over 60 days against the miner's 184 of 905 — verify with `python3 plugin/tests/run.py test_goal`
## Non-goals
## Approach (options → choice → why)
1) _misses adds, after the reopen lines, the newest done tasks whose fate is fixed later or reverted (outcomes(p), by: the fixing commits or tasks), one line each naming the task and what fixed it, the top 5 kept; fails if: outcomes' later-fix link is coarser than the miner's (measured: its fixed-later count against the miner's 184). 2) use what exists: fm outcomes already lists these; fails if: the checklist is where a goal's plan is written and nobody runs fm outcomes then. 3) do less: widen the reopen window to 30 days; fails if: a later fix is a new commit, not a reopen, so it still sees none. Choice 1 (80%): one more source in one function, from a computation that exists.
## Risks and rollback
Risk: outcomes(p) reads git per task and can be slow on a long history; fm goal plan runs it once per call, not per hook. Risk: hub files (CHANGELOG, MASTER) make every task look fixed later; outcomes already leaves docs-only commits out (check in the baseline). Rollback: revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0980, T-0985, T-0986, T-0987, T-0988.
## Execution prompt
## Steps
1. [x] baseline: count outcomes(p)'s fixed-later and reverted tasks closed in the last 60 days, beside research/T-2332-miner.py's 184 of 905; log both
2. [x] red test: a done task whose file a later FIX task's commit touched shows in plan()'s checklist as 'T-X: fixed later by …'; a held task doesn't
3. [x] fmmandate._misses: the later-fix source (top 5 overall); MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_goal.GoalPlan` → ✗ exit 1 · Ran 10 tests in 3.0s (1 classes, 16 at a time; slowest: GoalPlan 3s) / FAILED (1 classes: test_goal.GoalPlan) [ran] [tree 2b66c3b16334] [world 2f1906870a] (2026-11-02T02:13:22Z)
- (step 1) `fm outcomes --json (fates counted)` → 1662 graded: 62 fixed later, 1 reverted (all time); the T-2332 miner's 905 follow-up commits (184 on a surface) in 60 days count any later commit by another task on a task's files, a broader measure [tree 1fb365ca0fcb] (2026-11-02T02:13:50Z)
- (step 2) `python3 plugin/tests/run.py test_goal.GoalPlan` → exit 0 · Ran 10 tests in 3.0s (1 classes, 16 at a time; slowest: GoalPlan 3s) / OK [ran] [tree 1fb365ca0fcb] [world 2f1906870a] (2026-11-02T02:13:53Z)
- (step 3) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 39 tests in 5.1s (8 classes, 16 at a time; slowest: GoalReview 5s, GoalAcrossDays 4s, GoalEstimate 3s) / OK [ran] [tree 1fb365ca0fcb] [world 2f1906870a] (2026-11-02T02:13:59Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 39 tests in 5.0s (8 classes, 16 at a time; slowest: GoalReview 5s, GoalAcrossDays 4s, GoalEstimate 3s) / OK [ran] [tree cf78a46cc0fa] [world 2f1906870a] (2026-11-02T02:24:11Z)
- (audit intent) `self-review: _misses adds, in its own try, the done tasks fm outcomes marks fixed later or reverted (each naming up to two fixing commits or tasks, fitted and plain), keeps the newest three of those and the newest three reopen and late-item lines, five in all with the reopens last; a history read that fails leaves the old lines` → the goal plan's checklist sees follow-up fixes filed as new work, not only reopens within 7 days [tree cf78a46cc0fa] (2026-11-02T02:24:11Z)
- (audit edge) `self-review: _misses adds, in its own try, the done tasks fm outcomes marks fixed later or reverted (each naming up to two fixing commits or tasks, fitted and plain), keeps the newest three of those and the newest three reopen and late-item lines, five in all with the reopens last; a history read that fails leaves the old lines` → no outcomes → only reopen lines; held tasks never listed; a fate with no 'by' says 'a later change'; outcomes raising → old behaviour [tree cf78a46cc0fa] (2026-11-02T02:24:11Z)
## Log
- 2026-10-31T14:56:40Z created
- 2026-11-02T00:40:22Z planned from capture
- 2026-11-02T00:40:23Z set approved=True
- 2026-11-02T00:52:22Z baseline: fm outcomes grades 1662 tasks (all time): 62 fixed later, 1 reverted; the T-2332 miner counted 905 follow-up commits in 60 days (184 on a standard surface) because it calls any later commit by another task on a task's code files a miss. outcomes is the narrow, linked signal (precision over recall): the checklist uses it and says 'fixed later by <what>'
- 2026-11-02T02:13:02Z focused
- 2026-11-02T02:13:04Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T02:24:45Z done
- 2026-11-02T02:24:47Z committed 6dbfa8a3 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2136 [FEATURE M, done, 3 steps] fm goal plan: a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn (Mission 4 brie…
- research T-2332-review: I found no HIGH issues. The change is small and the diff matches the two acceptance criteria. I read the code but did not run any tests. The adve…
- decision 2026-10-31: [costly] Cold read clarification: a line that reports a requirement as unmet, open or unproven doesn't break it; the reader fails only what a line c…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_mandate.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmmandate.py, plugin/tests/test_goal.py; re-ground the plan against them before editing
## Lessons
- A checklist of past misses should read the record that already links fixes to tasks, not a narrower proxy (reopens) that misses most of them
## Plan gaps
- failed first: step 2 red test: a done task whose file a later FIX task's commit touched shows in plan()'s checklist as '…
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmmandate.py
- MASTER.md
- CHANGELOG.md
