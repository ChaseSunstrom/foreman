---
id: T-3346
type: FEATURE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:11:39Z
updated: 2026-11-06T06:33:41Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aca35f4f80860e1f6
lane_branch: worktree-agent-aca35f4f80860e1f6
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:52:23Z
plan0_scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
builder_returned: 2026-11-06T06:33:41Z
---
# sampo doctor warns on MCP servers configured with the deprecated HTTP+SSE transport (MCP 2026-07-28 reclassified it Deprecated, eligible for removal)
## Raw request
> Verify MCP 2026-07-28 spec changes (stateless, no handshake, SSE deprecated, Tasks and Apps as extensions; reported by theregister.com and developersdigest.tech, not yet read from the spec) and, if confirmed, add a sampo doctor check that flags configured MCP servers on SSE or pre-2026-07-28 protocol versions
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a .claude.json fixture with one type=sse and one type=http server yields exactly one warning naming the sse server, citing https://modelcontextprotocol.io/specification/2026-07-28/changelog; project .mcp.json is read too; no network or process spawn — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fixture test, red
2. [ ] check_mcp_transport walking the mcpServers dicts _supply already walks (doctor.py:2146)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor McpTransport` → ✗ exit 1 · Ran 115 tests in 64.4s (45 jobs, 16 at a time; slowest: ViewsRepair 9s, LockProbe 4s, Command 4s) / FAILED (1 classes: test_doctor.McpTransport) (ran] (tree 988967955c04] (world 2f1906870a] (2026-11-06T05:53:54Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 115 tests in 630.3s (45 jobs, 16 at a time; slowest: ViewsRepair 48s, Timing 4s, LockProbe 4s) / OK (ran] (tree 31d4a23afdf2] (world 2f1906870a] (2026-11-06T06:04:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 217 tests in 384.0s (76 jobs, 16 at a time; slowest: ViewsRepair 7s, RenameScan.test_no_fm_only_command_regex 6s, Bench 5s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 31d4a23afdf2] (world 2f1906870a] (2026-11-06T06:19:15Z)
- (step 2) `python3 plugin/tests/run.py test_left_out` → ✗ exit 1 · Ran 3 tests in 4.3s (1 jobs, 16 at a time; slowest: LeftOut 0s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 31d4a23afdf2] (world 2f1906870a] (2026-11-06T06:21:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 221 tests in 303.0s (71 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 6s, ViewsRepair 5s, LockProbe 3s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 27ce7a873d3c] (world 2f1906870a] (2026-11-06T06:33:19Z)
## Log
- 2026-11-06T05:11:39Z created
- 2026-11-06T05:49:43Z planned from capture
- 2026-11-06T05:52:21Z focused
- 2026-11-06T05:52:23Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3359 [FEATURE M, planned, 2 steps] Sampo's own MCP server speaks the 2026-07-28 protocol: stateless (no initialize handshake required), server/discover, the protocol v…
- playbook Deprecation: announce, shim, remove (fm playbooks show clean/deprecation)
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py
