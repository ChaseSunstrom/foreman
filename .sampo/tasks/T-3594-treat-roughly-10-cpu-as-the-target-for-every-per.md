---
id: T-3594
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-07T03:34:43Z
updated: 2026-11-07T03:34:43Z
steer_method_rate: 0.218
---
# Treat roughly 10% CPU as the target for every performance or efficiency change, not as a…
## Raw request
> ok, you can max out the CPU for now, but I do want you to make it more effecient and performant, don't CAP it at 10%, but make that the goal of all performance/effeciency enhancements, also why the hell is it still so slow to merge everything? its been like an hour, and none of the CPU fixes have been merged yet
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat roughly 10% CPU as the target for every performance or efficiency change, not as a hard cap. Don't throttle, rate-limit, or sleep-pad to reach it. Get there by removing wasted work.
- Allow full CPU use for now while the fixes are pending. Lift any existing limiter, but only the one that blocks the work, and note what was lifted so it can be restored if needed.
- Find the real CPU hot spots by profiling or measuring before changing code. Cover polling loops, busy-waits, redundant recomputation, needless re-renders or re-scans, unbatched I/O, and excess process or thread spawning. Fix the biggest costs first.
- For each efficiency change, record CPU use before and after under the same workload, and compare it to the 10% target. Report the numbers, and say plainly when the target isn't met.
- Add or update tests, benchmarks, or a regression check for each fix so CPU use can't quietly climb again. Update any docs or config that describe the CPU behavior.
- Don't let efficiency work break behavior. Run the existing tests, and report any failures with their output.
- Investigate why merging is so slow. Check the queue, CI duration and failures, blocked or required reviews, merge conflicts, stale branches, and runner capacity. Report the specific cause, with evidence, for why none of the CPU fixes have merged after about an hour.
- Fix the merge blockers within your own reach, such as rebasing, resolving conflicts, re-running flaky jobs, and splitting or ordering the CPU-fix PRs. Merge only where the user's existing workflow already allows it.
- Don't bypass required checks, reviews, or branch protections, and don't force-push or force-merge. Anything outward-facing, destructive, or irreversible, including merging to the main branch, needs the user's explicit grant. If a step needs that grant, say what is waiting and ask.
- Give the user a short status that covers what was found, what changed, what is merged, what is still blocked and why, and what is needed from them.
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
- 2026-11-07T03:34:43Z created
## Follow-ups captured
