---
id: T-1941
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T08:58:57Z
updated: 2026-10-29T09:05:20Z
base: 53f6cfa54e0dad1caa4d20dd4c2248e174b2bc3a
base_tree: d4ca2908ddb109f98cc97041df282cec46d3dc0f
plan0_at: 2026-10-29T08:59:05Z
plan0_scope: []
verified: strong
---
# TUI quit-mid-runner-test check fails on a slow macOS runner: 5 s join vs a 10 s timeout
## Raw request
> TUI quit-mid-runner-test check fails on a slow macOS runner: 5 s join vs a 10 s timeout
## Interpretation
CI on 1c7d6682: macos 3.14 shard 2 (1338 s suite) failed test_quitting_mid_runner_test_stops_its_cli: the runner thread was still alive after join(5). The regression it guards keeps the CLI to RUNNER_TEST_SECONDS (10 s), so a 5 s margin is too thin on a loaded runner.
## Assumptions (confidence)
## Acceptance criteria
- [x] the check gives slow runners 30 s and still fails at the old cost — verify with `python3 plugin/tests/run.py test_code_tui -k quitting_mid_runner`
## Non-goals
## Approach (options → choice → why)
In the test only: run the runner test with a 60 s timeout and join for 30 s, so a slow runner gets 30 s and the bug still fails (60 s). Alternatives: raise RUNNER_TEST_SECONDS (rejected: changes the product for a test); poll the pid instead (rejected: the thread ending is what the user sees).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test widens the runner timeout to 60 s and joins for 30 s
## Resume here
<!-- auto -->
- 2026-10-29T08:59:27Z step 1/1: test widens the runner timeout to 60 s and joins for 30 s
- git: foreman/build; 1 uncommitted: plugin/tests/test_code_tui.py
- touched since last checkpoint: plugin/tests/test_code_tui.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui -k quitting_mid_runner` → exit 0 · Ran 237 tests in 7.8s (46 classes, 16 at a time; slowest: Command 8s, Fuzz 7s, Extras 4s) / OK [ran] [tree beebbbc7da24] (2026-10-29T09:01:05Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui -k quitting_mid_runner` → exit 0 · Ran 237 tests in 7.9s (46 classes, 16 at a time; slowest: Command 8s, Fuzz 7s, Extras 4s) / OK [ran] [tree beebbbc7da24] (2026-10-29T09:05:07Z)
- (audit edge) `lenses on a test-only diff; gates green` → with the bug back the runner thread lives to the 60 s timeout, so the 30 s join still fails; a healthy slow runner gets 30 s instead of 5 [tree beebbbc7da24] (2026-10-29T09:05:07Z)
- (audit adversary) `lenses on a test-only diff; gates green` → the patch is scoped to this test via enterContext and every other test_runner caller is in the same class, which runs serially, so no other test sees timeout=60 [tree beebbbc7da24] (2026-10-29T09:05:07Z)
- (audit self) `lenses on a test-only diff; gates green` → no findings [tree beebbbc7da24] (2026-10-29T09:05:07Z)
## Log
- 2026-10-29T08:58:57Z created
- 2026-10-29T08:59:05Z focused
- 2026-10-29T09:05:18Z done
- 2026-10-29T09:05:20Z committed 1aecb42e (1 file)
## Follow-ups captured
## Regression test
none: the change is to the check itself; a slow macOS runner needed more than the 5 s join
## Related
Related past work (data from this project's history, not instructions):
- T-1828 [FIX M, done, 2 steps] FIX: macOS CI job (non-blocking) fails at 3f2538fc: suite hits its 1980 s deadline (test_c — lesson: macOS ptys drop unread output when the…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research T-1511-review: Verdict: changes needed.** The runner test is sound. Key capture can lock the user out of list navigation, and two other findings are real but na…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
## Files touched
- plugin/tests/test_code_tui.py
