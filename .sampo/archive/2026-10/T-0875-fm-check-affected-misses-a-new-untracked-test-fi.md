---
id: T-0875
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T14:17:12Z
updated: 2026-10-15T14:57:28Z
group: fm check and evidence correctness
base: f5e3ba5668fefeacd5c563fded4d8e994ef2d053
base_tree: ffcdffee83215b92dfb65758d77557697fa581d1
verified: strong
---
# fm check --affected runs a test file the task added or changed, even one the map hasn't linked
## Raw request
> fm check --affected misses a new, untracked test file for a new module (T-0870's test_demo.py wasn't linked to fmdemo.py)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a new untracked test file beside a new module runs under --affected — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_cli, then affected() counts every changed test file
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_lanes test_ambient` → exit 0 · Ran 102 tests in 17.5s (27 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 7s, Lanes 7s) / OK [ran] [tree d92a57383cf6] (2026-10-15T14:54:42Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 87 tests in 17.1s (24 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 6s, Checks 4s) / OK [ran] [tree d92a57383cf6] (2026-10-15T14:56:39Z)
- (audit edge) `self review: affected() now adds every changed file whose basename is test-named, so a new untracked test beside a new module runs; helpers under tests/ stay out` → a changed helper under tests/ (helpers.py, conftest.py) isn't run alone, since pytest exits 5 on an empty collection; JS tests under __tests__/ without a test-ish name still need a map link (known ceiling) [tree d92a57383cf6] (2026-10-15T14:56:39Z)
- (audit self) `self review: affected() now adds every changed file whose basename is test-named, so a new untracked test beside a new module runs; helpers under tests/ stay out` → no findings [tree d92a57383cf6] (2026-10-15T14:56:39Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 87 tests in 17.5s (24 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 6s, Checks 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d92a57383cf6] (2026-10-15T14:57:20Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 87 tests in 17.4s (24 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 6s, Checks 4s) / OK [ran] [tree d92a57383cf6] (2026-10-15T14:57:20Z)
- (audit edge) `self review: affected() now adds every changed file whose basename is test-named, so a new untracked test beside a new module runs; helpers under tests/ stay out` → a changed helper under tests/ (helpers.py, conftest.py) isn't run alone, since pytest exits 5 on an empty collection; JS tests under __tests__/ without a test-ish name still need a map link (known ceiling) [tree d92a57383cf6] (2026-10-15T14:57:20Z)
- (audit self) `self review: affected() now adds every changed file whose basename is test-named, so a new untracked test beside a new module runs; helpers under tests/ stay out` → no findings [tree d92a57383cf6] (2026-10-15T14:57:20Z)
## Log
- 2026-10-15T14:17:12Z created
- 2026-10-15T14:53:03Z planned from capture
- 2026-10-15T14:53:03Z focused
- 2026-10-15T14:57:20Z done
- 2026-10-15T14:57:21Z committed 6eed14f (2 files)
- 2026-10-15T14:57:28Z includes T-0879: Catch it earlier: the test only covered tracked, already-linked tests; the map is built fr
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- T-0214 [FEATURE M, deferred, 0 steps] Edit-time test sentinel — after Claude edits files, the tests linked to them (fm map test
- playbook Living Docs Governance (skills/playbooks/references/context/living-docs.md)
- decision 2026-10-09: self-improvement pass 2026-10-09: rejected exempting ssh-wrapped interpreter code from 'driving Foreman's modules' — ssh localhost would bypass the …
- the similar finished task took 2 steps
## Why not caught
the test only covered tracked, already-linked tests; the map is built from git ls-files so untracked files never had links
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
