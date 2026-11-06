---
id: T-2771
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T04:44:23Z
updated: 2026-11-03T04:47:21Z
steer_method_rate: 0.218
verified: weak
unproven: [meaning]
---
# When the current task is finished, do not stop or wait for further prompting:…
## Raw request
> make sure to keep going with everything else when done
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- When the current task is finished, do not stop or wait for further prompting: immediately continue with every remaining item in the user's request, plan, and task list, in order, until all of it is done.
- Before declaring completion, enumerate all outstanding work (open todos, unfinished steps in the plan, follow-ups discovered along the way, failing or skipped tests, pending docs/config/migration updates) and treat each as part of "everything else" to be completed.
- Make each item complete across every surface it touches: code, tests, docs, config, and related call sites, not just the first place it appeared.
- Verify each finished item with a concrete check (run the tests, build, lint, or inspect the output) before moving to the next, and report any failures or skipped steps faithfully with their output.
- Decide reasonable next steps independently using judgment rather than pausing to ask for confirmation on routine, reversible work.
- Keep outward-facing, destructive, or irreversible actions (pushing, publishing, sending messages, deleting or overwriting data, deploying, spending beyond budget) behind explicit user approval; if the next item requires one, finish everything else first, then ask for just that grant.
- Stop only when all outstanding items are done and verified, or when the remaining ones are blocked on something only the user can provide, and then state exactly what is blocked and why.
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
- (audit self) `recorded as a standing rule with fm decide --cites and a check (the drive's tests: test_drive_side, test_hooks.Stop); the drive is on` → no findings [tree 255e2fab14f1] (2026-11-03T04:47:17Z)
## Log
- 2026-11-03T04:44:23Z created
- 2026-11-03T04:47:21Z done
## Follow-ups captured
