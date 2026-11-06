---
id: T-1552
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, .github/workflows, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:52Z
updated: 2026-10-22T20:59:38Z
---
# Round 3 (T-1520): Reliability tooling: one machine-wide gate lock for release checks and t
## Raw request
> Round 3 (T-1520): Reliability tooling: one machine-wide gate lock for release checks and the canary, fm fsck for ledger, worktrees, locks and journals, stdlib-removal scans with the suite on the oldest and newest Python, an auto-bisect of a red canary, backtesting a cap or timeout on run history, a prediction ledger with a calibration curve, a weekly scaffold bit-rot canary, gates promoted from advisory to blocking by measured false-positive rate, and fm drill compound fault days (a065 a071 a072 a073 b057 b091 c086 c088 c091). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Reliability tooling: one machine-wide gate lock for release checks and the canary, fm fsck for ledger, worktrees, locks and journals, stdlib-removal scans with the suite on the oldest and newest Python, an auto-bisect of a red canary, backtesting a cap or timeout on run history, a prediction ledger with a calibration curve, a weekly scaffold bit-rot canary, gates promoted from advisory to blocking by measured false-positive rate, and fm drill compound fault days (a065 a071 a072 a073 b057 b091 c086 c088 c091). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm fsck reports a planted broken worktree, stale lock and torn journal; two gate runs on one machine queue on the lock; fm drill runs in a temp home — verify with `cd plugin/tests && python3 -m unittest test_reliability_tools`
## Non-goals
## Approach (options → choice → why)
Options: ad hoc scripts; chosen: one machine-wide gate lock (release checks and the canary queue), fm fsck for the ledger, worktrees, locks and journals (read-only report, --fix for safe repairs), stdlib-removal scans plus the suite on the oldest and newest Python in CI, an auto-bisect of a red canary across releases, backtesting a cap or timeout on run history, a prediction ledger with a calibration curve, a weekly scaffold bit-rot canary, gates promoted from advisory to blocking by measured false-positive rate, and fm drill compound fault days in a temp home.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] gate lock and fsck
3. [ ] python matrix, canary bisect, backtest, calibration
4. [ ] bit-rot canary, gate promotion, drill
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:52Z created
- 2026-10-22T18:06:30Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmdoctor.py', '.github/workflows', 'plugin/tests/test_reliability_tools.py', 'CHANGELOG.md']
- 2026-10-22T20:59:38Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1552
## Follow-ups captured
