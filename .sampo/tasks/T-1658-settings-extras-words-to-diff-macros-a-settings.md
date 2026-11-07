---
id: T-1658
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_settings_extras.py, MASTER.md, CHANGELOG.md, plugin/lib/fmideas.py]
depends_on: []
source: followup
created: 2026-10-22T20:58:49Z
updated: 2026-10-28T21:33:28Z
group: settings and control room extras
base: b3142bbcf25439034c4207c64dcc01a1879351ee
base_tree: 2fda4eafc6525a6a29eaff4bc0abd660bc2f502f
plan0_at: 2026-10-28T21:05:23Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_settings_extras.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Settings extras: log, macro, duel, replay (what-breaks), words-to-diff, undo that adapts
## Raw request
> Settings extras: words-to-diff, macros, a settings changelog, duel, replay, what-breaks simulator, undo that adapts (from T-1544; waits: after profiles and rules; words-to-diff needs the fake-model harness)
## Interpretation
T-1544's leftover settings ideas as fm settings actions, each usable from Claude Code (fm verbs) and fm code; a model is optional: words needs claude on PATH and says so when missing
## Assumptions (confidence)
## Acceptance criteria
- [x] fm settings log lists every set, import, macro, words and undo with old → new, filtered by KEY, --json — verify with `python3 plugin/tests/run.py test_settings_extras`
- [x] fm settings macro NAME --set K=V saves (keys checked), macro NAME runs as one undo step, macro lists — verify with `python3 plugin/tests/run.py test_settings_extras`
- [x] fm settings duel A B draws the same run under two tui.toml files side by side and names the keys they set differently — verify with `python3 plugin/tests/run.py test_settings_extras`
- [x] fm settings replay replays past runs and a stress burst at three sizes, timing frames; --set K=V does it with the change unwritten and names what breaks (exit 1) — verify with `python3 plugin/tests/run.py test_settings_extras`
- [x] fm settings words TEXT asks claude -p for a settings change, checks each key, shows old → new, --apply sets it as one undo step; no claude on PATH exits 2 naming it; changes undone twice are never proposed again — verify with `python3 plugin/tests/run.py test_settings_extras`
- [x] fm settings undo names a key undone 3+ times and where its changes came from — verify with `python3 plugin/tests/run.py test_settings_extras`
## Non-goals
## Approach (options → choice → why)
options: a new fmsettingsx module; each idea as an fm settings action in fmsettings; only some ideas → choice: six actions in fmsettings (log, macro, duel, replay, words) plus undo hints, one changelog.jsonl feeding log, undo hints and words → why: they share the history, set_key/_recorded and check_render already there; a module split adds imports and nothing else
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first (red)
2. [x] changelog, log and undo hints
3. [x] macro, duel, replay
4. [x] words
5. [x] docs, gates, review
## Resume here
<!-- auto -->
- 2026-10-28T21:31:13Z step 5/5: docs, gates, review
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmideas.py, plugin/lib/fmsettings.py, plugin/tests/test_settings_extras.py
- touched since last checkpoint: plugin/lib/fmideas.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/test_settings_room.py
- failures met: assertionerror: 'timed out' not found in "the ideas child didn't answer in 0 s (is `claud…; typeerror: startswith first arg must be bytes or a tuple of bytes, not str
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_extras` → ✗ exit 1 · Ran 10 tests in 0.9s (5 classes, 16 at a time; slowest: Macro 1s, Words 0s, Log 0s) / FAILED (5 classes) [ran] [tree b83f76e3849b] (2026-10-28T21:08:35Z)
- (step 2) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 10 tests in 1.2s (5 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Words 1s) / OK [ran] [tree 6ba49f70b4b5] (2026-10-28T21:15:43Z)
- (step 3) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 10 tests in 1.3s (5 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Words 1s) / OK [ran] [tree 6ba49f70b4b5] (2026-10-28T21:15:45Z)
- (step 4) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 10 tests in 1.2s (5 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Words 1s) / OK [ran] [tree 6ba49f70b4b5] (2026-10-28T21:15:46Z)
- (step 5) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 21:31 UTC); cached (fm check --fresh reruns) [ran] [tree 3100c4930d75] (2026-10-28T21:32:53Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 17 tests in 1.2s (6 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Review 1s) / OK [ran] [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (ac 2) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 17 tests in 1.2s (6 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Review 1s) / OK [ran] [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (ac 3) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 17 tests in 1.2s (6 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Review 1s) / OK [ran] [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (ac 4) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 17 tests in 1.2s (6 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Review 1s) / OK [ran] [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (ac 5) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 17 tests in 1.2s (6 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Review 1s) / OK [ran] [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (ac 6) `python3 plugin/tests/run.py test_settings_extras` → exit 0 · Ran 17 tests in 1.2s (6 classes, 16 at a time; slowest: Replay 1s, Macro 1s, Review 1s) / OK [ran] [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (audit intent) `one fm-reviewer pass; 7 findings verified and fixed test-first` → log, macro, duel, replay, words and adaptive undo each do what the brief asked; tests name each [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (audit adversary) `one fm-reviewer pass; 7 findings verified and fixed test-first` → model replies and file text go through _plain/_safe; a timeout never prints the argv; replay writes nothing [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (audit edge) `one fm-reviewer pass; 7 findings verified and fixed test-first` → invalid TOML in duel refused; changelog capped at CHANGELOG_MAX; events file capped at EVENTS_MAX [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (audit operator) `one fm-reviewer pass; 7 findings verified and fixed test-first` → undo names what keeps setting a key undone 3+ times; replay summary says how many runs already fail [tree 3100c4930d75] (2026-10-28T21:33:01Z)
- (audit maintainer) `one fm-reviewer pass; 7 findings verified and fixed test-first` → _plan_app separate from _app_change so replay never touches the guard path; one module of tests [tree 3100c4930d75] (2026-10-28T21:33:01Z)
## Log
- 2026-10-22T20:58:49Z created
- 2026-10-28T21:05:07Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_extras.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-28T21:05:20Z planned from capture
- 2026-10-28T21:05:21Z focused
- 2026-10-28T21:21:51Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_extras.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/lib/fmideas.py']
- 2026-10-28T21:21:51Z scope: fmideas.run_child's timeout message printed the child's argv (review finding)
- 2026-10-28T21:33:27Z done
- 2026-10-28T21:33:28Z committed dee0bde1 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1544 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Settings power: profiles keyed to the terminal (ssh, tmux, TERM, width,
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmsettings.py; re-ground the plan against them before editing
## Lessons
- CLI write tests need a pty: in_claude_code fails closed without one
## Plan gaps
- failed first: step 1 tests first (red)
## Files touched
- plugin/tests/test_settings_extras.py
- plugin/lib/fmcli.py
- plugin/lib/fmsettings.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmideas.py
