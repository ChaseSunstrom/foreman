---
id: T-2083
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/genesis/genesis.js, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T02:55:52Z
updated: 2026-10-30T13:18:52Z
base: cfcf35af48f84221ec7bf013ae61bb04c67d1783
base_tree: fda174603e7b84eda37560162d3a3ef7848c2a5d
plan0_at: 2026-10-30T13:09:38Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/genesis/genesis.js, CHANGELOG.md]
verified: strong
---
# Genesis page: seed ROW regex misses rows with backticks or no trailing pipe; md renderer…
## Raw request
> Genesis page: seed ROW regex misses rows with backticks or no trailing pipe; md renderer untested; focus lost after selectGen from a drawer chip
## Interpretation
Three slips on the Genesis surfaces: (1) fmgenesis.ROW drops a hand-written seed row whose file name is in backticks, and a row with no trailing pipe swallows the next row, so step says 'lists no Missions' or skips one; (2) the page's markdown renderer (escape, link filter) has no test; (3) a drawer chip that switches generation rewrites the drawer and focus falls to the page.
## Assumptions (confidence)
## Acceptance criteria
- [x] ROW reads backticked names and rows with no trailing pipe, one row per line — verify with `python3 plugin/tests/run.py test_genesis`
- [x] The page's md() escapes HTML, drops non-https links and renders tables, run under node — verify with `python3 plugin/tests/run.py test_genesis.GenesisExport`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: ROW on backticks and a missing trailing pipe; md() under node
2. [x] Widen ROW to one line per row with optional backticks
3. [x] show() moves focus to the drawer title when it replaces open content
## Resume here
<!-- auto -->
- 2026-10-30T13:14:25Z steps 3/3 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/genesis/genesis.js
- touched since last checkpoint: plugin/lib/fmgenesis.py, site/genesis/genesis.js, CHANGELOG.md, plugin/tests/test_genesis.py
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_genesis.GenesisStep.test_a_hand_written_seed_row_reads_with_backticks_or_no_trailing_pipe` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: GenesisStep 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bdcdd14579a2] (2026-10-30T13:12:11Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep.test_a_hand_written_seed_row_reads_with_backticks_or_no_trailing_pipe` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GenesisStep 0s) / FAILED (1 classes) [ran] [tree bdcdd14579a2] (2026-10-30T13:12:11Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep.test_a_hand_written_seed_row_reads_with_backticks_or_no_trailing_pipe` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: GenesisStep 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6529f701c830] (2026-10-30T13:12:24Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep.test_a_hand_written_seed_row_reads_with_backticks_or_no_trailing_pipe` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisStep 0s) / OK [ran] [tree 6529f701c830] (2026-10-30T13:12:24Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisStep.test_a_hand_written_seed_row_reads_with_backticks_or_no_trailing_pipe test_genesis.GenesisExport.test_the_page_markdown_escapes_and_keeps_only_safe_links` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: GenesisStep 0s, GenesisExport 0s) / OK [ran] [tree dc91dc01f491] (2026-10-30T13:13:26Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 76 tests in 8.6s (12 classes, 16 at a time; slowest: GenesisLive 8s, GenesisSweep 7s, GenesisCheck 6s) / FAILED (1 classes) [ran] [tree dc91dc01f491] (2026-10-30T13:13:35Z)
- (step 3) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/focus_check.py false` → exit 0 · 127.0.0.1 - - [30/Oct/2026 08:13:35] "GET /genesis.json HTTP/1.1" 200 - / dr-title open=true [ran] [tree dc91dc01f491] (2026-10-30T13:13:37Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 76 tests in 8.9s (12 classes, 16 at a time; slowest: GenesisLive 8s, GenesisSweep 7s, GenesisCheck 6s) / FAILED (1 classes) [ran] [tree dc91dc01f491] (2026-10-30T13:13:46Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis.GenesisExport` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: GenesisExport 2s) / OK [ran] [tree dc91dc01f491] (2026-10-30T13:13:48Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 76 tests in 8.6s (12 classes, 16 at a time; slowest: GenesisLive 8s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree f45b25883a9a] (2026-10-30T13:14:20Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 76 tests in 4.5s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f45b25883a9a] (2026-10-30T13:14:25Z)
- (audit self) `read the diff: ROW regex, two genesis.js lines, two new tests, one updated test input` → regex keeps one row per line ([^|\n]), mission- prefix still required; focus only moves when the dialog is already open [tree f45b25883a9a] (2026-10-30T13:16:00Z)
- (audit design) `headless Chromium: click a drawer generation chip, read document.activeElement` → before: BODY; after: dr-title, drawer stays open; no visual change [tree f45b25883a9a] (2026-10-30T13:16:00Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 76 tests in 4.2s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f45b25883a9a] (2026-10-30T13:16:11Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis.GenesisExport` → exit 0 · Ran 5 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisExport 1s) / OK [ran] [tree f45b25883a9a] (2026-10-30T13:16:11Z)
- (audit edge) `self + design audits recorded; headless Chromium focus check before/after` → a row with no closing pipe at end of file still reads; a row with no mission- prefix stays unparsed, so T-2119's fatal check holds [tree f45b25883a9a] (2026-10-30T13:16:11Z)
- (audit self) `self + design audits recorded; headless Chromium focus check before/after` → no findings [tree f45b25883a9a] (2026-10-30T13:16:11Z)
## Log
- 2026-10-30T02:55:52Z created
- 2026-10-30T13:09:35Z set type=FIX, tier=S
- 2026-10-30T13:09:35Z set scope=['plugin/lib/fmgenesis.py', 'plugin/tests/test_genesis.py', 'site/genesis/genesis.js', 'CHANGELOG.md']
- 2026-10-30T13:09:35Z planned: it has criteria and steps
- 2026-10-30T13:09:36Z focused
- 2026-10-30T13:09:39Z set approved=True
- 2026-10-30T13:14:25Z steer: T-2119's fatal-not-dry test used a backticked row as its unparseable example; now valid by design, so it uses a row without the mission- prefix (same intent)
- 2026-10-30T13:16:14Z done
- 2026-10-30T13:16:15Z committed 8bfb9341 (4 files)
- 2026-10-30T13:16:25Z guard authorization added: publish
- 2026-10-30T13:18:52Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2095-review: Verdict:** approve with nits. It meets the criteria as written. One resumability gap and one silent-skip case are worth fixing. I did not run `pl…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-2102-review: Verdict:** changes needed. Finding 1 is a MEDIUM that breaks the "seed N output passes step's seed-row rules (<= 8 rows)" MUST. I read the code a…
- decision 2026-10-30: T-2105: the breaker stops after three reverted generations in a row, not two
- similar past tasks were M: consider --tier M
- the similar finished task took 5 steps
- likely tests for the scope: plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/genesis/genesis.js; re-ground the plan against them before editing
## Plan gaps
- failed first: step 2 Widen ROW to one line per row with optional backticks
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- site/genesis/genesis.js
- CHANGELOG.md
