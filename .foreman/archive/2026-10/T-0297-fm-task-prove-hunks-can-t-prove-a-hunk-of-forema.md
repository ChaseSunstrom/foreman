---
id: T-0297
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T09:14:32Z
updated: 2026-10-04T09:45:02Z
base: 8d047ae1e9e7175a346d5a98bcb1f3db231b3200
base_tree: 3b1cf9c38a5e2000aa9d244b820da11b5ede351a
verified: strong
---
# Fm task prove --hunks can't prove a hunk of Foreman's own hook code whose revert crashes:
## Raw request
> fm task prove --hunks can't prove a hunk of Foreman's own hook code whose revert crashes: the hook's committed-library fallback loads HEAD, which in the proof worktree is the unmutated scratch commit, so the crash is masked — point the fallback at the task's base in proof runs, or report such hunks as untestable
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] in a checkout that ships Foreman's hook with its committed-library fallback, fm task prove --hunks runs every check with HEAD at the task's base (the scratch commit only in the index and files), so a mutation that crashes the hook falls back to pre-change code and shows as a failure; restoring between hunks still returns the scratch tree — verify with `python3 plugin/tests/run.py -p test_hunks.py -k Fallback`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first (test_hunks.py Fallback), then the HEAD swap and the restore in task_prove_hunks
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_hunks.py -k Fallback` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Fallback 0s) / FAILED (1 classes) [ran] [tree 38363e1c4fde] (2026-10-04T09:43:20Z)
- (step 1) `python3 plugin/tests/run.py -p test_hunks.py -k Fallback` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Fallback 0s) / OK [ran] [tree c0e174346a5b] (2026-10-04T09:43:40Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    33.9     150  [0] / SessionEnd                  28.2    32.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 812 tests in [ran] [tree c0e174346a5b] (2026-10-04T09:44:47Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_hunks.py` → exit 0 · 2/2 hunks proven [ran] [tree c0e174346a5b] (2026-10-04T09:44:52Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hunks.py -k Fallback` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Fallback 0s) / OK [ran] [tree 7f5186dd76d8] (2026-10-04T09:45:02Z)
- (audit edge) `self: red→green on a test that logs HEAD's tree during every check (baseline and each hunk) and requires the task's base; restore switched from reset --hard (which now would reset to the base) to read-tree -u --reset of the scratch commit, covered by the 2/2 proven result; the swap is limited to checkouts shipping Foreman's hook so other projects' checks see git as before; dogfooded: proving this task ran with the swap live, 2/2` → base stored as a tree or a commit (commit-tree of base^{tree}); deleted and new files still restored by read-tree + clean [tree 7f5186dd76d8] (2026-10-04T09:45:02Z)
- (audit self) `self: red→green on a test that logs HEAD's tree during every check (baseline and each hunk) and requires the task's base; restore switched from reset --hard (which now would reset to the base) to read-tree -u --reset of the scratch commit, covered by the 2/2 proven result; the swap is limited to checkouts shipping Foreman's hook so other projects' checks see git as before; dogfooded: proving this task ran with the swap live, 2/2` → no findings [tree 7f5186dd76d8] (2026-10-04T09:45:02Z)
## Log
- 2026-10-04T09:14:32Z created
- 2026-10-04T09:43:11Z focused
- 2026-10-04T09:45:02Z done
- 2026-10-04T09:45:02Z committed d32c074 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- T-0271 [FEATURE M, done, 3 steps] Hunk mutation proof: fm task prove --hunks — lesson: A proof tool must first show its check passes on the unmodified input; otherwise e…
- research brainstorm-pass-2: Source: research/brainstorm-20261004-020314 (4 lenses × 2 rounds, past pass 1 and three earlier lists; 82 new titles). Pack: pass 1's results…
- T-0037 [FIX M, done, 0 steps] Self-lockout #2: a bug in fmcore (record decorator on Python 3.14) made the hook unable to
- similar past tasks were M: consider --tier M
## Regression test
plugin/tests/test_hunks.py Fallback
## Lessons
- A fallback that loads 'the committed code' makes mutation tests lie unless 'committed' means the code before the change
## Files touched
- plugin/tests/test_hunks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
