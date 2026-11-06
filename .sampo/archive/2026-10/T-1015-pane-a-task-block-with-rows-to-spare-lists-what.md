---
id: T-1015
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T01:24:31Z
updated: 2026-10-16T01:25:24Z
base: 049461f6529b891abc5ef4f0e27f0e00ca79b1d8
base_tree: 63e4952f1cb9ce672fbf8cb70e26eeb7d7368e5a
verified: strong
---
# Pane: a task block with rows to spare lists what proves it done
## Raw request
> Pane: a task block with rows to spare lists what proves it done
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] when the task block has rows beyond its steps (no History to take them), it shows 'done when' and every criterion if all fit, else none — verify with `cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a quiet project's task block lists its criteria; a busy one doesn't
2. [x] register: criteria into spare task rows
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 92 tests across 1 file. [6.91s] [ran] [tree 47647d0df9c3] (2026-10-16T01:24:48Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 92 tests across 1 file. [7.03s] [ran] [tree 64aea525f8e0] (2026-10-16T01:25:02Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 92 tests across 1 file. [6.97s] [ran] [tree 264cc73e41c9] (2026-10-16T01:25:16Z)
- (audit edge) `self` → criteria show only when every one fits with its heading and a gap, and no steps are hidden; any History takes the spare rows first, so a busy project's pane is unchanged (the one-panel test still asserts no criteria) [tree 264cc73e41c9] (2026-10-16T01:25:16Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 92 tests across 1 file. [6.84s] [ran] [tree 264cc73e41c9] (2026-10-16T01:25:23Z)
- (audit edge) `new test for a quiet project; existing tests hold the busy case` → all criteria or none; never with hidden steps [tree 264cc73e41c9] (2026-10-16T01:25:23Z)
- (audit self) `new test for a quiet project; existing tests hold the busy case` → no findings [tree 264cc73e41c9] (2026-10-16T01:25:23Z)
## Log
- 2026-10-16T01:24:31Z created
- 2026-10-16T01:24:31Z focused
- 2026-10-16T01:25:24Z done
- 2026-10-16T01:25:24Z committed e1c761b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1012 [FEATURE S, done, 3 steps] Pane: History takes only the rows it fills; spare rows go to more Activity lanes and taller Today charts first
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
- similar finished tasks took 3–6 steps
## Plan gaps
- failed first: step 1 test: a quiet project's task block lists its criteria; a busy one doesn't
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
