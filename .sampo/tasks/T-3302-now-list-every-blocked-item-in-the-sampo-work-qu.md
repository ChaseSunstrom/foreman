---
id: T-3302
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T03:49:54Z
updated: 2026-11-06T03:49:54Z
steer_method_rate: 0.218
---
# Now: list every blocked item in the Sampo work queue (blocked tasks, stalled plans,…
## Raw request
> can you unblock everything thats blocked? and constantly review blocked things so they don't just sit in blocked forever? I shouldn't even need to ask you that, this is what I am talking about when I say think of everything and be self aware, I shouldn't even need to point out ANYTHING
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Now: list every blocked item in the Sampo work queue (blocked tasks, stalled plans, failed or waiting proofs, stuck builds, tests, reviews, merges, dependencies, and anything else marked blocked, waiting or stuck). For each one, state the cause of the block and what would clear it.
- Unblock each item yourself wherever you can. Fix the failing test or build, resolve the dependency or conflict, supply the missing information, split or reorder the work, or take the next step the item was waiting on. Don't report a blocker back to the user if you could have cleared it.
- Re-verify after each unblock. Run the relevant proof (tests, build, checks) and confirm the item is moving or finished. Don't mark it unblocked on the strength of a change alone.
- Ongoing: review the blocked list at the start of every session, after every completed task, and at regular intervals during long runs. No item should sit in blocked across reviews without a recorded attempt to clear it.
- Give each blocked item a recorded reason, a time it became blocked, the last attempt made and the next action. Treat any item whose blocker has since disappeared as unblocked, and resume it automatically.
- If a block can't be cleared by you, escalate it. This covers blocks that need a credential, a decision, an approval or an outside party. Ask the user one specific question, with a recommended answer, and keep working on everything else in the meantime.
- Keep outward, destructive and irreversible steps behind the user's explicit grant. This includes pushing, publishing, sending messages, deleting or overwriting data, spending money, changing permissions and force-merging. Don't bypass a guardrail, skip a check or weaken a test just to clear a block…
- Be proactive beyond this request. When you find a related problem (a stale or duplicate blocked item, a missing doc, a flaky test, or a root cause shared by several blocks), fix it or queue it without being asked. Include the docs, tests and tracking surfaces the change touches.
- Report each review briefly and honestly. List what was unblocked and verified, what is still blocked and why, and what needs the user. Say plainly if a step failed or was skipped.
- Treat this as a standing way of working. The user shouldn't have to repeat it or point out the obvious.
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
- 2026-11-06T03:49:54Z created
## Follow-ups captured
