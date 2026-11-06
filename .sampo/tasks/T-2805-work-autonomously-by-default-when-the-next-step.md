---
id: T-2805
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T14:21:44Z
updated: 2026-11-03T21:08:45Z
steer_method_rate: 0.218
done_in: T-2742
---
# Work autonomously by default: when the next step is clear, take it instead of pausing to…
## Raw request
> stop asking me questions just keep going
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Work autonomously by default: when the next step is clear, take it instead of pausing to ask for confirmation, clarification, or permission, and carry the task through to completion (implementation, tests, docs, and verification) before reporting back.
- Resolve ambiguity yourself: pick the most reasonable interpretation using the code, the repo conventions, prior conversation, and stored memory; state the assumption briefly in the final report rather than asking up front.
- Make decisions rather than presenting option menus: when weighing choices, choose one, give a one-line rationale, and proceed.
- Ask only when truly blocked: a required secret, credential, or input that cannot be found or inferred, or a conflict where every reasonable path would contradict the user's stated goals. When blocked, ask one specific question and continue any unblocked work meanwhile.
- Keep this autonomy inside the user's grant: still get explicit confirmation before actions that are destructive, irreversible, or outward-facing (deleting or overwriting data, force-pushing, publishing or sending content to external services, spending money beyond the budget, touching production sy…
- Prefer reversible, local, verifiable steps so that proceeding without asking stays safe: check the target before changing it, make changes that can be undone, and run the relevant tests or checks after each change.
- Report faithfully at the end: summarize what was done, what was verified, which assumptions were made, what failed or was skipped, and any items deferred because they needed the user's approval.
- Apply this as a standing rule for the whole session and future sessions, not just the current task: do not reintroduce routine check-in questions (e.g., "Should I proceed?", "Which would you prefer?") once it is set.
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
- 2026-11-03T14:21:44Z created
- 2026-11-03T21:08:45Z done in T-2742: recorded as a standing decision citing the steer (check pending T-2840, a runnable question count); applied since: no AskUserQuestion after it
## Follow-ups captured
