---
id: T-2086
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmmap.py, plugin/tests/test_map.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-30T03:04:17Z
updated: 2026-10-30T13:46:49Z
base: f0850f6aeabfd06d718d22f571eb6dc197d63ea5
base_tree: 9df38fc32193a0621c3ea367af6cf93a8e6ddce6
plan0_at: 2026-10-30T13:37:10Z
plan0_scope: [plugin/lib/fmmap.py, plugin/tests/test_map.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# T-2080's close passed its gates but fm ship's scratch-tree run failed…
## Raw request
> T-2080's close passed its gates but fm ship's scratch-tree run failed test_design_lint.Site on site/genesis/genesis.css: find why the close-time gate missed it (affected-only run, or a reused pass on another tree?)
## Interpretation
Diagnosed: T-2080's close ran only the fm map-linked tests (test_cli test_exam test_genesis). fm map links a test to sources by file name only, so test_design_lint, which lints the whole site/ folder, was never linked to site/genesis/genesis.css. Fix: a test that names a top-level folder as a string literal ("site", "mods"), other than its own, is linked to every file under it; tests_for matches files under a linked folder.
## Assumptions (confidence)
## Acceptance criteria
- [x] a change under a top-level folder runs the tests that name that folder (fm impact / tests_for), and not a folder the test lives in — verify with `python3 plugin/tests/run.py test_map`
- [x] the close-gate and map suites stay green — verify with `python3 plugin/tests/run.py test_map test_close_gates test_graph test_ecosystem test_debug`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_map: a test naming "site" is linked to site/style.css
2. [x] fmmap.build links folder literals; tests_for matches under them; VERSION bump
3. [x] MASTER + CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_map` → ✗ exit 1 · Ran 9 tests in 3.2s (3 classes, 16 at a time; slowest: Map 2s, Cold 0s, RoundG 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 44cb78647a52] (2026-10-30T13:38:30Z)
- `python3 plugin/tests/run.py test_map` → exit 0 · Ran 9 tests in 2.4s (3 classes, 16 at a time; slowest: Map 2s, Cold 0s, RoundG 0s) / OK [ran] [tree 44cb78647a52] (2026-10-30T13:38:30Z)
- (step 1) `python3 plugin/tests/run.py test_map` → exit 0 · Ran 9 tests in 2.4s (3 classes, 16 at a time; slowest: Map 2s, Cold 0s, RoundG 0s) / OK [ran] [tree 44cb78647a52] (2026-10-30T13:38:39Z)
- (step 2) `python3 plugin/tests/run.py test_map test_close_gates test_graph test_ecosystem test_debug` → exit 0 · Ran 55 tests in 13.5s (20 classes, 16 at a time; slowest: CloseGates 13s, HarnessCanary 4s, Map 3s) / OK [ran] [tree 44cb78647a52] (2026-10-30T13:38:53Z)
- (step 3) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 97540478a4ff] (2026-10-30T13:39:04Z)
- (ac 1) `python3 plugin/tests/run.py test_map` → exit 0 · Ran 9 tests in 2.4s (3 classes, 16 at a time; slowest: Map 2s, Cold 0s, RoundG 0s) / OK [ran] [tree 97540478a4ff] (2026-10-30T13:39:48Z)
- (ac 2) `python3 plugin/tests/run.py test_map test_close_gates test_graph test_ecosystem test_debug` → exit 0 · Ran 55 tests in 13.6s (20 classes, 16 at a time; slowest: CloseGates 13s, HarnessCanary 4s, Map 3s) / OK [ran] [tree 97540478a4ff] (2026-10-30T13:39:48Z)
- `python3 plugin/tests/run.py test_map test_close_gates` → exit 0 · Ran 25 tests in 13.3s (4 classes, 16 at a time; slowest: CloseGates 13s, Map 2s, Cold 0s) / OK [ran] [tree 97540478a4ff] (2026-10-30T13:39:48Z)
- (audit edge) `self: re-read the diff; links only widen (a folder literal can over-run tests at close, never skip one); the test's own top folder is excluded so plugin/ tests don't link the world; fixtures/helpers under tests/ and symlinks are skipped; reads capped at 200 KB; map VERSION bumped so old maps rebuild; on this repo a site/ change now links 15 tests incl. test_design_lint` → a literal that is only a key ("bench") over-runs a few tests at close; a glob path (site/*) matches; a repo with no folders links nothing; fm find never builds a map, so untrusted repos aren't read [tree 97540478a4ff] (2026-10-30T13:39:48Z)
- (audit self) `self: re-read the diff; links only widen (a folder literal can over-run tests at close, never skip one); the test's own top folder is excluded so plugin/ tests don't link the world; fixtures/helpers under tests/ and symlinks are skipped; reads capped at 200 KB; map VERSION bumped so old maps rebuild; on this repo a site/ change now links 15 tests incl. test_design_lint` → no findings [tree 97540478a4ff] (2026-10-30T13:39:48Z)
## Log
- 2026-10-30T03:04:17Z created
- 2026-10-30T13:37:08Z set type=FIX, tier=S, scope=['plugin/lib/fmmap.py', 'plugin/tests/test_map.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-30T13:37:09Z planned: it has criteria and steps
- 2026-10-30T13:37:09Z focused
- 2026-10-30T13:37:14Z criterion 2 verify: `python3 plugin/tests/run.py test_map test_close_gates test_graph test_eco` → `python3 plugin/tests/run.py test_map test_close_gates`
- 2026-10-30T13:37:22Z criterion 2 verify: `python3 plugin/tests/run.py test_map test_close_gates` → `python3 plugin/tests/run.py test_map test_close_gates test_graph test_ecosystem test_debug`
- 2026-10-30T13:40:11Z done
- 2026-10-30T13:40:13Z committed e2204cf8 (4 files)
- 2026-10-30T13:40:24Z guard authorization added: publish
- 2026-10-30T13:46:49Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2087 [FIX M, done, 3 steps] Genesis page matches the site: shared header, footer and style.css tokens — lesson: A sub-page that loads the site stylesheet inherits its …
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-0952 [FEATURE S, done, 1 steps] --affected also runs tests that historically change together with the edited files (the map's co-change pairs), so a hooks.json edit ru…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- likely tests for the scope: plugin/tests/test_map.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, MASTER.md, plugin/lib/fmmap.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_map.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- MASTER.md
