---
id: T-2148
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-30T10:53:35Z
updated: 2026-10-30T12:01:02Z
base: 1a1d9d5d3b1fcec8d57e6c52f404333de5556495
base_tree: 8f48207adb3159a5fcba66f3feb974382b26e9eb
plan0_at: 2026-10-30T11:47:15Z
plan0_scope: []
verified: strong
---
# Catch it earlier: T-2138 ran only test_hooks while iterating; the docs count lives in…
## Raw request
> T-2147 (Baseline red: `python3 plugin/tests/run.py` fails…) wasn't caught before it shipped: T-2138 ran only test_hooks while iterating; the docs count lives in test_docs, which only the full gate runs
## Interpretation
T-2138 edited MASTER.md and broke test_docs' note count; fm check --affected never ran test_docs because MASTER.md is a hub (no co-change pairs) and has no name-linked test. Make the affected set learn which files broke which tests from past baseline-red tasks.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm check --affected runs a test a closed baseline-red task named failing when a file its fix commit changed changes again, hub files included; open or dropped baseline tasks teach nothing — verify with `python3 plugin/tests/run.py test_affected_hubs`
## Non-goals
## Approach (options → choice → why)
Options: (1) link tests to the docs they name by text (README in 39 test files, CHANGELOG in 19: every close runs them; T-1467 cut exactly that); (2) a configured doc→test list (hardcoded, not learned); (3) learn from closed baseline-red tasks: the files each fix commit changed point at the tests the gate named failing, cached in the map (rebuilt per HEAD). Chose 3: data, not lists; the T-2147 fix touched only MASTER.md, so it links MASTER.md → test_docs and nothing else.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fmmap._broke learns {file: tests} from closed baseline tasks' fix commits; affected() adds them
## Resume here
<!-- auto -->
- 2026-10-30T11:48:29Z steps 1/1 done
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmmap.py, plugin/tests/test_affected_hubs.py
- touched since last checkpoint: plugin/tests/test_affected_hubs.py, plugin/lib/fmcli.py, plugin/lib/fmmap.py
## Docs impact
MASTER.md fm check --affected line, CHANGELOG bullet
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_affected_hubs` → red as expected (exit 1) · Ran 2 tests in 1.7s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / FAILED (1 classes) [ran] [tree 06d72b743bc9] (2026-10-30T11:47:21Z)
- (step 1) `python3 plugin/tests/run.py test_affected_hubs` → red as expected (exit 1) · Ran 2 tests in 1.9s (1 classes, 16 at a time; slowest: AffectedHubs 2s) / FAILED (1 classes) [ran] [tree f72144e1a8fd] (2026-10-30T11:47:51Z)
- `python3 plugin/tests/run.py test_affected_hubs` → ✗ exit 1 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f3034d6027e2] (2026-10-30T11:50:56Z)
- `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / OK [ran] [tree f3034d6027e2] (2026-10-30T11:50:56Z)
- `python3 plugin/tests/run.py test_affected_hubs` → ✗ exit 1 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7f06e0e0e2aa] (2026-10-30T11:54:38Z)
- `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / OK [ran] [tree 7f06e0e0e2aa] (2026-10-30T11:54:38Z)
- (ac 1) `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / OK [ran] [tree 7f06e0e0e2aa] (2026-10-30T11:54:40Z)
- (audit edge) `fm-reviewer pass (intent, edge, adversary, maintainer); live map measured: MASTER.md → test_docs, fmcli.py → 3 tests, 0.08 s` → docs-only fix linked CHANGELOG → doc links only to a test naming it; dotted unittest names now match; >20-file commits skipped [tree 7f06e0e0e2aa] (2026-10-30T11:54:40Z)
- (audit intent) `fm-reviewer pass (intent, edge, adversary, maintainer); live map measured: MASTER.md → test_docs, fmcli.py → 3 tests, 0.08 s` → archived baseline tasks now count (include_archive) [tree 7f06e0e0e2aa] (2026-10-30T11:54:40Z)
- (audit adversary) `fm-reviewer pass (intent, edge, adversary, maintainer); live map measured: MASTER.md → test_docs, fmcli.py → 3 tests, 0.08 s` → none; names and subjects only feed set and regex matches [tree 7f06e0e0e2aa] (2026-10-30T11:54:40Z)
- (audit maintainer) `fm-reviewer pass (intent, edge, adversary, maintainer); live map measured: MASTER.md → test_docs, fmcli.py → 3 tests, 0.08 s` → ok, third git log in build() is 0.05 s [tree 7f06e0e0e2aa] (2026-10-30T11:54:40Z)
## Log
- 2026-10-30T10:53:35Z created
- 2026-10-30T11:47:09Z set tier=M, type=FIX
- 2026-10-30T11:47:09Z planned: it has criteria and steps
- 2026-10-30T11:47:14Z focused
- 2026-10-30T11:55:01Z done
- 2026-10-30T11:55:03Z committed dca36dd2 (5 files)
- 2026-10-30T11:58:38Z guard authorization added: publish
- 2026-10-30T12:01:02Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1776 [FEATURE S, done, 1 steps] Catch it earlier: T-1608 ran test_guard_hardening, test_docs and test_cli; the help-positi — lesson: A test of a file's own contents be…
- T-0952 [FEATURE S, done, 1 steps] --affected also runs tests that historically change together with the edited files (the map's co-change pairs), so a hooks.json edit ru…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 1–5 steps
## Why not caught
a hub file has no co-change pairs, so --affected ran no docs test for a MASTER.md edit
## Lessons
- A file in every task's pairs carries no co-change signal; learn its tests from what it once broke
## Files touched
- plugin/tests/test_affected_hubs.py
- plugin/lib/fmcli.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- MASTER.md
