---
id: T-1823
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:13:25Z
updated: 2026-10-28T09:16:58Z
base: ffbddc08d6ffcbe7739a66d6e8d7c7c246c1d8ec
base_tree: f186e3685c41836476fe66b60f25d1aaadb2b311
plan0_at: 2026-10-28T09:09:31Z
plan0_scope: []
verified: strong
---
# FEATURE: a dropped builder result's redo starts from the drop reason and the first attempt
## Raw request
> FEATURE: a dropped builder result's redo starts from the drop reason and the first attempt's failing check (fmrecall.nearest_dropped exists; T-1798 brainstorm)
## Interpretation
When the main thread drops a builder's branch (its merge re-run was red, or review rejected it) and redoes the task with a new builder, the new builder starts blind. fm lane rm ID --why "<reason>" records the drop (reason, kept branch, the last merge_refused check on the ledger) on the brief, and the next fm lane brief adds a 'First attempt (dropped)' section with them.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane rm ID --why records the reason, kept branch and last red check; the next fm lane brief has a 'First attempt (dropped)' section with all three — verify with `cd plugin/tests && python3 -m unittest -q test_builder.DroppedRedo`
## Non-goals
No automatic redo; race losers (fm lane pick) keep their own drop path.
## Approach (options → choice → why)
Options: (a) meta lane_dropped written by lane rm --why, read by builder_brief; (b) builder_brief scans the ledger for lane_rm + merge_refused events; (c) fmrecall.nearest_dropped-style log grep. Choice: (a), the failing check taken from the ledger's last merge_refused enforce event at rm time — one place writes, one reads, no scan per brief.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: DroppedRedo in test_builder
2. [x] lane rm --why + builder_brief section; delegate.md step 4
3. [x] Gates and review
## Resume here
<!-- auto -->
- 2026-10-28T09:12:27Z step 2/3: lane rm --why + builder_brief section; delegate.md step 4
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/skills/intake/references/delegate.md, plugin/tests/test_builder.py
- touched since last checkpoint: plugin/tests/test_builder.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/skills/intake/references/delegate.md, CHANGELOG.md, MASTER.md
## Docs impact
CHANGELOG.md MASTER.md plugin/skills/intake/references/delegate.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_builder.DroppedRedo` → ✗ exit 1 · Ran 2 tests in 1.194s / FAILED (failures=1) [ran] [tree dd80818c8ad1] (2026-10-28T09:09:37Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_builder.DroppedRedo` → exit 0 · Ran 2 tests in 1.303s / OK [ran] [tree 5daefa01161c] (2026-10-28T09:11:44Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmlanes.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn,; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.4    42.7     150  [0] / SessionEnd                  35.6    38.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree d35af88f1907] (2026-10-28T09:15:50Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_builder test_lanes` → exit 0 · Ran 55 tests in 27.418s / OK [ran] [tree d35af88f1907] (2026-10-28T09:16:24Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_builder.DroppedRedo` → exit 0 · Ran 2 tests in 1.285s / OK [ran] [tree d35af88f1907] (2026-10-28T09:16:32Z)
- (audit intent) `self-review of the diff (fmlanes rm/remove/builder_brief, fmcli --why, delegate.md step 4, DroppedRedo tests): drop only from the main thread, uncommitted work still refused, branch kept, check fenced and redacted` → a redo builder's brief now carries the drop reason, the kept branch (git diff to read, never merge) and the last refused merge's red check; plain rm unchanged [tree d35af88f1907] (2026-10-28T09:16:32Z)
- (audit edge) `self-review of the diff (fmlanes rm/remove/builder_brief, fmcli --why, delegate.md step 4, DroppedRedo tests): drop only from the main thread, uncommitted work still refused, branch kept, check fenced and redacted` → a finished builder's CC-locked worktree blocked any rm of unmerged work; --why unlocks it (uncommitted work still refused); _last_refusal reads only the 500-event ledger tail; a stale dropped.json carries into later briefs on purpose [tree d35af88f1907] (2026-10-28T09:16:32Z)
- (audit adversary) `self-review of the diff (fmlanes rm/remove/builder_brief, fmcli --why, delegate.md step 4, DroppedRedo tests): drop only from the main thread, uncommitted work still refused, branch kept, check fenced and redacted` → a builder can't drop its own work (--why refused from a lane, tested); the check text goes through c.redact and a code fence, as data [tree d35af88f1907] (2026-10-28T09:16:32Z)
## Log
- 2026-10-28T08:13:25Z created
- 2026-10-28T08:14:55Z set status=planned
- 2026-10-28T09:09:31Z focused
- 2026-10-28T09:16:57Z done
- 2026-10-28T09:16:58Z committed 23f12f0e (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1798-triage: Source: research/brainstorm-20261028-025248 (4 rounds × 14 lenses, 626 distinct ideas; the simplicity lens failed in round 3).
- research brainstorm-intelligence-20261009: 768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capabilit…
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- the similar finished task took 4 steps
## Lessons
- brief meta is one line per key: keep structured or multi-line data in an audits/ sidecar file
## Plan gaps
- failed first: step 1 Failing test: DroppedRedo in test_builder
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- plugin/skills/intake/references/delegate.md
- CHANGELOG.md
- MASTER.md
