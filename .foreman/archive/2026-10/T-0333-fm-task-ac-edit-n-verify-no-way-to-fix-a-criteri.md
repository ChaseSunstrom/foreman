---
id: T-0333
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T02:25:26Z
updated: 2026-10-06T02:44:14Z
base: 60e6947febb8da29f4d8263b8002d67e613d265b
base_tree: f63fad9bf8e58afe81cb6c96f826844bab13fd34
verified: strong
---
# fm task ac ID edit N: set a criterion's text or verify command
## Raw request
> fm task ac edit N --verify: no way to fix a criterion's verify command; warn when a verify starts with typed:
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task ac ID edit N --verify CMD replaces only the verify tail, keeps the criterion's text, and a typed: verify warns it won't run — verify with `python3 plugin/tests/run.py -k test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] edit action
3. [x] docs
## Resume here
## Docs impact
MASTER.md (fm task ac edit), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cli.EditCriterion` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: EditCriterion 0s) / FAILED (1 classes) [ran] [tree 73e478e8a9c7] (2026-10-06T02:42:32Z)
- (step 2) `python3 plugin/tests/run.py -k test_cli.EditCriterion` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: EditCriterion 0s) / OK [ran] [tree 3c757d394eee] (2026-10-06T02:42:53Z)
- (step 3) `python3 plugin/tests/run.py -k test_doctor` → exit 0 · Ran 23 tests in 5.9s (7 classes, 16 at a time; slowest: Command 6s, RestoreState 0s, Briefs 0s) / OK [ran] [tree 3c757d394eee] (2026-10-06T02:42:59Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 73 tests in 14.4s (18 classes, 16 at a time; slowest: TaskLifecycle 14s, StateViews 5s, Checks 3s) / OK [ran] [tree 3c757d394eee] (2026-10-06T02:44:14Z)
- (audit self) `self-review of the diff: edit_ac rewrites only criterion N (checkbox kept), --verify "" drops the tail, unknown N and no-op edit are usage errors; typed: verify warns; full suite + fm check green` → no findings [tree 3c757d394eee] (2026-10-06T02:44:14Z)
## Log
- 2026-10-06T02:25:26Z created
- 2026-10-06T02:42:07Z planned from capture
- 2026-10-06T02:42:08Z focused
- 2026-10-06T02:44:14Z done
- 2026-10-06T02:44:14Z committed c8ba8de (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261006: 1. **Answer.** Four of the five friction points trace to small, local causes. The guard leaves a variable unknown when its value starts with `~`. …
- research T-0261-review-1: No bypass found. [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py changed since it was written]
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- research T-0120-review: Verdict [stale: mods/foreman-ui/hooks/register.tsx, plugin/lib/fmguard.py changed since it was written]
## Lessons
- A planning gate that requires a field needs a command to set that field after creation, or the gate turns a typo into a dead end.
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
