---
id: T-0302
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T13:17:33Z
updated: 2026-10-04T13:21:42Z
base: b194b51817a7dd1da6afa0fc1c1c8813b0b2ff04
base_tree: 65697cac5cb8b74298773121c690997ebc773421
verified: strong
---
# Fm ask accepts a grant on a closed task, which the guard can never use (grants apply only
## Raw request
> fm ask accepts a grant on a closed task, which the guard can never use (grants apply only to the active task): refuse it or say so
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ask on a closed task is refused by the hook (no dialog) and by fm ask itself; a standing core ask is unaffected — verify with `python3 plugin/tests/run.py -p test_cli.py -k AskClosed`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then refuse closed tasks in the hook's ask dialog and in cmd_ask
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_cli.py -k AskClosed` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: AskClosed 0s) / FAILED (1 classes) [ran] [tree 7d5e0aa033d9] (2026-10-04T13:19:48Z)
- (step 1) `python3 plugin/tests/run.py -p test_cli.py -k AskClosed` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: AskClosed 0s) / OK [ran] [tree ccd2dd3f6a1e] (2026-10-04T13:20:03Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.3     150  [0] / SessionEnd                  28.4    31.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:59 UTC; python3 plugin/tests/run.py → exit 0 · Ran 820 tests in [ran] [tree 885d8d2c5c43] (2026-10-04T13:21:35Z)
- (ac 1) `python3 plugin/tests/run.py -p test_cli.py -k AskClosed` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: AskClosed 0s) / OK [ran] [tree 885d8d2c5c43] (2026-10-04T13:21:42Z)
- (audit intent) `self: red→green on test_cli AskClosed (hook said ask, now deny); cli, hooks, guard and plugin suites pass; fm check exit 0` → the bug hit this session — a plugin yes landed on closed T-0300 and the guard couldn't use it; now the ask is refused before any dialog with how to ask instead [tree 885d8d2c5c43] (2026-10-04T13:21:42Z)
- (audit adversary) `self: red→green on test_cli AskClosed (hook said ask, now deny); cli, hooks, guard and plugin suites pass; fm check exit 0` → the change only adds refusals before a grant; no path grants more than before; standing core (project-wide) is untouched [tree 885d8d2c5c43] (2026-10-04T13:21:42Z)
- (audit edge) `self: red→green on test_cli AskClosed (hook said ask, now deny); cli, hooks, guard and plugin suites pass; fm check exit 0` → unknown id → the hook falls through and fm ask's need_brief refuses as before; dropped and done both count as closed (c.CLOSED) [tree 885d8d2c5c43] (2026-10-04T13:21:42Z)
- (audit self) `self: red→green on test_cli AskClosed (hook said ask, now deny); cli, hooks, guard and plugin suites pass; fm check exit 0` → no findings [tree 885d8d2c5c43] (2026-10-04T13:21:42Z)
## Log
- 2026-10-04T13:17:33Z created
- 2026-10-04T13:19:32Z focused
- 2026-10-04T13:21:42Z done
- 2026-10-04T13:21:42Z committed 2b2de0a (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
- research t0036-edge: Confirmed: no test exercises content_hash returning None at grant time, the unlocked-check-then-locked-consume race, or malformed/non-list `plugin_p…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor. [stale: plugin/uninstall.sh changed since it wa…
## Lessons
- Validate a request against where it will be read: a grant stored on a task the guard never consults is a silent no-op
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
