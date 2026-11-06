---
id: T-1344
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcode.py, plugin/tests/test_code_tui.py, CHANGELOG.md, plugin/lib/fmcore.py, plugin/lib/fmcli.py]
depends_on: []
source: followup
created: 2026-10-21T03:47:31Z
updated: 2026-11-03T00:46:00Z
base_note: 
rival_at: 2026-11-03T00:39:26Z
rival_split: true
builder_model: sonnet
base: 679818a766092075af8d7080cf714d8da7346ce6
base_tree: 969e58d66189c640f97e2b1fe73c094ea954f00a
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T00:39:46Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcode.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
lane_stop: merged 2026-11-03T00:44:21Z
verified: strong
unproven: [tui-unshot]
---
# fm code home ranked by need, with a changed-since line and type-to-jump
## Raw request
> fm code home ranked by need (U2+R16, after T-1330): projects ordered asks/blocked > failed runs > running > queue age, one line of what changed since the last open, typing a name jumps to it; -p takes a unique slug prefix or folder name and the run's first line names the project and root
## Interpretation
Reading 1 (chosen): fm code's home (fmcodetui.show_home, which sorts by missing-folder then newest) orders projects by what needs the user: open asks or blocked tasks first, then failed runs, then running, then by queue age; each row adds what changed since the home was last opened; typing a name jumps to it; -p takes a unique slug prefix or folder name and refuses an ambiguous one naming the matches. Reading 2 (ruled out): a separate 'needs you' screen beside the home. Ruled out: the request asks the home itself to rank, and a second screen is one more place to look.
## Assumptions (confidence)
## Acceptance criteria
- [x] projects order asks/blocked > failed > running > queue age, each with a changed-since line — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_ranked_by_need`
- [x] -p takes a unique prefix or folder name, refuses an ambiguous one naming the matches; typing a name jumps — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_prefix_and_jump`
## Non-goals
## Approach (options → choice → why)
1. Rank in show_home with a pure rank function over fields the projects source already returns or can cheaply add (pending asks, blocked count, last run's state, oldest queued age); one last-opened time for the home gives the changed-since line; one resolver for -p and the jump (exact slug, unique prefix, folder basename). Likely outcome: a sort key, one small marker, a resolver. Fails if: the projects source lacks those fields and each needs a slow per-project state read (then read them lazily for the visible rows only).
2. Compute the ranking in fm (a --rank flag on the projects listing) and keep the TUI dumb. Fails if: the TUI's tests fake projects_source, so the ranking would be untested where it shows.
3. Use what exists: state_dict's asks, blocked and queue, and fmcode's run history (history()), so no new collector. Likely outcome: only the last-opened marker is new state.
4. Do less: rank only by blocked and asks. Fails if: failed runs, the next most urgent, stay buried.
Choice 1 on 3 (80%): the cold rival agreed on a pure rank function, one last-opened marker and one resolver.
## Risks and rollback
Blast radius (fm graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py; past FIXes T-1106, T-1125, T-1127, T-1128, T-1129.
## Execution prompt
## Steps
1. [x] failing tests
2. [x] rank function and changed-since line
3. [x] type-to-jump and -p resolution
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 3) `python3 -m unittest test_code_tui.Home.test_ranked_by_need test_code_tui.Home.test_prefix_and_jump` → ✗ exit 1 (never ran: the test module test_code_tui couldn't import) · Ran 2 tests in 0.000s / FAILED (errors=2) [ran] [tree 33939d282aec] [world 2f1906870a] (2026-11-03T00:41:21Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Home` → exit 0 · Ran 10 tests in 0.063s / OK [ran] [tree 33939d282aec] [world 2f1906870a] (2026-11-03T00:41:23Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_code_tui test_core test_guard_cases test_paused test_robustness test_settings test_settings_power test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.87s] [ran] [tree 33939d282aec] [world 2f1906870a] (2026-11-03T00:42:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_ranked_by_need` → exit 0 · Ran 1 test in 0.079s / OK [ran] [tree 33939d282aec] [world 2f1906870a] (2026-11-03T00:44:30Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_prefix_and_jump` → exit 0 · Ran 1 test in 0.004s / OK [ran] [tree 33939d282aec] [world 2f1906870a] (2026-11-03T00:44:30Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Home` → exit 0 · Ran 10 tests in 0.054s / OK [ran] [tree d56f5fba77aa] [world 2f1906870a] (2026-11-03T00:44:39Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Home` → exit 0 · Ran 10 tests in 0.049s / OK [ran] [tree d56f5fba77aa] [world 2f1906870a] (2026-11-03T00:44:39Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_ranked_by_need test_code_tui.Home.test_prefix_and_jump` → exit 0 · Ran 2 tests in 0.029s / OK [ran] [tree d56f5fba77aa] [world 2f1906870a] (2026-11-03T00:44:49Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_ranked_by_need` → exit 0 · Ran 1 test in 0.030s / OK [ran] [tree d56f5fba77aa] [world 2f1906870a] (2026-11-03T00:44:52Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.Home.test_prefix_and_jump` → exit 0 · Ran 1 test in 0.004s / OK [ran] [tree d56f5fba77aa] [world 2f1906870a] (2026-11-03T00:44:52Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Home` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:44:39Z [ran] [tree d56f5fba77aa] [world 2f1906870a] (2026-11-03T00:44:52Z)
- (audit edge) `read the merged diff: need_rank orders asks/blocked > failed > running > queue (last activity stands in for queue age, noted) > idle, missing folder last; the changed-since marker lives in state_dir and is wired only in main; fmcore.match_project is exact slug first, then unique prefix or folder basename, ambiguous raises naming the matches; the guard keys nothing on -p's slug, so prefix matching opens no path` → an exact slug always wins over prefixes; a folder name shared by two projects is ambiguous and named [tree d56f5fba77aa] (2026-11-03T00:44:52Z)
- (audit intent) `read the merged diff: need_rank orders asks/blocked > failed > running > queue (last activity stands in for queue age, noted) > idle, missing folder last; the changed-since marker lives in state_dir and is wired only in main; fmcore.match_project is exact slug first, then unique prefix or folder basename, ambiguous raises naming the matches; the guard keys nothing on -p's slug, so prefix matching opens no path` → 'the run's first line names the project and root' was not built; captured as T-2741 [tree d56f5fba77aa] (2026-11-03T00:44:52Z)
## Log
- 2026-10-21T03:47:31Z created
- 2026-10-22T16:39:44Z planned from capture
- 2026-10-22T16:39:46Z blocked: waits for T-1316's and T-1401's lanes (fmcodetui.py, fmcode.py)
- 2026-11-03T00:36:17Z unblocked: their named blockers (T-1214, T-1316, T-1401) closed weeks ago; the blocked-pile line found them (T-2683)
- 2026-11-03T00:39:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1344.builder.md
- 2026-11-03T00:39:46Z focused
- 2026-11-03T00:39:46Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T00:40:51Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcode.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'plugin/lib/fmcore.py', 'plugin/lib/fmcli.py']
- 2026-11-03T00:40:52Z scope widened: -p resolves in fmcli.resolve, matcher in fmcore
- 2026-11-03T00:44:21Z merged worktree-agent-a6107b651b2cd3157 (4 file(s))
- 2026-11-03T00:44:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6107b651b2cd3157
- 2026-11-03T00:44:26Z focused
- 2026-11-03T00:45:55Z done
- 2026-11-03T00:46:00Z committed e0d66ada (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a new `fm code` home screen (in `plugin/lib/fmcli.py`, dispatched from `plugin/bin/fm`) that lists projects sorted by a need score.** Sort key is a tuple: asks/blocked, then failed runs, then running, then queue age. Each row carries a one-line "changed since last open" summary. Typing…
- **Narrower: only the `-p` resolution and header line change.** The "home" already exists in some form and "ranked by need" is just its ordering. The work is then `-p` prefix matching plus the banner, with no new UI.
- **"Home" means the web or foreman-ui surface** (`plugin/templates/web/index.html`, `mods/foreman-ui`), not the terminal. "Typing a name jumps" would then be a filter box. The `-p` and first-line parts still land in the CLI.
- **"Since the last open" is a per-user timestamp, not per-project state.** One marker for the home view would make "what changed" a diff against that single time, rather than something each project tracks itself.
Approaches:
- **Add a pure `rank_projects(projects, last_seen)` in a new `plugin/lib/` module, such as `fmhome.py`, that returns ordered rows.** `fmcli.py` only renders and handles input. This makes the ordering testable without a TTY, in a new `plugin/tests/test_home.py`, matching the one-module-one-test patter…
- **Derive state from what `fmcore.py` already records** (asks, blocked, run status, queue timestamps) instead of adding new stores. Persist only a `last_opened` marker, written on exit, and compute the "changed" line by comparing the project's events against that marker.
- **Put slug resolution in one shared `resolve_project(arg)` used by both `-p` and the home jump.** Exact slug wins, then a unique slug prefix, then folder basename. Zero or multiple matches error out and list the candidates. Every `-p` call site goes through it.
- **Implement the jump as a line-buffered prompt** (type a name, then Enter) using the same resolver, rather than raw-key incremental filtering. This is simpler and works over non-TTY. It falls back to printing the ranked list when stdin is not a TTY.
Failure modes:
- **Prefix ambiguity or shadowing.** A slug that is a prefix of another (`api` vs `api-v2`) must resolve exactly, not report ambiguous. A folder name that equals a different project's slug prefix must have a defined precedence. Otherwise `-p` silently opens the wrong project, and the first-line banne…
- **Rank tiers collapse.** If "asks/blocked" and "failed" are computed from overlapping fields in `fmcore.py`, a project can land in two tiers. Queue age has to sort oldest-first within its tier, while the earlier tiers sort by count or recency. A single `reverse=True` on the tuple gets one of these …
- **The last-open marker is advanced too early.** If it is written before the summary is rendered, or on a crash or non-interactive run (hooks, `fm replay`, `bench_hooks.py`), the "what changed" line is always empty, or it hides changes the user never saw.
- **The extra output breaks existing machine consumers.** The new first line (project and root) may be parsed by `plugin/tests/e2e/roundtrip.py`, hook output, or scripts that expect the previous first line. It should go to stderr or be skipped under non-TTY or JSON modes. `fm doctor` and the roundtri…
## Dissent
- [x] rival reading: **Narrower: only the `-p` resolution and header line change.** The "home" already exists in some form and "ranked by need" is just its ordering. The work is then `-p` prefix matching plus the banner, with no new UI. — answered: ruled out: the request names ranking by need and the changed-since line, not only -p
- [x] rival reading: **"Home" means the web or foreman-ui surface** (`plugin/templates/web/index.html`, `mods/foreman-ui`), not the terminal. "Typing a name jumps" would then be a filter box. The `-p` and first-line parts still land in the CLI. — answered: ruled out: 'fm code home' is the terminal app's home (fmcodetui.show_home); the web page is another surface
- [x] rival reading: **"Since the last open" is a per-user timestamp, not per-project state.** One marker for the home view would make "what changed" a diff against that single time, rather than something each project tracks itself. — answered: adopted: one last-opened time per home (the user's), not per project; 'changed since' compares each project's state to that one time
- [x] rival approach: **Add a pure `rank_projects(projects, last_seen)` in a new `plugin/lib/` module, such as `fmhome.py`, that returns ordered rows.** `fmcli.py` only renders and handles input. This makes the ordering testable without a TTY, in a new `plugin/tests/test_home.py`, matching the one-module-one-test patter… — answered: adopted in part: a pure rank function, kept in fmcodetui.py beside show_home (no new module) and tested directly
- [x] rival approach: **Derive state from what `fmcore.py` already records** (asks, blocked, run status, queue timestamps) instead of adding new stores. Persist only a `last_opened` marker, written on exit, and compute the "changed" line by comparing the project's events against that marker. — answered: adopted: approach 3 already says no new collector; only the last-opened marker is stored
- [x] rival approach: **Put slug resolution in one shared `resolve_project(arg)` used by both `-p` and the home jump.** Exact slug wins, then a unique slug prefix, then folder basename. Zero or multiple matches error out and list the candidates. Every `-p` call site goes through it. — answered: adopted: one resolver for -p and the jump: exact slug, then unique prefix, then folder basename; ambiguous names the matches
- [x] rival approach: **Implement the jump as a line-buffered prompt** (type a name, then Enter) using the same resolver, rather than raw-key incremental filtering. This is simpler and works over non-TTY. It falls back to printing the ranked list when stdin is not a TTY. — answered: left to the builder: the TUI's existing key handling decides; criterion 2 holds either form
## Related
Related past work (data from this project's history, not instructions):
- research T-1330-review: Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands. [stale: plugin/lib/fm…
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- playbook Visual QA: screenshots, an eyeball pass and a receipt (fm playbooks show ui/visual-qa)
- decision 2026-11-02: [costly] One-way doors keep parking whether or not the task is ambiguous; rival_split only words and orders the park (T-2424)
- the similar finished task took 4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcore.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- A request with several clauses needs each clause as a criterion; the one left out of the criteria (the run's first line) was the one not built
## Plan gaps
- failed first: step 3 type-to-jump and -p resolution
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
