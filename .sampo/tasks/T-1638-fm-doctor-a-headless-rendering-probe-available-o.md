---
id: T-1638
type: FEATURE
tier: S
status: dropped
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_shot.py, CHANGELOG.md]
depends_on: [T-1636]
source: user
created: 2026-10-22T20:57:50Z
updated: 2026-10-23T02:01:21Z
lane_branch: worktree-agent-a55e50abe35ec899e
base: 177c6ce8fb07e6dd16986f28b0903437d7e7cabb
base_tree: 27cc290df6b7fbdc366e43324e396e760bd09283
plan0_at: 2026-10-23T01:48:21Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_shot.py, CHANGELOG.md]
---
# fm doctor: a headless-rendering probe (available, or why not)
## Raw request
> fm doctor: a headless-rendering probe (available, or why not)
## Interpretation
fm doctor reports whether headless rendering is available: Playwright and a browser found through fmsmoke's detection, with the version, or the reason it isn't (not installed, browser missing, launch failed). Nothing is installed.
## Assumptions (confidence)
## Acceptance criteria
- [ ] doctor reports headless rendering available or why not — verify with `python3 plugin/tests/run.py test_shot.Doctor`
- [x] doctor reports headless rendering available or why not (tests in test_doctor) — verify with `python3 plugin/tests/run.py test_doctor.Headless`
## Non-goals
## Approach (options → choice → why)
Options: probe by launching a page (slow but certain); check paths only (fast, can lie); skip. Choice: a quick launch with a short timeout, cached for the doctor run.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] probe through fmsmoke.playwright()
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_shot.Doctor` → ✗ exit 1 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: Doctor 0s) / FAILED (1 classes) [ran] [tree b6b296e40347] (2026-10-23T01:49:28Z)
- (ac 1) `python3 plugin/tests/run.py test_shot.Doctor 2>&1 | grep -v "^$" | head -30` → ✗ exit 1 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Doctor 0s) / FAILED (1 classes) [ran] [tree b6b296e40347] (2026-10-23T01:49:52Z)
- (step 2) `python3 plugin/tests/run.py test_shot.Doctor` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: Doctor 0s) / OK [ran] [tree 5f8c662d30de] (2026-10-23T01:50:05Z)
- (step 2) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.9s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 889d571efd08] (2026-10-23T01:53:47Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:00:48Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:00:50Z)
- (ac 1) `python3 plugin/tests/run.py test_shot.Doctor` → ✗ exit 1 · run.py: no test matches test_shot.Doctor [ran] [tree 5946eb90ec00] (2026-10-23T02:01:00Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:01:00Z)
- (step 1) `python3 plugin/tests/run.py test_shot.Doctor` → ✗ exit 1 · run.py: no test matches test_shot.Doctor [ran] [tree 5946eb90ec00] (2026-10-23T02:01:00Z)
- (step 1) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:01:06Z)
- (ac 1) `python3 plugin/tests/run.py test_shot.Doctor` → ✗ exit 1 · run.py: no test matches test_shot.Doctor [ran] [tree 5946eb90ec00] (2026-10-23T02:01:07Z)
## Log
- 2026-10-22T20:57:50Z created
- 2026-10-22T20:57:51Z set scope=['plugin/lib/fmdoctor.py', 'plugin/tests/test_shot.py', 'CHANGELOG.md']
- 2026-10-22T20:57:52Z split from T-1531 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:55Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_shot.Doctor`
- 2026-10-22T21:30:18Z criterion 1 text: doctor reports headless rendering available or why not — verify with python3 plugin/tests/run.py test_shot.Doctor → doctor reports headless rendering available or why not
- 2026-10-22T23:42:27Z set depends_on=['T-1636']
- 2026-10-22T23:42:27Z depends on T-1636: the probe should reuse fmshot.chrome() rather than a third browser finder
- 2026-10-23T01:47:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1638.builder.md
- 2026-10-23T01:48:20Z focused
- 2026-10-23T02:00:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a55e50abe35ec899e (branch worktree-agent-a55e50abe35ec899e kept: not merged)
- 2026-10-23T02:00:36Z merged worktree-agent-a55e50abe35ec899e (3 file(s))
- 2026-10-23T02:00:39Z focused
- 2026-10-23T02:00:51Z criterion 1's verify (test_shot.Doctor) moved to test_doctor.Headless per review; its evidence is that command
- 2026-10-23T02:01:21Z dropped: criterion 1's check named test_shot.Doctor; the tests moved to test_doctor.Headless per review and an evidenced check can't be repointed; redone with the right check
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1531 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames,
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmdoctor.py, plugin/tests/test_shot.py; re-ground the plan against them before editing
