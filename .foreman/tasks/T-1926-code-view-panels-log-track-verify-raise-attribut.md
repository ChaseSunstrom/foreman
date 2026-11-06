---
id: T-1926
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T06:34:51Z
updated: 2026-10-29T07:11:15Z
base: b0d49b3cec535e3003b5f5e8e1bb1406245d109d
base_tree: 8fd19550517a0f12be2d8845e54f6dd8b7eb665a
plan0_at: 2026-10-29T07:08:37Z
plan0_scope: []
verified: strong
---
# Code view panels draw non-str event fields instead of failing
## Raw request
> Code view panels log/track/verify raise AttributeError/TypeError on non-str event fields under Fuzz (only an error line renders); coerce fields at the panel edge
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fuzzed events never make a built-in panel fail — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Fuzz asserts no 'panel … failed' line (red), then coerce the fields where they enter (green)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui.Fuzz.test_any_event_stream_draws_at_any_size` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Fuzz 0s) / FAILED (1 classes) [ran] [tree 48293da2cd2c] (2026-10-29T07:09:31Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 10.4s (46 classes, 16 at a time; slowest: Command 10s, Fuzz 9s, Events 5s) / OK [ran] [tree 38bf26b93261] (2026-10-29T07:09:48Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 7.9s (46 classes, 16 at a time; slowest: Command 8s, Fuzz 7s, Extras 4s) / OK [ran] [tree ca7c48d13da8] (2026-10-29T07:10:39Z)
- `python3 plugin/tests/run.py test_code_tui.Fuzz` → ✗ exit 1 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Fuzz 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ca7c48d13da8] (2026-10-29T07:10:50Z)
- `python3 plugin/tests/run.py test_code_tui.Fuzz` → exit 0 · Ran 3 tests in 6.7s (1 classes, 16 at a time; slowest: Fuzz 6s) / OK [ran] [tree ca7c48d13da8] (2026-10-29T07:10:50Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 8.0s (46 classes, 16 at a time; slowest: Command 8s, Fuzz 7s, Extras 4s) / OK [ran] [tree ca7c48d13da8] (2026-10-29T07:11:03Z)
- (audit intent) `red fuzz assertion at seed 0, coercion at State.apply's entry so every handler and panel gets words; probe over 5000 seeds and all panels clean` → fuzzed text/cmd/action of any type draw; the panel no longer fails [tree ca7c48d13da8] (2026-10-29T07:11:03Z)
- (audit edge) `red fuzz assertion at seed 0, coercion at State.apply's entry so every handler and panel gets words; probe over 5000 seeds and all panels clean` → None becomes empty, lists and dicts their repr; 5000 seeds over every built-in panel draw without a failed line [tree ca7c48d13da8] (2026-10-29T07:11:03Z)
- (audit adversary) `red fuzz assertion at seed 0, coercion at State.apply's entry so every handler and panel gets words; probe over 5000 seeds and all panels clean` → extension handlers see the same coerced event; truthiness checks on error/closed unchanged [tree ca7c48d13da8] (2026-10-29T07:11:03Z)
- (audit self) `red fuzz assertion at seed 0, coercion at State.apply's entry so every handler and panel gets words; probe over 5000 seeds and all panels clean` → no findings [tree ca7c48d13da8] (2026-10-29T07:11:03Z)
## Log
- 2026-10-29T06:34:51Z created
- 2026-10-29T07:08:36Z planned from capture
- 2026-10-29T07:08:36Z focused
- 2026-10-29T07:11:13Z done
- 2026-10-29T07:11:15Z committed ecc55cd8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1850-review: Verdict: approve with nits.** `bench()` matches the data shape of the records. I found no crash from real `fm code bench` output. The three real …
- research T-1873-review: Approve with nits. The feature works as described, and the refactor of `cmd_scene` into `_builtin` keeps the existing behaviour. One MEDIUM findi…
- research T-1516-review: Verdict:** approve with nits. The two renderer fixes are sound in ASCII and plain CJK rows. The sweep is weaker than its changelog claims: it ski…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Lessons
- Fix where fields enter (State.apply), not in each panel that reads them
## Plan gaps
- failed first: step 1 Fuzz asserts no 'panel … failed' line (red), then coerce the fields where they enter (green)
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
