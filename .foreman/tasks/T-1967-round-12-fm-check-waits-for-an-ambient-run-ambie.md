---
id: T-1967
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:34:08Z
updated: 2026-10-29T11:01:46Z
batch: [T-1964, T-1965, T-1966]
base: 7983e6c8a45cc3f0fd07722c1ccac31d88d52e95
base_tree: d56126ff7c2577da8c659be4616b0d6bc54b74c9
plan0_at: 2026-10-29T10:52:34Z
plan0_scope: []
verified: strong
---
# round 12: fm check waits for an ambient run, ambient skips during gates, loop round respects pace
## Raw request
> T-1964: FEATURE: a full fm check first waits (at most 5 minutes, saying so) for a running ambient test run on the tree, so two test runs never share the machine and a session doesn't prefix every background gate run with a pgrep wait loop
> DONE-WHEN: fm check with a live ambient run.pid prints that it waits for the ambient run and starts after it ends
> T-1965: FEATURE: the ambient runner starts no run while a full fm check runs on the tree (its gates test everything; the edit's note already says to rerun them), via one shared fmcore gates_live helper the hooks use too
> DONE-WHEN: an edit while gates_running names a live pid on this tree starts no ambient run
> T-1966: FEATURE: fm loop round's step 2 says, while usage runs ahead of pace, to ground the review's ideas in the main thread instead of fm mission and fm ideas, whose lens subagents wait then anyway
> DONE-WHEN: fm loop round with usage ahead of pace prints the main-thread step and no fm ideas line
## Interpretation
Do T-1964, T-1965, T-1966 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1967. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1964: fm check with a live ambient run.pid prints that it waits for the ambient run and starts after it ends — verify with `python3 plugin/tests/run.py test_ambient -k waits`
- [x] T-1965: an edit while gates_running names a live pid on this tree starts no ambient run — verify with `python3 plugin/tests/run.py test_ambient -k during`
- [x] T-1966: fm loop round with usage ahead of pace prints the main-thread step and no fm ideas line — verify with `python3 plugin/tests/run.py test_loop -k pace`
## Non-goals
## Approach (options → choice → why)
T-1964: in _cmd_check before the tree id, a full run polls fmambient.running(p) (renamed from _running) each second up to 300 s, saying so on stderr (--json stays one document). Options: a lock file both take (more code, ambient would need to wait too), or waiting in the drive hook (misses manual runs); chose the poll. T-1965: fmcore.gates_live(p, here=) replaces fmhooks._gates_live; fmambient.after_edit returns early when a full check runs on this tree. T-1966: fmloop._brief swaps step 2 for a main-thread step when fmbudget.degrade(p) names a reason.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1964: A full fm check first waits (at most 5 minutes, saying so) for a running ambient test run
2. [x] T-1965: The ambient runner starts no run while a full fm check runs on the tree (its gates test ev
3. [x] T-1966: Fm loop round's step 2 says, while usage runs ahead of pace, to ground the review's ideas
## Resume here
## Docs impact
MASTER.md (fmambient and forever-loop lines), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ambient test_loop -k waits -k during -k pace` → ✗ exit 1 · Ran 65 tests in 7.1s (46 classes, 16 at a time; slowest: Ambient 7s, Loop 5s, LoopReview 5s) / FAILED (2 classes) [ran] [tree c5c54cfe2cfd] (2026-10-29T10:53:16Z)
- (step 1) `python3 plugin/tests/run.py test_ambient -k waits` → exit 0 · Ran 26 tests in 14.8s (20 classes, 16 at a time; slowest: Ambient 14s, Stop 4s, Watch 3s) / OK [ran] [tree a692235b4508] (2026-10-29T10:54:50Z)
- (step 2) `python3 plugin/tests/run.py test_ambient test_round_f test_drive_side -k during` → exit 0 · Ran 35 tests in 13.7s (13 classes, 16 at a time; slowest: Ambient 13s, RoundF 9s, DriveSide 9s) / OK [ran] [tree a692235b4508] (2026-10-29T10:55:04Z)
- (step 3) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 14 tests in 4.3s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 4s, PipeProgramDebris 0s) / OK [ran] [tree a692235b4508] (2026-10-29T10:55:09Z)
- (step 3) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 14 tests in 4.0s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree c96223ca53cc] (2026-10-29T10:56:08Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmambient.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmloop.py — commit it thro; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.0    41.4     150  [0] / SessionEnd                  35.2    36.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree c96223ca53cc] (2026-10-29T11:00:17Z)
- (ac 1) `python3 plugin/tests/run.py test_ambient -k waits` → exit 0 · Ran 26 tests in 8.4s (20 classes, 16 at a time; slowest: Ambient 8s, Stop 2s, Watch 2s) / OK [ran] [tree c96223ca53cc] (2026-10-29T11:00:50Z)
- (ac 2) `python3 plugin/tests/run.py test_ambient -k during` → exit 0 · Ran 17 tests in 8.1s (11 classes, 16 at a time; slowest: Ambient 8s, Durable 2s, RoundF 1s) / OK [ran] [tree c96223ca53cc] (2026-10-29T11:00:50Z)
- (ac 3) `python3 plugin/tests/run.py test_loop -k pace` → exit 0 · Ran 29 tests in 4.2s (17 classes, 16 at a time; slowest: Loop 4s, LoopReview 4s, Demo 3s) / OK [ran] [tree c96223ca53cc] (2026-10-29T11:00:50Z)
- (audit intent) `self-review of the diff (usage ahead of pace, so no reviewer subagent): wait placed after gates_running is set so edits meanwhile start no ambient run; fmhooks and fmambient share c.gates_live; loop wording fixed to cover the risk-budget reason; full gates 4186 OK` → never two suites at once (fm check waits for ambient, ambient skips during gates) and a paced round drops the ideas fan-out, each proved by its own test [tree c96223ca53cc] (2026-10-29T11:00:50Z)
- (audit edge) `self-review of the diff (usage ahead of pace, so no reviewer subagent): wait placed after gates_running is set so edits meanwhile start no ambient run; fmhooks and fmambient share c.gates_live; loop wording fixed to cover the risk-budget reason; full gates 4186 OK` → a stale run.pid whose pid was reused waits at most 5 minutes; --json keeps stdout one document (the wait note goes to stderr); a gates marker without root (older fm) counts as this tree; a dirty ambient rerun during the wait is capped at 3 [tree c96223ca53cc] (2026-10-29T11:00:50Z)
## Log
- 2026-10-29T10:34:08Z created
- 2026-10-29T10:35:11Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_ambient -k waits`
- 2026-10-29T10:35:12Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_ambient -k during`
- 2026-10-29T10:35:12Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_loop -k pace`
- 2026-10-29T10:52:34Z focused
- 2026-10-29T11:01:44Z done
- 2026-10-29T11:01:46Z committed f9a472e3 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1754 [FEATURE M, done, 3 steps] fm code: a Next: line on every failure, the start event names the Foreman running it, and a registry that stops runners… — lesson: A re…
- decision 2026-10-29: Round 6 runs lean: review ideas only, no fm ideas fan-out
- similar finished tasks took 3–7 steps
## Lessons
- A slowdown reason from fmbudget.degrade can be the risk budget, not usage: word messages around the reason, not around usage pace
## Plan gaps
- failed first: step 1 T-1964: A full fm check first waits (at most 5 minutes, saying so) for a running ambient test run
## Files touched
- plugin/tests/test_ambient.py
- plugin/tests/test_loop.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmambient.py
- plugin/lib/fmcli.py
- plugin/lib/fmloop.py
- CHANGELOG.md
- MASTER.md
