---
id: T-1723
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/tests/test_settings.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T03:25:42Z
updated: 2026-10-23T03:41:07Z
base: cd6284395e05bc3267694e38d4b232c5d58a4f87
base_tree: 11069d6e80d149d341098f756610e1041c600e73
plan0_at: 2026-10-23T03:37:12Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/tests/test_settings.py, CHANGELOG.md]
verified: strong
---
# Fmsettings.set_key accepts an unknown key silently; only cmd_settings and apply check firs
## Raw request
> fmsettings.set_key accepts an unknown key silently; only cmd_settings and apply check first, so fm code's :set may fail without a word
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] set_key on an unknown key returns a refusal naming it, so fm code's :set and fm settings serve say so — verify with `python3 plugin/tests/run.py test_settings.Unknown`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: set_key('no.such', 1) refuses
2. [x] refuse in set_key when find() has nothing
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_settings.Unknown` → ✗ exit 1 · Ran 1 tests in 6.5s (1 classes, 16 at a time; slowest: Unknown 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 774bcf6458b9] (2026-10-23T03:37:53Z)
- `python3 plugin/tests/run.py test_settings.Unknown` → ✗ exit 1 · Ran 1 tests in 3.1s (1 classes, 16 at a time; slowest: Unknown 1s) / FAILED (1 classes) [ran] [tree 774bcf6458b9] (2026-10-23T03:37:53Z)
- `python3 plugin/tests/run.py test_settings.Unknown` → ✗ exit 1 · Ran 1 tests in 6.2s (1 classes, 16 at a time; slowest: Unknown 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f273788f7fb3] (2026-10-23T03:38:22Z)
- `python3 plugin/tests/run.py test_settings.Unknown` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: Unknown 0s) / OK [ran] [tree f273788f7fb3] (2026-10-23T03:38:22Z)
- (step 1) `python3 plugin/tests/run.py test_settings.Unknown` → exit 0 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: Unknown 1s) / OK [ran] [tree f273788f7fb3] (2026-10-23T03:38:26Z)
- (step 2) `python3 plugin/tests/run.py test_settings test_settings_serve test_settings_power` → exit 0 · Ran 103 tests in 21.9s (18 classes, 16 at a time; slowest: Command 20s, Rules 14s, Serve 11s) / OK [ran] [tree f273788f7fb3] (2026-10-23T03:38:52Z)
- (ac 1) `python3 plugin/tests/run.py test_settings.Unknown` → exit 0 · Ran 1 tests in 3.0s (1 classes, 16 at a time; slowest: Unknown 0s) / OK [ran] [tree f273788f7fb3] (2026-10-23T03:39:00Z)
- (ac 1) `python3 plugin/tests/run.py test_settings.Unknown` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: Unknown 0s) / OK [ran] [tree 040218261ea2] (2026-10-23T03:39:23Z)
- (audit edge) `self: one guard in _set_key, the function every caller routes through (cmd_settings and apply check first and keep their own messages; fm code's _settings_write and fm settings serve show refused lines already); the message matches cmd_settings' own` → a known key on a surface that lacks it is refused naming the surface [tree 040218261ea2] (2026-10-23T03:39:23Z)
- (audit self) `self: one guard in _set_key, the function every caller routes through (cmd_settings and apply check first and keep their own messages; fm code's _settings_write and fm settings serve show refused lines already); the message matches cmd_settings' own` → no findings [tree 040218261ea2] (2026-10-23T03:39:23Z)
## Log
- 2026-10-23T03:25:42Z created
- 2026-10-23T03:32:37Z set scope=['plugin/lib/fmsettings.py', 'plugin/tests/test_settings.py', 'CHANGELOG.md']
- 2026-10-23T03:37:07Z focused
- 2026-10-23T03:40:58Z done
- 2026-10-23T03:41:07Z committed e30400bd (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research T-1572-review: Verdict:** approve with nits. The screen cannot write a value the schema rejects, and it cannot skip the guard or lock path, except in one narrow…
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
- similar finished tasks took 2–6 steps
- likely tests for the scope: plugin/tests/test_settings.py
## Why not caught
only the CLI path had an unknown-key test, and it checks before calling set_key
## Lessons
- Put the refusal in the shared setter, not in each caller
## Files touched
- plugin/tests/test_settings.py
- plugin/lib/fmsettings.py
- CHANGELOG.md
