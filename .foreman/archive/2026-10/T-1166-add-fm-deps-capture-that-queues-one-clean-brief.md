---
id: T-1166
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmoutside.py, plugin/lib/fmcli.py, plugin/tests/test_outside.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:47:02Z
base: cc2787569efdc7ba984827a64096536072cce36f
base_tree: 02a67b54769a267ab83ad1ab56472a0c1288ee44
plan0_at: 2026-10-16T11:44:37Z
plan0_scope: [plugin/lib/fmoutside.py, plugin/lib/fmcli.py, plugin/tests/test_outside.py, CHANGELOG.md]
verified: strong
---
# Add `fm deps --capture` that queues one CLEAN brief per dependency a major version behind,
## Raw request
> FEATURE: Add `fm deps --capture` that queues one CLEAN brief per dependency a major version behind, without duplicating an existing open brief.
> DONE-WHEN: a test with two fake outdated dependencies captures two briefs and a second run captures none
## Interpretation
fm deps already lists dependencies a major version behind with the migration question; --capture turns each into one inbox brief so the upgrade isn't forgotten, never twice for the same dependency and target major.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm deps --capture queues one CLEAN brief per dependency a major version behind, naming the migration; a second run captures none — verify with `python3 plugin/tests/run.py test_outside`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_outside: --capture makes 3 briefs, rerun none
2. [x] --capture in fmoutside.cmd_deps, deduped by a CONTEXT line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_outside` → ✗ exit 1 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: Deps 2s, Landscape 1s, UiView 1s) / FAILED (1 classes) [ran] [tree 888657152110] (2026-10-16T11:44:46Z)
- (step 2) `python3 plugin/tests/run.py test_outside test_help` → exit 0 · Ran 13 tests in 3.3s (7 classes, 16 at a time; slowest: Deps 3s, Help 1s, Landscape 1s) / OK [ran] [tree fbebac6da186] (2026-10-16T11:45:00Z)
- (ac 1) `python3 plugin/tests/run.py test_outside` → exit 0 · Ran 8 tests in 3.7s (5 classes, 16 at a time; slowest: Deps 3s, Landscape 2s, UiView 2s) / OK [ran] [tree 9bb09c93d10a] (2026-10-16T11:45:11Z)
- (step 1) `python3 plugin/tests/run.py test_outside` → exit 0 · Ran 8 tests in 3.7s (5 classes, 16 at a time; slowest: Deps 3s, Landscape 2s, UiView 2s) / OK [ran] [tree 9bb09c93d10a] (2026-10-16T11:45:11Z)
- (audit edge) `self: reuses fmeco.capture_once with a Foreman-owned CONTEXT key per ecosystem, name and target major (a new major makes a new task); names were already shape-checked as untrusted (T-0281)` → a rerun captures none; a later major captures again [tree 9bb09c93d10a] (2026-10-16T11:45:11Z)
- (audit self) `self: reuses fmeco.capture_once with a Foreman-owned CONTEXT key per ecosystem, name and target major (a new major makes a new task); names were already shape-checked as untrusted (T-0281)` → no findings [tree 9bb09c93d10a] (2026-10-16T11:45:11Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:44:35Z set type=FEATURE, tier=S, scope=['plugin/lib/fmoutside.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_outside.py', 'CHANGELOG.md']
- 2026-10-16T11:44:36Z focused
- 2026-10-16T11:47:00Z done
- 2026-10-16T11:47:02Z committed bfda3805 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0278 [FEATURE M, done, 3 steps] Outside view: fm landscape (diff the harness landscape against the last scan) and fm deps (new majors of dependencies, … — lesson: A de…
- research T-0278-review-1: Approve with nits. Both features do what was asked. I found no HIGH issues, and the pre-audit hit is dismissed: it is `no_verify=False` at `plu…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-10-16: Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for eve…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_outside.py
## Plan gaps
- failed first: step 1 Failing test in test_outside: --capture makes 3 briefs, rerun none
## Files touched
- plugin/tests/test_outside.py
- plugin/lib/fmoutside.py
- plugin/lib/fmcli.py
- CHANGELOG.md
