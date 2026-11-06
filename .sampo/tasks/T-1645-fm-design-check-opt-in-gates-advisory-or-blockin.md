---
id: T-1645
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_gates.py, plugin/skills/ui-design/SKILL.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-22T20:58:11Z
updated: 2026-10-23T02:16:50Z
base: a55e3fb929597c88313001ef0ef9a43d9119ccdc
base_tree: 3775267d763399c6272a70ec0841738b74747ea5
plan0_at: 2026-10-23T02:11:08Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_gates.py, CHANGELOG.md]
verified: strong
---
# fm design check: opt-in gates, advisory or blocking, starting with the executable design brief
## Raw request
> fm design check: opt-in gates, advisory or blocking, starting with the executable design brief
## Interpretation
fm design check runs design gates a project opts into in DESIGN.md (advisory by default, blocking when marked): the first gate is the executable brief, where DESIGN.md's Direction section lists must-haves (a palette, a type pair, a motion rule) and the gate checks the code for them. Advisory gates exit 0 with findings; blocking ones exit 1, so fm check can include it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a brief gate on a fixture project reports pass or fail with a reason and exits 0 while advisory — verify with `python3 plugin/tests/run.py test_design_gates.Brief`
## Non-goals
## Approach (options → choice → why)
Options: always-blocking gates (people turn them off); advisory only (ignored); opt-in with an advisory/blocking switch. Choice: opt-in with the switch, starting advisory: a team promotes a gate once its false-positive rate is known.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] gate registry with an advisory flag
3. [x] brief contract gate
## Resume here
## Docs impact
plugin/skills/ui-design/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_gates.Brief` → red as expected (exit 1) · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Brief 1s) / FAILED (1 classes) [ran] [tree cafa9d3678eb] (2026-10-23T02:11:18Z)
- (step 2) `python3 plugin/tests/run.py test_design_gates test_design_lint test_docs` → exit 0 · Ran 101 tests in 8.9s (19 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Brief 1s) / OK [ran] [tree 1d3005dc3d31] (2026-10-23T02:15:02Z)
- (step 3) `python3 plugin/tests/run.py test_design_gates test_design_lint test_docs` → exit 0 · Ran 101 tests in 8.6s (19 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 2s, Brief 1s) / OK [ran] [tree 1d3005dc3d31] (2026-10-23T02:15:12Z)
- (ac 1) `python3 plugin/tests/run.py test_design_gates.Brief` → exit 0 · Ran 6 tests in 0.9s (1 classes, 16 at a time; slowest: Brief 1s) / OK [ran] [tree 1d3005dc3d31] (2026-10-23T02:15:13Z)
- (ac 1) `python3 plugin/tests/run.py test_design_gates.Brief` → exit 0 · Ran 6 tests in 1.7s (1 classes, 16 at a time; slowest: Brief 1s) / OK [ran] [tree 1d3005dc3d31] (2026-10-23T02:15:40Z)
- (audit intent) `self-review with an adversary and edge pass: DESIGN.md is project data, so must: text is matched as a literal substring (no regex), sizes capped (60-char families, 200-char musts), labels and file names cleaned of control and bidi characters before printing (tested); UI files come from fmdesign.collect (size and count capped, vendored dirs skipped); other design actions still require their argument (tested)` → fm design check runs the gates DESIGN.md opts into; the brief gate reports each must-have pass or fail with where it was found; advisory exits 0, blocking 1 [tree 1d3005dc3d31] (2026-10-23T02:15:40Z)
- (audit adversary) `self-review with an adversary and edge pass: DESIGN.md is project data, so must: text is matched as a literal substring (no regex), sizes capped (60-char families, 200-char musts), labels and file names cleaned of control and bidi characters before printing (tested); UI files come from fmdesign.collect (size and count capped, vendored dirs skipped); other design actions still require their argument (tested)` → no regex from DESIGN.md; terminal output cleaned; nothing written [tree 1d3005dc3d31] (2026-10-23T02:15:40Z)
- (audit edge) `self-review with an adversary and edge pass: DESIGN.md is project data, so must: text is matched as a literal substring (no regex), sizes capped (60-char families, 200-char musts), labels and file names cleaned of control and bidi characters before printing (tested); UI files come from fmdesign.collect (size and count capped, vendored dirs skipped); other design actions still require their argument (tested)` → no DESIGN.md or no ## Gates → nothing checked and said so; unknown gate or mode is a note (an unknown mode reads as advisory); durations match 200ms, .2s and 0.2s [tree 1d3005dc3d31] (2026-10-23T02:15:40Z)
## Log
- 2026-10-22T20:58:11Z created
- 2026-10-22T20:58:12Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_gates.py', 'CHANGELOG.md']
- 2026-10-22T20:58:13Z split from T-1535 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:57Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_design_gates.Brief`
- 2026-10-22T21:30:20Z criterion 1 text: a brief gate on a fixture project reports pass or fail with a reason and exits 0 while advisory — verify with python3 plugin/tests/run.py test_design_gates.Brief → a brief gate on a fixture project reports pass or fail with a reason and exits 0 while advisory
- 2026-10-23T02:11:07Z focused
- 2026-10-23T02:11:15Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_gates.py', 'plugin/skills/ui-design/SKILL.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T02:16:48Z done
- 2026-10-23T02:16:50Z committed 9e51167b (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1628-review: Verdict: approve with nits.** I read the code only and ran no tests; this session had no execution tool. The rule is cheap and its fixtures match…
- research T-1501-review: Verdict:** approve with nits. I found no HIGH issues and did not run the tests. I traced each `AUDIT_LENSES` consumer by reading the code. [stale…
- research T-1507-review: Verdict: changes needed.** The maths is sound. The problems are in extract's file handling, its speed on hostile input, and how a Tokens-only DES…
- decision 2026-10-15: New installs ask before turning on bypassPermissions (default No on a terminal; --bypass opts in; no terminal leaves the mode alone)
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py; re-ground the plan against them before editing
## Lessons
- Making a positional optional for one action silently loosens it for the rest; re-require it per action and test that
## Files touched
- plugin/tests/test_design_gates.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/ui-design/SKILL.md
