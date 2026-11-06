---
id: T-2840
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T21:08:33Z
updated: 2026-11-03T22:58:26Z
base: ade8648046324aea1f9150dd99ec1da43c52cd0d
base_tree: f667e53c5f079769d55370cfb5168b35cb2abd76
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T22:55:19Z
plan0_scope: []
verified: strong
---
# fm outcomes --questions [--since TS] [--none]: count the question_answered ledger rows…
## Raw request
> FEATURE: fm outcomes --questions [--since TS] [--none]: count the question_answered ledger rows (AskUserQuestion) by outcome; --none exits 1 when any was asked since TS, so the 'stop asking me questions' steer (2026-11-03) has a runnable check for fm decide --check and fm genesis sweep
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm outcomes --questions counts question_answered rows by outcome since TS; --none exits 1 when any question was asked since TS — verify with `python3 plugin/tests/run.py test_question_answers`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: c.ledger_events(p, ('question_answered',), since=TS) already filters by kind and time; sum asked/default/other/typed/dismissed in cmd_outcomes behind --questions, with --none exiting 1 when asked>0. Likely outcome: ~15 lines and 3 flags. Fails if --since takes a date the ledger can't compare (its ts is ISO text): it's compared as text, as ledger_events already does.
2. Do less: grep the ledger by hand. Fails: fm decide --check and the genesis sweep need a command they can run.
Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then --questions/--since/--none in outcomes.py and cli.py
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_question_answers test_judgment` → exit 0 · Ran 71 tests in 9.9s (22 classes, 16 at a time; slowest: DoorPark 10s, DoorGate 4s, Followups 4s) / OK [ran] [tree 4d0e5ed25754] [world 2f1906870a] (2026-11-03T22:57:39Z)
- `python3 plugin/tests/run.py test_question_answers test_judgment.SteerChecks` → ✗ exit 1 · Ran 12 tests in 2.9s (2 classes, 16 at a time; slowest: SteerChecks 2s, QuestionAnswers 0s) / FAILED (2 classes: test_judgment.SteerChecks, test_question_answers.QuestionAnswers) (start tree + this task's tests) [ran] [tree 4d0e5ed25754] [world 2f1906870a] (2026-11-03T22:57:45Z)
- `python3 plugin/tests/run.py test_question_answers test_judgment.SteerChecks` → exit 0 · Ran 12 tests in 2.2s (2 classes, 16 at a time; slowest: SteerChecks 2s, QuestionAnswers 0s) / OK [ran] [tree 4d0e5ed25754] [world 2f1906870a] (2026-11-03T22:57:45Z)
- (ac 1) `python3 plugin/tests/run.py test_question_answers` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: QuestionAnswers 0s) / OK [ran] [tree 4d0e5ed25754] [world 2f1906870a] (2026-11-03T22:57:47Z)
- (audit adversary) `self-review: --questions reads question_answered rows through ledger_events (kind and since); --none exits 1 on any call; check_argv admits only the exact read-only form with an ISO --since, refusing extra flags (--settle writes) and shell text` → check_argv runs outside the guard; the new form is argv-only, a fixed verb and flags, and a --since that must fullmatch an ISO time; --settle and appended flags are refused (tested) [tree 4d0e5ed25754] (2026-11-03T22:57:47Z)
- (audit edge) `self-review: --questions reads question_answered rows through ledger_events (kind and since); --none exits 1 on any call; check_argv admits only the exact read-only form with an ISO --since, refusing extra flags (--settle writes) and shell text` → no rows, rows before --since, a JSON and a text reading [tree 4d0e5ed25754] (2026-11-03T22:57:47Z)
- (audit self) `self-review: --questions reads question_answered rows through ledger_events (kind and since); --none exits 1 on any call; check_argv admits only the exact read-only form with an ISO --since, refusing extra flags (--settle writes) and shell text` → no findings [tree 4d0e5ed25754] (2026-11-03T22:57:47Z)
## Log
- 2026-11-03T21:08:33Z created
- 2026-11-03T22:55:18Z set tier=S
- 2026-11-03T22:55:18Z planned: it has criteria and steps
- 2026-11-03T22:55:19Z focused
- 2026-11-03T22:55:19Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T22:58:24Z done
- 2026-11-03T22:58:26Z committed feccbe61 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2471 [FEATURE L, done, 3 steps] Cold read made reliable: Haiku first and Sonnet decides on a non-pass, a FAIL counts only with the quoted line and the MUST/NEVER or st…
- research mission-20261102-151141.pack: Genesis gen-3 Mission 6: #2 Exhaustive thinking (gen-0.md #2), per the standing mandate 'Genesis: build Foreman into a self-direct…
- research mission-20261101-105530.pack: (none given: improve the project in every way that matters to its user) [stale: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/…
- decision 2026-11-03: [cites: user steer 2026-11-03: stop asking me questions just keep going] [check: pending T-2840] No mid-run questions: options go on an artifact, th…
## Why not caught
the steer had no runnable check: decide --check allowed only rune check, the scorecard and tests
## Files touched
- plugin/tests/test_question_answers.py
- plugin/lib/sampo/outcomes.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_judgment.py
- plugin/lib/sampo/core.py
