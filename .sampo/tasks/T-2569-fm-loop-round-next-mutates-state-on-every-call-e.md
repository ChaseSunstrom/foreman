---
id: T-2569
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T08:22:47Z
updated: 2026-11-02T09:15:40Z
base: c2c0683d152bc59b1c71da1054f99660cb80db8d
base_tree: 71ca7901231a27c2f5f219cbb2e857e52f437b03
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T08:23:18Z
plan0_scope: []
verified: strong
---
# fm loop round --next re-prints a round that just started (under 15 min, no tasks made) instead of closing it dry
## Raw request
> FIX: fm loop round --next mutates state on every call (ends the open round with its yield and starts the next), so reading its instructions twice ended rounds 26 and 27 as dry and switched the loop off; a round started minutes ago with no tasks made and no ideas run shouldn't close as dry: re-print the open round's instructions instead (fm loop round to print, --next only to advance)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two fm loop round --next calls within minutes leave the round number and dry streak unchanged after the first; a round older than 15 min, or one that made tasks, is still counted as before — verify with `python3 plugin/tests/run.py test_loop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_loop
2. [x] grace check in round_brief
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_loop` → ✗ exit 1 · Ran 22 tests in 5.1s (4 classes, 16 at a time; slowest: Loop 5s, LoopReview 3s, LagKept 0s) / FAILED (1 classes: test_loop.LoopReview) [ran] [tree 6500faa41106] [world 2f1906870a] (2026-11-02T08:23:45Z)
- (ac 1) `python3 plugin/tests/run.py test_loop 2>&1 | grep -E "^(ERROR|FAIL):|Error|^OK|FAILED" | head -6` → exit 0 · OK [ran] [tree c667f69b205c] [world 2f1906870a] (2026-11-02T08:24:07Z)
- (step 2) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 22 tests in 4.6s (4 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, LagKept 0s) / OK [ran] [tree c667f69b205c] [world 2f1906870a] (2026-11-02T08:24:23Z)
- `python3 plugin/tests/run.py test_loop` → ✗ exit 1 · Ran 22 tests in 5.5s (4 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, LagKept 0s) / FAILED (1 classes: test_loop.LoopReview) (start tree + this task's tests) [ran] [tree 3d18f0859cd9] [world 2f1906870a] (2026-11-02T08:40:30Z)
- `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 22 tests in 4.4s (4 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, LagKept 0s) / OK [ran] [tree 3d18f0859cd9] [world 2f1906870a] (2026-11-02T08:40:30Z)
- (ac 1) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 22 tests in 4.4s (4 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, LagKept 0s) / OK [ran] [tree 3d18f0859cd9] [world 2f1906870a] (2026-11-02T08:40:35Z)
- (audit intent) `self-review: the grace sits in round_brief beside T-1153's re-read; it needs an open round, a 'last' under GRACE_S and no task made since; fm loop yield still closes any round; test_foresight now isolates XDG_CONFIG_HOME` → three --next calls within minutes keep round 1 open and no dry count (test); an aged round still counts dry and two end the loop (the existing test, now aged 20 min) [tree 3d18f0859cd9] (2026-11-02T08:40:35Z)
- (audit edge) `self-review: the grace sits in round_brief beside T-1153's re-read; it needs an open round, a 'last' under GRACE_S and no task made since; fm loop yield still closes any round; test_foresight now isolates XDG_CONFIG_HOME` → a genuinely dry round finished in under 15 min re-prints until 15 min pass or fm loop yield records it; a missing or unparsable 'last' disables the grace (counted as before) [tree 3d18f0859cd9] (2026-11-02T08:40:35Z)
- (audit self) `self-review: the grace sits in round_brief beside T-1153's re-read; it needs an open round, a 'last' under GRACE_S and no task made since; fm loop yield still closes any round; test_foresight now isolates XDG_CONFIG_HOME` → no findings [tree 3d18f0859cd9] (2026-11-02T08:40:35Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 6e93e16aabfa] [world 2f1906870a] (2026-11-02T09:15:40Z)
## Log
- 2026-11-02T08:22:47Z created
- 2026-11-02T08:23:13Z planned from capture
- 2026-11-02T08:23:15Z focused
- 2026-11-02T08:23:18Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T08:34:56Z scope: plugin/tests/test_foresight.py — the gate failed on the host's real night timer (its skipped run exits 1); the Foresight tests now point XDG_CONFIG_HOME at the test's temp dir
- 2026-11-02T08:40:54Z done
- 2026-11-02T08:40:57Z committed 150192f9 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1879 [CLEAN M, done, 3 steps] Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f — lesson: An idempotence check compares what t…
- T-1825 [FEATURE M, done, 3 steps] FEATURE: fm run (headless) skips a model call when the tree and the failing check's output — lesson: count list items by line start, no…
- T-1153 [FIX S, done, 2 steps] Fm loop round advances the round number every time it is called, so reading the round's br
- decision 2026-11-02: [costly] Forever loop re-enabled: rounds 26-27 closed dry only because fm loop round --next was called 3 times to read its instructions (captured as…
- similar finished tasks took 2–3 steps
## Lessons
- A verb that both shows instructions and advances state must not advance on a call made seconds after the last; a drive line that names it will be called more than once
## Plan gaps
- failed first: step 1 red test in test_loop
## Files touched
- plugin/tests/test_loop.py
- plugin/lib/fmloop.py
- CHANGELOG.md
- plugin/tests/test_foresight.py
