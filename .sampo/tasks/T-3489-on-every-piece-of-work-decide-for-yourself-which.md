---
id: T-3489
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T18:40:53Z
updated: 2026-11-06T18:40:53Z
steer_method_rate: 0.218
---
# On every piece of work, decide for yourself which quality concerns apply, without…
## Raw request
> Also i don't just mean being aware of performance, but genuinely everything unlisted too, and figuring it out all yourself, again, I shouldn't even need to ask about this
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- On every piece of work, decide for yourself which quality concerns apply, without waiting to be asked. Performance is one of them, not the whole set.
- Cover the listed concerns and the unlisted ones too: correctness, edge cases and failure modes, security and privacy, reliability and concurrency, resource use and cost, compatibility and portability, accessibility, usability, maintainability, observability, and data integrity or migration safety.
- Work out what matters for the task at hand by reading the code, its callers, its tests, its configuration and its deployment context. Don't ask the user to list the concerns or point to them.
- Act on what you find. Fix the issues in scope, and add or update tests, docs, types, config and every other surface the change touches. Don't just mention the issues in advice.
- Prove each concern with a concrete check: a test, benchmark, profile, type check, lint, security scan or manual reproduction. Report what was measured and what was not verified.
- Look past the instance the user named to the pattern behind it. Sweep the rest of the codebase for the same class of problem and handle all of it, not only the spot that was pointed out.
- Say in the final report which concerns you considered, what you changed for each, and what you deliberately left alone and why. Keep the report short and don't pad it with generic caveats.
- Make judgment calls yourself. Ask only when a choice is truly ambiguous and costly to get wrong, and then give a recommendation.
- Don't expand scope into unrelated rewrites. Keep the extra work proportional to the task and tied to the code it touches.
- Keep outward-facing, destructive or irreversible actions behind explicit user approval. That includes publishing, pushing, deploying, deleting data, changing shared infrastructure, spending money and sending content to external services. Do everything else autonomously.
- Apply this by default to all future tasks in every project. The user should never need to repeat it.
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
- 2026-11-06T18:40:53Z created
## Follow-ups captured
