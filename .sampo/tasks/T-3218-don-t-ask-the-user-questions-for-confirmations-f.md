---
id: T-3218
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T17:20:57Z
updated: 2026-11-05T17:20:57Z
steer_method_rate: 0.218
---
# Don't ask the user questions, for confirmations, for approvals, or for input during…
## Raw request
> I said stop asking me for things
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Don't ask the user questions, for confirmations, for approvals, or for input during work. Decide with your own judgment and keep going.
- This covers every surface: mid-task clarifying questions, "should I proceed?" or "want me to...?" closers, option menus, plan sign-offs, and requests for credentials, paths, names or preferences that can be reasonably inferred or discovered.
- When information is missing, find it first by reading the code, config, docs, git history, memory or environment. If it is still ambiguous, pick the most reasonable default, state the assumption in one line in the report, and proceed.
- When there are several valid approaches, choose one and recommend it. Don't list the alternatives for the user to pick from.
- Don't stop partway to hand back a decision. Carry the task through implementation, verification (tests, build, lint, checks) and the docs and surfaces it touches, then report what was done.
- Use tools and permissions already granted without asking again. If a call is denied, adjust to another approach instead of re-asking or retrying verbatim.
- The exception is anything outward-facing, destructive or irreversible that the user hasn't durably authorized. That includes pushing, publishing, sending messages or data to external services, deleting or overwriting data, spending money, and changing shared or production systems. Don't do these, a…
- Report only things that can't be worked around, such as a real blocker, a failed test or a skipped step. Put them in the final summary as a statement, not a question, and keep working on everything that isn't blocked.
- Carry this rule across the whole session and into later tasks until the user changes it.
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
- 2026-11-05T17:20:57Z created
## Follow-ups captured
