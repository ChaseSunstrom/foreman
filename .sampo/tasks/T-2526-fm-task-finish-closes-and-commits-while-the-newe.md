---
id: T-2526
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_finish.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T02:38:13Z
updated: 2026-11-02T02:57:03Z
base: 048da03ec0fe4d21da1a5718dba29a4c98e2092a
base_tree: 3b9d40624dc2187df54249e9b8550d734c95fda9
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T02:45:24Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_finish.py, CHANGELOG.md]
verified: strong
---
# fm task finish refuses while the newest full fm check on this tree failed
## Raw request
> fm task finish closes and commits while the newest full fm check on the same tree is red: T-2334 closed (2fb3b24c) right after its gate failed test_proof.Proof (finish runs only the criteria and fm check --affected). Refuse a close whose tree's latest full check_run failed, naming the failing gate, unless a newer passing run exists
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish refuses a close (exit 2, nothing committed) when the newest check_run on the current tree (c.worktree_id) is a full run (no skip_tests) with a failing gate, naming that gate and its failing tests; a newer passing run on the tree, or no full run on it, lets the close go as before — verify with `python3 plugin/tests/run.py test_finish_proved test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: log a failing full check_run for the current tree (as fm check does), fm task finish refuses naming the gate; log a passing one after it, finish goes
2. [x] fmcli finish: before the close, the newest full check_run whose tree matches; refuse when any result exited non-zero; Why not caught; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_finish_proved.FinishAfterARedGate` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: FinishAfterARedGate 1s) / FAILED (1 classes: test_finish_proved.FinishAfterARedGate) [ran] [tree f90cf7a40bfa] [world 2f1906870a] (2026-11-02T02:45:56Z)
- (step 1) `python3 plugin/tests/run.py test_finish_proved.FinishAfterARedGate` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: FinishAfterARedGate 1s) / OK [ran] [tree 1cc04b287a70] [world 2f1906870a] (2026-11-02T02:47:29Z)
- (step 2) `python3 plugin/tests/run.py test_finish_proved test_cli` → exit 0 · Ran 148 tests in 32.1s (46 classes, 16 at a time; slowest: TaskLifecycle 32s, CaptureAndIntake 16s, StateViews 16s) / OK [ran] [tree 1cc04b287a70] [world 2f1906870a] (2026-11-02T02:48:02Z)
- `python3 plugin/tests/run.py test_finish_proved.FinishAfterARedGate` → ✗ exit 1 · Ran 1 tests in 2.9s (1 classes, 16 at a time; slowest: FinishAfterARedGate 1s) / FAILED (1 classes: test_finish_proved.FinishAfterARedGate) (start tree + this task's tests) [ran] [tree 1cc04b287a70] [world 2f1906870a] (2026-11-02T02:48:08Z)
- `python3 plugin/tests/run.py test_finish_proved.FinishAfterARedGate` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: FinishAfterARedGate 1s) / OK [ran] [tree 1cc04b287a70] [world 2f1906870a] (2026-11-02T02:48:08Z)
- (ac 1) `python3 plugin/tests/run.py test_finish_proved test_cli` → exit 0 · Ran 148 tests in 20.2s (46 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 8s, CaptureAndIntake 8s) / OK [ran] [tree 9cd9fdfb9525] [world 2f1906870a] (2026-11-02T02:56:24Z)
- (audit edge) `self-review: _red_full_check walks the ledger tail newest first for check_run events on the current tree (c.worktree_id) that skipped no tests, and refuses the close when the first such run has a failing result, naming its command and up to five failing tests; a newer passing run or an edited tree (a different id) lets the close go to its own runs; it raises before anything runs or commits` → a red full run then a green one on the same tree closes; an affected-only run (skip_tests) never blocks; no full run on the tree closes as before; malformed ledger rows are skipped [tree 9cd9fdfb9525] (2026-11-02T02:56:24Z)
- (audit self) `self-review: _red_full_check walks the ledger tail newest first for check_run events on the current tree (c.worktree_id) that skipped no tests, and refuses the close when the first such run has a failing result, naming its command and up to five failing tests; a newer passing run or an edited tree (a different id) lets the close go to its own runs; it raises before anything runs or commits` → no findings [tree 9cd9fdfb9525] (2026-11-02T02:56:24Z)
## Log
- 2026-11-02T02:38:13Z created
- 2026-11-02T02:38:34Z planned from capture
- 2026-11-02T02:45:23Z focused
- 2026-11-02T02:45:24Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T02:47:26Z criterion 1 verify: `python3 plugin/tests/run.py test_finish test_cli` → `python3 plugin/tests/run.py test_finish_proved test_cli`
- 2026-11-02T02:48:08Z scope: the test lives in test_finish_proved (test_finish doesn't exist); CHANGELOG.md entry
- 2026-11-02T02:57:00Z done
- 2026-11-02T02:57:03Z committed a044df9b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-1906 [FIX S, done, 3 steps] Fm task finish checks a FIX's red-to-green proof before running its checks — lesson: A refusal known before the checks run must be said bef…
- T-1907 [FIX S, done, 3 steps] Fm task finish asks for the adversary lens before its checks run — lesson: A refusal done makes late should run where finish gathers its ga…
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Why not caught
fm task finish runs each criterion's check and fm check --affected (T-1117), never the full suite, and it didn't read the full gate's own record on the tree; this session's T-2334 closed right after its gate failed test_proof.
## Lessons
- A close must read the strongest verdict already on record for its exact tree, not only rerun the narrow checks
## Plan gaps
- failed first: step 1 red test: log a failing full check_run for the current tree (as fm check does), fm task finish refu…
## Files touched
- plugin/tests/test_finish_proved.py
- plugin/lib/fmcli.py
- CHANGELOG.md
