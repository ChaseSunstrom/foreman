---
id: T-2738
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:36:22Z
updated: 2026-11-03T00:38:26Z
base: fc60bb351a236ab7e8ad5a2692bce16d2ceda040
base_tree: 275e5580cca900615614a272ab2210931b2f69aa
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T00:36:23Z
plan0_scope: []
verified: strong
---
# the blocked-pile line's unblock command joins ids with commas, the form fm task unblock takes (T-2683 printed them space-separated, which the command refuses)
## Raw request
> the blocked-pile line's unblock command joins ids with commas, the form fm task unblock takes (T-2683 printed them space-separated, which the command refuses)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the freed group's command is 'fm task unblock T-6,T-7' and that form runs — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the comma join
## Resume here
## Docs impact
none: the CHANGELOG's T-2683 line names the action, not its syntax
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_foresight test_left_out` → exit 0 · Ran 39 tests in 9.0s (9 classes, 16 at a time; slowest: PredictionBook 9s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:37:12Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_left_out` → exit 0 · Ran 39 tests in 9.4s (9 classes, 16 at a time; slowest: PredictionBook 9s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:37:22Z)
- `python3 plugin/tests/run.py test_foresight` → ✗ exit 1 · Ran 36 tests in 9.8s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / FAILED (1 classes: test_foresight.Foresight) (start tree + this task's tests) [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:37:41Z)
- `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 36 tests in 8.9s (8 classes, 16 at a time; slowest: PredictionBook 9s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:37:41Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:37:41Z [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:37:43Z)
- `python3 plugin/tests/run.py test_foresight test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:37:22Z [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:37:43Z)
- (audit edge) `the freed group's command is now a comma list (T-6,T-7), the form fm task unblock parses (_TASK_IDS); past six ids the rest are counted after the command, so what's printed still runs; ran that form on the real pile: 4 of 4 unblocked` → one freed task alone never groups (a group of one adds nothing), so a single-id command isn't printed [tree 969e58d66189] (2026-11-03T00:37:43Z)
- (audit self) `the freed group's command is now a comma list (T-6,T-7), the form fm task unblock parses (_TASK_IDS); past six ids the rest are counted after the command, so what's printed still runs; ran that form on the real pile: 4 of 4 unblocked` → no findings [tree 969e58d66189] (2026-11-03T00:37:43Z)
## Log
- 2026-11-03T00:36:22Z created
- 2026-11-03T00:36:22Z focused
- 2026-11-03T00:36:23Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T00:37:02Z scope: plugin/tests/test_foresight.py
- 2026-11-03T00:38:21Z done
- 2026-11-03T00:38:26Z committed 679818a7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1877 [FEATURE M, done, 3 steps] Task ids accept ranges and lists (T-0003..T-0007, T-1,T-2) on the bulk verbs where acting — lesson: A bulk loop over briefs must catch …
- T-1924 [PERFORMANCE M, done, 1 steps] Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_ — lesson: Tails after a substitution wer…
- research T-1585-rereview: Changes needed.** I had no shell tool, so I ran nothing and traced the code instead. Each finding below is a trace, not a measured result.
- decision 2026-11-02: Recommendation: Mission 7 builds four anticipation gaps where Foreman computes what the user will need but it never reaches them (the booked next-re…
## Why not caught
T-2683's test asserted the line's text, never ran the command it suggests
## Lessons
- A line that prints a command must be tested by running that command, not by matching its text
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
