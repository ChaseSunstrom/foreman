---
id: T-2141
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2135]
source: user
created: 2026-10-30T10:37:52Z
updated: 2026-10-31T03:14:49Z
inferred_deps: [T-2137]
inferred_why: T-2137: surfaces show the verdict
base: 7cac336306118fd07d9dc624dcafdda9e3bceaed
base_tree: 5f5f381ac117b430baa0df77f13c924afa619644
plan0_at: 2026-10-31T02:42:25Z
plan0_scope: []
verified: strong
---
# Goal surfaces: fm code, MCP goal tool, AGENTS.md block, site page, pane line, docs (Mission 4 brief 7)
## Raw request
> Goal surfaces: fm code, MCP goal tool, AGENTS.md block, site page, pane line, docs (Mission 4 brief 7)
## Interpretation
Mission 4 brief 7: the standing goal shows wherever the user or another agent looks, all from fmmandate's two sources (goal_line, T-2139; the stored verdict, T-2137), never a second formatter: (1) fm code's run prompt carries the goal line; (2) the MCP server lists a goal tool (show and verdict, read-only); (3) fm export agents' AGENTS.md block gets a Goal section (the line and verdict, data-framed); (4) the view model's signals (the pane/band) name a stopped goal with its first cause; (5) the site's Goal to finish page (the capability page for gen-0 §2 #4) describes fm goal set/item/link/show/verdict and the across-days line. Docs: MASTER, README where commands are listed, CHANGELOG.
## Assumptions (confidence)
## Acceptance criteria
- [x] the goal line and verdict show in fm code, the MCP tool list, the AGENTS.md block, the pane signals and the site's Goal to finish page — verify with `python3 plugin/tests/run.py test_mcp test_ui_signals test_site`
## Non-goals
## Approach (options → choice → why)
Options: (1) each surface calls goal_line and reads goal_verdict from meta (chosen: one source each, cheap, consistent; tests per surface); (2) a new goal surface module (an abstraction with one implementation); (3) only CLI plus docs (fails the 'every surface it belongs on' MUST). Choice 1. The pane signal reads only meta, never runs checks.
## Risks and rollback
## Execution prompt
## Steps
1. [x] MCP goal tool + fm code prompt line + AGENTS.md block, test-first
2. [x] pane signal + site page + MASTER/README/CHANGELOG
## Resume here
## Docs impact
MASTER.md, README.md, CHANGELOG.md, site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mcp test_ui_signals test_site test_export test_code_envelope 2>&1 | tail -25` → exit 0 · Ran 80 tests in 6.8s (35 classes, 16 at a time; slowest: Envelope 6s, Header 5s, Export 3s) / OK [ran] [tree d5ffb82ec061] (2026-10-31T02:44:30Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mcp test_ui_signals test_site test_site_build test_cli test_code test_export test_code_envelope 2>&1 | tail -15` → exit 0 · Ran 677 tests in 66.7s (172 classes, 16 at a time; slowest: Worker 66s, Fakes 42s, TaskLifecycle 25s) / OK [ran] [tree 06dd310f5ed4] (2026-10-31T02:45:47Z)
- `python3 plugin/tests/run.py test_mcp test_ui_signals test_site test_export` → ✗ exit 1 · Ran 76 tests in 6.8s (34 classes, 16 at a time; slowest: Header 5s, Export 3s, McpNew 2s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree fe8d0466506c] (2026-10-31T03:11:20Z)
- `python3 plugin/tests/run.py test_mcp test_ui_signals test_site test_export` → exit 0 · Ran 76 tests in 5.9s (34 classes, 16 at a time; slowest: Header 5s, Export 4s, McpNew 2s) / OK [ran] [tree fe8d0466506c] (2026-10-31T03:11:20Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_mcp test_ui_signals test_site test_export test_code_envelope test_hooks` → exit 0 · Ran 324 tests in 38.9s (67 classes, 16 at a time; slowest: Stop 39s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree fe8d0466506c] (2026-10-31T03:12:11Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mcp test_ui_signals test_site test_export test_code_envelope test_hooks` → exit 0 · Ran 324 tests in 46.6s (67 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 33s, PreToolUse 28s) / OK [ran] [tree fe8d0466506c] (2026-10-31T03:12:58Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp test_ui_signals test_site` → exit 0 · Ran 60 tests in 6.9s (29 classes, 16 at a time; slowest: Header 6s, McpNew 5s, McpTools 4s) / OK [ran] [tree fe8d0466506c] (2026-10-31T03:13:06Z)
- (audit intent) `fm-reviewer intent+adversary+edge+operator+maintainer+design: approve with nits, fixed in 969a4467: one fresh_verdict (goal stands, same set_at and root, at most a day old) feeds the pane signal, AGENTS.md (dated, else left out), the MCP tool and the Stop gate; progress counts archived briefs so tidy can't change the count; fm code frames the goal as data and defangs it; the MCP test can now fail; stale/other-root/expired cases tested; merge with T-2136 resolved; 324 tests green; red-to-green proven` → the goal shows in fm code's prompt, a read-only MCP goal tool, AGENTS.md, the band and the site's Planning page [tree fe8d0466506c] (2026-10-31T03:13:06Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+operator+maintainer+design: approve with nits, fixed in 969a4467: one fresh_verdict (goal stands, same set_at and root, at most a day old) feeds the pane signal, AGENTS.md (dated, else left out), the MCP tool and the Stop gate; progress counts archived briefs so tidy can't change the count; fm code frames the goal as data and defangs it; the MCP test can now fail; stale/other-root/expired cases tested; merge with T-2136 resolved; 324 tests green; red-to-green proven` → every surface reads meta and briefs only, no check runs; the goal text is quoted data and defanged where it leaves the machine (AGENTS.md); hidden in a sensitive project [tree fe8d0466506c] (2026-10-31T03:13:06Z)
- (audit edge) `fm-reviewer intent+adversary+edge+operator+maintainer+design: approve with nits, fixed in 969a4467: one fresh_verdict (goal stands, same set_at and root, at most a day old) feeds the pane signal, AGENTS.md (dated, else left out), the MCP tool and the Stop gate; progress counts archived briefs so tidy can't change the count; fm code frames the goal as data and defangs it; the MCP test can now fail; stale/other-root/expired cases tested; merge with T-2136 resolved; 324 tests green; red-to-green proven` → a stale, other-root, replaced or expired verdict shows nowhere; archived briefs count [tree fe8d0466506c] (2026-10-31T03:13:06Z)
- (audit operator) `fm-reviewer intent+adversary+edge+operator+maintainer+design: approve with nits, fixed in 969a4467: one fresh_verdict (goal stands, same set_at and root, at most a day old) feeds the pane signal, AGENTS.md (dated, else left out), the MCP tool and the Stop gate; progress counts archived briefs so tidy can't change the count; fm code frames the goal as data and defangs it; the MCP test can now fail; stale/other-root/expired cases tested; merge with T-2136 resolved; 324 tests green; red-to-green proven` → no checks or git in any surface; fm code adds one project lookup per prompt [tree fe8d0466506c] (2026-10-31T03:13:06Z)
- (audit design) `fm-reviewer intent+adversary+edge+operator+maintainer+design: approve with nits, fixed in 969a4467: one fresh_verdict (goal stands, same set_at and root, at most a day old) feeds the pane signal, AGENTS.md (dated, else left out), the MCP tool and the Stop gate; progress counts archived briefs so tidy can't change the count; fm code frames the goal as data and defangs it; the MCP test can now fail; stale/other-root/expired cases tested; merge with T-2136 resolved; 324 tests green; red-to-green proven` → a plain text block on the Planning page, no outside host [tree fe8d0466506c] (2026-10-31T03:13:06Z)
## Log
- 2026-10-30T10:37:52Z created
- 2026-10-31T02:42:04Z set approved=True
- 2026-10-31T02:42:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2141.builder.md
- 2026-10-31T02:42:25Z focused
- 2026-10-31T03:11:06Z merged worktree-agent-a04b4673c650e5458 (15 file(s))
- 2026-10-31T03:11:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a04b4673c650e5458
- 2026-10-31T03:11:06Z focused
- 2026-10-31T03:12:58Z scope: plugin/lib/fmcode.py, plugin/lib/fmmcp.py, plugin/lib/fmcost.py, plugin/lib/fmwatch.py, plugin/lib/fmmandate.py (fresh_verdict, progress), plugin/lib/fmhooks.py (_goal_gate uses fresh_verdict), site/pages.py, README.md, MASTER.md, CHANGELOG.md, tests
- 2026-10-31T03:14:49Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2136 [FEATURE M, planned, 3 steps] fm goal plan: a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn (Mission 4 b…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
## Lessons
- Every surface that shows a cached verdict needs the same freshness rule; one helper keeps the band, the export and the Stop gate from disagreeing
## Files touched
- plugin/tests/test_mcp.py
- plugin/tests/test_ui_signals.py
- plugin/tests/test_export.py
- plugin/tests/test_code_envelope.py
- plugin/tests/test_site.py
- plugin/lib/fmcode.py
- plugin/lib/fmmcp.py
- plugin/lib/fmcost.py
- plugin/lib/fmwatch.py
- site/pages.py
- README.md
- MASTER.md
- plugin/lib/fmmandate.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmfind.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmprove.py
- plugin/skills/genesis/SKILL.md
- plugin/tests/test_find.py
- plugin/tests/test_genesis.py
- plugin/tests/test_goal.py
