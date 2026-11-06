---
id: T-1316
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T00:29:18Z
updated: 2026-10-22T16:44:51Z
base: 50ff43b3423a521e1a8c98508cea2a1627724f3c
base_tree: 9697b3331b2ab6037453ea5547857bef54f45431
plan0_at: 2026-10-22T16:37:13Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app: bracketed paste into the prompt
## Raw request
> pasting multi-line text in prompt mode submits at the first newline, and the remaining lines then arrive as hotkeys (`q`, `s` and so on). Bracketed paste is not handled
> (noticed by an agent; research T-1300-review)
## Interpretation
fm code's app reads keys raw; a multi-line paste into prompt mode submits at the first newline and the remaining lines arrive as hotkeys (q quits, s stops). Terminals support bracketed paste (ESC[?2004h on; pasted text arrives between ESC[200~ and ESC[201~).
## Assumptions (confidence)
## Acceptance criteria
- [x] a bracketed paste of three lines into the prompt lands as one multi-line entry, nothing submitted and no hotkey fired; outside the prompt a paste fires nothing — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Paste`
- [x] the app turns bracketed paste on at start and off at exit — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Paste.test_modes_on_and_off`
## Non-goals
## Approach (options → choice → why)
Turn bracketed paste on with the app's other terminal modes (and off on exit, including on a crash path that restores the terminal); the key reader collects everything between 200~ and 201~ as one paste event; prompt mode inserts it with newlines kept (no submit), other modes ignore it (never as hotkeys). Options: heuristics on key timing (unreliable over ssh) → rejected; disabling hotkeys while the prompt is open (still submits at the first newline) → rejected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] paste mode on/off with the other modes
3. [x] reader collects a paste; prompt inserts it
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → ✗ exit 1 · Ran 4 tests in 0.113s / FAILED (failures=3, errors=1) [ran] [tree 81330784ed13] (2026-10-22T16:39:06Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Paste.test_modes_on_and_off` → exit 0 · Ran 1 test in 0.222s / OK [ran] [tree 69d8fe9714d5] (2026-10-22T16:41:36Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.227s / OK [ran] [tree 69d8fe9714d5] (2026-10-22T16:41:39Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → ✗ exit 1 · Ran 5 tests in 0.136s / FAILED (failures=3, errors=2) (start tree + this task's tests) [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:20Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.246s / OK [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.218s / OK [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:21Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.Paste.test_modes_on_and_off` → exit 0 · Ran 1 test in 0.204s / OK [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:22Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.222s / OK [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.218s / OK [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:24Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.218s / OK [ran] [tree 2a993dbb9c15] (2026-10-22T16:44:25Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Paste` → exit 0 · Ran 5 tests in 0.219s / OK [ran] [tree 56f841d41205] (2026-10-22T16:44:33Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.Paste.test_modes_on_and_off` → exit 0 · Ran 1 test in 0.202s / OK [ran] [tree 56f841d41205] (2026-10-22T16:44:33Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove; a pty test checks ESC[?2004h then ESC[?2004l on a clean exit and on a raise; merged; Paste tests green.` → pasted ESC and control characters are dropped before they reach the screen; 64 KB cap at every layer; a missing end marker times out after 1 s instead of swallowing every later key [tree 56f841d41205] (2026-10-22T16:44:33Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove; a pty test checks ESC[?2004h then ESC[?2004l on a clean exit and on a raise; merged; Paste tests green.` → a paste containing ESC[201~ ends early (terminals don't send it); the modes live in fmcodeterm.py since T-1300 [tree 56f841d41205] (2026-10-22T16:44:33Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove; a pty test checks ESC[?2004h then ESC[?2004l on a clean exit and on a raise; merged; Paste tests green.` → no submit and no hotkey on paste; outside the prompt a paste does nothing [tree 56f841d41205] (2026-10-22T16:44:33Z)
## Log
- 2026-10-21T00:29:18Z created
- 2026-10-22T16:02:00Z planned from capture
- 2026-10-22T16:02:07Z blocked: waits for T-1302's lane to merge (both edit fmcodetui.py); unblock after, with T-1468
- 2026-10-22T16:10:08Z set status=planned
- 2026-10-22T16:36:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1316.builder.md
- 2026-10-22T16:37:12Z focused
- 2026-10-22T16:41:42Z scope: plugin/lib/fmcodeterm.py added: the terminal modes (ENTER/LEAVE) and the key reader live there since T-1300, not in fmcodetui.py
- 2026-10-22T16:44:15Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcodeterm.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-22T16:44:16Z merged worktree-agent-a1640dde1fa8e253b (3 file(s))
- 2026-10-22T16:44:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1640dde1fa8e253b
- 2026-10-22T16:44:18Z focused
- 2026-10-22T16:44:49Z done
- 2026-10-22T16:44:51Z committed cbaf7878 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- research T-1330-review: Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands. [stale: plugin/lib/fm…
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcodeterm.py, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Why not caught
no test pasted into the prompt; T-1300's review noticed it
## Lessons
- Raw-key TUIs need bracketed paste from the start: without it, pasted text is a stream of hotkeys.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
