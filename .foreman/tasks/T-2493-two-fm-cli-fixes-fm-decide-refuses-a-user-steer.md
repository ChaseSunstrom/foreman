---
id: T-2493
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-01T17:47:17Z
updated: 2026-11-01T18:01:32Z
batch: [T-2465, T-2475]
base: d59dd45591a79a527c01b2a5b7d0dc6f844ca8a6
base_tree: 51167e2cd152cec830f56038382cce181d9c9ed5
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T17:47:22Z
plan0_scope: []
verified: strong
---
# Two fm CLI fixes: fm decide refuses a user-steer row without --check; a mistyped flag's hint names only the typed comma…
## Raw request
> T-2465: FIX: fm decide accepts a --cites 'user steer …' row with no --check, and fm doctor's steer-checks line fails only later (hit twice this session: 2026-10-31 and T-2462's row); refuse it at record time, naming --check
> T-2475: FIX: a mistyped flag's 'did you mean' suggests a flag from any command (fm night --print-timer suggested --print, which fm night doesn't take); suggest only the typed command's own flags
## Interpretation
Reading 1: do T-2465, T-2475 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2493. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670). Reading 2: each one alone; ruled out because one plan read and one gate run serve them all cheaper.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2465: fm decide --cites 'user steer …' with no --check warns on stderr, naming --check and --revisited; with --check it says nothing — verify with `python3 plugin/tests/run.py test_judgment`
- [x] T-2475: fm night --print-timer suggests none of another command's flags; fm check --evidance still suggests --evidence — verify with `python3 plugin/tests/run.py test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2465: red test, then the refusal in fm decide
2. [x] T-2475: red test, then match flags of the typed subcommand only
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_steer_rule_without_a_check_warns_when_it_is_recorded test_judgment` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: SteerChecks 0s) / FAILED (1 classes: test_judgment.SteerChecks) [ran] [tree 9077ca27af69] (2026-11-01T17:47:53Z)
- `python3 plugin/tests/run.py -k test_a_steer_rule_without_a_check_warns_when_it_is_recorded test_judgment` → ✗ exit 1 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: SteerChecks 0s) / FAILED (1 classes: test_judgment.SteerChecks) (start tree + this task's tests) [ran] [tree 993920f2a20d] (2026-11-01T17:48:05Z)
- `python3 plugin/tests/run.py -k test_a_steer_rule_without_a_check_warns_when_it_is_recorded test_judgment` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: SteerChecks 0s) / OK [ran] [tree 993920f2a20d] (2026-11-01T17:48:05Z)
- (step 1) `python3 plugin/tests/run.py test_judgment` → ✗ exit 1 · Ran 58 tests in 11.6s (16 classes, 16 at a time; slowest: DoorPark 11s, DoorGate 7s, Followups 5s) / FAILED (1 classes: test_judgment.SteerChecks) [ran] [tree 993920f2a20d] (2026-11-01T17:48:18Z)
- (step 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 58 tests in 13.0s (16 classes, 16 at a time; slowest: DoorPark 13s, DoorGate 7s, Followups 5s) / OK [ran] [tree 954c015b94a5] (2026-11-01T17:48:54Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_mistyped_flag_is_matched_against_the_typed_commands_own_flags_only test_gate_friction` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Typos 0s) / FAILED (1 classes: test_gate_friction.Typos) [ran] [tree f0e22aadfeda] (2026-11-01T17:49:05Z)
- `python3 plugin/tests/run.py -k test_a_mistyped_flag_is_matched_against_the_typed_commands_own_flags_only test_gate_friction` → ✗ exit 1 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: Typos 0s) / FAILED (1 classes: test_gate_friction.Typos) (start tree + this task's tests) [ran] [tree 370fc2875d17] (2026-11-01T17:49:26Z)
- `python3 plugin/tests/run.py -k test_a_mistyped_flag_is_matched_against_the_typed_commands_own_flags_only test_gate_friction` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Typos 0s) / OK [ran] [tree 370fc2875d17] (2026-11-01T17:49:26Z)
- (step 2) `python3 plugin/tests/run.py test_gate_friction test_cli test_judgment` → exit 0 · Ran 212 tests in 25.4s (61 classes, 16 at a time; slowest: TaskLifecycle 25s, DoorPark 12s, StateViews 10s) / OK [ran] [tree 370fc2875d17] (2026-11-01T17:49:52Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 58 tests in 8.6s (16 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree 00f843f1f4e2] (2026-11-01T17:50:15Z)
- (ac 2) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 12 tests in 2.2s (2 classes, 16 at a time; slowest: Typos 2s, Flakes 1s) / OK [ran] [tree 00f843f1f4e2] (2026-11-01T17:50:17Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 58 tests in 8.2s (16 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree 00f843f1f4e2] (2026-11-01T17:55:54Z)
- (ac 2) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 12 tests in 2.2s (2 classes, 16 at a time; slowest: Typos 2s, Flakes 1s) / OK [ran] [tree 00f843f1f4e2] (2026-11-01T17:55:54Z)
- (audit intent) `main-thread lens pass over the two fmcli changes and their tests` → fm decide warns at record time when a user-steer rule has no --check, naming --check and --revisited (warn, not refuse: a checkless steer row is a state the doctor and sweep must still detect); a mistyped flag is matched against the typed command's own parser tree plus the root's [tree 00f843f1f4e2] (2026-11-01T17:55:54Z)
- (audit edge) `main-thread lens pass over the two fmcli changes and their tests` → -p PROJECT before the verb is skipped when finding the command; an unknown verb falls back to every flag, as before; a near-miss steer citation keeps its own warning [tree 00f843f1f4e2] (2026-11-01T17:55:54Z)
- (audit self) `main-thread lens pass over the two fmcli changes and their tests` → no findings [tree 00f843f1f4e2] (2026-11-01T17:55:54Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 00f843f1f4e2] (2026-11-01T17:57:00Z)
## Log
- 2026-11-01T17:47:17Z created
- 2026-11-01T17:47:21Z focused
- 2026-11-01T17:47:22Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T17:47:44Z steer(self): T-2465 warns instead of refusing: a steer row without a check is a valid state the doctor and sweep detect (20 tests record one on purpose); the failure was not seeing the gap at record time, which a warning naming --check and --revisited fixes
- 2026-11-01T17:47:45Z criterion 1 text: T-2465: fm decide --cites 'user steer …' with no --check exits non-zero and names --check; with --check it records → T-2465: fm decide --cites 'user steer …' with no --check warns on stderr, naming --check and --revisited; with --check it says nothing
- 2026-11-01T17:50:06Z scope: plugin/lib/fmcli.py (cmd_decide warning, _Parser.error flag scope), plugin/tests/test_judgment.py, plugin/tests/test_gate_friction.py, CHANGELOG.md
- 2026-11-01T17:56:29Z done
- 2026-11-01T17:56:32Z committed 71d9a8ab (4 files)
- 2026-11-01T17:57:00Z guard authorization added: publish
- 2026-11-01T18:01:32Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-2475 [FIX S, planned, 1 steps] A mistyped flag's 'did you mean' suggests only the typed command's own flags (fm night --print-timer suggested --print, which fm night d…
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
## Lessons
- Say a gap at the moment it's made: a warning at record time beats a doctor line later
## Plan gaps
- failed first: step 1 T-2465: red test, then the refusal in fm decide
- failed first: step 2 T-2475: red test, then match flags of the typed subcommand only
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmcli.py
- plugin/tests/test_gate_friction.py
- CHANGELOG.md
