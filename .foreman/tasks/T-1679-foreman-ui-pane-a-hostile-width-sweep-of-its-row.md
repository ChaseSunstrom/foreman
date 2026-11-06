---
id: T-1679
type: FEATURE
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/tests/pane-hostile.test.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T21:35:12Z
updated: 2026-10-23T09:41:21Z
group: pane safety and width
base: 2e2af403e381cb5ff2ef597c94fce93a5fce1833
base_tree: 4280330c1d78e8585c301489bfb1561ec05b66d5
plan0_at: 2026-10-23T09:37:11Z
plan0_scope: [mods/foreman-ui/tests/pane-hostile.test.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, CHANGELOG.md]
verified: strong
---
# Foreman-ui pane: a hostile-width sweep of its rows (CJK, emoji, combining, RTL, zero-width
## Raw request
> foreman-ui pane: a hostile-width sweep of its rows (CJK, emoji, combining, RTL, zero-width, controls) like test_code_tui.HostileWidth, through the mod's own renderer (follow-up of T-1516)
## Interpretation
A hostile-width sweep of the foreman-ui pane through its own renderer, as test_code_tui.HostileWidth does for the app: each hostile string (CJK, emoji, combining, RTL with an override, zero-width, controls, variation selectors, a mix, a long one) fills every text slot of a busy view; at 20x12, 40x16, 80x24 and 121x34 nothing fixed is wider than the pane, text wider than it in columns (wide glyphs 2) truncates or wraps, and no drawn text holds a control, escape or bidi override. A failure is fixed in the mod.
## Assumptions (confidence)
## Acceptance criteria
- [x] every hostile string fits every size and draws no control, escape or bidi override — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the sweep test; fix what it finds in the mod
## Resume here
## Docs impact
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 142 tests across 4 files. [12.50s] [ran] [tree bb646f5707cf] (2026-10-23T09:40:39Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 142 tests across 4 files. [12.18s] [ran] [tree bb646f5707cf] (2026-10-23T09:40:52Z)
- (audit edge) `self review; claude plugin test mods/foreman-ui: 142 pass, the nine hostile cases among them` → line breaks survive cleaning (split, clean, join); a nested span inside a truncating Text counts as cut; 26 columns draws the full pane and 20 the one-line floor (test) [tree bb646f5707cf] (2026-10-23T09:40:52Z)
- (audit adversary) `self review; claude plugin test mods/foreman-ui: 142 pass, the nine hostile cases among them` → a view string with U+202E reversed a title's display (spoofing what a task says); cleanDeep now strips bidi overrides, isolates and controls from every view string at the one place the view enters the pane [tree bb646f5707cf] (2026-10-23T09:40:52Z)
- (audit self) `self review; claude plugin test mods/foreman-ui: 142 pass, the nine hostile cases among them` → no findings [tree bb646f5707cf] (2026-10-23T09:40:52Z)
## Log
- 2026-10-22T21:35:12Z created
- 2026-10-23T09:21:32Z set tier=S, scope=['mods/foreman-ui/tests/pane-hostile.test.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/register.tsx', 'CHANGELOG.md']
- 2026-10-23T09:37:10Z focused
- 2026-10-23T09:41:19Z done
- 2026-10-23T09:41:21Z committed 49e1fe71 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Terminal and mod UI (fm playbooks show ui/terminal-ui)
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1516 [FEATURE S, done, 3 steps] Brainstorm T-1479 round 2 (cluster 21): fm code app test net: a width-oracle sweep over ho — lesson: A width test that shares the imple…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar finished tasks took 3–5 steps
- steps similar plans added late: Done and left at a glance: a work bar (done today, now, queued, inbox, blocked) under the head; a segment per step unde… (T-1026)
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, mods/foreman-ui/hooks/kit.ts; re-ground the plan against them before editing
## Files touched
- mods/foreman-ui/tests/pane-hostile.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
