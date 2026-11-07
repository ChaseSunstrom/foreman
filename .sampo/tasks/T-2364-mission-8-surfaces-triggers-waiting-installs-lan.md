---
id: T-2364
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmcp.py, plugin/lib/fmcore.py, plugin/lib/fmagents.py, site/pages.py]
depends_on: [T-2355, T-2374, T-2351, T-2406]
source: user
created: 2026-10-31T14:01:07Z
updated: 2026-11-01T05:32:20Z
builder_model: sonnet
base: e44eb7fbf77fdd5ec78d74b090d54ec14f599c88
base_tree: 1043968e52d3a0c257213a51fabcae7cafbacbaf
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-01T05:15:36Z
plan0_scope: [plugin/lib/fmmcp.py, plugin/lib/fmcore.py, plugin/lib/fmagents.py, site/pages.py]
inferred_deps: [T-2331]
inferred_why: T-2331: Mission 8 surfaces follow the mission-self build
group: Mission 8 surfaces
verified: strong
---
# Mission 8 surfaces: triggers, waiting installs, lane recoveries and self-fix verdicts on every surface (Mission 8, #7 #9 #11 #12)
## Raw request
> Mission 8 surfaces: triggers, waiting installs, lane recoveries and self-fix verdicts on every surface (Mission 8, #7 #9 #11 #12)
## Interpretation
Reading 1: Mission 8's state (triggers fired with routes, installs waiting for the yes, lanes recovering, self-fix trials due) shows on every surface gen-0's completeness MUST names: fm state, pane band, MCP, fm code, other agents, site, docs. Reading 2: document it in MASTER and README only. Rejected: the MUST names state surfaces, and a CLI-only capability is not done.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm state and the pane band carry one self-running line: triggers fired today with their routes, installs waiting for the yes, lanes recovering, self-fix trials due, and the prediction book's hit rate beside its baseline (T-2406) — verify with `python3 plugin/tests/run.py test_cli`
- [x] The MCP tool list gains a read-only triggers tool (table, recoveries, trials); fm code shows the same recovery action and line; the AGENTS.md block names fm night --tick and fm triggers — verify with `python3 plugin/tests/run.py test_mcp test_code test_agents`
- [x] The site gains a Self-running page (trigger precision and routes, installs waiting, recoveries, trial verdicts, prediction hit rates beside their baselines, the lean ratchet per generation); MASTER.md, README and CHANGELOG name it — verify with `python3 plugin/tests/run.py test_site`
## Non-goals
## Approach (options → choice → why)
1) One self-running line in fm state and the pane band (triggers fired today with routes, installs waiting for the yes, lanes recovering, trials due); a read-only MCP tool triggers, which Desktop reads there; fm code shows the same recovery action and line; the AGENTS.md block names fm night --tick and fm triggers; a site page; MASTER, README, CHANGELOG. Fails if: the line grows hook context, which stays one short line read from state. 2) Use what exists: the band and state line mechanisms of earlier missions, with new fields only. Likely outcome: the surfaces of #1 to #5 stay the pattern and each gets a test. 3) Do less: docs only. Fails if: the MUST names state surfaces. 4) A separate dashboard. Breaks upkeep: a new surface to keep in step. Choice 1 (85%): it extends the surfaces earlier missions built.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, MASTER.md, plugin/lib/fmhooks.py, plugin/tests/test_core.py; past FIXes T-0876, T-0907, T-0985, T-0986, T-0990.
## Execution prompt
## Steps
1. [x] red tests: state line; MCP tool; fm code line; AGENTS block; site page
2. [x] the surfaces
3. [x] docs: MASTER, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-11-01T05:23:37Z steps 3/3 done
- git: foreman/build; 17 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmagents.py, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcore.py, plugin/lib/fmmcp.py, plugin/lib/fmtriggers.py, plugin/lib/fmwatch.py
- touched since last checkpoint: plugin/tests/test_cli.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2364_edits.py, plugin/tests/test_agents.py, plugin/tests/test_code.py, plugin/tests/test_mcp.py, plugin/tests/test_site.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmtriggers.py, plugin/lib/fmmcp.py, plugin/lib/fmwatch.py, plugin/lib/fmagents.py, plugin/lib/fmcode.py, site/stats.py, site/pages.py
## Docs impact
MASTER.md (fmtriggers T-2364), README.md (Self-running line), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_mcp test_code test_agents test_site -k self_running -k triggers_tool -k agents_block_names_the_tick` → ✗ exit 1 · Ran 5 tests in 1.5s (5 classes, 16 at a time; slowest: SelfRunningNote 1s, SelfRunningLine 0s, TriggersTool 0s) / FAILED (5 classes: test_agents.SelfRunningAgentsLine, test_cli.SelfRunningLine, test_c [ran] [tree 4ad2ade2cfd0] (2026-11-01T05:17:45Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_mcp test_code test_agents test_site -k self_running -k triggers_tool -k agents_block_names_the_tick` → exit 0 · Ran 5 tests in 1.4s (5 classes, 16 at a time; slowest: SelfRunningNote 1s, SelfRunningLine 0s, TriggersTool 0s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:21:33Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_mcp test_code test_agents test_site -k self_running -k triggers_tool -k agents_block_names_the_tick` → exit 0 · Ran 5 tests in 1.4s (5 classes, 16 at a time; slowest: SelfRunningNote 1s, SelfRunningLine 0s, TriggersTool 0s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:21:35Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 138 tests in 8.3s (43 classes, 16 at a time; slowest: Fences 8s, Header 5s, DocsProof 2s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:21:44Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 142 tests in 20.0s (43 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:22:04Z)
- (ac 2) `python3 plugin/tests/run.py test_mcp test_code test_agents` → exit 0 · Ran 505 tests in 66.9s (120 classes, 16 at a time; slowest: Worker 67s, Fakes 41s, Bench 18s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:23:12Z)
- (ac 3) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 35 tests in 4.8s (19 classes, 16 at a time; slowest: Header 4s, Landing 2s, Session 1s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:23:17Z)
- `python3 plugin/tests/run.py test_cli test_mcp test_code test_agents test_site -k self_running -k triggers_tool -k agents_block_names_the_tick` → ✗ exit 1 · Ran 5 tests in 2.4s (5 classes, 16 at a time; slowest: SelfRunningNote 1s, SelfRunningLine 0s, TriggersTool 0s) / FAILED (5 classes: test_agents.SelfRunningAgentsLine, test_cli.SelfRunningLine, test_c (start tree + this task's tests) [ran] [tree 6937c180ac6e] (2026-11-01T05:23:21Z)
- `python3 plugin/tests/run.py test_cli test_mcp test_code test_agents test_site -k self_running -k triggers_tool -k agents_block_names_the_tick` → exit 0 · Ran 5 tests in 1.4s (5 classes, 16 at a time; slowest: SelfRunningNote 1s, SelfRunningLine 0s, TriggersTool 0s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:23:21Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 142 tests in 20.0s (43 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:30:33Z)
- (ac 2) `python3 plugin/tests/run.py test_mcp test_code test_agents` → exit 0 · Ran 505 tests in 66.9s (120 classes, 16 at a time; slowest: Worker 67s, Fakes 41s, Bench 18s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:30:33Z)
- (ac 3) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 35 tests in 4.8s (19 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree 6937c180ac6e] (2026-11-01T05:30:33Z)
- (audit intent) `fm check exit 0 (5503 tests); red→green per surface; fm task prove proved fails-without/passes-with; fm state timed 0.26 s with the new line` → one Self-running line answers what ran or waits by itself on fm state, the band, fm code, MCP triggers, AGENTS and the site; each reads fmtriggers.self_running, no second source [tree 6937c180ac6e] (2026-11-01T05:30:33Z)
- (audit adversary) `fm check exit 0 (5503 tests); red→green per surface; fm task prove proved fails-without/passes-with; fm state timed 0.26 s with the new line` → the line carries counts and trigger names only; trigger names come from Foreman's own table, the site page escapes text, the MCP tool is read-only argv [tree 6937c180ac6e] (2026-11-01T05:30:33Z)
- (audit edge) `fm check exit 0 (5503 tests); red→green per surface; fm task prove proved fails-without/passes-with; fm state timed 0.26 s with the new line` → nothing fired and nothing waiting prints no line (fm state, band, fm code stay quiet); a missing tick.json or trigger table reads as zero [tree 6937c180ac6e] (2026-11-01T05:30:33Z)
## Log
- 2026-10-31T14:01:07Z created
- 2026-10-31T16:07:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2364.builder.md
- 2026-10-31T16:07:35Z builder slot freed
- 2026-10-31T16:11:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2364.builder.md
- 2026-10-31T16:11:13Z builder slot freed
- 2026-10-31T17:12:08Z plan (second-plan review, taken): (1) each field's source named: triggers and routes from fmtriggers (T-2355), installs waiting from grant_queued (T-2374), recoveries from fmlanes stop marks (T-2354), trials due from T-2351, prediction hit rate from T-2406; a missing source prints nothing for that field, never an error; depends on those tasks; (2) criteria cover every surface named (state, pane band, fm code, MCP, site, docs, other agents via fmagents), each with a test; (3) one function builds the line, used by all surfaces, with a test that outputs are identical; (4) a worst-case fixture test caps the line at 160 chars with '+N more'.
- 2026-10-31T17:12:08Z set depends_on=['T-2355', 'T-2374', 'T-2351', 'T-2406']
- 2026-11-01T05:15:35Z focused
- 2026-11-01T05:15:36Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-01T05:17:43Z scope: tests in test_cli, test_mcp, test_code, test_agents, test_site; fmtriggers.self_running, fmcli cmd_state, fmwatch band signal, fmcode start note, site/stats.py; docs
- 2026-11-01T05:21:26Z scope: tests in test_cli, test_mcp, test_code, test_agents, test_site; fmtriggers.self_running and its JSON; fmcli cmd_state; fmwatch band signal; fmcode start note; site/stats.py; docs MASTER, README (inside details), CHANGELOG
- 2026-11-01T05:32:17Z done
- 2026-11-01T05:32:20Z committed a3b7b352 (17 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The state line and pane band depend on data that this task doesn't produce. Triggers fired with routes, installs waiting, recoveries, trials due and the prediction hit rate (T-2406) must already exist in state. Neither the plan nor its steps say where each field is read from, or what happens …
- HIGH: The acceptance criteria cover only 3 of the 7 surfaces the interpretation names. Missing are "other agents" and docs beyond the three named files. The pane band is claimed but verified only by `test_cli`. The interpretation rejected "CLI-only is done", yet nothing proves the surface list is c…
- MEDIUM: The hook-context constraint is "one short line read from state", but nothing enforces it. A growing line (many triggers, long routes) silently bloats every session. — Add a test that asserts a max length or item count with truncation, such as "+N more", on a worst-case state fixture.
- MEDIUM: The site page and MCP tool are broader than the line. The page includes precision, per-generation lean ratchet and baselines, and the MCP tool includes the table, recoveries and trials. These data sources are not identified, and the criteria only say the tests pass. Weak assertions like "pa…
- MEDIUM: "fm code shows the same recovery action and line" is vague. It is unclear whether that is a shared function or duplicated formatting, and duplication drifts. — Build the line once in a single function used by state, band, code and MCP. Test that all outputs are identical for the same fixtur…
- LOW: There is no rollback or staging note. These touch the shared hook and band output, and a bug there affects every session. Option 2 ("use what exists") is also the real plan but is listed as an alternative. — Make the line failure-safe: on a read error, print nothing and never raise in the hook…
Verdict: revise — the data sources and the T-2406 dependency are unspecified, and the criteria don't prove all the surfaces or the line-size limit, so the red tests could pass without proving the request.
## Dissent
- [ ] HIGH: The state line and pane band depend on data that this task doesn't produce. Triggers fired with routes, installs waiting, recoveries, trials due and the prediction hit rate (T-2406) must already exist in state. Neither the plan nor its steps say where each field is read from, or what happens …
- [ ] HIGH: The acceptance criteria cover only 3 of the 7 surfaces the interpretation names. Missing are "other agents" and docs beyond the three named files. The pane band is claimed but verified only by `test_cli`. The interpretation rejected "CLI-only is done", yet nothing proves the surface list is c…
- [ ] MEDIUM: The hook-context constraint is "one short line read from state", but nothing enforces it. A growing line (many triggers, long routes) silently bloats every session. — Add a test that asserts a max length or item count with truncation, such as "+N more", on a worst-case state fixture.
- [ ] MEDIUM: The site page and MCP tool are broader than the line. The page includes precision, per-generation lean ratchet and baselines, and the MCP tool includes the table, recoveries and trials. These data sources are not identified, and the criteria only say the tests pass. Weak assertions like "pa…
- [ ] MEDIUM: "fm code shows the same recovery action and line" is vague. It is unclear whether that is a shared function or duplicated formatting, and duplication drifts. — Build the line once in a single function used by state, band, code and MCP. Test that all outputs are identical for the same fixtur…
- [ ] LOW: There is no rollback or staging note. These touch the shared hook and band output, and a bug there affects every session. Option 2 ("use what exists") is also the real plan but is listed as an alternative. — Make the line failure-safe: on a read error, print nothing and never raise in the hook…
## Related
Related past work (data from this project's history, not instructions):
- T-2378 [FEATURE M, done, 4 steps] #5 on every surface (Mission 6): fm code's shell failures get the miss note and the same finish checks, other agents get it through fma…
- T-2395 [FEATURE M, done, 4 steps] Proof surfaces (Mission 7, #6/#10): the rollup by kind on MCP, the pane, fm code, the AGENTS.md block, Desktop through MCP and a site p…
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_core.py, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint…
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmagents.py, plugin/lib/fmcore.py, plugin/lib/fmmcp.py, site/pages.py; re-ground the plan against them before editing
## Lessons
- One summary function feeding every surface keeps them from drifting; the surface parity test (ui-demo.json) catches a new field missing from the demo
## Plan gaps
- failed first: step 1 red tests: state line; MCP tool; fm code line; AGENTS block; site page
## Files touched
- plugin/tests/test_cli.py
- plugin/tests/test_agents.py
- plugin/tests/test_code.py
- plugin/tests/test_mcp.py
- plugin/tests/test_site.py
- plugin/lib/fmtriggers.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmmcp.py
- plugin/lib/fmwatch.py
- plugin/lib/fmagents.py
- plugin/lib/fmcode.py
- site/stats.py
- site/pages.py
- CHANGELOG.md
- MASTER.md
- README.md
