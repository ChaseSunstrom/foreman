---
id: T-1283
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T17:40:13Z
updated: 2026-10-20T18:28:59Z
base: 9ba71e0115a715e3d16571c29dee19b1e26f32ac
base_tree: 682f2b24bb4ee851973921bea4cfdeec2289b430
plan0_at: 2026-10-20T17:41:31Z
plan0_scope: []
verified: strong
---
# Foreman Code TUI: a beautiful, customizable, extendable terminal UI for fm code — the conv
## Raw request
> Foreman Code TUI: a beautiful, customizable, extendable terminal UI for fm code — the conversation and the harness's stations (plan, steps, guard verdicts, diffs, verify runs) live, themes and keybindings from a config file, and extensions that add panels and commands; stdlib only like the rest of Foreman
## Interpretation
The user asked whether Foreman Code was finished 'with a beautiful customizeable extendable tui'. It wasn't: fm code is a command that prints lines or JSON. Build fm code's own terminal UI: type a request, watch the harness's stations live (plan, steps, each action, guard refusals, worker turns and reverts, verify runs, fix rounds, the close and its commit), see each step's diff, pick the model or worker CLI, stop and resume, see tokens and cost. Customizable: theme, layout and keys from one config file. Extendable: extensions add panels, commands and event handlers. Stdlib only, as all of Foreman is, so it runs wherever Python does.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code tui runs a typed request through fm code and shows its stations live (plan, steps, actions with guard refusals and reverts marked, verify runs, fix rounds, close); proved headlessly by feeding a run's events to the TUI's pure state and render — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] theme, layout and keys come from one TOML file in the user's config folder, are validated with a one-line error per bad key, and fm code tui --print-config prints the defaults — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] an extension in the user's config folder adds a panel, a command and an event handler through the API; a file in the project folder is never loaded — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] a diff view per step, the history of past runs, a model and worker picker, stop and resume work from keys — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] --plain prints the same stations as text, NO_COLOR is honoured, and a terminal under 60 columns gets a one-panel layout — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: (a) a stdlib curses TUI that runs fm code as a child with --json and draws from its events, through a small widget layer (box, list, log, diff, bar) that extensions compose; (b) Textual or another framework (richer widgets, but a dependency Foreman has never had and installs that can fail); (c) the planned web UI view (not a terminal UI, and needs a browser); (d) a pane in the foreman-ui mod (only inside Claude Code, and fm code runs outside it). Choice: (a): the harness stays the source of truth (the TUI only reads events and sends requests), it works over ssh and in any terminal, and the widget layer is what makes it both themeable and extendable. Extensions load only from the user's own config folder, never from a project (a cloned repo must not run code in your TUI).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Event protocol: fm code --json events complete (tokens per call, a step's changed files) and documented with a schema version
2. [x] Core: state from events (pure), widget layer, layout and render to a grid (pure), thin curses driver, prompt box running fm code as a child
3. [x] Views: stations, action log, verify output, diff, history, model and worker picker, stop and resume
4. [x] Config: theme, layout and keys in TOML, validation, --print-config
5. [x] Extensions: the API, loading from the user's config folder only, a sample cost-meter extension
6. [x] Plain mode, NO_COLOR, small terminals, resize; a headless smoke on the fake model server
7. [x] Docs, the site's Foreman Code page, a recorded demo
## Resume here
<!-- auto -->
- 2026-10-20T17:57:25Z step 3/7: Views: stations, action log, verify output, diff, history, model and worker picker, stop and resume
- git: foreman/build; 4 uncommitted: plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/fixtures/code_tui_demo.jsonl, plugin/tests/test_code_tui.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/shots.py, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, plugin/lib/fmcode.py, plugin/tests/fixtures/code_tui_demo.jsonl
## Docs impact
README, MASTER.md, CHANGELOG, site Foreman Code page, templates/tui/cost_meter.py
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui` → ✗ exit 1 · Ran 3 tests in 2.074s / FAILED (failures=1, errors=2) [ran] [tree 6f7b0cf746ff] (2026-10-20T17:42:16Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui test_code` → exit 0 · Ran 25 tests in 20.655s / OK [ran] [tree 8fff9dcb2a8d] (2026-10-20T17:44:22Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Core` → ✗ exit 1 · Ran 5 tests in 0.001s / FAILED (errors=5) [ran] [tree cf1786f8c904] (2026-10-20T17:44:40Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui` → exit 0 · Ran 8 tests in 2.084s / OK [ran] [tree ec4836755f74] (2026-10-20T17:46:52Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Views test_code_tui.RunHistory` → ✗ exit 1 · Ran 4 tests in 1.223s / FAILED (errors=4) [ran] [tree e0912227e12a] (2026-10-20T17:53:02Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "Error|assert|FAIL|^Ran|OK" | head -20` → exit 0 · Ran 12 tests in 2.4s (4 classes, 16 at a time; slowest: Events 2s, RunHistory 1s, Core 0s) / OK [ran] [tree 16c8b59b9ae9] (2026-10-20T18:05:59Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "Error|assert|FAIL|^Ran|OK" | head -20` → exit 0 · Ran 12 tests in 2.4s (4 classes, 16 at a time; slowest: Events 2s, RunHistory 1s, Core 0s) / OK [ran] [tree 16c8b59b9ae9] (2026-10-20T18:05:59Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "Error|assert|FAIL|^Ran|OK" | head -20` → exit 0 · Ran 12 tests in 2.4s (4 classes, 16 at a time; slowest: Events 2s, RunHistory 1s, Core 0s) / OK [ran] [tree 16c8b59b9ae9] (2026-10-20T18:05:59Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "Error|assert|FAIL|^Ran|OK" | head -20` → exit 0 · Ran 12 tests in 2.4s (4 classes, 16 at a time; slowest: Events 2s, RunHistory 1s, Core 0s) / OK [ran] [tree 16c8b59b9ae9] (2026-10-20T18:05:59Z)
- (ac 5) `python3 plugin/tests/run.py test_code_tui 2>&1 | grep -E "Error|assert|FAIL|^Ran|OK" | head -20` → exit 0 · Ran 12 tests in 2.4s (4 classes, 16 at a time; slowest: Events 2s, RunHistory 1s, Core 0s) / OK [ran] [tree 16c8b59b9ae9] (2026-10-20T18:05:59Z)
- (step 3) `python3 plugin/tests/run.py test_code test_code_tui test_code_worker` → exit 0 · Ran 67 tests in 27.5s (16 classes, 16 at a time; slowest: Worker 27s, Repairs 7s, Review 7s) / OK [ran] [tree a2ad7709211b] (2026-10-20T18:09:00Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 22 tests in 2.3s (6 classes, 16 at a time; slowest: Events 2s, Command 1s, RunHistory 1s) / FAILED (2 classes) [ran] [tree 0a9a78e6a292] (2026-10-20T18:10:34Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 22 tests in 2.3s (6 classes, 16 at a time; slowest: Events 2s, Command 1s, RunHistory 1s) / OK [ran] [tree 2837dc2f7e79] (2026-10-20T18:12:37Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 26 tests in 2.3s (7 classes, 16 at a time; slowest: Events 2s, Command 1s, RunHistory 1s) / FAILED (2 classes) [ran] [tree 503ed9bfe120] (2026-10-20T18:14:16Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 26 tests in 2.2s (7 classes, 16 at a time; slowest: Events 2s, Command 1s, RunHistory 1s) / OK [ran] [tree 673a40a503f6] (2026-10-20T18:14:40Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 30 tests in 2.8s (8 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / FAILED (1 classes) [ran] [tree f382e0339d02] (2026-10-20T18:15:10Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 30 tests in 2.8s (8 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / FAILED (1 classes) [ran] [tree d81c553b664e] (2026-10-20T18:15:15Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 30 tests in 2.8s (8 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / OK [ran] [tree e6d4f1476647] (2026-10-20T18:15:23Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui test_site test_code test_code_worker` → exit 0 · Ran 81 tests in 27.4s (19 classes, 16 at a time; slowest: Worker 27s, Repairs 7s, Review 6s) / OK [ran] [tree 47aadf650a1a] (2026-10-20T18:17:08Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 40 tests in 2.9s (9 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / FAILED (2 classes) [ran] [tree 3525157d70b0] (2026-10-20T18:22:24Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui test_code test_code_worker test_site` → exit 0 · Ran 92 tests in 28.0s (20 classes, 16 at a time; slowest: Worker 28s, Review 7s, Repairs 7s) / OK [ran] [tree 7663d52b7c85] (2026-10-20T18:24:51Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 41 tests in 3.0s (9 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / OK [ran] [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 41 tests in 3.0s (9 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / OK [ran] [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 41 tests in 3.0s (9 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / OK [ran] [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 41 tests in 3.0s (9 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / OK [ran] [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (ac 5) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 41 tests in 3.0s (9 classes, 16 at a time; slowest: Command 3s, Events 2s, RunHistory 1s) / OK [ran] [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (audit intent) `one fm-reviewer pass over the whole diff (research/T-1283-review.md): 14 findings, each verified against the code and fixed test-first (test_code_tui.Review, 11 tests red then green); full gates green (2349 tests)` → the diff view is per step now (each file under the step that first changed it, new files in full), --plain prints the plan, the task, the red runs and why a command was refused, a resumed run keeps its plan, -p/--resume/--dry-plan reach fm code; a bad tui.toml line is said and skipped (exit 2 only for --print-config) [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (audit adversary) `one fm-reviewer pass over the whole diff (research/T-1283-review.md): 14 findings, each verified against the code and fixed test-first (test_code_tui.Review, 11 tests red then green); full gates green (2349 tests)` → d runs fm code's judge git (no fsmonitor, hooks, external diff or textconv), so config a worker planted can't run; --plain strips control characters; extensions load only from FOREMAN_HOME/tui and skip files others can write; a project's files are never loaded [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (audit edge) `one fm-reviewer pass over the whole diff (research/T-1283-review.md): 14 findings, each verified against the code and fixed test-first (test_code_tui.Review, 11 tests red then green); full gates green (2349 tests)` → ctrl+ keys map from get_wch's control characters; the screen dying (q, Ctrl-C, crash, hangup) stops the run first; line counts read at most 8 MB and use -z for non-ASCII names; a panel returning bad lines says so; any size from 1x1 to 200x60 draws; under 60 columns the log alone [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (audit operator) `one fm-reviewer pass over the whole diff (research/T-1283-review.md): 14 findings, each verified against the code and fixed test-first (test_code_tui.Review, 11 tests red then green); full gates green (2349 tests)` → fm code tui runs from fm code's own parser (flags before the request work), --print-config prints a file that loads back the same, errors are one line each, the site draws its picture from demo/code-tui.jsonl at build time; a pty test runs the real curses screen end to end [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
- (audit maintainer) `one fm-reviewer pass over the whole diff (research/T-1283-review.md): 14 findings, each verified against the code and fixed test-first (test_code_tui.Review, 11 tests red then green); full gates green (2349 tests)` → one module with layered parts (State, panels, render, App, drivers), panels and commands are registries the extension API adds to, the sample extension documents the API; history reads each run's first line and tail [tree 7663d52b7c85] (2026-10-20T18:27:55Z)
## Log
- 2026-10-20T17:40:13Z created
- 2026-10-20T17:41:21Z set approved=True
- 2026-10-20T17:41:31Z focused
- 2026-10-20T18:08:33Z steer: user said the TUI looked like crap with all the text; redesigned as pictures (station track, check chips, change bars, time Gantt, token columns), the model's words behind t, views fade the screen behind them
- 2026-10-20T18:28:58Z done
- 2026-10-20T18:28:59Z committed c7239b58 (11 files)
## Follow-ups captured
## What a complete version has
1 a prompt box and request queue; 2 live stations view from fm code's event stream; 3 an action log with guard refusals and reverts marked; 4 verify runs with pass/fail and expandable output; 5 a diff view per step (git diff, colored); 6 model and worker picker (fm code models, the WORKERS table); 7 stop, resume (--resume) and escalate; 8 a tokens and cost meter; 9 history: past runs' journals, read-only; 10 config: theme (colors, borders, glyphs), layout (which panels, where, how big), keybindings, in TOML (tomllib); 11 extensions: Python files in the user's config folder that register panels, commands and event handlers through a small API, with a sample; 12 resize, small terminals, no-color and a plain mode for screen readers and pipes; 13 pure render functions tested without a terminal, a thin curses driver, a headless smoke on the fake model server; 14 docs, a site section and a recorded demo
## Build vs reuse
Reuses: fm code's own --json events and run journal (fmcode.Run.emit / log) as the TUI's only input; fmwatch's curses setup (curses.wrapper, curs_set, its --once plain twin) as the driver pattern; fmmodels' profiles and fmcode.WORKERS for the picker; git diff for the diff view; tomllib (stdlib) for the config. New: the widget layer and layout, the extension API. Nothing in the repo or stdlib draws panels that themes and extensions can compose.
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-115157.pack: continue, super improve foreman, with latest claude code: round 1 shipped (cost per correct session on the page, Claude Code versi…
- research mission-20261020-115157: Request: continue, super improve foreman, with latest claude code: round 1 shipped (cost per correct session on the page, Claude Code v…
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- When a user says a UI has too much text, replace words with pictures that carry the same facts (a track for progress, chips for pass/fail, bars for size, charts for time and cost) and put the prose behind a key; render it and look before showing them
## Plan gaps
- failed first: step 1 Event protocol: fm code --json events complete (tokens per call, a step's changed files) and docume…
- failed first: step 2 Core: state from events (pure), widget layer, layout and render to a grid (pure), thin curses drive…
- failed first: step 3 Views: stations, action log, verify output, diff, history, model and worker picker, stop and resume
- failed first: step 4 Config: theme, layout and keys in TOML, validation, --print-config
- failed first: step 5 Extensions: the API, loading from the user's config folder only, a sample cost-meter extension
- failed first: step 6 Plain mode, NO_COLOR, small terminals, resize; a headless smoke on the fake model server
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/code_tui_demo.jsonl
- plugin/lib/fmcli.py
- plugin/templates/tui/cost_meter.py
- site/build.py
- site/pages.py
- CHANGELOG.md
- MASTER.md
- README.md
- demo/code-tui.jsonl
