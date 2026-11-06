---
id: T-2137
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2135]
source: user
created: 2026-10-30T10:37:52Z
updated: 2026-10-31T02:29:24Z
base: 357a557a29afb467203b22fea0510aa8fc41eeed
base_tree: 66846682da3b08a1cc1678f80839205c464291a0
plan0_at: 2026-10-31T02:00:28Z
plan0_scope: []
verified: strong
---
# fm goal verdict: finished vs stopped with the stop's cause, deterministic; a done claim on an unfinished goal blocks once at Stop (Mission 4 brief 3)
## Raw request
> fm goal verdict: finished vs stopped with the stop's cause, deterministic; a done claim on an unfinished goal blocks once at Stop (Mission 4 brief 3)
## Interpretation
fm goal verdict (fmmandate) turns the goal ledger into one deterministic answer: finished only when every item has tasks, all of them done, every done-when check passes now (guarded, as fm goal show runs them), every clause of the goal's text is covered by an item (word overlap, so a clause no item mentions is unaccounted) and fm check's last recorded result is green; otherwise stopped with each cause named (item N has no task / open tasks / check fails / clause unaccounted / gates red or never run). At Stop, a done claim (the reply says done/finished/complete) while a goal stands with verdict stopped blocks once per claim with the cause, counted toward DRIVE_MAX like other drive blocks.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal verdict says finished only when every item's tasks are done, its done-when commands pass now, no clause is unaccounted and gates are green; otherwise stopped with the cause — verify with `python3 plugin/tests/run.py test_goal`
- [x] a done claim while the goal is stopped is blocked once and counts toward DRIVE_MAX — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: (1) verdict as a pure function over the ledger + one fm goal verdict verb and a Stop hook check reading a cached verdict (chosen: deterministic, cheap at Stop because it never runs checks there: it reads the last fm goal show/verdict result stored in meta with its tree id, and an unknown verdict doesn't block); (2) run all checks at Stop (too slow for a hook); (3) model-judged verdict (not deterministic). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] verdict rules, test-first (each cause from seeded events)
2. [x] Stop: a done claim on a stopped goal blocks once; drive names 'plan item N' when the queue is empty
3. [x] docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 11 tests in 4.7s (3 classes, 16 at a time; slowest: Goal 4s, GoalReview 4s, GenesisDraft 0s) / OK [ran] [tree 35767c229ebc] (2026-10-31T02:04:05Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 215 tests in 68.2s (28 classes, 16 at a time; slowest: Stop 68s, NoTaskGate 46s, PreToolUse 32s) / OK [ran] [tree 35767c229ebc] (2026-10-31T02:05:14Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_compact test_docs test_drive_side test_edit_cards test_goal test_guard_cases test_guard_evasions test_hooks test_mandate test_memory test_onwrite test_paused test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.51s] [ran] [tree 35767c229ebc] (2026-10-31T02:06:55Z)
- (ac 1) `python3 plugin/tests/run.py test_goal 2>&1 | tail -25` → exit 0 · Ran 12 tests in 10.9s (3 classes, 16 at a time; slowest: GoalReview 10s, Goal 8s, GenesisDraft 0s) / OK [ran] [tree 49d6233a4034] (2026-10-31T02:11:43Z)
- (step 3) `python3 plugin/tests/run.py test_goal 2>&1 | tail -25` → exit 0 · Ran 12 tests in 10.9s (3 classes, 16 at a time; slowest: GoalReview 10s, Goal 8s, GenesisDraft 0s) / OK [ran] [tree 49d6233a4034] (2026-10-31T02:11:43Z)
- (ac 1) `python3 plugin/tests/run.py test_goal 2>&1 | tail -12` → exit 0 · Ran 12 tests in 9.8s (3 classes, 16 at a time; slowest: GoalReview 9s, Goal 8s, GenesisDraft 0s) / OK [ran] [tree b565e6057807] (2026-10-31T02:11:57Z)
- `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 224 tests in 34.3s (31 classes, 16 at a time; slowest: Stop 33s, NoTaskGate 24s, PreToolUse 19s) / OK (start tree + this task's tests) [ran] [tree 66846682da3b] (2026-10-31T02:23:41Z)
- `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 224 tests in 33.4s (31 classes, 16 at a time; slowest: Stop 33s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 66846682da3b] (2026-10-31T02:23:41Z)
- `python3 plugin/tests/run.py test_goal test_hooks` → ✗ exit 1 · Ran 227 tests in 34.9s (31 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree fa0f47b49100] (2026-10-31T02:25:53Z)
- `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 227 tests in 34.4s (31 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree fa0f47b49100] (2026-10-31T02:25:53Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_close_gates` → exit 0 · Ran 244 tests in 35.0s (33 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree fa0f47b49100] (2026-10-31T02:26:40Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_close_gates` → exit 0 · Ran 244 tests in 35.1s (33 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree fa0f47b49100] (2026-10-31T02:27:16Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_close_gates` → exit 0 · Ran 244 tests in 35.3s (33 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree fa0f47b49100] (2026-10-31T02:27:51Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 12 tests in 3.3s (3 classes, 16 at a time; slowest: GoalReview 3s, Goal 2s, GenesisDraft 0s) / OK [ran] [tree fa0f47b49100] (2026-10-31T02:28:29Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 215 tests in 34.1s (28 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree fa0f47b49100] (2026-10-31T02:28:29Z)
- (audit intent) `fm-reviewer five lenses on the branch: changes needed, fixed in 599901f9: the stored verdict is bound to the goal's set_at and cleared by put/clear/no-goal, check_run must come from this tree (ledger_events over the whole ledger), the hold-once key is salted with set_at and session, the gate is wrapped so Stop can't break, clauses need 2 shared words across item text, done-when and task titles, an item is done only with a done task and none open (dropped ignored), no goal exits 2; test_goal test_mandate test_hooks test_close_gates green; red-to-green proven` → fm goal verdict is finished only with every item done, checks passing now, clauses covered and gates green on this tree, else stopped with each cause; a done claim on a stopped goal blocks once at Stop [tree fa0f47b49100] (2026-10-31T02:28:29Z)
- (audit adversary) `fm-reviewer five lenses on the branch: changes needed, fixed in 599901f9: the stored verdict is bound to the goal's set_at and cleared by put/clear/no-goal, check_run must come from this tree (ledger_events over the whole ledger), the hold-once key is salted with set_at and session, the gate is wrapped so Stop can't break, clauses need 2 shared words across item text, done-when and task titles, an item is done only with a done task and none open (dropped ignored), no goal exits 2; test_goal test_mandate test_hooks test_close_gates green; red-to-green proven` → check_run can't be forged by fm log (T-2244) and must match this tree; a verdict for a replaced, cleared or ended goal never blocks; causes are plain'd [tree fa0f47b49100] (2026-10-31T02:28:29Z)
- (audit edge) `fm-reviewer five lenses on the branch: changes needed, fixed in 599901f9: the stored verdict is bound to the goal's set_at and cleared by put/clear/no-goal, check_run must come from this tree (ledger_events over the whole ledger), the hold-once key is salted with set_at and session, the gate is wrapped so Stop can't break, clauses need 2 shared words across item text, done-when and task titles, an item is done only with a done task and none open (dropped ignored), no goal exits 2; test_goal test_mandate test_hooks test_close_gates green; red-to-green proven` → other-tree greens, stale verdicts, dropped-only items, a corrupt gate.json, the same causes in a later session all tested [tree fa0f47b49100] (2026-10-31T02:28:29Z)
- (audit operator) `fm-reviewer five lenses on the branch: changes needed, fixed in 599901f9: the stored verdict is bound to the goal's set_at and cleared by put/clear/no-goal, check_run must come from this tree (ledger_events over the whole ledger), the hold-once key is salted with set_at and session, the gate is wrapped so Stop can't break, clauses need 2 shared words across item text, done-when and task titles, an item is done only with a done task and none open (dropped ignored), no goal exits 2; test_goal test_mandate test_hooks test_close_gates green; red-to-green proven` → Stop reads meta only, no checks or git, and yields at DRIVE_MAX [tree fa0f47b49100] (2026-10-31T02:28:29Z)
- (audit maintainer) `fm-reviewer five lenses on the branch: changes needed, fixed in 599901f9: the stored verdict is bound to the goal's set_at and cleared by put/clear/no-goal, check_run must come from this tree (ledger_events over the whole ledger), the hold-once key is salted with set_at and session, the gate is wrapped so Stop can't break, clauses need 2 shared words across item text, done-when and task titles, an item is done only with a done task and none open (dropped ignored), no goal exits 2; test_goal test_mandate test_hooks test_close_gates green; red-to-green proven` → verdict reuses drift's guarded checks; one item-done rule shared with T-2139 [tree fa0f47b49100] (2026-10-31T02:28:29Z)
## Log
- 2026-10-30T10:37:52Z created
- 2026-10-31T02:00:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2137.builder.md
- 2026-10-31T02:00:28Z focused
- 2026-10-31T02:24:00Z steer: criterion 2's verify named test_hooks_stop, which doesn't exist; the Stop tests live in test_hooks (class Stop)
- 2026-10-31T02:24:37Z merged worktree-agent-abeed10a9b1edd511 (7 file(s))
- 2026-10-31T02:24:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abeed10a9b1edd511
- 2026-10-31T02:24:43Z focused
- 2026-10-31T02:27:51Z scope: plugin/lib/fmmandate.py (verdict), plugin/lib/fmhooks.py (_goal_gate), plugin/lib/fmcli.py (verdict parser), plugin/tests/test_goal.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md
- 2026-10-31T02:29:24Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2138 [FEATURE M, done, 2 steps] Stop wiring: a done claim while the last request has unaccounted clauses blocks once with them (Mission 4 brief 4) — lesson: A freshnes…
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-2138-review: Verdict: approve with nits.** The gate does what the acceptance criterion says. I did not run the tests. The nits below are scope and test gaps, …
## Lessons
- A cached verdict a hook trusts must carry what it was computed for (goal id, tree) and be dropped when that changes
## Files touched
- plugin/tests/test_goal.py
- plugin/tests/test_hooks.py
- plugin/lib/fmmandate.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- MASTER.md
- CHANGELOG.md
