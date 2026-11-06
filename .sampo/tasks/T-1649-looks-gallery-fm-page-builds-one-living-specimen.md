---
id: T-1649
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_looks_gallery.py, CHANGELOG.md, plugin/lib/looks.html, MASTER.md, plugin/lib/fmtaste.py]
depends_on: []
source: user
created: 2026-10-22T20:58:26Z
updated: 2026-10-22T23:04:27Z
base: 30c1721a61e3da45f0220e20ea6d081bb94826ba
base_tree: 1d37d1598b736422819aa2f6b28053d5c082c0e0
plan0_at: 2026-10-22T22:12:50Z
plan0_scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_looks_gallery.py, CHANGELOG.md]
verified: strong
---
# Looks gallery: fm page builds one living specimen per look card, single file, no network
## Raw request
> Looks gallery: fm page builds one living specimen per look card, single file, no network
## Interpretation
fm page looks builds a single-file gallery with one living specimen per look card (its palette, type pair, a component sample and its motion, playing once and honouring reduced motion), with no outside host.
## Assumptions (confidence)
## Acceptance criteria
- [x] the page holds one specimen per look card, one file, no outside host — verify with `python3 plugin/tests/run.py test_looks_gallery.Gallery`
## Non-goals
## Approach (options → choice → why)
Options: screenshots (static, stale); live specimens built from each card's tokens; a link list. Choice: live specimens: they show motion and type as they really render.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test counting specimens
2. [x] catalogue loader
3. [x] specimen template
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_looks_gallery.Gallery` → ✗ exit 1 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: Gallery 1s) / FAILED (1 classes) [ran] [tree fc33f8820459] (2026-10-22T22:18:54Z)
- (step 2) `python3 plugin/tests/run.py -k test_the_loader_reads_palette_roles_and_the_type_pair` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Gallery 0s) / OK [ran] [tree 2babd9ac1900] (2026-10-22T22:42:52Z)
- (step 3) `python3 plugin/tests/run.py test_looks_gallery.Gallery` → exit 0 · Ran 4 tests in 1.9s (1 classes, 16 at a time; slowest: Gallery 2s) / OK [ran] [tree 2babd9ac1900] (2026-10-22T22:42:55Z)
- (step 3) `python3 plugin/tests/run.py test_looks_gallery.Gallery` → ✗ exit 1 · Ran 5 tests in 3.6s (1 classes, 16 at a time; slowest: Gallery 3s) / FAILED (1 classes) [ran] [tree 816b6521f1ef] (2026-10-22T22:54:49Z)
- (step 3) `python3 plugin/tests/run.py test_looks_gallery.Gallery` → exit 0 · Ran 5 tests in 1.4s (1 classes, 16 at a time; slowest: Gallery 1s) / OK [ran] [tree df97d6d22e76] (2026-10-22T22:55:36Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery test_taste_ledger` → exit 0 · Ran 18 tests in 2.9s (6 classes, 16 at a time; slowest: Gallery 3s, Ledger 2s, Calibration 2s) / OK [ran] [tree 0a4a6fd57da5] (2026-10-22T23:03:43Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery.Gallery` → exit 0 · Ran 5 tests in 2.2s (1 classes, 16 at a time; slowest: Gallery 2s) / OK [ran] [tree 0a4a6fd57da5] (2026-10-22T23:03:47Z)
- (audit intent) `fm-reviewer full pass on the lane (adversary, edge, maintainer, design); all five LOWs fixed test-first: --out refuses a file Foreman didn't write, ticker readable under reduced motion, one look-card parser, hostile line/Motion text escaped, first-specimen border; real afterglow on the pause button fixed after the T-1707 lint fix` → fm page looks writes one self-contained HTML file with a living specimen per look card (12), each in its card's colours, type, motion and texture [tree 0a4a6fd57da5] (2026-10-22T23:03:47Z)
- (audit adversary) `fm-reviewer full pass on the lane (adversary, edge, maintainer, design); all five LOWs fixed test-first: --out refuses a file Foreman didn't write, ticker readable under reduced motion, one look-card parser, hostile line/Motion text escaped, first-specimen border; real afterglow on the pause button fixed after the T-1707 lint fix` → card text is html-escaped (title, line, aria-label, prose; hostile fixture), colours pattern-checked to #hex6, faces from an allowlist, names sanitised; single-pass placeholder substitution; --out refuses links and any existing file without the template's marker [tree 0a4a6fd57da5] (2026-10-22T23:03:47Z)
- (audit edge) `fm-reviewer full pass on the lane (adversary, edge, maintainer, design); all five LOWs fixed test-first: --out refuses a file Foreman didn't write, ticker readable under reduced motion, one look-card parser, hostile line/Motion text escaped, first-specimen border; real afterglow on the pause button fixed after the T-1707 lint fix` → below-fold motion is finished before it is observed so nothing waits hidden; without IntersectionObserver everything plays on load; reduced motion keeps fades only and the ticker scrolls by hand [tree 0a4a6fd57da5] (2026-10-22T23:03:47Z)
- (audit design) `fm-reviewer full pass on the lane (adversary, edge, maintainer, design); all five LOWs fixed test-first: --out refuses a file Foreman didn't write, ticker readable under reduced motion, one look-card parser, hostile line/Motion text escaped, first-specimen border; real afterglow on the pause button fixed after the T-1707 lint fix` → every specimen is its own interface, not a shared card; afterglow lint clean; focus rings and 40px targets; per-specimen colour-scheme [tree 0a4a6fd57da5] (2026-10-22T23:03:47Z)
## Log
- 2026-10-22T20:58:26Z created
- 2026-10-22T20:58:27Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_looks_gallery.py', 'CHANGELOG.md']
- 2026-10-22T20:58:28Z split from T-1539 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:59Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_looks_gallery.Gallery`
- 2026-10-22T21:30:22Z criterion 1 text: the page holds one specimen per look card, one file, no outside host — verify with python3 plugin/tests/run.py test_looks_gallery.Gallery → the page holds one specimen per look card, one file, no outside host
- 2026-10-22T22:12:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1649.builder.md
- 2026-10-22T22:12:50Z focused
- 2026-10-22T22:33:23Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_looks_gallery.py', 'CHANGELOG.md', 'plugin/lib/looks.html', 'MASTER.md']
- 2026-10-22T22:33:24Z scope: + plugin/lib/looks.html (the gallery template, like page.html beside fmpage.py) and MASTER.md (one short note on fm page looks, asked by the main thread)
- 2026-10-22T22:53:57Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_looks_gallery.py', 'CHANGELOG.md', 'plugin/lib/looks.html', 'MASTER.md', 'plugin/lib/fmtaste.py']
- 2026-10-22T22:53:58Z scope: + plugin/lib/fmtaste.py (review nit 3: one parser for look cards, fmtaste.looks returns body + section())
- 2026-10-22T23:03:29Z merged worktree-agent-adac2476fbc405f2c (7 file(s))
- 2026-10-22T23:03:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adac2476fbc405f2c
- 2026-10-22T23:03:31Z focused
- 2026-10-22T23:03:44Z scope: plugin/lib/fmtaste.py (one look-card parser, review item) and MASTER.md (the fm page looks note)
- 2026-10-22T23:04:27Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1654 [FEATURE M, planned, 3 steps] Live task graph showpiece: a one-file 3D page of the task graph, held to the same checks
- T-1539 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second po
- T-1653 [FEATURE M, planned, 3 steps] The repo as a 3D city: one-file page from fm map data with a poster, aria-label and reduced-motion path
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_page.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/lib/fmtaste.py, plugin/lib/looks.html, plugin/tests/test_looks_gallery.py; re-ground the plan against them before editing
## Lessons
- Never gate visible content on a scroll trigger: finish below-fold animations up front and replay them on view, or screenshots and slow devices show empty plates
## Plan gaps
- failed first: step 1 failing test counting specimens
## Files touched
- plugin/tests/test_looks_gallery.py
- plugin/lib/fmpage.py
- plugin/lib/fmcli.py
- plugin/lib/looks.html
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmtaste.py
- plugin/commands/settings.md
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcore.py
- plugin/lib/fmdesign.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlandlock.py
- plugin/lib/fmraster.py
- plugin/lib/fmscene.py
- plugin/lib/fmsettings.py
- plugin/skills/doctor/SKILL.md
- plugin/skills/playbooks/references/ui/scene-3d.md
- plugin/skills/playbooks/references/ui/templates/scene.html
- plugin/tests/fixtures/design/afterglow/crafted.css
- plugin/tests/fixtures/design/afterglow/crafted_nest.css
- plugin/tests/fixtures/design/afterglow/crafted_star.css
- plugin/tests/fixtures/design/afterglow/slop.css
- plugin/tests/helpers.py
- plugin/tests/test_guard_hardening.py
- plugin/tests/test_library.py
- plugin/tests/test_motion_verify.py
