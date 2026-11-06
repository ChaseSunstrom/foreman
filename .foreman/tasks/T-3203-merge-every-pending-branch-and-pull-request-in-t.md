---
id: T-3203
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T13:21:54Z
updated: 2026-11-05T13:21:54Z
steer_method_rate: 0.218
---
# Merge every pending branch and pull request in the current work, without asking for…
## Raw request
> yes, merge everything, you don;t need to ask me, I already said you can do anything
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Merge every pending branch and pull request in the current work, without asking for confirmation first. The user has explicitly granted this.
- Before each merge, list what is pending and check each item's state: conflicts, failing or missing checks, and review status. Merge in dependency order.
- Run the tests, type checks and lint the change touches both before and after merging. If a merge breaks something, fix it or revert it, and report which.
- Resolve ordinary merge conflicts by reading both sides and keeping the intent of each. Don't discard either side's changes just to get a clean merge.
- If an item fails checks, has unresolved conflicts that can't be settled from the code, or would clearly break the build, skip it, say why, and keep merging the rest. Don't push it through by bypassing protections or skipping checks.
- Update the docs, changelog and tests that the merged changes affect, so the merged result is complete.
- The grant covers merging only. Force-pushes, history rewrites, deleting remote branches or data, tagging or publishing releases, deploys, and anything else outward-facing or irreversible still need the user's own go-ahead.
- Before any deletion or overwrite that a merge involves, inspect the target first.
- Don't treat "do anything" as a blanket grant. Take actions beyond merging only where the user has actually said so in this session.
- After finishing, report faithfully: what was merged, what was skipped or failed and why, and the test output, stated plainly with no hedging on verified results.
- Keep applying this for the rest of the session. Don't re-ask about merges that fall inside this grant.
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
- 2026-11-05T13:21:54Z created
## Follow-ups captured
