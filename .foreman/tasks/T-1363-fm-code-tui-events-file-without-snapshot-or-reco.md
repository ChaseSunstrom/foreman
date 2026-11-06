---
id: T-1363
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T04:21:11Z
updated: 2026-10-21T06:44:41Z
base: f84e7013fa6eed26d2971cc6042991382bdf9b72
base_tree: 11459c0f88d74a7c72fee8bc6ce339dd0f226e60
plan0_at: 2026-10-21T06:39:24Z
plan0_scope: []
verified: strong
---
# fm code tui --events FILE alone replays the run: on the screen in a terminal, as plain lines otherwise
## Raw request
> fm code tui --events FILE without --snapshot or --record silently ignores the file: it should replay it on the screen (or refuse, saying how to replay)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code tui --plain --events FILE (or with no terminal) prints the run's Activity lines and exits 0 for a closed run, 1 otherwise; an unreadable FILE says so and exits 2 — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] on a terminal, fm code tui --events FILE opens the screen on that run (App.replay), as h's Enter does — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: --plain --events prints the run; a missing file exits 2
2. [x] main(): --events without --snapshot/--record replays (screen or plain)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 85 tests in 14.4s (13 classes, 16 at a time; slowest: Fuzz 14s, Command 9s, Events 7s) / FAILED (1 classes) [ran] [tree 60b800a6525b] (2026-10-21T06:39:54Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error" | head` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree a3428712b729] (2026-10-21T06:40:18Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error" | head` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree a3428712b729] (2026-10-21T06:40:18Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 85 tests in 14.1s (13 classes, 16 at a time; slowest: Fuzz 14s, Command 9s, Events 6s) / OK [ran] [tree b289da310b83] (2026-10-21T06:40:38Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 85 tests in 29.9s (13 classes, 16 at a time; slowest: Fuzz 29s, Command 16s, Events 11s) / OK [ran] [tree 8c1dfe12d1b6] (2026-10-21T06:41:18Z)
- `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 85 tests in 36.2s (13 classes, 16 at a time; slowest: Fuzz 32s, Command 16s, Events 13s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8c1dfe12d1b6] (2026-10-21T06:42:11Z)
- `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 85 tests in 14.3s (13 classes, 16 at a time; slowest: Fuzz 14s, Command 10s, Events 7s) / OK [ran] [tree 8c1dfe12d1b6] (2026-10-21T06:42:11Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 85 tests in 23.8s (13 classes, 16 at a time; slowest: Fuzz 23s, Command 10s, Events 7s) / OK [ran] [tree 8c1dfe12d1b6] (2026-10-21T06:42:36Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 85 tests in 23.8s (13 classes, 16 at a time; slowest: Fuzz 23s, Command 10s, Events 7s) / OK [ran] [tree 8c1dfe12d1b6] (2026-10-21T06:42:36Z)
- (audit edge) `self: read the diff; --events alone goes to replay_file before any project lookup, so it works anywhere; plain prints entry_text (control characters already stripped there)` → a missing file exits 2 naming it; malformed lines are skipped by App.replay; the screen path (a terminal) reuses App.replay, the same code h's Enter runs, not separately tested in a pty [tree 8c1dfe12d1b6] (2026-10-21T06:42:36Z)
- (audit self) `self: read the diff; --events alone goes to replay_file before any project lookup, so it works anywhere; plain prints entry_text (control characters already stripped there)` → no findings [tree 8c1dfe12d1b6] (2026-10-21T06:42:36Z)
## Log
- 2026-10-21T04:21:11Z created
- 2026-10-21T06:12:47Z planned from capture
- 2026-10-21T06:39:23Z focused
- 2026-10-21T06:41:18Z scope: CHANGELOG.md — its line
- 2026-10-21T06:44:38Z done
- 2026-10-21T06:44:41Z committed b640405d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1300 [FEATURE L, done, 7 steps] Foreman Code TUI in motion: a truecolor renderer, eased animation (pulse, spinner, travelling light, rolling counters, growing bars, fl…
- research brainstorm-20261020-tui: Method.** I read all of ideas.md (about 560 distinct titles; near-duplicates are merged with "/"). I grepped fmcodetui.py and fmcode.py…
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
- similar past tasks were L: consider --tier L
## Lessons
- A flag that only means something with another flag should do the obvious thing alone, or refuse; silently ignoring it reads as broken
## Plan gaps
- failed first: step 1 Failing tests: --plain --events prints the run; a missing file exits 2
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
