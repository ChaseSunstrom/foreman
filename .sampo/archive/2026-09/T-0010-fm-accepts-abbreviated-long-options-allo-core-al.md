---
id: T-0010
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-09-26T12:24:05Z
updated: 2026-09-26T12:25:50Z
---
# Reject abbreviated fm options so --allow can't be spelled past the guard
## Raw request
> fm accepts abbreviated long options (--allo core, --al=core), which bypasses the guard's self-authorize check and lets an agent grant itself core
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm rejects abbreviated long options (exit 2, allow unchanged) — verify with `python3 -m unittest test_cli.TaskLifecycle.test_abbreviated_options_are_rejected`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first: abbreviated --allo/--al=/--all and --sour exit 2 (RED seen: 0 != 2)
2. [x] _Parser with allow_abbrev=False for fm and all subparsers; full suite green
## Resume here
## Verification evidence
- (step 1) `python3 -m unittest test_cli.TaskLifecycle.test_abbreviated_options_are_rejected (before fix)` → FAIL: AssertionError: 0 != 2 : ['--allo', 'core'] (2026-09-26T12:25:50Z)
- (step 2) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests` → Ran 180 tests OK (new test passes) (2026-09-26T12:25:50Z)
- (ac 1) `unittest test_abbreviated_options_are_rejected` → OK: --allo core, --al=core, --all core, --sour exit 2; allow stays [] (2026-09-26T12:25:50Z)
## Log
- 2026-09-26T12:24:05Z created
- 2026-09-26T12:24:10Z planned from capture
- 2026-09-26T12:25:45Z focused
- 2026-09-26T12:25:45Z process: fmcli.py edited before fm focus T-0010 (brief existed, focus skipped); recorded here
- 2026-09-26T12:25:50Z done
## Follow-ups captured
