---
id: T-2527
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrelease.py, plugin/lib/fmcli.py, plugin/lib/fmci.py, plugin/tests/test_ship.py, plugin/tests/test_ci_watch.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T03:11:41Z
updated: 2026-11-02T03:41:38Z
base: 18101f0e33b9a7ce4da98ae3f39850afee9f43b6
base_tree: 34498c9db3fde869b1b1e3009a7f55d77afeacc0
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T03:26:52Z
plan0_scope: [plugin/lib/fmrelease.py, plugin/lib/fmcli.py, plugin/lib/fmci.py, plugin/tests/test_ship.py, plugin/tests/test_ci_watch.py, CHANGELOG.md]
verified: strong
---
# fm ci-watch --last-ship watches the main commit the newest fm ship pushed
## Raw request
> fm ci-watch --last-ship: watch the commit the newest fm ship pushed (read from its ship event), so nobody types a SHA from memory; this session started ci-watch on a mistyped SHA twice (T-2504's watch, ship135's)
## Interpretation
After fm ship, the session must watch CI on the commit main now holds, without copying a sha by hand or extracting it from the ship output (both failed this session: a typed sha, then an empty extraction that silently watched the build branch's HEAD).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship records the pushed main tip in refs/foreman/shipped-tip and fm ci-watch --last-ship watches it; with none recorded it refuses with a usage error — verify with `python3 plugin/tests/run.py test_ci_watch test_ship`
- [x] fm ci-watch --commit with an empty value refuses instead of silently watching HEAD — verify with `python3 plugin/tests/run.py test_ci_watch`
## Non-goals
## Approach (options → choice → why)
1. A ref refs/foreman/shipped-tip moved to the pushed tip, read by --last-ship (git-native, survives sessions, one line each side). 2. use what exists: refs/foreman/shipped already exists, but it holds the branch pick, not the re-picked main sha, so CI never runs on it. 3. A ship ledger event read back by --last-ship (needs a ledger scan and a new event type). 4. do less: only refuse an empty --commit and keep extracting the sha from ship's output. Choice 1 (85%): the ref sits beside SHIPPED and fails loudly when absent; 4 is also taken, as the guard on --commit.
## Risks and rollback
A failed update-ref leaves the previous tip; ship prints a warning naming it, and the watch names the sha it watches. Rollback: revert the commit; the ref is inert.
## Execution prompt
## Steps
1. [x] red test: ci-watch --last-ship resolves refs/foreman/shipped-tip, refuses when absent; ship moves the ref to the tip
2. [x] fmrelease moves refs/foreman/shipped-tip to tip after the push; fmci/fmcli --last-ship reads it
## Resume here
## Docs impact
CHANGELOG; fm ci-watch --help names --last-ship
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ci_watch.CiWatch.test_last_ship_watches_the_shipped_tip_and_an_empty_commit_refuses test_ship.Ship.test_ships_the_unpushed_commits_after_the_test_and_spends_the_grant` → ✗ exit 1 · Ran 2 tests in 1.0s (2 classes, 16 at a time; slowest: Ship 1s, CiWatch 0s) / FAILED (2 classes: test_ci_watch.CiWatch, test_ship.Ship) [ran] [tree e961983a291c] [world 2f1906870a] (2026-11-02T03:27:06Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch test_ship` → exit 0 · Ran 48 tests in 26.3s (3 classes, 16 at a time; slowest: Ship 26s, CiWatch 3s, CiCause 0s) / OK [ran] [tree 3198e990404a] [world 2f1906870a] (2026-11-02T03:28:30Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch test_ship` → exit 0 · Ran 48 tests in 25.8s (3 classes, 16 at a time; slowest: Ship 26s, CiWatch 3s, CiCause 0s) / OK [ran] [tree bdb63e6c4453] [world 2f1906870a] (2026-11-02T03:40:27Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 17 tests in 2.9s (2 classes, 16 at a time; slowest: CiWatch 3s, CiCause 0s) / OK [ran] [tree bdb63e6c4453] [world 2f1906870a] (2026-11-02T03:40:27Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch.CiWatch.test_last_ship_watches_the_shipped_tip_and_an_empty_commit_refuses test_ship.Ship.test_ships_the_unpushed_commits_after_the_test_and_spends_the_grant` → exit 0 · Ran 2 tests in 1.0s (2 classes, 16 at a time; slowest: Ship 1s, CiWatch 0s) / OK [ran] [tree bdb63e6c4453] [world 2f1906870a] (2026-11-02T03:40:27Z)
- (audit intent) `self-review of the diff: ref written beside SHIPPED with a warning on failure; ci-watch refuses an empty --commit before any lookup; --last-ship and --commit are mutually exclusive` → after fm ship the session watches the commit main holds with no sha copied or extracted by hand, which is what failed twice this session [tree bdb63e6c4453] (2026-11-02T03:40:27Z)
- (audit edge) `self-review of the diff: ref written beside SHIPPED with a warning on failure; ci-watch refuses an empty --commit before any lookup; --last-ship and --commit are mutually exclusive` → no ship recorded refuses naming fm ship; a whitespace-only --commit refuses; a failed update-ref warns and leaves the older tip, and the watch line names the sha it watches [tree bdb63e6c4453] (2026-11-02T03:40:27Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree bdb63e6c4453] [world 2f1906870a] (2026-11-02T03:41:38Z)
## Log
- 2026-11-02T03:11:41Z created
- 2026-11-02T03:18:31Z planned from capture
- 2026-11-02T03:26:51Z focused
- 2026-11-02T03:26:52Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T03:28:43Z scope: fmrelease writes refs/foreman/shipped-tip after the push (picks differ from tip once re-picked, so SHIPPED can't serve); fmci reads it for --last-ship and refuses an empty --commit; fmcli adds the flag in a group with --commit
- 2026-11-02T03:29:43Z set tier=M
- 2026-11-02T03:29:45Z set approved=True
- 2026-11-02T03:41:11Z done
- 2026-11-02T03:41:13Z committed f3548456 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1948 [FEATURE S, done, 3 steps] fm ship remembers what it shipped and can watch CI
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- T-2058 [FIX S, done, 1 steps] fm ship --watch / ci-watch says CI green from the first workflow run of a commit (pages)… — lesson: A commit has one run per workflow: CI i…
- decision 2026-10-30: [revisited: feel free to push to main] [cites: user steer 2026-10-29: push to main without asking] [check: python3 plugin/tests/run.py test_ship.Shi…
- similar finished tasks took 1–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_release.py
## Why not caught
ci-watch treated --commit '' as unset (a falsy test), so a failed $(grep) extraction silently watched the build branch's HEAD; nothing recorded the pushed main tip outside ship's printed line.
## Lessons
- a falsy test on an optional CLI value turns a failed shell extraction into the default target silently; refuse empty values explicitly
## Plan gaps
- failed first: step 1 red test: ci-watch --last-ship resolves refs/foreman/shipped-tip, refuses when absent; ship moves t…
## Files touched
- plugin/tests/test_ship.py
- plugin/tests/test_ci_watch.py
- plugin/lib/fmrelease.py
- plugin/lib/fmci.py
- plugin/lib/fmcli.py
- CHANGELOG.md
