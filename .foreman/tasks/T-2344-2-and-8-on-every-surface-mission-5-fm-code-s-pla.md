---
id: T-2344
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmmcp.py, plugin/lib/fmagents.py, site, mods/foreman-ui, plugin/tests/test_code.py, plugin/tests/test_mcp.py, plugin/tests/test_agents.py, plugin/tests/test_site.py]
depends_on: [T-2335, T-2337, T-2338, T-2339, T-2342, T-2343]
source: user
created: 2026-10-31T13:58:39Z
updated: 2026-10-31T19:39:54Z
builder_model: sonnet
base: 7958b82a8b9c688eb9e924b9dcfe0f7696445c2e
base_tree: 9b8fb6ebbd693d3f702dbfdeab9711abce76baf1
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T19:21:50Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmmcp.py, plugin/lib/fmagents.py, site, mods/foreman-ui, plugin/tests/test_code.py, plugin/tests/test_mcp.py, plugin/tests/test_agents.py, plugin/tests/test_site.py]
verified: strong
---
# #2 and #8 on every surface (Mission 5): fm code's planner writes readings, options with failure modes and a choice confidence and meets the same gate; an MCP calibration tool (read-only); the AGENTS.md block's plan line; Desktop through MCP; a site page; a pane band line; MASTER, README, CHANGELOG
## Raw request
> #2 and #8 on every surface (Mission 5): fm code's planner writes readings, options with failure modes and a choice confidence and meets the same gate; an MCP calibration tool (read-only); the AGENTS.md block's plan line; Desktop through MCP; a site page; a pane band line; MASTER, README, CHANGELOG
## Interpretation
Reading 1: gen-0's 'works on every surface it belongs on (Claude Code, fm code, other agents, Desktop)', a site page because it's user-facing and a pane line because it has state. Reading 2: CLI only, since plans are made in Claude Code. fm code files M tasks through its own planner, and calibration is state the user reads: Reading 1.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code's planner prompt and check_plan ask an M plan for 2+ readings (or why one), 3+ options each with a failure mode, and 'Choice N (NN%)', and the task it files passes fm focus's gate unchanged — verify with `python3 plugin/tests/run.py test_code -k PlanReadings`
- [x] the MCP tool list gains calibration (read-only: buckets, Brier beside the base rate, the bars, races run and how often the first choice lost, doors parked); the AGENTS.md block's plan line is rewritten in place to name the plan shape and fm calibration (no net growth); the site has a Calibrated judgment page built from fm calibration --json — verify with `python3 plugin/tests/run.py test_mcp test_agents test_site -k Judgment`
- [x] the pane band shows one line (doors parked, the Brier gap to the base rate) only when one needs action, and MASTER.md, README and CHANGELOG describe the plan shape, races, doors and fm calibration — verify with `python3 plugin/tests/run.py test_docs test_ui_signals -k Judgment`
## Non-goals
## Approach (options → choice → why)
1) each surface reads fm calibration --json and the shared plan gate, so no surface has a second implementation; fails if: fm code's planner output can't meet the gate, which its test proves. 2) use what exists: copy the goal page's pattern (T-2141: an MCP tool, a site page, a band line) per surface; fails if: copies drift from the CLI, so it is taken inside option 1 as the template, not as copies. 3) do less: MCP and docs only; fails if: gen-0's Completeness MUST names fm code, other agents and Desktop. 4) one generic Foreman state endpoint every surface polls; fails if: a new API for what fm calibration --json already prints. Choice 1 (80%): one source, each surface a thin reader.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (test_code PlanReadings; test_mcp, test_agents, test_site Judgment; test_docs Judgment)
2. [x] fm code planner and check_plan
3. [x] MCP calibration tool, AGENTS.md plan line, site page, pane band line
4. [x] MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code -k PlanReadings` → exit 0 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: PlanReadings 2s) / OK [ran] [tree a5a38fdbe5fe] (2026-10-31T19:27:14Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 451 tests in 66.0s (95 classes, 16 at a time; slowest: Worker 66s, Fakes 41s, Bench 17s) / OK [ran] [tree a5a38fdbe5fe] (2026-10-31T19:28:20Z)
- (step 3) `python3 plugin/tests/run.py test_ui_signals test_watch test_ui 2>&1 | grep -E "^(FAIL|ERROR):|^Ran .*s\)|^OK|^FAILED" | head -6` → exit 0 · Ran 58 tests in 17.1s (18 classes, 16 at a time; slowest: UiView 17s, GoalSignal 2s, Ship 2s) / OK [ran] [tree fc95cce3ebad] (2026-10-31T19:31:24Z)
- (step 4) `python3 plugin/tests/run.py test_agents test_export 2>&1 | grep -E "^(FAIL|ERROR):|^Ran .*s\)|^OK|^FAILED|Assertion" | head -6` → exit 0 · Ran 37 tests in 6.5s (12 classes, 16 at a time; slowest: Hook 6s, Export 5s, Install 2s) / OK [ran] [tree 7bdbc95a4732] (2026-10-31T19:32:31Z)
- (step 3) `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui_signals test_outcomes` → exit 0 · Ran 141 tests in 15.0s (52 classes, 16 at a time; slowest: Survival 15s, CalibrationLedgerBets 9s, ModelRouter 9s) / OK [ran] [tree a07184f0bfb1] (2026-10-31T19:34:56Z)
- (ac 2) `python3 plugin/tests/run.py test_mcp test_agents test_site -k Judgment` → exit 0 · Ran 3 tests in 0.4s (3 classes, 16 at a time; slowest: JudgmentTool 0s, JudgmentPage 0s, Judgment 0s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:37:05Z)
- (ac 3) `python3 plugin/tests/run.py test_docs test_ui_signals -k Judgment` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: JudgmentSignal 0s, Judgment 0s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:37:06Z)
- (ac 1) `python3 plugin/tests/run.py test_code -k PlanReadings` → exit 0 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: PlanReadings 2s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:37:09Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 135 tests in 8.4s (40 classes, 16 at a time; slowest: Fences 8s, Header 5s, DocsProof 3s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:37:19Z)
- `python3 plugin/tests/run.py test_code -k PlanReadings` → ✗ exit 1 · Ran 3 tests in 3.4s (1 classes, 16 at a time; slowest: PlanReadings 2s) / FAILED (1 classes: test_code.PlanReadings) (start tree + this task's tests) [ran] [tree 15d6d7f7402e] (2026-10-31T19:37:46Z)
- `python3 plugin/tests/run.py test_code -k PlanReadings` → exit 0 · Ran 3 tests in 3.3s (1 classes, 16 at a time; slowest: PlanReadings 3s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:37:46Z)
- (ac 1) `python3 plugin/tests/run.py test_code -k PlanReadings` → exit 0 · Ran 3 tests in 4.0s (1 classes, 16 at a time; slowest: PlanReadings 4s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:38:07Z)
- (ac 2) `python3 plugin/tests/run.py test_mcp test_agents test_site -k Judgment` → exit 0 · Ran 3 tests in 0.6s (3 classes, 16 at a time; slowest: JudgmentTool 0s, JudgmentPage 0s, Judgment 0s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:38:07Z)
- (ac 3) `python3 plugin/tests/run.py test_docs test_ui_signals -k Judgment` → exit 0 · Ran 4 tests in 1.5s (2 classes, 16 at a time; slowest: JudgmentSignal 1s, Judgment 0s) / OK [ran] [tree 15d6d7f7402e] (2026-10-31T19:38:07Z)
- (audit intent) `main-thread review of the diff (pace gate holds): every surface reads one source (fmoutcomes.snapshot, the plan gate's own _content_gaps), no copies; model text can't carry newlines into the brief; the rival fetch never blocks; S plans take the old path. Two catches fixed during the build: a fixed character bound in the AGENTS.md test would break on other install paths (bounded the line and line count instead), and the Judgment page had no figure while nothing is scored, which T-1784's every-page-has-a-figure rule caught (tiles always shown)` → fm code M plans meet the same gate (stub-checked before filing, real gate at focus); MCP calibration read-only (meta and ledger size unchanged, tested); band line only when a door is parked or stated Brier loses to the base rate; AGENTS.md plan line rewritten at 191 chars of 192; site Judgment page from fm calibration --json; MASTER, README, CHANGELOG [tree 15d6d7f7402e] (2026-10-31T19:38:07Z)
- (audit edge) `main-thread review of the diff (pace gate holds): every surface reads one source (fmoutcomes.snapshot, the plan gate's own _content_gaps), no copies; model text can't carry newlines into the brief; the rival fetch never blocks; S plans take the old path. Two catches fixed during the build: a fixed character bound in the AGENTS.md test would break on other install paths (bounded the line and line count instead), and the Judgment page had no figure while nothing is scored, which T-1784's every-page-has-a-figure rule caught (tiles always shown)` → one reading needs ruled_out; duplicate options are quoted back by the gate's own distinctness check; a model's confidence under the race bar gets the rival read before focus; an empty calibration renders zero tiles plus a not-scored note [tree 15d6d7f7402e] (2026-10-31T19:38:07Z)
- (audit maintainer) `main-thread review of the diff (pace gate holds): every surface reads one source (fmoutcomes.snapshot, the plan gate's own _content_gaps), no copies; model text can't carry newlines into the brief; the rival fetch never blocks; S plans take the old path. Two catches fixed during the build: a fixed character bound in the AGENTS.md test would break on other install paths (bounded the line and line count instead), and the Judgment page had no figure while nothing is scored, which T-1784's every-page-has-a-figure rule caught (tiles always shown)` → no second implementation of the plan gate or of calibration; the S path and its T-2335 exemption are unchanged and still tested [tree 15d6d7f7402e] (2026-10-31T19:38:07Z)
## Log
- 2026-10-31T13:58:39Z created
- 2026-10-31T16:02:36Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2344.builder.md
- 2026-10-31T16:02:36Z builder slot freed
- 2026-10-31T16:10:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2344.builder.md
- 2026-10-31T16:10:52Z builder slot freed
- 2026-10-31T19:21:49Z focused
- 2026-10-31T19:21:50Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T19:36:52Z criterion 3 verify: `python3 plugin/tests/run.py test_docs -k Judgment` → `python3 plugin/tests/run.py test_docs test_ui_signals -k Judgment`
- 2026-10-31T19:37:38Z scope: fmoutcomes (extras, snapshot, band_line: the one source every surface reads), fmwatch (the band signal), site/pages.py and site/stats.py (the Judgment page), README, MASTER, CHANGELOG, and tests test_docs, test_ui_signals, test_agents, test_site, test_mcp, test_code; plus other tasks' commits (T-2355, T-2438, T-2383) that landed while T-2344 was focused
- 2026-10-31T19:39:51Z done
- 2026-10-31T19:39:54Z committed 12009229 (16 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2378 [FEATURE M, planned, 4 steps] #5 on every surface (Mission 6): fm code's shell failures get the miss note and the same finish checks, other agents get it through …
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_claims.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_design_gates.py, plugi…
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcode.py, plugin/lib/fmmcp.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Lessons
- A surface added for a feature reads the feature's one source (a snapshot or the gate itself), never a copy; a page rule like 'every page has a figure' must hold when the data is empty
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- plugin/tests/test_mcp.py
- plugin/lib/fmmcp.py
- plugin/lib/fmoutcomes.py
- plugin/tests/test_ui_signals.py
- plugin/lib/fmwatch.py
- plugin/tests/test_agents.py
- plugin/lib/fmagents.py
- plugin/tests/test_site.py
- site/pages.py
- site/stats.py
- plugin/tests/test_docs.py
- README.md
- CHANGELOG.md
- MASTER.md
