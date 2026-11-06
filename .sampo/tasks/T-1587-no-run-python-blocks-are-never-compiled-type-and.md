---
id: T-1587
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_check.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T19:19:21Z
updated: 2026-10-23T08:43:27Z
base: 86dc5e7b74b351951729519cbd17ec403cecf28c
base_tree: 51288a058e4ffbd3da5f99f5bc3aa63d5a3fc051
plan0_at: 2026-10-23T08:43:03Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_check.py, CHANGELOG.md]
verified: strong
---
# fm check playbooks compiles the python blocks marked no-run (they never run, so a syntax slip in one went unseen)
## Raw request
> - no-run python blocks are never compiled; `type-and-colour.md:145` could get `ast.parse` or a self-test
> (noticed by an agent; research T-1505-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a playbook whose python no-run block doesn't parse fails fm check playbooks naming its line, while the repo's own 41 such blocks pass — verify with `python3 plugin/tests/run.py test_playbook_check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] a failing test with a broken no-run block, then compile() in the check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_check test_playbook_machinery` → exit 0 · Ran 56 tests in 4.0s (13 classes, 16 at a time; slowest: Load 4s, Snippets 2s, Verbs 2s) / OK [ran] [tree 430d29c2366b] (2026-10-23T08:43:20Z)
- (audit intent) `self` → pass: a broken no-run block fails naming its line; the repo's own pass [tree a9deb2a7a24f] (2026-10-23T08:43:21Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_check` → exit 0 · Ran 31 tests in 2.4s (8 classes, 16 at a time; slowest: Snippets 2s, Repo 1s, Cli 1s) / OK [ran] [tree a9deb2a7a24f] (2026-10-23T08:43:23Z)
- (audit intent) `self: intent, edge` → no-run blocks are compiled, never run [tree a9deb2a7a24f] (2026-10-23T08:43:23Z)
- (audit edge) `self: intent, edge` → compile() never executes code; a NUL byte (ValueError) is reported too [tree a9deb2a7a24f] (2026-10-23T08:43:23Z)
- (audit self) `self: intent, edge` → no findings [tree a9deb2a7a24f] (2026-10-23T08:43:23Z)
## Log
- 2026-10-22T19:19:21Z created
- 2026-10-23T08:39:53Z planned from capture
- 2026-10-23T08:39:54Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/tests/test_playbook_check.py', 'CHANGELOG.md']
- 2026-10-23T08:43:02Z focused
- 2026-10-23T08:43:25Z done
- 2026-10-23T08:43:27Z committed b427b1a7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- T-1063 [FEATURE M, done, 2 steps] Steers compile to checkers: a steer or interrupt is typed (scope, style, safety, wrong app — lesson: Never let the agent create a restr…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
- similar past tasks were M: consider --tier M
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_check.py; re-ground the plan against them before editing
## Lessons
- Code that is shown but never run still needs one cheap check: compile it
## Files touched
- plugin/lib/fmplaybooks.py
- plugin/tests/test_playbook_check.py
- CHANGELOG.md
