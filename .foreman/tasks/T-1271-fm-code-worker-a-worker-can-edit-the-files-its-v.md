---
id: T-1271
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T14:15:27Z
updated: 2026-10-20T17:32:45Z
base: b4f884a1fb652afd3eb71db38e78d850c1d38a23
base_tree: 6a1d2a7c35b52e9ad56adb5070dacdfa3cc390c2
plan0_at: 2026-10-20T17:25:36Z
plan0_scope: []
verified: strong
---
# fm code --worker --verify: the worker can't change the files the user's verify names; such edits are put back and reported
## Raw request
> fm code --worker: a worker can edit the files its verify runs (the test itself); flag or refuse a turn that changes a file the verify command names
## Interpretation
The review of T-1214 found a worker can edit the check that judges it: with --verify 'python3 test_calc.py', rewriting test_calc.py to print ok passes the harness's verify. When the user gave the verify, the files it names are the user's spec: a worker turn's edits to them are reverted and reported. Without --verify the plan may ask the worker to write the failing test, so nothing is protected there.
## Assumptions (confidence)
## Acceptance criteria
- [x] with --verify, a worker turn that edits a file or folder the verify command names (test_calc.py, tests/) has that edit put back and reported, and the task still closes on the real check; without --verify, planned test-writing steps stay free — verify with `python3 plugin/tests/run.py test_code_worker`
## Non-goals
## Approach (options → choice → why)
Options: (a) the verify command's words that are paths in the repo (files, and every file under a named folder) are judged as protected in Run.judge; (b) snapshot and compare the verify's output instead (a rewritten test can print anything); (c) run the verify from a pristine copy of HEAD's test files (misses an untracked test the user wrote). Choice: (a). ponytail: a file the test imports (conftest.py, a helper) isn't named, so it isn't protected; the worker's environment can't widen what the verify trusts beyond that.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a worker that rewrites test_calc.py to pass, plus the real fix
2. [x] Protect the verify's named paths in Run.judge when --verify was given; docs
## Resume here
## Docs impact
CHANGELOG and MASTER's Workers bullet
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -v "^$" | tail -25` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 26.6s (1 classes, 16 at a time; slowest: Worker 26s) / FAILED (1 classes) [ran] [tree 8e00f2b2522e] (2026-10-20T17:26:59Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -v "^$" | tail -25` → ✗ exit 1 · Ran 21 tests in 26.6s (1 classes, 16 at a time; slowest: Worker 26s) / FAILED (1 classes) [ran] [tree 47d3a4f215d1] (2026-10-20T17:27:31Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -v "^$" | tail -8` → exit 0 · Ran 21 tests in 30.3s (1 classes, 16 at a time; slowest: Worker 30s) / OK [ran] [tree c4e9da7c1679] (2026-10-20T17:28:08Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -v "^$" | tail -8` → exit 0 · Ran 21 tests in 30.3s (1 classes, 16 at a time; slowest: Worker 30s) / OK [ran] [tree c4e9da7c1679] (2026-10-20T17:28:08Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 21 tests in 26.9s (1 classes, 16 at a time; slowest: Worker 27s) / OK [ran] [tree 7becaf9ac356] (2026-10-20T17:28:42Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_worker.Worker.test_a_folder_the_verify_names_is_protected_too` → ✗ exit 1 · Ran 1 test in 1.221s / FAILED (failures=1) [ran] [tree 72e810e73ee0] (2026-10-20T17:30:35Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 21 tests in 26.2s (1 classes, 16 at a time; slowest: Worker 26s) / OK [ran] [tree c26f2de7615a] (2026-10-20T17:31:15Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 21 tests in 26.3s (1 classes, 16 at a time; slowest: Worker 26s) / OK [ran] [tree 0258afc7c088] (2026-10-20T17:31:53Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 21 tests in 26.3s (1 classes, 16 at a time; slowest: Worker 26s) / OK [ran] [tree 0258afc7c088] (2026-10-20T17:31:53Z)
- (audit intent) `main session reviewed the builder's diff and closed two gaps test-first: a new file in a named folder, and bytecode caches reported as reverts` → the T-1214 review showed a worker could pass by rewriting the test; with the user's own --verify the check is now out of the worker's reach [tree 0258afc7c088] (2026-10-20T17:31:53Z)
- (audit adversary) `main session reviewed the builder's diff and closed two gaps test-first: a new file in a named folder, and bytecode caches reported as reverts` → rewriting, deleting or adding a file under what the verify names is put back (a new conftest.py too); writing outside it (a helper the test imports from elsewhere) still passes, noted in the code; a verify word outside the repo or naming the root is ignored, so '.' can't freeze the whole repo [tree 0258afc7c088] (2026-10-20T17:31:53Z)
- (audit edge) `main session reviewed the builder's diff and closed two gaps test-first: a new file in a named folder, and bytecode caches reported as reverts` → without --verify nothing is protected, so a planned failing-test step stays free; __pycache__ and .pyc under a named folder are left alone; a deleted named file comes back from the snapshot [tree 0258afc7c088] (2026-10-20T17:31:53Z)
- (audit self) `main session reviewed the builder's diff and closed two gaps test-first: a new file in a named folder, and bytecode caches reported as reverts` → no findings [tree 0258afc7c088] (2026-10-20T17:31:53Z)
## Log
- 2026-10-20T14:15:27Z created
- 2026-10-20T17:20:42Z planned from capture
- 2026-10-20T17:25:21Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1271.builder.md
- 2026-10-20T17:25:35Z focused
- 2026-10-20T17:30:20Z merged worktree-agent-a317894e81fe1ebe7 (3 file(s))
- 2026-10-20T17:30:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a317894e81fe1ebe7
- 2026-10-20T17:30:21Z focused
- 2026-10-20T17:32:44Z done
- 2026-10-20T17:32:45Z committed a7560bc7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1214-review: Verdict: changes needed.** The judge works for the tested cases, but several simple moves get past it. [stale: site/pages.py changed since it was…
- research T-0964-harness: 1) **What the harness is.** claude-code-harness is a plan, work, review loop run as skills (`/harness-plan`, `-work`, `-review`, `-sync`, `-rele…
- T-1214 [FEATURE M, done, 3 steps] fm code --worker: an external CLI does the work, and the harness judges its diff and runs the verify — lesson: Judge a worker by what c…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- Protect a folder by prefix, not by the files it held: what a worker adds there can change the check as much as what it edits
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- MASTER.md
- .github/workflows/pages.yml
- .github/workflows/test.yml
- CHANGELOG.md
- plugin/tests/test_workflows.py
