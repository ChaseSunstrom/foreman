---
id: T-1768
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T09:19:31Z
updated: 2026-10-23T09:27:03Z
base: e612083bf101ec179d47b0235d0529654394f549
base_tree: 8778c97af8485a76477807c16b8ba05472a0ab54
plan0_at: 2026-10-23T09:25:59Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# The piped-gate note fires on 'fm check' text inside a quoted grep pattern (grep "a\|fm che
## Raw request
> The piped-gate note fires on 'fm check' text inside a quoted grep pattern (grep "a\|fm check b" f | cut): strip quoted strings before matching
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm check text inside quotes (a grep pattern) gets no piped-gate note; a real piped fm check still does — verify with `python3 plugin/tests/run.py test_hooks.GatePipe`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing case, then strip quoted text before matching
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_hooks.GatePipe` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: GatePipe 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree cb11183c84fd] (2026-10-23T09:26:06Z)
- `python3 plugin/tests/run.py test_hooks.GatePipe` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: GatePipe 0s) / FAILED (1 classes) [ran] [tree cb11183c84fd] (2026-10-23T09:26:06Z)
- `python3 plugin/tests/run.py test_hooks.GatePipe` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: GatePipe 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 45d29b6815ae] (2026-10-23T09:26:08Z)
- `python3 plugin/tests/run.py test_hooks.GatePipe` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: GatePipe 0s) / OK [ran] [tree 45d29b6815ae] (2026-10-23T09:26:08Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.GatePipe` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: GatePipe 0s) / OK [ran] [tree 45d29b6815ae] (2026-10-23T09:26:13Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.GatePipe` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: GatePipe 0s) / OK [ran] [tree 45d29b6815ae] (2026-10-23T09:26:14Z)
- (audit edge) `self review; GatePipe green` → single- and double-quoted text (with escaped quotes) is blanked before matching; FOREMAN_GATE_WAIT=600 fm quiet -- fm check | tail still notes (test) [tree 45d29b6815ae] (2026-10-23T09:26:14Z)
- (audit self) `self review; GatePipe green` → no findings [tree 45d29b6815ae] (2026-10-23T09:26:14Z)
## Log
- 2026-10-23T09:19:31Z created
- 2026-10-23T09:25:57Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-10-23T09:25:58Z focused
- 2026-10-23T09:27:01Z done
- 2026-10-23T09:27:03Z committed 0b6b03d0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0264-review-1: All three reviews are below. Only fmhooks, fmcore, fmcli, fmplugins and fmevolve were read. I did not run the tests or the PreToolUse hook. [st…
- research rsi-pass-20261009b: 1. **Answer.** I could ground three improvements. The biggest is that the guard-block log records the wrong part of the command. That made t…
- T-1759 [FIX S, done, 1 steps] A piped fm check reads green when the gates are red: say so on the Bash call
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- the similar finished task took 1 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Why not caught
T-1759's negatives had no fm check inside quoted text; the note fired on my own grep within minutes
## Files touched
- CHANGELOG.md
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
