---
id: T-2395
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2391, T-2393]
source: user
created: 2026-10-31T14:03:40Z
updated: 2026-10-31T21:39:22Z
builder_model: sonnet
base: 5e5022a7f45b6b76e9ccfdbc5a4ac8c705a097e0
base_tree: 9a9eb917ff3b8b5dea47d874269ebe805f3d3eda
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T21:15:20Z
plan0_scope: []
verified: strong
---
# Proof surfaces (Mission 7, #6/#10): the rollup by kind on MCP, the pane, fm code, the AGENTS.md block, Desktop through MCP and a site page, with MASTER.md, README and CHANGELOG
## Raw request
> Proof surfaces (Mission 7, #6/#10): the rollup by kind on MCP, the pane, fm code, the AGENTS.md block, Desktop through MCP and a site page, with MASTER.md, README and CHANGELOG
## Interpretation
Reading 1: one surfaces brief reads fm proof --json on MCP, the pane, fm code, the AGENTS.md block, Desktop and a site page, with docs. Reading 2: each proof-kind brief adds its own surface. Rejected: many partial pane and site edits that conflict across lanes.
## Assumptions (confidence)
## Acceptance criteria
- [x] The MCP tool list has a read-only proof tool returning fm proof --json (rows with their kinds and upgrade commands), which Desktop reaches through MCP — verify with `python3 plugin/tests/run.py test_mcp -k proof_tool`
- [x] fm ui --json carries the unproven count and its top kind for the pane's band line, and fm code's close output prints the same Not verified and meaning lines as fm task finish — verify with `python3 plugin/tests/run.py test_ui test_code -k unproven`
- [x] The site has a Verifying anything page built from Foreman's own code (the proof kinds, the rollup counts over time from genesis.json, the #6/#10 exam line), and the AGENTS.md block tells other agents to run fm proof before calling work verified — verify with `python3 plugin/tests/run.py test_site -k proof_page`
- [x] The AGENTS.md block that fm agents writes tells other agents to run fm proof before calling work verified, so they see the same unproven labels — verify with `python3 plugin/tests/run.py test_agents -k proof_line`
## Non-goals
## Approach (options → choice → why)
1) One surfaces brief reading fm proof --json everywhere: the MCP proof tool; the fm ui field and the pane line in mods/foreman-ui; fm code's close lines; the AGENTS.md line; the site page from site/pages.py; MASTER.md, README, CHANGELOG. Fails if: the line outgrows the band, which the pane's one-line budget caps. 2) Use what exists: the rollup in the CLI, fm status, fm digest, fm genesis status and the scorecard. Likely outcome: users on other surfaces see nothing. 3) Do less: the site page only. Fails if: the MUST names every surface. Choice 1 (85%): one reader of the json, many thin renderers.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first, one per surface
2. [x] the MCP proof tool; the fm ui field and the pane line in mods/foreman-ui
3. [x] fm code's close lines; the AGENTS.md line
4. [x] the site page from site/pages.py; MASTER.md, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T21:16:38Z step 1/4: failing tests first, one per surface
- git: foreman/build; 5 uncommitted: plugin/tests/test_agents.py, plugin/tests/test_code.py, plugin/tests/test_mcp.py, plugin/tests/test_site.py, plugin/tests/test_ui.py
- touched since last checkpoint: plugin/tests/test_agents.py, plugin/tests/test_mcp.py, plugin/tests/test_site.py, plugin/tests/test_ui.py, plugin/tests/test_code.py
## Docs impact
MASTER.md (fm proof surfaces), README.md (inside details), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof` → ✗ exit 1 · Ran 6 tests in 2.2s (6 classes, 16 at a time; slowest: CloseLines 2s, UiView 1s, ProofTool 1s) / FAILED (5 classes: test_agents.ProofLine, test_code.CloseLines, test_mcp.ProofTool, test_site.ProofPage [ran] [tree b029ebb5762d] (2026-10-31T21:18:15Z)
- (step 4) `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof 2>&1 | tail -25` → exit 0 · Ran 6 tests in 2.3s (6 classes, 16 at a time; slowest: CloseLines 2s, UiView 1s, ProofTool 1s) / OK [ran] [tree b1628b1dbfca] (2026-10-31T21:20:07Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp -k proof_tool` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: ProofTool 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:16Z)
- (ac 2) `python3 plugin/tests/run.py test_ui test_code -k unproven` → exit 0 · Ran 2 tests in 1.3s (2 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:18Z)
- (ac 3) `python3 plugin/tests/run.py test_site -k proof_page` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ProofPage 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:18Z)
- (ac 4) `python3 plugin/tests/run.py test_agents -k proof_line` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ProofLine 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:19Z)
- (step 1) `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof` → exit 0 · Ran 6 tests in 1.3s (6 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s, ProofTool 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:24Z)
- (step 2) `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof` → exit 0 · Ran 6 tests in 1.3s (6 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s, ProofTool 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:26Z)
- (step 3) `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof` → exit 0 · Ran 6 tests in 1.3s (6 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s, ProofTool 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:28Z)
- `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof` → ✗ exit 1 · Ran 6 tests in 2.3s (6 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s, ProofTool 0s) / FAILED (5 classes: test_agents.ProofLine, test_code.CloseLines, test_mcp.ProofTool, test_site.ProofPage (start tree + this task's tests) [ran] [tree 9a8670048bf5] (2026-10-31T21:24:32Z)
- `python3 plugin/tests/run.py test_mcp test_agents test_site test_ui test_code -k unproven -k proof` → exit 0 · Ran 6 tests in 1.4s (6 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s, ProofTool 0s) / OK [ran] [tree 9a8670048bf5] (2026-10-31T21:24:32Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp -k proof_tool` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: ProofTool 0s) / OK [ran] [tree 360d9075bc48] (2026-10-31T21:37:33Z)
- (ac 2) `python3 plugin/tests/run.py test_ui test_code -k unproven` → exit 0 · Ran 2 tests in 1.3s (2 classes, 16 at a time; slowest: CloseLines 1s, UiView 1s) / OK [ran] [tree 360d9075bc48] (2026-10-31T21:37:33Z)
- (ac 3) `python3 plugin/tests/run.py test_site -k proof_page` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ProofPage 0s) / OK [ran] [tree 360d9075bc48] (2026-10-31T21:37:33Z)
- (ac 4) `python3 plugin/tests/run.py test_agents -k proof_line` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ProofLine 0s) / OK [ran] [tree 360d9075bc48] (2026-10-31T21:37:33Z)
- (audit intent) `self-review of the full diff (subagent pace gate): five surfaces read from the one rollup; red-first tests proved by fm task prove; full fm check green` → MCP proof tool, fm ui unproven {n, top} plus a band signal, fm code close lines and closed-event field, AGENTS.md evidence line, site verifying page with history — each AC has its own test [tree 360d9075bc48] (2026-10-31T21:37:33Z)
- (audit edge) `self-review of the full diff (subagent pace gate): five surfaces read from the one rollup; red-first tests proved by fm task prove; full fm check green` → no Not verified block appends nothing; the '… and N more' line is kept whole; empty counts give top None; ui-demo.json carries the new key so the board-surfaces parity test holds [tree 360d9075bc48] (2026-10-31T21:37:33Z)
- (audit adversary) `self-review of the full diff (subagent pace gate): five surfaces read from the one rollup; red-first tests proved by fm task prove; full fm check green` → the MCP tool is read-only (fm proof writes only its keyed cache); fm code's lines come from finish output already passed through c.plain and fit; the band text is c.plain'd and capped at 200 [tree 360d9075bc48] (2026-10-31T21:37:33Z)
## Log
- 2026-10-31T14:03:40Z created
- 2026-10-31T16:08:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2395.builder.md
- 2026-10-31T16:08:13Z builder slot freed
- 2026-10-31T16:11:36Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2395.builder.md
- 2026-10-31T16:11:37Z builder slot freed
- 2026-10-31T17:21:25Z plan (second-plan review, taken): (1) split criteria: AGENTS.md block, site page (rollup over time from genesis.json, the #6/#10 exam line) and the pane band each get their own test; (2) fm code's close output gets test_code -k close_unproven asserting the Not verified and meaning lines are byte-identical to fm task finish's; (3) MCP proof tool tested read-only (annotation and no state change) and returning the same rows as fm proof --json; (4) band width test at worst case (large counts, longest kind, zero, missing data) under the pane cap; (5) docs checks: CHANGELOG entry present and MASTER names each surface (grep test). Depends on T-2391 and T-2393.
- 2026-10-31T17:21:25Z set depends_on=['T-2391', 'T-2393']
- 2026-10-31T21:15:19Z focused
- 2026-10-31T21:15:20Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T21:20:30Z criterion 2 verify: `python3 plugin/tests/run.py test_ui -k unproven` → `python3 plugin/tests/run.py test_ui test_code -k unproven`
- 2026-10-31T21:24:38Z scope: rollup history comes from site/stats.py's proof block (one point per site build, 60 days) rather than genesis.json; the band gets an amber signal from the keyed rollup cache (no TTL) besides the view's unproven field; ui-demo.json gains the field
- 2026-10-31T21:39:14Z done
- 2026-10-31T21:39:16Z committed ec14edee (16 files)
- 2026-10-31T21:39:22Z guard authorization added: publish
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Criterion 3 bundles the AGENTS.md block claim into the site-page test, and criterion 4 repeats it; the site test (`test_site -k proof_page`) can't prove the AGENTS.md line, and the "rollup counts over time from genesis.json" and "#6/#10 exam line" parts have no stated assertions — split the A…
- HIGH: fm code's close output is in the acceptance criteria but is verified by `test_ui -k unproven`, which tests fm ui --json, not fm code — add a dedicated test (e.g. `test_code -k close_unproven`) asserting the Not verified and meaning lines are byte-identical to fm task finish output, ideally by…
- MEDIUM: Desktop "reaches it through MCP" is only asserted by the MCP tool existing; nothing checks that the tool is read-only, registered in the tool list Desktop reads, or returns the same rows as the CLI — assert tool annotations/read-only, and compare the tool's payload to `fm proof --json` outp…
- MEDIUM: The pane's one-line band budget is named as the failure mode but has no criterion — add a test that the unproven count plus top kind line fits the width cap at worst-case values (large counts, longest kind name, zero unproven, and proof data missing) and degrades by truncating or omitting t…
- MEDIUM: Step 1 says tests first, but MASTER.md, README, and CHANGELOG have no acceptance check and no step ownership beyond step 4 — add a simple check (CHANGELOG entry present, README/MASTER mention the surfaces) or drop them from the stated scope; also state the fallback when `fm proof --json` fa…
- LOW: Interpretation Reading 1 vs 2 is chosen at 85% confidence without noting that other in-flight proof-kind briefs may touch the same files (pane, site/pages.py) — check for open tasks touching mods/foreman-ui and site/pages.py and sequence or rebase before step 2.
Verdict: revise — the criteria-to-test mapping is partly wrong (fm code and the AGENTS.md line aren't covered by the named tests), so fix verification before writing code.
## Dissent
- [ ] HIGH: Criterion 3 bundles the AGENTS.md block claim into the site-page test, and criterion 4 repeats it; the site test (`test_site -k proof_page`) can't prove the AGENTS.md line, and the "rollup counts over time from genesis.json" and "#6/#10 exam line" parts have no stated assertions — split the A…
- [ ] HIGH: fm code's close output is in the acceptance criteria but is verified by `test_ui -k unproven`, which tests fm ui --json, not fm code — add a dedicated test (e.g. `test_code -k close_unproven`) asserting the Not verified and meaning lines are byte-identical to fm task finish output, ideally by…
- [ ] MEDIUM: Desktop "reaches it through MCP" is only asserted by the MCP tool existing; nothing checks that the tool is read-only, registered in the tool list Desktop reads, or returns the same rows as the CLI — assert tool annotations/read-only, and compare the tool's payload to `fm proof --json` outp…
- [ ] MEDIUM: The pane's one-line band budget is named as the failure mode but has no criterion — add a test that the unproven count plus top kind line fits the width cap at worst-case values (large counts, longest kind name, zero unproven, and proof data missing) and degrades by truncating or omitting t…
- [ ] MEDIUM: Step 1 says tests first, but MASTER.md, README, and CHANGELOG have no acceptance check and no step ownership beyond step 4 — add a simple check (CHANGELOG entry present, README/MASTER mention the surfaces) or drop them from the stated scope; also state the fallback when `fm proof --json` fa…
- [ ] LOW: Interpretation Reading 1 vs 2 is chosen at 85% confidence without noting that other in-flight proof-kind briefs may touch the same files (pane, site/pages.py) — check for open tasks touching mods/foreman-ui and site/pages.py and sequence or rebase before step 2.
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2344 [FEATURE M, done, 4 steps] #2 and #8 on every surface (Mission 5): fm code's planner writes readings, options with failure modes and a choice confidence and meets…
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Lessons
- A new view-model key must land in ui-demo.json in the same change: test_board_surfaces pins demo-vs-real key parity
## Plan gaps
- failed first: step 1 failing tests first, one per surface
## Files touched
- plugin/tests/test_agents.py
- plugin/tests/test_mcp.py
- plugin/tests/test_site.py
- plugin/tests/test_ui.py
- plugin/tests/test_code.py
- plugin/lib/fmmcp.py
- plugin/lib/fmagents.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmcode.py
- site/pages.py
- site/stats.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/ui-demo.json
