---
id: T-3159
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T06:06:07Z
updated: 2026-11-05T06:06:07Z
steer_method_rate: 0.218
---
# Start now and keep a running work log of everything done, for as long as the work…
## Raw request
> also start keeping track of everything that youre doing and from my next message, as that will be in the morning 8 hours from now and I will be curious what all has been done
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Start now and keep a running work log of everything done, for as long as the work continues. Append each entry as it happens, not reconstructed afterward, so it survives context summarization and interruptions.
- Keep the log in one durable local file outside the project's source tree, for example a timestamped Markdown file in the working directory's notes area. Create it at the start and name its path in the first reply.
- Give every entry a timestamp, what was done, and why. Cover:
- files created, edited, moved or deleted (with paths);
- commands run and their outcomes;
- tests, builds and checks run, with pass/fail results and failing output;
- decisions taken and the alternatives rejected;
- errors, dead ends and retries;
- steps skipped or left incomplete, and why;
- budget or time used, where known.
- Record failures and skipped work as plainly as successes. Never log something as done unless it was verified.
- Record anything that needs the user's approval or was held back, such as outward-facing, destructive or irreversible actions, in a separate "Awaiting your decision" list. Keep working on what is safe in the meantime.
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
- 2026-11-05T06:06:07Z created
## Follow-ups captured
