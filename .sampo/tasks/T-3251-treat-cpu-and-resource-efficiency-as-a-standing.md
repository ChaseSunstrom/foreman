---
id: T-3251
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T00:06:15Z
updated: 2026-11-06T00:06:15Z
steer_method_rate: 0.218
---
# Treat CPU and resource efficiency as a standing requirement on all work in the harness:…
## Raw request
> how can we make it so what youre doing doesnt eat up the entire CPU, and is much more efficient? without losing speed/quality, and actually even faster
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat CPU and resource efficiency as a standing requirement on all work in the harness: the agent's own processes, the commands it runs, and the builds, tests, searches and scripts it launches. Act on it by default rather than only advising.
- Measure before optimizing. Record a baseline (wall-clock time, peak CPU %, core count used, peak memory) for the heavy operations, then re-measure after each change. Keep a change only if the numbers show the same or better speed and the same or better quality.
- Never trade away quality for lower CPU use. Tests, type checks, lint and review depth must stay as strict as before. Verify this by comparing results (same pass/fail set, same outputs) before and after each optimization.
- Run independent tool calls and subtasks in parallel, but cap concurrency to the machine (for example, at most cores minus one, or a bounded worker pool). Don't spawn unbounded processes, threads or sub-agents.
- Lower the priority of heavy background work (`nice`/`ionice` or an equivalent) so the user's machine stays responsive. Foreground interactive work keeps normal priority.
- Do less redundant work:
- Prefer the dedicated file and search tools, scoped to the relevant paths, over broad shell scans.
- Exclude `node_modules`, build output and VCS directories from searches.
- Don't re-read, re-run or re-derive anything already established in the session.
- Use incremental and cached execution:
- Run only the affected tests, builds and checks for the change at hand.
- Enable build and test caches.
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
- 2026-11-06T00:06:15Z created
## Follow-ups captured
