---
id: T-2807
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T14:59:06Z
updated: 2026-11-03T17:55:31Z
builder_model: haiku
route_probe: 1
base: 7d3e5abf68582f371dd025c7ea08838c81fcaa10
base_tree: 908dcba00dc9c1de3316a5a18cf37bc353c7f21e
plan0_at: 2026-11-03T15:00:48Z
plan0_scope: []
lane_stop: merged 2026-11-03T15:20:45Z
verified: strong
unproven: [ui-unshot]
---
# The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5)
## Raw request
> The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5)
## Interpretation
1. Display text only (chosen): every string a user reads says Sampo, with Smith, Rune, Louhi or the Ward where a line means one role; ids, paths, env names, fm command text and anything matched by code stay, per SAMPO.md's 'nothing a user already has may break'.
2. Full identity rename (ids, folders and plugin names too): ruled out here, because plugin ids and the marketplace listing are outward steps the user applies (T-2742 step 9 lists them) and old installs must keep resolving.
3. Leave these surfaces for the docs step: ruled out; T-2742 step 5 names them and the rename scan counts them.
## Assumptions (confidence)
## Acceptance criteria
- [x] the pane, band, toasts and mod README say Sampo (role names where a row means one); the plugin id foreman-ui@foreman, its folder, FOREMAN_* and fm command text stay — verify with `claude plugin test mods/foreman-ui`
- [x] the rename scan finds no Foreman under mods/foreman-ui outside the kept forms, and BASELINE drops by the lines removed — verify with `python3 plugin/tests/run.py test_rename_scan test_statusline_ui`
## Non-goals
## Approach (options → choice → why)
1. Sweep with fm sub, then a by-meaning pass (chosen): fm sub for the mechanical 'Foreman' → 'Sampo' over display strings with a denylist of kept forms, then read each changed line by meaning and grep every test or code reader of each string (T-2779's lesson). Likely outcome: one green commit. Fails if: a string is matched by a regex elsewhere and the grep misses it; the targeted tests catch most.
2. Hand edit line by line. Likely outcome: same result, several times slower on hundreds of lines. Fails if: fatigue misses lines; no better on readers.
3. A display-name constant read everywhere (NAME = 'Sampo'). Likely outcome: more diff and an abstraction for a value that never changes again. Fails if: strings in markdown, JSON and TSX can't import it anyway.
4) use what exists: fm sub plus the rename scan's KEPT regex as the denylist, as T-2768 and T-2779 did. Likely outcome: this is option 1's tooling; nothing new built. Fails if: KEPT misses a kept form; the by-meaning pass catches it.
5) do less: rename only what the scan counts and leave the tests' fixture strings. Likely outcome: fewer lines but tests asserting old display text go red. Fails if: any test matches a renamed string, which most here do.
Choice: 1 with 4's tooling (85%).
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py.
## Execution prompt
## Steps
1. [x] inventory the mod's visible strings and every test or reader that matches one
2. [x] rename strings and tests together; lower BASELINE
3. [x] run the mod's tests and the scan
## Resume here
<!-- auto -->
- 2026-11-03T15:13:53Z step 2/3: rename strings and tests together; lower BASELINE
- git: worktree-agent-aea286d13c7c8852b; 14 uncommitted: mods/foreman-ui/README.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/fixtures/golden.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tests/pane-hostile.test.tsx, mods/foreman-ui/tests/pane-sweep.test.tsx, mods/foreman-ui/tests/replay.test.tsx
- touched since last checkpoint: mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/pane-hostile.test.tsx, mods/foreman-ui/tests/pane-sweep.test.tsx, mods/foreman-ui/tests/replay.test.tsx, mods/foreman-ui/tools/pane_replay.py, mods/foreman-ui/tools/shot.py, mods/foreman-ui/types/index.d.ts, .fm-scratch/rename1.json, mods/foreman-ui/README.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tests/fixtures/golden.ts, plugin/tests/test_rename_scan.py
- failures met: posttoolusefailure 0.0 0.0 0 [0]
## Docs impact
mods/foreman-ui/README.md
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · SessionEnd                  39.9    59.5     150  [0] / machine busy (load 1.2 per core): judged by each hook's CPU time, not wall time (T-0805) (flaky again (failed first in 3+ recent runs): treated as a failure; find the race) [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T15:11:06Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 15:11 UTC) [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T15:12:26Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 15:11 UTC) [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T15:12:34Z)
- (step 1) `fm check --evidence T-2807 --step 1` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 15:11 UTC); cached (fm check --fresh reruns) [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T15:12:34Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.43s] [ran] [tree b12592e1dda0] [world 2f1906870a] (2026-11-03T15:15:52Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.43s] [ran] [tree b12592e1dda0] [world 2f1906870a] (2026-11-03T15:15:52Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.23s] [ran] [tree b12592e1dda0] [world 2f1906870a] (2026-11-03T15:16:07Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui 2>&1 | tail -n 6` → ✗ exit 1 · Ran 9 tests in 1.7s (2 classes, 16 at a time; slowest: StatuslineUi 1s, RenameScan 0s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree 919c8b01941f] [world 2f1906870a] (2026-11-03T15:16:33Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui 2>&1 | tail -n 4` → exit 0 · Ran 9 tests in 2.3s (2 classes, 16 at a time; slowest: StatuslineUi 2s, RenameScan 0s) / OK [ran] [tree 5286c34584c2] [world 2f1906870a] (2026-11-03T15:16:44Z)
- (step 3) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui 2>&1 | tail -n 4` → exit 0 · Ran 9 tests in 2.3s (2 classes, 16 at a time; slowest: StatuslineUi 2s, RenameScan 0s) / OK [ran] [tree 5286c34584c2] [world 2f1906870a] (2026-11-03T15:16:44Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui` → exit 0 · Ran 9 tests in 2.2s (2 classes, 16 at a time; slowest: StatuslineUi 2s, RenameScan 0s) / OK [ran] [tree 5286c34584c2] [world 2f1906870a] (2026-11-03T15:16:49Z)
- (step 3) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui` → exit 0 · Ran 9 tests in 2.1s (2 classes, 16 at a time; slowest: StatuslineUi 2s, RenameScan 0s) / OK [ran] [tree 5286c34584c2] [world 2f1906870a] (2026-11-03T15:17:07Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.54s] [ran] [tree 5286c34584c2] [world 2f1906870a] (2026-11-03T15:17:21Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_claims test_code_tui test_design_surfaces test_docsdrift test_plugins test_rename_scan test_replay test_settings test_shot test_suite_hygiene test_supply_delta test_ui test_ui_replay && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.39s] [ran] [tree 3c4c840753eb] [world 2f1906870a] (2026-11-03T15:18:16Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 153 tests across 4 files. [34.12s] [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:54:32Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui` → exit 0 · Ran 11 tests in 5.8s (2 classes, 16 at a time; slowest: StatuslineUi 5s, RenameScan 2s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:54:32Z)
- (audit intent) `self: read the diff and the merge with T-2779 (where both renamed a line, T-2779's Ward wording was kept); claude plugin test mods/foreman-ui 153 pass` → the pane, band, toasts and mod README say Sampo [tree 07445d19b39c] (2026-11-03T17:54:32Z)
- (audit edge) `self: read the diff and the merge with T-2779 (where both renamed a line, T-2779's Ward wording was kept); claude plugin test mods/foreman-ui 153 pass` → code-matched strings (pane id, skill namespace, guard prefixes) stay and are listed in KEPT; the mod id, folder and FOREMAN_* stay [tree 07445d19b39c] (2026-11-03T17:54:32Z)
- (audit adversary) `self: read the diff and the merge with T-2779 (where both renamed a line, T-2779's Ward wording was kept); claude plugin test mods/foreman-ui 153 pass` → display text only; the guard-refusal regex accepts Foreman, Sampo and Ward so older refusals still parse [tree 07445d19b39c] (2026-11-03T17:54:32Z)
## Log
- 2026-11-03T14:59:06Z created
- 2026-11-03T15:00:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2807.builder.md
- 2026-11-03T15:00:47Z focused
- 2026-11-03T15:20:45Z merged worktree-agent-aea286d13c7c8852b (4 file(s))
- 2026-11-03T15:20:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aea286d13c7c8852b
- 2026-11-03T17:53:46Z focused
- 2026-11-03T17:55:31Z done
## Follow-ups captured
## Build vs reuse
reuse: fm sub (codemod with per-file counts), the rename scan test's KEPT regex as the denylist, T-2768's and T-2779's by-meaning pass; nothing new built
## Related
Related past work (data from this project's history, not instructions):
- T-2808 [CLEAN M, planned, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step…
- T-2809 [CLEAN M, planned, 3 steps] The operating rules and the hook scripts' display text say Sampo: rules/foreman.md prose, statusline, compact and subagent-statusline …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Lessons
- Merge overlapping renames by keeping the wording that names the role
## Plan gaps
- failed first: step 1 inventory the mod's visible strings and every test or reader that matches one
## Files touched
- mods/foreman-ui/README.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/fixtures/golden.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/tests/pane-hostile.test.tsx
- mods/foreman-ui/tests/pane-sweep.test.tsx
- mods/foreman-ui/tests/replay.test.tsx
- mods/foreman-ui/tools/pane_replay.py
- mods/foreman-ui/tools/shot.py
- mods/foreman-ui/types/index.d.ts
- .fm-scratch/rename1.json
- plugin/tests/test_rename_scan.py
- .fm-scratch/rename2.json
- mods/foreman-ui/.claude-plugin/plugin.json
- .fm-scratch/kept.pl
- ANDON.md
