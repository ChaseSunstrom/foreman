---
id: T-0406
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:24:12Z
updated: 2026-10-09T04:27:49Z
base: 6c92a15094ff33db1c496f3e033e5a522324ac25
base_tree: 06ac4f982211bad691a1d0b8dc2678deccaba539
verified: strong
---
# Evidence for a step should move the UI's current step there (JARVIS: steps 3-5 proven, band stuck on step 1/5 — only finish ticks steps)
## Raw request
> Evidence for a step should move the UI's current step there (JARVIS: steps 3-5 proven, band stuck on step 1/5 — only finish ticks steps)
## Interpretation
The user saw JARVIS work on other steps while Claude Code's Foreman band kept showing an earlier one. fm task evidence --step N records proof but never ticks the step or moves its CURRENT marker; only fm task finish (or fm task step done) does. So the band showed T-0278 step 1/5, 0 done, while steps 3, 4 and 5 had passing runs.
## Assumptions (confidence)
## Acceptance criteria
- [x] a passing step run ticks it and moves CURRENT to the next open step; a failing run reopens it and makes it current; finish still refuses a step whose newest run failed — verify with `python3 plugin/tests/run.py -k test_step_evidence_moves_the_current_step`
## Non-goals
## Approach (options → choice → why)
(A, chosen) evidence for step N moves the work there: a run that closes it (evidence in, no failed run newer than a pass) ticks it and makes the next open step after it current; a failed run reopens it and makes it current. Rejected: (B) ask Claude to run fm task step current N — the rules already say evidence per step and it isn't done; (C) infer the step from edited files — guesswork; (D) show the last-evidenced step in the band only — the brief and fm next would still disagree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first
2. [x] Brief.track_step + the evidence handler
3. [x] gate, changelog, ship
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py -k test_step_evidence_moves_the_current_step` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: TaskLifecycle 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 89866ee32a7b] (2026-10-09T04:26:22Z)
- `python3 plugin/tests/run.py -k test_step_evidence_moves_the_current_step` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: TaskLifecycle 1s) / OK [ran] [tree 89866ee32a7b] (2026-10-09T04:26:22Z)
- (step 1) `python3 plugin/tests/run.py -k test_step_evidence_moves_the_current_step` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: TaskLifecycle 1s) / OK [ran] [tree 89866ee32a7b] (2026-10-09T04:26:23Z)
- (step 2) `python3 plugin/tests/run.py -p test_cli.py` → exit 0 · Ran 73 tests in 14.9s (16 classes, 16 at a time; slowest: TaskLifecycle 15s, StateViews 5s, Checks 3s) / OK [ran] [tree 89866ee32a7b] (2026-10-09T04:26:38Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.3    33.2     150  [0] / SessionEnd                  29.3    35.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 940 tests in [ran] [tree bbe286371051] (2026-10-09T04:27:37Z)
- (ac 1) `python3 plugin/tests/run.py -k test_step_evidence_moves_the_current_step` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: TaskLifecycle 1s) / OK [ran] [tree bbe286371051] (2026-10-09T04:27:48Z)
- (audit intent) `self: one rule in Brief.add_evidence so every evidence writer follows it; full suite 940/940; seen working on this task's own steps (fm next moved to step 3 after steps 1-2 had evidence)` → the band and fm next follow the step being proven — ticked on a closing run, current on a failure (test); JARVIS's T-0278 case reproduced in the test [tree bbe286371051] (2026-10-09T04:27:48Z)
- (audit edge) `self: one rule in Brief.add_evidence so every evidence writer follows it; full suite 940/940; seen working on this task's own steps (fm next moved to step 3 after steps 1-2 had evidence)` → inconclusive runs move nothing; fm task step done after evidence is idempotent; fm task prove's red then green ends ticked; a failure on a ticked step reopens it, so finish can't skip a step whose newest run failed [tree bbe286371051] (2026-10-09T04:27:48Z)
- (audit maintainer) `self: one rule in Brief.add_evidence so every evidence writer follows it; full suite 940/940; seen working on this task's own steps (fm next moved to step 3 after steps 1-2 had evidence)` → track_step reuses _refuse_failed_run/has_evidence, the rule finish already applies [tree bbe286371051] (2026-10-09T04:27:48Z)
## Log
- 2026-10-09T04:24:12Z created
- 2026-10-09T04:24:12Z focused
- 2026-10-09T04:27:48Z done
- 2026-10-09T04:27:49Z committed 6eca3f8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
## Lessons
- State the UI shows must change where the work happens (recording evidence), not only at the close
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
