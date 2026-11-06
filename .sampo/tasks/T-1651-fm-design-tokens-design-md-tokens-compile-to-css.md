---
id: T-1651
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_design_surfaces.py, CHANGELOG.md]
depends_on: [T-1507]
source: user
created: 2026-10-22T20:58:31Z
updated: 2026-10-23T02:20:36Z
base: 5f30c5f91834a2c57ca7760c8b13ddb90fc35489
base_tree: 5622f090d89b075ee92aaa1b18bde0c0a73d2288
plan0_at: 2026-10-23T01:48:39Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_design_surfaces.py, CHANGELOG.md]
verified: strong
---
# fm design tokens: DESIGN.md tokens compile to CSS variables, an fm code app theme and the Claude Code pane palette
## Raw request
> fm design tokens: DESIGN.md tokens compile to CSS variables, an fm code app theme and the Claude Code pane palette
## Interpretation
fm design tokens [--to css|app|pane] compiles DESIGN.md's ## Tokens table (written by T-1507's extract) to CSS custom properties, an fm code app theme table that fm settings accepts, and the Claude Code pane's palette, so one file drives every surface.
## Assumptions (confidence)
## Acceptance criteria
- [x] one fixture DESIGN.md gives CSS variables and a theme table fm settings accepts — verify with `python3 plugin/tests/run.py test_design_surfaces.Tokens`
## Non-goals
## Approach (options → choice → why)
Options: a token build tool like Style Dictionary (a Node dependency); per-surface hand edits (drift); our own emitters. Choice: our emitters over T-1507's parser: three small outputs, validated by fm settings.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] token reader (reuse T-1507's extract)
3. [x] three emitters, the theme written through fm settings
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces.Tokens 2>&1 | tail -8` → ✗ exit 1 · Ran 8 tests in 11.1s (1 classes, 16 at a time; slowest: Tokens 6s) / FAILED (1 classes) [ran] [tree 1ef0c4faddcc] (2026-10-23T01:52:42Z)
- (step 1) `python3 plugin/tests/run.py test_design_surfaces.Tokens` → ✗ exit 1 · Ran 8 tests in 3.1s (1 classes, 16 at a time; slowest: Tokens 3s) / FAILED (1 classes) [ran] [tree ec4958042e91] (2026-10-23T01:52:53Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces.Tokens 2>&1 | grep -v "^ File\|^Traceback" | tail -40` → exit 0 · Ran 8 tests in 7.7s (1 classes, 16 at a time; slowest: Tokens 7s) / OK [ran] [tree cb710cfef40a] (2026-10-23T01:54:03Z)
- (step 2) `python3 plugin/tests/run.py test_design_surfaces.Tokens test_design_tokens` → exit 0 · Ran 42 tests in 12.6s (4 classes, 16 at a time; slowest: Extract 12s, Palette 5s, Tokens 5s) / OK [ran] [tree da1c1d3a7679] (2026-10-23T01:55:00Z)
- (step 3) `python3 plugin/tests/run.py test_design_surfaces.Tokens` → exit 0 · Ran 8 tests in 3.7s (1 classes, 16 at a time; slowest: Tokens 3s) / OK [ran] [tree da1c1d3a7679] (2026-10-23T01:55:05Z)
- (step 1) `python3 plugin/tests/run.py test_design_surfaces.Tokens` → ✗ exit 1 · Ran 14 tests in 3.8s (1 classes, 16 at a time; slowest: Tokens 3s) / FAILED (1 classes) [ran] [tree 9f28a24ee1ea] (2026-10-23T02:09:50Z)
- (step 3) `python3 plugin/tests/run.py test_design_surfaces.Tokens test_design_tokens` → exit 0 · Ran 48 tests in 9.0s (4 classes, 16 at a time; slowest: Extract 9s, Tokens 4s, Palette 3s) / OK [ran] [tree bb4db7df4325] (2026-10-23T02:12:05Z)
- (step 3) `python3 plugin/tests/run.py test_design_surfaces test_design_tokens test_design_gates test_design_lint test_cli` → exit 0 · Ran 193 tests in 25.6s (41 classes, 16 at a time; slowest: TaskLifecycle 25s, StateViews 11s, AuditPrep 10s) / OK [ran] [tree 9bebcddef0cc] (2026-10-23T02:18:33Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces test_design_tokens test_design_gates` → exit 0 · Ran 54 tests in 3.5s (5 classes, 16 at a time; slowest: Extract 3s, Tokens 2s, Palette 1s) / OK [ran] [tree 46a9a0b16098] (2026-10-23T02:19:49Z)
- (step 1) `python3 plugin/tests/run.py test_design_surfaces.Tokens` → exit 0 · Ran 14 tests in 1.9s (1 classes, 16 at a time; slowest: Tokens 2s) / OK [ran] [tree 46a9a0b16098] (2026-10-23T02:19:58Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces.Tokens` → exit 0 · Ran 14 tests in 1.9s (1 classes, 16 at a time; slowest: Tokens 2s) / OK [ran] [tree 46a9a0b16098] (2026-10-23T02:20:01Z)
- (audit intent) `fm-reviewer pass (shared with T-1637); fixed test-first: CSS values written only when brackets/quotes balance and free of ; { } < \ @ url( comments (11 bad forms tested); preset picked from the mapped screen's lightness and every preset style faint-checked; primary before accent, *-foreground preferred for text/muted (shadcn table tested); columns by header name; dark under .dark/[data-theme] too` → fm design tokens compiles DESIGN.md's Tokens to CSS variables, an fm code [colors] theme fm settings accepts, and the pane palette JSON [tree 46a9a0b16098] (2026-10-23T02:20:01Z)
- (audit adversary) `fm-reviewer pass (shared with T-1637); fixed test-first: CSS values written only when brackets/quotes balance and free of ; { } < \ @ url( comments (11 bad forms tested); preset picked from the mapped screen's lightness and every preset style faint-checked; primary before accent, *-foreground preferred for text/muted (shadcn table tested); columns by header name; dark under .dark/[data-theme] too` → table cells can't break out of CSS (fall back to hex or a named left-out comment); TOML/JSON carry only #hex and checked names [tree 46a9a0b16098] (2026-10-23T02:20:01Z)
- (audit edge) `fm-reviewer pass (shared with T-1637); fixed test-first: CSS values written only when brackets/quotes balance and free of ; { } < \ @ url( comments (11 bad forms tested); preset picked from the mapped screen's lightness and every preset style faint-checked; primary before accent, *-foreground preferred for text/muted (shadcn table tested); columns by header name; dark under .dark/[data-theme] too` → a light token file gets the paper preset; styles too faint on the new screen are left out and named; a reordered table maps by header [tree 46a9a0b16098] (2026-10-23T02:20:01Z)
- (audit operator) `fm-reviewer pass (shared with T-1637); fixed test-first: CSS values written only when brackets/quotes balance and free of ; { } < \ @ url( comments (11 bad forms tested); preset picked from the mapped screen's lightness and every preset style faint-checked; primary before accent, *-foreground preferred for text/muted (shadcn table tested); columns by header name; dark under .dark/[data-theme] too` → prints only (writing tui.toml is the user's step); the pane loading the palette is captured as T-1717 [tree 46a9a0b16098] (2026-10-23T02:20:01Z)
## Log
- 2026-10-22T20:58:31Z created
- 2026-10-22T20:58:31Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_surfaces.py', 'CHANGELOG.md']
- 2026-10-22T20:58:32Z split from T-1540 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:58:33Z set depends_on=['T-1507']
- 2026-10-22T21:29:59Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_design_surfaces.Tokens`
- 2026-10-22T21:30:22Z criterion 1 text: one fixture DESIGN.md gives CSS variables and a theme table fm settings accepts — verify with python3 plugin/tests/run.py test_design_surfaces.Tokens → one fixture DESIGN.md gives CSS variables and a theme table fm settings accepts
- 2026-10-23T01:47:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1651.builder.md
- 2026-10-23T01:48:37Z focused
- 2026-10-23T02:18:56Z merged worktree-agent-aa815e4d263451487 (6 file(s))
- 2026-10-23T02:18:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa815e4d263451487
- 2026-10-23T02:19:45Z focused
- 2026-10-23T02:19:50Z scope: tests fixture, fmsettings check, MASTER.md and the fmcli design parser; files from build merges (T-1645/T-1703/T-1700) committed by their tasks
- 2026-10-23T02:20:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1507 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 12): design tokens: a design-extract skill that derives — lesson: A parser that re-scans the parent …
- T-1540 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): One token file for every surface: DESIGN.md tokens drive the web, the fm
- research T-1507-review: Verdict: changes needed.** The maths is sound. The problems are in extract's file handling, its speed on hostile input, and how a Tokens-only DES…
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/lib/fmsettings.py, plugin/tests/test_design_surfaces.py; re-ground the plan against them before editing
## Lessons
- Role guessing from token names needs a readability backstop: faint-check every style the theme ends up with, not only the ones written
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/fixtures/design-surfaces/DESIGN.md
- plugin/tests/test_design_surfaces.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
- plugin/README.md
- plugin/lib/fmcore.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmmotion.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- plugin/skills/debug-test/SKILL.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/release/SKILL.md
- plugin/skills/research/SKILL.md
- plugin/tests/fixtures/skill_triggers.json
- plugin/tests/test_core.py
- plugin/tests/test_cost.py
- plugin/tests/test_docs.py
- plugin/tests/test_doctor.py
- plugin/tests/test_hooks.py
- plugin/tests/test_lanes.py
- plugin/tests/test_motion_verify.py
- plugin/tests/test_playbook_machinery.py
- plugin/lib/fmcost.py
- plugin/skills/ui-design/SKILL.md
