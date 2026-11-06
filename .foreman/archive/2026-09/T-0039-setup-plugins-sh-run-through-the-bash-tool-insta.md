---
id: T-0039
type: SECURITY
tier: S
status: done
priority: normal
scope: [setup-plugins.sh, plugin/tests/test_setup.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-09-26T21:42:04Z
updated: 2026-09-26T21:49:14Z
base: 876f59977ce8e2659609d989201226f890c4fa58
---
# setup-plugins.sh refuses a real run inside a Claude Code session (CLAUDECODE=1): install one plugin with fm ask --pin + fm plugins install instead; --dry-run still works
## Raw request
> setup-plugins.sh run through the Bash tool installs plugins without the guard seeing claude plugin install (script body): have it refuse under CLAUDE_CODE / Foreman sessions or route through fm plugins install (pin)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with CLAUDECODE=1 setup-plugins.sh without --dry-run exits nonzero naming fm plugins install and changes nothing; with --dry-run it runs; outside a session it is unchanged
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_setup, then the check in setup-plugins.sh, docs
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 411 tests in 93.968s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.7    31.8     150  [0] / SessionEnd                  26.2    30.9     150  [0] [ran] [tree df8472520c8c] (2026-09-26T21:49:13Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_setup.SetupPluginsInSession` → exit 0 · Ran 2 tests in 0.066s / OK [ran] [tree df8472520c8c] (2026-09-26T21:49:13Z)
- (audit self) `self checklist: diff re-read; callers of setup-plugins.sh (install.sh passes flags through, fm doctor uses --dry-run, test stubs); CLAUDECODE is what Claude Code sets in its shells (checked: CLAUDECODE=1 here); speed bump like the guard (an agent could unset it), documented` → no findings; 411 tests OK [tree df8472520c8c] (2026-09-26T21:49:14Z)
## Log
- 2026-09-26T21:42:04Z created
- 2026-09-26T21:46:50Z planned from capture
- 2026-09-26T21:46:50Z focused
- 2026-09-26T21:49:14Z done
## Follow-ups captured
