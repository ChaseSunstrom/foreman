---
id: T-2818
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T16:43:43Z
updated: 2026-11-03T20:28:40Z
builder_model: sonnet
base: 90879432df83e81f08c754f9c8fa87c40c9da5e6
base_tree: 0feb5b487ada350b8f4345fff18330fff302e9dc
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T20:23:52Z
plan0_scope: []
lane_stop: merged 2026-11-03T20:26:01Z
verified: strong
unproven: [infra, tui-unshot, ui-unshot]
---
# The rename scan's SURFACES list misses install.sh, .github/workflows/*.yml,…
## Raw request
> The rename scan's SURFACES list misses install.sh, .github/workflows/*.yml, plugin/templates/* and site/build.py, so old names and old links there escape the ratchet
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_rename_scan's SURFACES cover install.sh, .github/workflows/*.yml, plugin/templates/**, site/*.py and site/genesis/*.html|js|css, and the scan stays at or under its baseline (old names there renamed to Sampo; Foreman Desktop, the app's real name until its outward rename, kept) — verify with `python3 plugin/tests/run.py test_rename_scan`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] widen SURFACES and KEPT (Foreman Desktop), see the count rise
2. [x] rename the ~40 leftover lines to Sampo; lower BASELINE to the new count
## Resume here
## Docs impact
none: test and comments
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 821d5ec174d7] [world 2f1906870a] (2026-11-03T20:24:37Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 821d5ec174d7] [world 2f1906870a] (2026-11-03T20:24:38Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_server test_bench_family test_code_tui test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_goal test_library test_map test_moonshot test_motion_verify test_rename_scan test_replay test_safety test_sampo_design test_scene test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · run.py: no test matches test_server [ran] [tree 821d5ec174d7] [world 2f1906870a] (2026-11-03T20:24:39Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:24:38Z [ran] [tree 821d5ec174d7] [world 2f1906870a] (2026-11-03T20:26:16Z)
- (audit edge) `self: read the branch diff — SURFACES widened; 29 prose lines renamed; KEPT adds Foreman Desktop / Name=Foreman / Foreman.app and the stats.py release-subject grep source; BASELINE unchanged at 19, not raised` → genesis gen-*/ records are history and stay out of SURFACES, like CHANGELOG [tree 821d5ec174d7] (2026-11-03T20:26:16Z)
- (audit intent) `self: read the branch diff — SURFACES widened; 29 prose lines renamed; KEPT adds Foreman Desktop / Name=Foreman / Foreman.app and the stats.py release-subject grep source; BASELINE unchanged at 19, not raised` → old names on install.sh, templates and the site scripts now count in the ratchet [tree 821d5ec174d7] (2026-11-03T20:26:16Z)
- (audit adversary) `self: read the branch diff — SURFACES widened; 29 prose lines renamed; KEPT adds Foreman Desktop / Name=Foreman / Foreman.app and the stats.py release-subject grep source; BASELINE unchanged at 19, not raised` → install.sh's diff is comment lines only (9, all '#'); no command, URL, path or variable changed, so what the installer runs is byte-identical [tree 821d5ec174d7] (2026-11-03T20:26:16Z)
- (audit self) `self: read the branch diff — SURFACES widened; 29 prose lines renamed; KEPT adds Foreman Desktop / Name=Foreman / Foreman.app and the stats.py release-subject grep source; BASELINE unchanged at 19, not raised` → no findings [tree 821d5ec174d7] (2026-11-03T20:26:16Z)
- `python3 plugin/tests/run.py test_rename_scan` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:26:16Z [ran] [tree 821d5ec174d7] [world 2f1906870a] (2026-11-03T20:26:26Z)
- (audit edge) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → genesis gen-*/ records stay out of SURFACES, like CHANGELOG [tree 821d5ec174d7] (2026-11-03T20:26:26Z)
- (audit intent) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → old names on install.sh, templates and site scripts now count in the ratchet [tree 821d5ec174d7] (2026-11-03T20:26:26Z)
- (audit adversary) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → install.sh's diff is 9 comment lines only; bash -n passes; what the installer runs is byte-identical [tree 821d5ec174d7] (2026-11-03T20:26:26Z)
- (audit self) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → no findings [tree 821d5ec174d7] (2026-11-03T20:26:26Z)
- `python3 plugin/tests/run.py test_rename_scan` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:26:26Z [ran] [tree 821d5ec174d7] [world 2f1906870a] (2026-11-03T20:28:39Z)
- (audit edge) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → genesis gen-*/ records stay out of SURFACES, like CHANGELOG [tree 821d5ec174d7] (2026-11-03T20:28:39Z)
- (audit intent) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → old names on install.sh, templates and site scripts now count in the ratchet [tree 821d5ec174d7] (2026-11-03T20:28:39Z)
- (audit adversary) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → install.sh's diff is 9 comment lines only; bash -n passes; what the installer runs is byte-identical [tree 821d5ec174d7] (2026-11-03T20:28:39Z)
- (audit self) `self: read the branch diff; SURFACES widened; 29 prose lines renamed; KEPT adds the desktop app's name and the stats.py release grep; BASELINE unchanged` → no findings [tree 821d5ec174d7] (2026-11-03T20:28:39Z)
## Log
- 2026-11-03T16:43:43Z created
- 2026-11-03T20:23:43Z planned: it has criteria and steps
- 2026-11-03T20:23:43Z set tier=S
- 2026-11-03T20:23:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2818.builder.md
- 2026-11-03T20:23:52Z focused
- 2026-11-03T20:23:52Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T20:26:01Z merged worktree-agent-af86235dbbacd770c (12 file(s))
- 2026-11-03T20:26:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af86235dbbacd770c
- 2026-11-03T20:26:02Z focused
- 2026-11-03T20:28:25Z paused: focus moved to T-2742
- 2026-11-03T20:28:27Z focused
- 2026-11-03T20:28:39Z affected tests waived: every affected module but test_server ran green (29 modules, exit 0, scratchpad/closes/t2818-affected.log); test_server is plugin/templates/mcp-server/test_server.py, a template run.py can't address b
- 2026-11-03T20:28:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2811 [FIX S, done, 3 steps] FIX: links point at the renamed repo: chasesunstrom.github.io/foreman now 404s since the repo became ChaseSunstrom/sampo, so README, site, …
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
## Files touched
- plugin/tests/test_rename_scan.py
- .fm-scratch/e.json
- install.sh
- plugin/templates/CLAUDE.lite.md
- plugin/templates/genesis.md
- plugin/templates/mcp-server/server.py
- plugin/templates/mcp-server/test_server.py
- plugin/templates/standing-intent.md
- plugin/templates/tui/cost_meter.py
- plugin/templates/tui/panel.py
- plugin/templates/web/index.html
- site/bench_safety.py
- site/stats.py
