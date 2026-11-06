---
id: T-2881
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T03:40:57Z
updated: 2026-11-04T03:40:57Z
steer_method_rate: 0.218
---
# Read "jeff" as the name of a classifier in Sampo, not a person, a typo, or an unrelated…
## Raw request
> I meant jeff as the classifier or whatever, similar to jev, there might be other ones
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Read "jeff" as the name of a classifier in Sampo, not a person, a typo, or an unrelated identifier. Read "jev" the same way. Both belong to a family of named classifiers.
- Expect more names of this kind. When an unfamiliar short name shows up where a classifier would fit, look it up in the repo and config first, and treat it as another member of the family. Don't guess it's a typo or a person.
- Resolve each name to its concrete definition by searching code, config, prompts, tests, docs and logs. Confirm which classifier it is before acting. If several candidates match, pick the best-supported one and say so, rather than stalling.
- When an instruction names one classifier and the pattern clearly covers its siblings, apply it to jeff, jev and any others found. List which ones were covered.
- Keep every surface consistent. A change to or reference to a classifier covers its code, config, prompts, tests, docs and naming, across all siblings.
- Verify by running the relevant tests or checks, and report the results as they are, including failures.
- Revisit any earlier work in this conversation that assumed "jeff" meant something else, and correct it.
- Act directly instead of advising. Report what was found and changed, and name any classifier you couldn't resolve.
- Anything outward-facing, destructive or irreversible stays behind the user's explicit approval. That includes publishing, deploying, deleting, overwriting, and retraining on live data.
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
- 2026-11-04T03:40:57Z created
## Follow-ups captured
