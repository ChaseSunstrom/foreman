---
id: T-1287
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T20:56:41Z
updated: 2026-10-20T21:24:06Z
base: 4cebb1ff639b4ee9197d2a79a58ea4ad9a17776e
base_tree: 1e5c3b79a6adbd052ea3ec0b1a54179d0ec58b18
plan0_at: 2026-10-20T21:13:15Z
plan0_scope: []
verified: strong
---
# Plugin/tests/run.py exits 0 when one of several named test modules doesn't exist (run.py t
## Raw request
> plugin/tests/run.py exits 0 when one of several named test modules doesn't exist (run.py test_secrets test_nosuch → OK), so a criterion naming a wrong test file passes silently (T-1283 and T-1244 named test_site, which doesn't exist); an unknown module name should fail the run
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a test module name given to run.py that matches no test fails the run with one line naming it, even when other names match (run.py test_secrets test_nosuch exits 1 and says test_nosuch) — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_run.py, then the check in run.py's main after the classes are found
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_run.Args -k test_run.UnknownNames` → ✗ exit 1 · Ran 3 tests in 303.6s (2 classes, 16 at a time; slowest: UnknownNames 303s, Args 0s) / FAILED (1 classes) [ran] [tree eec477d5646d] (2026-10-20T21:18:26Z)
- `python3 plugin/tests/run.py test_run.Args test_run.UnknownNames` → exit 0 · Ran 3 tests in 1.1s (2 classes, 16 at a time; slowest: UnknownNames 0s, Args 0s) / OK (start tree + this task's tests) [ran] [tree 4c82fe09cb7d] (2026-10-20T21:19:43Z)
- `python3 plugin/tests/run.py test_run.Args test_run.UnknownNames` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: UnknownNames 0s, Args 0s) / OK [ran] [tree 4c82fe09cb7d] (2026-10-20T21:19:43Z)
- (step 1) `python3 plugin/tests/run.py -k test_run.Args -k test_run.UnknownNames` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: UnknownNames 0s, Args 0s) / OK [ran] [tree 4c82fe09cb7d] (2026-10-20T21:19:49Z)
- (ac 1) `python3 plugin/tests/run.py test_run.Args test_run.UnknownNames` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: UnknownNames 0s, Args 0s) / OK [ran] [tree 4c82fe09cb7d] (2026-10-20T21:19:50Z)
- (ac 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 23 tests in 2.6s (20 classes, 16 at a time; slowest: Bench 3s, TimeoutWithoutProc 2s, Timeout 2s) / OK [ran] [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
- (audit intent) `self review: run.py records which names matched a test id during discovery and fails, naming them, when one matched none; red run (old runner passed the unknown name), then green; full gates green` → run.py test_secrets test_nosuch fails and names test_nosuch [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
- (audit adversary) `self review: run.py records which names matched a test id during discovery and fails, naming them, when one matched none; red run (old runner passed the unknown name), then green; full gates green` → test tooling only [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
- (audit edge) `self review: run.py records which names matched a test id during discovery and fails, naming them, when one matched none; red run (old runner passed the unknown name), then green; full gates green` → -k filters are unchanged (only positional names must match); a name matching a test method id counts [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
- (audit operator) `self review: run.py records which names matched a test id during discovery and fails, naming them, when one matched none; red run (old runner passed the unknown name), then green; full gates green` → fm check --affected hands names of existing test files, so it still passes (full gates green) [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
- (audit maintainer) `self review: run.py records which names matched a test id during discovery and fails, naming them, when one matched none; red run (old runner passed the unknown name), then green; full gates green` → classes() takes an optional hit set; one check in main [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
- (audit self) `self review: run.py records which names matched a test id during discovery and fails, naming them, when one matched none; red run (old runner passed the unknown name), then green; full gates green` → no findings [tree 472c8ae00a0e] (2026-10-20T21:23:16Z)
## Log
- 2026-10-20T20:56:41Z created
- 2026-10-20T21:13:14Z focused
- 2026-10-20T21:24:05Z done
- 2026-10-20T21:24:06Z committed ad1aa2c8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- T-1145 [FEATURE S, done, 2 steps] Check a verify command when it is added (fm task ac add/edit, --ac ':: cmd'): a python tes
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 2–2 steps
## Lessons
- A runner that treats names as filters must fail on a filter that matched nothing, or a typo'd test name in a criterion passes forever
## Plan gaps
- failed first: step 1 Failing test in test_run.py, then the check in run.py's main after the classes are found
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- CHANGELOG.md
