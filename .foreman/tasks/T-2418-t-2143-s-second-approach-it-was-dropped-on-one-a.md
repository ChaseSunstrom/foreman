---
id: T-2418
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T14:56:40Z
updated: 2026-11-01T23:53:59Z
group: critique-finish follow-ups
---
# T-2143's second approach (it was dropped on one): a byte-stable goal card placed where…
## Raw request
> T-2143's second approach (it was dropped on one): a byte-stable goal card placed where the cached prefix is (a file Claude Code loads with CLAUDE.md), unchanged while the goal stands; if this fails too, not-yet.md with its blocker (from gen-1/critique-finish.md)
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
- 2026-10-31T14:56:40Z created
- 2026-11-01T23:53:59Z dropped: its own fallback: the second approach has no measurable win either (the goal card is ~30 tokens; SessionStart context is cached after its first write per session), so it went to not-yet.md with its blocker and what would unblock it (a 2k+ token card, measured by fm cost)
## Follow-ups captured
