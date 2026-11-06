---
id: T-2517
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-01T23:30:27Z
updated: 2026-11-02T00:26:33Z
base: 32b1a015035f1adeeb6d76ffe1990dac52f31e49
base_tree: 013df9f6be3cbca5e9d8058780c887e71fcf5c96
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T00:18:22Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# fm lane brief says when the task's own content passes 4k chars, with fm lane stats' numbers
## Raw request
> fm lane brief says when a task's own content (criteria, approach, interpretation, steps) passes ~4k chars: in Oct 21-31 such briefs landed 26/46 (57%) vs 230/237 (97%); suggest splitting it or keeping it in the main thread, with the numbers from fm lane stats; never refuse
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief, for a task whose own sections (raw request, interpretation, approach, criteria, steps) pass 4000 chars, prints one line naming its size and the landing rates of briefs up to 8k and over 8k from fm lane stats, and suggests splitting it or keeping it in the main thread; it still writes the brief (never refuses); a smaller task prints nothing new — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a task with a 5k-char Approach gets the line on fm lane brief (and the brief is still written); a plain S task doesn't
2. [x] fmlanes.builder_brief: measure the task's own sections, print the advisory with fmlanes.stats(p)'s rows; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_big_task_s_brief_says_so_and_is_still_written` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Lanes 0s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree dc6130c3d591] [world 2f1906870a] (2026-11-02T00:18:27Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -1` → exit 0 · OK [ran] [tree 2d0eee682d96] [world 2f1906870a] (2026-11-02T00:18:59Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_big_task_s_brief_says_so_and_is_still_written` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Lanes 0s) / OK [ran] [tree 2d0eee682d96] [world 2f1906870a] (2026-11-02T00:19:03Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 139 tests in 21.9s (12 classes, 16 at a time; slowest: LaneRecovery 22s, Lanes 17s, RaceEvidence 10s) / OK [ran] [tree 2d0eee682d96] [world 2f1906870a] (2026-11-02T00:19:25Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 139 tests in 21.4s (12 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 16s, RaceEvidence 10s) / OK [ran] [tree 80b1a6446b24] [world 2f1906870a] (2026-11-02T00:25:54Z)
- (audit edge) `self-review: the advisory measures only the task's own sections (raw request, interpretation, approach, criteria, steps), goes into the warnings fm lane brief already prints, quotes fm lane stats' landed/briefs for up to 8k and longer, and never stops the brief (it is written before; the test checks the file)` → a small task prints nothing new; no lane history yet says 0 of 0; the brief file exists either way [tree 80b1a6446b24] (2026-11-02T00:25:54Z)
- (audit self) `self-review: the advisory measures only the task's own sections (raw request, interpretation, approach, criteria, steps), goes into the warnings fm lane brief already prints, quotes fm lane stats' landed/briefs for up to 8k and longer, and never stops the brief (it is written before; the test checks the file)` → no findings [tree 80b1a6446b24] (2026-11-02T00:25:54Z)
## Log
- 2026-11-01T23:30:27Z created
- 2026-11-02T00:00:37Z planned from capture
- 2026-11-02T00:18:21Z focused
- 2026-11-02T00:18:22Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T00:26:30Z done
- 2026-11-02T00:26:33Z committed 86738884 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2516 [PERFORMANCE S, dropped, 3 steps] Trim the builder brief's contract back under 3.5k chars (long briefs land 56% vs 97%)
- T-2340 [FEATURE M, done, 3 steps] L plans race their design (Mission 5, #2): an L task under the race bar gets one throwaway S spike per top option, built by builder lan…
- T-0216 [FEATURE S, done, 1 steps] fm audit prep --split: up to three parallel fresh-context reviewer briefs by lens group; suggested for big L diffs
- decision 2026-10-31: [revisited: Parallel Missions 5-8] [check: python3 plugin/tests/run.py test_lanes] Parallel Missions 5-8 still holds: an L stays in the main thread,…
- similar finished tasks took 1–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lanes.py
## Lessons
- Advise at the moment of choice with the measured numbers, and leave the choice open
## Plan gaps
- failed first: step 1 red test: a task with a 5k-char Approach gets the line on fm lane brief (and the brief is still wri…
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
