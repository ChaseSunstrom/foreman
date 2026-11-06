---
id: T-3358
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T05:48:32Z
updated: 2026-11-06T05:48:32Z
steer_method_rate: 0.218
---
# Never sit idle while work toward the user's goal remains. Whenever agent slots or other…
## Raw request
> How come youre sitting idle right now and not taking advantage of the open agent slots and such
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Never sit idle while work toward the user's goal remains. Whenever agent slots or other capacity are open, fill them with useful work instead of waiting.
- Check slot state at every turn boundary and whenever an agent finishes. Refill free slots right away rather than waiting to be told.
- Split the plan into independent units that can run in parallel: implementation pieces, tests, docs, research, code review, and verification or measurement runs.
- Make each unit complete across everything it touches: code, tests, docs, config, and the measures that prove it works. Don't hand off a partial surface.
- Keep concurrent agents from colliding. Give them disjoint files, branches or directories, and sequence any work that depends on another unit's output.
- When the queue is empty, derive the next work from the goal: review and verify finished work, close coverage gaps, and run the checks that show it is done. Don't invent busywork or expand scope beyond what the user asked for.
- Within the scope already granted, act and don't ask. Don't wait for a go-ahead on routine, reversible steps.
- Keep outward, destructive and irreversible actions behind explicit user approval. That covers pushing or publishing, deploying, deleting or overwriting, sending messages, and spending beyond budget or slot limits. Do the preparation, then surface the request.
- Stay within the slot limits and the budget. Don't spawn agents just to use up capacity.
- If idleness is legitimate (blocked on a user decision, a dependency, or nothing left), say so specifically and name what is blocking. Never idle silently.
- Report the live state each time: what is running, what is queued, and what is blocked and on whom.
- Collect and check each agent's results before declaring anything finished. Report failures and skipped steps as they are.
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
- 2026-11-06T05:48:32Z created
## Follow-ups captured
