---
id: T-2720
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:17:49Z
updated: 2026-11-02T23:18:53Z
base: 478e8d3b6a4ca62a856c0edd0ab959e4e006c647
base_tree: acb59415ce6bcac48f3b72245e7d93559a60d2f0
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:17:50Z
plan0_scope: []
verified: strong
---
# M-02's kill result sits beside its script in bench/moonshot (3 of 3 rebuilt, viable)
## Raw request
> M-02's kill result sits beside its script in bench/moonshot (3 of 3 rebuilt, viable)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the result file holds M-02's full viable verdict — verify with `python3 -c "import json; d=json.load(open('bench/moonshot/m02-result.json')); assert (d['passed'], d['of'], d['verdict']) == (3, 3, 'viable')"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] rerun M-02's kill test into bench/moonshot/m02-result.json
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -c "import json; d=json.load(open('bench/moonshot/m02-result.json')); assert (d['passed'], d['of'], d['verdict']) == (3, 3, 'viable')"` → exit 0 · (no output) [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:56Z)
- (ac 1) `python3 -c "import json; d=json.load(open('bench/moonshot/m02-result.json')); assert (d['passed'], d['of'], d['verdict']) == (3, 3, 'viable')"` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:17:56Z [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:57Z)
- (audit intent) `reran bench/moonshot/kill_m02.py into m02-result.json: semver, table and ranges each rebuilt blind by a tool-less child on attempt 1 and passed every original test, reproducing T-2679's viable` → review #20 asked for M-02's result beside its kill script; it is committed and reruns [tree e6e91a66d21b] (2026-11-02T23:17:57Z)
- (audit self) `reran bench/moonshot/kill_m02.py into m02-result.json: semver, table and ranges each rebuilt blind by a tool-less child on attempt 1 and passed every original test, reproducing T-2679's viable` → no findings [tree e6e91a66d21b] (2026-11-02T23:17:57Z)
## Log
- 2026-11-02T23:17:49Z created
- 2026-11-02T23:17:49Z redo of T-2719: takes over its start point and edited files
- 2026-11-02T23:17:49Z focused
- 2026-11-02T23:17:50Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:17:55Z scope: bench/moonshot/m02-result.json
- 2026-11-02T23:18:50Z done
- 2026-11-02T23:18:53Z committed 7157321a (1 file)
- 2026-11-02T23:18:53Z includes T-2713: FIX: cross-cutting review gen-3 #20 (what is presented ahead of its proof): a kill test…
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2679 [RESEARCH M, done, 2 steps] Kill test M-02 (code as a regenerable cache of intent and proofs): rebuild three deleted spec-suite modules from their spec and tests …
- T-2719 [FIX S, dropped, 3 steps] bench/moonshot keeps verdicts only: M-02's result beside its script, the confounded M-12 run removed
- decision 2026-11-02: Recommendation: M-02 is viable at the kill stage (3 of 3 spec-suite modules rebuilt blind passed every test) and moves to its slice: regenerate one …
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
- similar past tasks were L: consider --tier L
## Regression test
none: a data file; its check is the criterion
## Why not caught
T-2687 moved M-02's script into bench/ without its output, which lived only in a scratch file's tail
## Files touched
- bench/moonshot/m02-result.json
