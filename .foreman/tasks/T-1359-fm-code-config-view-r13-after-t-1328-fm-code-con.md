---
id: T-1359
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcli.py, plugin/tests/test_code_worker.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:50Z
updated: 2026-10-23T07:22:51Z
group: runner checks, routing and config
base: 98f2b1942018335cccf769dd1a4034ccdca9a386
base_tree: b17e92a270c4fb34778abb011ff9a25e2969682a
plan0_at: 2026-10-23T07:18:43Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcli.py, plugin/tests/test_code_worker.py, README.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code config: every effective fm code setting with its source (flag, env, project, code.toml or models.json, default), --explain KEY says what it does, and a broken code.toml is named with its line while the view falls back to defaults
## Raw request
> fm code config view (R13, after T-1328): fm code config prints every effective setting with its source (flag, env, project, global, default), --explain KEY says what it does, a bad file names the line and falls back
## Interpretation
fm code's behaviour now comes from flags, environment variables, the project, code.toml and models.json; the user wants one view of what's in force and why, an explanation per setting, and a clear pointer when their file is broken.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code config lists runner, model, lean, limit_wait, chain, on hooks, worker timeout, max steps, max usd, confinement and sensitivity, each with its value and where it came from — verify with `python3 plugin/tests/run.py test_code_worker.Config`
- [x] fm code config --explain KEY says what the setting does and how to change it; an unknown key names the known ones — verify with `python3 plugin/tests/run.py test_code_worker.Config`
- [x] a code.toml that doesn't parse is named with its line, and the view shows the defaults it falls back to (a run still refuses it) — verify with `python3 plugin/tests/run.py test_code_worker.Config`
## Non-goals
## Approach (options → choice → why)
Complete version: a CONFIG table (key, what it does, how to change it, how to read it) and config_view(p, args) that resolves each key in order flag > env > project > file > default, returning [{key, value, source}] and a problem line for a broken file; fm code config prints it (--json too), --explain KEY one entry. Options: (1) a table in fmcode read by one function (chosen: the settings are fm code's own, resolved where fm code already reads them); (2) fold them into fmsettings' schema (it writes tui.toml and the pane's options, with a writer and history: code.toml's tables, acks and runners don't fit its key=value rows); (3) document them only (the request is to see what's in force). A broken code.toml: the view falls back to defaults and names the parse error's line, while runs keep refusing it (a typo must never quietly switch runners or drop an ack).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: sources, explain, a broken file
2. [x] fmcode: CONFIG table and config_view; fm code config [--explain KEY]
3. [x] docs: README, CHANGELOG, MASTER
## Resume here
## Docs impact
README fm code section, CHANGELOG, MASTER; fm code --help gains --explain
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker.Config` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: Config 1s) / OK [ran] [tree c7bf853600cd] (2026-10-23T07:19:50Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_cli` → exit 0 · Ran 194 tests in 74.7s (39 classes, 16 at a time; slowest: Worker 75s, TaskLifecycle 24s, Failover 11s) / OK [ran] [tree c7bf853600cd] (2026-10-23T07:21:05Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 8.6s (16 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 79e706d5ea04] (2026-10-23T07:21:15Z)
- (audit intent) `self: request re-read` → pass: every setting with value and source, --explain, a broken file named with its line and the view falling back (runs refuse; decision recorded) [tree 79e706d5ea04] (2026-10-23T07:21:21Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker.Config` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: Config 1s) / OK [ran] [tree 79e706d5ea04] (2026-10-23T07:21:22Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker.Config` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: Config 1s) / OK [ran] [tree 79e706d5ea04] (2026-10-23T07:21:22Z)
- (ac 3) `python3 plugin/tests/run.py test_code_worker.Config` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: Config 1s) / OK [ran] [tree 79e706d5ea04] (2026-10-23T07:21:22Z)
- (audit intent) `self review (subagents paused at 77% weekly usage): intent, edge` → all three criteria met [tree 79e706d5ea04] (2026-10-23T07:21:22Z)
- (audit edge) `self review (subagents paused at 77% weekly usage): intent, edge` → an unreadable models.json is the problem line, not a crash; a sensitive flag set false reads as the default; values print as JSON for lists and booleans, — for none; an unknown --explain key lists the known ones [tree 79e706d5ea04] (2026-10-23T07:21:22Z)
## Log
- 2026-10-21T03:47:50Z created
- 2026-10-23T07:11:49Z planned from capture
- 2026-10-23T07:12:01Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code_worker.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:18:42Z focused
- 2026-10-23T07:22:49Z done
- 2026-10-23T07:22:51Z committed 5ff4cad9 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- T-1496 [FEATURE M, done, 3 steps] fm code app: settings schema and a comment-preserving tui.toml writer — lesson: Decide 'is Claude running this?' once (CLAUDECODE) and …
- research T-1510-review: Verdict: changes needed.** One terminal-escape hole (it is the key question you asked) and one injection path in the slash command. Nothing was r…
- decision 2026-10-23: A broken code.toml: fm code config falls back to defaults and names the line; runs keep refusing it
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/tests/test_code_worker.py; re-ground the plan against them before editing
## Lessons
- A read-only view may fall back on a broken file; the run that acts on it must not
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- MASTER.md
- README.md
