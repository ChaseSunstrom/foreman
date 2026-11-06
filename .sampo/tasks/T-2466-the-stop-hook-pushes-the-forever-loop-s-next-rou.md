---
id: T-2466
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T09:35:18Z
updated: 2026-11-01T09:51:43Z
base: 4f7b950486a26a749d127d2d0651060ac7a7c98c
base_tree: 1ea9f5f6b8f3ff2840164ab6e6f55e788b397257
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T09:35:19Z
plan0_scope: []
verified: strong
---
# The Stop hook pushes the forever loop's next round while fm drive --round-first holds new work for the open Genesis round
## Raw request
> The Stop hook pushes the forever loop's next round while fm drive --round-first holds new work for the open Genesis round
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] no loop push while the round is held — verify with `python3 plugin/tests/run.py test_loop test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then skip the loop push while c._round_first(p)
## Resume here
## Docs impact
none: internal hook behaviour MASTER describes under fm drive --round-first
## Verification evidence
- `python3 plugin/tests/run.py -k test_the_drive_holds_the_loop_while_the_genesis_round_is_open test_loop` → ✗ exit 1 · Ran 1 tests in 2.5s (1 classes, 16 at a time; slowest: Loop 1s) / FAILED (1 classes: test_loop.Loop) (start tree + this task's tests) [ran] [tree e9f984d07bb2] (2026-11-01T09:35:35Z)
- `python3 plugin/tests/run.py -k test_the_drive_holds_the_loop_while_the_genesis_round_is_open test_loop` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Loop 0s) / OK [ran] [tree e9f984d07bb2] (2026-11-01T09:35:35Z)
- (step 1) `python3 plugin/tests/run.py test_loop test_hooks test_core` → exit 0 · Ran 396 tests in 54.2s (61 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 39s, PreToolUse 34s) / OK [ran] [tree e9f984d07bb2] (2026-11-01T09:36:30Z)
- `python3 plugin/tests/run.py -k test_the_drained_product_check_waits_while_the_genesis_round_is_held test_hooks` → ✗ exit 1 · Ran 1 tests in 2.7s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree cf26b7a3299c] (2026-11-01T09:37:34Z)
- `python3 plugin/tests/run.py -k test_the_drained_product_check_waits_while_the_genesis_round_is_held test_hooks` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree cf26b7a3299c] (2026-11-01T09:37:34Z)
- (step 1) `python3 plugin/tests/run.py test_loop test_hooks test_core` → exit 0 · Ran 397 tests in 45.3s (61 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree cf26b7a3299c] (2026-11-01T09:38:20Z)
- (ac 1) `python3 plugin/tests/run.py test_loop test_hooks` → exit 0 · Ran 265 tests in 52.0s (35 classes, 16 at a time; slowest: Stop 52s, NoTaskGate 37s, PreToolUse 32s) / OK [ran] [tree cf26b7a3299c] (2026-11-01T09:39:18Z)
- (ac 1) `python3 plugin/tests/run.py test_loop test_hooks` → exit 0 · Ran 265 tests in 41.4s (35 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree cf26b7a3299c] (2026-11-01T09:45:43Z)
- (audit intent) `main-thread lens pass over the 2-line diff and its two tests` → the Stop hook's loop push and its drained product-check push both wait while fm drive --round-first holds new work, as fm next, side work, the friction pass and the inbox pick already do [tree cf26b7a3299c] (2026-11-01T09:45:43Z)
- (audit edge) `main-thread lens pass over the 2-line diff and its two tests` → round-first off gives the old behaviour (both tests' off halves are the existing T-1057 and T-0415 tests, green); the wait branch still speaks, so the turn ends with what it waits on [tree cf26b7a3299c] (2026-11-01T09:45:43Z)
- (audit operator) `main-thread lens pass over the 2-line diff and its two tests` → no more brainstorm-round or product-sweep pushes during the round; hook bench green in fm check [tree cf26b7a3299c] (2026-11-01T09:45:43Z)
- (audit self) `main-thread lens pass over the 2-line diff and its two tests` → no findings [tree cf26b7a3299c] (2026-11-01T09:45:43Z)
## Log
- 2026-11-01T09:35:18Z created
- 2026-11-01T09:35:18Z focused
- 2026-11-01T09:35:19Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T09:36:36Z scope: plugin/lib/fmhooks.py (the loop push) and plugin/tests/test_loop.py only
- 2026-11-01T09:36:56Z steer(self): the drained push (T-0415: check the product end to end, then plan and work the first) is the same leak: it starts new maintenance while the round is held; folded in
- 2026-11-01T09:38:25Z scope: plugin/lib/fmhooks.py (the loop push and the drained push) and plugin/tests/test_loop.py, test_hooks.py only
- 2026-11-01T09:46:41Z done
- 2026-11-01T09:46:43Z committed cd2f93a3 (3 files)
- 2026-11-01T09:46:48Z guard authorization added: publish
- 2026-11-01T09:51:43Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2464 [FIX S, done, 1 steps] The Stop hook's drive offers inbox items fm drive --round-first holds (its inbox pick and its planning list skip _round_held) — lesson: A h…
- T-2459 [FIX S, done, 2 steps] Round first covers the drive's side-work offers too: while background work runs, the Stop hook offered T-2365 (filed by Foreman) despite fm…
- T-1879 [CLEAN M, done, 3 steps] Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f — lesson: An idempotence check compares what t…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
## Lessons
- Every drive push that starts new work (loop round, product sweep, inbox, side work, friction) must check the round hold; T-2459/2460/2464/2466 found them one at a time
## Files touched
- plugin/tests/test_loop.py
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
