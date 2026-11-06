---
id: T-0956
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:42Z
updated: 2026-10-15T22:00:21Z
base: fb4ada3e5e5634c0581ad42a911a13920c8445b5
base_tree: e6c3c22cb9b9286351354ac864c13ba067169b79
verified: strong
---
# Closing: one verdict line for close warnings, a Landed line, and a leftovers scan
## Raw request
> Closing: one verdict line for close warnings, a Landed line, and a leftovers scan
## Interpretation
Board clusters r2-close-warning-quality (_close_warnings_of, fmcli.py ~1347: fold into 'N warnings: kinds' first), close-out (append 'Landed: committed <sha> · pushed/not pushed' or 'not committed' near fmcli.py ~592 from git status --porcelain and rev-list @{u}..) and r2-diff-and-release-gates (conflict markers and new breakpoint()/debugger/console.log lines in changed non-test files as a close warning, reusing the warnings' file loop).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish prints one 'N warnings: kinds' line before the details — verify with `python3 plugin/tests/run.py -k BoardClose`
- [x] fm task finish ends with a Landed line: committed with the sha and whether it is pushed, or not committed — verify with `python3 plugin/tests/run.py -k BoardClose`
- [x] A changed non-test file with a conflict marker or a newly added breakpoint()/debugger/console.log line yields a close warning — verify with `python3 plugin/tests/run.py -k BoardClose`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardClose class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
MASTER, README, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardClose` → ✗ exit 1 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: BoardClose 1s) / FAILED (1 classes) [ran] [tree 91bc5268520b] (2026-10-15T21:40:48Z)
- (step 2) `python3 plugin/tests/run.py -k BoardClose` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: BoardClose 1s) / OK [ran] [tree 3a5a501533c2] (2026-10-15T21:41:26Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift test_help` → exit 0 · Ran 35 tests in 1.2s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, Help 1s, PromptApprovals 1s) / OK [ran] [tree ae7277d8bd90] (2026-10-15T21:44:55Z)
- (step 2) `python3 plugin/tests/run.py test_execution test_verification` → exit 0 · Ran 20 tests in 2.2s (14 classes, 16 at a time; slowest: BoardClose 2s, SmokeCmd 1s, NotVerified 1s) / OK [ran] [tree 4b6af1985500] (2026-10-15T22:00:17Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardClose` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: BoardClose 2s) / OK [ran] [tree 4b6af1985500] (2026-10-15T22:00:20Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardClose` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: BoardClose 2s) / OK [ran] [tree 4b6af1985500] (2026-10-15T22:00:20Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardClose` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: BoardClose 2s) / OK [ran] [tree 4b6af1985500] (2026-10-15T22:00:20Z)
- (audit intent) `one fm-reviewer pass (sonnet): 1 medium, 4 low plus my own live catch (Landed counted another task's files); all fixed test-first` → one verdict line before the warnings, a Landed line last, conflict markers and debugger lines flagged [tree 4b6af1985500] (2026-10-15T22:00:20Z)
- (audit edge) `one fm-reviewer pass (sonnet): 1 medium, 4 low plus my own live catch (Landed counted another task's files); all fixed test-first` → other tasks' files excluded as the commit excludes them, git failure or no base says unknown, a commit retry also says where it landed [tree 4b6af1985500] (2026-10-15T22:00:20Z)
- (audit operator) `one fm-reviewer pass (sonnet): 1 medium, 4 low plus my own live catch (Landed counted another task's files); all fixed test-first` → the last line answers 'did it land?' without git log [tree 4b6af1985500] (2026-10-15T22:00:20Z)
- (audit maintainer) `one fm-reviewer pass (sonnet): 1 medium, 4 low plus my own live catch (Landed counted another task's files); all fixed test-first` → _theirs is shared by the commit and the Landed line, one rule [tree 4b6af1985500] (2026-10-15T22:00:20Z)
## Log
- 2026-10-15T21:12:42Z created
- 2026-10-15T21:30:35Z grounding: warnings print one by one at fmcli.py:583 (_close_warnings, line 1333/_close_warnings_of 1347); finish flow at fmcli.py:602-837 commits via --commit. Plan: collect the warnings, print 'N warnings: kinds' (kind = the text before the first ':') then the details; the finish path prints a final 'Landed: committed SHA (pushed|not pushed)' or 'Landed: not committed' (git rev-parse HEAD, git branch -r --contains); a new _close_warnings_of rule scans the task's changed non-test files' added lines (git diff) for ^(<<<<<<<|=======|>>>>>>>) and newly added breakpoint()/debugger;/console.log(. Lane-able: fmcli only.
- 2026-10-15T21:38:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0956.builder.md
- 2026-10-15T21:38:56Z focused
- 2026-10-15T21:50:27Z merged worktree-agent-a0e80fb272eae3718 (5 file(s))
- 2026-10-15T21:50:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0e80fb272eae3718
- 2026-10-15T21:57:30Z focused
- 2026-10-15T22:00:20Z done
- 2026-10-15T22:00:21Z committed f188dca (2 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- research brainstorm-round3-probe-20261014: 46 new titles. Grounded:
- decision 2026-10-15: T-0950: no board-leftover probe
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
- start here (files T-0672 touched): plugin/tests/test_safety.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmfriction.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py
## Lessons
- A status line that recomputes what a sibling step decided (which files are mine) must call the same function, or the two disagree on the first shared tree
## Plan gaps
- failed first: step 1 Failing tests in a BoardClose class
## Files touched
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
- plugin/tests/test_verification.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmnight.py
- plugin/lib/fmserve.py
- plugin/tests/test_board_hooks.py
- plugin/tests/test_serve.py
