---
id: T-1922
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T05:59:31Z
updated: 2026-10-29T06:35:39Z
base: f236445b2c852debecc2aee4883320c224c42522
base_tree: ef93eea8b045968e525511da88bf640269d394ab
plan0_at: 2026-10-29T06:33:09Z
plan0_scope: []
verified: strong
---
# CI: test_code_tui.Fuzz killed (exit -9) on macOS 3.14 shard 2 at 6cbedd9b; 300 seeds x 6 s
## Raw request
> CI: test_code_tui.Fuzz killed (exit -9) on macOS 3.14 shard 2 at 6cbedd9b; 300 seeds x 6 sizes x 3 renders may pass the 480 s class cap on a slow runner
## Interpretation
test_code_tui Fuzz was killed on macOS CI (exit -9, no output): fmcodetui._time pads a bar with spaces sized by an unclamped start, so a phase stamped before the run asks for gigabytes
## Assumptions (confidence)
## Acceptance criteria
- [x] A phase stamped before the run keeps every time-chart row within the width — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Clamp the bar start at 0 in _time; one test with an early-stamped step checks every row stays within the width
## Risks and rollback
## Execution prompt
## Steps
1. [x] Clamp the time-chart bar start; test red then green
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 237 tests in 17.4s (46 classes, 16 at a time; slowest: Core 16s, Fuzz 8s, Command 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ec0f0f869970] (2026-10-29T06:33:57Z)
- `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 13.3s (46 classes, 16 at a time; slowest: Command 13s, Fuzz 11s, Events 5s) / OK [ran] [tree ec0f0f869970] (2026-10-29T06:33:57Z)
- `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 237 tests in 22.9s (46 classes, 16 at a time; slowest: Core 21s, Fuzz 13s, Command 13s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ec0f0f869970] (2026-10-29T06:34:37Z)
- `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 13.0s (46 classes, 16 at a time; slowest: Command 13s, Fuzz 11s, Events 5s) / OK [ran] [tree ec0f0f869970] (2026-10-29T06:34:37Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 13.5s (46 classes, 16 at a time; slowest: Command 13s, Fuzz 12s, Events 5s) / OK [ran] [tree ec38b0d99d96] (2026-10-29T06:35:05Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 237 tests in 13.2s (46 classes, 16 at a time; slowest: Command 13s, Fuzz 11s, Events 5s) / OK [ran] [tree ec38b0d99d96] (2026-10-29T06:35:19Z)
- (audit intent) `Self-review: the only producer of the start is _time; checked the end clamp already holds; ran Fuzz under a memory trace.` → an early-stamped phase draws within the width [tree ec38b0d99d96] (2026-10-29T06:35:19Z)
- (audit adversary) `Self-review: the only producer of the start is _time; checked the end clamp already holds; ran Fuzz under a memory trace.` → a start a million seconds early stays at column 0 [tree ec38b0d99d96] (2026-10-29T06:35:20Z)
- (audit edge) `Self-review: the only producer of the start is _time; checked the end clamp already holds; ran Fuzz under a memory trace.` → a zero-length run still renders [tree ec38b0d99d96] (2026-10-29T06:35:20Z)
- (audit self) `Self-review: the only producer of the start is _time; checked the end clamp already holds; ran Fuzz under a memory trace.` → no findings [tree ec38b0d99d96] (2026-10-29T06:35:20Z)
## Log
- 2026-10-29T05:59:31Z created
- 2026-10-29T05:59:34Z set type=FIX
- 2026-10-29T06:00:22Z local: Fuzz 3 tests in 7.5 s (python 3.14.8, linux) vs 480 s cap: not slowness, likely a hang on macOS/3.14; CI logs need gh auth (403); annotations only say exit -9. Check if run.py's T-1808 stack dump reaches annotations; next CI run may repeat
- 2026-10-29T06:33:08Z set type=FIX, tier=S
- 2026-10-29T06:33:08Z planned: it has criteria and steps
- 2026-10-29T06:33:09Z focused
- 2026-10-29T06:35:36Z done
- 2026-10-29T06:35:39Z committed 3a55d165 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-1911 [FIX S, done, 3 steps] MacOS CI shard 2 exits 1 with no ::error annotation (only run.py's notice), so its failure — lesson: A runner's failure report must name wh…
- T-1828 [FIX M, done, 2 steps] FIX: macOS CI job (non-blocking) fails at 3f2538fc: suite hits its 1980 s deadline (test_c — lesson: macOS ptys drop unread output when the…
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
## Why not caught
Fuzz events kept timestamps in order, so no bar ever started before the run; Linux raised a MemoryError the panel caught, while macOS committed the memory and was killed.
## Lessons
- Clamp both ends of any computed width before padding with it.
## Files touched
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py
- CHANGELOG.md
