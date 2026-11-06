---
id: T-2656
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:37:18Z
base: f4485da5aa235878630c5b68642f1affbeb73d58
base_tree: 65a94bceb2c312cd7b6a62a285dcfc6d2c857293
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:34:59Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# A capture that near-duplicates a deferred task of its type wakes it: the words are logged on it and its revisit is set to today, so fm next names it due back, instead of a near-duplicate refusal
## Raw request
> FEATURE: Wake a deferred task when new evidence matches its brief (c23: Triage and wake-up of deferred and inbox work; value 3, effort M, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm capture of words matching a deferred task logs them on it, makes it due back today and creates no new task; an open (not deferred) match is still refused as a near-duplicate — verify with `python3 plugin/tests/run.py test_wake_deferred`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the wake in fmcli._near
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_wake_deferred test_backlog` → exit 0 · Ran 25 tests in 7.8s (5 classes, 16 at a time; slowest: Extras 7s, Reverify 7s, Capture 5s) / OK [ran] [tree 0f76a45f938e] [world 2f1906870a] (2026-11-02T20:36:02Z)
- (step 2) `python3 plugin/tests/run.py test_wake_deferred test_backlog` → exit 0 · Ran 25 tests in 9.0s (5 classes, 16 at a time; slowest: Extras 9s, Reverify 8s, Capture 5s) / OK [ran] [tree 0f76a45f938e] [world 2f1906870a] (2026-11-02T20:36:12Z)
- (step 3) `grep -q 'wakes that task' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 0f76a45f938e] [world 2f1906870a] (2026-11-02T20:36:12Z)
- (ac 1) `python3 plugin/tests/run.py test_wake_deferred` → exit 0 · Ran 2 tests in 2.2s (1 classes, 16 at a time; slowest: WakeDeferred 2s) / OK [ran] [tree 0f76a45f938e] [world 2f1906870a] (2026-11-02T20:36:17Z)
- (audit edge) `self: the wake reuses the deferral's own due mechanism (revisit set to today), so fm next and every reader of due deferrals pick it up unchanged; --anyway still makes a new task; an open match is still refused (tested)` → a deferred task of another type isn't woken (near_tasks' same is type-matched); the capture's text is logged through c.plain and fit to 200 chars [tree 0f76a45f938e] (2026-11-02T20:36:17Z)
- (audit self) `self: the wake reuses the deferral's own due mechanism (revisit set to today), so fm next and every reader of due deferrals pick it up unchanged; --anyway still makes a new task; an open match is still refused (tested)` → no findings [tree 0f76a45f938e] (2026-11-02T20:36:17Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:34:57Z planned from capture
- 2026-11-02T20:34:58Z focused
- 2026-11-02T20:34:59Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:37:16Z done
- 2026-11-02T20:37:18Z committed b2f5906c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2649 [FEATURE M, dropped, 0 steps] fm doctor row: list deciders with no sample size or an abstain rate near 100% (c16:…
- T-2653 [FEATURE S, done, 3 steps] Every nonzero fm exit prints one Next: command, not only a UsageError that carries one: a PolicyError, LockTimeout, CorruptState or Val…
- T-2641 [FEATURE S, done, 3 steps] A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; first …
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- similar finished tasks took 3–3 steps
## Files touched
- plugin/tests/test_wake_deferred.py
- plugin/lib/fmcli.py
- CHANGELOG.md
