---
id: T-0754
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/tests/test_learning2.py]
depends_on: []
source: self
created: 2026-10-09T21:46:14Z
updated: 2026-10-09T21:47:08Z
base: 8abc58a69a72588e758d0643e8ad6182a1bdc3c1
base_tree: d587bc0ede029464332b73bc33b26197f1a00be9
verified: strong
---
# Eval inbox: guard false-positive candidates are blocks today's guard allows, not blocks later granted
## Raw request
> fm evals inbox lists every guard block later granted as a possible false positive; block-then-grant is the guard working. Real candidates are blocks today's guard allows (fmfriction._recheck)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a granted block isn't listed; a block today's guard allows is — verify with `python3 plugin/tests/run.py -p test_learning2.py -k EvalInbox`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test both; read candidates through fmfriction._recheck
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_learning2.py -k EvalInbox` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: EvalInbox 0s) / FAILED (1 classes) [ran] [tree ed5817a840de] (2026-10-09T21:46:26Z)
- (step 1) `python3 plugin/tests/run.py -p test_learning2.py -k EvalInbox` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: EvalInbox 0s) / FAILED (1 classes) [ran] [tree 80f837758540] (2026-10-09T21:46:35Z)
- (step 1) `python3 plugin/tests/run.py -p test_learning2.py -k EvalInbox` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: EvalInbox 0s) / OK [ran] [tree 94176e91d646] (2026-10-09T21:46:50Z)
- (ac 1) `python3 plugin/tests/run.py -p test_learning2.py -k EvalInbox` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: EvalInbox 0s) / OK [ran] [tree 94176e91d646] (2026-10-09T21:47:07Z)
- `python3 plugin/tests/run.py -p test_learning2.py` → exit 0 · Ran 7 tests in 0.8s (7 classes, 16 at a time; slowest: Playbook 1s, Retire 0s, SmokeFate 0s) / OK [ran] [tree 94176e91d646] (2026-10-09T21:47:07Z)
- (audit self) `self: candidates now come from fmfriction._recheck (fmreplay verdicts with no grants), so only blocks the rule itself allows today are listed; 'brief' blocks are excluded because they depended on there being no active task, not on a rule; a granted block is no longer a candidate (tested); live: 5 candidates, 0.5 s` → no findings [tree 94176e91d646] (2026-10-09T21:47:07Z)
## Log
- 2026-10-09T21:46:14Z created
- 2026-10-09T21:46:17Z planned from capture
- 2026-10-09T21:46:20Z focused
- 2026-10-09T21:47:08Z done
- 2026-10-09T21:47:08Z committed 4a9bf49 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0161 [SECURITY M, done, 3 steps] Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151) — lesson: Fail-closed mean…
- T-0187 [FEATURE M, done, 3 steps] Self-improvement scoreboard: the friction digest rechecks each earlier guard block with today's guard and shows the trend since the las…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Why not caught
none: T-0752's test asserted the heuristic it was written with; running the command on the real ledger showed every listed block was the guard working
## Plan gaps
- failed first: step 1 test both; read candidates through fmfriction._recheck
## Files touched
- plugin/tests/test_learning2.py
- plugin/lib/fmcost.py
