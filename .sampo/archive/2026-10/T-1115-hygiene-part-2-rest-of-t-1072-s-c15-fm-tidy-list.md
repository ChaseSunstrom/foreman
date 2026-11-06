---
id: T-1115
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py]
depends_on: []
source: followup
created: 2026-10-16T05:40:18Z
updated: 2026-10-16T05:43:48Z
base: e11b9e8cef1c5d49fd0211a913eceb01447c0981
base_tree: ff493ab8c27a4f8d57415adbe77ee7beb8314a69
verified: strong
---
# Hygiene part 2 (rest of T-1072's C15): fm tidy lists hints the model keeps ignoring (hints
## Raw request
> Hygiene part 2 (rest of T-1072's C15): fm tidy lists hints the model keeps ignoring (hints_quiet) and rules that never fired in 60 days, as candidates to retire
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm tidy lists a user rule that matched no call in 60 days (never one that did) and the hints the model keeps ignoring, as info, removing nothing — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test
2. [x] Record each rule hit's time; list quiet rules and ignored hints in _hygiene
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 21 tests in 3.0s (9 classes, 16 at a time; slowest: StalePlans 3s, Apply 2s, TidyHygiene 2s) / FAILED (1 classes) [ran] [tree 6f5d71fef1ec] (2026-10-16T05:42:46Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_rules test_hooks` → exit 0 · Ran 178 tests in 37.0s (30 classes, 16 at a time; slowest: Stop 37s, PreToolUse 19s, SessionStart 15s) / OK [ran] [tree 8585c15ff4a9] (2026-10-16T05:43:38Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 21 tests in 2.6s (9 classes, 16 at a time; slowest: StalePlans 3s, Apply 2s, TidyHygiene 2s) / OK [ran] [tree 7e8b252faa04] (2026-10-16T05:43:47Z)
- (step 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 21 tests in 2.6s (9 classes, 16 at a time; slowest: StalePlans 3s, Apply 2s, TidyHygiene 2s) / OK [ran] [tree 7e8b252faa04] (2026-10-16T05:43:47Z)
- (audit self) `self: driven through the real PreToolUse hook for the hit; a dry and an --apply tidy both leave the rules in place` → no findings [tree 7e8b252faa04] (2026-10-16T05:43:47Z)
## Log
- 2026-10-16T05:40:18Z created
- 2026-10-16T05:42:31Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmtidy.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T05:42:34Z focused
- 2026-10-16T05:43:44Z scope: CHANGELOG.md — release note
- 2026-10-16T05:43:48Z done
- 2026-10-16T05:43:48Z committed 03a248c (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- research wave1-plan-ac858e27ec64c546f: === T-1077 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- T-1099 [FIX S, done, 3 steps] Ledger roll takes the ledger lock and keeps time order: _roll_ledger keeps unparseable-ts — lesson: Rewriting a file other processes append…
- decision 2026-10-04: [revisit: after 2026-10-04] hints go quiet after QUIET_AFTER=6 ignored showings
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_tidy.py
## Lessons
- To retire something by disuse, record its use first; a list of unused things needs a hit log, not a guess
## Plan gaps
- failed first: step 1 Failing test
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
