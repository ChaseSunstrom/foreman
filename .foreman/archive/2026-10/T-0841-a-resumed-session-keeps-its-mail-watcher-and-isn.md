---
id: T-0841
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T13:26:04Z
updated: 2026-10-15T13:33:31Z
base: e679fac75ff5d499fe6f93bae47b91b15d8a6dbc
base_tree: a9ba7529414b2fc100dafb4d6c406fbc84fd32f1
verified: strong
---
# A resumed session keeps its mail watcher and isn't 'another session': fm bus watch follows its claude process's latest session id, and the session claim recognises its own process
## Raw request
> A resumed session keeps its mail watcher and isn't 'another session': fm bus watch follows its claude process's latest session id, and the session claim recognises its own process
## Interpretation
Live, 2026-10-15: the user restarted Claude Code and resumed this conversation. The process started as session 84ca4893, then resumed into af0c3568. The plugin monitor's fm bus watch kept 84ca4893 (from FOREMAN_SESSION_ID at its start), so af0c3568's mail is never printed, and SessionStart reported 84ca4893 as another session active 0m ago. SessionStart's record_pid already maps the claude pid to af0c3568.
## Assumptions (confidence)
## Acceptance criteria
- [x] a watcher started under one session id prints mail for the id its claude process resumed into; SessionStart for a resume in the same claude process adds no 'another session' note — verify with `python3 plugin/tests/run.py test_bus`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for both
2. [x] watch re-reads its anchor's by-pid record; the session claim stores the claude pid
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 13 tests in 5.0s (5 classes, 16 at a time; slowest: Watch 5s, Approvals 4s, Bus 1s) / OK [ran] [tree c68b5848b3e3] (2026-10-15T13:29:52Z)
- (step 2) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 13 tests in 5.0s (5 classes, 16 at a time; slowest: Watch 5s, Approvals 4s, Bus 1s) / OK [ran] [tree c68b5848b3e3] (2026-10-15T13:29:58Z)
- `python3 plugin/tests/run.py test_bus` → ✗ exit 1 · Ran 13 tests in 10.3s (5 classes, 16 at a time; slowest: Watch 10s, Approvals 4s, Bus 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c68b5848b3e3] (2026-10-15T13:30:13Z)
- `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 13 tests in 5.0s (5 classes, 16 at a time; slowest: Watch 5s, Approvals 4s, Bus 1s) / OK [ran] [tree c68b5848b3e3] (2026-10-15T13:30:13Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                52.5    74.5     150  [0] / SessionEnd                  48.6    58.3     150  [0] (slower: 20.5 s vs a usual 12.4 s); claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 66 tests across 1 file. [3.17s]; python [ran] [tree c68b5848b3e3] (2026-10-15T13:33:01Z)
- (ac 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 13 tests in 5.3s (5 classes, 16 at a time; slowest: Watch 5s, Approvals 4s, Bus 1s) / OK [ran] [tree c68b5848b3e3] (2026-10-15T13:33:31Z)
- (audit edge) `self: found live after the user restarted Claude Code and resumed this conversation (watcher on 84ca4893, conversation af0c3568, by-pid already mapping claude 8019 → af0c3568); the watcher now follows its claude process's latest SessionStart record, and the session claim stores the claude pid so a resume in the same process isn't 'another session' (SessionStart and fm focus)` → outside Claude Code (tests in CI, fm run children whose ancestor isn't named claude) claude_pid is None and the old behaviour holds; an explicit fm bus watch SID never follows; on an id switch the old heartbeat is removed and the mail re-read, so mail sent between the resume and the next poll still prints [tree c68b5848b3e3] (2026-10-15T13:33:31Z)
- (audit self) `self: found live after the user restarted Claude Code and resumed this conversation (watcher on 84ca4893, conversation af0c3568, by-pid already mapping claude 8019 → af0c3568); the watcher now follows its claude process's latest SessionStart record, and the session claim stores the claude pid so a resume in the same process isn't 'another session' (SessionStart and fm focus)` → no findings [tree c68b5848b3e3] (2026-10-15T13:33:31Z)
## Log
- 2026-10-15T13:26:04Z created
- 2026-10-15T13:26:04Z focused
- 2026-10-15T13:33:31Z done
- 2026-10-15T13:33:31Z committed deff87a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0777 [FEATURE M, done, 3 steps] Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux — les…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0708 [FEATURE M, done, 5 steps] Frontier 08 — Orchestrator control plane — lesson: Cross-session control fits in the hooks that already run: deliver on the next tool c…
- decision 2026-09-26: T-0014 fm run: minimal one-shot worker (fresh claude -p per task, drive scoped to that task via FOREMAN_DRIVE_TASK, per-task timeout, stop on no pro…
## Lessons
- A session id isn't a process: Claude Code can resume a different conversation in the same process, so anything keyed on the id at start must follow the process's latest SessionStart
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
- plugin/lib/fmcli.py
