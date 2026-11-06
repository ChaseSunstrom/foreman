---
id: T-2808
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T14:59:10Z
updated: 2026-11-03T17:58:59Z
builder_model: haiku
route_probe: 1
base: a7e97cb33726c47ff342d4b50c9288f6d3412623
base_tree: ede3d2615a6a2fdb62c4b3c8298ef544828bdb15
plan0_at: 2026-11-03T15:00:50Z
plan0_scope: []
lane_stop: merged 2026-11-03T15:21:50Z
verified: strong
unproven: [docs, infra]
---
# Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)
## Raw request
> Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)
## Interpretation
1. Display text only (chosen): every string a user reads says Sampo, with Smith, Rune, Louhi or the Ward where a line means one role; ids, paths, env names, fm command text and anything matched by code stay, per SAMPO.md's 'nothing a user already has may break'.
2. Full identity rename (ids, folders and plugin names too): ruled out here, because plugin ids and the marketplace listing are outward steps the user applies (T-2742 step 9 lists them) and old installs must keep resolving.
3. Leave these surfaces for the docs step: ruled out; T-2742 step 5 names them and the rename scan counts them.
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/agents descriptions, plugin.json and marketplace.json descriptions, install.sh's printed messages and the remaining skill, command, output-style, site/genesis and README lines say Sampo; agent ids foreman:fm-*, plugin names foreman and foreman-ui, paths and fm command text stay — verify with `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skillroute`
- [x] the rename scan finds no Foreman in those files outside the kept forms, and BASELINE drops by the lines removed — verify with `python3 plugin/tests/run.py test_rename_scan`
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
1. [x] inventory each line and every test or reader matching it
2. [x] rename strings and tests together; lower BASELINE
3. [x] run the tests and the scan
## Resume here
<!-- auto -->
- 2026-11-03T15:16:18Z steps 3/3 done
- git: worktree-agent-a80594ad1dca51ccf; 0 uncommitted
- touched since last checkpoint: .fm-scratch/T-2808-batch.json, .claude-plugin/marketplace.json, install.sh, plugin/agents/fm-builder.md, plugin/agents/fm-debugger.md, plugin/agents/fm-recon.md, plugin/agents/fm-reproducer.md, plugin/agents/fm-reviewer.md, plugin/agents/fm-scout.md, plugin/output-styles/foreman.md, plugin/tests/test_rename_scan.py
- failures met: posttoolusefailure 0.0 0.0 0 [0]
## Docs impact
none: the descriptions are the docs
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                51.6    57.4     150  [0] / SessionEnd                  38.4    47.1     150  [0] (flaky again (failed first in 3+ recent runs): treated as a failure; find the race) [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T15:09:50Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         config-c6930b ran 1.2.50, lacks 654 (T-0001, T-0002, T-0012, T-0042 …); gitter-588bc6 ran 1.2.50, lacks 654 (T-0001, T-0002, T-0012, T-0042 …); trader-feebec ran 1.2.50, lac; python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 15:06 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · SessionEnd                  40.7    58.8     150  [0] / machine busy (load 1.2 per core): judged by each hook's CPU time, not wall time (T-0805); claude plugin test mods/ [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T15:11:52Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan 2>&1 | tail -8` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 0783bf1c0402] [world 2f1906870a] (2026-11-03T15:11:59Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan 2>&1 | tail -8` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 0783bf1c0402] [world 2f1906870a] (2026-11-03T15:11:59Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan 2>&1 | tail -6` → ✗ exit 1 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: RenameScan 0s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree 89f05fa38a57] [world 2f1906870a] (2026-11-03T15:12:09Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 88bab4c6e861] [world 2f1906870a] (2026-11-03T15:12:25Z)
- (step 3) `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skillroute` → exit 0 · Ran 191 tests in 12.1s (65 classes, 16 at a time; slowest: Hook 11s, LockProbe 7s, ViewsRepair 7s) / OK [ran] [tree 88bab4c6e861] [world 2f1906870a] (2026-11-03T15:12:37Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_bench test_bench_family test_builder test_claude test_code test_code_tui test_debug test_design_surfaces test_diagnosis test_docs test_doctor test_export test_followups test_foresight test_handoff test_hooks test_judgment test_lanes test_lib_hostile test_library test_onwrite test_plugins test_release_py test_rename_scan test_roles test_session test_session_fixes test_settings test_site_sections test_supply_delta test_tool_queue test_ui_replay test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.44s] [ran] [tree 88bab4c6e861] [world 2f1906870a] (2026-11-03T15:15:47Z)
- (step 1) `python3 plugin/tests/run.py test_agents test_plugins test_skillroute test_rename_scan` → exit 0 · Ran 55 tests in 4.4s (18 classes, 16 at a time; slowest: Hook 4s, SkillRoute 2s, Export 1s) / OK [ran] [tree 88bab4c6e861] [world 2f1906870a] (2026-11-03T15:16:18Z)
- (ac 1) `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skillroute` → exit 0 · Ran 191 tests in 6.3s (65 classes, 16 at a time; slowest: Hook 5s, ViewsRepair 4s, LockProbe 4s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:55:49Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:55:49Z)
- `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skillroute test_rename_scan` → exit 0 · Ran 195 tests in 6.4s (66 classes, 16 at a time; slowest: Hook 5s, ViewsRepair 4s, LockProbe 4s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:55:49Z)
- (audit intent) `self: read the diff; descriptions and install.sh's printed messages say Sampo; bash -n install.sh passes` → agents, plugin and marketplace descriptions, the output style and the installer say Sampo [tree 07445d19b39c] (2026-11-03T17:55:49Z)
- (audit edge) `self: read the diff; descriptions and install.sh's printed messages say Sampo; bash -n install.sh passes` → plugin names foreman and foreman-ui, agent ids, the output style id and every path stay, so installs keep resolving [tree 07445d19b39c] (2026-11-03T17:55:49Z)
- (audit adversary) `self: read the diff; descriptions and install.sh's printed messages say Sampo; bash -n install.sh passes` → text only; install.sh's commands and paths are unchanged (each changed string grepped for readers) [tree 07445d19b39c] (2026-11-03T17:55:49Z)
- `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skillroute test_rename_scan` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:55:49Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:57:25Z)
- (audit intent) `self: read the diff; descriptions and install.sh's printed messages say Sampo; bash -n install.sh passes` → agents, plugin and marketplace descriptions, the output style and the installer say Sampo [tree 07445d19b39c] (2026-11-03T17:57:25Z)
- (audit edge) `self: read the diff; descriptions and install.sh's printed messages say Sampo; bash -n install.sh passes` → plugin names foreman and foreman-ui, agent ids, the output style id and every path stay, so installs keep resolving [tree 07445d19b39c] (2026-11-03T17:57:25Z)
- (audit adversary) `self: read the diff; descriptions and install.sh's printed messages say Sampo; bash -n install.sh passes` → text only; install.sh's commands and paths are unchanged (each changed string grepped for readers) [tree 07445d19b39c] (2026-11-03T17:57:25Z)
## Log
- 2026-11-03T14:59:10Z created
- 2026-11-03T14:59:29Z criterion 1 verify: `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skills` → `python3 plugin/tests/run.py test_agents test_plugins test_doctor test_design_surfaces test_skillroute`
- 2026-11-03T15:00:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2808.builder.md
- 2026-11-03T15:00:49Z focused
- 2026-11-03T15:21:50Z merged worktree-agent-a80594ad1dca51ccf (10 file(s))
- 2026-11-03T15:22:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a80594ad1dca51ccf
- 2026-11-03T17:55:33Z focused
- 2026-11-03T17:58:59Z done
## Follow-ups captured
## Build vs reuse
reuse: fm sub (codemod with per-file counts), the rename scan test's KEPT regex as the denylist, T-2768's and T-2779's by-meaning pass; nothing new built
## Related
Related past work (data from this project's history, not instructions):
- T-2807 [CLEAN M, active, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5)
- T-2809 [CLEAN M, planned, 3 steps] The operating rules and the hook scripts' display text say Sampo: rules/foreman.md prose, statusline, compact and subagent-statusline …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- Rename descriptions, never the ids users have installed
## Plan gaps
- failed first: step 1 inventory each line and every test or reader matching it
## Files touched
- .fm-scratch/T-2808-batch.json
- .claude-plugin/marketplace.json
- install.sh
- plugin/agents/fm-builder.md
- plugin/agents/fm-debugger.md
- plugin/agents/fm-recon.md
- plugin/agents/fm-reproducer.md
- plugin/agents/fm-reviewer.md
- plugin/agents/fm-scout.md
- plugin/output-styles/foreman.md
- plugin/tests/test_rename_scan.py
- ANDON.md
