---
id: T-2080
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T02:06:21Z
updated: 2026-10-30T03:06:20Z
base: aafc340dfdbf473ce86ee7b93b8e6b25cb24ba11
base_tree: 967661f7ef8f7bec8543b18130a6bbd009e03794
plan0_at: 2026-10-30T02:06:36Z
plan0_scope: []
verified: ok
---
# Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main
## Raw request
> Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main
## Interpretation
User (mid-run): push the Genesis work to main so they can see every idea, and track Genesis on the website with an interactive graph like ~/Downloads/9af2c148….jpg (the 'Drawing 01' blueprint poster: prompt tower L0–L4, 13 capability cards in Finds/Thinks/Does/Proves, ambition scale, rules, waits-for-your-yes), more detailed. The tower lives in gitignored state/, so it must be exported into the repo (site/genesis/) and the page must be driven by that export so it tracks the run, not a static copy. The push is the user's explicit grant (spent on this task's ship).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis export writes genesis.json (capabilities, missions, gaps by tier, tasks, docs) with home paths and secrets scrubbed — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- [x] site/genesis/index.html renders the tower, 13 capability cards, tier scale and doc drawer from genesis.json with no outside hosts, light and dark, 360 px — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Complete version: export verb (data + docs, scrubbed), a static page in the poster's blueprint look with live data (generation tabs, mission status, task step progress, gap tiers per capability, exam scores, coverage/not-yet counts, standing rules), a doc drawer that renders every tower doc, linked from the site, light+dark, 360 px, keyboard. Approaches: (A) fm genesis export DIR writes genesis.json + the md docs into site/genesis/, a hand-written index.html + genesis.js renders it [chosen: live, readable on GitHub too, no build step change]; (B) a feature page in site/pages.py rendered by build.py [rejected: the feature shell is too narrow for the graph, and build.py can't read gitignored state]; (C) a Python-rendered static SVG poster [rejected: not interactive]; (D) d3/graph lib [rejected: the site loads no outside hosts; plain SVG is enough].
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test for export + page
2. [x] fm genesis export (parse gen-0 caps, seed mission table, gap map tiers, task status, docs)
3. [x] site/genesis page: tower SVG, capability cards, tier scale, lineage, doc drawer
4. [x] export the live tower, shoot 360/1440 light+dark, link from site nav, docs
## Resume here
<!-- auto -->
- 2026-10-30T02:53:46Z step 1/4: red test for export + page
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/index.html, plugin/tests/test_exam.py, site/genesis/
- failures met: modulenotfounderror: no module named 'playwright'
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 7 tests in 1.7s (2 classes, 16 at a time; slowest: Genesis 1s, GenesisExport 0s) / FAILED (1 classes) [ran] [tree 595c97a21ef6] (2026-10-30T02:07:32Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError| File.*test_genesis)|Error:|Ran|OK|FAILED" | head -12` → ✗ exit 1 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: Genesis 2s, GenesisExport 0s) / FAILED (1 classes) [ran] [tree 6f688766657c] (2026-10-30T02:08:45Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError| File.*test_genesis)|Error:|Ran|OK|FAILED" | head -12` → ✗ exit 1 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: Genesis 2s, GenesisExport 0s) / FAILED (1 classes) [ran] [tree 6f688766657c] (2026-10-30T02:08:45Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 7 tests in 1.7s (2 classes, 16 at a time; slowest: Genesis 1s, GenesisExport 0s) / OK [ran] [tree 23ca636f53a2] (2026-10-30T02:17:20Z)
- (step 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_site test_site_build` → exit 0 · Ran 32 tests in 2.8s (11 classes, 16 at a time; slowest: Header 3s, Genesis 2s, Landing 2s) / OK [ran] [tree fed0a600bb97] (2026-10-30T02:20:11Z)
- (step 4) `re-export (4 docs, 1 gen) + headless-chrome shots against a local server: 1440 dark/light, 360 dark, drawer #mission=exam dark and #cap=1 light; nav and feature card link genesis/index.html; MASTER.md + CHANGELOG updated; shots in /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/g-*.png` → renders in both themes, no sideways scroll at 360, drawer shows meta + doc [tree fed0a600bb97] (2026-10-30T02:20:22Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -25` → ✗ exit 1 · Ran 9 tests in 6.1s (2 classes, 16 at a time; slowest: Genesis 5s, GenesisExport 2s) / FAILED (1 classes) [ran] [tree eb28f7d6ea92] (2026-10-30T02:28:05Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -25` → ✗ exit 1 · Ran 9 tests in 6.1s (2 classes, 16 at a time; slowest: Genesis 5s, GenesisExport 2s) / FAILED (1 classes) [ran] [tree eb28f7d6ea92] (2026-10-30T02:28:05Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK)" | head` → ✗ exit 1 · Ran 9 tests in 2.4s (2 classes, 16 at a time; slowest: Genesis 2s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree d4d6b647be85] (2026-10-30T02:28:15Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK)" | head` → ✗ exit 1 · Ran 9 tests in 2.4s (2 classes, 16 at a time; slowest: Genesis 2s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree d4d6b647be85] (2026-10-30T02:28:15Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 9 tests in 1.5s (2 classes, 16 at a time; slowest: Genesis 1s, GenesisExport 1s) / OK [ran] [tree d1d134f0c319] (2026-10-30T02:56:01Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 9 tests in 1.5s (2 classes, 16 at a time; slowest: Genesis 1s, GenesisExport 1s) / OK [ran] [tree d1d134f0c319] (2026-10-30T02:56:01Z)
- (audit adversary) `fm-reviewer pass (adversary, edge, design, maintainer, intent); 2 medium + contrast fixed test-first` → every exported string scrubbed (home → ~, secrets redacted), frac() escaped — fixed [tree d1d134f0c319] (2026-10-30T02:56:01Z)
- (audit edge) `fm-reviewer pass (adversary, edge, design, maintainer, intent); 2 medium + contrast fixed test-first` → no tower refused, junk exam lines dropped, malformed #hash safe — fixed [tree d1d134f0c319] (2026-10-30T02:56:01Z)
- (audit design) `fm-reviewer pass (adversary, edge, design, maintainer, intent); 2 medium + contrast fixed test-first` → light/dark AA contrast, dl order valid — fixed [tree d1d134f0c319] (2026-10-30T02:56:01Z)
- (audit intent) `fm-reviewer pass (adversary, edge, design, maintainer, intent); 2 medium + contrast fixed test-first` → graph, drawer, deep links, landing link met [tree d1d134f0c319] (2026-10-30T02:56:01Z)
## Log
- 2026-10-30T02:06:21Z created
- 2026-10-30T02:06:35Z criterion 1 verify: `PY plugin/tests/run.py test_genesis` → `python3 plugin/tests/run.py test_genesis`
- 2026-10-30T02:06:35Z criterion 2 verify: `PY plugin/tests/run.py test_genesis` → `python3 plugin/tests/run.py test_genesis`
- 2026-10-30T02:06:35Z set approved=True
- 2026-10-30T02:06:35Z guard authorization added: publish
- 2026-10-30T02:06:36Z focused
- 2026-10-30T02:06:43Z focused
- 2026-10-30T02:06:44Z steer: user wants an in-depth look at everything from each generation/tower level: every doc readable in full on the page, per-generation detail (seed, missions, critiques, tasks, exam, decisions), not just the overview graph
- 2026-10-30T02:06:53Z criterion 1 verify: `python3 plugin/tests/run.py test_genesis` → `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- 2026-10-30T02:06:53Z criterion 2 verify: `python3 plugin/tests/run.py test_genesis` → `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- 2026-10-30T02:22:09Z direction: user's blueprint reference (~/Downloads, a JPEG of a tower graph): crane/tower metaphor, tiles per mission, dark blueprint palette
- 2026-10-30T02:22:09Z scope: site/ (genesis page + landing link), MASTER.md, CHANGELOG.md — docs/site surface of the export verb
- 2026-10-30T02:56:21Z done
- 2026-10-30T02:56:23Z committed 808b72aa (2 files)
- 2026-10-30T03:06:20Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- decision 2026-10-30: [cites: user steer 2026-10-29: NO IDEA IS KILLED FOR AMBITION] Genesis standing rule: no idea is killed for ambition — a failed spike gets ≥2 genuin…
- T-1791 [FEATURE S, dropped, 3 steps] Push foreman/build to main so the site publishes
- similar finished tasks took 3–6 steps
## Lessons
- An export that feeds a public page scrubs the whole data tree at the end, not field by field: one recursive pass can't miss a new field
## Plan gaps
- failed first: step 1 red test for export + page
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmgenesis.py
- site/genesis/gap-map.md
- site/genesis/gen-0.md
- site/genesis/gen-1/mission-exam.md
- site/genesis/gen-1/seed.md
- site/genesis/genesis.json
- site/genesis/genesis.css
- site/genesis/index.html
- site/genesis/genesis.js
- site/index.html
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_exam.py
