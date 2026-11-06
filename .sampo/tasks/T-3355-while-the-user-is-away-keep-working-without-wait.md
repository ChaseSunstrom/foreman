---
id: T-3355
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T05:38:32Z
updated: 2026-11-06T05:38:32Z
steer_method_rate: 0.218
---
# While the user is away, keep working without waiting for check-ins. Pick up the next…
## Raw request
> I am going afk, I will want to see a shit ton of things completed by the time I wake up, so feel free to keep running a bunch of agents
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- While the user is away, keep working without waiting for check-ins. Pick up the next most valuable unfinished work from the user's stated goals, open tasks, failing tests and known TODOs, and continue until the work runs out or a hard limit is reached.
- Run multiple agents in parallel on independent tasks, and keep each agent on its own files or branch so they don't conflict. Run dependent tasks in sequence.
- Count a task as complete only when it is finished end to end. That means the code change, its tests, updated docs and config, and a passing build, lint and test run, with the output as evidence.
- Report failures, skipped steps and unverified work plainly. Never present partial work as done.
- Stay within the user's grant. Do not push, publish, deploy, send messages, spend money outside the budget, delete or overwrite data, or take other outward-facing or irreversible actions without explicit permission. Instead, prepare those actions ready to run, such as local commits, drafts, or a wri…
- Do not widen scope beyond the user's work and repo. Do not touch unrelated systems, credentials or shared resources.
- Do not stop at the first blocker. Park a blocked task with a note on what is needed, and move to the next task. Retry a failed approach only with a changed approach, not verbatim.
- Track spend against the USD budget, and stop launching new agents before it is exhausted. Do not spawn agents or loops that have no clear finish condition.
- Keep a running log of what was done, what was verified, what is blocked, and what needs a decision. Make changes easy to review and revert, using small, separate, well-described commits or patches where version control exists.
- When the user returns, lead with a concise summary: completed and verified items, failures and blockers, pending approvals, and suggested next steps.
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
- 2026-11-06T05:38:32Z created
## Follow-ups captured
