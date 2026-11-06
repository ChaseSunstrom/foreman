---
id: T-0069
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-09-27T02:03:00Z
updated: 2026-09-27T02:15:08Z
base: bd86fd6a901ddc6ebe53cdade19ca7c92e6bd58f
---
# Merge candidate improve/20260926 (T-0063: smarter + leaner Foreman) into foreman/build and main, push
## Raw request
> Merge candidate improve/20260926 (T-0063: smarter + leaner Foreman) into foreman/build and main, push
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] live foreman/build and main at the candidate head, tests pass live :: python3 -m unittest discover -s plugin/tests -q
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fast-forward foreman/build and main to improve/20260926, run tests, push both
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 433 tests in 106.109s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.8    32.9     150  [0] / SessionEnd                  26.4    31.6     150  [0] [ran] [tree eefc4ef7673e] (2026-09-27T02:15:02Z)
- (ac 1) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed on this tree (run at 02:15 UTC) [ran] [tree eefc4ef7673e] (2026-09-27T02:15:08Z)
- (audit self) `self checklist: fast-forward only (ancestor checked), gates green on the live copy, push plain (no force)` → no findings [tree eefc4ef7673e] (2026-09-27T02:15:08Z)
## Log
- 2026-09-27T02:03:00Z created
- 2026-09-27T02:03:00Z focused
- 2026-09-27T02:12:51Z user approved core in Claude Code's permission prompt
- 2026-09-27T02:15:08Z done
## Follow-ups captured
