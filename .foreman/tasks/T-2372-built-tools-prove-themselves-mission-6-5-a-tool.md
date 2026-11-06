---
id: T-2372
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnew.py, plugin/lib/fmmcp.py, plugin/lib/fmcli.py, plugin/lib/fmtoolproof.py, plugin/lib/fmwhich.py, plugin/tests/test_tool_proof.py, plugin/tests/test_scaffold.py, MASTER.md, CHANGELOG.md]
depends_on: [T-2369]
source: self
created: 2026-10-31T14:02:00Z
updated: 2026-10-31T16:49:26Z
builder_model: sonnet
base: 002eb587fd495cb1c9ecb7f69d7460609c1056a3
base_tree: c3107e96427e4f1e37cbf4527cad6e24f79ba3ec
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:12:38Z
plan0_scope: [plugin/lib/fmnew.py, plugin/lib/fmmcp.py, plugin/lib/fmcli.py, plugin/tests/test_tool_proof.py, plugin/tests/test_scaffold.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-10-31T16:45:18Z
verified: strong
---
# Built tools prove themselves (Mission 6, #5): a tool made by fm new tool or fm mcp new during a task closes only after a search receipt, a red-then-green test, a test that fails on a stubbed tool, and a real use
## Raw request
> Built tools prove themselves (Mission 6, #5): a tool made by fm new tool or fm mcp new during a task closes only after a search receipt, a red-then-green test, a test that fails on a stubbed tool, and a real use
## Interpretation
Reading 1: fm task finish refuses to close a task that built a tool until four checks pass: a search receipt, a red then green run by fm, a test that fails on a stubbed tool, and a real use in the session transcript (gap map #5 build-test-use loop). Reading 2: trust T-2278's scaffold, whose test fails until the tool works. Rejected: nothing checks the test was ever red, would catch a broken tool, or that the tool was then used, and Mission 4's lesson says every done signal needs a check that can fail.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task that ran fm new tool or fm mcp new closes only when a tool_search receipt for its need precedes the build, the tool's test went red and then green, the test fails against a stubbed copy of the tool, and the tool ran on the task's work after going green; no typed reason replaces any of the four; each missing piece is named in the refusal; tool_proved is logged; a task that built nothing gets no new check — verify with `python3 plugin/tests/run.py test_scaffold test_tool_proof`
## Non-goals
## Approach (options → choice → why)
1) fm new tool and fm mcp new log tool_built {path, test, task, need}; fm task finish checks for each tool: a tool_search receipt for its need before the build (fm which; local, so always required); the test's evidence shows a red run then a green run, run by fm; with the body replaced by a stub in a scratch copy the test fails; and the use: Claude Code's own session transcript shows a Bash call invoking the tool after the green run, other than through its own test. On a host with no transcript the use is labelled unproven and the tool is not marked proved. Then it logs tool_proved {path, need}. One refusal names what is missing. Fails if: a stub run hangs, which a timeout in the scratch copy bounds. 2) A quarantine shelf that tools leave once proved. Breaks: a second home for every tool and a move nobody remembers. 3) Use what exists: T-2278's failing-test scaffold alone. Likely outcome: a test the session edits until it passes proves nothing. 4) Do less: only the search receipt and the red-then-green check, no stub or use. Fails if: a tool that is never used or whose test cannot fail still ships. Choice 1 (80%): four conditions, each refused on its own in a test.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, README.md, plugin/tests/test_guard.py; past FIXes T-0875, T-0880, T-0908, T-0926, T-0928.
## Execution prompt
## Steps
1. [x] red tests first (test_tool_proof): each of the four conditions refused on its own, all four together pass, tool_proved logged
2. [x] tool_built events in fmnew and fmmcp; the stub-mutation run in a scratch copy
3. [x] fm task finish's built-tool check
4. [x] docs: MASTER.md, CHANGELOG.md
## Resume here
<!-- auto -->
- 2026-10-31T16:17:18Z step 1/4: red tests first (test_tool_proof): each of the four conditions refused on its own, all four together pass, tool_proved logged
- git: worktree-agent-a294e5de65074892e; 6 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmmcp.py, plugin/lib/fmnew.py, plugin/lib/fmwhich.py, plugin/lib/fmtoolproof.py, plugin/tests/test_tool_proof.py
- touched since last checkpoint: plugin/lib/fmtoolproof.py, plugin/lib/fmnew.py, plugin/lib/fmmcp.py, plugin/lib/fmwhich.py, plugin/lib/fmcli.py, plugin/tests/test_tool_proof.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tool_proof` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 2.1s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 9e6c96ec5e01] (2026-10-31T16:15:27Z)
- (ac 1) `python3 plugin/tests/run.py test_scaffold test_tool_proof 2>&1 | tail -25` → ✗ exit 1 · Ran 28 tests in 27.3s (5 classes, 16 at a time; slowest: ToolProof 27s, BuildWhatIsMissing 2s, Born 0s) / FAILED (1 classes: test_tool_proof.ToolProof) [ran] [tree 84875a3a18d0] (2026-10-31T16:18:41Z)
- (ac 1) `python3 plugin/tests/run.py test_scaffold test_tool_proof 2>&1 | tail -15` → exit 0 · Ran 28 tests in 27.8s (5 classes, 16 at a time; slowest: ToolProof 27s, BuildWhatIsMissing 4s, Born 1s) / OK [ran] [tree 826bc2ec0a76] (2026-10-31T16:19:15Z)
- (step 1) `python3 plugin/tests/run.py test_tool_proof` → exit 0 · Ran 15 tests in 12.8s (1 classes, 16 at a time; slowest: ToolProof 13s) / OK [ran] [tree 826bc2ec0a76] (2026-10-31T16:19:30Z)
- (step 2) `python3 plugin/tests/run.py test_scaffold test_tool_proof` → exit 0 · Ran 28 tests in 21.2s (5 classes, 16 at a time; slowest: ToolProof 21s, BuildWhatIsMissing 2s, Born 0s) / OK [ran] [tree 826bc2ec0a76] (2026-10-31T16:19:52Z)
- (step 3) `python3 plugin/tests/run.py test_scaffold test_tool_proof` → exit 0 · Ran 28 tests in 14.5s (5 classes, 16 at a time; slowest: ToolProof 14s, BuildWhatIsMissing 4s, Born 1s) / OK [ran] [tree c7865467903d] (2026-10-31T16:20:16Z)
- (step 4) `grep -c fmtoolproof MASTER.md` → exit 0 · 1 [ran] [tree c7865467903d] (2026-10-31T16:20:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_guard_cases test_mcp test_paused test_robustness test_scaffold test_tool_proof test_ui_signals test_verify_strength test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.99s] [ran] [tree c7865467903d] (2026-10-31T16:20:59Z)
- (step 3) `python3 plugin/tests/run.py test_scaffold test_tool_proof test_which` → exit 0 · Ran 69 tests in 71.5s (10 classes, 16 at a time; slowest: ToolProof 71s, Shelves 6s, Which 6s) / OK [ran] [tree c6dd0ae19f83] (2026-10-31T16:32:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_guard_cases test_mcp test_paused test_proof test_robustness test_scaffold test_tool_proof test_ui_signals test_verify_strength test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [51.31s] [ran] [tree c6dd0ae19f83] (2026-10-31T16:35:16Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_guard_cases test_mcp test_paused test_proof test_robustness test_scaffold test_tool_proof test_ui_signals test_verify_strength test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [26.61s] [ran] [tree c6dd0ae19f83] (2026-10-31T16:37:10Z)
- (step 1) `python3 plugin/tests/run.py test_scaffold test_tool_proof test_which test_goal test_lanes` → exit 0 · Ran 193 tests in 32.9s (25 classes, 16 at a time; slowest: ToolProof 33s, LaneRecovery 21s, Lanes 16s) / OK [ran] [tree 7fe4a4668bca] (2026-10-31T16:45:57Z)
- (ac 1) `python3 plugin/tests/run.py test_scaffold test_tool_proof` → exit 0 · Ran 39 tests in 33.1s (6 classes, 16 at a time; slowest: ToolProof 33s, BuildWhatIsMissing 3s, Born 1s) / OK [ran] [tree fe97bd96f6aa] (2026-10-31T16:46:46Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 2 MEDIUM, 1 LOW fixed test-first in 4814b463 before merge` → four proofs each named in the refusal; a task that built nothing gets no check [tree fe97bd96f6aa] (2026-10-31T16:46:46Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 2 MEDIUM, 1 LOW fixed test-first in 4814b463 before merge` → no fail-open on an unreadable tool; use proven only by an fm-run line running the tool, never a transcript or typed text [tree fe97bd96f6aa] (2026-10-31T16:46:46Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 2 MEDIUM, 1 LOW fixed test-first in 4814b463 before merge` → env passed through minus credentials, so tools needing HOME or LANG pass; an env cause is named [tree fe97bd96f6aa] (2026-10-31T16:46:46Z)
- (audit maintainer) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 2 MEDIUM, 1 LOW fixed test-first in 4814b463 before merge` → runs() and runs_test() are pure functions with their own tests [tree fe97bd96f6aa] (2026-10-31T16:46:46Z)
## Log
- 2026-10-31T14:02:00Z created
- 2026-10-31T16:07:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2372.builder.md
- 2026-10-31T16:08:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2372.builder.md
- 2026-10-31T16:08:45Z builder slot freed
- 2026-10-31T16:11:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2372.builder.md
- 2026-10-31T16:11:14Z builder slot freed
- 2026-10-31T16:12:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2372.builder.md
- 2026-10-31T16:12:37Z focused
- 2026-10-31T16:12:38Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T16:16:40Z set scope=['plugin/lib/fmnew.py', 'plugin/lib/fmmcp.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmtoolproof.py', 'plugin/lib/fmwhich.py', 'plugin/tests/test_tool_proof.py', 'plugin/tests/test_scaffold.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-31T16:16:40Z scope: new module fmtoolproof.py holds the proof; fmwhich logs the receipt's task
- 2026-10-31T16:45:18Z merged worktree-agent-a294e5de65074892e (7 file(s))
- 2026-10-31T16:45:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a294e5de65074892e
- 2026-10-31T16:45:22Z focused
- 2026-10-31T16:46:12Z scope: files outside the globs came from merging foreman/build, the fmmcp cmd_new 3-line hook and the changelog line
- 2026-10-31T16:47:43Z done
- 2026-10-31T16:49:26Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-1906 [FIX S, done, 3 steps] Fm task finish checks a FIX's red-to-green proof before running its checks — lesson: A refusal known before the checks run must be said bef…
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mcp.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmmcp.py, plugin/lib/fmnew.py, plugin/lib/fmtoolproof.py, plugin/lib/fmwhich.py, plugin/tests/test_tool_proof.py; re-ground the plan against them before editing
## Lessons
- A proof gate that catches every exception and returns no gaps is a bypass: fail closed per item and fail open only where the input is the ledger itself
## Plan gaps
- failed first: step 1 red tests first (test_tool_proof): each of the four conditions refused on its own, all four togethe…
## Files touched
- plugin/tests/test_tool_proof.py
- plugin/lib/fmtoolproof.py
- plugin/lib/fmnew.py
- plugin/lib/fmmcp.py
- plugin/lib/fmwhich.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
