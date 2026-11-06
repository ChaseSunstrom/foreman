---
id: T-1097
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmwatch.py, plugin/lib/fmbus.py, plugin/tests/test_session_files.py]
depends_on: []
source: user
created: 2026-10-16T04:37:44Z
updated: 2026-10-16T04:49:19Z
base: 158bf06cd3c615174447cd55a0e24f3e81f386bd
base_tree: 1d417b4edc4a5397af8d9ecc0c7e06dfa7700df5
verified: strong
---
# fm ui crashes when the newest sessions/*.json is a subagent's outline list, blanking the band and the pane
## Raw request
> fm ui crashes when the newest sessions/*.json is a subagent's outline list, blanking the band and the pane
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ui skips session files that aren't a session snapshot — verify with `python3 plugin/tests/run.py test_watch`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a list-shaped sessions/<sid>.outlined-<agent>.json newest; fm ui --json still works
2. [x] Skip non-object snapshots and the outline side files in _latest_session
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_session_files` → ✗ exit 1 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: SideFiles 0s) / FAILED (1 classes) [ran] [tree eb7c07456e7c] (2026-10-16T04:38:13Z)
- (step 2) `python3 plugin/tests/run.py test_session_files test_cockpit test_board_surfaces` → ✗ exit 1 · Ran 11 tests in 1.6s (3 classes, 16 at a time; slowest: BoardSurfaces 1s, Cockpit 1s, SideFiles 0s) / FAILED (1 classes) [ran] [tree 0e83c2eed8ab] (2026-10-16T04:38:22Z)
- (step 2) `python3 plugin/tests/run.py test_session_files test_cockpit test_board_surfaces` → exit 0 · Ran 11 tests in 1.6s (3 classes, 16 at a time; slowest: BoardSurfaces 2s, Cockpit 1s, SideFiles 0s) / OK [ran] [tree c24b3d026471] (2026-10-16T04:38:49Z)
- (ac 1) `python3 plugin/tests/run.py test_watch` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Harness 0s) / OK [ran] [tree cae81d05adad] (2026-10-16T04:49:08Z)
- (step 1) `python3 plugin/tests/run.py test_session_files test_board_surfaces test_docs` → exit 0 · Ran 40 tests in 2.2s (12 classes, 16 at a time; slowest: BoardSurfaces 2s, TaskLifecycle 1s, SideFiles 1s) / OK [ran] [tree cae81d05adad] (2026-10-16T04:49:08Z)
- (audit edge) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → an empty, list-shaped or unreadable snapshot is skipped, never fatal [tree cae81d05adad] (2026-10-16T04:49:08Z)
- (audit operator) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → the band and pane no longer go blank when a subagent's outline file is the newest in the sessions folder [tree cae81d05adad] (2026-10-16T04:49:08Z)
- (audit self) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → no findings [tree cae81d05adad] (2026-10-16T04:49:08Z)
- `python3 plugin/tests/run.py test_session_files test_board_surfaces test_docs` → exit 0 · Ran 40 tests in 2.8s (12 classes, 16 at a time; slowest: BoardSurfaces 3s, TaskLifecycle 2s, TaskDocsDrift 1s) / OK [ran] [tree cae81d05adad] (2026-10-16T04:49:18Z)
- (audit edge) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → an empty, list-shaped or unreadable snapshot is skipped, never fatal [tree cae81d05adad] (2026-10-16T04:49:18Z)
- (audit operator) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → the band and pane no longer go blank when a subagent's outline file is the newest in the sessions folder [tree cae81d05adad] (2026-10-16T04:49:18Z)
- (audit adversary) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → the guard eval prompts only re-embed the current rules text verbatim (sync_evals.py); no guard logic changed; a crafted sessions file can now only be skipped, not crash fm ui [tree cae81d05adad] (2026-10-16T04:49:18Z)
- (audit self) `self: root cause is side files sharing the sessions folder (fmhooks writes sid.outlined-<agent>.json, a list); both readers of session snapshots (fmwatch._latest_session, fmbus._snapshot) now skip anything not an object; red then green; also repaired T-1057's leftovers the full gate caught (ui-demo loop key, rules footprint, eval prompts re-synced)` → no findings [tree cae81d05adad] (2026-10-16T04:49:18Z)
## Log
- 2026-10-16T04:37:44Z created
- 2026-10-16T04:37:44Z focused
- 2026-10-16T04:38:20Z set scope=['plugin/lib/fmwatch.py', 'plugin/lib/fmbus.py', 'plugin/tests/test_session_files.py']
- 2026-10-16T04:38:47Z scope: plugin/lib/ui-demo.json — T-1057 added the loop key to fm ui without the demo view; test_board_surfaces caught it here
- 2026-10-16T04:46:49Z scope: plugin/rules/foreman.md — T-1057's rules line pushed the rules over the 6000-char footprint; trimmed
- 2026-10-16T04:48:49Z scope: plugin/evals/*/prompt.md — re-synced (sync_evals.py) after the rules trim; they embed the rules
- 2026-10-16T04:49:19Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-0777 [FEATURE M, done, 3 steps] Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux — les…
- T-1023 [FEATURE M, done, 4 steps] Can you have a graph of sub agents/worktrees/brainstorms? — lesson: A list kept for a time window must be filtered at every draw, not o…
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
## Plan gaps
- failed first: step 1 Failing test: a list-shaped sessions/<sid>.outlined-<agent>.json newest; fm ui --json still works
- failed first: step 2 Skip non-object snapshots and the outline side files in _latest_session
## Files touched
- plugin/tests/test_session_files.py
- plugin/lib/fmbus.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
