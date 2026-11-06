---
id: T-2201
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:25:20Z
updated: 2026-10-30T20:10:11Z
base: da2761e4dbd8dce22ecbe86b360cc501a71d24b7
base_tree: bdcf6ee57e11befec601038714a1638d10233c15
plan0_at: 2026-10-30T20:00:46Z
plan0_scope: []
verified: strong
---
# fm mcp genesis_status: Desktop and other agents read the tower's status (fm genesis…
## Raw request
> fm mcp genesis_status: Desktop and other agents read the tower's status (fm genesis status: generation, stage, next action, the exam count) through MCP; T-2172 added exam_scorecard only (gen-0 every-surface MUST, from mission-genesis's surfaces line)
## Interpretation
Desktop and other agents can read the exam scorecard through fm mcp (T-2172) but not the tower's status (generation, stage, next action, exam count): gen-0's every-surface MUST for #13.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm mcp lists genesis_status and calling it returns fm genesis status's text — verify with `python3 plugin/tests/run.py test_mcp`
## Non-goals
## Approach (options → choice → why)
One read-only tool row in fmmcp.TOOLS, genesis_status → fm genesis status, beside exam_scorecard; options: fold it into exam_scorecard (mixes two answers), a resource instead of a tool (Desktop clients surface tools better), a tool row (chosen). Build vs reuse: the existing _TEXT schema and _fm runner.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_mcp lists and calls genesis_status
2. [x] fmmcp row; MASTER, CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/README.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mcp` → ✗ exit 1 · Ran 22 tests in 1.9s (9 classes, 16 at a time; slowest: McpNew 2s, McpTools 1s, McpFind 1s) / FAILED (2 classes) [ran] [tree e5b575ff9b25] (2026-10-30T20:00:55Z)
- (step 2) `python3 plugin/tests/run.py test_mcp test_docs` → exit 0 · Ran 102 tests in 8.3s (30 classes, 16 at a time; slowest: Fences 8s, McpNew 2s, McpTools 1s) / OK [ran] [tree 31af1e803e79] (2026-10-30T20:01:32Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 22 tests in 1.9s (9 classes, 16 at a time; slowest: McpNew 2s, McpTools 1s, McpFind 1s) / OK [ran] [tree 31af1e803e79] (2026-10-30T20:01:54Z)
- (step 1) `python3 plugin/tests/run.py test_mcp test_docs` → exit 0 · Ran 102 tests in 8.2s (30 classes, 16 at a time; slowest: Fences 8s, McpNew 2s, McpTools 2s) / OK [ran] [tree 31af1e803e79] (2026-10-30T20:01:54Z)
- (audit self) `self: a read-only tool row beside exam_scorecard running fm genesis status with no arguments; no input reaches argv, output is the user's own tower status; ok` → no findings [tree 31af1e803e79] (2026-10-30T20:01:54Z)
## Log
- 2026-10-30T19:25:20Z created
- 2026-10-30T20:00:15Z set tier=S
- 2026-10-30T20:00:15Z planned: it has criteria and steps
- 2026-10-30T20:00:46Z focused
- 2026-10-30T20:02:20Z done
- 2026-10-30T20:02:22Z committed f854209e (5 files)
- 2026-10-30T20:07:19Z guard authorization added: publish
- 2026-10-30T20:10:11Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: The Genesis line and the exam_scorecard MCP tool show the held-out scorecard to sessions: aggregate N/M pass on the shared line, per-capability coun…
## Lessons
- A capability with state needs its status on every surface in the same task: T-2172 added the scorecard to MCP but not the tower status beside it
## Plan gaps
- failed first: step 1 red: test_mcp lists and calls genesis_status
## Files touched
- plugin/tests/test_mcp.py
- plugin/lib/fmmcp.py
- CHANGELOG.md
- MASTER.md
- README.md
