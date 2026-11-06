---
id: T-1413
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T17:38:48Z
updated: 2026-10-21T19:34:09Z
base: 2dcc5d9348a9f57872693ac22e55c6afd4bf671e
base_tree: 7500510a884f8a875e7b0e0a81c52322b03cd714
plan0_at: 2026-10-21T19:30:39Z
plan0_scope: []
verified: strong
---
# fm vetoes rm is the user's to run, like fm rule rm
## Raw request
> fm vetoes rm lets Claude lift a veto the user recorded: the guard holds fm rule rm as the user's to run (fmguard.py ~28) but not fm vetoes rm; give it the same treatment (noticed by T-1410's builder)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard refuses Claude's fm vetoes rm N with the reason and the command for the user, as it does fm rule rm — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing guard test, then add vetoes rm beside rule rm in fmguard's user-only verbs
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 197 tests in 19.2s (61 classes, 16 at a time; slowest: GuardAgainstBash 18s, GuardCases 9s, Hook 6s) / FAILED (1 classes) [ran] [tree 97a7f02b34f2] (2026-10-21T19:31:07Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_vetoes test_user_rules` → exit 0 · Ran 210 tests in 18.3s (63 classes, 16 at a time; slowest: GuardAgainstBash 17s, UserRules 16s, GuardCases 8s) / OK [ran] [tree b046d612894b] (2026-10-21T19:31:32Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 197 tests in 16.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 16s, GuardCases 7s, Hook 5s) / OK [ran] [tree b8d61ef77572] (2026-10-21T19:32:05Z)
- (audit intent) `self: one entry in USER_ONLY_FM beside rule rm, reusing its matcher (flags before rm like --json are handled as for rule); tests pin both blocked forms and the read forms allowed` → Claude's fm vetoes rm N is refused with the reason and the command for the user (test_guard) [tree b8d61ef77572] (2026-10-21T19:32:05Z)
- (audit adversary) `self: one entry in USER_ONLY_FM beside rule rm, reusing its matcher (flags before rm like --json are handled as for rule); tests pin both blocked forms and the read forms allowed` → same matcher as fm rule rm, so 'fm vetoes --json rm 2' and '-p x' forms are caught; a worker of fm code is also refused by T-1388's read-only allowlist [tree b8d61ef77572] (2026-10-21T19:32:05Z)
- (audit self) `self: one entry in USER_ONLY_FM beside rule rm, reusing its matcher (flags before rm like --json are handled as for rule); tests pin both blocked forms and the read forms allowed` → no findings [tree b8d61ef77572] (2026-10-21T19:32:05Z)
## Log
- 2026-10-21T17:38:48Z created
- 2026-10-21T18:32:59Z planned from capture
- 2026-10-21T18:33:12Z criterion 1 verify: `python3 plugin/tests/run.py test_guard_rules` → `python3 plugin/tests/run.py test_guard`
- 2026-10-21T18:33:36Z grounded: fmguard.USER_ONLY_FM (line ~21) holds rule rm as the user's; add 'vetoes': ('rm', …, 'fm vetoes rm N'); test row in test_guard.UntestedRuleSites plus 'fm vetoes' and 'fm vetoes --json' in test_near_misses_stay_allowed
- 2026-10-21T19:30:39Z focused
- 2026-10-21T19:34:06Z done
- 2026-10-21T19:34:09Z committed 385a7abb (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1410 [FEATURE S, done, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it — lesson: A record the user can create should…
- T-1063 [FEATURE M, done, 2 steps] Steers compile to checkers: a steer or interrupt is typed (scope, style, safety, wrong app — lesson: Never let the agent create a restr…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 2–7 steps
## Regression test
test_guard.UntestedRuleSites: 'fm vetoes rm 2' and 'fm vetoes --json rm 2' blocked as self-authorize (red before, step 1 evidence exit 1); 'fm vetoes' and 'fm vetoes --json' stay allowed
## Why not caught
T-1410 added the retract hint without checking the guard's user-only table; its builder noticed
## Lessons
- When a new user-only record gets a remove verb, add it to the guard's USER_ONLY_FM table in the same task
## Plan gaps
- failed first: step 1 failing guard test, then add vetoes rm beside rule rm in fmguard's user-only verbs
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
