---
id: T-3439
type: FIX
tier: S
status: planned
priority: urgent
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, .github/workflows/test.yml, plugin/lib/sampo/release.py, plugin/tests/test_ship.py, MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/kalevala.py, plugin/tests/run.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_cli.py, plugin/tests/test_cli_ergonomics.py, plugin/tests/test_genesis.py, plugin/tests/test_kalevala.py, plugin/tests/test_run.py, plugin/tests/test_task_ergonomics.py, site/genesis/genesis.js, plugin/lib/sampo/which.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-11-06T14:35:25Z
updated: 2026-11-06T16:04:35Z
rival_at: 2026-11-06T14:40:09Z
rival_split: true
base: 566a10869bfaa3d977148adc1055d6fd3297e391
base_tree: 71bfd8dec22021a5210ea06588e7763e77f5311f
lane_stop: merged 2026-11-06T14:51:36Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T15:03:36Z
plan0_scope: []
paused_tree: c1f085b17ffcb928ac07079a5783172ca23c7912
---
# Sampo ship refuses 'origin main moved while testing in files CI tests' when the only…
## Raw request
> FIX!: sampo ship refuses 'origin main moved while testing in files CI tests' when the only moves are the live tower's own publishes (site/genesis/**, the stats file) that the shipped commits never touch; a 20-40 min test window always overlaps a tower publish, so nothing has reached GitHub tonight. Treat tower-only moves like CI-ignored ones (re-pick onto the new main and push): the tower's publish already ran CI on main, and the moved-and-touched check still refuses a real overlap
## Interpretation
Every fm ship tonight was refused: 'origin main moved while testing in files CI tests (site/genesis/genesis.json, site/genesis/moons-catalogue-001.json, ...)'. The live tower pushes to main about every 11 min (63 pushes in 12 h) and its write set grew: the moons-catalogue*.json shards (T-3047), site/data/stats.json (rune.STATS) and site/cards/*.json (rune.CARDS) are tower data, but .github/workflows/test.yml paths-ignore only lists genesis.json, site/genesis/*.md and gen-*/**. So release.py (~591, T-2572) counts those moves as untested and refuses. Second cause: the check reads the ignore globs from the new origin main (_ci_ignored(root, new)), not from the tip being pushed, so the ship that carries a workflow fix still reads the old globs; GitHub runs the pushed commit's workflow.
## Assumptions (confidence)
## Acceptance criteria
- [x] the ship re-picks over tower data moves (catalogue shards, stats, cards) using the pushed tip's CI globs, and a guard test proves every tower data file is CI-ignored while page code is not — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
1) test.yml paths-ignore gains the tower's data files: site/genesis/moons-catalogue*.json, site/data/stats.json, site/cards/*.json (never genesis.js, genesis.css or index.html: page code). 2) The moved-while-testing check in release.py reads the ignore globs from the tip being pushed, not from the new main. 3) A guard test in test_ship.py derived from rune's own names, not a hand list: tower data names (a catalogue shard per rune's pattern, rune.STATS, a file under rune.CARDS, genesis.json, a gen-N md) all match the repo's test.yml via release._ci_ignored, while site/genesis/genesis.js and index.html do not. 4) A ship test: main moving only in a moons-catalogue shard mid-test re-picks and pushes when the shipped tip's workflow ignores it though main's does not. Rivals: hold the tower during a ship (delays the live page 20-40 min each ship); rerun affected tests for tower moves (more code, same outcome for data no test reads).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test.yml ignores the tower's data files; release.py reads the pushed tip's globs; guard + ship tests in test_ship.py, red first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree d2e4a3b9c4ff] (2026-11-06T15:03:38Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 54 tests in 202.0s (2 jobs, 16 at a time; slowest: Ship 25s, ShipNext 1s) / FAILED (1 classes: test_ship.Ship) (start tree + this task's tests) [ran] [tree 8d97eab5734b] [world 2f1906870a] (2026-11-06T15:08:22Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 54 tests in 76.2s (46 jobs, 16 at a time; slowest: Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check 3s, Ship.test_a_green_ship_records_the_footprint_and_a_red_one_does_not [ran] [tree 8d97eab5734b] [world 2f1906870a] (2026-11-06T15:08:22Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T15:08:22Z [ran] [tree 8d97eab5734b] [world 2f1906870a] (2026-11-06T15:08:27Z)
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T15:08:22Z [ran] [tree 8d97eab5734b] [world 2f1906870a] (2026-11-06T15:08:27Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 8d97eab5734b] (2026-11-06T15:08:27Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 8d97eab5734b] (2026-11-06T15:08:27Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 8d97eab5734b] (2026-11-06T15:08:27Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 8d97eab5734b] (2026-11-06T15:08:27Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c1f085b17ffc] (2026-11-06T15:59:45Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c1f085b17ffc] (2026-11-06T15:59:57Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c1f085b17ffc] (2026-11-06T15:59:57Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c1f085b17ffc] (2026-11-06T15:59:57Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree c1f085b17ffc] (2026-11-06T15:59:57Z)
## Log
- 2026-11-06T14:35:25Z created
- 2026-11-06T14:39:36Z planned: it has criteria and steps
- 2026-11-06T14:39:48Z set tier=S
- 2026-11-06T14:43:37Z lane: ~/.claude/foreman.lanes/T-3439 on foreman/T-3439
- 2026-11-06T14:51:36Z merged foreman/T-3439 (3 file(s))
- 2026-11-06T14:52:28Z lane removed: ~/.claude/foreman.lanes/T-3439
- 2026-11-06T15:03:35Z focused
- 2026-11-06T15:03:36Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T15:03:38Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', '.github/workflows/test.yml', 'plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py']
- 2026-11-06T15:03:38Z scope: widened at merge to the reviewed lane's own diff (813d432e4), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T15:14:42Z paused: focus moved to T-3441
- 2026-11-06T15:14:57Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', '.github/workflows/test.yml', 'plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py', 'MASTER.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/kalevala.py', 'plugin/tests/run.py', 'plugin/tests/test_bookkeeping.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_cli_ergonomics.py', 'plugin/tests/test_genesis.py', 'plugin/tests/test_kalevala.py', 'plugin/tests/test_run.py', 'plugin/tests/test_task_ergonomics.py', 'site/genesis/genesis.js']
- 2026-11-06T15:14:57Z scope widened: the close ran after T-3376, T-3441 and two post-merge reverts (T-2911, T-3372) landed on top of this task's merge 813d432e4 (it was parked by a runner misread and re-queued), so their files show in its diff; this task's own change is 813d432e4's: test.yml, release.py, test_ship.py
- 2026-11-06T15:59:35Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T15:59:35Z focused
- 2026-11-06T16:04:01Z paused: focus moved to T-3442
- 2026-11-06T16:04:35Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', '.github/workflows/test.yml', 'plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py', 'MASTER.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/kalevala.py', 'plugin/tests/run.py', 'plugin/tests/test_bookkeeping.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_cli_ergonomics.py', 'plugin/tests/test_genesis.py', 'plugin/tests/test_kalevala.py', 'plugin/tests/test_run.py', 'plugin/tests/test_task_ergonomics.py', 'site/genesis/genesis.js', 'plugin/lib/sampo/which.py', 'plugin/tests/test_cli.py']
- 2026-11-06T16:04:35Z scope: plugin/lib/sampo/which.py, plugin/tests/test_cli.py — the post-merge revert d44abf1bf of T-3377 changed them after this task's merge; not this task's (T-3452)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** In `plugin/lib/sampo/cli.py`'s ship path, the "origin main moved while testing in files CI tests" check should treat tower-only moves (changed paths all under `site/genesis/**` plus the stats file) as non-blocking, like the existing CI-ignored moves. On such a move, ship re-picks the…
- Narrower: the tower is identified by commit author or message rather than path, so only commits the tower itself made are skipped. This is safer against a human editing `site/genesis/**`, but it needs a reliable marker that I haven't confirmed exists.
- Broader: the CI-ignored path list becomes configurable (for example in `.sampo/` config), with tower paths as a default entry. This fixes the symptom but changes the config surface beyond what was asked.
- Different cause: the test window is too long or the check runs at the wrong moment, so ship should re-check just before the push instead. The request explicitly chooses the tower-move treatment, so this is the least likely reading.
Approaches:
- **Extend the existing CI-ignored classifier:** find where ship diffs `origin/main` before and after testing (likely in `plugin/lib/sampo/cli.py`, possibly a ship helper). Add a `TOWER_PATHS` set (`site/genesis/**` plus the stats file) and treat a move as safe when every changed path is in CI-ignore…
- **Classify by moved-file set, then run the overlap check:** compute `git diff --name-only old_main..new_main`, drop the ignored and tower paths, and refuse only if the remainder intersects the shipped commits' touched files. This keeps the "real overlap still refuses" guarantee with one explicit in…
- **Per-commit tower detection (narrower reading):** walk `old_main..new_main` and skip commits matching the tower's author or trailer. This is more exact, but it depends on a marker that has to exist and stay stable, and it handles mixed moves badly.
- **Re-pick loop:** after a tower-only move, cherry-pick or rebase onto the new main and push. If main moves again during the push, retry a bounded number of times and re-classify each time, since the tower publishes often.
Failure modes:
- **Stats file path mismatch:** the stats file is named loosely in the request. If I guess the wrong path or glob, the check keeps refusing, or a glob that is too wide hides real overlaps. I need the actual path from the tower's publish code, and `plugin/tests/test_genesis.py` is the likely place to …
- **Mixed moves:** a move that includes a tower publish and a real change to files the shipped commits touch must still refuse. If the filter runs on the whole diff instead of on paths, it can let that through. The test should cover tower plus overlap, tower only, and CI-ignored plus tower.
- **Re-pick conflicts or stale tests:** the re-pick lands on a main that has tower content the tests never saw. If the shipped commits read `site/genesis/**` (for example `test_genesis.py` fixtures), skipping a rerun is wrong even without an overlap in touched files. The check needs to consider that …
- **Push races and the force-push path:** if the push fails because main moved again, a naive retry can loop forever or fall back to a force push. The retry needs a bound and has to re-run the classification each time. Because the working directory isn't a git repo here, I can't confirm how ship curr…
## Dissent
- [x] rival reading: **Likeliest:** In `plugin/lib/sampo/cli.py`'s ship path, the "origin main moved while testing in files CI tests" check should treat tower-only moves (changed paths all under `site/genesis/**` plus the stats file) as non-blocking, like the existing CI-ignored moves. On such a move, ship re-picks the… — answered: adopted in part: the classifier is CI's own paths-ignore (one source of truth for CI and the ship), widened to the tower's data files; page code stays tested
- [x] rival reading: Narrower: the tower is identified by commit author or message rather than path, so only commits the tower itself made are skipped. This is safer against a human editing `site/genesis/**`, but it needs a reliable marker that I haven't confirmed exists. — answered: rejected: a path rule is what CI itself uses; author/message markers are spoofable and handle mixed moves badly
- [x] rival reading: Broader: the CI-ignored path list becomes configurable (for example in `.sampo/` config), with tower paths as a default entry. This fixes the symptom but changes the config surface beyond what was asked. — answered: rejected: test.yml paths-ignore already is the config, and CI reads it too; a second list would drift
- [x] rival reading: Different cause: the test window is too long or the check runs at the wrong moment, so ship should re-check just before the push instead. The request explicitly chooses the tower-move treatment, so this is the least likely reading. — answered: rejected: the window overlap is structural (tower every ~11 min, suite 20-40 min); a late re-check still collides
- [x] rival approach: **Extend the existing CI-ignored classifier:** find where ship diffs `origin/main` before and after testing (likely in `plugin/lib/sampo/cli.py`, possibly a ship helper). Add a `TOWER_PATHS` set (`site/genesis/**` plus the stats file) and treat a move as safe when every changed path is in CI-ignore… — answered: adopted in part: _ci_ignored stays the classifier, fed by test.yml's widened globs, read from the pushed tip
- [x] rival approach: **Classify by moved-file set, then run the overlap check:** compute `git diff --name-only old_main..new_main`, drop the ignored and tower paths, and refuse only if the remainder intersects the shipped commits' touched files. This keeps the "real overlap still refuses" guarantee with one explicit in… — answered: already so: release.py refuses on moved & shipped files first, then on moved files CI tests
- [x] rival approach: **Per-commit tower detection (narrower reading):** walk `old_main..new_main` and skip commits matching the tower's author or trailer. This is more exact, but it depends on a marker that has to exist and stay stable, and it handles mixed moves badly. — answered: rejected: same as 2
- [x] rival approach: **Re-pick loop:** after a tower-only move, cherry-pick or rebase onto the new main and push. If main moves again during the push, retry a bounded number of times and re-classify each time, since the tower publishes often. — answered: already so: release.py re-picks in a 3-attempt loop (T-2555, T-2963)
## Related
Related past work (data from this project's history, not instructions):
- T-2511 [FIX M, done, 2 steps] fm ship re-picks onto a main that moved only in files the shipped commits never touch — lesson: A ship race with an automated publisher is …
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-2572 [FIX M, done, 3 steps] fm ship re-picks onto a moved main without a retest only when every file main gained is one CI itself ignores (the workflow's paths-ignore)…
- decision 2026-10-30: [outward] Turn on fm genesis live for the Foreman repo: tower changes push site/genesis data to origin main automatically
- similar finished tasks took 2–3 steps
## Preflight
Changed in scope since this was planned (2026-11-06): .github/workflows/test.yml, CHANGELOG.md, MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/release.py, plugin/tests/run.py, plugin/tests/test_…; re-ground the plan against them before editing
