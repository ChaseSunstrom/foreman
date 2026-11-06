---
id: T-3369
type: CLEAN
tier: S
status: planned
priority: normal
scope: [install.sh, INSTALL.md, MASTER.md, README.md, site/stats.py, plugin/tests/test_install.py]
depends_on: []
source: followup
created: 2026-11-06T06:03:46Z
updated: 2026-11-06T06:03:47Z
---
# Install and docs read SAMPO_* first: install.sh reads only FOREMAN_* (install.sh:19-26) while the code already reads SAMPO_* (core.py:68); docs name FOREMAN_HOME x40, REPO x8, DESKTOP_REPO x6, QUIET x2, NO_BACKGROUND x1 (INSTALL.md, MASTER.md, README.md, install.sh, site/stats.py): say SAMPO_* with FOREMAN_* as the old alias
## Raw request
> Install and docs read SAMPO_* first: install.sh reads only FOREMAN_* (install.sh:19-26) while the code already reads SAMPO_* (core.py:68); docs name FOREMAN_HOME x40, REPO x8, DESKTOP_REPO x6, QUIET x2, NO_BACKGROUND x1 (INSTALL.md, MASTER.md, README.md, install.sh, site/stats.py): say SAMPO_* with FOREMAN_* as the old alias
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] install.sh honours SAMPO_HOME (FOREMAN_HOME still works) and the docs name SAMPO_* first — verify with `python3 plugin/tests/run.py test_install test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] install.sh reads both; docs  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T06:03:46Z created
## Follow-ups captured
