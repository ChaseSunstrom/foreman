---
id: T-3359
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/mcp.py, plugin/tests/test_mcp.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:49:45Z
updated: 2026-11-06T06:47:35Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a2d0cd7763dbd327d
lane_branch: worktree-agent-a2d0cd7763dbd327d
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:53:29Z
plan0_scope: [plugin/lib/sampo/mcp.py, plugin/tests/test_mcp.py, CHANGELOG.md]
builder_returned: 2026-11-06T06:47:35Z
group: MCP 2026-07-28 protocol support
---
# Sampo's own MCP server speaks the 2026-07-28 protocol: stateless (no initialize handshake required), server/discover, the protocol version per request in _meta, ping removed for new clients, with the 2025-06-18 initialize path kept for older clients
## Raw request
> Sampo's own MCP server speaks the 2026-07-28 protocol: stateless (no initialize handshake required), server/discover, the protocol version per request in _meta, ping removed for new clients, with the 2025-06-18 initialize path kept for older clients
## Interpretation
Reading 1: a new-protocol request is one carrying io.modelcontextprotocol/protocolVersion in params._meta; serve it with no handshake. Reading 2 (ruled out): a separate server process or port per generation, needless since the JSON-RPC shapes coexist.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a 2026-07-28 client gets server/discover and tool calls with no initialize; a 2025-06-18 client's initialize/ping still work; unknown versions get the spec's error — verify with `python3 plugin/tests/run.py test_mcp`
## Non-goals
## Approach (options → choice → why)
1) Dispatch inside _answer on _meta version; likely outcome: ~15 lines, fails if a client sends the version elsewhere. 2) Separate legacy/new handler modules; fails if the two drift apart. 3) Per-connection mode state set by first message; fails on a client that mixes generations. 4) use what exists: the current _answer already dispatches by method; likely outcome: extend it, fails if it grows tangled. 5) do less: add only server/discover and leave versions unchecked; likely outcome: violates the spec error rule. Choice 4 (80%): stateless by nature, smallest diff.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] tests for both protocol generations, red  <- CURRENT
2. [x] dual-version dispatch in mcp.py (VERSION at :21, initialize/ping at :282-286)
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 30 tests in 155.1s (16 jobs, 16 at a time; slowest: McpTools 10s, Edges 3s, McpReview 2s) / OK (ran] (tree 7302695b2a1f] (world 2f1906870a] (2026-11-06T05:56:34Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_mcp test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 246 tests in 616.0s (80 jobs, 16 at a time; slowest: RenameScan 41s, LockProbe 18s, Bench 16s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 7302695b2a1f] (world 2f1906870a] (2026-11-06T06:07:13Z)
- (step 2) `python3 plugin/tests/run.py test_left_out` → ✗ exit 1 · Ran 3 tests in 102.0s (1 jobs, 16 at a time; slowest: LeftOut 0s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 7302695b2a1f] (world 2f1906870a] (2026-11-06T06:09:27Z)
- (step 2) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 30 tests in 149.9s (16 jobs, 16 at a time; slowest: McpTools 3s, McpNew 2s, Review 1s) / OK (ran] (tree c3d4e1668978] (world 2f1906870a] (2026-11-06T06:24:15Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_mcp test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 247 tests in 652.6s (88 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 5s, ViewsRepair 5s, LockProbe 3s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree bb9d530cc1a3] (world 2f1906870a] (2026-11-06T06:37:15Z)
- (step 2) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 31 tests in 601.1s (16 jobs, 16 at a time; slowest: McpTools 4s, Review 1s, McpFind 1s) / OK (ran] (tree bb9d530cc1a3] (world 2f1906870a] (2026-11-06T06:47:23Z)
## Log
- 2026-11-06T05:49:45Z created
- 2026-11-06T05:53:26Z focused
- 2026-11-06T05:53:29Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0245 [FEATURE M, done, 2 steps] Foreman MCP server — fm mcp serves read-only tools over stdio (state, next, recall, resear — lesson: An argument handed to a CLI subpro…
- T-3346 [FEATURE S, active, 2 steps] sampo doctor warns on MCP servers configured with the deprecated HTTP+SSE transport (MCP 2026-07-28 reclassified it Deprecated, eligi…
- T-2904 [CLEAN M, dropped, 1 steps] Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- the similar finished task took 2 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_mcp.py
