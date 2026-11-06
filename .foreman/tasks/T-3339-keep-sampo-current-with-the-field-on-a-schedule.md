---
id: T-3339
type: FEATURE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/outside.py, plugin/tests/test_outside.py, plugin/lib/sampo/cli.py, docs/map/ops-2.md]
depends_on: []
source: user
created: 2026-11-06T05:04:57Z
updated: 2026-11-06T07:02:07Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a8ac414757f610849
lane_branch: worktree-agent-a8ac414757f610849
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:57:02Z
plan0_scope: [plugin/lib/sampo/outside.py, plugin/tests/test_outside.py, plugin/lib/sampo/cli.py, docs/map/ops-2.md]
builder_returned: 2026-11-06T07:02:07Z
---
# Landscape scan: weekly, four fixed tracks (what users want or miss; models, APIs and MCP servers; Codex/Cursor/Gemini CLI/opencode/Aider features; agent research) with no planner call, and Decision/[read] lines never taken for items
## Raw request
> Keep Sampo current with the field, on a schedule: the landscape scan (outside.cmd_landscape, night job) asks one question every 30 days and only lists new items; nothing becomes a task and nothing watches releases. Make it weekly with two tracks: what users want or miss (today's question) and what just shipped (Claude Code releases and changelog, new models and APIs, MCP servers, Codex/Cursor/Gemini CLI/opencode/Aider features, agent research papers); file each new item Sampo doesn't cover (recall.covered) once as a FEATURE capture with sources, through the capture-once path (dedupe, open cap, precision muting); a Claude Code release Sampo hasn't adapted to files an 'adapt to CC x.y' task (T-1253's shape); local model for clustering and dedupe, Claude only for the research. User: 'periodically research tools and capabilities that people want and stuff that's coming out that's new and add features to sampo'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] no planner call in the stub log; LANDSCAPE_DAYS is 7 and --if-due skips within 7 days; Decision placeholders and [read] marks are not items; items carry (claim, url, track) — verify with `python3 plugin/tests/run.py test_outside`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [x] SUBS and fanout; items() fix; help and map text
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_outside` → exit 0 · Ran 16 tests in 547.9s (13 jobs, 16 at a time; slowest: Deps 4s, Landscape 2s, Release 2s) / OK (ran] (tree 686a14708377] (world 2f1906870a] (2026-11-06T06:08:37Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_outside test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2366 tests in 2050.4s (705 jobs, 16 at a time; slowest: AffectedPairs 332s, LeanKindGateSessionLine 79s, LeanKindGateHookDelay 77s) / FAILED (3 classes: test_cli.AffectedPairs, test_left_out.LeftO (ran] (tree 686a14708377] (world 2f1906870a] (2026-11-06T06:43:08Z)
## Log
- 2026-11-06T05:04:57Z created
- 2026-11-06T05:54:21Z planned from capture
- 2026-11-06T05:56:56Z focused
- 2026-11-06T05:57:02Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T07:01:03Z step 1: no red run was recorded before the code change (tests and code were written together); step 2 evidence is the first run of test_outside
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3362 [FEATURE M, planned, 2 steps] Landscape files what Sampo lacks: new verified items recall.covered misses are clustered locally (moonscale _reps/_bar) and filed on…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_cli.py, plugi…
