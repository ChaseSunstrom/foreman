---
id: T-3248
type: FEATURE
tier: M
status: active
priority: normal
scope: [site/assets/diagrams/*, plugin/tests/test_readme_diagrams.py, CHANGELOG.md, site/index.html]
depends_on: []
source: followup
created: 2026-11-05T21:12:35Z
updated: 2026-11-06T04:37:29Z
builder: 2026-11-05T23:56:14Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|3723|7619
lane: ~/.claude/foreman/.claude/worktrees/agent-a5d99302bb1fb7a77
lane_branch: worktree-agent-a5d99302bb1fb7a77
base: 1abcaddff1f0976804e109c8dc7fdaed858a4e0f
base_tree: 6ecf06a9cad7232547a96fa2661d24f0355b70b4
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T23:56:45Z
plan0_scope: [site/assets/diagrams/*, plugin/tests/test_readme_diagrams.py, CHANGELOG.md]
group: README figures and diagrams
---
# README diagrams (T-3245 part 2): redraw site/assets/diagrams loop, guard and architecture in Sampo's look and name (they still say Foreman), light and dark, gated by sampo works check
## Raw request
> README diagrams (T-3245 part 2): redraw site/assets/diagrams loop, guard and architecture in Sampo's look and name (they still say Foreman), light and dark, gated by sampo works check
## Interpretation
The three hand-made diagrams under site/assets/diagrams (loop, guard, architecture) still say Foreman and use the old look. Reading 1 (chosen): redraw each in Sampo's tokens and name, light and dark, same content. Reading 2: generate them from code; rejected: the shapes are hand-composed and rarely change.
## Assumptions (confidence)
## Acceptance criteria
- [ ] loop, guard and architecture exist as dark and light SVGs in Sampo's tokens, say Sampo (never Foreman) and pass sampo works check — verify with `python3 plugin/tests/run.py test_readme_diagrams`
## Non-goals
## Approach (options → choice → why)
1) use what exists: redraw the three SVGs by hand in the live page's tokens (colours from live.css), keep their structure, swap Foreman for Sampo, add a -dark variant each; sampo works check gates them. likely outcome: on-brand diagrams in both themes. 2) generate from a script: fails if: more code than the three drawings. 3) do less, recolour only: fails if: the name stays Foreman and dark mode is missing. Choice 1 (85%): three static drawings change rarely; hand-drawn keeps them crafted.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] failing test: no diagram says Foreman; both themes exist and pass works check  <- CURRENT
2. [x] redraw the three diagrams
## Resume here
<!-- auto -->
- 2026-11-06T04:34:19Z step 1/2: failing test: no diagram says Foreman; both themes exist and pass works check
- git: worktree-agent-a5d99302bb1fb7a77; 2 uncommitted: plugin/tests/test_readme_diagrams.py, site/index.html
- touched since last checkpoint: plugin/tests/test_readme_diagrams.py, site/index.html
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_readme_diagrams` → ✗ exit 1 · Ran 3 tests in 0.7s (1 jobs, 16 at a time; slowest: ReadmeDiagrams 0s) / FAILED (1 classes: test_readme_diagrams.ReadmeDiagrams) [ran] [tree 68a557f03c56] [world 2f1906870a] (2026-11-05T23:58:16Z)
- (step 2) `python3 plugin/tests/run.py test_readme_diagrams` → exit 0 · Ran 3 tests in 2.5s (1 jobs, 16 at a time; slowest: ReadmeDiagrams 0s) / OK [ran] [tree 7dd12d9dc341] [world 2f1906870a] (2026-11-06T00:23:28Z)
- (step 2) `nice sampo works check site/assets/diagrams/architecture-dark.svg site/assets/diagrams/architecture-light.svg` → exit 0 · ✓ unique: nearest 572 cells (bar > 4 of 576 cells off by > 96/255 from every earlier work that passed) / 2 of 2 works passed [ran] [tree 7dd12d9dc341] [world 2f1906870a] (2026-11-06T00:23:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_readme_diagrams test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1081 tests in 129.2s (227 jobs, 16 at a time; slowest: Ship 127s, GenesisRead 62s, GenesisCheck 61s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree 7dd12d9dc341] [world 2f1906870a] (2026-11-06T00:26:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_readme_diagrams test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [23.65s] [ran] [tree 9099cbb62122] [world 2f1906870a] (2026-11-06T00:28:37Z)
- (step 2) `nice -n 10 sampo works check site/assets/diagrams/loop-dark.svg site/assets/diagrams/loop-light.svg site/assets/diagrams/guard-dark.svg site/assets/diagrams/guard-light.svg` → ✗ exit 1 · ✗ unique: 0 cells from site/assets/diagrams/loop-light.svg (bar > 4 of 576 cells off by > 96/255 from every earlier work that passed) / 2 of 4 works passed [ran] [tree 7226444dbc55] [world 2f1906870a] (2026-11-06T04:36:01Z)
- (step 2) `nice -n 10 sampo works check site/assets/diagrams/loop-dark.svg site/assets/diagrams/loop-light.svg` → exit 0 · ✓ unique: nearest 576 cells (bar > 4 of 576 cells off by > 96/255 from every earlier work that passed) / 2 of 2 works passed [ran] [tree 7226444dbc55] [world 2f1906870a] (2026-11-06T04:36:19Z)
- (step 2) `nice -n 10 sampo works check site/assets/diagrams/guard-dark.svg site/assets/diagrams/guard-light.svg` → exit 0 · ✓ unique: nearest 567 cells (bar > 4 of 576 cells off by > 96/255 from every earlier work that passed) / 2 of 2 works passed [ran] [tree 7226444dbc55] [world 2f1906870a] (2026-11-06T04:36:59Z)
## Log
- 2026-11-05T21:12:35Z created
- 2026-11-05T23:56:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3248.builder.md
- 2026-11-05T23:56:42Z focused
- 2026-11-05T23:56:45Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-06T04:34:18Z criterion 1 verify: `python3 plugin/tests/run.py test_readme_figures` → `python3 plugin/tests/run.py test_readme_diagrams`
- 2026-11-06T04:37:24Z set scope=['site/assets/diagrams/*', 'plugin/tests/test_readme_diagrams.py', 'CHANGELOG.md', 'site/index.html']
- 2026-11-06T04:37:29Z scope: + site/index.html — review fix: the architecture img height 410 → 420 to match the redrawn 880x420 viewBox
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2052-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: approve with nits.** I read the brief, the diff and the ful…
- T-3245 [FEATURE L, planned, 6 steps] Completely update the README to the Sampo look with the charts and such; turn every…
- T-3247 [FEATURE M, active, 4 steps] README figures (T-3245 part 1): demo/readme_figures.py draws every README table and four real-data charts as light and dark SVGs in S…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
