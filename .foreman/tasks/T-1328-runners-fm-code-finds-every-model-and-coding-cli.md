---
id: T-1328
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:07Z
updated: 2026-10-21T05:30:20Z
base: 778674f593ad65aecd61544c48a8c058c23fdc40
base_tree: df48d88cd104bfac7f03351c6331b7cb0e9a042d
plan0_at: 2026-10-21T04:26:20Z
plan0_scope: []
verified: strong
---
# Runners: fm code finds every model and coding CLI on the machine, works with no setup, and one config line picks the default
## Raw request
> Runners: fm code finds every model and coding CLI on the machine, works with no setup, and one config line picks the default
## Interpretation
With only Claude Code installed, fm code needs --worker claude typed every time, and nothing lists what runners the machine has or lets the user pick a default once. 'Manage ANY CLI/model': fm code should find every model and coding CLI, use a safe default with no setup, and take a default from one config line, globally or per project, without ever weakening the worker presets' safety (no preset auto-approves a worker's shell commands).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code runners lists models and CLIs (claude, codex, gemini, aider, opencode, qwen, cursor-agent, custom ones from config) with what each can do; with no model set, fm code uses the first installed CLI that can plan read-only and says so; runner = NAME in the config (global or per project) picks it — verify with `python3 plugin/tests/run.py test_code test_code_worker`
## Non-goals
## Approach (options → choice → why)
One registry RUNNERS {name: {work, plan, stream}} replaces WORKERS and PLANNERS: claude (plan: --permission-mode plan, stream: stream-json), codex (exec --full-auto / --sandbox read-only, --json), gemini and qwen (--approval-mode auto_edit / default), aider (--message / --chat-mode ask), opencode (run / run --agent plan), cursor-agent and goose and amp (work only until a read-only mode is confirmed). Models stay in fmmodels. Config: $FOREMAN_HOME/code.toml (runner = NAME; [runner.NAME] work/plan/stream for a custom CLI), never read from a repo (a repo file naming a command would run it); a project's choice is a name only, kept in Foreman state (fm code runners --use NAME [--project]). fm code runners lists models and CLIs: installed, can plan, streams, default. Default when nothing is set: a configured or local model, else the first installed CLI that can plan read-only, said in the start line. Options weighed: per-repo config file (rejected: code execution from a cloned repo), env vars only (no discoverability), a TUI-only setting (the CLI path would still fail).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: runner list (installed, verified planner, streams), auto-default only to a verified planner, a named unverified one warns, config pick (global, project name only), a custom CLI from code.toml, a project naming an unknown runner
2. [x] RUNNERS registry; WORKERS and PLANNERS kept as views of it (TUI picker and bench unchanged)
3. [x] choose_profile and the worker path read RUNNERS and the config ($FOREMAN_HOME/code.toml, project name in state)
4. [x] fm code runners [--check] [--use NAME [--project]]; evidence on this machine
5. [x] Docs: README, MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-21T04:30:13Z step 1/5: Failing tests: runner list (installed, verified planner, streams), auto-default only to a verified planner, a named unverified one warns, config pick (global, project name only), a custom CLI from code.toml, a project naming an unknown runner
- git: foreman/build; 1 uncommitted: plugin/tests/test_code_worker.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker` → ✗ exit 1 · Ran 40 tests in 93.4s (1 classes, 16 at a time; slowest: Worker 93s) / FAILED (1 classes) [ran] [tree bc5c3c15854b] (2026-10-21T04:28:15Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code test_code_tui test_code_bench` → exit 0 · Ran 167 tests in 91.6s (27 classes, 16 at a time; slowest: Worker 91s, Bench 31s, Review 20s) / OK [ran] [tree 9f23ddec445e] (2026-10-21T05:07:03Z)
- (step 3) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 40 tests in 88.2s (1 classes, 16 at a time; slowest: Worker 88s) / OK [ran] [tree 9f23ddec445e] (2026-10-21T05:08:37Z)
- (step 4) `fm code runners --check` → exit 0 · amp           —          no preset: define it in code.toml / (* used with no --worker or --model: no model is set up; it plans read-only and works) [ran] [tree 9f23ddec445e] (2026-10-21T05:08:38Z)
- (step 5) `grep -c 'fm code runners' README.md CHANGELOG.md` → exit 0 · README.md:1 / CHANGELOG.md:1 [ran] [tree 300777ea4423] (2026-10-21T05:08:51Z)
- (step 5) `python3 plugin/tests/run.py test_code_worker test_guard test_code test_code_tui` → exit 0 · Ran 370 tests in 101.1s (86 classes, 16 at a time; slowest: Worker 101s, Bench 33s, Repairs 23s) / OK [ran] [tree 75b10ba237a9] (2026-10-21T05:25:41Z)
- (ac 1) `python3 plugin/tests/run.py test_code test_code_worker` → exit 0 · Ran 174 tests in 98.9s (27 classes, 16 at a time; slowest: Worker 98s, Bench 33s, Review 22s) / OK [ran] [tree 75b10ba237a9] (2026-10-21T05:27:35Z)
- (audit intent) `one fm-reviewer pass (five lenses); 6 findings verified and fixed test-first; saved as research T-1328-review` → fm code runners lists CLIs and models; no model + no flag uses the verified planner and says so; config and project pick by name; any CLI by code.toml template [tree 75b10ba237a9] (2026-10-21T05:27:35Z)
- (audit adversary) `one fm-reviewer pass (five lenses); 6 findings verified and fixed test-first; saved as research T-1328-review` → a project's runner is a name checked against the registry and code.toml (hand-edited meta test); code.toml, tui.toml, tui/ and models.json are now guard-protected core [tree 75b10ba237a9] (2026-10-21T05:27:35Z)
- (audit edge) `one fm-reviewer pass (five lenses); 6 findings verified and fixed test-first; saved as research T-1328-review` → malformed code.toml lists built-ins with the problem; template without {prompt} named; --use edits only the top-level key, verified by tomllib before writing; --here alone refused; --use '' clears [tree 75b10ba237a9] (2026-10-21T05:27:35Z)
- (audit operator) `one fm-reviewer pass (five lenses); 6 findings verified and fixed test-first; saved as research T-1328-review` → a broken models.json or mistyped default is a loud error, never a quiet switch to claude; the note event names the runner in --json and the TUI [tree 75b10ba237a9] (2026-10-21T05:27:35Z)
- (audit maintainer) `one fm-reviewer pass (five lenses); 6 findings verified and fixed test-first; saved as research T-1328-review` → WORKERS/PLANNERS stay views of RUNNERS so the TUI picker and bench are unchanged; local servers are probed up to twice on a no-model run (accepted) [tree 75b10ba237a9] (2026-10-21T05:27:35Z)
## Log
- 2026-10-21T03:24:07Z created
- 2026-10-21T03:37:01Z steer (second plan): (1) a runner's read-only plan mode counts as verified only where it was run here (claude); the auto-default picks only verified planners; an unverified one plans only when named, behind the planner tree check (any change stops the run) and with a one-line warning; (2) evidence includes fm code runners on this machine, not only stubs; (3) commands come only from the built-in registry and the user's $FOREMAN_HOME/code.toml; a project's choice is a name and can't define a command; (4) WORKERS and PLANNERS stay as views of RUNNERS so callers (TUI picker, bench) keep working, one step per change; (5) streaming stays in T-1329, here 'stream' is only listed; (6) installed vs usable: fm code runners --check runs each CLI's --version
- 2026-10-21T04:26:20Z focused
- 2026-10-21T04:30:18Z paused: focus moved to T-1323
- 2026-10-21T04:57:12Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T04:57:12Z focused
- 2026-10-21T05:00:58Z hypothesis: RUNNERS + code.toml + pick_runner make the auto-default, config and unverified-note tests pass; runners command still missing so its 3 tests stay red
- 2026-10-21T05:12:54Z steer-free note: T-1329 test draft and sanitized stream fixture staged in scratchpad; applied after T-1328 closes so its commit stays clean
- 2026-10-21T05:14:03Z scope: plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_code_tui.py, plugin/lib/fmcodetui.py — review: code.toml turns text into commands, so it (and tui.toml, tui/, models.json) becomes a protected path; the TUI shows the runner note
- 2026-10-21T05:30:18Z done
- 2026-10-21T05:30:20Z committed 25e56aed (9 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The default is chosen by "first installed CLI that can plan read-only", but the plan flags for several runners (codex `--sandbox read-only`, gemini/qwen `default` approval mode, aider `--chat-mode ask`, opencode `--agent plan`) are asserted from memory. None is confirmed to actually block wri…
- HIGH: The criterion "verify with `python3 plugin/tests/run.py test_code test_code_worker`" only proves the logic against stubs. Nothing shows that `fm code runners` detects real installs, or that "works with no setup" holds on a machine with only one CLI, only a local model, or nothing. The empty c…
- HIGH: The config security story is incomplete. `code.toml` in `$FOREMAN_HOME` is trusted, but the per-project choice is "a name only, kept in Foreman state". That name could still refer to a custom `[runner.NAME]` command, and the plan doesn't say what happens when a project name doesn't resolve, o…
- MEDIUM: Replacing WORKERS and PLANNERS with one registry is a refactor of existing behavior, but the plan lists no migration step, and step 2 bundles registry, subcommand and config into one item. Existing callers, the TUI path (the plan notes that "the CLI path would still fail"), and users' curre…
- MEDIUM: The "stream" capability is listed (stream-json, --json) but the acceptance criteria don't say what it changes, and runners without it need a defined fallback output path. Parsing each CLI's stream format is a hidden cost. — Either scope streaming to claude and codex and show "no" for the re…
- LOW: Detection by name on PATH can match unrelated binaries (e.g. `amp`, `goose`) and installed isn't the same as authenticated, so the auto-default may choose a CLI that can't run. — Show "installed" separately from "usable". Optionally run a cheap `--version` probe with a timeout, and have `fm co…
Verdict: revise — the read-only claims and the empty and precedence cases need pinning down, and the custom-command security needs to be specified, before writing the failing tests.
## Dissent
- [ ] HIGH: The default is chosen by "first installed CLI that can plan read-only", but the plan flags for several runners (codex `--sandbox read-only`, gemini/qwen `default` approval mode, aider `--chat-mode ask`, opencode `--agent plan`) are asserted from memory. None is confirmed to actually block wri…
- [ ] HIGH: The criterion "verify with `python3 plugin/tests/run.py test_code test_code_worker`" only proves the logic against stubs. Nothing shows that `fm code runners` detects real installs, or that "works with no setup" holds on a machine with only one CLI, only a local model, or nothing. The empty c…
- [ ] HIGH: The config security story is incomplete. `code.toml` in `$FOREMAN_HOME` is trusted, but the per-project choice is "a name only, kept in Foreman state". That name could still refer to a custom `[runner.NAME]` command, and the plan doesn't say what happens when a project name doesn't resolve, o…
- [ ] MEDIUM: Replacing WORKERS and PLANNERS with one registry is a refactor of existing behavior, but the plan lists no migration step, and step 2 bundles registry, subcommand and config into one item. Existing callers, the TUI path (the plan notes that "the CLI path would still fail"), and users' curre…
- [ ] MEDIUM: The "stream" capability is listed (stream-json, --json) but the acceptance criteria don't say what it changes, and runners without it need a defined fallback output path. Parsing each CLI's stream format is a hidden cost. — Either scope streaming to claude and codex and show "no" for the re…
- [ ] LOW: Detection by name on PATH can match unrelated binaries (e.g. `amp`, `goose`) and installed isn't the same as authenticated, so the auto-default may choose a CLI that can't run. — Show "installed" separately from "usable". Optionally run a cheap `--version` probe with a timeout, and have `fm co…
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- A config file that turns text into a command is a code file: put it under the guard's protected paths the day it is introduced
## Plan gaps
- failed first: step 1 Failing tests: runner list (installed, verified planner, streams), auto-default only to a verified …
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- README.md
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/lib/fmcore.py
- plugin/tests/test_vetoes.py
