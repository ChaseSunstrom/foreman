---
id: T-1669
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdrill.py, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/lib/fmbudget.py, plugin/lib/fmcodebench.py, plugin/lib/fmreplay.py, plugin/lib/fmserve.py, plugin/lib/fmcode.py, plugin/lib/fmsession.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/lib/fmcodetui.py, plugin/tests/test_drill.py, plugin/tests/test_design_gates.py, plugin/tests/test_reliability_tools.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:59:18Z
updated: 2026-10-28T16:41:47Z
base: 14ed36ef1418da1f0b1bdc926e2f8be665bdf0a5
base_tree: 4d41fc8eba918f973ed112da610232f7dda19073
plan0_at: 2026-10-28T16:09:02Z
plan0_scope: [plugin/lib/fmdrill.py, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/tests/test_drill.py, plugin/tests/test_design_gates.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155
## Raw request
> fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-1552; waits: after fm fsck)
## Interpretation
Two parts from T-1552. (1) fm drill [--seed N] [--faults K]: a scripted Foreman day (init, task new, hooks, log, evidence, checkpoint, capture) in a temp home, with K>=3 seeded faults planted at random steps and left in place so they overlap (torn ledger, torn journal, stale lock, broken lane, corrupt JSON state, unreadable journal); passes when no step crashes, fm fsck / fm verify-ledger name each fault they cover, fsck --fix clears the locks and the task reads back; the same seed replays the same plan. (2) Design gates get a third mode, trial: advisory until 10 distinct would-blocks at under 10% marked wrong (fm design check --wrong GATE), then blocking; the same rolling window demotes it; fm design check shows the rate.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm drill passes a seeded compound-fault day in a temp home, names each planted fault, replays a seed; a trial gate promotes and demotes by its overridden rate — verify with `python3 plugin/tests/run.py test_drill test_design_gates`
## Non-goals
## Approach (options → choice → why)
Drill: (a) subprocess day in a temp home with seeded planted faults (chosen: tests the real CLI and hooks, reuses fsck's fault kinds, no coupling to internals); (b) in-process fault injection by monkeypatching os.write/open (deeper but brittle, coupled); (c) replay recorded real session payloads (realistic, but needs recordings and leaks private text). Promotion: (a) trial mode in DESIGN.md with a rolling window of distinct would-blocks and explicit --wrong overrides (chosen: measured, reversible, no new config); (b) per-gate thresholds in project settings (config for values that never change); (c) promote on a pass streak (measures nothing about false positives).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: test_drill, trial gate in test_design_gates
2. [x] fm drill (fmdrill.py, fmcli verb)
3. [x] trial gate mode and --wrong in fmdesign
4. [x] docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-28T16:30:00Z step 2/4: fm drill (fmdrill.py, fmcli verb)
- git: foreman/build; 18 uncommitted: plugin/lib/fmbudget.py, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodebench.py, plugin/lib/fmcodetui.py, plugin/lib/fmcore.py, plugin/lib/fmdesign.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/lib/fmplaybooks.py
- touched since last checkpoint: plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/lib/fmbudget.py, plugin/lib/fmcodebench.py, plugin/lib/fmplaybooks.py, plugin/lib/fmreplay.py, plugin/lib/fmserve.py, plugin/lib/fmsession.py, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmrecall.py, plugin/lib/fmdrill.py, plugin/lib/fmcli.py, plugin/lib/fmdesign.py
- failures met: ls: cannot access 'logs/': no such file or directory
## Docs impact
MASTER: fmdrill bullet, trial gate on the fmdesign line, fsck corrupt state; CHANGELOG: drill and trial
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_drill test_design_gates test_reliability_tools` → ✗ exit 1 (never ran: no tests ran) · Ran 36 tests in 4.3s (6 classes, 16 at a time; slowest: Fsck 4s, Trial 1s, GateLock 1s) / FAILED (3 classes) [ran] [tree 66dc46449db7] (2026-10-28T16:22:26Z)
- (step 2) `python3 plugin/tests/run.py test_drill test_reliability_tools` → exit 0 · Ran 25 tests in 4.3s (4 classes, 16 at a time; slowest: Fsck 4s, Drill 3s, GateLock 1s) / OK [ran] [tree a54793f514aa] (2026-10-28T16:31:44Z)
- (step 3) `python3 plugin/tests/run.py test_design_gates test_design` → exit 0 · Ran 105 tests in 3.4s (17 classes, 16 at a time; slowest: Extract 3s, Trial 2s, Tokens 2s) / OK [ran] [tree a54793f514aa] (2026-10-28T16:31:51Z)
- (step 4) `grep -c 'T-1669' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:3 / CHANGELOG.md:2 [ran] [tree 710722fb79a8] (2026-10-28T16:32:06Z)
- (audit intent) `fm-reviewer T-1669-review` → AC met; would-block unit is a changed UI state while a must fails (documented: a rerun on the same code adds none); skipped faults stay named in the report [tree 44f7db247269] (2026-10-28T16:36:17Z)
- (audit adversary) `fm-reviewer T-1669-review` → --wrong is a self-report like editing DESIGN.md (now said in MASTER); PermissionError state errors limited to paths in the state folder (fixed, tested) [tree 44f7db247269] (2026-10-28T16:36:17Z)
- (audit edge) `fm-reviewer T-1669-review` → --wrong outside a project now errors (fixed); trial a11y gets blocking strictness (fixed); concurrent checks may double-count a would-block (accepted: rare, one person's checks) [tree 44f7db247269] (2026-10-28T16:36:18Z)
- (audit operator) `fm-reviewer T-1669-review` → MASTER fsck clause moved after the journal clause (fixed); remaining open(a) appenders are logs and lists, not hash-chained journals [tree 44f7db247269] (2026-10-28T16:36:18Z)
- (audit maintainer) `fm-reviewer T-1669-review` → failure-path drill test added (missed verdict -> not ok, home kept, FAILED); local blocks renamed hits [tree 44f7db247269] (2026-10-28T16:36:18Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 74 tests in 9.1s (18 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 44f7db247269] (2026-10-28T16:36:20Z)
- (step 1) `python3 plugin/tests/run.py test_drill test_design_gates test_reliability_tools` → exit 0 · Ran 45 tests in 4.4s (7 classes, 16 at a time; slowest: Fsck 4s, Drill 4s, Trial 2s) / OK [ran] [tree 44f7db247269] (2026-10-28T16:40:10Z)
- (ac 1) `python3 plugin/tests/run.py test_drill test_design_gates` → exit 0 · Ran 27 tests in 4.0s (5 classes, 16 at a time; slowest: Drill 4s, Trial 2s, StateErrors 1s) / OK [ran] [tree 44f7db247269] (2026-10-28T16:40:15Z)
- (audit self) `one fm-reviewer pass over five lenses; six findings fixed test-first, two accepted with reasons; full gates green` → 24-seed drill sweep all pass; a missed fault fails and keeps the home [tree 44f7db247269] (2026-10-28T16:40:15Z)
## Log
- 2026-10-22T20:59:18Z created
- 2026-10-28T16:08:55Z set tier=M, scope=['plugin/lib/fmdrill.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmdesign.py', 'plugin/tests/test_drill.py', 'plugin/tests/test_design_gates.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-28T16:09:01Z focused
- 2026-10-28T16:10:51Z paused: focus moved to T-1840
- 2026-10-28T16:11:26Z focused
- 2026-10-28T16:18:04Z scope: fmcore.py, fmhooks.py, fmdoctor.py, fmcli.py handler and the jsonl appenders: the drill found corrupt meta.json unnamed (fm doctor dies on it, hooks crash silently), an unreadable ledger crashing every fm verb with a traceback, and torn jsonl tails gluing the next record; all block the drill's exit-0 criterion
- 2026-10-28T16:21:53Z scope: test_reliability_tools.py (fsck's corrupt-state test sits with the other fsck tests)
- 2026-10-28T16:22:55Z set scope=['plugin/lib/fmdrill.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmdesign.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmbudget.py', 'plugin/lib/fmcodebench.py', 'plugin/lib/fmreplay.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmcode.py', 'plugin/lib/fmsession.py', 'plugin/lib/fmplaybooks.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_drill.py', 'plugin/tests/test_design_gates.py', 'plugin/tests/test_reliability_tools.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-28T16:41:45Z done
- 2026-10-28T16:41:47Z committed 06520890 (20 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1552 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Reliability tooling: one machine-wide gate lock for release checks and t
- T-1667 [FEATURE M, done, 3 steps] fm fsck: a read-only report of broken worktrees, stale locks and torn journals, --fix for the safe repairs — lesson: A dead-pid check i…
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- decision 2026-10-22: T-1405: an unreadable /proc process of ours keeps a stale index.lock only when it is a git; any other unreadable process doesn't block (31 of this h…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/tests/test_design_gates.py; re-ground the plan against them before editing
## Lessons
- A corrupt meta.json hides its project from all_projects, so a drill must re-check after repair; a self-check needs a test that shows it can fail
## Plan gaps
- failed first: step 1 failing tests: test_drill, trial gate in test_design_gates
## Files touched
- plugin/tests/test_drill.py
- plugin/tests/test_reliability_tools.py
- plugin/tests/test_design_gates.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmbudget.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodebench.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmrecall.py
- plugin/lib/fmreplay.py
- plugin/lib/fmserve.py
- plugin/lib/fmsession.py
- plugin/lib/fmdrill.py
- plugin/lib/fmdesign.py
- CHANGELOG.md
- MASTER.md
