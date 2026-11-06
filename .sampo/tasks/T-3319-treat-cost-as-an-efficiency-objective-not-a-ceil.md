---
id: T-3319
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T04:25:26Z
updated: 2026-11-06T04:25:26Z
steer_method_rate: 0.218
---
# Treat cost as an efficiency objective, not a ceiling: never meet a spending limit by…
## Raw request
> And I don't want to just "cap" the cost of things to prevent the work from getting done, I want it to still get done without burning a fuck ton of money, and quick, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat cost as an efficiency objective, not a ceiling: never meet a spending limit by dropping, truncating, skipping or weakening the work. The task must still finish at full scope and quality, and cutting scope to save money counts as failure.
- Reduce cost by making the work cheaper: avoid redundant calls, re-reads, retries and repeated derivation of facts already established; reuse and cache results; use targeted searches and edits instead of broad ones; pass only the context a step needs.
- Match model size and reasoning effort to the difficulty of each step: use smaller or faster models and low effort for mechanical, well-specified or bulk steps, and reserve the largest models and deep reasoning for steps that need them, without lowering correctness.
- Run independent steps in parallel and keep the critical path short, so work finishes quickly as well as cheaply. Don't pay for extra latency or extra spend where neither buys quality.
- Prefer the cheapest verification that is still conclusive (targeted tests, scoped checks, a run of only what changed) before any expensive full run. Run the full suite when the change warrants it, and never skip verification to save cost.
- Stop runaway spend early: bound loops, retries and long-running jobs, and when a step is burning budget without progress, change approach or surface the problem instead of continuing. Do this by changing the approach, not by abandoning the goal.
- Track spend against the budget as work proceeds, and report cost, time and tradeoffs honestly in the outcome. Say plainly what was spent and what was done, and never hide a quality shortfall behind a cost saving.
- Ask before any spend that is outward-facing, irreversible or outside the stated budget, such as paid external services, large cloud jobs or purchases. Cost optimization does not grant authority to incur these.
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
- 2026-11-06T04:25:26Z created
## Follow-ups captured
