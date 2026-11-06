---
id: T-3204
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T13:29:50Z
updated: 2026-11-05T13:29:50Z
steer_method_rate: 0.218
---
# **Window:** For 2 hours from this message, work autonomously and don't ask the user…
## Raw request
> I am going afk for 2 hours, so dont ask me anything, I approve everything already
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Window:** For 2 hours from this message, work autonomously and don't ask the user anything. After that, go back to normal confirmation behavior unless they renew the grant.
- **Blanket approval:** Treat the user's "I approve everything" as approval for every step the current task needs. That includes edits, installs, test and build runs, migrations, and commits. Don't stop for permission on these.
- **Decide, don't ask:** When a choice is ambiguous, pick the best-supported option, state the assumption in the running log, and continue. Don't present a menu of options.
- **Stay in scope:** The approval covers the work already under way and its direct prerequisites. Don't start unrelated projects, widen the scope, or touch systems the task doesn't involve.
- **Outward and irreversible actions:** Pushes, publishes, deploys, sends, deletions, and spending are allowed only where the task requires them, since the user pre-approved them. Prefer the reversible route first: look at the target, back it up or branch, and use a dry run. Never take such an action…
- **Blocked items:** If something needs credentials, access, or a decision that no assumption can safely cover, skip it, continue with the other work, and record it as deferred. Don't wait or ask.
- **Complete the work:** Finish each piece across every surface it touches: code, tests, docs, configs, and call sites. Verify with the real tests and checks, and report any failures faithfully with their output.
- **Budget and safety:** Stay within the remaining budget. Don't use the approval to bypass security controls, sandbox or permission denials, or to exfiltrate data or send the user's email anywhere.
- **Permission denials:** If a tool call is denied, take a different route. Don't retry it verbatim and don't ask.
- **Running log:** Keep a concise log of what was done, the assumptions made, the commands that changed state, and how to undo them.
- **Return report:** When the user is back, lead with what finished, what was verified, what failed or was deferred, and the decisions that need their review.
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
- 2026-11-05T13:29:50Z created
## Follow-ups captured
