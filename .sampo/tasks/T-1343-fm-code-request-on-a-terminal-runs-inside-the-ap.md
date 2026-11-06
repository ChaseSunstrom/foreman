---
id: T-1343
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-21T03:47:30Z
updated: 2026-10-21T17:11:39Z
base: e276a24995b75b89ab1eaa762fcd4b1e7922cd0d
base_tree: fd55e9e77d93f4e18c99bfdd6f514f5ac2241247
plan0_at: 2026-10-21T13:40:35Z
plan0_scope: []
verified: strong
---
# fm code "<request>" on a terminal runs inside the app, like claude "<prompt>"; piped, --plain or --json stay plain lines
## Raw request
> fm code \"<request>\" on a terminal runs inside the app (U1, after T-1330): the same run view as n, piped or non-tty stays plain lines, fm code tui stays an alias, echo ctx | fm code \"req\" adds stdin as context
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] on a terminal, fm code "<request>" opens the app with that run going (a pty test with a fake model sees the screen and CLOSED); --plain on a terminal prints today's lines — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] piped or without a terminal, and with --json, fm code's output is unchanged — verify with `python3 plugin/tests/run.py test_code test_code_worker`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing pty test: fm code "fix add" --model fake on a terminal draws the app and closes
2. [x] cmd_code: a request on a terminal (no --json, --plain, --dry-plan) goes to fmcodetui.main; docs
## Resume here
<!-- auto -->
- 2026-10-21T16:51:42Z steps 2/2 done
- git: foreman/build; 1 uncommitted: CHANGELOG.md
## Docs impact
README.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k on_a_terminal test_code_tui` → ✗ exit 1 · Ran 97 tests in 46.0s (14 classes, 16 at a time; slowest: Command 45s, Fuzz 43s, Events 15s) / FAILED (1 classes) [ran] [tree cf82fa08dbde] (2026-10-21T13:44:20Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code test_code_worker` → ✗ exit 1 · Ran 201 tests in 109.8s (29 classes, 16 at a time; slowest: Worker 109s, Command 80s, Bench 44s) / FAILED (1 classes) [ran] [tree 3d705192a979] (2026-10-21T13:47:32Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code test_code_worker` → exit 0 · Ran 201 tests in 74.3s (29 classes, 16 at a time; slowest: Worker 74s, Bench 21s, Review 15s) / OK [ran] [tree 3d705192a979] (2026-10-21T13:50:13Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_code test_code_worker` → exit 0 · Ran 209 tests in 126.8s (29 classes, 16 at a time; slowest: Worker 126s, Bench 32s, Review 19s) / OK [ran] [tree 121ef7427f33] (2026-10-21T16:40:05Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code test_code_worker` → exit 0 · Ran 209 tests in 126.5s (29 classes, 16 at a time; slowest: Worker 126s, Bench 29s, Review 19s) / OK [ran] [tree 121ef7427f33] (2026-10-21T16:42:12Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 98 tests in 25.5s (14 classes, 16 at a time; slowest: Command 25s, Fuzz 21s, Events 10s) / OK [ran] [tree 06949f07bede] (2026-10-21T16:45:23Z)
- (ac 2) `python3 plugin/tests/run.py test_code test_code_worker` → exit 0 · Ran 209 tests in 154.4s (29 classes, 16 at a time; slowest: Worker 154s, Bench 42s, Review 30s) / OK [ran] [tree 06949f07bede] (2026-10-21T16:45:23Z)
- (audit edge) `self: read the builder's diff; the app branch in cmd_code needs a request, both stdin and stdout on a terminal and none of --resume/--task/--json/--plain/--dry-plan; the app's own child runs fm code --json with stdin closed, so it never reopens the app; two pty tests (app, --plain) plus the unchanged piped suites pass on the merged tree` → in the app, q exits 0 even after a blocked run, so 'fm code x && …' typed on a terminal can't see a failure (piped or --plain still can); TERM=dumb still draws escape codes, as the T-1330 app does [tree 06949f07bede] (2026-10-21T16:45:23Z)
- (audit self) `self: read the builder's diff; the app branch in cmd_code needs a request, both stdin and stdout on a terminal and none of --resume/--task/--json/--plain/--dry-plan; the app's own child runs fm code --json with stdin closed, so it never reopens the app; two pty tests (app, --plain) plus the unchanged piped suites pass on the merged tree` → no findings [tree 06949f07bede] (2026-10-21T16:45:23Z)
- (audit edge) `self: read the builder's diff; the app branch in cmd_code needs a request, both stdin and stdout on a terminal and none of --resume/--task/--json/--plain/--dry-plan; the app's own child runs fm code --json with stdin closed, so it never reopens the app; two pty tests (app, --plain) plus the unchanged piped suites pass on the merged tree` → in the app, q exits 0 even after a blocked run, so 'fm code x && …' typed on a terminal can't see a failure (piped or --plain still can); TERM=dumb still draws escape codes, as the T-1330 app does [tree 06949f07bede] (2026-10-21T16:49:18Z)
- (audit self) `self: read the builder's diff; the app branch in cmd_code needs a request, both stdin and stdout on a terminal and none of --resume/--task/--json/--plain/--dry-plan; the app's own child runs fm code --json with stdin closed, so it never reopens the app; two pty tests (app, --plain) plus the unchanged piped suites pass on the merged tree` → no findings [tree 06949f07bede] (2026-10-21T16:49:18Z)
- (audit edge) `self: read the builder's diff; the app branch in cmd_code needs a request, both stdin and stdout on a terminal and none of --resume/--task/--json/--plain/--dry-plan; the app's own child runs fm code --json with stdin closed, so it never reopens the app; two pty tests (app, --plain) plus the unchanged piped suites pass on the merged tree` → in the app, q exits 0 even after a blocked run, so 'fm code x && …' typed on a terminal can't see a failure (piped or --plain still can); TERM=dumb still draws escape codes, as the T-1330 app does [tree eeec304e30d8] (2026-10-21T17:03:08Z)
- (audit self) `self: read the builder's diff; the app branch in cmd_code needs a request, both stdin and stdout on a terminal and none of --resume/--task/--json/--plain/--dry-plan; the app's own child runs fm code --json with stdin closed, so it never reopens the app; two pty tests (app, --plain) plus the unchanged piped suites pass on the merged tree` → no findings [tree eeec304e30d8] (2026-10-21T17:03:08Z)
## Log
- 2026-10-21T03:47:30Z created
- 2026-10-21T13:39:24Z planned from capture
- 2026-10-21T13:40:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1343.builder.md
- 2026-10-21T13:40:34Z focused
- 2026-10-21T16:33:50Z merged worktree-agent-a55624e1695b43bc0 (4 file(s))
- 2026-10-21T16:33:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a55624e1695b43bc0
- 2026-10-21T16:37:56Z focused
- 2026-10-21T16:42:21Z scope: CHANGELOG.md — its line
- 2026-10-21T16:48:55Z paused: focus moved to T-1381
- 2026-10-21T16:49:14Z focused
- 2026-10-21T16:49:17Z scope: CHANGELOG.md — its line
- 2026-10-21T16:51:42Z paused: focus moved to T-1382
- 2026-10-21T17:03:06Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-21T17:03:06Z focused
- 2026-10-21T17:03:07Z scope: CHANGELOG.md — its line
- 2026-10-21T17:11:39Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- T-1330 [FEATURE L, done, 4 steps] fm code opens the app: a home screen over every Foreman project (queue, inbox, active, blocked, past runs) that runs any queued task or…
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
## Lessons
- A command that opens a full-screen app on a terminal needs an explicit way back to plain output (--plain), and its own children must never meet the same condition
## Plan gaps
- failed first: step 1 Failing pty test: fm code "fix add" --model fake on a terminal draws the app and closes
- failed first: step 2 cmd_code: a request on a terminal (no --json, --plain, --dry-plan) goes to fmcodetui.main; docs
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcode.py
- plugin/lib/fmcli.py
- README.md
- CHANGELOG.md
- plugin/lib/fmcodetui.py
- plugin/lib/fmcore.py
- plugin/lib/fmmodels.py
- plugin/tests/test_code_worker.py
