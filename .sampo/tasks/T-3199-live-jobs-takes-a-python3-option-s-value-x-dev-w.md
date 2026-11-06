---
id: T-3199
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/live.py, plugin/tests/test_live.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T11:55:52Z
updated: 2026-11-05T21:08:34Z
base: 88050b92964c3febdcb6f21f3100ca7f28cc03e3
base_tree: 335adfee808746b8fa1cbc78000696d4d689fa13
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T21:04:40Z
plan0_scope: [plugin/lib/sampo/live.py, plugin/tests/test_live.py, CHANGELOG.md]
verified: strong
---
# live.jobs takes a python3 option's value (-X dev, -W x) for the program, so those jobs…
## Raw request
> live.jobs takes a python3 option's value (-X dev, -W x) for the program, so those jobs are missed (T-3044 builder)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 options that take a value (-X dev, -W x, --check-hash-based-pycs mode) and -m MODULE are read past; -c CODE names no program — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing cases in the job-kind table
2. [x] jobs() skips option values when finding the program
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live` → ✗ exit 1 · Ran 95 tests in 25.9s (80 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 25s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 7efcacb99531] [world 2f1906870a] (2026-11-05T21:05:40Z)
- (step 2) `python3 plugin/tests/run.py test_live test_progress` → exit 0 · Ran 110 tests in 24.0s (82 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 23s, Page.test_the_network_view_draws_three_columns_and_pulses [ran] [tree 0917f5feee79] [world 2f1906870a] (2026-11-05T21:06:56Z)
- `python3 plugin/tests/run.py test_live.Snapshot` → ✗ exit 1 · Ran 19 tests in 8.9s (1 jobs, 16 at a time; slowest: Snapshot 6s) / FAILED (1 classes: test_live.Snapshot) (start tree + this task's tests) [ran] [tree 2e9de6aaadaa] [world 2f1906870a] (2026-11-05T21:07:08Z)
- `python3 plugin/tests/run.py test_live.Snapshot` → exit 0 · Ran 19 tests in 1.7s (19 jobs, 16 at a time; slowest: Snapshot.test_complete_and_embed_log_their_calls_even_when_the_call_fails 1s, Snapshot.test_every_field_of_the_contract_is_there_and_json 1s, Snap [ran] [tree 2e9de6aaadaa] [world 2f1906870a] (2026-11-05T21:07:08Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 95 tests in 26.7s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 26s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree 2e9de6aaadaa] [world 2f1906870a] (2026-11-05T21:07:37Z)
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 95 tests in 26.7s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 26s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree 2e9de6aaadaa] [world 2f1906870a] (2026-11-05T21:07:37Z)
- (audit intent) `self: _program_at walks python3's words: -c stops (no program), -m names the module, -X/-W/--check-hash-based-pycs skip their value, any other dash word is a flag` → python3 -X dev plugin/bin/sampo moons grow shows as a grow job [tree 2e9de6aaadaa] (2026-11-05T21:07:37Z)
- (audit edge) `self: _program_at walks python3's words: -c stops (no program), -m names the module, -X/-W/--check-hash-based-pycs skip their value, any other dash word is a flag` → -Xdev (joined) is one flag; -m with nothing after names nothing [tree 2e9de6aaadaa] (2026-11-05T21:07:37Z)
- (audit self) `self: _program_at walks python3's words: -c stops (no program), -m names the module, -X/-W/--check-hash-based-pycs skip their value, any other dash word is a flag` → no findings [tree 2e9de6aaadaa] (2026-11-05T21:07:37Z)
## Log
- 2026-11-05T11:55:52Z created
- 2026-11-05T21:04:36Z planned: it has criteria and steps
- 2026-11-05T21:04:37Z set scope=['plugin/lib/sampo/live.py', 'plugin/tests/test_live.py', 'CHANGELOG.md']
- 2026-11-05T21:04:37Z focused
- 2026-11-05T21:04:40Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T21:05:47Z focused
- 2026-11-05T21:08:30Z done
- 2026-11-05T21:08:34Z committed a4f92e3e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3083 [FEATURE M, done, 3 steps] Job progress, the data half: a per-pid progress file Sampo's long loops write, jeff-train's events read through JEFF_EVENTS, and live.p…
- research T-2978-minting: `sampo exam gen --from-repo PATH [--only GLOB] [--test-cmd CMD] --n N --seed S`: [stale: plugin/lib/sampo/lake.py, plugin/tests/run.py changed s…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-02: [check: python3 plugin/tests/run.py test_genesis.GenerationReview] An option a session repeats takes every value, and each is checked before any app…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_live.py
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
the job table had no python options with values; it does now
## Lessons
- finding a program in an interpreter's argv must know which options take a value
## Plan gaps
- failed first: step 1 failing cases in the job-kind table
## Files touched
- plugin/tests/test_live.py
- plugin/lib/sampo/live.py
- CHANGELOG.md
