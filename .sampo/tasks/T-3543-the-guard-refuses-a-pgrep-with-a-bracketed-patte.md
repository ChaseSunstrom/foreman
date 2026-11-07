---
id: T-3543
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T22:04:59Z
updated: 2026-11-07T00:44:55Z
group: guard refuses legitimate lane and task work
lane: ~/.claude/foreman.lanes/T-3543
lane_branch: foreman/T-3543
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:37:30Z
plan0_scope: []
---
# The guard refuses a pgrep with a bracketed pattern (pgrep -f '[f]m ui --json') as…
## Raw request
> FIX: the guard refuses a pgrep with a bracketed pattern (pgrep -f '[f]m ui --json') as matching its own shell, though the bracket is the documented fix for exactly that; recognise the bracket form, with a FORMS row
## Interpretation
The guard rule is hooks.py _self_match (not fmguard.py). A bare bracketed pattern (pgrep -f '[f]m ui --json') already passes; every logged refusal of a 'bracketed' pgrep held the plain text elsewhere in the command (T-3244: an echo; the 2026-11-06 22:04 incident was in fact an unbracketed pgrep -f "fm ui --json"), which really matches the shell. The defect is the message: it tells a bracketed pattern to bracket one letter, so a correct refusal reads as an over-refusal and gets filed again.
## Assumptions (confidence)
## Acceptance criteria
- [ ] pgrep -f/pkill -f '[f]m ui --json' and ps aux | grep '[f]m ui' pass; the same pgrep/pkill unbracketed stay refused — verify with `nice -n 10 python3 plugin/tests/run.py test_hooks`
- [ ] a bracketed pattern whose plain text sits elsewhere in the command stays refused, and the refusal names that text instead of telling it to bracket one letter — verify with `nice -n 10 python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
(1) skip bracketed patterns: loosens, the shell really matches → no. (2) drop as not-a-bug like T-3244: it will be filed a third time → no. (3) pin the bracketed/unbracketed pgrep, pkill and ps|grep forms in test_hooks, and when a bracketed pattern still hits, name the other text that matches and say to move it (a script file) or bracket it there → chosen: no rule change, the message stops misleading.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: bracket/unbracketed rows and the message for a bracket that still matches
2. [x] name the matching text in _self_match's refusal
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_hooks.Hooks.test_a_process_match_on_its_own_command_is_refused` → ✗ exit 1 · run.py: no test matches test_hooks.Hooks.test_a_process_match_on_its_own_command_is_refused [ran] [tree 7961648e3ad7] [world 2f1906870a] (2026-11-07T00:37:48Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_hooks.PreToolUse.test_a_process_match_on_its_own_command_is_refused` → ✗ exit 1 · Ran 1 tests in 1.7s (1 jobs, 16 at a time; slowest: PreToolUse 1s) / FAILED (1 classes: test_hooks.PreToolUse) [ran] [tree 7961648e3ad7] [world 2f1906870a] (2026-11-07T00:37:55Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_hooks.PreToolUse.test_a_process_match_on_its_own_command_is_refused` → exit 0 · Ran 1 tests in 2.1s (1 jobs, 16 at a time; slowest: PreToolUse 2s) / OK [ran] [tree bac543c8f228] [world 2f1906870a] (2026-11-07T00:38:07Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 272 tests in 152.6s (134 jobs, 16 at a time; slowest: PreToolUse 79s, SessionStart.test_budget_holds_with_large_queue 43s, NoTaskGateClose 31s) / OK [ran] [tree f0c0a04533e7] [world 2f1906870a] (2026-11-07T00:40:43Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 28 tests in 14.0s (28 jobs, 16 at a time; slowest: PreToolUse.test_a_broken_core_library_keeps_grants_visible_and_protection_on 6s, PreToolUse.test_a_bare_stdin_reader_is_refused_before_it_hangs 4 [ran] [tree 573aa6c1da94] [world 2f1906870a] (2026-11-07T00:44:55Z)
## Log
- 2026-11-06T22:04:59Z created
- 2026-11-07T00:34:07Z set tier=S
- 2026-11-07T00:34:14Z planned: it has criteria and steps
- 2026-11-07T00:37:24Z lane: ~/.claude/foreman.lanes/T-3543 on foreman/T-3543
- 2026-11-07T00:37:28Z focused
- 2026-11-07T00:37:30Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3244 [FIX S, dropped, 0 steps] Guard over-refusal: pgrep -fc '[f]m ui --json' (a bracketed pattern that can't match its…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-3154 [FIX S, done, 1 steps] The self-match guard judges each alternative of a process-search pattern, and only patterns that are really run
- decision 2026-11-02: [revisited: steer-expansion exam. From a user's raw words] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: python3 plugin/tes…
- similar finished tasks took 1–3 steps
