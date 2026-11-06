---
id: T-1226
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T16:46:57Z
updated: 2026-10-16T16:55:36Z
base: 45f0bb6d71bff10af0acea5ee5e07cfede2fbe35
base_tree: 2103ad59e7312364c0ab15877eb7b9ccf2305c8d
plan0_at: 2026-10-16T16:46:58Z
plan0_scope: []
verified: strong
---
# Chat approvals can't be self-granted: a non-interactive claude (claude --resume SID -p yes) or a scheduled yes-prompt never resolves a pending fm ask
## Raw request
> Chat approvals can't be self-granted: a non-interactive claude (claude --resume SID -p yes) or a scheduled yes-prompt never resolves a pending fm ask
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A pending fm ask isn't granted by a prompt from a -p/--print/stream-json Claude process, and the guard refuses CronCreate/ScheduleWakeup/RemoteTrigger prompts that read as a yes; an interactive yes still grants — verify with `python3 plugin/tests/run.py test_hooks test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: a print-mode process's yes doesn't grant; scheduled yes-prompts are refused; interactive yes grants
2. [x] Hook checks the Claude process's argv before resolving chat approvals; guard refuses yes-shaped scheduled prompts
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_prompt_claude_sends_itself -k test_a_scheduled_prompt -k test_yes_grants` → exit 0 · Ran 3 tests in 2.9s (1 classes, 16 at a time; slowest: Approvals 3s) / OK [ran] [tree d4b40109dc4b] (2026-10-16T16:53:06Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_session_fixes test_guard` → exit 0 · Ran 352 tests in 38.2s (83 classes, 16 at a time; slowest: Stop 38s, PreToolUse 22s, Approvals 17s) / OK [ran] [tree d4b40109dc4b] (2026-10-16T16:53:45Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 348 tests in 37.3s (79 classes, 16 at a time; slowest: Stop 37s, PreToolUse 21s, Approvals 17s) / OK [ran] [tree d4b40109dc4b] (2026-10-16T16:54:31Z)
- (audit adversary) `automated security review finding (chat approvals from non-user prompts) confirmed live: fm guard try allowed claude --resume <this session> -p yes. Fixed test-first; self-adversary pass found two bypasses of the first fix (a claude renamed bash, a pasted-block prefix) and closed them test-first; live check in this interactive session: not program-sent` → claude -r SID -p yes, --print, --output-format=stream-json, --input-format stream-json, a claude symlinked as bash with -p or -cp, CronCreate/ScheduleWakeup/RemoteTrigger 'yes'/'Yes, go ahead'/'ok' and a pasted-block prefix: none grants. Residual: typing into Claude's own terminal (tmux send-keys, a pty) is still a person-shaped prompt; the guard is a speed bump, not a sandbox [tree d4b40109dc4b] (2026-10-16T16:54:31Z)
- (audit edge) `automated security review finding (chat approvals from non-user prompts) confirmed live: fm guard try allowed claude --resume <this session> -p yes. Fixed test-first; self-adversary pass found two bypasses of the first fix (a claude renamed bash, a pasted-block prefix) and closed them test-first; live check in this interactive session: not program-sent` → a failing process check counts as program-sent (no approval, dialog still grants); no procfs falls back to ps args; a program-sent prompt leaves the pending ask pending instead of cancelling it [tree d4b40109dc4b] (2026-10-16T16:54:31Z)
- (audit operator) `automated security review finding (chat approvals from non-user prompts) confirmed live: fm guard try allowed claude --resume <this session> -p yes. Fixed test-first; self-adversary pass found two bypasses of the first fix (a claude renamed bash, a pasted-block prefix) and closed them test-first; live check in this interactive session: not program-sent` → IDE/desktop/web frontends that drive Claude Code through stream-json answer asks through the permission dialog, not a chat yes; Remote Control still types into the interactive process [tree d4b40109dc4b] (2026-10-16T16:54:31Z)
- (audit self) `automated security review finding (chat approvals from non-user prompts) confirmed live: fm guard try allowed claude --resume <this session> -p yes. Fixed test-first; self-adversary pass found two bypasses of the first fix (a claude renamed bash, a pasted-block prefix) and closed them test-first; live check in this interactive session: not program-sent` → no findings [tree d4b40109dc4b] (2026-10-16T16:54:31Z)
## Log
- 2026-10-16T16:46:57Z created
- 2026-10-16T16:46:58Z focused
- 2026-10-16T16:55:35Z done
- 2026-10-16T16:55:36Z committed b78a1f1a (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1157 [FEATURE M, done, 2 steps] Add `fm todo`, the list of what only the user can do (pending asks, blocked-on-user tasks, — lesson: a list of things to resolve needs …
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor. [stale: plugin/uninstall.sh changed since it wa…
## Lessons
- An approval channel is only as strong as its least-trusted writer: any path that can put text into the session's prompt (resume -p, schedulers) is a self-approval path until it is ruled out by origin
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_hooks.py
- plugin/hooks/hooks.json
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
