---
id: T-2255
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-31T02:10:02Z
updated: 2026-10-31T05:20:36Z
base: 12f054f65c7706a6f62924c7530d1af738f425c7
base_tree: 92f713364e06aea49566c7e5bfb7e0e22216d370
plan0_at: 2026-10-31T04:43:44Z
plan0_scope: []
verified: strong
---
# Catch it earlier: the builder ran test_execution, not test_close_gates, where T-1122's…
## Raw request
> T-2254 (fm task finish: a scope: log line claims its file again even while another task is open (T-1122), only Docs impact waits for others to close) wasn't caught before it shipped: the builder ran test_execution, not test_close_gates, where T-1122's test lives; ship59's full run caught it
## Interpretation
Tests that catch a file's breakage often live in modules not named after it (T-1122's test in test_close_gates for fmcli._claimed; budgets in test_doctor/test_playbook_use for rules and skills). The map learns such links from closed baseline-red tasks (T-2148 _broke), but a red ship run (ship59, ship62, ship63, ship64) files no baseline task, so each fix went through an ordinary task and nothing was learned; the next builder runs the same named tests and misses it again.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fm ship whose scratch-tree test fails captures one urgent baseline-red task naming the failing tests (the same text fm check writes, not twice for the same set), names it on the error line, and still pushes nothing; once that task is finished by a commit naming it, fm impact on the fix's file lists the failing test — verify with `python3 plugin/tests/run.py test_ship test_map`
## Non-goals
## Approach (options → choice → why)
1) fm ship's scratch-tree test keeps streaming its output but also keeps it (tee to a temp file, bounded), and on failure passes (cmd, code, output) to fmcli._baseline (the tree is the commit being shipped, so it's vouchable): one urgent baseline FIX naming the failing tests, the same text fm check writes; the ship's error line names the task id. Fixing it under that id feeds _broke, so fm impact and the close's linked tests include the test next time. 2) parse the CI log instead — rejected: later, remote, untrusted. 3) teach _broke to follow 'fixed by T-NNNN' drop reasons — deferred: the workflow fix covers new cases. Choice 1. Publish semantics unchanged: a failed test still pushes nothing.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: a stub test command that fails a named test in the scratch tree; the baseline task, its text and the no-push
2. [x] fm ship keeps the output and calls _baseline
3. [x] CHANGELOG, MASTER fm ship line
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_ship test_map test_close_gates` → exit 0 · Ran 47 tests in 27.2s (5 classes, 16 at a time; slowest: CloseGates 27s, Ship 26s, Map 5s) / OK [ran] [tree f0d44e83aaba] (2026-10-31T04:46:04Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs test_release test_ship && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [31.52s] [ran] [tree f0d44e83aaba] (2026-10-31T04:47:09Z)
- (step 3) `python3 plugin/tests/run.py test_ship test_close_gates test_affected_hubs 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → exit 0 · Ran 43 tests in 79.2s (3 classes, 16 at a time; slowest: Ship 79s, CloseGates 63s, AffectedHubs 3s) / OK [ran] [tree 2e36a56beeac] (2026-10-31T04:59:03Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_guard_cases test_paused test_release test_ship && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [48.41s] [ran] [tree 2e36a56beeac] (2026-10-31T05:02:06Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 25 tests in 55.0s (1 classes, 16 at a time; slowest: Ship 53s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d569b0b2f854] (2026-10-31T05:18:11Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 25 tests in 26.6s (1 classes, 16 at a time; slowest: Ship 26s) / OK [ran] [tree d569b0b2f854] (2026-10-31T05:18:11Z)
- (step 1) `python3 plugin/tests/run.py test_ship test_close_gates test_affected_hubs` → exit 0 · Ran 43 tests in 26.8s (3 classes, 16 at a time; slowest: Ship 26s, CloseGates 22s, AffectedHubs 2s) / OK [ran] [tree d569b0b2f854] (2026-10-31T05:18:48Z)
- (step 2) `python3 plugin/tests/run.py test_ship test_close_gates test_affected_hubs` → exit 0 · Ran 43 tests in 31.1s (3 classes, 16 at a time; slowest: Ship 31s, CloseGates 25s, AffectedHubs 2s) / OK [ran] [tree d569b0b2f854] (2026-10-31T05:19:19Z)
- (step 3) `grep -c T-2255 CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:1 [ran] [tree d569b0b2f854] (2026-10-31T05:19:19Z)
- (ac 1) `python3 plugin/tests/run.py test_ship test_map` → exit 0 · Ran 35 tests in 33.1s (4 classes, 16 at a time; slowest: Ship 33s, Map 5s, Cold 1s) / OK [ran] [tree d569b0b2f854] (2026-10-31T05:19:53Z)
- (audit intent) `self + one fm-reviewer pass (3 medium, 3 low, all fixed with tests)` → a red ship files the same urgent baseline task fm check writes and names it, so its fix feeds the map's learned links (T-2148); a green ship marks it green again (test_ship red-to-green) [tree d569b0b2f854] (2026-10-31T05:19:53Z)
- (audit adversary) `self + one fm-reviewer pass (3 medium, 3 low, all fixed with tests)` → publish semantics unchanged (no push after a failed test, grants untouched); failing names from the shipped tree's output are plained and fitted before they enter a task [tree d569b0b2f854] (2026-10-31T05:19:53Z)
- (audit edge) `self + one fm-reviewer pass (3 medium, 3 low, all fixed with tests)` → output goes to a temp file, so a test leaving a process on stdout can't hang the ship; a capture failure still ends with 'nothing was pushed'; an environment failure captures nothing [tree d569b0b2f854] (2026-10-31T05:19:53Z)
## Log
- 2026-10-31T02:10:02Z created
- 2026-10-31T04:43:25Z set tier=M
- 2026-10-31T04:43:26Z planned: it has criteria and steps
- 2026-10-31T04:43:30Z criterion 1 verify: `python3 plugin/tests/run.py test_release test_map` → `python3 plugin/tests/run.py test_ship test_map`
- 2026-10-31T04:43:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2255.builder.md
- 2026-10-31T04:43:43Z focused
- 2026-10-31T05:16:47Z merged worktree-agent-acfcbeb062159620b (5 file(s))
- 2026-10-31T05:16:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acfcbeb062159620b
- 2026-10-31T05:16:48Z focused
- 2026-10-31T05:19:19Z scope: plugin/lib/fmrelease.py (ship test run), plugin/lib/fmcli.py (_baseline names plained), plugin/tests/test_ship.py, MASTER.md, CHANGELOG.md
- 2026-10-31T05:20:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2254 [FIX S, done, 1 steps] fm task finish: a scope: log line claims its file again even while another task is open (T-1122), only Docs impact waits for others to clos…
- T-2148 [FIX M, done, 1 steps] Catch it earlier: T-2138 ran only test_hooks while iterating; the docs count lives in… — lesson: A file in every task's pairs carries no co…
- T-2267 [FEATURE S, done, 1 steps] fm task finish for a lane-merged task runs the always-on budget checks (test_doctor… — lesson: A folder link heuristic tuned on one rep…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
## Lessons
- Replacing an inherited stdout with a pipe changes when a run 'ends' (EOF, not exit): stream through a file when the child may leave a process behind
## Files touched
- plugin/lib/fmrelease.py
- plugin/tests/test_ship.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
