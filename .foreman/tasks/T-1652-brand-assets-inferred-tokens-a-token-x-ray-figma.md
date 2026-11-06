---
id: T-1652
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_surfaces.py, plugins/foreman-design/**, plugin/lib/fmcritique.py, plugin/tests/test_critique.py, .claude-plugin/marketplace.json, MASTER.md, CHANGELOG.md, plugin/skills/ui-design/SKILL.md, plugin/lib/fmrelease.py, plugin/tests/test_release.py]
depends_on: []
source: followup
created: 2026-10-22T20:58:34Z
updated: 2026-10-28T21:04:49Z
base: 1c85af030410e5dae3a09459e4da5781ace74aa8
base_tree: 68b2e78f43c6f5d77d21392a4c0d232df54eb4a1
plan0_at: 2026-10-28T20:35:13Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_surfaces.py, plugins/foreman-design/**, .claude-plugin/marketplace.json, plugin/skills/ui-design/SKILL.md, MASTER.md, CHANGELOG.md]
verified: strong
---
# Brand assets, Figma-as-data import, inferred tokens, a token x-ray, a foreman-design plugin entry
## Raw request
> Brand assets, inferred tokens, a token x-ray, Figma-as-data import, a foreman-design plugin entry (from T-1540; waits: after fm design tokens; an MCP import path needs a guard review)
## Interpretation
Five extras on DESIGN.md tokens (T-1540 round 3): brand assets drawn in the token roles; a Figma variables or DTCG JSON export read as data into a ## Tokens table (a file the user exported, no MCP, so no guard review); token rows inferred from the literals hand edits left; an x-ray shot marking which elements wear token colours; and the design skills offered as an optional foreman-design plugin.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design tokens DESIGN.md --to brand --out DIR writes favicon.svg and card.svg in the accent/bg/text roles — verify with `python3 plugin/tests/run.py test_design_surfaces`
- [x] a DTCG or Figma variables .json reads as tokens: --to md prints a ## Tokens table read_design reads back; a bad file exits 2 — verify with `python3 plugin/tests/run.py test_design_surfaces`
- [x] fm design infer PATHS proposes token rows for literals used 2+ times that no token holds — verify with `python3 plugin/tests/run.py test_design_surfaces`
- [x] fm design xray PAGE --tokens DESIGN.md --out x.png outlines on-token and off-token elements and prints coverage — verify with `python3 plugin/tests/run.py test_design_surfaces`
- [x] the foreman-design marketplace entry validates: plugin.json, and each skill link resolves to a SKILL.md — verify with `python3 plugin/tests/run.py test_design_surfaces`
## Non-goals
## Approach (options → choice → why)
Options: a new fm brand command; an fm design brand action; --to brand on fm design tokens. Chosen: extend fm design tokens (--to brand writes favicon.svg + card.svg; a .json source is read as DTCG/Figma; --to md prints the table), fm design infer reuses _literals (what the debt budget counts), fm design xray reuses fmshot.Browser + fmcritique._open, and plugins/foreman-design symlinks the three design skills (CC copies symlinks' targets). Why: every piece reuses a reader or browser path that exists; one new action each, no new module.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first (red)
2. [x] tokens: --to brand, .json import, --to md
3. [x] infer and xray
4. [x] foreman-design plugin entry + docs (skill, MASTER, CHANGELOG)
## Resume here
<!-- auto -->
- 2026-10-28T21:00:02Z step 1/4: tests first (red)
- git: foreman/build; 12 uncommitted: .claude-plugin/marketplace.json, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcritique.py, plugin/lib/fmdesign.py, plugin/lib/fmrelease.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_critique.py, plugin/tests/test_design_surfaces.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1652-i.txt, plugin/tests/test_design_surfaces.py, plugin/tests/test_release.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1652-j.txt, .claude-plugin/marketplace.json, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/lib/fmrelease.py, plugins/foreman-design/.claude-plugin/plugin.json
- failures met: plugin.json
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/ui-design/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_surfaces` → ✗ exit 1 · Ran 23 tests in 2.1s (7 classes, 16 at a time; slowest: Tokens 2s, PaneSaved 1s, Imported 1s) / FAILED (5 classes) [ran] [tree c37d90ca5fc7] (2026-10-28T20:41:21Z)
- (step 2) `python3 plugin/tests/run.py test_design_surfaces` → ✗ exit 1 · Ran 23 tests in 2.1s (7 classes, 16 at a time; slowest: Tokens 2s, Xray 2s, PaneSaved 1s) / FAILED (1 classes) [ran] [tree 89eb08346a6e] (2026-10-28T20:49:38Z)
- `python3 plugin/tests/run.py test_design_surfaces` → ✗ exit 1 · Ran 23 tests in 2.9s (7 classes, 16 at a time; slowest: Tokens 2s, PaneSaved 1s, Imported 1s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree 4b8f8a014d94] (2026-10-28T20:51:19Z)
- `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 23 tests in 2.1s (7 classes, 16 at a time; slowest: Tokens 2s, Xray 2s, PaneSaved 1s) / OK [ran] [tree 4b8f8a014d94] (2026-10-28T20:51:19Z)
- (step 2) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 23 tests in 2.1s (7 classes, 16 at a time; slowest: Tokens 2s, Xray 2s, PaneSaved 1s) / OK [ran] [tree 4b8f8a014d94] (2026-10-28T20:51:22Z)
- (step 3) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 23 tests in 2.1s (7 classes, 16 at a time; slowest: Tokens 2s, Xray 2s, PaneSaved 1s) / OK [ran] [tree 4b8f8a014d94] (2026-10-28T20:51:24Z)
- (step 4) `~/.local/bin/claude plugin validate . && python3 plugin/tests/run.py test_design_surfaces test_docs test_skills` → exit 0 · Ran 98 tests in 9.3s (26 classes, 16 at a time; slowest: Fences 9s, Tokens 2s, Xray 2s) / OK [ran] [tree 4b8f8a014d94] (2026-10-28T20:51:34Z)
- `python3 plugin/tests/run.py test_design_surfaces test_release test_critique` → ✗ exit 1 · Ran 87 tests in 14.5s (22 classes, 16 at a time; slowest: Release 14s, InABrowser 7s, BoardVerbs 4s) / FAILED (8 classes) (start tree + this task's tests) [ran] [tree 2fda4eafc652] (2026-10-28T20:58:51Z)
- `python3 plugin/tests/run.py test_design_surfaces test_release test_critique` → exit 0 · Ran 87 tests in 14.2s (22 classes, 16 at a time; slowest: Release 14s, InABrowser 7s, BoardVerbs 4s) / OK [ran] [tree 2fda4eafc652] (2026-10-28T20:58:51Z)
- (audit intent) `fm-reviewer vs the 5 criteria` → nothing missing; all five met in code and tests [tree 2fda4eafc652] (2026-10-28T20:59:13Z)
- (audit adversary) `fm-reviewer + red test` → worker --out writes (tokens md/brand, palette) refused; xray --out must be .png; both tested [tree 2fda4eafc652] (2026-10-28T20:59:13Z)
- (audit edge) `fm-reviewer + red tests` → DTCG shared groups in both themes, skips counted to stderr; empty page exits 2; md onto own source refused [tree 2fda4eafc652] (2026-10-28T20:59:13Z)
- (audit operator) `fm-reviewer + test_release` → foreman-design version follows foreman in fm release; description says not to enable both; help mentions brand [tree 2fda4eafc652] (2026-10-28T20:59:14Z)
- (audit maintainer) `fm-reviewer` → non-browser paths now tested (brand no roles, infer --json, worker, xray args) [tree 2fda4eafc652] (2026-10-28T20:59:14Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 28 tests in 2.6s (8 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (ac 2) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 28 tests in 2.6s (8 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (ac 3) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 28 tests in 2.6s (8 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (ac 4) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 28 tests in 2.6s (8 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (ac 5) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 28 tests in 2.6s (8 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → all 5 criteria met (brand assets, Figma/DTCG import, infer, xray, foreman-design plugin); nothing missing [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → --out from an fm code worker refused (palette and tokens); xray --out must be .png; md --out onto its source refused [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → Tokens Studio shared groups, aliases to nothing, name collisions and >MAX_ROWS counted and named on stderr; empty page exits 2 [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → foreman-design version rides fm release's bump; marketplace says don't enable both [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → _url shared by critique and xray; DESIGN_PJ one constant [tree 2fda4eafc652] (2026-10-28T21:03:47Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → all 5 criteria met (brand assets, Figma/DTCG import, infer, xray, foreman-design plugin); nothing missing [tree 2fda4eafc652] (2026-10-28T21:04:20Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → --out from an fm code worker refused (palette and tokens); xray --out must be .png; md --out onto its source refused [tree 2fda4eafc652] (2026-10-28T21:04:20Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → Tokens Studio shared groups, aliases to nothing, name collisions and >MAX_ROWS counted and named on stderr; empty page exits 2 [tree 2fda4eafc652] (2026-10-28T21:04:20Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → foreman-design version rides fm release's bump; marketplace says don't enable both [tree 2fda4eafc652] (2026-10-28T21:04:20Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 9 findings verified red-first and fixed; full gates 4021 tests green` → _url shared by critique and xray; DESIGN_PJ one constant [tree 2fda4eafc652] (2026-10-28T21:04:20Z)
## Log
- 2026-10-22T20:58:34Z created
- 2026-10-28T20:32:01Z planned from capture
- 2026-10-28T20:35:12Z focused
- 2026-10-28T20:52:45Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_surfaces.py', 'plugins/foreman-design/**', 'plugin/lib/fmcritique.py', 'plugin/tests/test_critique.py', '.claude-plugin/marketplace.json', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/ui-design/SKILL.md']
- 2026-10-28T20:52:45Z scope widened: xray shares fm critique's page-path bug (site/index.html opened as site/site/index.html); fixed once in fmcritique._url
- 2026-10-28T20:56:31Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_surfaces.py', 'plugins/foreman-design/**', 'plugin/lib/fmcritique.py', 'plugin/tests/test_critique.py', '.claude-plugin/marketplace.json', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/ui-design/SKILL.md', 'plugin/lib/fmrelease.py', 'plugin/tests/test_release.py']
- 2026-10-28T20:56:31Z steer: review fixes — worker --out guard, DTCG shared groups + skip note, xray --out .png + nothing painted, md onto own source, foreman-design version follows foreman in fm release
- 2026-10-28T21:04:47Z done
- 2026-10-28T21:04:49Z committed b3142bbc (15 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1540 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): One token file for every surface: DESIGN.md tokens drive the web, the fm
- T-1507 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 12): design tokens: a design-extract skill that derives — lesson: A parser that re-scans the parent …
- research T-1507-review: Verdict: changes needed.** The maths is sound. The problems are in extract's file handling, its speed on hostile input, and how a Tokens-only DES…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): .claude-plugin/marketplace.json, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_design_surfaces.py; re-ground the plan against them before editing
## Lessons
- a tokens importer must count what it drops and say so, never silently fewer; a second plugin linking the first's skills has to ride its release bump
## Plan gaps
- failed first: step 1 tests first (red)
- failed first: step 2 tokens: --to brand, .json import, --to md
## Files touched
- plugin/tests/test_design_surfaces.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- plugins/foreman-design/.claude-plugin/plugin.json
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- plugin/skills/ui-design/SKILL.md
- plugin/tests/test_critique.py
- plugin/lib/fmcritique.py
- plugin/tests/test_release.py
- plugin/lib/fmrelease.py
- plugins/foreman-design/skills/design-extract
- plugins/foreman-design/skills/directions
- plugins/foreman-design/skills/ui-design
