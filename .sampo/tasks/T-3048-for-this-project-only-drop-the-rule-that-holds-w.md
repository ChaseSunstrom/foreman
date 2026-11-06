---
id: T-3048
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T00:11:10Z
updated: 2026-11-05T04:44:35Z
steer_method_rate: 0.218
---
# For this project only, drop the rule that holds work back or pauses/throttles it once…
## Raw request
> remove the weekly usage 80% lean on this project specifically, I have a few subscriptions to claude, so no need to worry about usage, don't waste it, but no need to hold back at that point
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- For this project only, drop the rule that holds work back or pauses/throttles it once weekly Claude usage reaches 80%; remove that threshold everywhere it is configured or documented in the project (settings, scripts, harness config, prompts, docs, tests, notes) so no check, warning, or stop fires …
- Do not apply the change outside this project: leave global, other-project, and user-level usage limits and settings untouched.
- Keep the other usage discipline: do not waste usage, so avoid redundant runs, needless retries, idle loops, and oversized or duplicated work, while no longer rationing work for fear of the weekly cap.
- Keep any hard limits that are not the 80% rule (a real API/plan cutoff, the dollar budget, rate-limit handling, and error backoff) working as before, and surface them if they are hit.
- Work at full pace on this project at any usage level below the real cap, without asking permission to continue because usage is high.
- Check the removal by searching the project for the 80% / weekly-usage threshold and confirming no remaining references, and by running the project's tests or checks to show nothing else broke.
- Record the decision (several Claude subscriptions, so weekly usage is not a concern here, but waste is) in the project's notes or memory so later sessions follow it.
- Anything outward-facing, destructive, or irreversible (pushing, deploying, deleting, spending money beyond the stated budget) still needs the user's explicit go-ahead.
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
- 2026-11-05T00:11:10Z created
- 2026-11-05T04:44:35Z dropped: done in T-3049: weekly_lean is off for this project; the 5-hour 90% rule stays
## Follow-ups captured
