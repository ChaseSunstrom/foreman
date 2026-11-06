---
id: T-3158
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T06:04:06Z
updated: 2026-11-05T06:04:06Z
steer_method_rate: 0.218
---
# Put the capability the user just discussed (the "that") into the custom model…
## Raw request
> maybe add that as part of the custom model or something, and we will want more than just want Sampo has done/need, we will need basically every possibility
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Put the capability the user just discussed (the "that") into the custom model definition, or the closest equivalent configuration layer, instead of leaving it as a one-off or hardcoded path. If the antecedent or the right place can't be determined from the recent conversation and the repo, ask one …
- Treat the custom model as the single source of truth for this capability. Other call sites, prompts and configs should read from it, not duplicate it.
- Scope it to the full space of possibilities, not just the cases Sampo has already handled or needed. Enumerate the dimensions (inputs, states, modes, edge and failure cases, and variants of the thing), then cover each one.
- Keep a written coverage list of those possibilities in the repo, such as a table or checklist next to the model. Mark each item as covered, intentionally excluded (with a reason) or open, so completeness can be checked rather than asserted.
- Add tests for each enumerated possibility, including ones Sampo has never encountered. Add a test or check that fails when a new possibility appears in the model or the data without being handled.
- Update every surface the change touches: schema and types, defaults, validation, docs, examples, migration or backward compatibility for existing Sampo behavior, and any UI or CLI that exposes it.
- Make the model extensible so a missing possibility becomes a data or config addition and doesn't require a code rewrite.
- Run the full existing test suite and the new tests. Report results as they are, including failures, skipped items and any possibilities left open.
- Make the edits directly rather than only proposing them, and keep them local. Anything outward-facing, destructive or irreversible, such as publishing, deleting or overwriting existing models or data, or touching external services, waits for the user's explicit go-ahead.
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
- 2026-11-05T06:04:06Z created
## Follow-ups captured
