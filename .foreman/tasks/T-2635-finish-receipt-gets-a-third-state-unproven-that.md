---
id: T-2635
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:33:15Z
base: 12db206c96c82b5ab8e8eb0a3f7e55264dc6dae5
base_tree: aefaccfae7a1fc7fc2771e02d9a5c4f2c53e51e6
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:30:38Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# A close with an unproven proof kind records it: the receipt says 'unproven: KINDS' beside its grade, the brief and task_done event keep the kinds, and the weekly line doesn't count it as strongly verified
## Raw request
> FEATURE: Finish receipt gets a third state, unproven, that an override cannot flip to proven (c01: First-class 'unproven' receipt state; value 4, effort M, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a PERFORMANCE task closed on a plain run stores unproven [perf-typed] in its meta and task_done event, its receipt line names it, and the weekly line counts it as unproven, not strongly verified; a close with no needs stores nothing — verify with `python3 plugin/tests/run.py test_unproven_close`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] store the kinds at close; receipt and weekly line read them
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_unproven_close` → red as expected (exit 1) · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: UnprovenClose 1s) / FAILED (1 classes: test_unproven_close.UnprovenClose) [ran] [tree e1d27011e1cc] [world 2f1906870a] (2026-11-02T20:31:11Z)
- (step 2) `python3 plugin/tests/run.py test_unproven_close test_verify_strength test_proof` → exit 0 · Ran 61 tests in 28.5s (11 classes, 16 at a time; slowest: Proof 28s, VerifyStrength 17s, Repeat 9s) / OK [ran] [tree 65a94bceb2c3] [world 2f1906870a] (2026-11-02T20:32:04Z)
- (step 3) `grep -q 'closed unproven' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 65a94bceb2c3] [world 2f1906870a] (2026-11-02T20:32:05Z)
- (ac 1) `python3 plugin/tests/run.py test_unproven_close` → exit 0 · Ran 2 tests in 2.3s (1 classes, 16 at a time; slowest: UnprovenClose 2s) / OK [ran] [tree 65a94bceb2c3] [world 2f1906870a] (2026-11-02T20:32:10Z)
- (audit edge) `self: proof_needs is read once more inside the close's mutate, wrapped so a rollup error never fails the close; the meta key is cleared before it is set, so a reopened and reclosed task carries only its newest kinds; weekly line and receipt read the stored kinds` → a close with no needs stores no key and the receipt and weekly line say nothing (tested); a reopened task's kinds are recomputed at its next close [tree 65a94bceb2c3] (2026-11-02T20:32:10Z)
- (audit self) `self: proof_needs is read once more inside the close's mutate, wrapped so a rollup error never fails the close; the meta key is cleared before it is set, so a reopened and reclosed task carries only its newest kinds; weekly line and receipt read the stored kinds` → no findings [tree 65a94bceb2c3] (2026-11-02T20:32:10Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:30:37Z planned from capture
- 2026-11-02T20:30:38Z focused
- 2026-11-02T20:30:38Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:30:39Z steer: re-grounded to S: the receipt already lists each unproven kind and the commit carries an Unproven: trailer; the gap is the stored grade (verified: strong) that digests and the weekly line count while fm prove still lists the task
- 2026-11-02T20:32:05Z scope: plugin/lib/fmcli.py and plugin/lib/fmcost.py (the close and the weekly line), CHANGELOG.md
- 2026-11-02T20:33:10Z done
- 2026-11-02T20:33:15Z committed f4485da5 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2637 [FEATURE M, dropped, 0 steps] fm outcomes: per proof kind, how often a proven task was later reverted or corrected…
- T-2651 [FEATURE S, done, 3 steps] fm task evidence --bench CMD --under MS: a benchmark that is a pass/fail proof, failing when the median is over the threshold (today --…
- T-2648 [FEATURE S, done, 3 steps] fm drill gains a fault that drops one ledger event class (every task_done line, say): each reader that leans on it must name what's mis…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- similar finished tasks took 3–3 steps
## Files touched
- plugin/tests/test_unproven_close.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- CHANGELOG.md
