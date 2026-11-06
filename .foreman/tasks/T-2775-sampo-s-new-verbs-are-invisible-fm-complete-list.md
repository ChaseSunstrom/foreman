---
id: T-2775
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli*.py, plugin/tests/test_rename_aliases.py, plugin/tests/test_help.py]
depends_on: []
source: discovered
created: 2026-11-03T04:52:06Z
updated: 2026-11-03T14:26:42Z
builder_model: sonnet
base: f0a45b19a6d917e4885844b6603835619899e82e
base_tree: bf26dcaadc16363b46041e003f51c156192df5c2
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-03T04:55:13Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli*.py, plugin/tests/test_rename_aliases.py]
lane_stop: merged 2026-11-03T05:10:13Z
verified: strong
---
# sampo's names show in completion and help: fm complete offers smith, rune, louhi, moons, underworld and ward and walks each to its old verb's subcommands; the shell hook completes sampo as well as fm; fm help --all lists the Sampo names with what each runs
## Raw request
> FEATURE: sampo's new verbs are invisible: fm complete lists none of smith, rune, louhi, moons, underworld or ward, and fm help never mentions them, so tab completion and help still teach only the old names (T-2766 follow-up, T-2742 step 5)
## Interpretation
Reading 1 (chosen): the new names exist (T-2766) but nothing teaches them: tab completion and fm help offer only the old verbs. Completion and help should offer both, derived from the one RENAMES map. Reading 2: replace the old verbs in help. Rejected: the old names stay first-class for two releases (SAMPO.md).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm complete '' lists the six Sampo names, fm complete rune '' lists genesis's subcommands, and the bash hook binds both fm and sampo — verify with `python3 plugin/tests/run.py test_rename_aliases test_cli`
- [x] fm help --all has a Sampo-names block naming what each runs, from RENAMES (not a second list) — verify with `python3 plugin/tests/run.py test_rename_aliases`
## Non-goals
## Approach (options → choice → why)
1) Derive from RENAMES: completion offers the keys and walks a key to its old verb's parser; help prints one block from RENAMES. Likely outcome: ~20 lines. Fails if: moons/underworld map to a subcommand path (genesis moonshot), so the walk must follow the whole list. 2) Use what exists: register the names as argparse aliases. Likely outcome: completion and help for free. Fails if: argparse aliases print the alias in usage and change parse results that T-2766's silent mapping deliberately avoids. 3) Do less: completion only. Fails if: fm help, the documented entry point, still never says sampo. Choice 1 (80%).
## Risks and rollback
Blast radius (fm graph blast): unknown, no co-change history for plugin/lib/sampo/cli.py, plugin/tests/test_rename_aliases.py.
## Execution prompt
## Steps
1. [x] red tests in test_rename_aliases for completion, the hook and help
2. [x] cmd_complete maps a typed Sampo name through RENAMES before walking; _BASH_HOOK binds sampo; cmd_help adds the block from RENAMES
3. [x] run test_rename_aliases and test_cli
## Resume here
## Docs impact
none: fm help --all is the doc
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_rename_aliases 2>&1 | tail -8` → ✗ exit 1 · Ran 8 tests in 20.2s (1 classes, 16 at a time; slowest: RenameAliases 13s) / FAILED (1 classes: test_rename_aliases.RenameAliases) [ran] [tree b6d5f20f38c2] [world 2f1906870a] (2026-11-03T04:56:19Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases test_cli 2>&1 | tail -12` → exit 0 · Ran 153 tests in 60.5s (45 classes, 16 at a time; slowest: TaskLifecycle 60s, CaptureAndIntake 24s, StateViews 23s) / OK [ran] [tree bec3891e6d43] [world 2f1906870a] (2026-11-03T04:57:34Z)
- (step 1) `python3 plugin/tests/run.py test_rename_aliases test_cli 2>&1 | tail -12` → exit 0 · Ran 153 tests in 60.5s (45 classes, 16 at a time; slowest: TaskLifecycle 60s, CaptureAndIntake 24s, StateViews 23s) / OK [ran] [tree bec3891e6d43] [world 2f1906870a] (2026-11-03T04:57:34Z)
- (step 3) `python3 plugin/tests/run.py test_rename_aliases test_cli` → exit 0 · Ran 153 tests in 48.1s (45 classes, 16 at a time; slowest: TaskLifecycle 47s, CaptureAndIntake 26s, StateViews 24s) / OK [ran] [tree bec3891e6d43] [world 2f1906870a] (2026-11-03T04:58:26Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_rename_aliases && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [59.78s] [ran] [tree bec3891e6d43] [world 2f1906870a] (2026-11-03T05:00:39Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases test_cli` → exit 0 · Ran 154 tests in 51.2s (45 classes, 16 at a time; slowest: TaskLifecycle 51s, CaptureAndIntake 22s, StateViews 22s) / OK [ran] [tree 71af56884018] [world 2f1906870a] (2026-11-03T14:25:47Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 12.5s (1 classes, 16 at a time; slowest: RenameAliases 12s) / OK [ran] [tree 71af56884018] [world 2f1906870a] (2026-11-03T14:25:47Z)
- (step 2) `python3 plugin/tests/run.py test_rename_aliases test_cli test_help` → exit 0 · Ran 160 tests in 66.1s (48 classes, 16 at a time; slowest: TaskLifecycle 65s, CaptureAndIntake 30s, StateViews 27s) / OK [ran] [tree 71af56884018] [world 2f1906870a] (2026-11-03T14:25:47Z)
- (audit intent) `self: read the merged diff; completion maps a typed Sampo name through RENAMES before walking, the hook binds sampo, help prints the block from RENAMES; fixed the help test that read the block as commands` → tab completion and fm help teach the Sampo names [tree 71af56884018] (2026-11-03T14:25:47Z)
- (audit edge) `self: read the merged diff; completion maps a typed Sampo name through RENAMES before walking, the hook binds sampo, help prints the block from RENAMES; fixed the help test that read the block as commands` → moons and underworld walk two-word paths; names only at the top level; a partial name completes by prefix; -p SLUG before the verb isn't walked (as before) [tree 71af56884018] (2026-11-03T14:25:47Z)
- (audit adversary) `self: read the merged diff; completion maps a typed Sampo name through RENAMES before walking, the hook binds sampo, help prints the block from RENAMES; fixed the help test that read the block as commands` → completion prints parser names only; nothing typed is executed [tree 71af56884018] (2026-11-03T14:25:47Z)
## Log
- 2026-11-03T04:52:06Z created
- 2026-11-03T04:54:33Z planned from capture
- 2026-11-03T04:54:35Z set approved=True
- 2026-11-03T04:54:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2775.builder.md
- 2026-11-03T04:55:11Z focused
- 2026-11-03T04:55:13Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T05:10:13Z merged worktree-agent-a5b4c2fcf5f46c180 (2 file(s))
- 2026-11-03T05:13:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5b4c2fcf5f46c180
- 2026-11-03T14:22:10Z focused
- 2026-11-03T14:22:12Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_cli*.py', 'plugin/tests/test_rename_aliases.py', 'plugin/tests/test_help.py']
- 2026-11-03T14:22:17Z scope: plugin/tests/test_help.py — the help test read the new Sampo-names block as six extra commands (a red on main after the merge); it now stops at the block
- 2026-11-03T14:26:40Z done
- 2026-11-03T14:26:42Z committed bf522960 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- T-2766 [FEATURE M, planned, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently a…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/tests/test_rename_aliases.py; re-ground the plan against them before editing
## Lessons
- A help block added below the tiers must not look like a tier line to the parsers that read help
## Files touched
- plugin/tests/test_rename_aliases.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_help.py
