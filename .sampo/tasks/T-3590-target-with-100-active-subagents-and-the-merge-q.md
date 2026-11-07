---
id: T-3590
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-07T03:28:12Z
updated: 2026-11-07T03:28:12Z
steer_method_rate: 0.218
---
# **Target:** With 100 active subagents and the merge queue running, total CPU use stays…
## Raw request
> can you keep super improving the performance/effeciency? I want to be at max 10% CPU usage across 100 active subagents/merge queue, I don't want my CPU to be pegged at 100%, it makes my PC unusable and its unhealthy for it, and its wasteful if it could be 1000000x more effecient and performant
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Target:** With 100 active subagents and the merge queue running, total CPU use stays at or below 10% of the machine's capacity, averaged over a sustained window. It must never sit pegged near 100%, and the PC must stay responsive while the load runs.
- **Standing work:** Keep improving CPU performance and efficiency continuously as part of normal work, not as a one-off pass. Treat any regression against the target as a defect to fix.
- **Measure first:** Build a repeatable benchmark that simulates 100 active subagents plus the merge queue. It records CPU (average, peak, per-process), memory, wakeups and process counts. Take a baseline, profile to find the real hot spots, and rank fixes by measured CPU saved. Don't optimize by gue…
- **Cover every surface:** Check and fix all of these:
- the scheduler and orchestration loop
- polling and busy-waits, replacing them with event-driven or backoff waits
- subprocess and shell spawning
- file watching and directory scans
- git operations
- build, test and lint runs, using incremental or cached runs and skipping redundant ones
- logging and output streaming
- serialization and JSON handling
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
- 2026-11-07T03:28:12Z created
## Follow-ups captured
