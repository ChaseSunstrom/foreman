---
id: T-3477
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T18:30:50Z
updated: 2026-11-06T18:30:50Z
steer_method_rate: 0.218
---
# Before calling any piece of work done, review it as the user would: walk through…
## Raw request
> how come I even needed to point this stuff out and ask for it to be fixed, this was also what I mean by you need to think of everything, I shouldn't need to point anything out
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Before calling any piece of work done, review it as the user would: walk through everything the change touches (code paths, callers, config, UI and output, error and edge cases, tests, docs, changelog, migrations, and related files). Fix every gap found without waiting to be told.
- Treat a user's correction as evidence of a missed class of problem, not a single bug. Find and fix every other instance of the same pattern across the project, then say what was found.
- Before handing off, list the requirements, stated and implied. Check each against the actual result (run it, test it, look at the output), not just against the intent.
- Run the relevant build, tests, linters, and type checks, and exercise the changed behavior directly. Add or update tests for what changed, including regressions for anything the user had to point out.
- Keep docs, comments, examples, and naming in sync with the change in the same pass.
- Check neighboring and sibling things: other call sites, parallel implementations, platforms, configs, and environments that should behave the same way.
- Act on gaps rather than advising about them. Make the fix, don't offer a list of suggestions, and ask only when the answer genuinely can't be determined.
- Report faithfully at the end: what was done, what was verified and how, and what was not done or could not be verified. Don't claim completeness that wasn't checked.
- When the user has to point something out anyway, acknowledge the miss briefly, fix it fully, and extend the check to the whole category so it doesn't recur.
- Anything outward-facing, destructive, or irreversible (pushing, publishing, sending, deleting, overwriting, spending money, touching shared systems) still requires the user's explicit grant. Thoroughness never extends to those actions on its own.
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
- 2026-11-06T18:30:50Z created
## Follow-ups captured
