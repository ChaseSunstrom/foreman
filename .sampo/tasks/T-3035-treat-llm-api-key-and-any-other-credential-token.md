---
id: T-3035
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T23:49:36Z
updated: 2026-11-05T04:44:35Z
steer_method_rate: 0.218
---
# Treat `LLM_API_KEY`, and any other credential, token or secret the user hands over, as a…
## Raw request
> here is this: LLM_API_KEY=[REDACTED], keep it and store it somewhere so you don't forget, I shouldn't even need to tell you this
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat `LLM_API_KEY`, and any other credential, token or secret the user hands over, as a standing, persistent secret. Store it the first time it is given, without waiting to be told again or asked to confirm.
- Store it in a local secrets file outside version control, such as a user-owned `.env` or equivalent config store, with owner-only permissions (0600). Add that path to `.gitignore` before writing the value. Never put the value in the memory index, memory files, source, tests, fixtures, docs, comment…
- Store the value exactly as given as `LLM_API_KEY=[REDACTED] If the pasted value is a redaction placeholder or looks truncated or malformed, say so and ask for the real one instead of storing a fake.
- Load the key from the environment or secrets file at the start of every session and for every run that needs it (app, scripts, tests, evals). Code reads it via the environment variable and never hardcodes it. If it is missing, check the secrets file first and only then ask the user.
- Record the variable's name, purpose and where it is loaded from, but never the value, in a durable place: a `.env.example` with a blank placeholder, a README setup note, and a memory entry that points to the location.
- Never print, log, echo or quote the key in output, errors, diffs, test results, traces or summaries. Mask it (for example `sk-…abcd`) if it must be referenced, and scrub it from any captured output before sharing.
- Send the key only to the service it belongs to, in an auth header. Never put it in URLs, query strings, telemetry, issue text, pastes or third-party tools.
- After storing, verify without revealing it: confirm the file exists, has the right permissions, is gitignored, and that the variable loads (for example, check it is non-empty). Report the location and the verification result plainly, and say if any step was skipped or failed.
- If the key is found committed, logged or exposed anywhere, flag it immediately and recommend rotation. Do not rotate, revoke, delete or replace it without the user's explicit grant.
- Apply the same handling to any later secret the user shares, without being told again.
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
- 2026-11-04T23:49:36Z created
- 2026-11-05T04:44:35Z dropped: done in T-3036/T-3080: the key lives in ~/.config/sampo/secrets.env (600), read by models.secret(); never echoed or committed
## Follow-ups captured
