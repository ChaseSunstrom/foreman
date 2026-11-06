---
id: T-3356
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_steer.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:39:06Z
updated: 2026-11-06T05:40:52Z
base: 68960f03fce20d7ff138fad44a53d715428ce15e
base_tree: 8d0a6cbf2668cf5639f89f49df2cff920a543a53
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T05:39:56Z
plan0_scope: [plugin/tests/test_steer.py, CHANGELOG.md]
verified: ok
unproven: [meaning]
---
# Steer test waits for its background decision
## Raw request
> test_steer.Live.test_a_steer_is_expanded_in_the_background_filed_and_a_low_score_asks_for_a_read races its background expansion: it waits for the filed task, then asserts the decision is already in 'decide --review' (test_steer.py:156); under load the decision lands later, so the ship's full suite failed and nothing was pushed (2026-11-06). Wait for the decision with the same wait_for helper
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the test waits for the decision with wait_for instead of asserting it at once; test_steer passes — verify with `python3 plugin/tests/run.py test_steer`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] wait_for the decision
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_steer` → exit 0 · Ran 24 tests in 3.6s (9 jobs, 16 at a time; slowest: Veto 3s, Court 3s, Live 2s) / OK [ran] [tree 114436f06056] [world 2f1906870a] (2026-11-06T05:40:08Z)
- (audit self) `one assertion became a poll on the same condition with the helper the test already uses for the task; same claim, now tolerant of the background write's timing` → no findings [tree 114436f06056] (2026-11-06T05:40:09Z)
- (ac 1) `python3 plugin/tests/run.py test_steer` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T05:40:08Z [ran] [tree 114436f06056] [world 2f1906870a] (2026-11-06T05:40:15Z)
- (audit self) `self audit after the last change` → no findings [tree 114436f06056] (2026-11-06T05:40:15Z)
## Log
- 2026-11-06T05:39:06Z created
- 2026-11-06T05:39:52Z planned from capture
- 2026-11-06T05:39:53Z focused
- 2026-11-06T05:39:56Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T05:40:48Z done
- 2026-11-06T05:40:52Z committed 00b285292 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2012 [FEATURE M, done, 5 steps] fm ship --task ships a closed task, the away line on a returning prompt, playbook did-you-mean, one suite wait, the loo… — lesson: A co…
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-2605 [FIX S, done, 2 steps] The self-change gate's loaded wall-time check compares medians (p50), so a hook that waits is caught even when load inflates p95 — lesson: …
- decision 2026-11-02: [revisited: steer-expansion exam. From a user's raw words] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: python3 plugin/tes…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Regression test
none: a race that shows only under host load; the fix replaces an immediate assertion with the file's existing wait_for poll, and test_steer passes
## Lessons
- A test of background work must poll for every effect it asserts, not just the first one.
## Files touched
- plugin/tests/test_steer.py
