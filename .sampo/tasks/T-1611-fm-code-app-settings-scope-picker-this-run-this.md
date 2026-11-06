---
id: T-1611
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/tests/test_settings_scopes.py, plugin/tests/test_guard.py, .gitignore, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T20:54:19Z
updated: 2026-10-23T17:45:40Z
group: settings surfaces and safety
base: 48e22b97fbcaaaeea6ec0a4108bc18cbfb2f08ba
base_tree: 41855d015192f1a35385b50d8e5ef7066cc6a435
plan0_at: 2026-10-23T17:44:54Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/tests/test_settings_scopes.py, plugin/tests/test_guard.py, .gitignore, CHANGELOG.md, MASTER.md]
verified: strong
---
# Fm code app settings scope picker (this run, this project, everywhere) and repo policy pin
## Raw request
> fm code app settings scope picker (this run, this project, everywhere) and repo policy pins that a project's own settings can't override (follow-up of T-1543)
## Interpretation
The fm code app's settings get scopes: everywhere (tui.toml, as now), this project (a settings file kept with Foreman's state for the project, never in the repo) and this run (held in memory). s in the settings screen picks where the next :set goes (and :set takes --scope). A repo's committed .foreman/policy.toml [pin] table pins settings over every scope; keys and motion are never pinned (the person's hands and comfort). Rows show which scope or pin sets them; a pinned setting refuses a :set and says why. fm settings set --scope project is the Claude Code surface.
## Assumptions (confidence)
## Acceptance criteria
- [x] s and --scope put a :set in this run, this project or everywhere; the repo's [pin] wins over every scope, never pins keys or motion, and a pinned setting refuses a :set — verify with `python3 plugin/tests/run.py test_settings_scopes`
## Non-goals
## Approach (options → choice → why)
Options: (a) merge every layer into one TOML text and load once (duplicate keys break TOML); (b) a profile-like when clause per project inside tui.toml (mixes scopes in one file, a repo can't ship pins); (c) layered(): load tui.toml as now, then apply the project file, the run's table and the pins through the same _apply checks, recording the narrowest scope per setting. Chosen (c): reuses every check, one function the app calls wherever it loads its config. Project settings live with Foreman's per-project state so a cloned repo can't rebind keys; the policy file is the repo's and is limited to look settings.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] layered scopes and pins in fmcodetui
3. [x] the settings screen's scope picker and marks
4. [x] fm settings set --scope project
5. [x] docs
## Resume here
## Docs impact
MASTER.md (fmcodetui layered scopes line), CHANGELOG.md; the settings screen's note names s and the scope.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_scopes` → ✗ exit 1 · Ran 6 tests in 0.4s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / FAILED (3 classes) [ran] [tree 522a1976afb6] (2026-10-23T17:40:32Z)
- (step 1) `python3 plugin/tests/run.py test_settings_scopes` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:43:57Z)
- (step 2) `python3 plugin/tests/run.py test_settings_scopes` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:43:58Z)
- (step 3) `python3 plugin/tests/run.py test_settings_scopes` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:44:00Z)
- (step 4) `python3 plugin/tests/run.py test_settings_scopes` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:44:01Z)
- (step 5) `python3 plugin/tests/run.py test_docs test_suite_hygiene test_guard test_settings test_code_tui test_cli` → exit 0 · Ran 827 tests in 27.4s (208 classes, 16 at a time; slowest: TaskLifecycle 27s, Mutation 13s, Command 13s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:44:29Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_scopes` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:44:30Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_scopes test_guard` → exit 0 · Ran 294 tests in 8.3s (90 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:45:10Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_scopes` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Cli 0s, App 0s, Layers 0s) / OK [ran] [tree 880fb276fd7b] (2026-10-23T17:45:11Z)
- (audit intent) `self-review of layered(), the app's scope picker and the CLI: every layer goes through _apply's checks; pins skip keys and motion and say so; tui.toml-only tables refused in layers; the project file sits in FOREMAN_HOME/tui.projects, which the guard now treats as core like tui.toml (tested in test_guard's table and by an agent-shell set refused); a run set writes nothing; photographed the settings screen with a pin and the scope note` → s and --scope send a :set to this run, this project or everywhere; a repo pins look settings over all scopes; fm settings set --scope project works from a shell [tree 880fb276fd7b] (2026-10-23T17:45:11Z)
- (audit edge) `self-review of layered(), the app's scope picker and the CLI: every layer goes through _apply's checks; pins skip keys and motion and say so; tui.toml-only tables refused in layers; the project file sits in FOREMAN_HOME/tui.projects, which the guard now treats as core like tui.toml (tested in test_guard's table and by an agent-shell set refused); a run set writes nothing; photographed the settings screen with a pin and the scope note` → a bad value in a layer is said and the rest apply; [pin] that isn't a table is said; a pinned setting refuses a :set in every scope here; a run setting is gone when the app quits; a plugin setting refuses --scope project [tree 880fb276fd7b] (2026-10-23T17:45:11Z)
- (audit adversary) `self-review of layered(), the app's scope picker and the CLI: every layer goes through _apply's checks; pins skip keys and motion and say so; tui.toml-only tables refused in layers; the project file sits in FOREMAN_HOME/tui.projects, which the guard now treats as core like tui.toml (tested in test_guard's table and by an agent-shell set refused); a run set writes nothing; photographed the settings screen with a pin and the scope note` → a cloned repo can't rebind keys or raise motion (PIN_FREE) and can't add profiles, rules or extension settings (LAYER_ONLY); project settings can bind keys, so they live outside the repo and are core to the guard: an agent's shell can't write them without the user's yes [tree 880fb276fd7b] (2026-10-23T17:45:11Z)
## Log
- 2026-10-22T20:54:19Z created
- 2026-10-23T17:30:11Z set type=FEATURE, tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_scopes.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:40:22Z lane: ~/.claude/foreman.lanes/T-1611 on foreman/T-1611
- 2026-10-23T17:43:56Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_settings_scopes.py', 'plugin/tests/test_guard.py', '.gitignore', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:43:56Z scope: fmguard.py, test_guard.py and .gitignore: project settings bind keys, so they live beside tui.toml as core config the guard protects
- 2026-10-23T17:44:50Z merged foreman/T-1611 (9 file(s))
- 2026-10-23T17:44:52Z lane removed: ~/.claude/foreman.lanes/T-1611
- 2026-10-23T17:44:53Z focused
- 2026-10-23T17:45:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1543-review: Verdict: approve with nits.** The three-part acceptance criterion is met. I could not run the tests, because I had no shell in this audit. The ta…
- T-1543 [FEATURE M, done, 4 steps] Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren — lesson: A file watcher must stat before it…
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_guard.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): .gitignore, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmguard.py, plugin/lib/fmsettings.py, plugin/tests/test_guard.py, plugin/tests/test_settings_scopes.py; re-ground the plan against them before editing
## Lessons
- A new settings file that can bind keys needs the same guard protection as tui.toml: decide its home by what the guard already protects, not by where state usually lives.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- .gitignore
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmguard.py
- plugin/lib/fmsettings.py
- plugin/tests/test_guard.py
- plugin/tests/test_settings_scopes.py
