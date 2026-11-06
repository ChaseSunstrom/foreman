---
id: T-3095
type: CLEAN
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/lib/sampo/core.py, plugin/lib/fm*.py, plugin/tests/test_doctor.py]
depends_on: []
source: discovered
created: 2026-11-05T02:06:49Z
updated: 2026-11-06T03:52:48Z
---
# The fm*.py alias modules say they stay for two releases (T-2742) but nothing records the…
## Raw request
> The fm*.py alias modules say they stay for two releases (T-2742) but nothing records the release they can go; record the removal release and have doctor flag them after it
## Interpretation
Reading 1 (taken): the 132 fm*.py alias modules (old import paths after the Sampo rename, T-2742) say 'kept for two releases' with no release named; record the removal version once (two minor versions past the rename's 1.2.x: 1.4.0), have each alias's docstring name it, and have sampo doctor warn once the plugin's version reaches it. Reading 2 (ruled out): remove the aliases now: 'nothing a user already has may break'; third-party imports may still use them.
## Assumptions (confidence)
## Acceptance criteria
- [ ] The removal version is recorded once (core.ALIAS_UNTIL = 1.4.0) and every fm*.py alias's docstring names it — verify with `python3 plugin/tests/run.py test_doctor`
- [ ] sampo doctor warns, naming the aliases and the version, once the plugin's version reaches ALIAS_UNTIL; below it, no warning — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
1) use what exists: one constant in core (ALIAS_UNTIL) read by doctor's existing checks, the aliases' docstrings rewritten mechanically: likely outcome: a small diff plus a docstring sweep. 2) a date instead of a version: fails if: releases slip and the date passes with users still on old versions. 3) do less: a note in MASTER.md: fails if: nothing reminds anyone. Choice 1 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] constant, docstrings, doctor warning (test first)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T02:06:49Z created
- 2026-11-05T02:08:39Z set scope=['plugin/lib/sampo/doctor.py', 'plugin/lib/sampo/core.py', 'plugin/lib/fm*.py', 'plugin/tests/test_doctor.py']
- 2026-11-05T02:08:40Z planned: it has criteria and steps
- 2026-11-05T02:08:41Z set approved=True
- 2026-11-05T02:08:41Z blocked: planned; waits for a builder slot
- 2026-11-06T03:52:48Z unblocked
## Follow-ups captured
