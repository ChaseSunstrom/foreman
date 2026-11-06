---
id: T-2258
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2162]
source: followup
created: 2026-10-31T03:42:17Z
updated: 2026-10-31T04:14:43Z
base: c8e5da7514590e2030e510997a0685a16c5959c3
base_tree: 69c342b136afcbdff02ccff6ba1606b2f33da8f6
plan0_at: 2026-10-31T03:43:13Z
plan0_scope: []
verified: strong
---
# Long-horizon exam (1/3): fm exam long gen/run/grade from local git history, oracle and empty arms
## Raw request
> Long-horizon exam (1/3): fm exam long gen/run/grade from local git history, oracle and empty arms
## Interpretation
Steer 2026-10-30 rule 3: the deciding end-of-run score is a long-horizon tier: real past changes replayed from their base, hidden checks from what shipped. Slice 1 is the harness with zero-token arms (oracle, empty) so the tier is exam-checked before any session runs on it; slices 2 and 3 add the session arms with faults and the full metrics.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam long gen [--from PATH] [--n N] turns a trusted local repo's history (default: Foreman's own) into N goals: each a past task's multi-commit change (commits ending '(T-NNNN)'), the repo rendered at the change's base as a fresh one-commit repo (no future history), the goal text from the change, and hidden checks = the test functions the change added, kept only when they fail at the base and pass at the target; fm exam long run RUN --agent oracle|empty and fm exam long grade RUN score true-done (hidden checks pass) and regressions (base-passing sampled tests that now fail) per goal into the tower's exam.jsonl as tier long — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
Options: (1) a separate module fmlong with gen/run/grade over local git history (chosen: fmexam is 1500 lines of planted-defect scenarios; this is a different scenario source and grader); (2) fold into fmexam as a new kind (one scenario per kind doesn't fit a multi-commit goal); (3) clone public repos (forbidden: gen-0 NEVER sweep or clone outside repos). Choice 1; repo code runs only in a trusted tree (Foreman's home, or fm prove --yes-run's) on a throwaway copy.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (test_long) on a temp git repo with three task changes: gen picks the windows, renders no future history, keeps only checks red at base and green at target; oracle scores true-done, empty doesn't; an untrusted --from refuses to run code
2. [x] fmlong.py: gen, run (oracle, empty), grade; fm exam long wired in fmcli
3. [x] docs (MASTER, CHANGELOG)
## Resume here
<!-- auto -->
- 2026-10-31T03:54:14Z step 1/3: red tests (test_long) on a temp git repo with three task changes: gen picks the windows, renders no future history, keeps only checks red at base and green at target; oracle scores true-done, empty doesn't; an untrusted --from refuses to run code
- git: worktree-agent-a0496f3d827dea091; 3 uncommitted: plugin/lib/fmexam.py, plugin/lib/fmlong.py, plugin/tests/test_long.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmlong.py, plugin/lib/fmexam.py, plugin/tests/test_long.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -40` → ✗ exit 1 · Ran 9 tests in 8.8s (7 classes, 16 at a time; slowest: Long 5s, Approvals 4s, Stop 4s) / FAILED (1 classes) [ran] [tree 6dff3e718577] (2026-10-31T03:45:44Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -30` → exit 0 · Ran 9 tests in 4.5s (7 classes, 16 at a time; slowest: Long 4s, Approvals 3s, Stop 2s) / OK [ran] [tree 3e9a827ab9b3] (2026-10-31T03:46:10Z)
- (step 2) `python3 plugin/tests/run.py test_long 2>&1 | tail -30` → exit 0 · Ran 9 tests in 4.5s (7 classes, 16 at a time; slowest: Long 4s, Approvals 3s, Stop 2s) / OK [ran] [tree 3e9a827ab9b3] (2026-10-31T03:46:10Z)
- (step 3) `python3 plugin/tests/run.py test_long test_exam test_cli 2>&1 | tail -15` → exit 0 · Ran 185 tests in 91.8s (57 classes, 16 at a time; slowest: ExamAuthors 91s, ExamGen 62s, TaskLifecycle 50s) / OK [ran] [tree 3e9a827ab9b3] (2026-10-31T03:47:45Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 9 tests in 3.5s (7 classes, 16 at a time; slowest: Long 3s, Approvals 3s, Stop 2s) / OK [ran] [tree 3e9a827ab9b3] (2026-10-31T03:47:53Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -40` → ✗ exit 1 · Ran 14 tests in 4.7s (7 classes, 16 at a time; slowest: Long 4s, Approvals 1s, Stop 1s) / FAILED (1 classes) [ran] [tree 336cfdcfabcf] (2026-10-31T03:53:56Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | grep -v "Warning\|^ " | tail -30` → ✗ exit 1 · Ran 14 tests in 5.1s (7 classes, 16 at a time; slowest: Long 5s, Approvals 1s, Stop 1s) / FAILED (1 classes) [ran] [tree 6a4bf2eef26b] (2026-10-31T03:54:08Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -15` → exit 0 · Ran 14 tests in 5.0s (7 classes, 16 at a time; slowest: Long 5s, Approvals 1s, Stop 1s) / OK [ran] [tree 00af60782f28] (2026-10-31T03:54:54Z)
- (step 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -15` → exit 0 · Ran 14 tests in 5.0s (7 classes, 16 at a time; slowest: Long 5s, Approvals 1s, Stop 1s) / OK [ran] [tree 00af60782f28] (2026-10-31T03:54:54Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 14 tests in 16.6s (7 classes, 16 at a time; slowest: Long 15s, Approvals 4s, AuditPrep 4s) / OK [ran] [tree bdfd748200b0] (2026-10-31T03:56:42Z)
- `cd plugin/tests && python3 -m unittest -q test_long test_exam` → ✗ exit 1 · Ran 43 tests in 179.509s / FAILED (failures=7, errors=1) (start tree + this task's tests) [ran] [tree 4c85c5db575e] (2026-10-31T04:09:36Z)
- `cd plugin/tests && python3 -m unittest -q test_long test_exam` → exit 0 · Ran 43 tests in 183.971s / OK [ran] [tree 4c85c5db575e] (2026-10-31T04:09:36Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_long test_exam test_docs` → exit 0 · Ran 106 tests in 194.486s / OK [ran] [tree 4c85c5db575e] (2026-10-31T04:13:17Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 14 tests in 5.1s (7 classes, 16 at a time; slowest: Long 5s, Approvals 1s, Stop 1s) / OK [ran] [tree 4c85c5db575e] (2026-10-31T04:13:23Z)
- (audit intent) `self + one fm-reviewer pass (12 findings, all fixed with tests); spot-checked: runner runs python -I -B from outside the tree with FOREMAN_/CLAUDE/credential env stripped, in its own process group; key re-validated at grade (id regex, safe paths, 40-hex revs)` → gen turns past multi-commit task changes into goals with hidden checks from the tests each added; oracle and empty arms grade as tier long exam lines (test_long red-to-green proven) [tree 4c85c5db575e] (2026-10-31T04:13:23Z)
- (audit adversary) `self + one fm-reviewer pass (12 findings, all fixed with tests); spot-checked: runner runs python -I -B from outside the tree with FOREMAN_/CLAUDE/credential env stripped, in its own process group; key re-validated at grade (id regex, safe paths, 40-hex revs)` → an answer tree shadowing unittest or adding a root test_app.py can't pass; ids and paths untrusted at grade; runner timeout returns None, not all-red [tree 4c85c5db575e] (2026-10-31T04:13:23Z)
- (audit edge) `self + one fm-reviewer pass (12 findings, all fixed with tests); spot-checked: runner runs python -I -B from outside the tree with FOREMAN_/CLAUDE/credential env stripped, in its own process group; key re-validated at grade (id regex, safe paths, 40-hex revs)` → a renamed unanswered goal still counts in the denominator; gen that keeps nothing exits non-zero without spending a run id; --n 0 is a usage error [tree 4c85c5db575e] (2026-10-31T04:13:23Z)
## Log
- 2026-10-31T03:42:17Z created
- 2026-10-31T03:42:46Z set approved=True
- 2026-10-31T03:42:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2258.builder.md
- 2026-10-31T03:43:13Z focused
- 2026-10-31T04:03:25Z merged worktree-agent-a0496f3d827dea091 (6 file(s))
- 2026-10-31T04:03:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0496f3d827dea091
- 2026-10-31T04:03:26Z focused
- 2026-10-31T04:13:17Z scope: plugin/lib/fmlong.py (new), plugin/lib/fmexam.py (tier long summary), plugin/lib/fmcli.py (exam long parser), plugin/tests/test_long.py, MASTER.md, CHANGELOG.md
- 2026-10-31T04:14:43Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2160 [FEATURE M, done, 3 steps] Write the steer's standing rules (testing cadence, real coverage, long-horizon tier as… — lesson: Two readers of the same rows (steer_c…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
- decision 2026-10-30: [revisited: long-horizon tier is the deciding end-of-run score] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run]…
## Lessons
- A held-out check built from a change's own tests is only honest if it is red at the base and green after, run in an interpreter that can't import the answer's shadows
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- plugin/lib/fmexam.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
