---
id: T-2831
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T19:12:37Z
updated: 2026-11-03T21:08:45Z
steer_method_rate: 0.218
done_in: T-2742
---
# Publish the current state of the work's artifacts (reports, outputs, proofs, test…
## Raw request
> can you upload what is current to the artifact page? and keep a running live update of them
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Publish the current state of the work's artifacts (reports, outputs, proofs, test results, docs, generated files) to the project's artifact page now. Don't just describe how to do it.
- Treat the user's request as the grant for this one destination only: the artifact page they named. Publishing to any other external service, page, or audience needs a fresh grant.
- Before each upload, check what is going out. Exclude secrets, credentials, tokens, `.env` contents, personal data, and unrelated or untracked scratch files. Report anything held back and why.
- Before overwriting an existing artifact entry, look at what is there. Update it in place, and never delete or replace entries the agent didn't create without asking.
- Keep the page live. After every meaningful change to an artifact (a finished step, a changed result, a new test run, a revised doc), re-upload the affected items so the page matches the work. Do this without being asked each time.
- Make updates incremental and idempotent. Upload only what changed, keep stable names or IDs so entries update rather than pile up as duplicates, and show a timestamp or version on each entry.
- Keep each upload faithful to the real state. If tests fail or a step was skipped or is unfinished, the page says so, with the output, and never shows a passing or complete state that isn't true.
- Verify each upload landed. Re-fetch or list the page entry and confirm it matches the local source, then tell the user the result plainly, including failures.
- If the upload mechanism is missing or fails (no credentials, unknown page, tool denied), say so, name what's needed, and don't retry the denied call verbatim. Keep working locally and queue the updates.
- Continue the running updates for the rest of the session, and across context summaries, until the user says to stop. Stopping needs only their word, and no confirmation is needed.
- Report briefly after each update: what was published, where, and what changed. Don't flood the user with chatter.
- Do not expand scope on the user's behalf: no new pages, no public sharing or link-visibility changes, no notifications to other people, unless the user grants them.
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
- 2026-11-03T19:12:37Z created
- 2026-11-03T21:08:45Z done in T-2742: recorded as a standing decision (check pending T-2788); the picker artifact is republished on every render
## Follow-ups captured
