---
id: T-2172
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:21:30Z
updated: 2026-10-30T18:54:26Z
base: c8f64f80bd05329d249cc192359db10b136db3b5
base_tree: 5085187e5f6845e561d6e744f79767d3524e583f
plan0_at: 2026-10-30T18:43:56Z
plan0_scope: []
verified: strong
---
# fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and…
## Raw request
> fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and has no pane/status line; add both, per gen-0's every-surface MUST (found by T-2166's cold read of mission-exam.md)
## Interpretation
gen-0 MUST: a capability with state has a pane/status surface and works on every surface (Claude Code, fm code, other agents, Desktop). The exam scorecard (the DONE-WHEN pass: every §2 capability on its held-out exam) prints only from fm exam scorecard. Put a one-word count on the Genesis health line (fmgenesis.health, cached on tower file stats, so exam.jsonl changes refresh it): session start, fm state, fm watch's pane JSON and fm code all render it via c.genesis_line; and an MCP tool exam_scorecard so Desktop and other agents can read the full card.
## Assumptions (confidence)
## Acceptance criteria
- [x] the Genesis health line names the held-out scorecard count, and an MCP tool exam_scorecard returns fm exam scorecard — verify with `python3 plugin/tests/run.py test_genesis test_mcp`
## Non-goals
## Approach (options → choice → why)
Options: (a) health() adds g['exam'] = 'exam N/M held out' from scorecard() and genesis_line appends it; MCP tool exam_scorecard runs fm exam scorecard (chosen: one cached field reaches every status surface already wired to the Genesis line; one table row for MCP); (b) a separate exam pane widget (rejected: a new surface per client, the Genesis line already reaches all); (c) put the scorecard in fm state's text only (rejected: misses fm watch/pane and Desktop). The smoke count rides along so a Haiku-only exam never reads as a production score.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: genesis_line shows exam N/M; MCP tools/list has exam_scorecard and tools/call returns the card
2. [x] implement health exam field, genesis_line, MCP row; MASTER, README MCP row if listed, CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/README.md ~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisHealth test_mcp` → ✗ exit 1 · Ran 25 tests in 1.8s (10 classes, 16 at a time; slowest: McpNew 2s, McpTools 1s, GenesisHealth 1s) / FAILED (3 classes) [ran] [tree 30212f44d536] (2026-10-30T18:43:59Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_mcp test_hooks` → exit 0 · Ran 326 tests in 36.6s (50 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree 32bb3498ac1b] (2026-10-30T18:45:28Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisHealth` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: GenesisHealth 1s) / FAILED (1 classes) [ran] [tree abc2b90a1321] (2026-10-30T18:45:59Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_mcp test_hooks` → exit 0 · Ran 326 tests in 37.0s (50 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree 6f82a2ed525d] (2026-10-30T18:46:41Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_mcp test_hooks` → exit 0 · Ran 326 tests in 39.7s (50 classes, 16 at a time; slowest: Stop 39s, NoTaskGate 29s, PreToolUse 24s) / OK [ran] [tree be31ccd6d06a] (2026-10-30T18:49:33Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_mcp` → exit 0 · Ran 112 tests in 7.2s (22 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisLive 5s, GenesisSweep 5s) / OK [ran] [tree be31ccd6d06a] (2026-10-30T18:50:42Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_mcp test_hooks` → exit 0 · Ran 326 tests in 38.7s (50 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree be31ccd6d06a] (2026-10-30T18:50:42Z)
- (audit intent) `one foreman:fm-reviewer pass (research T-2172-review): 1 MEDIUM plausible (held-out counts on session surfaces: aggregate only, decided), 1 LOW fixed` → the done gate shows on every surface (session start, fm state, fm ui/pane, fm code via genesis_line) and Desktop reads it through fm mcp exam_scorecard; live line 'gen 1 · exam 0/13 pass, 4 Haiku skipped' [tree be31ccd6d06a] (2026-10-30T18:50:42Z)
- (audit edge) `one foreman:fm-reviewer pass (research T-2172-review): 1 MEDIUM plausible (held-out counts on session surfaces: aggregate only, decided), 1 LOW fixed` → no exam part before any graded or Haiku line; scorecard errors drop only that part; exit 1 from fm exam scorecard is an answer over MCP; a Foreman update refreshes the cached line [tree be31ccd6d06a] (2026-10-30T18:50:42Z)
- (audit adversary) `one foreman:fm-reviewer pass (research T-2172-review): 1 MEDIUM plausible (held-out counts on session surfaces: aggregate only, decided), 1 LOW fixed` → the line is built from integers, plain'd and defanged; MCP output is redacted and a sensitive project serves nothing; argv fixed, no arguments; counts only, never scenario ids, reach sessions (fm decide) [tree be31ccd6d06a] (2026-10-30T18:50:42Z)
- (audit self) `one foreman:fm-reviewer pass (research T-2172-review): 1 MEDIUM plausible (held-out counts on session surfaces: aggregate only, decided), 1 LOW fixed` → no findings [tree be31ccd6d06a] (2026-10-30T18:50:42Z)
## Log
- 2026-10-30T15:21:30Z created
- 2026-10-30T15:28:55Z also: README has no fm exam line (only Genesis's); add one beside Genesis
- 2026-10-30T15:33:57Z widened: fm mcp has no genesis tool either, so Desktop can't read the tower's status; one read-only MCP tool for exam scorecard + genesis status covers both
- 2026-10-30T18:33:09Z planned: it has criteria and steps
- 2026-10-30T18:33:09Z set tier=S
- 2026-10-30T18:43:56Z focused
- 2026-10-30T18:51:06Z done
- 2026-10-30T18:51:08Z committed e09f12f0 (8 files)
- 2026-10-30T18:51:36Z guard authorization added: publish
- 2026-10-30T18:54:26Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (sixth): the frame may grow, never shrink] [check: pending T-2188] Standing rule from gen 2 on: the Genesis fram…
## Why not caught
gen-0's every-surface MUST had no check for the exam scorecard; T-2166's cold read of mission-exam.md caught it
## Lessons
- Put a new piece of state on the one line every surface already renders instead of building a widget per client; and key a cache on the code that computes it, or an update hides until the data changes.
## Plan gaps
- failed first: step 1 red tests: genesis_line shows exam N/M; MCP tools/list has exam_scorecard and tools/call returns th…
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_mcp.py
- plugin/lib/fmgenesis.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmmcp.py
- plugin/lib/fmcore.py
