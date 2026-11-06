---
id: T-1639
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmflow.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/tests/test_flow.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:57:54Z
updated: 2026-10-23T02:42:38Z
base: 23c1ebdcbd219cd85737c88ad3349654aabfa114
base_tree: fcce3a810dc1964820a962bf44db0e6b195d715e
plan0_at: 2026-10-23T02:08:22Z
plan0_scope: [plugin/lib/fmflow.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/tests/test_flow.py, CHANGELOG.md]
verified: strong
---
# fm flow FILE: a user journey (goto, click, type, expect) run as a verify command that fails on a missing element
## Raw request
> fm flow FILE: a user journey (goto, click, type, expect) run as a verify command that fails on a missing element
## Interpretation
fm flow FILE runs a user journey written as steps (goto URL, click SELECTOR, type SELECTOR TEXT, expect SELECTOR [TEXT], wait MS) through the smoke harness's optional browser; it exits non-zero naming the step that failed, so it can be a criterion's verify command. Without a browser it says so and exits 2 (not a pass).
## Assumptions (confidence)
## Acceptance criteria
- [x] a journey whose expect misses its selector exits non-zero naming the step — verify with `python3 plugin/tests/run.py test_flow.Journey`
## Non-goals
## Approach (options → choice → why)
Options: Playwright test files (a JS toolchain per project); a tiny line-based journey format run by our harness; recorded clicks (brittle). Choice: the line format: readable in a brief, parsed in Python, driven by the existing cjs harness.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with parsed steps and a stub driver
2. [x] parser and runner
3. [x] optional browser driver
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_flow.Journey` → ✗ exit 1 · run.py: no test matches test_flow.Journey [ran] [tree aafef56eb793] (2026-10-23T02:11:23Z)
- (step 2) `python3 plugin/tests/run.py test_flow.Journey test_flow.Untrusted` → exit 0 · Ran 13 tests in 7.4s (2 classes, 16 at a time; slowest: Journey 7s, Untrusted 5s) / OK [ran] [tree 40be46b46733] (2026-10-23T02:14:59Z)
- (step 3) `python3 plugin/tests/run.py test_flow` → exit 0 · Ran 14 tests in 6.8s (3 classes, 16 at a time; slowest: Journey 7s, Untrusted 5s, InABrowser 1s) / OK [ran] [tree 40be46b46733] (2026-10-23T02:15:06Z)
- (step 1) `python3 plugin/tests/run.py test_flow.Journey` → exit 0 · Ran 7 tests in 6.6s (1 classes, 16 at a time; slowest: Journey 6s) / OK [ran] [tree 40be46b46733] (2026-10-23T02:15:16Z)
- (step 1) `python3 plugin/tests/run.py test_flow.Journey` → exit 0 · Ran 10 tests in 10.7s (1 classes, 16 at a time; slowest: Journey 10s) / OK [ran] [tree e35a8b245dae] (2026-10-23T02:31:39Z)
- (step 2) `python3 plugin/tests/run.py test_flow.Journey test_flow.Untrusted test_flow.BrowserClose` → exit 0 · Ran 19 tests in 10.5s (3 classes, 16 at a time; slowest: Journey 10s, Untrusted 8s, BrowserClose 1s) / OK [ran] [tree e35a8b245dae] (2026-10-23T02:31:54Z)
- (step 3) `python3 plugin/tests/run.py test_flow test_fmshot` → exit 0 · Ran 49 tests in 46.4s (8 classes, 16 at a time; slowest: Diff 46s, Untrusted 31s, Journey 19s) / OK [ran] [tree e35a8b245dae] (2026-10-23T02:32:41Z)
- (ac 1) `python3 plugin/tests/run.py test_flow test_fmshot test_doctor` → exit 0 · Ran 114 tests in 23.3s (30 classes, 16 at a time; slowest: Diff 23s, Journey 11s, Capture 9s) / OK [ran] [tree 6b6644fc3b99] (2026-10-23T02:41:33Z)
- (ac 1) `python3 plugin/tests/run.py test_flow.Journey` → exit 0 · Ran 10 tests in 10.5s (1 classes, 16 at a time; slowest: Journey 10s) / OK [ran] [tree 6b6644fc3b99] (2026-10-23T02:41:44Z)
- (audit intent) `fm-reviewer pass (shared with T-1648); HIGH fixed: goto opens only files under the flow's folder after resolving links (/etc/passwd, ../x, file:///etc, outside links, dirs refused); MEDIUMs: backslash/userinfo/whitespace/control URLs refused and the rebuilt URL navigated; every request goes through CDP Fetch and anything outside the policy fails, a page load that leaves fails its step naming the URL; LOWs: wait not clamped by --timeout, malformed replies fail the step, public fmshot helpers, bounded close, real-browser ACT tests` → fm flow FILE runs goto/click/type/expect/wait in headless Chromium as a verify command: exit 1 names the failed step, 2 with no browser, never a pass [tree 6b6644fc3b99] (2026-10-23T02:41:44Z)
- (audit adversary) `fm-reviewer pass (shared with T-1648); HIGH fixed: goto opens only files under the flow's folder after resolving links (/etc/passwd, ../x, file:///etc, outside links, dirs refused); MEDIUMs: backslash/userinfo/whitespace/control URLs refused and the rebuilt URL navigated; every request goes through CDP Fetch and anything outside the policy fails, a page load that leaves fails its step naming the URL; LOWs: wait not clamped by --timeout, malformed replies fail the step, public fmshot helpers, bounded close, real-browser ACT tests` → a flow from a cloned repo can't read files outside its folder or reach the network beyond localhost (Fetch-level blocking, not just the first URL); selectors and text reach the page only as JSON args to one fixed function [tree 6b6644fc3b99] (2026-10-23T02:41:44Z)
- (audit edge) `fm-reviewer pass (shared with T-1648); HIGH fixed: goto opens only files under the flow's folder after resolving links (/etc/passwd, ../x, file:///etc, outside links, dirs refused); MEDIUMs: backslash/userinfo/whitespace/control URLs refused and the rebuilt URL navigated; every request goes through CDP Fetch and anything outside the policy fails, a page load that leaves fails its step naming the URL; LOWs: wait not clamped by --timeout, malformed replies fail the step, public fmshot helpers, bounded close, real-browser ACT tests` → a click that navigates is caught after 0.25 s or by the next step, and blocked either way; a hung browser ends the step; the 600 s journey limit holds [tree 6b6644fc3b99] (2026-10-23T02:41:44Z)
- (audit maintainer) `fm-reviewer pass (shared with T-1648); HIGH fixed: goto opens only files under the flow's folder after resolving links (/etc/passwd, ../x, file:///etc, outside links, dirs refused); MEDIUMs: backslash/userinfo/whitespace/control URLs refused and the rebuilt URL navigated; every request goes through CDP Fetch and anything outside the policy fails, a page load that leaves fails its step naming the URL; LOWs: wait not clamped by --timeout, malformed replies fail the step, public fmshot helpers, bounded close, real-browser ACT tests` → fm flow uses fmshot's public helpers, no second CDP client [tree 6b6644fc3b99] (2026-10-23T02:41:44Z)
## Log
- 2026-10-22T20:57:54Z created
- 2026-10-22T20:57:55Z set scope=['plugin/lib/fmflow.py', 'plugin/lib/fmcli.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_flow.py', 'CHANGELOG.md']
- 2026-10-22T20:57:56Z split from T-1532 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:55Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_flow.Journey`
- 2026-10-22T21:30:19Z criterion 1 text: a journey whose expect misses its selector exits non-zero naming the step — verify with python3 plugin/tests/run.py test_flow.Journey → a journey whose expect misses its selector exits non-zero naming the step
- 2026-10-23T02:08:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1639.builder.md
- 2026-10-23T02:08:22Z focused
- 2026-10-23T02:41:00Z merged worktree-agent-ae000c461ef3a0551 (7 file(s))
- 2026-10-23T02:41:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae000c461ef3a0551
- 2026-10-23T02:41:08Z focused
- 2026-10-23T02:41:33Z scope: plugin/lib/fmshot.py (public safe/usable/find_browser/killable, Browser.send/on, bounded close), fmdoctor.py (fmshot.safe), MASTER.md, fmcli flow slot
- 2026-10-23T02:42:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1532 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Journeys and states: fm flow runs user journeys as verify commands, fm s
- T-1636 [FEATURE M, done, 3 steps] fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser — lesson: Headless Chro…
- T-1642 [FEATURE M, planned, 3 steps] fm critique: a computed-style census critiqued against DESIGN.md, and why-does-this-look-like-this for a selector
- decision 2026-10-22: Round-3 L tasks split into 34 M/S children (T-1618..T-1669, T-1609/T-1610 for T-1513); the parts recon judged speculative went to the inbox as follo…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmflow.py, plugin/lib/smoke_web.cjs, plugin/tests/test_flow.py; re-ground the plan against them before editing
## Lessons
- A URL policy checked only at the first navigation isn't a policy: enforce it on every request at the protocol level
## Plan gaps
- failed first: step 1 failing test with parsed steps and a stub driver
## Files touched
- plugin/tests/test_flow.py
- plugin/lib/fmflow.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcost.py
- plugin/lib/fmdesign.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmshot.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/fixtures/design-surfaces/DESIGN.md
- plugin/tests/test_design_gates.py
- plugin/tests/test_design_surfaces.py
- plugin/tests/test_doctor.py
- plugin/tests/test_fmshot.py
- plugin/lib/fmhooks.py
- plugin/lib/fmroll.py
- plugin/tests/test_design_tokens.py
- plugin/tests/test_docs.py
- plugin/tests/test_hooks.py
- plugin/tests/test_looks_gallery.py
