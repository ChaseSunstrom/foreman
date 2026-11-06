---
id: T-2839
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T20:38:59Z
updated: 2026-11-03T21:01:35Z
base: 7fe23cfbdb92a3fb241db1bffa51dc80f9568a8e
base_tree: 98ce5aa793ab50e49275a2ebd55319385bc861c4
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T20:59:58Z
plan0_scope: []
verified: ok
unproven: [meaning, typed]
---
# A criterion whose text quotes the dash form ("… — verify with `CMD` …") is read by…
## Raw request
> FIX: a criterion whose text quotes the dash form ("… — verify with `CMD` …") is read by verify_of from the wrong backtick span: T-2789's AC ran 'CMD`... python3' (exit 127). verify_of should take the last '— verify with `…`' at the end of the line, as split_verify's _VERIFY_TAIL does
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] verify_of and strip_verify read the last dash-form verify at the end of a criterion, so a criterion whose text quotes the dash form runs its real command — verify with `python3 plugin/tests/run.py test_task_ergonomics`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a criterion quoting the dash form yields its trailing command
2. [x] fix: _VERIFY_OF matches only the last occurrence
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics.SplitVerify` → red: verify_of returned "CMD`' at every entry point — verify with `python3 run.py test_x" for a criterion quoting the dash form [tree 3888ef3c5804] (2026-11-03T21:00:17Z)
- (step 2) `python3 plugin/tests/run.py test_task_ergonomics test_cli test_core` → green: OK [tree 3888ef3c5804] (2026-11-03T21:00:49Z)
- `python3 plugin/tests/run.py test_task_ergonomics.SplitVerify` → ✗ exit 1 · Ran 17 tests in 8.0s (1 classes, 16 at a time; slowest: SplitVerify 7s) / FAILED (1 classes: test_task_ergonomics.SplitVerify) (start tree + this task's tests) [ran] [tree 3888ef3c5804] [world 2f1906870a] (2026-11-03T21:01:05Z)
- `python3 plugin/tests/run.py test_task_ergonomics.SplitVerify` → exit 0 · Ran 17 tests in 6.7s (1 classes, 16 at a time; slowest: SplitVerify 6s) / OK [ran] [tree 3888ef3c5804] [world 2f1906870a] (2026-11-03T21:01:05Z)
- (ac 1) `python3 plugin/tests/run.py test_task_ergonomics` → exit 0 · Ran 36 tests in 6.9s (4 classes, 16 at a time; slowest: SplitVerify 7s, TaskErgonomics 6s, ExpectFail 2s) / OK [ran] [tree 3888ef3c5804] [world 2f1906870a] (2026-11-03T21:01:13Z)
- (audit intent) `self: _VERIFY_OF now captures only a span that holds no further '— verify with '', so search and sub both act on the last occurrence at the end of the line; criteria without a quoted form match exactly as before` → a criterion that quotes the dash form runs its own trailing command [tree 3888ef3c5804] (2026-11-03T21:01:13Z)
- (audit edge) `self: _VERIFY_OF now captures only a span that holds no further '— verify with '', so search and sub both act on the last occurrence at the end of the line; criteria without a quoted form match exactly as before` → a command containing backticks still matches (only the marker phrase is excluded from the span); strip_verify removes only the trailing form [tree 3888ef3c5804] (2026-11-03T21:01:13Z)
- (audit adversary) `self: _VERIFY_OF now captures only a span that holds no further '— verify with '', so search and sub both act on the last occurrence at the end of the line; criteria without a quoted form match exactly as before` → parsing only; the read command still passes the existing runnable and lint checks [tree 3888ef3c5804] (2026-11-03T21:01:13Z)
- (audit self) `self: _VERIFY_OF now captures only a span that holds no further '— verify with '', so search and sub both act on the last occurrence at the end of the line; criteria without a quoted form match exactly as before` → no findings [tree 3888ef3c5804] (2026-11-03T21:01:13Z)
## Log
- 2026-11-03T20:38:59Z created
- 2026-11-03T20:59:57Z planned: it has criteria and steps
- 2026-11-03T20:59:58Z set tier=S
- 2026-11-03T20:59:58Z focused
- 2026-11-03T20:59:58Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T21:01:33Z done
- 2026-11-03T21:01:35Z committed 360ccb14 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- T-2789 [CLEAN S, done, 2 steps] The verify-phrase parsing lives in four places (task new --ac, task ac add, task ac edit…
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
- similar finished tasks took 2–5 steps
## Why not caught
no test stored a criterion whose prose quotes the dash form; T-2789's own criterion was the first
## Lessons
- A suffix marker regex must exclude the marker from its capture, or the first quoted copy wins
## Files touched
- plugin/tests/test_task_ergonomics.py
- plugin/lib/sampo/core.py
