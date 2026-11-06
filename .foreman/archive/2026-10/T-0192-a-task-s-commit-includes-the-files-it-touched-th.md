---
id: T-0192
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py,plugin/tests/test_paused.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T19:32:10Z
updated: 2026-10-03T19:34:08Z
base: ce878a4a2ef06e779bb2f110a9b813dc10c6cde5
base_tree: 5b79702587ad11c07e5ff9950d8739f8dad36bd9
verified: strong
---
# A task's commit includes the files it touched that still differ from HEAD, even when its focus snapshot already held them
## Raw request
> A task's commit includes the files it touched that still differ from HEAD, even when its focus snapshot already held them
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a file written in the command that focused the task goes into its commit — verify with `python3 plugin/tests/run.py -k test_a_file_written_as_the_task_started_is_committed`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] commit the touched files that differ from HEAD
3. [x] gates
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_file_written_as_the_task_started_is_committed` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PausedTask 0s) / FAILED (1 classes) [ran] [tree 6a7a8ef7e994] (2026-10-03T19:32:15Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_file_written_as_the_task_started_is_committed` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PausedTask 0s) / FAILED (1 classes) [ran] [tree 0bfe521c2661] (2026-10-03T19:32:23Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_file_written_as_the_task_started_is_committed` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PausedTask 0s) / OK [ran] [tree f9db6b698480] (2026-10-03T19:32:28Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    34.1     150  [0] / SessionEnd                  28.7    30.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 0a6931829a64] (2026-10-03T19:33:15Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.3    31.8     150  [0] / SessionEnd                  27.8    30.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree f1e8d2f2f2d0] (2026-10-03T19:34:08Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_file_written_as_the_task_started_is_committed` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PausedTask 0s) / OK [ran] [tree f1e8d2f2f2d0] (2026-10-03T19:34:08Z)
- (audit self) `self-review: only touched files git still reports as changed are added (an unrelated uncommitted file stays out, the test's b.txt); untracked files listed singly (-uall) so a new directory isn't swept in; git failing falls back to the old list` → no findings [tree f1e8d2f2f2d0] (2026-10-03T19:34:08Z)
## Log
- 2026-10-03T19:32:10Z created
- 2026-10-03T19:32:10Z focused
- 2026-10-03T19:34:08Z done
- 2026-10-03T19:34:08Z committed bfcfce8 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower.
- similar past tasks were M: consider --tier M
## Lessons
- When one shell command both edits and focuses, the start snapshot swallows the edit: trust the hooks' touch record over the snapshot for what the task wrote.
## Files touched
- plugin/tests/test_paused.py
- plugin/lib/fmcli.py
- CHANGELOG.md
