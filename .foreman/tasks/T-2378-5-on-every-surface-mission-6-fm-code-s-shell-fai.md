---
id: T-2378
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmagents.py, plugin/lib/fmmcp.py, plugin/lib/fmhooks.py, site/pages.py, mods/foreman-ui, plugin/tests/test_code.py, plugin/tests/test_agents.py, plugin/tests/test_mcp.py, plugin/tests/test_site.py, MASTER.md, README.md, CHANGELOG.md]
depends_on: [T-2374]
source: self
created: 2026-10-31T14:02:04Z
updated: 2026-10-31T20:29:23Z
builder_model: sonnet
base: 313f2fa550406a83b225e6d6b334de4d858060e7
base_tree: 963ed05ee1c0647a8fcf4cc51cc43b8974e0b1f4
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-10-31T20:11:54Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmagents.py, plugin/lib/fmmcp.py, plugin/lib/fmhooks.py, site/pages.py, mods/foreman-ui, plugin/tests/test_code.py, plugin/tests/test_agents.py, plugin/tests/test_mcp.py, plugin/tests/test_site.py, MASTER.md, README.md, CHANGELOG.md]
verified: strong
---
# #5 on every surface (Mission 6): fm code's shell failures get the miss note and the same finish checks, other agents get it through fmagents, MCP gets read-only which and grants tools, the site gets a #5 page, the band shows queued grants, docs
## Raw request
> #5 on every surface (Mission 6): fm code's shell failures get the miss note and the same finish checks, other agents get it through fmagents, MCP gets read-only which and grants tools, the site gets a #5 page, the band shows queued grants, docs
## Interpretation
Reading 1: #5 reaches every surface gen-0's completeness MUST names: fm code's shell failures, other agents through fmagents, MCP read-only which and grants tools, the site, the band and docs. Reading 2: CLI plus docs. Rejected: #5 lives on the CLI and Claude Code's PostToolUseFailure hook only, and the MUST counts a capability done only on every surface it belongs on.
## Assumptions (confidence)
## Acceptance criteria
- [x] an fm code shell failure 'command not found: X' gets the same note and the same finish check; fmagents routes the miss for each host that has a post-tool failure event and the AGENTS.md block carries the line otherwise; MCP tools/list has read-only which and grants; the site page renders from state; the band shows queued grants; MASTER.md, README.md and CHANGELOG.md name each — verify with `python3 plugin/tests/run.py test_code test_agents test_mcp test_site`
## Non-goals
## Approach (options → choice → why)
1) Reuse, not rebuild: fm code's shell-tool failure path calls the same capability-miss function (moved where both can import it) and its close runs the same finish checks; fmagents routes each host's post-tool failure event where the host has one, else the AGENTS.md block carries one line; MCP gains read-only which and grants tools, which Desktop reaches through MCP; site/pages.py gets a #5 page as T-2127 did for #1; the band shows 'N installs wait on you' while the queue isn't empty; MASTER.md, README.md, CHANGELOG.md. Fails if: the moved function changes the hook's behaviour, which its existing test pins. 2) A separate fm code implementation. Breaks: two copies drift. 3) Do less: CLI only plus docs. Fails if: the MUST isn't met. 4) Use what exists: T-2127's page and band patterns for #1, with #5 data. Likely outcome: low risk, but it covers only the site and band. Choice 1 (80%): one shared function behind every surface.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/tests/test_hooks.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py; past FIXes T-0877, T-0907, T-0908, T-0928, T-0980.
## Execution prompt
## Steps
1. [x] red tests first in test_code, test_agents, test_mcp and test_site for each surface
2. [x] shared capability-miss function; fm code, fmagents and MCP wiring
3. [x] site page and band line
4. [x] docs: MASTER.md, README.md, CHANGELOG.md
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code -k MissNote` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: MissNote 1s) / OK [ran] [tree 60abd631288f] (2026-10-31T20:21:08Z)
- (step 2) `python3 plugin/tests/run.py test_code test_agents test_mcp` → exit 0 · Ran 499 tests in 73.4s (114 classes, 16 at a time; slowest: Worker 73s, Fakes 43s, Bench 19s) / OK [ran] [tree 60abd631288f] (2026-10-31T20:22:22Z)
- (step 3) `python3 plugin/tests/run.py test_ui_signals test_site test_docs test_watch 2>&1 | grep -E "^(FAIL|ERROR):|^Ran .*s\)|^OK|^FAILED|AssertionError" | head -6` → exit 0 · Ran 148 tests in 10.3s (49 classes, 16 at a time; slowest: Fences 10s, Header 6s, DocsProof 6s) / OK [ran] [tree 84fd4eb1ea0e] (2026-10-31T20:23:12Z)
- (step 3) `python3 plugin/tests/run.py test_ui_signals test_site` → exit 0 · Ran 43 tests in 4.8s (23 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree 5cae66d52164] (2026-10-31T20:25:08Z)
- (step 4) `python3 plugin/tests/run.py test_site test_docs` → exit 0 · Ran 136 tests in 8.5s (41 classes, 16 at a time; slowest: Fences 8s, Header 5s, DocsProof 3s) / OK [ran] [tree 5cae66d52164] (2026-10-31T20:25:18Z)
- (ac 1) `python3 plugin/tests/run.py test_code test_agents test_mcp test_site` → exit 0 · Ran 532 tests in 67.5s (131 classes, 16 at a time; slowest: Worker 67s, Fakes 42s, Bench 19s) / OK [ran] [tree 5cae66d52164] (2026-10-31T20:26:26Z)
- `python3 plugin/tests/run.py test_code -k MissNote` → ✗ exit 1 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: MissNote 1s) / FAILED (1 classes: test_code.MissNote) (start tree + this task's tests) [ran] [tree 5cae66d52164] (2026-10-31T20:26:30Z)
- `python3 plugin/tests/run.py test_code -k MissNote` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: MissNote 1s) / OK [ran] [tree 5cae66d52164] (2026-10-31T20:26:30Z)
- (ac 1) `python3 plugin/tests/run.py test_code test_agents test_mcp test_site` → exit 0 · Ran 532 tests in 67.7s (131 classes, 16 at a time; slowest: Worker 67s, Fakes 42s, Bench 19s) / OK [ran] [tree 5cae66d52164] (2026-10-31T20:27:54Z)
- (audit intent) `main-thread review (pace gate holds): each surface reuses one path (Claude Code's own PostToolUseFailure hook for fm code and for other agents' after-tool events; fmwhich.search and fmgrants for MCP; fmgrants.line for the band), no copy; the MCP which tool searches in-process so another client can't leave a search receipt that T-2372 would count; grants omits the command. A DST bug found on the way (fm code's limit reset) fixed test-first` → fm code's missing tool gets the note and the record on the task (finish refuses past it); Codex, Gemini CLI and opencode route it; AGENTS.md names fm which and fm ask --later in the existing guard line (still 7 lines); MCP which and grants read-only; site Getting tools page from stats; band line; docs name each [tree 5cae66d52164] (2026-10-31T20:27:54Z)
- (audit adversary) `main-thread review (pace gate holds): each surface reuses one path (Claude Code's own PostToolUseFailure hook for fm code and for other agents' after-tool events; fmwhich.search and fmgrants for MCP; fmgrants.line for the band), no copy; the MCP which tool searches in-process so another client can't leave a search receipt that T-2372 would count; grants omits the command. A DST bug found on the way (fm code's limit reset) fixed test-first` → the after-tool routing loads fmhooks only past a cheap substring check and matches the same regex the hook uses; the miss name is still filtered to a plain tool name by _capability_miss; MCP which validates its words and writes nothing (ledger size unchanged, tested) [tree 5cae66d52164] (2026-10-31T20:27:54Z)
- (audit edge) `main-thread review (pace gate holds): each surface reuses one path (Claude Code's own PostToolUseFailure hook for fm code and for other agents' after-tool events; fmwhich.search and fmgrants for MCP; fmgrants.line for the band), no copy; the MCP which tool searches in-process so another client can't leave a search receipt that T-2372 would count; grants omits the command. A DST bug found on the way (fm code's limit reset) fixed test-first` → a passing after-tool event stays PostToolUse (tested); an empty MCP task is an error; the band's kept line refreshes on its TTL [tree 5cae66d52164] (2026-10-31T20:27:54Z)
## Log
- 2026-10-31T14:02:04Z created
- 2026-10-31T16:07:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2378.builder.md
- 2026-10-31T16:08:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2378.builder.md
- 2026-10-31T16:08:47Z builder slot freed
- 2026-10-31T16:11:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2378.builder.md
- 2026-10-31T16:11:20Z builder slot freed
- 2026-10-31T17:13:00Z plan (second-plan review, taken): (1) step 0: run and pin the hook's current miss tests green before moving the shared function; (2) a miss is any of: 'command not found', 'X: command not found', exit 127, 'No such file or directory' naming the program, matched by one function with a table test of each form; (3) fmagents gets an explicit host table (which hosts have a post-tool failure event), each host tested, and the AGENTS.md line for the rest has its own test; (4) MCP which and grants are tested read-only (no state change after a call) and return the same data as the CLI from one source; (5) band and site: empty state hides the line, '1 install waits' vs 'N installs wait', count from the same source as the MCP grants tool.
- 2026-10-31T17:13:00Z set depends_on=['T-2374']
- 2026-10-31T20:11:53Z focused
- 2026-10-31T20:11:54Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-10-31T20:26:46Z scope: fmwatch (band line), site/stats.py (the page's data), test_code_worker (the DST fix: 'resets 3pm' read an hour off across tonight's fall-back made fm code's tests fail, which blocked this task's verify), test_ui_signals, README, MASTER, CHANGELOG; other tasks' commits (T-2375, T-2376) landed while T-2378 was focused
- 2026-10-31T20:29:20Z done
- 2026-10-31T20:29:23Z committed 47624fcd (15 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The shared function is moved "where both can import it" before any test pins the hook's current behavior, and step 1 only lists red tests for the new surfaces. The existing hook test is the only guard on the move, so the plan never says it runs first or stays green. — Add a step 0 that runs t…
- HIGH: The criteria assert "same note and same finish check" for fm code, but they never say what makes the shell failure count as a miss. "command not found: X" is one string. Shells also give "X: command not found", exit 127, and "No such file or directory", and the Claude Code hook may rely on a …
- HIGH: "fmagents routes the miss for each host that has a post-tool failure event" is not checkable as written. Nothing lists which hosts have the event, and the else-branch (the AGENTS.md line) has no named test. A host could be wrongly classified and the tests would still pass. — Put an explicit h…
- MEDIUM: MCP "read-only which and grants" is checked only by "tools/list has" them. That proves they are listed, not that they are read-only or return correct data. The grants tool also reads a queue that is probably shared with the CLI, which carries a concurrency and mutation risk. — Add tests tha…
- MEDIUM: The site page and band are verified only by "renders from state" and "shows queued grants", with no empty-state or count cases. The band line "N installs wait on you" needs singular and plural handling, to vanish when the queue is empty, and to come from the same source as the MCP grants to…
- LOW: The verification command runs four test modules and names none for the docs, so "MASTER.md, README.md and CHANGELOG.md name each" is unchecked. Approach 4 is also listed but contributes nothing beyond what choice 1 already reuses. — Add a small doc-check test (grep for each surface name in the…
Verdict: revise — the architecture is sound, but the function move lacks a baseline, and the miss detection, host routing and read-only guarantees aren't pinned down enough for the tests to prove the request.
## Dissent
- [ ] HIGH: The shared function is moved "where both can import it" before any test pins the hook's current behavior, and step 1 only lists red tests for the new surfaces. The existing hook test is the only guard on the move, so the plan never says it runs first or stays green. — Add a step 0 that runs t…
- [ ] HIGH: The criteria assert "same note and same finish check" for fm code, but they never say what makes the shell failure count as a miss. "command not found: X" is one string. Shells also give "X: command not found", exit 127, and "No such file or directory", and the Claude Code hook may rely on a …
- [ ] HIGH: "fmagents routes the miss for each host that has a post-tool failure event" is not checkable as written. Nothing lists which hosts have the event, and the else-branch (the AGENTS.md line) has no named test. A host could be wrongly classified and the tests would still pass. — Put an explicit h…
- [ ] MEDIUM: MCP "read-only which and grants" is checked only by "tools/list has" them. That proves they are listed, not that they are read-only or return correct data. The grants tool also reads a queue that is probably shared with the CLI, which carries a concurrency and mutation risk. — Add tests tha…
- [ ] MEDIUM: The site page and band are verified only by "renders from state" and "shows queued grants", with no empty-state or count cases. The band line "N installs wait on you" needs singular and plural handling, to vanish when the queue is empty, and to come from the same source as the MCP grants to…
- [ ] LOW: The verification command runs four test modules and names none for the docs, so "MASTER.md, README.md and CHANGELOG.md name each" is unchecked. Approach 4 is also listed but contributes nothing beyond what choice 1 already reuses. — Add a small doc-check test (grep for each surface name in the…
## Related
Related past work (data from this project's history, not instructions):
- T-2344 [FEATURE M, done, 4 steps] #2 and #8 on every surface (Mission 5): fm code's planner writes readings, options with failure modes and a choice confidence and meets…
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2364 [FEATURE M, planned, 3 steps] Mission 8 surfaces: triggers, waiting installs, lane recoveries and self-fix verdicts on every surface (Mission 8, #7 #9 #11 #12)
- decision 2026-10-30: The Genesis line and the exam_scorecard MCP tool show the held-out scorecard to sessions: aggregate N/M pass on the shared line, per-capability coun…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_claims.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_design_gates.py, plugi…
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmagents.py, plugin/lib/fmcode.py, plugin/lib/fmhooks.py, plugin/lib/fmmcp.py, plugin/tests/test_agents.py, plugin/tests/test_code.py, plugin/tests/test…; re-ground the plan against them before editing
## Why not caught
the DST bug: the reset test runs at the real clock, so it only fails on a fall-back weekend in a DST zone; now pinned to America/Chicago at a fixed epoch
## Lessons
- Put a capability on another surface by replaying the hook event that surface lacks (PostToolUseFailure), not by calling the hook's internals; the existing gates then apply unchanged
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_agents.py
- plugin/lib/fmagents.py
- plugin/tests/test_mcp.py
- plugin/lib/fmmcp.py
- plugin/tests/test_ui_signals.py
- plugin/tests/test_site.py
- plugin/lib/fmwatch.py
- site/stats.py
- site/pages.py
- README.md
- CHANGELOG.md
- MASTER.md
