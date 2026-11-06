---
id: T-0404
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:16:44Z
updated: 2026-10-09T04:18:35Z
base: 7dcf1bfc8be1dd68bc9faa79ca93cef50e86bd03
base_tree: 518097e18b5fe4974ea5bb776e04d174d5e19031
verified: strong
---
# Guard: a brief refusal whose own command runs fm focus should say to run the focus as its own command (JARVIS: 'fm focus T-0278 …; sed -i …' refused twice in a row)
## Raw request
> Guard: a brief refusal whose own command runs fm focus should say to run the focus as its own command (JARVIS: 'fm focus T-0278 …; sed -i …' refused twice in a row)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the brief refusal of a line containing fm focus says to run it as its own command; others don't — verify with `python3 plugin/tests/run.py -k test_brief_refusal_with_focus_in_the_line`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the hint
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 04:16 UTC) [ran] [tree 518097e18b5f] (2026-10-09T04:16:45Z)
- `python3 plugin/tests/run.py -k test_brief_refusal_with_focus_in_the_line` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: FocusHint 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f8b0167303eb] (2026-10-09T04:17:01Z)
- `python3 plugin/tests/run.py -k test_brief_refusal_with_focus_in_the_line` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: FocusHint 0s) / OK [ran] [tree f8b0167303eb] (2026-10-09T04:17:01Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.3    33.0     150  [0] / SessionEnd                  29.1    30.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 939 tests in [ran] [tree fd4093082806] (2026-10-09T04:18:35Z)
- (ac 1) `python3 plugin/tests/run.py -k test_brief_refusal_with_focus_in_the_line` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: FocusHint 0s) / OK [ran] [tree fd4093082806] (2026-10-09T04:18:35Z)
- (audit intent) `self: message text only, appended to a brief refusal after the decision; consumers of the detail only log it` → JARVIS's 'fm focus T-0278 …; sed -i …' refusal now says to run the focus first (test) [tree fd4093082806] (2026-10-09T04:18:35Z)
- (audit edge) `self: message text only, appended to a brief refusal after the decision; consumers of the detail only log it` → fm task new … --focus also counts; a line with no focus keeps the plain message (test) [tree fd4093082806] (2026-10-09T04:18:35Z)
- (audit adversary) `self: message text only, appended to a brief refusal after the decision; consumers of the detail only log it` → brief is never authorizable and stays refused; only its text grows [tree fd4093082806] (2026-10-09T04:18:35Z)
- (audit self) `self: message text only, appended to a brief refusal after the decision; consumers of the detail only log it` → no findings [tree fd4093082806] (2026-10-09T04:18:35Z)
## Log
- 2026-10-09T04:16:44Z created
- 2026-10-09T04:16:45Z focused
- 2026-10-09T04:18:35Z done
- 2026-10-09T04:18:35Z committed db6e495 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- T-0395 [CLEAN S, done, 1 steps] Guard: the pipe-shell refusal of curl | python3 -c should say how it passes (JARVIS lost a turn: hf download > log on the same line)
- T-0384 [FIX M, done, 3 steps] FIX: guard false positives seen on JARVIS: (1) cd ABS && A > f; B > g resolves f/g against — lesson: Making the guard more precise means re…
- decision 2026-10-08: T-0368: entry points re-exec under a saved supported Python
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
