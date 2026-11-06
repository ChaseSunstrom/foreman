---
id: T-2136
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2135]
source: user
created: 2026-10-30T10:37:52Z
updated: 2026-10-31T03:09:13Z
base: 13a39d0214854895d6ad0f23b81d7f060b059aad
base_tree: 5670d03efa7da689e54dbd5a13a80ada480b806b
plan0_at: 2026-10-31T02:42:38Z
plan0_scope: []
verified: strong
---
# fm goal plan: a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn (Mission 4 brief 2)
## Raw request
> fm goal plan: a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn (Mission 4 brief 2)
## Interpretation
fm goal plan proposes the standing goal's contents list instead of the session inventing it: (a) user items, one per clause of the goal's own words (m['clauses']); (b) standard items, the finish standard gen-0 names (tests, docs: MASTER/README/CHANGELOG, a site page if user-facing, a pane/status surface if it has state, every surface it belongs on), each kept only for a surface fmmission.surfaces finds in this repo; (c) model items from one tool-less child's best-in-class list for this kind of goal, kept only when the item names something the repo has (a path, a surface or an fm verb that exists), else shown as a proposal, never added; plus (d) checklist lines from the project's past misses: items added to a goal after a done claim and tasks reopened within 7 days. It prints the plan tagged user/standard/model; --apply adds the items it kept (each still needs its --done-when).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal plan tags each item user/standard/model, keeps a model item only when it names something the repo has, and adds the project's past misses as checklist lines — verify with `python3 plugin/tests/run.py test_goal`
## Non-goals
## Approach (options → choice → why)
Options: (1) a plan verb that composes the three sources and prints, --apply adds (chosen: the session reviews before the ledger changes; deterministic parts tested directly, the child stubbed); (2) auto-add on fm goal set (no review, noisy); (3) model-only plan (ungrounded). Choice 1. The child's reply is untrusted: only lines naming an existing path/surface/verb become items.
## Risks and rollback
## Execution prompt
## Steps
1. [x] user clauses + the finish standard from fmmission.surfaces, test-first
2. [x] a tool-less child's best-in-class list, grounded or shown as a proposal (child stubbed in tests)
3. [x] misses: items added after a done claim, tasks reopened within 7 days; top misses become checklist lines; docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → ✗ exit 1 · Ran 23 tests in 3.4s (5 classes, 16 at a time; slowest: GoalReview 3s, Goal 2s, GoalAcrossDays 2s) / FAILED (1 classes) [ran] [tree c7dea756258d] (2026-10-31T02:43:58Z)
- (ac 1) `python3 plugin/tests/run.py test_goal 2>&1 | grep -B3 -A18 "^FAIL\|^ERROR" | head -80` → ✗ exit 1 · Ran 23 tests in 3.3s (5 classes, 16 at a time; slowest: GoalReview 3s, Goal 2s, GoalAcrossDays 2s) / FAILED (1 classes) [ran] [tree 17b2efafa1e3] (2026-10-31T02:44:04Z)
- (step 3) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 23 tests in 3.4s (5 classes, 16 at a time; slowest: GoalReview 3s, Goal 2s, GoalAcrossDays 2s) / OK [ran] [tree aa87f8ed2731] (2026-10-31T02:44:36Z)
- `python3 plugin/tests/run.py test_goal` → ✗ exit 1 · Ran 26 tests in 4.2s (5 classes, 16 at a time; slowest: GoalReview 3s, Goal 2s, GoalAcrossDays 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5f5f381ac117] (2026-10-31T03:07:26Z)
- `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 26 tests in 3.3s (5 classes, 16 at a time; slowest: GoalReview 3s, GoalPlan 3s, Goal 2s) / OK [ran] [tree 5f5f381ac117] (2026-10-31T03:07:26Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate test_mission test_cli` → exit 0 · Ran 169 tests in 18.9s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 8s) / OK [ran] [tree 5f5f381ac117] (2026-10-31T03:07:57Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mandate test_mission test_cli` → exit 0 · Ran 169 tests in 18.9s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 8s) / OK [ran] [tree 5f5f381ac117] (2026-10-31T03:08:16Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_mandate test_mission test_cli` → exit 0 · Ran 169 tests in 18.8s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 8s) / OK [ran] [tree 5f5f381ac117] (2026-10-31T03:08:35Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 26 tests in 3.3s (5 classes, 16 at a time; slowest: GoalReview 3s, GoalPlan 3s, Goal 2s) / OK [ran] [tree 5f5f381ac117] (2026-10-31T03:08:39Z)
- (audit intent) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 2c7b8934: a kept model item is built from its grounded token (the model's sentence only under proposals), grounding needs a tracked path with a slash or extension inside the repo, a surface as a whole word or a real fm verb, a new goal resets the done claim, dedupe is normalized and within-run, malformed event times are skipped; --apply goes through add_item (guarded, runnable check); a sensitive project gets no model call; test_goal test_mandate test_mission test_cli green; red-to-green proven` → fm goal plan proposes user, standard and grounded model items plus a checklist from past misses; --apply adds them with a check [tree 5f5f381ac117] (2026-10-31T03:08:39Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 2c7b8934: a kept model item is built from its grounded token (the model's sentence only under proposals), grounding needs a tracked path with a slash or extension inside the repo, a surface as a whole word or a real fm verb, a new goal resets the done claim, dedupe is normalized and within-run, malformed event times are skipped; --apply goes through add_item (guarded, runnable check); a sensitive project gets no model call; test_goal test_mandate test_mission test_cli green; red-to-green proven` → the child's reply never becomes item text; only a grounded token does; nothing it says runs [tree 5f5f381ac117] (2026-10-31T03:08:39Z)
- (audit edge) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 2c7b8934: a kept model item is built from its grounded token (the model's sentence only under proposals), grounding needs a tracked path with a slash or extension inside the repo, a surface as a whole word or a real fm verb, a new goal resets the done claim, dedupe is normalized and within-run, malformed event times are skipped; --apply goes through add_item (guarded, runnable check); a sensitive project gets no model call; test_goal test_mandate test_mission test_cli green; red-to-green proven` → plain words and ../ paths don't ground, duplicates in one reply, the 7-day reopen boundary, a replaced goal, a garbage timestamp [tree 5f5f381ac117] (2026-10-31T03:08:39Z)
- (audit maintainer) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 2c7b8934: a kept model item is built from its grounded token (the model's sentence only under proposals), grounding needs a tracked path with a slash or extension inside the repo, a surface as a whole word or a real fm verb, a new goal resets the done claim, dedupe is normalized and within-run, malformed event times are skipped; --apply goes through add_item (guarded, runnable check); a sensitive project gets no model call; test_goal test_mandate test_mission test_cli green; red-to-green proven` → --apply reuses add_item, so every item gets the guard's stored-command check [tree 5f5f381ac117] (2026-10-31T03:08:39Z)
## Log
- 2026-10-30T10:37:52Z created
- 2026-10-31T02:42:04Z set approved=True
- 2026-10-31T02:42:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2136.builder.md
- 2026-10-31T02:42:38Z focused
- 2026-10-31T03:07:13Z merged worktree-agent-a7a4614a0418ef328 (5 file(s))
- 2026-10-31T03:07:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7a4614a0418ef328
- 2026-10-31T03:07:17Z focused
- 2026-10-31T03:08:35Z scope: plugin/lib/fmmandate.py (plan, _grounded, _misses, the goal_verdict event), plugin/lib/fmcli.py (plan), plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md
- 2026-10-31T03:09:13Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
## Lessons
- Grounding a model's line must turn the grounded fact into the item, not bless the whole sentence that mentioned it
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmmandate.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
