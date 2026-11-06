---
id: T-1589
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T19:20:58Z
updated: 2026-10-22T20:23:53Z
base: 7982d36827e3e4b106f2ec996fe8cd4fc2a49291
base_tree: 5e3385be1fb3c25132aac622d6903e93146ff132
plan0_at: 2026-10-22T20:22:45Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# Fm settings list --json and diff --json crash on a TOML datetime in tui.toml: fmcli.out's
## Raw request
> fm settings list --json and diff --json crash on a TOML datetime in tui.toml: fmcli.out's json.dumps has no default= for non-JSON values
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm --json output never crashes on non-JSON values (a TOML datetime prints as text) and shows DEL and C1 control characters escaped — verify with `cd plugin/tests && python3 -m unittest test_cli.OutJson`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] default=str and escaped controls in fmcli.out
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_cli.OutJson` → red as expected (exit 1) · Ran 1 test in 0.002s / FAILED (errors=1) [ran] [tree 9f88544a50bf] (2026-10-22T20:22:56Z)
- `cd plugin/tests && python3 -m unittest test_cli.OutJson` → ✗ exit 1 · Ran 1 test in 0.001s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree 98961b8f9f62] (2026-10-22T20:23:05Z)
- `cd plugin/tests && python3 -m unittest test_cli.OutJson` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree 98961b8f9f62] (2026-10-22T20:23:05Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_settings` → exit 0 · Ran 143 tests in 22.2s (41 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 8s, AuditPrep 7s) / OK [ran] [tree 98961b8f9f62] (2026-10-22T20:23:28Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.OutJson` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree 98961b8f9f62] (2026-10-22T20:23:28Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.OutJson` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree f06f7b0cdb4f] (2026-10-22T20:23:29Z)
- (audit adversary) `self: intent: --json never crashes on non-JSON values · adversary: DEL and C1 controls escaped as \uXXXX inside JSON strings (they occur only in strings); C0 controls were already escaped by json · edge: default=str covers datetime, date, time, Path, sets print as their str · operator: one helper change for every --json · maintainer: OutJson red first; test_cli and test_settings pass` → a value with \x9b (CSI) or \x7f prints escaped and round-trips through json.loads [tree f06f7b0cdb4f] (2026-10-22T20:23:29Z)
- (audit self) `self: intent: --json never crashes on non-JSON values · adversary: DEL and C1 controls escaped as \uXXXX inside JSON strings (they occur only in strings); C0 controls were already escaped by json · edge: default=str covers datetime, date, time, Path, sets print as their str · operator: one helper change for every --json · maintainer: OutJson red first; test_cli and test_settings pass` → no findings [tree f06f7b0cdb4f] (2026-10-22T20:23:29Z)
## Log
- 2026-10-22T19:20:58Z created
- 2026-10-22T20:22:44Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-10-22T20:22:44Z focused
- 2026-10-22T20:23:52Z done
- 2026-10-22T20:23:53Z committed 3454f1e5 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- research T-1510-review: Verdict: changes needed.** One terminal-escape hole (it is the key question you asked) and one injection path in the slash command. Nothing was r…
- T-1496 [FEATURE M, done, 3 steps] fm code app: settings schema and a comment-preserving tui.toml writer — lesson: Decide 'is Claude running this?' once (CLAUDECODE) and …
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Why not caught
--json output had only been fed JSON-native values
## Lessons
- One output helper is the place to make every --json safe: values from TOML aren't all JSON types
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
