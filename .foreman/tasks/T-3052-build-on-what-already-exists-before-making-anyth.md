---
id: T-3052
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T00:18:49Z
updated: 2026-11-05T00:18:49Z
steer_method_rate: 0.218
---
# Build on what already exists. Before making anything new, find the existing code, tools,…
## Raw request
> and keep like building on built things going forward, for example if new things change how you behave, like coming up with ideas/more thoughts and such better, add that to the genesis of genesis, an infinite loop, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Build on what already exists. Before making anything new, find the existing code, tools, prompts, docs, and tests that cover the need, then extend or compose them. Don't rebuild, fork, or replace them unless the user says to.
- Treat each finished piece as a foundation for the next. Record what was built, what it enables, and where it lives, so later work starts from it.
- When a new change improves how Sampo behaves (better ideation, deeper or broader thinking, better planning, sharper checks), fold that improvement back into the genesis, the foundational definition that seeds Sampo's behavior. Don't leave it only in the one place where it first appeared.
- Propagate those improvements one level up as well, into the genesis of genesis: the meta-layer that produces and refines the genesis. Improvements to how Sampo improves belong there.
- Run this as a continuing loop: build, observe what changed in behavior, feed it back into the genesis and the meta-layer, then build again with the improved behavior. Run it on every relevant piece of work, not just once.
- Make each iteration concrete and checkable. Name the behavior that changed, the file or setting that now encodes it, and a test, example, or before/after comparison showing the change is real. Don't record a claimed improvement that can't be shown.
- Keep every surface consistent when the genesis changes. Update the prompts, configs, docs, tests, and examples that depend on it, and re-run the affected tests and checks.
- Apply feedback changes directly. Don't just suggest them. Keep them small and reviewable, and leave the earlier version recoverable (diff, backup, or changelog entry).
- Keep the loop continuous but bounded. Each pass has a stated scope, a budget check, and a stopping condition, and the loop pauses and reports if an improvement doesn't verify, regresses behavior, or conflicts with an existing rule or user instruction.
- Get the user's explicit grant before anything outward, destructive, or irreversible. That includes publishing or pushing, sending data to external services, deleting or overwriting prior work, spending money, and changing permissions or safety constraints. Self-modification must never loosen the us…
- Locate the actual genesis and genesis-of-genesis artifacts in the project before editing. If they don't exist or can't be identified, say so and propose where they would live rather than inventing them.
- Report each pass faithfully: what was built on, what improved, what was folded back into which layer, what was verified, and what failed or was skipped.
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
- 2026-11-05T00:18:49Z created
## Follow-ups captured
