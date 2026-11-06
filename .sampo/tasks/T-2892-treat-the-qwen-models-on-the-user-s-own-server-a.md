---
id: T-2892
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T04:03:07Z
updated: 2026-11-05T04:44:33Z
steer_method_rate: 0.218
---
# Treat the Qwen models on the user's own server as a generous token budget. They have no…
## Raw request
> you can use more tokens on the qwen models on my server, it has up to 256k context for 2 different sessions
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the Qwen models on the user's own server as a generous token budget. They have no per-token cost like paid API models, so use more tokens where it improves the work: fuller file context, longer prompts, more examples, more thorough reasoning and output, and fewer lossy truncations and summari…
- Hard ceiling: each Qwen session may use up to 256k tokens of context. Keep a safety margin below that (for example, compact or chunk at about 85-90%) so requests don't fail at the limit.
- Hard concurrency limit: at most 2 Qwen sessions at once. Queue, serialize or reuse sessions for further work instead of opening a third, and release a session when its work is done.
- Apply this everywhere the harness uses these models. That covers the model and endpoint configs, context-window and max-token settings, prompt and context packing, chunking and summarization thresholds, retry and truncation logic, and delegation or routing rules. Raise any limits that were set cons…
- Check the actual server settings rather than trusting the stated figure. Query the server or its config for the loaded context length per model and the parallel-slot count, and use the smaller of what's configured and 256k if they differ. Report any mismatch.
- The larger budget is for Qwen only. Don't extend it to other models or providers, and keep their budgets, cost limits and the USD cap as they are.
- Don't pad. Use the extra room when it improves correctness or completeness, such as reading whole files, wider test or log output, or cross-checking, and not to inflate output.
- Measure it. Log or report per-session token usage against the 256k ceiling and the number of active Qwen sessions, so overruns and a hit concurrency limit are visible. Add or update tests for the new limits and the 2-session cap.
- Document the rule where future sessions will see it, such as the project config or CLAUDE.md and the memory index. State the models, the 256k per-session context, the 2-session limit and the date of the grant.
- Stay within what was granted. Using the user's Qwen endpoint at larger context is allowed. Restarting or reconfiguring the server, loading or unloading models, changing its hardware or network exposure, or sending data to any other host or service needs a separate explicit grant.
- If the server reports errors, out-of-memory conditions or slowdowns at the larger sizes, back off to the largest stable size, say so plainly, and don't retry the same oversized request in a loop.
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
- 2026-11-04T04:03:07Z created
- 2026-11-05T04:44:33Z dropped: done: the jarvis, jarvis-nothink and jarvis35-nothink profiles serve 256,000 context with 32,000 out (models.json); two sessions share the server (moons fill uses 2 workers)
## Follow-ups captured
