---
id: T-1757
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T06:21:32Z
updated: 2026-10-23T08:11:26Z
base: 025c5d2aa1d85360f8ce07fefafe1d2b4485eb8b
base_tree: 205721ad24ab4efbeb953d75ba3ed3efaaccc339
plan0_at: 2026-10-23T08:04:30Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
verified: strong
---
# fm code warns once at start when fm doctor sees two Foreman installs or Foreman's hook registered twice
## Raw request
> fm code warns once at start when fm doctor sees two Foreman installs or Foreman's hook registered twice (rest of T-1355; the doctor's hook state writers check already finds a duplicate)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code's start notes fm doctor's two-installs or duplicate-hook finding once per distinct finding (state/code-warned.json keeps what was said), and says nothing when both pass — verify with `python3 plugin/tests/run.py test_code.Failures`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then install_warning() in fmcode, noted after the start event
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.Failures` → exit 0 · Ran 4 tests in 5.0s (1 classes, 16 at a time; slowest: Failures 5s) / OK [ran] [tree 9649a75c950e] (2026-10-23T08:09:50Z)
- (audit intent) `self` → pass: a doctor finding is noted once per distinct finding; a check that trips never stops a run [tree 7d8aee519849] (2026-10-23T08:09:51Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Failures` → exit 0 · Ran 4 tests in 4.9s (1 classes, 16 at a time; slowest: Failures 5s) / OK [ran] [tree 7d8aee519849] (2026-10-23T08:09:56Z)
- (audit intent) `self: intent, edge` → the remaining part of T-1355 done [tree 7d8aee519849] (2026-10-23T08:09:56Z)
- (audit edge) `self: intent, edge` → a check raising returns nothing; an unreadable remembered file starts fresh; a new finding is said even after an old one [tree 7d8aee519849] (2026-10-23T08:09:56Z)
- (audit self) `self: intent, edge` → no findings [tree 7d8aee519849] (2026-10-23T08:09:56Z)
## Log
- 2026-10-23T06:21:32Z created
- 2026-10-23T08:04:00Z planned from capture
- 2026-10-23T08:04:01Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-10-23T08:04:29Z focused
- 2026-10-23T08:11:24Z done
- 2026-10-23T08:11:26Z committed 88adf015 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1754 [FEATURE M, done, 3 steps] fm code: a Next: line on every failure, the start event names the Foreman running it, and a registry that stops runners… — lesson: A re…
- T-1355 [FEATURE S, done, 0 steps] One live Foreman (R3): fm code's start event names the Foreman running it (root, version),
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- similar finished tasks took 0–3 steps
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Lessons
- A warning a run repeats every start gets ignored: say each distinct finding once
## Files touched
- plugin/lib/fmcode.py
- plugin/tests/test_code.py
- CHANGELOG.md
