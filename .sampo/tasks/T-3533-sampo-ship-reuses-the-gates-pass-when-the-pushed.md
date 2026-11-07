---
id: T-3533
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, plugin/lib/sampo/cli.py, plugin/lib/sampo/release.py, plugin/tests/test_ship.py]
depends_on: []
source: self
created: 2026-11-06T21:52:50Z
updated: 2026-11-07T02:20:48Z
base: afca369d5306798d95690ce1a45d2cb7977963e6
base_tree: 26dea69e852fd2d4d59227aa10701119e0110227
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T22:18:29Z
plan0_scope: []
group: stats.json driven tower commits and ship tests
lane_stop: merged 2026-11-07T02:10:19Z
lane_verified: 3819e5bd7a1dcb443c2690cc0884d26f6342cd38
verified: strong
unproven: [perf-typed]
---
# sampo ship reuses the gates' pass when the pushed tree also differs in files tests read (the tower's daily site/data/stats.json on main): it runs only the tests those files affect, not the whole suite
## Raw request
> sampo ship reuses the gates' pass when the pushed tree also differs in files tests read (the tower's daily site/data/stats.json on main): it runs only the tests those files affect, not the whole suite
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] when the pushed tree differs from the gated tree in non-ignored files, sampo ship runs only the affected tests of those files (cli.affected over just them) and reuses the gates' pass when they are green, printing which files and tests; a red affected run or a code file difference still runs the suite — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] affected-only top-up in _gated_pass, test-first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k T3533_or_stats test_ship` → ✗ exit 1 · run.py: no test matches test_ship with -k T3533_or_stats [ran] [tree 2fc4a326448b] [world 2f1906870a] (2026-11-06T22:22:08Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k difference test_ship` → ✗ exit 1 · Ran 3 tests in 1.8s (3 jobs, 16 at a time; slowest: Ship.test_a_stats_only_difference_runs_its_affected_tests_not_the_suite 1s, Ship.test_a_code_difference_still_runs_the_suite 1s, Ship.test_a_red_aff [ran] [tree 2fc4a326448b] [world 2f1906870a] (2026-11-06T22:22:15Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_ship` → exit 0 · Ran 61 tests in 11.7s (53 jobs, 16 at a time; slowest: Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check 5s, Ship.test_a_green_ship_records_the_footprint_and_a_red_one_does_not [ran] [tree ae1dd7c71027] [world 2f1906870a] (2026-11-06T22:23:58Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c2cc226b1a46] (2026-11-07T02:19:35Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 63 tests in 5.5s (55 jobs, 16 at a time; slowest: Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check 3s, Ship.test_a_green_ship_records_the_footprint_and_a_red_one_does_not [ran] [tree c2cc226b1a46] [world 2f1906870a] (2026-11-07T02:19:43Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c2cc226b1a46] (2026-11-07T02:19:43Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c2cc226b1a46] (2026-11-07T02:19:43Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c2cc226b1a46] (2026-11-07T02:19:43Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree c2cc226b1a46] (2026-11-07T02:19:43Z)
## Log
- 2026-11-06T21:52:50Z created
- 2026-11-06T22:16:28Z lane: ~/.claude/foreman.lanes/T-3533 on foreman/T-3533
- 2026-11-06T22:18:27Z focused
- 2026-11-06T22:18:29Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-07T02:10:19Z merged foreman/T-3533 in merge train
- 2026-11-07T02:18:07Z verified: the full suite is green on 9b743b958, which contains 3819e5bd7
- 2026-11-07T02:19:34Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py']
- 2026-11-07T02:19:34Z scope: widened at merge to the reviewed lane's own diff (3819e5bd7), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T02:20:42Z done
- 2026-11-07T02:20:45Z committed 90c9e675f (1 file)
- 2026-11-07T02:20:48Z lane removed: ~/.claude/foreman.lanes/T-3533; dropped: merged and closed
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3439 [FIX S, done, 1 steps] Sampo ship refuses 'origin main moved while testing in files CI tests' when the only… — lesson: A new file the tower publishes must join te…
- T-3468 [PERFORMANCE M, planned, 1 steps] Sampo ship reruns the whole suite (20 min at -j 6) on a tree that differs from the…
- T-2955 [FIX M, done, 2 steps] fm ship can't ship a branch that touched a file fm genesis live keeps publishing to main: the tower's commits make the replay fall back to …
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- similar finished tasks took 1–2 steps
## Measurements
ship test time after a train when main moved only site/data/stats.json: 17-25 min full suite → 103 s (29 test modules, 1,112 tests, at load ~30)
## Lessons
- A reuse check that refuses on any difference should run the tests that difference affects instead.
## Plan gaps
- failed first: step 1 affected-only top-up in _gated_pass, test-first
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/release.py
- plugin/tests/test_ship.py
