---
id: T-1717
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcore.py, plugin/lib/fmwatch.py, plugin/lib/fmcli.py, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/tests/test_design_surfaces.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T01:55:56Z
updated: 2026-10-23T10:59:28Z
base: be37403235e30114f31408731c48bc092b17c65f
base_tree: d7e927bb66884220c6f904d6c0534817960ebe4c
plan0_at: 2026-10-23T10:53:38Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcore.py, plugin/lib/fmwatch.py, plugin/lib/fmcli.py, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/tests/test_design_surfaces.py, CHANGELOG.md]
verified: strong
---
# Foreman-ui pane: load a custom palette (the JSON fm design tokens --to pane prints) over k
## Raw request
> foreman-ui pane: load a custom palette (the JSON fm design tokens --to pane prints) over kit.ts's C, e.g. from a plugin option or a file in FOREMAN_HOME (T-1651 follow-up)
## Interpretation
fm design tokens DESIGN.md --to pane --save keeps the pane palette JSON under Foreman's state; fm ui's view carries it checked (known keys, #rrggbb values only) as palette_custom; the foreman-ui pane, on the default palette, paints it over the default at each refresh (cb and riso, chosen explicitly, still win); --to pane --clear forgets it; an fm code worker can't save or clear it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a saved pane palette reaches fm ui checked, the pane paints it on the default palette, cb still wins, and --clear forgets it — verify with `python3 plugin/tests/run.py test_design_surfaces.PaneSaved`
## Non-goals
## Approach (options → choice → why)
Options: a plugin option holding JSON (a settings value hard to edit and validate); the pane reading a file itself (mods read no files: it runs fm); fm ui carrying the saved palette (one validated reader in fmcore, which the pane already polls). Choice: the last; saving is the opt-in, so the default palette option needs no new value.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then pane_palette, --save/--clear, the view field and the pane's overlay
## Resume here
## Docs impact
CHANGELOG line; fm design -h documents --save and --clear; the pane has no README naming its palette (options are in its manifest).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_surfaces.PaneSaved` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PaneSaved 0s) / FAILED (1 classes) [ran] [tree c59522d745c2] (2026-10-23T10:54:05Z)
- (step 1) `python3 plugin/tests/run.py test_design_surfaces test_design_tokens test_board_surfaces && claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 144 tests across 4 files. [11.93s] [ran] [tree cf40da258204] (2026-10-23T10:56:44Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces.PaneSaved` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: PaneSaved 1s) / OK [ran] [tree cf40da258204] (2026-10-23T10:56:45Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces test_design_tokens test_board_surfaces && claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 145 tests across 4 files. [11.18s] [ran] [tree 33b072bf672f] (2026-10-23T10:58:45Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces.PaneSaved` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: PaneSaved 1s) / OK [ran] [tree 33b072bf672f] (2026-10-23T10:58:47Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): re-read the whole diff by lens; two findings fixed test-first (--save with another --to was silently ignored; the pane's key check accepted inherited names like toString)` → fm design tokens DESIGN.md --to pane --save makes the pane paint that palette on its default setting, cb and riso still win, --clear forgets it; the demo view carries the new key [tree 33b072bf672f] (2026-10-23T10:58:47Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): re-read the whole diff by lens; two findings fixed test-first (--save with another --to was silently ignored; the pane's key check accepted inherited names like toString)` → --save with --to css/app now refuses instead of doing nothing; --clear names no file and works with or without one; a damaged or hostile file reads as {} or only valid keys (Python allowlist + #rrggbb, 64 KB cap) and the pane checks again with own-key lookups [tree 33b072bf672f] (2026-10-23T10:58:47Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): re-read the whole diff by lens; two findings fixed test-first (--save with another --to was silently ignored; the pane's key check accepted inherited names like toString)` → an fm code worker can't save or clear (FOREMAN_WORKER_OF refused); the write is fm's own atomic replace in Foreman's state folder (a planted link is replaced, not followed); inherited keys (toString, constructor, __proto__) never reach C [tree 33b072bf672f] (2026-10-23T10:58:47Z)
## Log
- 2026-10-23T01:55:56Z created
- 2026-10-23T10:37:21Z set tier=M, scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmwatch.py', 'plugin/lib/fmcli.py', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'plugin/tests/test_design_surfaces.py', 'CHANGELOG.md']
- 2026-10-23T10:39:56Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmwatch.py', 'plugin/lib/fmcli.py', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/types/index.d.ts', 'plugin/tests/test_design_surfaces.py', 'CHANGELOG.md']
- 2026-10-23T10:53:37Z focused
- 2026-10-23T10:56:14Z scope: plugin/lib/ui-demo.json gets palette_custom (the demo view must carry every key a real view has: test_board_surfaces)
- 2026-10-23T10:59:27Z done
- 2026-10-23T10:59:28Z committed 60063b1c (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- research T-1512-review: Verdict:** approve with nits. I found no defect in the probe, the hush write or the escaping. I could not run the tests (read-only), so every poi…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdesign.py, plugin/lib/fmwatch.py, plugin/tests/test_design_surf…; re-ground the plan against them before editing
## Lessons
- A key allowlist in TypeScript wants Object.prototype.hasOwnProperty, not in: 'toString' in {} is true
## Plan gaps
- failed first: step 1 failing tests, then pane_palette, --save/--clear, the view field and the pane's overlay
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_design_surfaces.py
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmdesign.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
