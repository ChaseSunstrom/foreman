---
id: T-1119
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ui.py]
depends_on: []
source: followup
created: 2026-10-16T05:55:58Z
updated: 2026-10-16T06:59:07Z
base: 48918c8f9001c8a13acf3eb9c5456b8c5d362b13
base_tree: 0291311ce466b94c4af8e830f646d804d14362fe
verified: ok
---
# Pane flag for a stopped builder: its lane node shows 'stopped · fm lane resume ID' (fm ui
## Raw request
> Pane flag for a stopped builder: its lane node shows 'stopped · fm lane resume ID' (fm ui passes fmlanes.stopped state; rows.tsx/register.tsx render it) — follow-up to T-1028
## Interpretation
T-1028 made fm next flag a builder whose Claude Code session ended (fmlanes.stopped). The pane's Agents graph shows each worktree as a ⎇ node (fmwatch._worktrees → v.worktrees → register.tsx treeNode) but not that it stopped. Add stopped: true to a worktree whose lane task fmlanes.stopped(p, briefs) lists, and render that node's status as 'stopped · fm lane resume T-…' in the warn colour. Keep ui-demo.json's keys in step with fm ui (a worktree with stopped).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ui --json marks a stopped lane's worktree stopped: true; the pane shows 'stopped · fm lane resume T-…' on that node — verify with `python3 plugin/tests/run.py test_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: python (view marks stopped) and mod (node text)
2. [x] _worktrees adds stopped; types, demo json, treeNode status
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 42.9s (7 classes, 16 at a time; slowest: UiView 43s, UiSkills 2s, SkillRoute 2s) / OK [ran] [tree b24df8023f1b] (2026-10-16T06:52:02Z)
- (step 2) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 55.3s (7 classes, 16 at a time; slowest: UiView 55s, UiSkills 4s, SkillRoute 4s) / OK [ran] [tree b24df8023f1b] (2026-10-16T06:52:59Z)
- (ac 1) `python3 plugin/tests/run.py test_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 117 tests across 1 file. [11.15s] [ran] [tree 5b4db2e13066] (2026-10-16T06:58:26Z)
- `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 11.8s (7 classes, 16 at a time; slowest: UiView 12s, UiSkills 1s, CloseOut 1s) / OK [ran] [tree 5b4db2e13066] (2026-10-16T06:58:26Z)
- (audit self) `review: one fm-reviewer pass (combined with T-1085): no defects; nit accepted (a stopped lane's node shows stopped rather than N to merge)` → no findings [tree 5b4db2e13066] (2026-10-16T06:58:26Z)
## Log
- 2026-10-16T05:55:58Z created
- 2026-10-16T06:47:17Z set scope=['plugin/lib/fmwatch.py', 'plugin/lib/ui-demo.json', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'plugin/tests/test_ui.py']
- 2026-10-16T06:47:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1119.builder.md
- 2026-10-16T06:47:28Z focused
- 2026-10-16T06:57:27Z merged worktree-agent-a78c7cd45e489d168 (6 file(s))
- 2026-10-16T06:57:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a78c7cd45e489d168
- 2026-10-16T06:57:29Z focused
- 2026-10-16T06:57:51Z scope: CHANGELOG.md — release note
- 2026-10-16T06:59:06Z done
- 2026-10-16T06:59:07Z committed f024d39 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmwatch.py changed since it was written]
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- similar past tasks were M: consider --tier M
## Preflight
Changed in scope since this was planned (2026-10-16): mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_ui.py; re-ground the plan against them before editing
## Lessons
- A state the CLI already knows (stopped builders) belongs on the pane node it concerns, not only in fm next
## Files touched
- plugin/tests/test_ui.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/fmwatch.py
- mods/foreman-ui/types/index.d.ts
- plugin/lib/ui-demo.json
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
