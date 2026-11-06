---
id: T-0019
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_hooks.py]
depends_on: []
source: discovered
created: 2026-09-26T13:15:05Z
updated: 2026-09-26T15:52:04Z
---
# Drive lets the turn end while background agents or commands are running
## Raw request
> Drive should know about running background subagents/commands: while work waits on them, the Stop note should say so (and allow the turn to end) instead of pushing to continue
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A Stop while a background agent (SubagentStart, no SubagentStop yet) or a background Bash command (run_in_background, no task-notification yet) is running in this session isn't blocked by drive; once they finish, drive pushes again — verify with python3 -m unittest test_hooks
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] TDD: record background Bash start/finish events, derive running work per session from the event tail, _drive yields while any runs
## Resume here
## Verification evidence
- (step 1) `python3 -m unittest test_hooks (2 new drive tests); live background probe; bench_hooks` → RED then OK; live: bg_start b1hts2vc4 → notification → bg_done, _running = []; Stop p95 41.2 ms; full suite OK (3f12096) (2026-09-26T15:52:04Z)
- (ac 1) `python3 -m unittest test_hooks; live probe` → OK: Stop not blocked while SubagentStart without Stop, or run_in_background without its task-notification; blocks again once they finish (2026-09-26T15:52:04Z)
- (audit self) `S checklist: parent session ids verified in real events, id format matches notifications, stale bound 6 h, foreground subagents balanced, latency within budget` → no findings [tree 87828f7a49b9] (2026-09-26T15:52:04Z)
## Log
- 2026-09-26T13:15:05Z created
- 2026-09-26T14:38:10Z planned from capture
- 2026-09-26T14:59:53Z observed 2026-09-26 ~10:05: while two background audit agents ran, drive blocked three consecutive Stops, including one after a text-only turn (stop_hook_active, no tool calls); check what counted as progress (_progressed: ledger size or session tool events) when fixing
- 2026-09-26T15:28:32Z user approved core in Claude Code's permission prompt
- 2026-09-26T15:47:56Z focused
- 2026-09-26T15:52:04Z done
## Follow-ups captured
