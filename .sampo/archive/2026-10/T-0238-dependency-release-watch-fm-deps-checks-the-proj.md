---
id: T-0238
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-0227]
source: user
created: 2026-10-04T05:27:19Z
updated: 2026-10-04T07:55:40Z
done_in: T-0278
---
# Dependency-release watch — fm deps checks the project's dependencies (requirements, pyproj
## Raw request
> FEATURE: dependency-release watch — fm deps checks the project's dependencies (requirements, pyproject, package.json, Cargo.toml) against their latest releases and, for a new major, pre-researches the migration with fm research ask #T-0227
> CONTEXT: stdlib urllib to PyPI/npm/crates JSON APIs (public https only, like fmresearch.fetch)
> DONE-WHEN: with a fake registry response, fm deps lists an outdated major and offers the migration research
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-04T05:27:19Z created
- 2026-10-04T05:27:29Z set tier=M
- 2026-10-04T07:46:35Z batched into T-0278
- 2026-10-04T07:55:40Z done in T-0278 (batch)
## Follow-ups captured
