---
id: T-2883
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:45:46Z
updated: 2026-11-04T03:49:29Z
base: 453e829fc3219b06c5d4ed83fe9bc272ff01f551
base_tree: ed5c7871a42d0fb76fcc057d8c035d9f1b18613b
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T03:45:47Z
plan0_scope: []
verified: strong
---
# The drive's still-running line names how many it left out past three, instead of cutting silently
## Raw request
> The drive's still-running line names how many it left out past three, instead of cutting silently
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] five running shells: the drive's reason names three and '2 left out' — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: five shells running, the reason says 2 left out
2. [x] fix: the three drive lines use core.joinmore
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop.test_the_still_running_line_says_how_many_it_left_out` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 35564f8cd581] [world 2f1906870a] (2026-11-04T03:46:00Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Stop.test_the_still_running_line_says_how_many_it_left_out` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 66ebf8775f34] [world 2f1906870a] (2026-11-04T03:46:18Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 256 tests in 54.3s (31 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 32s, PreToolUse 26s) / OK [ran] [tree 66ebf8775f34] [world 2f1906870a] (2026-11-04T03:48:22Z)
- (audit edge) `red test then green; test_hooks and test_left_out pass` → with three or fewer running, joinmore prints them as before with no note; with zero the line is never reached (running is non-empty there) [tree 66ebf8775f34] (2026-11-04T03:48:22Z)
- (audit intent) `red test then green; test_hooks and test_left_out pass` → the reader of the drive's reason now sees how many it left out, so a fourth running builder can't read as dropped [tree 66ebf8775f34] (2026-11-04T03:48:22Z)
- (audit self) `red test then green; test_hooks and test_left_out pass` → no findings [tree 66ebf8775f34] (2026-11-04T03:48:22Z)
## Log
- 2026-11-04T03:45:46Z created
- 2026-11-04T03:45:46Z focused
- 2026-11-04T03:45:47Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T03:49:27Z done
- 2026-11-04T03:49:29Z committed af995fe7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2673 [FIX S, done, 3 steps] every list fm cuts at N says how many it left out and the flag that shows them: one helper in fmcore for the fmcli sites that cut silently
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- T-2676 [FIX S, done, 3 steps] every plugin/lib/fm*.py module that prints a cut list says how many it left out: test_left_out's scan covers all of them
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
- similar finished tasks took 2–3 steps
## Why not caught
the silent-cut scan exempted lines marked 'text for a model, not a screen'
## Lessons
- a cut list in text for a model misleads the model as much as a person: the 'not a list' exemption was wrong
## Plan gaps
- failed first: step 1 test: five shells running, the reason says 2 left out
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
