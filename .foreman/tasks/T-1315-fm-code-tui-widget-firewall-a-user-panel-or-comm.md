---
id: T-1315
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py]
depends_on: [T-1306]
source: followup
created: 2026-10-21T00:23:07Z
updated: 2026-10-21T04:48:15Z
base: 915b65128f2c16449afeab3db2b26428a3931459
base_tree: d6c20d081e07b51fa5b63ae08b01751e76f4eb67
plan0_at: 2026-10-21T04:25:18Z
plan0_scope: [plugin/lib/fmcodetui.py]
verified: strong
---
# fm code tui widget firewall: a user extension's panel, command or event handler that fails or runs slow is reported and switched off, never taking the screen down
## Raw request
> fm code tui widget firewall: a user panel or command from ~/.claude/foreman/tui/*.py that raises or runs long is shown as a red error box and disabled, never taking the screen down (C10)
## Interpretation
A user's own TUI extension (a .py in ~/.claude/foreman/tui/) adds panels, commands and event handlers. Today a panel that raises shows a one-line error (good), a handler that raises is dropped (good), but a command that raises takes the whole screen down (App.key calls it bare), and a panel or handler that is slow freezes every frame with no limit. The firewall: none of them can crash or freeze the screen; a failing or slow one is shown as an error and switched off for the session.
## Assumptions (confidence)
## Acceptance criteria
- [x] an extension command that raises is reported in Activity and switched off, and the screen keeps running — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] an extension panel slower than its budget on 3 frames running, a handler or a command over budget, is switched off with a note naming it and how long it took; built-in panels never are — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] an extension command that raises is reported in Activity and switched off, and the screen keeps running — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] an extension panel over its time budget on 3 frames running, or a handler or command over budget, is switched off with a note naming it and how long it took; built-in panels never are — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: A) try/except around commands only (fixes the crash, not the freeze); B) A plus a per-call time budget for panels, handlers and commands measured with time.monotonic: past the budget once (panels: 3 frames running) the extension's piece is switched off with a note in Activity (chosen: stdlib, no threads, matches how handlers are already dropped); C) run extensions in a thread with a timeout (can't stop a stuck thread in Python, and the canvas isn't thread-safe); D) a subprocess per extension (heavy, breaks the in-process API). Built-in panels are never switched off.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: a raising command, a slow panel, a slow handler, a slow command; built-ins untouched
2. [x] Guard calls: command try/except + budget, panel timing over 3 frames, handler budget; one note per switch-off
3. [x] Docs: the extension template and README name the budgets
4. [x] Failing tests: a raising command, a slow panel, a slow handler, a slow command; built-ins untouched
5. [x] Guard calls: command try/except + budget, panel timing over 3 frames, handler budget; one note per switch-off
6. [x] Docs: the extension template and README name the budgets
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_tui 2>&1 | tail -30` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (14.9 s; last 40 of 103 lines) [ran] [tree 35d35aa48588] (2026-10-21T04:26:37Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui 2>&1 | tail -30` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (14.9 s; last 40 of 103 lines) [ran] [tree 35d35aa48588] (2026-10-21T04:26:37Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui 2>&1 | tail -30` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (14.9 s; last 40 of 103 lines) [ran] [tree 35d35aa48588] (2026-10-21T04:26:37Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui 2>&1 | tail -30` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (14.9 s; last 40 of 103 lines) [ran] [tree 35d35aa48588] (2026-10-21T04:26:37Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "^(FAIL|ERROR|Assertion|Ran)"` → ✗ exit 1 · Ran 82 tests in 17.3s (13 classes, 16 at a time; slowest: Fuzz 17s, Command 8s, Events 6s) / FAILED (1 classes) [ran] [tree e22ff9369273] (2026-10-21T04:27:01Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "^(FAIL|ERROR|Assertion|Ran)"` → ✗ exit 1 · Ran 82 tests in 17.3s (13 classes, 16 at a time; slowest: Fuzz 17s, Command 8s, Events 6s) / FAILED (1 classes) [ran] [tree e22ff9369273] (2026-10-21T04:27:01Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "^(FAIL|ERROR|Assertion|Ran)"` → ✗ exit 1 · Ran 82 tests in 17.3s (13 classes, 16 at a time; slowest: Fuzz 17s, Command 8s, Events 6s) / FAILED (1 classes) [ran] [tree e22ff9369273] (2026-10-21T04:27:01Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "^(FAIL|ERROR|Assertion|Ran)"` → ✗ exit 1 · Ran 82 tests in 17.3s (13 classes, 16 at a time; slowest: Fuzz 17s, Command 8s, Events 6s) / FAILED (1 classes) [ran] [tree e22ff9369273] (2026-10-21T04:27:01Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 82 tests in 19.9s (13 classes, 16 at a time; slowest: Fuzz 19s, Command 9s, Events 7s) / FAILED (1 classes) [ran] [tree e22ff9369273] (2026-10-21T04:27:23Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 28.3s (13 classes, 16 at a time; slowest: Fuzz 28s, Command 10s, Events 7s) / OK [ran] [tree 82c53bebc799] (2026-10-21T04:28:48Z)
- (step 3) `grep -n 'switched off' README.md plugin/templates/tui/cost_meter.py` → exit 0 · README.md:309:- `fm code tui "make calc.add add"` runs the same loop in a terminal UI: a track of the stations, check chips, change bars, a time chart and tokens per call, with the diff (`d`), past ru [ran] [tree 94546547e833] (2026-10-21T04:29:06Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 58.9s (13 classes, 16 at a time; slowest: Fuzz 58s, Command 28s, Events 18s) / OK [ran] [tree 07522c38859e] (2026-10-21T04:32:51Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 18.2s (13 classes, 16 at a time; slowest: Fuzz 18s, Command 8s, Events 7s) / OK [ran] [tree 2d232c31c9d2] (2026-10-21T04:43:53Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 15.0s (13 classes, 16 at a time; slowest: Fuzz 15s, Command 9s, Events 6s) / OK [ran] [tree 2d232c31c9d2] (2026-10-21T04:44:14Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 13.9s (13 classes, 16 at a time; slowest: Fuzz 14s, Command 8s, Events 6s) / OK [ran] [tree 2d232c31c9d2] (2026-10-21T04:44:29Z)
- (step 6) `grep -c 'switched off' README.md plugin/templates/tui/cost_meter.py` → exit 0 · README.md:1 / plugin/templates/tui/cost_meter.py:1 [ran] [tree 2d232c31c9d2] (2026-10-21T04:44:30Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 23.9s (13 classes, 16 at a time; slowest: Fuzz 23s, Command 14s, Events 11s) / OK [ran] [tree 564275203999] (2026-10-21T04:45:18Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 23.9s (13 classes, 16 at a time; slowest: Fuzz 23s, Command 14s, Events 11s) / OK [ran] [tree 564275203999] (2026-10-21T04:45:18Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 23.9s (13 classes, 16 at a time; slowest: Fuzz 23s, Command 14s, Events 11s) / OK [ran] [tree 564275203999] (2026-10-21T04:45:18Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 82 tests in 23.9s (13 classes, 16 at a time; slowest: Fuzz 23s, Command 14s, Events 11s) / OK [ran] [tree 564275203999] (2026-10-21T04:45:18Z)
- (audit intent) `self: read the full diff; budgets are named constants; built-ins identified by function identity so an extension that replaces a built-in name can still be switched off; strikes counted once per frame` → every criterion (raising command, slow panel/handler/command, built-ins untouched) has a test that failed first and passes [tree 564275203999] (2026-10-21T04:45:18Z)
- (audit edge) `self: read the full diff; budgets are named constants; built-ins identified by function identity so an extension that replaces a built-in name can still be switched off; strikes counted once per frame` → a stuck extension that never returns still freezes the screen (accepted, documented) [tree 564275203999] (2026-10-21T04:45:18Z)
- (audit operator) `self: read the full diff; budgets are named constants; built-ins identified by function identity so an extension that replaces a built-in name can still be switched off; strikes counted once per frame` → a switched-off command stays listed in the keys view (cosmetic, left) [tree 564275203999] (2026-10-21T04:45:18Z)
- (audit maintainer) `self: read the full diff; budgets are named constants; built-ins identified by function identity so an extension that replaces a built-in name can still be switched off; strikes counted once per frame` → tests patch budgets below 1 ms and sleep 10 ms, so they're fast and not load-sensitive [tree 564275203999] (2026-10-21T04:45:18Z)
## Log
- 2026-10-21T00:23:07Z created
- 2026-10-21T03:43:28Z planned from capture
- 2026-10-21T03:45:33Z set depends_on=['T-1306']
- 2026-10-21T04:24:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1315.builder.md
- 2026-10-21T04:25:16Z focused
- 2026-10-21T04:43:01Z merged worktree-agent-afc54fa8823a66813 (4 file(s))
- 2026-10-21T04:43:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afc54fa8823a66813
- 2026-10-21T04:43:31Z focused
- 2026-10-21T04:44:45Z scope: CHANGELOG.md — every task adds its line
- 2026-10-21T04:48:13Z done
- 2026-10-21T04:48:15Z committed eec9ab25 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- research brainstorm-20261020-tui: Method.** I read all of ideas.md (about 560 distinct titles; near-duplicates are merged with "/"). I grepped fmcodetui.py and fmcode.py…
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- decision 2026-10-20: Foreman Code's TUI (T-1283) is a stdlib curses client of fm code's --json event stream with a widget layer that themes and extensions build on; exte…
## Preflight
Changed in scope since this was planned (2026-10-21): plugin/lib/fmcodetui.py; re-ground the plan against them before editing
## Lessons
- A firewall around user code needs a budget per call kind and a strike count for the per-frame one, or one GC pause switches a panel off
## Plan gaps
- failed first: step 1 Failing tests: a raising command, a slow panel, a slow handler, a slow command; built-ins untouched
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/templates/tui/cost_meter.py
- README.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- plugin/tests/test_release.py
