---
id: T-3030
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_hooks.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-04T22:15:19Z
updated: 2026-11-06T14:25:21Z
base: c53e668e206bbfea1192eb1c5f82f104836d8594
base_tree: 6e5108b3f12c924080fafa7ad405dfb971e364ed
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:46:28Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_hooks.py, CHANGELOG.md]
builder_returned: 2026-11-06T13:21:14Z
lane_stop: merged 2026-11-06T14:21:11Z
verified: strong
---
# An edit made while sampo task finish runs is warned and never attributed to the task being closed
## Raw request
> An edit made while a long sampo task finish runs is attributed to the task being closed (finish focuses it), which stales that close's own audits and pulls the file into its commit; T-2995's close failed this way when T-3028's test edit landed mid-check. Either finish shouldn't need the focus, or the hook should warn that a close is running and attribute nothing to it
## Interpretation
Finish focuses its task, so edits during it are attributed to it. Mark the close; the hook then attributes nothing.
## Assumptions (confidence)
## Acceptance criteria
- [x] while sampo task finish ID runs (a closing marker in meta with its pid, read through c.gates_live's key form), an edit in the project gets the note 'a close of ID is running: this edit isn't part of it' and is not journalled to ID, so ID's audits stay fresh and its commit leaves the file out; with no close running, attribution is as today; a stale marker (dead pid) counts as none — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: snapshot at finish start (touches audits and commit logic, large) vs a closing marker read by the edit hook (small). Chose the marker: finish writes meta closing{task,pid}, cleared in finally; hook reads it via gates_live(key=closing), notes and journals the edit to no task. Dead pid = none.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in test_hooks: an edit under a live closing marker is not journalled to the closing task and gets the note; a dead pid's marker is ignored
2. [x] finish writes and clears the closing marker; the edit hook reads it (gates_live key='closing') beside _gates_note
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.ClosingMarker` → ✗ exit 1 · Ran 2 tests in 67.3s (1 jobs, 16 at a time; slowest: ClosingMarker 1s) / FAILED (1 classes: test_hooks.ClosingMarker) [ran] [tree 2f4cbc577809] [world 2f1906870a] (2026-11-06T12:48:09Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.ClosingMarker` → ✗ exit 1 · Ran 2 tests in 53.5s (1 jobs, 16 at a time; slowest: ClosingMarker 2s) / FAILED (1 classes: test_hooks.ClosingMarker) [ran] [tree d612359b5725] [world 2f1906870a] (2026-11-06T12:49:24Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.ClosingMarker` → exit 0 · Ran 2 tests in 56.7s (1 jobs, 16 at a time; slowest: ClosingMarker 2s) / OK [ran] [tree e426c4d7b2ad] [world 2f1906870a] (2026-11-06T12:50:34Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_compact test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.91s] [ran] [tree e426c4d7b2ad] [world 2f1906870a] (2026-11-06T12:53:44Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.ClosingMarker` → ✗ exit 1 · Ran 3 tests in 139.5s (1 jobs, 16 at a time; slowest: ClosingMarker 2s) / FAILED (1 classes: test_hooks.ClosingMarker) [ran] [tree 4b047bcdda76] [world 2f1906870a] (2026-11-06T13:15:29Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.ClosingMarker` → exit 0 · Ran 3 tests in 22.1s (1 jobs, 16 at a time; slowest: ClosingMarker 2s) / OK [ran] [tree e6bda7f2751b] [world 2f1906870a] (2026-11-06T13:16:00Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_compact test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [20.67s] [ran] [tree e6bda7f2751b] [world 2f1906870a] (2026-11-06T13:21:01Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 2953a27bc6b4] (2026-11-06T14:21:14Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 265 tests in 105.5s (216 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 5s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 2953a27bc6b4] [world 2f1906870a] (2026-11-06T14:23:03Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 2953a27bc6b4] (2026-11-06T14:23:03Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 2953a27bc6b4] (2026-11-06T14:23:03Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 2953a27bc6b4] (2026-11-06T14:23:03Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 2953a27bc6b4] (2026-11-06T14:23:03Z)
## Log
- 2026-11-04T22:15:19Z created
- 2026-11-05T02:56:53Z planned from capture
- 2026-11-05T02:56:54Z set approved=True
- 2026-11-05T02:56:54Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-11-05T02:56:54Z blocked: planned and approved; waits for a builder slot, and after T-3087's merge (cli.py)
- 2026-11-06T03:53:43Z unblocked
- 2026-11-06T12:46:25Z focused
- 2026-11-06T12:46:28Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T14:21:11Z merged worktree-agent-a8b27f89a4ff017c0 (3 file(s))
- 2026-11-06T14:21:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8b27f89a4ff017c0
- 2026-11-06T14:21:12Z focused
- 2026-11-06T14:21:14Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T14:21:14Z scope: widened at merge to the reviewed lane's own diff (928dd7fa2), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T14:25:17Z done
- 2026-11-06T14:25:21Z committed 10e7eac9a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2784 [FIX M, done, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's l…
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py, …
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing tests in test_hooks: an edit under a live closing marker is not journalled to the closing t…
- failed first: step 2 finish writes and clears the closing marker; the edit hook reads it (gates_live key='closing') besi…
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
