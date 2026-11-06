---
id: T-2624
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsecond.py, plugin/tests/test_second.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-11-02T18:07:55Z
updated: 2026-11-02T18:10:51Z
base: 083fa7c639beb244e6d547235e49665fc830934c
base_tree: d8545ec805a4becd932931326e0bf43076cdd170
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T18:07:58Z
plan0_scope: [plugin/lib/fmsecond.py, plugin/tests/test_second.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# The session review captures no credential lines or asks already closed: it skips a redacted ask and reads recently closed work
## Raw request
> The session review captures no credential lines or asks already closed: it skips a redacted ask and reads recently closed work
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an ask holding a redacted credential isn't captured, and the child's prompt lists recently closed work — verify with `python3 plugin/tests/run.py test_second.Session.test_a_credential_line_is_no_task_and_closed_work_is_shown`
- [x] the second-read tests still pass — verify with `python3 plugin/tests/run.py test_second`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] skip redacted asks; closed work and paste/credential rule in the prompt
3. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_second.Session.test_a_credential_line_is_no_task_and_closed_work_is_shown` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Session 0s) / FAILED (1 classes: test_second.Session) [ran] [tree 7d2c20cb8865] [world 2f1906870a] (2026-11-02T18:08:08Z)
- (step 1) `python3 plugin/tests/run.py test_second.Session.test_a_credential_line_is_no_task_and_closed_work_is_shown` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Session 1s) / FAILED (1 classes: test_second.Session) [ran] [tree bb8010cec6b3] [world 2f1906870a] (2026-11-02T18:08:25Z)
- (step 2) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 38 tests in 15.7s (13 classes, 16 at a time; slowest: Rival 15s, RivalSplit 4s, Session 3s) / OK [ran] [tree f72bad1dc657] [world 2f1906870a] (2026-11-02T18:08:53Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 9507da7210ff] [world 2f1906870a] (2026-11-02T18:09:40Z)
- (ac 1) `python3 plugin/tests/run.py test_second.Session.test_a_credential_line_is_no_task_and_closed_work_is_shown` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Session 1s) / OK [ran] [tree 9507da7210ff] [world 2f1906870a] (2026-11-02T18:10:05Z)
- (ac 2) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 38 tests in 16.2s (13 classes, 16 at a time; slowest: Rival 16s, RivalSplit 4s, Session 3s) / OK [ran] [tree 9507da7210ff] [world 2f1906870a] (2026-11-02T18:10:05Z)
- (step 1) `python3 plugin/tests/run.py test_second.Session.test_a_credential_line_is_no_task_and_closed_work_is_shown` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Session 1s) / OK [ran] [tree 9507da7210ff] [world 2f1906870a] (2026-11-02T18:10:05Z)
- (audit edge) `self (S): read the diff; the redaction check runs before the overlap test under the same lock; closed titles are redacted like open ones; prompt grows by at most 40 short lines once a day` → an ask that only mentions the word REDACTED without brackets is still captured (marker is '[REDACTED'); no closed tasks → '- nothing'; sensitive projects still skip before any read [tree 9507da7210ff] (2026-11-02T18:10:05Z)
- (audit self) `self (S): read the diff; the redaction check runs before the overlap test under the same lock; closed titles are redacted like open ones; prompt grows by at most 40 short lines once a day` → no findings [tree 9507da7210ff] (2026-11-02T18:10:05Z)
## Log
- 2026-11-02T18:07:55Z created
- 2026-11-02T18:07:56Z focused
- 2026-11-02T18:07:58Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T18:10:46Z done
- 2026-11-02T18:10:51Z committed 1d29428d (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2374 [FEATURE M, done, 4 steps] Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and th…
- T-1606 [SECURITY M, done, 5 steps] Guard trust: pasted secrets, approval fatigue, fm doctor --wrong (from T-1553) — lesson: A claim like 'kept redacted' must be tested b…
- research T-0276-review-1: Verdict: changes needed.** One race and one privacy gap are verified. One self-triggering effect is likely but I did not confirm it by running …
- decision 2026-10-31: Mission 6's install-grant queue is the capability-miss captures (one durable task per missing tool, filed once ever by the hook, the tool rung and t…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_second.py
## Why not caught
the session review's tests only fed one clean ask; no fixture held a pasted credential or an ask a closed task settled
## Lessons
- A reviewer told what is still open, but not what was settled, re-raises settled asks: give it both sides of the ledger
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_second.py
- plugin/lib/fmsecond.py
- CHANGELOG.md
- MASTER.md
