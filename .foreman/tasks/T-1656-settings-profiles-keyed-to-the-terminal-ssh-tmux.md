---
id: T-1656
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings_power.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:58:42Z
updated: 2026-10-22T22:55:22Z
base: 8586253736eb6d2388bdc40c7d7902d394054ace
base_tree: b2285366c07b2bca39d965b52234c7806ea4c806
plan0_at: 2026-10-22T22:12:53Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings_power.py, CHANGELOG.md]
verified: strong
---
# Settings profiles keyed to the terminal (ssh, tmux, TERM, width) picked automatically, shown by fm settings profile
## Raw request
> Settings profiles keyed to the terminal (ssh, tmux, TERM, width) picked automatically, shown by fm settings profile
## Interpretation
Settings profiles: tui.toml can hold [profile.NAME] tables with a when clause on terminal facts (ssh session, inside tmux, TERM, columns below N, colour depth); the fm code app applies the first matching profile over the base settings at start, and fm settings profile lists the profiles and which one matches now.
## Assumptions (confidence)
## Acceptance criteria
- [x] given the environment the right profile is chosen and fm settings profile lists it — verify with `python3 plugin/tests/run.py test_settings_power.Profile`
## Non-goals
## Approach (options → choice → why)
Options: separate config files per terminal (duplication); conditional tables in one file; environment variables only. Choice: conditional tables: one file, readable, and the schema validates them like any other key.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with an env dict
2. [x] fact reader and profile table
3. [x] wire into config load
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Profile 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 2.6s (1 classes, 16 at a time; slowest: Profile 0s) / FAILED (1 classes) [ran] [tree 6630d3e6f4a8] (2026-10-22T22:17:15Z)
- (step 1) `python3 plugin/tests/run.py test_settings_power.Profile` → ✗ exit 1 · Ran 6 tests in 0.6s (1 classes, 16 at a time; slowest: Profile 0s) / FAILED (1 classes) [ran] [tree 6630d3e6f4a8] (2026-10-22T22:17:18Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Profile 2>&1 | tail -15` → exit 0 · Ran 7 tests in 1.6s (1 classes, 16 at a time; slowest: Profile 1s) / OK [ran] [tree e654c22853c3] (2026-10-22T22:22:02Z)
- (step 2) `python3 plugin/tests/run.py test_settings_power.Profile` → exit 0 · Ran 7 tests in 0.7s (1 classes, 16 at a time; slowest: Profile 0s) / OK [ran] [tree 90b3e7a5a588] (2026-10-22T22:22:36Z)
- (step 3) `python3 plugin/tests/run.py test_settings_power test_settings test_settings_safety test_code_tui` → exit 0 · Ran 235 tests in 9.6s (39 classes, 16 at a time; slowest: Fuzz 9s, Command 9s, Events 4s) / OK [ran] [tree 90b3e7a5a588] (2026-10-22T22:22:46Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Profile 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|FAILED" | head -20` → ✗ exit 1 · Ran 15 tests in 3.0s (1 classes, 16 at a time; slowest: Profile 2s) / FAILED (1 classes) [ran] [tree 9c9ede564630] (2026-10-22T22:32:02Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Profile 2>&1 | grep -vE "^\s*$" | tail -40` → ✗ exit 1 · Ran 15 tests in 9.6s (1 classes, 16 at a time; slowest: Profile 8s) / FAILED (1 classes) [ran] [tree ca1133fa1050] (2026-10-22T22:34:45Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Profile 2>&1 | grep -vE "^\s*$" | tail -30` → exit 0 · Ran 15 tests in 7.9s (1 classes, 16 at a time; slowest: Profile 7s) / OK [ran] [tree 802d6d0336fa] (2026-10-22T22:35:24Z)
- (step 3) `python3 plugin/tests/run.py test_settings_power test_settings test_settings_safety test_code_tui` → exit 0 · Ran 243 tests in 11.6s (39 classes, 16 at a time; slowest: Fuzz 11s, Command 10s, Events 5s) / OK [ran] [tree cd51f64a14ed] (2026-10-22T22:37:10Z)
- (step 2) `python3 plugin/tests/run.py test_settings_power.Profile` → exit 0 · Ran 15 tests in 1.7s (1 classes, 16 at a time; slowest: Profile 1s) / OK [ran] [tree cd51f64a14ed] (2026-10-22T22:37:14Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power test_settings test_settings_safety test_code_tui` → exit 0 · Ran 243 tests in 10.4s (39 classes, 16 at a time; slowest: Fuzz 10s, Command 9s, Events 4s) / OK [ran] [tree d80a345cfdc5] (2026-10-22T22:53:44Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Profile` → exit 0 · Ran 15 tests in 1.4s (1 classes, 16 at a time; slowest: Profile 1s) / OK [ran] [tree d80a345cfdc5] (2026-10-22T22:53:46Z)
- (audit intent) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → settings profiles keyed to the terminal (ssh, tmux, width) pick the right overrides, and fm settings profile lists which applies and why [tree d80a345cfdc5] (2026-10-22T22:53:46Z)
- (audit adversary) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → profile names with a line break or U+202E print escaped in fm settings and the TUI; guard refusals keep their own escaping [tree d80a345cfdc5] (2026-10-22T22:53:46Z)
- (audit edge) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → no terminal → width unknown, no width_below profile applies and the output says so; a broken when is passed over, a bad value skipped with a note; COLUMNS=0 ignored [tree d80a345cfdc5] (2026-10-22T22:53:46Z)
- (audit operator) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → fm settings set and :set warn when a profile overrides the key on some terminals; export help says profiles aren't carried [tree d80a345cfdc5] (2026-10-22T22:53:46Z)
- (audit intent) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → settings profiles keyed to the terminal (ssh, tmux, width) pick the right overrides, and fm settings profile lists which applies and why [tree d80a345cfdc5] (2026-10-22T22:54:31Z)
- (audit adversary) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → profile names with a line break or U+202E print escaped in fm settings and the TUI; guard refusals keep their own escaping [tree d80a345cfdc5] (2026-10-22T22:54:31Z)
- (audit edge) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → no terminal → width unknown, no width_below profile applies and the output says so; a broken when is passed over, a bad value skipped with a note; COLUMNS=0 ignored [tree d80a345cfdc5] (2026-10-22T22:54:31Z)
- (audit operator) `fm-reviewer full pass on the lane; every finding fixed test-first (9 new tests failed first): escaped profile names, unknown width matches no width_below profile, silent-override notes after set/:set, empty when refused, print-config round-trips` → fm settings set and :set warn when a profile overrides the key on some terminals; export help says profiles aren't carried [tree d80a345cfdc5] (2026-10-22T22:54:31Z)
## Log
- 2026-10-22T20:58:42Z created
- 2026-10-22T20:58:43Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_power.py', 'CHANGELOG.md']
- 2026-10-22T20:58:44Z split from T-1544 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:01Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_settings_power.Profile`
- 2026-10-22T21:30:24Z criterion 1 text: given the environment the right profile is chosen and fm settings profile lists it — verify with python3 plugin/tests/run.py test_settings_power.Profile → given the environment the right profile is chosen and fm settings profile lists it
- 2026-10-22T22:12:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1656.builder.md
- 2026-10-22T22:12:53Z focused
- 2026-10-22T22:20:28Z scope: plugin/commands/settings.md (the /foreman:settings command lists fm settings profile, CC parity) and MASTER.md (one short addition), asked for by the main thread
- 2026-10-22T22:32:07Z review fixes (coordinator): 9 failing tests first in test_settings_power.Profile: escaping, unknown width, override notes, empty when, print-config tables, problem wording, normalised sets, screen glyph/about, export help
- 2026-10-22T22:53:23Z merged worktree-agent-ae59302fb7a4c2c00 (7 file(s))
- 2026-10-22T22:53:23Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae59302fb7a4c2c00
- 2026-10-22T22:53:26Z focused
- 2026-10-22T22:54:31Z scope: plugin/commands/settings.md and MASTER.md — the plugin's settings command and the system map describe profiles (CC plugin parity)
- 2026-10-22T22:55:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1544 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Settings power: profiles keyed to the terminal (ssh, tmux, TERM, width,
- research T-1572-review: Verdict:** approve with nits. The screen cannot write a value the schema rejects, and it cannot skip the guard or lock path, except in one narrow…
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_settings_power.py; re-ground the plan against them before editing
## Lessons
- Overrides that apply only on some terminals must say so where the value is set, or a user's set looks like it silently failed
## Plan gaps
- failed first: step 1 failing test with an env dict
## Files touched
- plugin/tests/test_settings_power.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- plugin/commands/settings.md
- CHANGELOG.md
- MASTER.md
