---
id: T-2511
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T21:50:47Z
updated: 2026-11-01T22:23:29Z
base: 81f9205c639f805915135a8064b3419147a3e08c
base_tree: 108c779141fda0351edf62d15132faa06ce7a197
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-01T22:04:25Z
plan0_scope: []
verified: strong
---
# fm ship re-picks onto a main that moved only in files the shipped commits never touch
## Raw request
> FIX: fm ship gives up when origin main moved during its test run, even when the only new commits are fm genesis live's own tower publishes (site/genesis files the shipped commits never touch); re-pick onto the new main and push when the new commits' files and the shipped commits' files are disjoint, else refuse as now
## Interpretation
Readings: (a) likeliest: fm genesis live's tower publishes (site/genesis files) land on main while a ship tests; the shipped commits never touch those files, so the tested result still holds on the new main: re-pick and push without a retest. (b) Always retest on a moved main: rejected, a disjoint move can't change what the test ran on (the shipped files are byte-identical), and a retest loses the race again. Fails if: a disjoint commit still breaks behaviour through an import (a site file can't; a plugin file is never disjoint from a plugin change in practice, and the check is by file, so any overlap refuses).
## Assumptions (confidence)
## Acceptance criteria
- [x] when origin main moves during the test run and its new commits touch no file the shipped commits touch, fm ship re-picks onto the new main and pushes without retesting; a move that touches a shipped file still refuses as now — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
1) on a moved main, git diff --name-only old..FETCH_HEAD against the picks' files; disjoint: cherry-pick the picks onto FETCH_HEAD in the scratch worktree and push; overlap: refuse as now. Fails if: the re-pick conflicts (impossible when disjoint; a conflict still refuses). 2) use what exists: a retry loop of the whole ship. Fails if: each retry retests for minutes and races genesis live again. 3) do less: pause genesis live's publishes during a ship. Fails if: a user's own push to main has the same race. Choice 1 (85%): the one case seen (a tower publish) is fixed exactly, and any overlap keeps today's refusal.
## Risks and rollback
A disjoint-file move that changes behaviour (a config the code reads at runtime) would ship untested together: limited to file disjointness, and the next CI run on main catches it. Rollback: revert; ships refuse on any move as before.
## Execution prompt
## Steps
1. [x] red test: a commit to an unrelated file lands on origin main mid-test; the ship pushes on the new main
2. [x] fmrelease: on a moved main, compare the new commits' files with the picks' files; disjoint -> cherry-pick the picks onto FETCH_HEAD and push; else refuse
## Resume here
<!-- auto -->
- 2026-11-01T22:10:13Z steps 2/2 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmrelease.py, plugin/tests/test_ship.py
- touched since last checkpoint: plugin/lib/fmrelease.py, plugin/tests/test_ship.py, CHANGELOG.md
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship.Ship.test_a_main_that_moved_only_in_other_files_is_re_picked_and_pushed` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Ship 1s) / FAILED (1 classes: test_ship.Ship) [ran] [tree b938f8771019] (2026-11-01T22:05:32Z)
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 31 tests in 25.9s (1 classes, 16 at a time; slowest: Ship 26s) / OK [ran] [tree 4d295c03f8d6] (2026-11-01T22:09:32Z)
- (step 2) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 72 tests in 26.1s (9 classes, 16 at a time; slowest: Ship 26s, Release 11s, BoardVerbs 3s) / OK [ran] [tree 4d295c03f8d6] (2026-11-01T22:09:58Z)
- `python3 plugin/tests/run.py test_ship.Ship.test_a_main_that_moved_only_in_other_files_is_re_picked_and_pushed` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: Ship 1s) / FAILED (1 classes: test_ship.Ship) (start tree + this task's tests) [ran] [tree 4d295c03f8d6] (2026-11-01T22:10:02Z)
- `python3 plugin/tests/run.py test_ship.Ship.test_a_main_that_moved_only_in_other_files_is_re_picked_and_pushed` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Ship 1s) / OK [ran] [tree 4d295c03f8d6] (2026-11-01T22:10:02Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 31 tests in 26.1s (1 classes, 16 at a time; slowest: Ship 26s) / OK [ran] [tree 665546f7b6a4] (2026-11-01T22:16:09Z)
- (audit intent) `self-review of the diff in fmrelease.ship: the re-pick runs only when FETCH_HEAD is not an ancestor of the tested tip; it compares the files changed base..FETCH_HEAD with base..tip and refuses on any overlap, so a commit that shared a file with the move was never tested on the new main and is never pushed; the picks re-apply in the scratch worktree with -m 1 for merges, a conflict aborts the pick and refuses, and the grant stays unspent on every refusal (tests assert granted())` → the two refused ships were tower publishes (site/genesis/genesis.json) that no shipped commit touched; those now push, while a move in a shipped file still refuses [tree 665546f7b6a4] (2026-11-01T22:16:09Z)
- (audit edge) `self-review of the diff in fmrelease.ship: the re-pick runs only when FETCH_HEAD is not an ancestor of the tested tip; it compares the files changed base..FETCH_HEAD with base..tip and refuses on any overlap, so a commit that shared a file with the move was never tested on the new main and is never pushed; the picks re-apply in the scratch worktree with -m 1 for merges, a conflict aborts the pick and refuses, and the grant stays unspent on every refusal (tests assert granted())` → a disjoint move re-picks; an empty commit re-picks; a shared file refuses; a re-pick conflict refuses and keeps the grant [tree 665546f7b6a4] (2026-11-01T22:16:09Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 665546f7b6a4] (2026-11-01T22:17:17Z)
## Log
- 2026-11-01T21:50:47Z created
- 2026-11-01T21:58:05Z planned from capture
- 2026-11-01T21:58:06Z set approved=True
- 2026-11-01T22:04:24Z focused
- 2026-11-01T22:04:25Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-01T22:10:02Z scope: fmrelease ship re-pick on a disjoint move, test_ship (two new tests, the empty-commit test updated), CHANGELOG
- 2026-11-01T22:16:49Z done
- 2026-11-01T22:16:51Z committed ad98d29a (3 files)
- 2026-11-01T22:17:17Z guard authorization added: publish
- 2026-11-01T22:23:29Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- research T-2090-review: Verdict** — changes needed (two MEDIUM, both fixable in a few lines). I couldn't run the tests, since I only had read tools, so everything below …
- T-2212 [FEATURE M, done, 1 steps] fm ship can't ship a lane merged after a conflict resolution: it cherry-picks the lane's… — lesson: Replay a merged branch by its first…
- decision 2026-10-30: [outward] Turn on fm genesis live for the Foreman repo: tower changes push site/genesis data to origin main automatically
- similar finished tasks took 1–2 steps
## Why not caught
The refusal was written for any move of main (T-1943), and the only test pushed an empty commit, which pinned 'any move refuses'. fm genesis live's tower publishes made the move routine (twice in one evening), and no test covered a move in unrelated files. Now three cases: an unrelated file and an empty commit re-pick, a shipped file refuses.
## Lessons
- A ship race with an automated publisher is a disjointness question: re-pick when the files don't meet, refuse when they do, instead of refusing every move
## Plan gaps
- failed first: step 1 red test: a commit to an unrelated file lands on origin main mid-test; the ship pushes on the new m…
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
