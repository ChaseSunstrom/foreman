---
id: T-0111
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_rank.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T03:05:24Z
updated: 2026-10-03T08:20:08Z
base: 17ed9d173e78583881191c736e55420bf4a61af6
base_tree: 29fdc5ba7500f20875ae1f9b4014ea0df499ff03
verified: ok
---
# Rank the inbox by value for effort within the intake type order
## Raw request
> Rank the inbox by value for effort
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] The inbox (fm state, fm next) puts urgent first, keeps the type order, ranks within a type by value (source, items depending on it, age) per tier effort, and never puts an item before a captured item it depends on — verify with `python3 plugin/tests/run.py -k test_rank`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] rank_inbox in state_dict and next_for
3. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Inbox ranking) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_rank` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: RankInbox 0s, Find 0s) / OK [ran] [tree 45b0ccbcef17] (2026-10-03T08:20:06Z)
- (step 2) `python3 plugin/tests/run.py -k test_rank` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: RankInbox 0s, Find 0s) / OK [ran] [tree 45b0ccbcef17] (2026-10-03T08:20:07Z)
- (step 3) `grep -q T-0111 MASTER.md && grep -q T-0111 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 45b0ccbcef17] (2026-10-03T08:20:07Z)
- (ac 1) `python3 plugin/tests/run.py -k test_rank` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: RankInbox 0s, Find 0s) / OK [ran] [tree 45b0ccbcef17] (2026-10-03T08:20:08Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:20 UTC); cached (fm check --fresh reruns) [ran] [tree 45b0ccbcef17] (2026-10-03T08:20:08Z)
- (audit self) `self: the test covers urgent-free type order (FIX before FEATURE), value per effort (S followup beats L user), a dependency pulling its dependent after it, and fm next agreeing; one ranking feeds fm state, INBOX.md, the dashboard and fm next` → no findings [tree 45b0ccbcef17] (2026-10-03T08:20:08Z)
## Log
- 2026-10-03T03:05:24Z created
- 2026-10-03T08:18:44Z planned from capture
- 2026-10-03T08:18:44Z focused
- 2026-10-03T08:20:08Z done
- 2026-10-03T08:20:08Z committed 96d4fad (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- research t0018-r4-edge: id":"8a23d3ef-86ad-40e5-8b8c-023d98996326","isSidechain":true,"agentId":"a885e6176c24d785f","message":{"model":"claude-sonnet-5","id":"msg_011CfS…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py; re-ground the plan against them before editing
## Lessons
- Rank inside the existing order rather than replacing it: the type order encodes a policy the value score can't see.
## Files touched
- plugin/tests/test_rank.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
