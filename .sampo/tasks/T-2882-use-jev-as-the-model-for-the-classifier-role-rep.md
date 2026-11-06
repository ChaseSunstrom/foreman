---
id: T-2882
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T03:42:01Z
updated: 2026-11-05T04:44:33Z
steer_method_rate: 0.218
---
# Use "jev" as the model for the classifier role, replacing whatever model is currently…
## Raw request
> no, jev, as the classifier model, its somewhat new so you might want to research it
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Use "jev" as the model for the classifier role, replacing whatever model is currently used there. Do not swap in a familiar model, and do not change the models used for other roles.
- Treat "jev" as new and unfamiliar. Before wiring it in, research it from primary sources (official docs, model card, API reference, release notes, the repo's own references). Do not rely on memory or guesses.
- Confirm the exact identifier or ID, provider or endpoint, and how to authenticate. Also confirm supported parameters, input and context limits, output and structured-output format, rate limits, pricing and latency. If "jev" can't be resolved to one real model, stop and ask the user which they mean …
- Check that the classifier's prompt, label schema, output parsing and thresholds work with this model's actual behavior. Adapt them where they don't, and say what was adapted.
- Update every place the classifier model is named or assumed: code, config and defaults, env vars, docs and README, tests and fixtures, eval scripts, cost or latency budgets, and any mocks. Search the whole repo so no stale reference to the old model remains.
- Verify the change by running the existing tests plus a before/after comparison on labeled classifier examples. Report real results, including failures and anything skipped.
- Record the research findings (source links, model ID, limits, caveats) in the docs or the PR notes so the choice can be checked later.
- Make the change directly, but ask first before any outward, paid or irreversible step. That includes live API calls that cost money beyond the budget, publishing, pushing, deleting, or handling credentials. Never put API keys in code or logs.
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
- 2026-11-04T03:42:01Z created
- 2026-11-05T04:44:33Z dropped: done: Jeff is the classifier stack sampo-decide is trained on (T-2970: a LoRA on Jeff v1.3, live, research T-2970-sampo-decide)
## Follow-ups captured
