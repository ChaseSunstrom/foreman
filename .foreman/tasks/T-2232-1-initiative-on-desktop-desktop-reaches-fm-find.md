---
id: T-2232
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T23:40:25Z
updated: 2026-10-31T08:17:51Z
base: 40ae930636cf9897d4754c3c2a2f11ba1594ecd1
base_tree: 4c51627d4db66840b59c3ad443d8b371d49e4feb
plan0_at: 2026-10-31T08:12:04Z
plan0_scope: []
verified: strong
---
# #1 (initiative) on Desktop: Desktop reaches fm find only through the MCP server; add a…
## Raw request
> #1 (initiative) on Desktop: Desktop reaches fm find only through the MCP server; add a Desktop path (or record n/a with why) so the Initiative row's Desktop cell is grounded
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm mcp register desktop prints Claude Desktop's mcpServers stanza for Foreman's server (JSON: an absolute fm path and args mcp -p <project>), so Desktop reaches fm find and the rest; the README's MCP line names it — verify with `python3 plugin/tests/run.py test_mcp`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then the desktop branch in fmmcp.cmd_register, README line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T08:13:33Z steps 1/1 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, README.md, plugin/lib/fmmcp.py, plugin/tests/test_mcp.py
- touched since last checkpoint: plugin/tests/test_mcp.py, plugin/lib/fmmcp.py, CHANGELOG.md, README.md
## Docs impact
README.md, CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_mcp` → ✗ exit 1 · Ran 22 tests in 9.699s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 2e48a5bdf5f6] (2026-10-31T08:13:16Z)
- `cd plugin/tests && python3 -m unittest -q test_mcp` → exit 0 · Ran 22 tests in 8.792s / OK [ran] [tree 2e48a5bdf5f6] (2026-10-31T08:13:16Z)
- (step 1) `python3 plugin/tests/run.py test_mcp test_docs` → exit 0 · Ran 107 tests in 10.3s (32 classes, 16 at a time; slowest: Fences 10s, McpNew 3s, McpTools 3s) / OK [ran] [tree 2e48a5bdf5f6] (2026-10-31T08:13:27Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 24 tests in 1.9s (10 classes, 16 at a time; slowest: McpNew 2s, McpTools 1s, McpFind 1s) / OK [ran] [tree 2e48a5bdf5f6] (2026-10-31T08:17:34Z)
- (audit intent) `self-review of the diff: desktop branch runs only with no extra args, resolves the project slug through fmcli.resolve, names fm by absolute path (which() or the plugin's bin/fm) since Desktop starts servers without a shell PATH; the test parses the printed JSON and checks command and args` → Desktop users get a paste-ready mcpServers stanza that starts fm mcp for this project, so fm find reaches Desktop [tree 2e48a5bdf5f6] (2026-10-31T08:17:34Z)
- (audit edge) `self-review of the diff: desktop branch runs only with no extra args, resolves the project slug through fmcli.resolve, names fm by absolute path (which() or the plugin's bin/fm) since Desktop starts servers without a shell PATH; the test parses the printed JSON and checks command and args` → fm off PATH falls back to PLUGIN_ROOT/bin/fm; extra args after desktop fall through to the usage error; the stanza only prints, never edits Desktop's config [tree 2e48a5bdf5f6] (2026-10-31T08:17:34Z)
- (audit self) `self-review of the diff: desktop branch runs only with no extra args, resolves the project slug through fmcli.resolve, names fm by absolute path (which() or the plugin's bin/fm) since Desktop starts servers without a shell PATH; the test parses the printed JSON and checks command and args` → no findings [tree 2e48a5bdf5f6] (2026-10-31T08:17:34Z)
## Log
- 2026-10-30T23:40:25Z created
- 2026-10-31T08:12:02Z set tier=S
- 2026-10-31T08:12:02Z planned: it has criteria and steps
- 2026-10-31T08:12:03Z focused
- 2026-10-31T08:15:16Z scope: plugin/lib/fmmcp.py (cmd_register desktop), plugin/tests/test_mcp.py, README.md, CHANGELOG.md
- 2026-10-31T08:17:50Z done
- 2026-10-31T08:17:51Z committed 899b26cf (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- T-2223 [FEATURE M, done, 1 steps] Refresh coverage.md from the code: built cells read empty (find × MCP, find × fm code… — lesson: A cold reader with no code access can …
- similar past tasks were M: consider --tier M
## Lessons
- Desktop launches MCP servers with no shell PATH and no cwd, so any stanza must carry an absolute command and the project explicitly
## Files touched
- plugin/tests/test_mcp.py
- plugin/lib/fmmcp.py
- CHANGELOG.md
- README.md
