---
id: T-3000
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T18:49:27Z
updated: 2026-11-05T04:44:34Z
steer_method_rate: 0.218
group: live page data and polish
---
# For any work on the Sampo live view, treat `/api/state` as the source of truth. The page…
## Raw request
> Sampo live
> The page files (plugin/web/live) are not here; /api/state has the data.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- For any work on the Sampo live view, treat `/api/state` as the source of truth. The page files at `plugin/web/live` are not in this workspace, so don't search for them, recreate them from guesses, or stop because they're missing.
- Before reporting on or changing anything about live, fetch `/api/state` and read the actual response. Base every claim about fields, shape, values and status on that output, and don't assume a schema.
- Use read-only requests (GET) against `/api/state` by default. Any call that writes, mutates state, restarts something or reaches a host the user hasn't named needs the user's explicit grant first.
- If the endpoint is unreachable, returns an error or returns empty data, report the exact status and output. Don't invent data, fill in plausible values, or present stale data as current.
- When a task would normally mean editing the page (layout, rendering, wiring), say that the source isn't present. Then do what the data allows: describe, verify or diagnose from the state, or produce the change as a patch or spec the user can apply where the files live. Don't fabricate the missing f…
- Check the live behaviour the user cares about against the state data itself: the fields exist, their values are consistent, and they are fresh (check timestamps, and fetch twice if change over time matters). Report what was verified and what couldn't be, because the rendered page isn't available to…
- Record the discovered shape of `/api/state` (key fields, types, quirks) in the report, so later work doesn't rediscover it. Save it to memory only if it's non-obvious and durable.
- Keep tokens, cookies and other credentials found in state or responses out of logs, reports and any outbound request.
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
- 2026-11-04T18:49:27Z created
- 2026-11-05T04:44:34Z dropped: done: the live page (sampo watch --web, the sampo-live service on :46459) with the modern theme (T-3055) and charts (T-3092)
## Follow-ups captured
