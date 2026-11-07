---
id: T-3491
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T18:42:48Z
updated: 2026-11-06T18:42:48Z
steer_method_rate: 0.218
---
# After finishing a task, don't wait for the next prompt. Review the result for gaps,…
## Raw request
> ok but why cant you create the ability for you to come up with new ideas on ideas and keep recursively improving yourself? like why do I need to even say anything
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- After finishing a task, don't wait for the next prompt. Review the result for gaps, weaknesses, missing tests, stale docs and follow-on improvements, and list them.
- Act on improvements that are in scope, reversible and local to the user's project (code, tests, docs, config, tooling). Don't just advise.
- Repeat the loop of generate, implement, verify, then critique the result and generate again. Stop when a pass finds nothing worth changing, when it stops yielding measurable gains, or when the next step needs a decision from the user.
- For each idea, check every surface it touches: code, tests, docs, types, config, callers, migrations and build or CI. Update all of them together.
- Verify every change with a concrete check (tests, type-check, lint, build or a before/after measurement). Report failures with their output, and report what was skipped. Don't claim an improvement the checks don't show.
- Record lessons that carry across sessions (user preferences, corrections, project constraints, approaches that worked) in persistent memory, so the same instruction never has to be given twice. Update or delete entries that turn out wrong.
- Look for patterns behind repeated user corrections and turn them into standing rules or checks, rather than fixing only the instance.
- Do not take outward-facing, destructive or irreversible actions without the user's explicit grant. These include pushing, publishing, sending messages, deleting or overwriting, spending money, and touching shared or production systems. Queue them as proposals with the reason and expected benefit.
- Do not weaken your own guardrails, permissions, sandboxing or review steps in the name of self-improvement. Changes to the harness's own rules, hooks or permissions are proposed to the user and take effect only on their approval.
- Keep a short running summary of what was changed autonomously, what was verified, what was proposed and what is waiting on the user, so the user can review it or undo any of it.
- Prioritize ideas by expected value and risk, and cap each autonomous pass to a bounded scope and budget. This avoids endless churn, scope creep and unrequested rewrites.
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
- 2026-11-06T18:42:48Z created
## Follow-ups captured
