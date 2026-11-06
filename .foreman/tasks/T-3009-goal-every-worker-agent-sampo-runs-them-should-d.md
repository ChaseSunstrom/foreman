---
id: T-3009
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T19:32:11Z
updated: 2026-11-04T19:32:11Z
steer_method_rate: 0.218
---
# **Goal:** Every worker agent Sampo runs ("them") should deliver work at the level of the…
## Raw request
> I want them to get to your level of ability on anything though, whatever it takes.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Goal:** Every worker agent Sampo runs ("them") should deliver work at the level of the strongest model on any task, in any domain, not just the current one. Treat any shortfall as a defect to close.
- **Scope:** Apply this to planning, implementation, proving (tests, checks, review) and finishing (docs, cleanup, handoff) across all task types, languages and codebases.
- **Check it concretely:** Judge quality by observable results: tests and builds pass, requirements are met, review finds no material issues, and output matches what the strongest model would produce on the same task. Where a gap is suspected, compare against a reference run or an eval.
- **Act, don't advise:** When a worker falls short, fix the cause directly. Improve its prompt, context, tools, task decomposition, examples or verification loops, or rerun the work with more care. Don't just report the gap.
- **Escalate rather than lower the bar:** If a worker can't reach the bar after a real attempt, escalate to a stronger model or a more thorough process rather than shipping weaker work. Never narrow scope, weaken tests or fake a pass to appear to meet the bar.
- **Cover every surface:** Closing a gap includes the tests, docs, configs, evals and related code it touches, not only the one failing spot.
- **Make improvements durable:** Record what closed each gap (skills, prompts, memory, guidance) in reusable form so later runs start at the higher level.
- **Measure progress:** Track recurring failure types and whether they shrink, and report honestly where a gap remains. Don't claim parity without evidence.
- **"Whatever it takes" is bounded:** Pursue it with all means within the current budget and permissions.
- **Keep gated actions behind the user's grant:** Ask first before anything outward-facing (publishing, sending data to external services), destructive or irreversible (deleting or overwriting), or costly beyond the remaining budget. Approval for one such action doesn't carry over to the next.
- **Interpretation:** Read "them" as the agents and workers Sampo orchestrates, and "your level" as the top capability of the model the user is addressing. If that reading is wrong, surface the ambiguity rather than guessing silently.
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
- 2026-11-04T19:32:11Z created
## Follow-ups captured
