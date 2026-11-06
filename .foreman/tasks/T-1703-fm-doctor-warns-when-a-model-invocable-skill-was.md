---
id: T-1703
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/lib/fmcost.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: [T-1702]
source: user
created: 2026-10-22T22:36:40Z
updated: 2026-10-23T02:17:37Z
group: skills and routing
base: 9e51167be6b14d69fdba23c8d14b919b02ef455d
base_tree: 1d3005dc3d31bd2ca8a67319667a09494dc504a6
plan0_at: 2026-10-23T02:08:18Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/lib/fmcost.py, plugin/tests/test_doctor.py, CHANGELOG.md]
verified: strong
---
# fm doctor warns when a model-invocable skill was named often but never loaded in 30 days
## Raw request
> fm doctor warns when a model-invocable skill was named often but never loaded in 30 days
## Interpretation
A skill nobody loads is either mis-described or not needed; doctor should say so instead of letting it rot. Uses fm usage's named-not-loaded data.
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor warns for a skill with zero loads and more than N mentions in 30 days, and stays quiet otherwise; never deletes — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: auto-retire (premature); a report only. Choice: a warning with the counts.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] doctor check
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -5` → ✗ exit 1 · Ran 65 tests in 2.9s (22 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, LockProbe 1s) / FAILED (1 classes) [ran] [tree 675649e1d8a1] (2026-10-23T02:08:49Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 65 tests in 5.9s (22 classes, 16 at a time; slowest: Command 5s, ViewsRepair 4s, Fsck 2s) / OK [ran] [tree d36155fbe6e4] (2026-10-23T02:09:34Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_cost` → exit 0 · Ran 83 tests in 17.9s (29 classes, 16 at a time; slowest: TaskCostCap 17s, SkillUsage 6s, Command 5s) / OK [ran] [tree d36155fbe6e4] (2026-10-23T02:09:53Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_cost` → exit 0 · Ran 83 tests in 7.1s (29 classes, 16 at a time; slowest: TaskCostCap 7s, SkillUsage 2s, Command 2s) / OK [ran] [tree 16bf4648882a] (2026-10-23T02:17:16Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 65 tests in 2.4s (22 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, LockProbe 1s) / OK [ran] [tree 5622f090d89b] (2026-10-23T02:17:25Z)
- (audit intent) `self-review: counting reused from fm usage (note_skill factored out of cmd_usage), distinct sessions over 30 days, WARN never FAIL, user-only skills and the idle next skipped, nothing deleted; a chatty single session counts once (tested)` → doctor names skills offered often and never loaded, so a mis-described skill doesn't rot unseen [tree 5622f090d89b] (2026-10-23T02:17:25Z)
- (audit edge) `self-review: counting reused from fm usage (note_skill factored out of cmd_usage), distinct sessions over 30 days, WARN never FAIL, user-only skills and the idle next skipped, nothing deleted; a chatty single session counts once (tested)` → one session repeating a name counts once; a skill loaded once in the window never warns (deliberate); next excluded because the idle line names it every turn [tree 5622f090d89b] (2026-10-23T02:17:25Z)
- (audit self) `self-review: counting reused from fm usage (note_skill factored out of cmd_usage), distinct sessions over 30 days, WARN never FAIL, user-only skills and the idle next skipped, nothing deleted; a chatty single session counts once (tested)` → no findings [tree 5622f090d89b] (2026-10-23T02:17:25Z)
## Log
- 2026-10-22T22:36:40Z created
- 2026-10-22T22:36:41Z set scope=['plugin/lib/fmdoctor.py', 'plugin/lib/fmcost.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md']
- 2026-10-22T22:36:42Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T22:36:42Z set depends_on=['T-1702']
- 2026-10-23T02:08:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1703.builder.md
- 2026-10-23T02:08:17Z focused
- 2026-10-23T02:17:02Z merged worktree-agent-a977173735a41430b (3 file(s))
- 2026-10-23T02:17:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a977173735a41430b
- 2026-10-23T02:17:07Z focused
- 2026-10-23T02:17:35Z done
- 2026-10-23T02:17:37Z committed 5f30c5f9 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1698 [CLEAN S, done, 3 steps] Skill descriptions in task terms, and fm doctor's skills lint (Foreman jargon, overlapping descriptions) — lesson: Skill descriptions tri…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- likely tests for the scope: plugin/tests/test_cost.py, plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcost.py, plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Lessons
- Count offers per session, not per event, or an every-turn hint drowns the signal
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
