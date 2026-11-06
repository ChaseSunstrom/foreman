---
id: T-1713
type: CLEAN
tier: S
status: done
priority: normal
scope: [MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-23T01:27:14Z
updated: 2026-10-23T03:00:59Z
base: 319db56a750d6116dc3ce9f5d0c3d76e9d3ae54c
base_tree: eaecda33798a95625a2bce216c245e9634af65fb
plan0_at: 2026-10-23T02:49:51Z
plan0_scope: [MASTER.md, CHANGELOG.md]
verified: ok
---
# MASTER.md: one line per plugin/lib module instead of one 22,000-character table row
## Raw request
> MASTER.md keeps many modules on one long table line, so two lanes touching it conflict on every merge: split the plugin/lib row into one line per module
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] MASTER.md's plugin/lib row points to a list with one bullet per module, every module named before is still named, and the docs tests pass — verify with `python3 plugin/tests/run.py test_docs test_doctor test_docsdrift`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] behaviour lock
2. [x] split the row
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · SessionEnd                 158.0   400.9     150  [0] / machine busy (load 3.6 per core): judged by each hook's CPU time, not wall time (T-0805) [ran] [tree eaecda33798a] (2026-10-23T02:58:35Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_doctor test_docsdrift` → exit 0 · Ran 131 tests in 10.2s (37 classes, 16 at a time; slowest: Fences 10s, Command 6s, TaskLifecycle 4s) / OK [ran] [tree 3924ad7e3928] (2026-10-23T02:59:38Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_doctor test_docsdrift` → exit 0 · Ran 131 tests in 12.1s (37 classes, 16 at a time; slowest: Fences 12s, Command 2s, TaskLifecycle 2s) / OK [ran] [tree 3924ad7e3928] (2026-10-23T02:59:51Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_doctor test_docsdrift` → exit 0 · Ran 131 tests in 12.3s (37 classes, 16 at a time; slowest: Fences 12s, Command 6s, TaskLifecycle 5s) / OK [ran] [tree 3924ad7e3928] (2026-10-23T03:00:11Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_doctor test_docsdrift` → exit 0 · Ran 131 tests in 12.1s (37 classes, 16 at a time; slowest: Fences 12s, Command 6s, ViewsRepair 4s) / OK [ran] [tree 3924ad7e3928] (2026-10-23T03:00:25Z)
- (audit self) `self: a depth-aware splitter (backticks and brackets) cut the 22,013-char cell at top-level ', '' into 66 module bullets; docs, doctor and docs-drift tests green` → every module named before is a bullet now; the longest line left is 3,367 chars (one module's own entry) [tree 3924ad7e3928] (2026-10-23T03:00:25Z)
## Log
- 2026-10-23T01:27:14Z created
- 2026-10-23T02:49:40Z planned from capture
- 2026-10-23T02:49:44Z set scope=['MASTER.md', 'CHANGELOG.md']
- 2026-10-23T02:49:48Z focused
- 2026-10-23T03:00:12Z behaviour lock: the pre-edit full run's only failures were the two load flakes captured as T-1721; the docs tests that read MASTER.md passed before and after
- 2026-10-23T03:00:58Z done
- 2026-10-23T03:00:59Z committed 88f60b15 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1144 [CLEAN M, done, 2 steps] Help tiers no longer a shared line every new command edits: each fm command declares its h — lesson: A registry every feature appends to …
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- T-1161 [FEATURE M, done, 2 steps] Record files that conflicted at `fm lane merge` and warn in `fm lane brief` when a new lan — lesson: count distinct actors, not events,…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, MASTER.md; re-ground the plan against them before editing
## Lessons
- A shared single-line registry in a doc is a merge-conflict magnet: one line per entry
## Plan gaps
- failed first: step 1 behaviour lock
## Files touched
- MASTER.md
- CHANGELOG.md
