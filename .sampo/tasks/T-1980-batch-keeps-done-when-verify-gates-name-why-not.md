---
id: T-1980
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T12:10:05Z
updated: 2026-10-29T12:25:21Z
batch: [T-1976, T-1977, T-1978, T-1979]
base: 24df129229f1db89aa08f156627689bc6b9f149f
base_tree: 3d1eb91bb1e9877bb416253c92115a94b99f10e4
plan0_at: 2026-10-29T12:10:21Z
plan0_scope: []
verified: strong
---
# Batch keeps DONE-WHEN verify, gates name why-not-caught, fm ship marks its test run, first_touch keeps project files
## Raw request
> T-1976: FIX: fm batch drops a member's verify command when its criteria come from the DONE-WHEN fallback: "x :: cmd" stays in the text with no verify, so fm focus on the batch is refused until each criterion is re-edited (T-1974 needed three fm task ac edits). _make_batch splits the fallback with rpartition(" :: ") as the other DONE-WHEN readers do (fmcli _make_batch).
> DONE-WHEN: a batch of intake tasks whose criteria live only in DONE-WHEN lines keeps their verify commands and focuses at once :: python3 plugin/tests/run.py test_batch
> T-1977: FIX: fm gates and fm focus's "Done needs" line leave out why-not-caught for an M or L FIX, yet fm task finish refuses without it, so the close is refused once before it passes (fmcli gates()).
> DONE-WHEN: fm gates fix m names why-not-caught and an S fix does not :: python3 plugin/tests/run.py test_speed
> T-1978: FIX: fm ship's test suite runs in its scratch tree with no marker, so a full fm check started meanwhile runs a second suite beside it (the T-1964/T-1971 rule covers only this tree), and a ship started during a full check does the same. fm ship marks its test run (meta ship_testing: pid, scratch root) and waits for a live full check or ambient run here first; a full fm check on another tree waits for a live ship test run (at most 10 minutes, saying so). The ship's own fm check in its scratch tree does not wait for itself (fmrelease ship, fmcli _cmd_check).
> DONE-WHEN: a full fm check started during fm ship's test run waits for it and says so; the ship marks and clears its run :: python3 plugin/tests/run.py test_ship test_ambient
> T-1979: FIX: c.first_touch counts a Write outside the project (a scratchpad file) as the task's first edit, unlike task_touches, so a CLEAN ship task that edited no repo file was refused for a missing behaviour lock (T-1975). first_touch keeps only project files, as task_touches does (fmcore first_touch).
> DONE-WHEN: a CLEAN task whose only edit is outside the project closes without a behaviour lock :: python3 plugin/tests/run.py test_close_gates
## Interpretation
Four fixes from round 14: fm batch keeps a member's DONE-WHEN verify command; fm gates names why-not-caught for an M/L FIX; fm ship marks its scratch-tree test run so a full fm check waits for it (and ship waits for a live check here); first_touch counts only project files.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1976: a batch of intake tasks whose criteria live only in DONE-WHEN lines keeps their verify commands and focuses at once — verify with `python3 plugin/tests/run.py test_batch`
- [x] T-1977: fm gates fix m names why-not-caught and an S fix does not — verify with `python3 plugin/tests/run.py test_speed`
- [x] T-1978: a full fm check started during fm ship's test run waits for it and says so; the ship marks and clears its run — verify with `python3 plugin/tests/run.py test_ship test_ambient`
- [x] T-1979: a CLEAN task whose only edit is outside the project closes without a behaviour lock — verify with `python3 plugin/tests/run.py test_verify_strength`
## Non-goals
## Approach (options → choice → why)
(a) split DONE-WHEN with partition(' :: ') in _make_batch vs a shared helper → inline partition (one reader). (b) gates() adds why-not-caught for FIX M/L. (c) options: reuse gates_running for ship (clashes with the owner check and here= semantics) / a ship lock file / a meta ship_testing key read through gates_live(key=) → meta key, cleared only by its owner; the ship's own fm check in the scratch tree (p.root == its root) never waits for it. (d) first_touch filters to p.root like task_touches.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1976: Fm batch drops a member's verify command when its criteria come from the DONE-WHEN fallbac
2. [x] T-1977: Fm gates and fm focus's "Done needs" line leave out why-not-caught for an M or L FIX, yet
3. [x] T-1978: Fm ship's test suite runs in its scratch tree with no marker, so a full fm check started m
4. [x] T-1979: C.first_touch counts a Write outside the project (a scratchpad file) as the task's first e
## Resume here
<!-- auto -->
- 2026-10-29T12:18:19Z step 2/4: T-1977: Fm gates and fm focus's "Done needs" line leave out why-not-caught for an M or L FIX, yet
- git: foreman/build; 10 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmrelease.py, plugin/tests/test_ambient.py, plugin/tests/test_batch.py, plugin/tests/test_ship.py, plugin/tests/test_speed.py, plugin/tests/test_verify_strength.py
- touched since last checkpoint: plugin/tests/test_batch.py, plugin/tests/test_speed.py, plugin/tests/test_ambient.py, plugin/tests/test_verify_strength.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmrelease.py, CHANGELOG.md, MASTER.md, plugin/tests/test_ship.py
## Docs impact
CHANGELOG Unreleased line (T-1980); MASTER.md fm ship entry names the ship_testing marker and the wait both ways (T-1978). fm gates text itself documents why-not-caught for M/L FIX.
## Verification evidence
- `python3 plugin/tests/run.py test_batch test_speed test_ambient test_ship test_verify_strength` → ✗ exit 1 · Ran 87 tests in 16.0s (12 classes, 16 at a time; slowest: VerifyStrength 15s, Ambient 13s, Ship 10s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree 05e8f04c743e] (2026-10-29T12:11:55Z)
- `python3 plugin/tests/run.py test_batch test_speed test_ambient test_ship test_verify_strength` → ✗ exit 1 · Ran 87 tests in 15.2s (12 classes, 16 at a time; slowest: VerifyStrength 15s, Ambient 13s, Ship 10s) / FAILED (5 classes) [ran] [tree 05e8f04c743e] (2026-10-29T12:11:55Z)
- (step 1) `python3 plugin/tests/run.py test_batch test_speed test_ambient test_ship test_verify_strength 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)" | head -12` → exit 0 · Ran 87 tests in 22.0s (12 classes, 16 at a time; slowest: VerifyStrength 22s, Ambient 21s, Ship 20s) / OK [ran] [tree 5c8eddace213] (2026-10-29T12:12:49Z)
- `python3 plugin/tests/run.py test_batch test_speed test_ambient test_ship test_verify_strength` → ✗ exit 1 · Ran 87 tests in 16.1s (12 classes, 16 at a time; slowest: VerifyStrength 15s, Ambient 13s, Ship 11s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree 5c8eddace213] (2026-10-29T12:13:25Z)
- `python3 plugin/tests/run.py test_batch test_speed test_ambient test_ship test_verify_strength` → exit 0 · Ran 87 tests in 15.4s (12 classes, 16 at a time; slowest: Ambient 15s, VerifyStrength 15s, Ship 12s) / OK [ran] [tree 5c8eddace213] (2026-10-29T12:13:25Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmrelease.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.8    43.1     150  [0] / SessionEnd                  35.2    37.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 63a932e6cbdc] (2026-10-29T12:17:50Z)
- (step 2) `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 3.4s (1 classes, 16 at a time; slowest: Speed 3s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:19:33Z)
- (step 3) `python3 plugin/tests/run.py test_ambient test_ship` → exit 0 · Ran 24 tests in 14.8s (2 classes, 16 at a time; slowest: Ambient 15s, Ship 12s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:19:48Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 18 tests in 15.3s (2 classes, 16 at a time; slowest: VerifyStrength 15s, Repeat 8s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:20:04Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmrelease.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 12:17 UTC; claude plugin test [ran] [tree 05fc7fc5627e] (2026-10-29T12:23:53Z)
- (ac 1) `python3 plugin/tests/run.py test_batch` → exit 0 · Ran 36 tests in 9.9s (7 classes, 16 at a time; slowest: BatchEdit 10s, Batch 6s, Related 3s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
- (ac 2) `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 3.4s (1 classes, 16 at a time; slowest: Speed 3s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
- (ac 3) `python3 plugin/tests/run.py test_ship test_ambient` → exit 0 · Ran 24 tests in 14.8s (2 classes, 16 at a time; slowest: Ambient 15s, Ship 12s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
- (ac 4) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 18 tests in 15.2s (2 classes, 16 at a time; slowest: VerifyStrength 15s, Repeat 8s) / OK [ran] [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
- (audit intent) `self-review (optional work dropped): inner ship check has p.root == realpath(wt) == marker root so it never waits; finally clears the marker only when it's ours; first_touch filters by project root prefix like task_touches` → all four round-14 fixes land with a red-then-green test each [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
- (audit edge) `self-review (optional work dropped): inner ship check has p.root == realpath(wt) == marker root so it never waits; finally clears the marker only when it's ours; first_touch filters by project root prefix like task_touches` → the ship's own fm check doesn't wait on its marker (e2e test with default fm check) [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
- (audit adversary) `self-review (optional work dropped): inner ship check has p.root == realpath(wt) == marker root so it never waits; finally clears the marker only when it's ours; first_touch filters by project root prefix like task_touches` → a stale ship_testing marker is dropped once its pid dies; worst case a 10-minute wait [tree 05fc7fc5627e] (2026-10-29T12:24:50Z)
## Log
- 2026-10-29T12:10:05Z created
- 2026-10-29T12:10:13Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_batch`
- 2026-10-29T12:10:13Z criterion 1 text: T-1976: a batch of intake tasks whose criteria live only in DONE-WHEN lines keeps their verify commands and focuses at once :: python3 plugin/tests/run.py test_batch → T-1976: a batch of intake tasks whose criteria live only in DONE-WHEN lines keeps their verify commands and focuses at once
- 2026-10-29T12:10:13Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_speed`
- 2026-10-29T12:10:13Z criterion 2 text: T-1977: fm gates fix m names why-not-caught and an S fix does not :: python3 plugin/tests/run.py test_speed → T-1977: fm gates fix m names why-not-caught and an S fix does not
- 2026-10-29T12:10:14Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_ship test_ambient`
- 2026-10-29T12:10:14Z criterion 3 text: T-1978: a full fm check started during fm ship's test run waits for it and says so; the ship marks and clears its run :: python3 plugin/tests/run.py test_ship test_ambient → T-1978: a full fm check started during fm ship's test run waits for it and says so; the ship marks and clears its run
- 2026-10-29T12:10:14Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_close_gates`
- 2026-10-29T12:10:14Z criterion 4 text: T-1979: a CLEAN task whose only edit is outside the project closes without a behaviour lock :: python3 plugin/tests/run.py test_close_gates → T-1979: a CLEAN task whose only edit is outside the project closes without a behaviour lock
- 2026-10-29T12:10:21Z focused
- 2026-10-29T12:10:58Z criterion 4 verify: `python3 plugin/tests/run.py test_close_gates` → `python3 plugin/tests/run.py test_verify_strength`
- 2026-10-29T12:25:19Z done
- 2026-10-29T12:25:21Z committed a3597781 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1974 [FIX M, done, 3 steps] round 13: one full check per tree, fm risk shows what spent it, ambient after mid-gate edits — lesson: A shared marker written by one proce…
- T-1971 [FIX M, done, 0 steps] A second full fm check started while another runs on the same tree overwrites its gates_ru
- T-1967 [FEATURE M, done, 3 steps] round 12: fm check waits for an ambient run, ambient skips during gates, loop round respects pace — lesson: A slowdown reason from fmbu…
- decision 2026-10-23: Gates behind volt's 2-hour cargo test lock: stop our own queued fm check runs and land the drafted tasks first, then one gate covers all of them bef…
- similar finished tasks took 0–3 steps
## Why not caught
none: each was a gap no test named — batch criteria, gates text, overlapping ship/check suites and scratchpad first-touch had no coverage until now
## Lessons
- A marker that one process waits on needs an owner key (root) so the marker's own child process doesn't wait on itself
## Files touched
- plugin/tests/test_batch.py
- plugin/tests/test_speed.py
- plugin/tests/test_ambient.py
- plugin/tests/test_ship.py
- plugin/tests/test_verify_strength.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
