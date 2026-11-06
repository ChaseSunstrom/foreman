---
id: T-3347
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/session.py, plugin/lib/sampo/agents.py, plugin/lib/sampo/cli.py, plugin/tests/test_session.py, plugin/tests/test_agents.py, MASTER.md, docs/map, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:11:41Z
updated: 2026-11-06T06:49:24Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aaa348eb82bf29491
lane_branch: worktree-agent-aaa348eb82bf29491
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:54:41Z
plan0_scope: [plugin/lib/sampo/session.py, plugin/lib/sampo/agents.py, plugin/tests/test_session.py, plugin/tests/test_agents.py, MASTER.md, docs/map, CHANGELOG.md]
builder_returned: 2026-11-06T06:49:24Z
---
# Agent adapters follow the field: Gemini CLI marked for Code Assist/API keys only (individual users moved to Antigravity CLI on 2026-06-18), Antigravity CLI (agy -p --output-format stream-json) and Cursor CLI (cursor-agent -p --output-format stream-json --force) added to session.AGENTS with fixture-tested normalisers
## Raw request
> Verify the Gemini CLI adapter still targets a live tool: a search result says Gemini CLI was replaced for individual users by the closed-source Antigravity CLI on 2026-06-18 (unverified). If true, adapt fmagents' Gemini adapter or mark it legacy; also evaluate the Cursor Agent SDK (2026-10-20) as a fourth adapter
## Interpretation
Reading 1: add agy and cursor as session agents with unverified-fixture normalisers, Gemini kept but marked legacy. Reading 2: replace Gemini outright; ruled out, Gemini CLI stays maintained for Enterprise/API keys.
## Assumptions (confidence)
## Acceptance criteria
- [ ] argv('agy', …) and argv('cursor', …) build the documented headless commands; recorded stream-json fixture lines for each normalise to Sampo's events (Cursor: system/init, assistant, tool_call started/completed, result); the Gemini adapter's docs say legacy — verify with `python3 plugin/tests/run.py test_session test_agents`
## Non-goals
## Approach (options → choice → why)
1) Per-agent branches mirroring existing ones, reuse _detail/_text; likely outcome: small diff, works. 2) A table-driven generic normaliser; fails if shapes diverge (they do), over-engineered for two. 3) do less: only docs, no adapters; fails the criteria. Choice 1 (80%): smallest diff matching the existing pattern.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] fixture tests, red
2. [ ] agy and cursor branches plus normalisers  <- CURRENT
3. [x] Gemini legacy note in docs and doctor
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_session` → exit 0 · Ran 46 tests in 501.0s (28 jobs, 16 at a time; slowest: Session 13s, Say 4s, SessionTrailer 4s) / OK (ran] (tree 87cd10d9be77] (world 2f1906870a] (2026-11-06T06:03:48Z)
- (step 3) `python3 plugin/tests/run.py test_agents` → exit 0 · Ran 28 tests in 70.5s (11 jobs, 16 at a time; slowest: Hook 17s, Export 3s, Install 1s) / OK (ran] (tree 87cd10d9be77] (world 2f1906870a] (2026-11-06T06:09:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 1230.03s) · timed out after 1230.03s (ran] (tree 6d5cf320dee2] (world 2f1906870a] (2026-11-06T06:41:40Z)
- (step 3) `python3 plugin/tests/run.py test_session test_help` → exit 0 · Ran 56 tests in 90.2s (32 jobs, 16 at a time; slowest: Session 4s, Say 2s, SessionTrailer 2s) / OK (ran] (tree 6d5cf320dee2] (world 2f1906870a] (2026-11-06T06:49:15Z)
## Log
- 2026-11-06T05:11:41Z created
- 2026-11-06T05:49:47Z planned from capture
- 2026-11-06T05:54:38Z focused
- 2026-11-06T05:54:41Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:21:07Z set scope=['plugin/lib/sampo/session.py', 'plugin/lib/sampo/agents.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_session.py', 'plugin/tests/test_agents.py', 'MASTER.md', 'docs/map', 'CHANGELOG.md']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2904 [CLEAN M, dropped, 1 steps] Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
- research T-0318-agents: Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP …
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, pl…
