---
id: T-2118
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T07:47:38Z
updated: 2026-10-30T12:51:59Z
base: aa82235f03a543e02a6446788dddc004b8e4cfe3
base_tree: 27cd27c9d30b486fe14e527de8226f08f154a3ad
plan0_at: 2026-10-30T12:35:46Z
plan0_scope: []
verified: strong
---
# FEATURE M: Genesis on every surface gen-0 names: fm code (fm genesis step as its next…
## Raw request
> FEATURE M: Genesis on every surface gen-0 names: fm code (fm genesis step as its next action), other agents (the shim line), Desktop (a tower panel), statusline tower health — #13's coverage cells on those surfaces are all ideas (critique-genesis)
## Interpretation
The genesis tower's next action (fmgenesis.step) shows only in fm next, and only when the queue is empty. gen-0 says a capability works on every surface it belongs on. Show the tower's health (gen, stage, kind, action) on the statusline, in fm state and fm code's project view, in AGENTS.md for other agents, and in the Desktop/pane view, cheaply: step costs ~80 ms, so it must be cached.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmgenesis.health caches step() and refreshes on a tower edit or a task status change; None without a tower — verify with `python3 plugin/tests/run.py test_genesis.GenesisHealth`
- [x] status.json carries genesis and the statusline draws a tower segment, warn-coloured when not ok — verify with `python3 plugin/tests/run.py test_statusline_ui`
- [x] fm state text and --json, fm code's project view, fm export agents and fm ui --json (with an amber/red signal) show the tower — verify with `python3 plugin/tests/run.py test_genesis.GenesisHealth`
## Non-goals
No new verbs. No tower editing from the surfaces. The site already has its genesis page (T-2105 era) and stays as is.
## Approach (options → choice → why)
Complete version: one cached health(p) read by state_dict, so status.json (statusline), fm state (text and --json, which fm code reads), fm ui --json (pane, Desktop) and fm export agents all get it from one place; a red/amber signal when the tower is blocked, stopped or fatal; no tower = nothing shown and one stat. A: cached fmgenesis.health(p) keyed on tower file mtimes plus task statuses, fed through state_dict (chosen: one source, ~1 ms warm). B: call step() on each surface (rejected: 80 ms on every hook and statusline tick). C: a detached hourly refresh (rejected: stale after a task closes). D: fm next only (rejected: hidden while the queue is busy, which is always).
## Risks and rollback
A step() crash must never break state_dict (try/except → None). Cache key misses a change → stale line until the next tower or task edit; key includes every task's status. Rollback: revert the commit.
## Execution prompt
## Steps
1. [x] health() in fmgenesis with its cache, test-first
2. [x] state_dict/status_dict/render_state wiring and the statusline segment
3. [x] fm code project row, AGENTS.md section, fm ui view key, signal and the pane row
4. [x] docs: MASTER.md, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-30T12:49:31Z steps 4/4 done
- git: foreman/build; 16 uncommitted: CHANGELOG.md, MASTER.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/hooks/statusline, plugin/lib/fmcodetui.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmgenesis.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmgenesis.py, plugin/tests/test_statusline_ui.py, plugin/tests/test_genesis.py, plugin/tests/test_code_tui.py, plugin/lib/fmagents.py, plugin/lib/ui-demo.json
## Docs impact
MASTER.md fmgenesis line; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree 58bf710c4772] (2026-10-30T12:41:19Z)
- (step 2) `python3 plugin/tests/run.py test_statusline_ui` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: StatuslineUi 1s) / OK [ran] [tree 58bf710c4772] (2026-10-30T12:41:20Z)
- (step 3) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree 58bf710c4772] (2026-10-30T12:41:22Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.2s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 723e3d25dd4d] (2026-10-30T12:41:43Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree 723e3d25dd4d] (2026-10-30T12:41:48Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree 723e3d25dd4d] (2026-10-30T12:41:50Z)
- (ac 2) `python3 plugin/tests/run.py test_statusline_ui` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: StatuslineUi 1s) / OK [ran] [tree 723e3d25dd4d] (2026-10-30T12:41:51Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.21s] [ran] [tree b86242fe9702] (2026-10-30T12:43:43Z)
- (audit intent) `fm-reviewer intent lens; status.json refresh after tower edits` → fixed: cmd_genesis regen_views after mutating actions; statusline test drives fm genesis put [tree b484678638ad] (2026-10-30T12:46:27Z)
- (audit adversary) `fm-reviewer adversary lens; seed text on SessionStart/STATE` → fixed: genesis_line defangs; test_a_seed_row_that_reads_as_an_instruction_stays_data; sha1 is a cache key only [tree b484678638ad] (2026-10-30T12:46:27Z)
- (audit edge) `fm-reviewer edge lens; crash caching` → fixed: a raising step isn't cached; test asserts the next call recovers [tree b484678638ad] (2026-10-30T12:46:27Z)
- (audit maintainer) `fm-reviewer maintainer lens; wiring tests` → fixed: open_project test in test_code_tui, pane tests ok/done in foreman-ui.test.tsx (153 pass) [tree b484678638ad] (2026-10-30T12:46:28Z)
- (audit operator) `fm-reviewer operator lens; always-on cost` → fixed: shim line removed (AGENTS.md section is already gated on a tower); duplicate blocked signal kept: it names the Mission [tree b484678638ad] (2026-10-30T12:46:28Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree b484678638ad] (2026-10-30T12:46:35Z)
- (step 2) `python3 plugin/tests/run.py test_statusline_ui` → exit 0 · Ran 7 tests in 1.6s (1 classes, 16 at a time; slowest: StatuslineUi 1s) / OK [ran] [tree b484678638ad] (2026-10-30T12:46:36Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui test_genesis.GenesisHealth` → exit 0 · Ran 242 tests in 7.3s (47 classes, 16 at a time; slowest: Fuzz 7s, Command 6s, Extras 4s) / OK [ran] [tree b484678638ad] (2026-10-30T12:46:44Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree b484678638ad] (2026-10-30T12:46:57Z)
- (ac 2) `python3 plugin/tests/run.py test_statusline_ui` → exit 0 · Ran 7 tests in 1.6s (1 classes, 16 at a time; slowest: StatuslineUi 1s) / OK [ran] [tree b484678638ad] (2026-10-30T12:46:57Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / OK [ran] [tree b484678638ad] (2026-10-30T12:46:57Z)
- (audit edge) `one fm-reviewer pass over 5 lenses; all 5 findings fixed test-first` → a raising step isn't cached; no tower returns None [tree b484678638ad] (2026-10-30T12:46:57Z)
- (audit adversary) `one fm-reviewer pass over 5 lenses; all 5 findings fixed test-first` → genesis_line defanged on every surface [tree b484678638ad] (2026-10-30T12:46:57Z)
- (audit intent) `re-read gen-0's 'pane/status surface if it has state' against the diff after the demo-key fix` → every surface named carries genesis; the demo view now matches a real one [tree c433a1e7d073] (2026-10-30T12:50:58Z)
- (audit edge) `demo key added; test_board_surfaces, foreman-ui mod (153) re-run` → a raising step isn't cached; no tower returns None; demo has every real key [tree c433a1e7d073] (2026-10-30T12:50:58Z)
- (audit edge) `one fm-reviewer pass over 5 lenses; all 5 findings fixed test-first; re-audited after the demo-key fix` → a raising step isn't cached; no tower returns None [tree c433a1e7d073] (2026-10-30T12:51:04Z)
- (audit adversary) `one fm-reviewer pass over 5 lenses; all 5 findings fixed test-first; re-audited after the demo-key fix` → genesis_line defanged on every surface [tree c433a1e7d073] (2026-10-30T12:51:04Z)
## Log
- 2026-10-30T07:47:38Z created
- 2026-10-30T12:35:45Z planned: it has criteria and steps
- 2026-10-30T12:35:45Z focused
- 2026-10-30T12:43:31Z scope: mods/foreman-ui/tests/foreman-ui.test.tsx — the pane's genesis row gets its test
- 2026-10-30T12:46:47Z scope: plugin/tests/test_code_tui.py — fm code's project-view genesis row test (review)
- 2026-10-30T12:50:58Z scope: plugin/lib/ui-demo.json — fm ui --demo carries the genesis key a real view has (test_board_surfaces)
- 2026-10-30T12:51:57Z done
- 2026-10-30T12:51:59Z committed c96a3382 (16 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
## Lessons
- A new state surface must be refreshed by the verbs that change its source, not only by task mutations: a hand-called regen_views in a test hides that gap
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcore.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/hooks/statusline
- plugin/lib/fmagents.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcost.py
- plugin/lib/fmhooks.py
- plugin/lib/fmwatch.py
- plugin/tests/test_statusline_ui.py
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_code_tui.py
- plugin/lib/ui-demo.json
