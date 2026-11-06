---
id: T-2902
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T06:15:37Z
updated: 2026-11-04T06:15:37Z
steer_method_rate: 0.218
---
# Run the continued genesis and moons implementation workstreams concurrently with the…
## Raw request
> can you run the continued genesis/moons implementations along side it? so its not just that stuff? feel free to do tons of stuff in parallel
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Run the continued genesis and moons implementation workstreams concurrently with the current main task. Do not let the current task be the only thing in progress.
- Pick up each workstream from its last recorded state (plans, TODOs, notes, branches, unfinished files). Do not restart or re-plan finished parts, and state which next step each one resumes from.
- Run independent work in parallel: separate agents or tool calls for the main task, genesis, moons, and their tests, docs and verification. Serialize only where one step depends on another's output.
- Keep parallel work from colliding. Give each stream its own files or working area, avoid two streams editing the same file, and check for conflicts before merging results.
- Finish each stream completely. Cover every surface it touches: code, tests, docs, configs and any dependent call sites. Run the relevant tests or checks for each stream and report the actual results, including failures.
- Act without asking for step-by-step approval on local, reversible work (reading, editing, building, testing). Pause for the user's explicit grant before anything outward-facing, destructive or irreversible: pushes, publishing, deploys, deleting or overwriting files, and spending beyond the remainin…
- Track spend against the budget ($200 remaining). Scale parallelism to stay within it and say so if the plan would exceed it.
- Report each stream separately: what was done, what was verified, what is blocked or skipped, and what is next. Do not merge them into one summary that hides a stalled stream.
- Treat this as the default way of working from now on. When the main task is active, check whether genesis and moons have pending continuation work and run it alongside.
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
- 2026-11-04T06:15:37Z created
## Follow-ups captured
