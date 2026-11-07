---
id: T-3468
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/release.py, plugin/tests/test_ship.py, CHANGELOG.md, docs/map/**, MASTER.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh]
depends_on: []
source: discovered
created: 2026-11-06T16:56:39Z
updated: 2026-11-07T00:48:02Z
base: 89d0d3468a2770da2f90299261ea1f467b4500ce
base_tree: 9b757399c14a04329ce334557e059834a049f1f8
lane_stop: merged 2026-11-06T18:53:59Z
verified: strong
unproven: [perf-typed]
---
# Sampo ship reruns the whole suite (20 min at -j 6) on a tree that differs from the…
## Raw request
> sampo ship reruns the whole suite (20 min at -j 6) on a tree that differs from the train's just-gated one only by tower data files CI ignores (T-3439's paths-ignore): reuse that check_run pass when the only difference is in those paths, so a ship after a train costs minutes and doesn't double the machine's load during the next train
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo ship skips its own suite run when the gates passed on the same code tree and the pushed tree differs from HEAD's only in CI-ignored paths, CHANGELOG.md and the sync mirror; any other difference runs the suite — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then the reuse check before the ship's test run
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship.Ship.test_a_ship_reuses_the_gates_pass_when_only_ci_skipped_tower_files_differ` → ✗ exit 1 · Ran 1 tests in 117.5s (1 jobs, 16 at a time; slowest: Ship 1s) / FAILED (1 classes: test_ship.Ship) [ran] [tree ec070131eb96] [world 2f1906870a] (2026-11-06T18:24:15Z)
- (step 1) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 101 tests in 8.7s (79 jobs, 16 at a time; slowest: BoardVerbs 4s, Release.test_the_canary_runs_detached_and_its_failure_lands_in_the_inbox_and_the_notify_hook 4s, ReleaseProof 3s) / OK [ran] [tree 6b870c96a53b] [world 2f1906870a] (2026-11-06T18:26:12Z)
- (step 1) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 102 tests in 36.3s (32 jobs, 16 at a time; slowest: Ship 35s, Release.test_the_canary_runs_detached_and_its_failure_lands_in_the_inbox_and_the_notify_hook 4s, BoardVerbs 3s) / OK [ran] [tree 9ea68507d8fd] [world 2f1906870a] (2026-11-06T18:31:28Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 0da6e8c5f0be] (2026-11-06T18:59:20Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 8938eecee068] (2026-11-07T00:44:54Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 60 tests in 58.8s (52 jobs, 16 at a time; slowest: Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check 3s, Ship.test_a_green_ship_records_the_footprint_and_a_red_one_does_not [ran] [tree 8938eecee068] [world 2f1906870a] (2026-11-07T00:45:58Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 8938eecee068] (2026-11-07T00:45:58Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 8938eecee068] (2026-11-07T00:45:58Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 8938eecee068] (2026-11-07T00:45:58Z)
## Log
- 2026-11-06T16:56:39Z created
- 2026-11-06T18:20:37Z set tier=M, scope=['plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md']
- 2026-11-06T18:20:38Z planned: it has criteria and steps
- 2026-11-06T18:20:38Z lane: ~/.claude/foreman.lanes/T-3468 on foreman/T-3468
- 2026-11-06T18:24:15Z start point recorded late (no focus had kept one): its diff starts at 81de611
- 2026-11-06T18:53:59Z merged foreman/T-3468 in merge train
- 2026-11-06T18:59:19Z set scope=['plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T18:59:20Z scope: widened at merge to the reviewed lane's own diff (9dec1d336), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-07T00:44:54Z set scope=['plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh']
- 2026-11-07T00:44:54Z scope: widened at merge to the reviewed lane's own diff (9dec1d336), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T00:47:52Z done
- 2026-11-07T00:48:02Z lane removed: ~/.claude/foreman.lanes/T-3468; dropped: merged and closed
## Follow-ups captured
## Measurements
ship test run: 999 s (the full 7,141-test suite rerun at the 12:37 ship, after the train's gates had passed the same code) → 0 s when the gates' pass covers the pushed tree (only CI-ignored or mirror .md paths differ; test_ship's reuse case)
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A second full run of the same code is waste: a gate pass needs to be findable by every later step that would rerun it.
## Plan gaps
- failed first: step 1 failing tests, then the reuse check before the ship's test run
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/sampo/release.py
- plugin/tests/test_ship.py
- scripts/probe-plugin-rename.sh
