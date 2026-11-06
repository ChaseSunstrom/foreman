---
id: T-2242
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:06:20Z
updated: 2026-10-31T03:07:00Z
inferred_deps: [T-2185, T-2199, T-2238]
inferred_why: T-2185: named in its request; T-2199: named in its request; T-2238: reviews hotspot-ranked files first
base: b3697fd5ed230eafe44a52990a12872d3801f0dd
base_tree: 70ea57ea66b48d4de9b75fb2c8e03204939a0d6d
plan0_at: 2026-10-31T02:01:27Z
plan0_scope: []
verified: strong
---
# fm prove --bugs: a cheap child reviews the hottest files for bug candidates, each proven by a model-written failing test
## Raw request
> fm find bug rung: a cheap tool-less child reviews the top-ranked files (hotspots first) and emits bug candidates, each with a failing test; fm prove runs it on a trusted or exam-sandbox copy with T-2199's stub control, so the bug kind (s0-001: 0/18 found) gets candidates and proofs (T-2185 rung a; after T-2199)
## Interpretation
T-2185 rung a. The exam's finders arm found 0/18 bug scenarios: no lexical finder sees a logic bug. A cheap model reading the files most likely to hold bugs (T-2238's hotspots) can name candidates, and T-2199's _written already proves a candidate with a model-written failing test checked by stub controls. This joins them: candidates in, proofs out, nothing filed without a red test.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove PATH --bugs N (a trusted tree only, never a sensitive project) asks one tool-less child per file for at most 5 bug candidates in the N hottest files (fmfind.hotspots, else the largest source files), keeps only lines it names that exist inside a function, and proves each through _written (red 3/3 with the raise and benign stub controls); proven ones file as bug tasks with --capture, the rest stay leads; the child's reply is untrusted data — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung`
## Non-goals
## Approach (options → choice → why)
Options: (1) a child per hot file returns 'LINE: what is wrong' lines, parsed strictly and proven by _written (chosen: reuses the proof machinery; cost bounded by N files x (1 + 5) small calls); (2) one child over all files (context grows, worse line accuracy); (3) let the child write the test in the same call (unverifiable grounding; _written's separate call keeps the test independent of the claim). Choice 1; default N=3, cap 10.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (FindBugRung) with a stubbed child: candidates parsed strictly, bad lines dropped, a sensitive project and an untrusted tree get none, a proven candidate becomes a bug ticket
2. [x] bug_candidates(root, n) and fm prove --bugs
3. [x] docs (MASTER fmprove, CHANGELOG)
## Resume here
<!-- auto -->
- 2026-10-31T02:42:11Z steps 3/3 done
- git: worktree-agent-a8ea3e31de070bbb8; 15 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmfind.py, plugin/lib/fmgenesis.py, plugin/lib/fmhooks.py, plugin/lib/fmmandate.py, plugin/lib/fmprove.py, plugin/lib/fmserve.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmfind.py, plugin/lib/fmgenesis.py, plugin/lib/fmhooks.py, plugin/lib/fmmandate.py, plugin/lib/fmserve.py, plugin/skills/genesis/SKILL.md, plugin/tests/test_genesis.py, plugin/tests/test_goal.py, plugin/tests/test_hooks.py, plugin/lib/fmprove.py, plugin/tests/test_find.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung 2>&1 | tail -40` → ✗ exit 1 · Ran 7 tests in 2.238s / FAILED (failures=1) [ran] [tree 799ddd487678] (2026-10-31T02:03:09Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung 2>&1 | tail -20` → exit 0 · Ran 7 tests in 1.382s / OK [ran] [tree 0d3ca89b81a5] (2026-10-31T02:03:14Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung 2>&1 | tail -20` → exit 0 · Ran 7 tests in 1.382s / OK [ran] [tree 0d3ca89b81a5] (2026-10-31T02:03:14Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung` → exit 0 · Ran 7 tests in 1.230s / OK [ran] [tree 9e840237176d] (2026-10-31T02:03:26Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find 2>&1 | tail -6` → exit 0 · Ran 72 tests in 32.120s / OK [ran] [tree 9e840237176d] (2026-10-31T02:04:01Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 72 tests in 29.843s / OK [ran] [tree 9e840237176d] (2026-10-31T02:04:33Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [36.70s] [ran] [tree 9e840237176d] (2026-10-31T02:05:50Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|AssertionError)"` → exit 0 · Ran 76 tests in 43.002s / OK [ran] [tree 8ba561cc3eed] (2026-10-31T02:13:06Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree 3603ca38f013] (2026-10-31T02:41:45Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree 3603ca38f013] (2026-10-31T02:41:45Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung` → ✗ exit 1 · Ran 11 tests in 0.662s / FAILED (failures=1, errors=9) (start tree + this task's tests) [ran] [tree 5670d03efa7d] (2026-10-31T03:01:06Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung` → exit 0 · Ran 11 tests in 1.110s / OK [ran] [tree 5670d03efa7d] (2026-10-31T03:01:06Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find test_cli` → exit 0 · Ran 209 tests in 110.836s / OK [ran] [tree 5670d03efa7d] (2026-10-31T03:03:10Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find test_cli` → exit 0 · Ran 209 tests in 116.741s / OK [ran] [tree 5670d03efa7d] (2026-10-31T03:05:07Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find test_cli` → exit 0 · Ran 209 tests in 77.538s / OK [ran] [tree 5670d03efa7d] (2026-10-31T03:06:25Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindBugRung` → exit 0 · Ran 11 tests in 1.107s / OK [ran] [tree 5670d03efa7d] (2026-10-31T03:06:27Z)
- (audit intent) `fm-reviewer five lenses: changes needed, fixed in 40574711 and f291e6c0: a proven bug-rung test is saved and fm prove --only bug-ID reruns it on a fresh copy (red stays open, green is fixed, missing can't pass), keys leave out the model's wording, bug candidates prove first within one deadline, the child sees numbered lines range-checked to what it was sent, the sensitive check reads the tree's own project (also in _written), < and > stripped from says, child failures print, --bugs with --only is a usage error, --bugs N reads clearly; merge with T-2241 resolved keeping both; test_find test_cli green; red-to-green proven` → fm prove --bugs N reviews the hottest files with a cheap child and files only bugs a model-written test shows red with stub controls [tree 5670d03efa7d] (2026-10-31T03:06:27Z)
- (audit adversary) `fm-reviewer five lenses: changes needed, fixed in 40574711 and f291e6c0: a proven bug-rung test is saved and fm prove --only bug-ID reruns it on a fresh copy (red stays open, green is fixed, missing can't pass), keys leave out the model's wording, bug candidates prove first within one deadline, the child sees numbered lines range-checked to what it was sent, the sensitive check reads the tree's own project (also in _written), < and > stripped from says, child failures print, --bugs with --only is a usage error, --bugs N reads clearly; merge with T-2241 resolved keeping both; test_find test_cli green; red-to-green proven` → the child's reply is parsed as line numbers and plain'd, defanged text only; nothing it says runs; no child in an untrusted tree or a sensitive project; credentials stripped from the copy [tree 5670d03efa7d] (2026-10-31T03:06:27Z)
- (audit edge) `fm-reviewer five lenses: changes needed, fixed in 40574711 and f291e6c0: a proven bug-rung test is saved and fm prove --only bug-ID reruns it on a fresh copy (red stays open, green is fixed, missing can't pass), keys leave out the model's wording, bug candidates prove first within one deadline, the child sees numbered lines range-checked to what it was sent, the sensitive check reads the tree's own project (also in _written), < and > stripped from says, child failures print, --bugs with --only is a usage error, --bugs N reads clearly; merge with T-2241 resolved keeping both; test_find test_cli green; red-to-green proven` → a recheck with the saved test missing, a crashing test, a fixed function, lines past the cut, a numeric path argument [tree 5670d03efa7d] (2026-10-31T03:06:27Z)
- (audit operator) `fm-reviewer five lenses: changes needed, fixed in 40574711 and f291e6c0: a proven bug-rung test is saved and fm prove --only bug-ID reruns it on a fresh copy (red stays open, green is fixed, missing can't pass), keys leave out the model's wording, bug candidates prove first within one deadline, the child sees numbered lines range-checked to what it was sent, the sensitive check reads the tree's own project (also in _written), < and > stripped from says, child failures print, --bugs with --only is a usage error, --bugs N reads clearly; merge with T-2241 resolved keeping both; test_find test_cli green; red-to-green proven` → at most 10 files and 10 test children inside one 900 s deadline, each call through fmbudget [tree 5670d03efa7d] (2026-10-31T03:06:27Z)
- (audit maintainer) `fm-reviewer five lenses: changes needed, fixed in 40574711 and f291e6c0: a proven bug-rung test is saved and fm prove --only bug-ID reruns it on a fresh copy (red stays open, green is fixed, missing can't pass), keys leave out the model's wording, bug candidates prove first within one deadline, the child sees numbered lines range-checked to what it was sent, the sensitive check reads the tree's own project (also in _written), < and > stripped from says, child failures print, --bugs with --only is a usage error, --bugs N reads clearly; merge with T-2241 resolved keeping both; test_find test_cli green; red-to-green proven` → bug candidates reuse _written and keyed; the saved test makes a bug task's criterion real [tree 5670d03efa7d] (2026-10-31T03:06:27Z)
## Log
- 2026-10-31T00:06:20Z created
- 2026-10-31T02:01:02Z planned from capture
- 2026-10-31T02:01:03Z set approved=True
- 2026-10-31T02:01:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2242.builder.md
- 2026-10-31T02:01:26Z focused
- 2026-10-31T03:01:02Z merged worktree-agent-a8ea3e31de070bbb8 (6 file(s))
- 2026-10-31T03:01:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8ea3e31de070bbb8
- 2026-10-31T03:01:03Z focused
- 2026-10-31T03:06:25Z scope: plugin/lib/fmprove.py (bug_candidates, _keep, _recheck, --bugs), plugin/lib/fmfind.py (keyed), plugin/lib/fmcli.py (--bugs flag), plugin/tests/test_find.py, MASTER.md, CHANGELOG.md
- 2026-10-31T03:07:00Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2199 [FEATURE M, done, 4 steps] fm prove: model-written failing tests prove vuln, bug, slow and flaky candidates (red… — lesson: A proof that a model-written test exer…
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
- the similar finished task took 4 steps
## Lessons
- A proof that lives in a throwaway copy has to be kept, or the task it files can't be re-checked and its criterion passes empty
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmprove.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/lib/fmfind.py
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmhooks.py
- plugin/lib/fmmandate.py
- plugin/lib/fmserve.py
- plugin/skills/genesis/SKILL.md
- plugin/tests/test_genesis.py
- plugin/tests/test_goal.py
- plugin/tests/test_hooks.py
