---
id: T-3033
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T23:44:44Z
updated: 2026-11-04T23:44:44Z
steer_method_rate: 0.218
---
# Build a graph / neural-net-style visualization mode in Sampo that shows the agents,…
## Raw request
> can you have a graph/neural net like visualization mode for the different agents/models/tools working together? on the local/website? etc.? also keep going on genesiss while all of the otehr stuff is going, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Build a graph / neural-net-style visualization mode in Sampo that shows the agents, models and tools working together as nodes, with edges for delegation, messages, tool calls and data flow.
- Make it live: node and edge state (idle, running, waiting, failed, done) updates as events happen, and edges show direction and activity. Include which model or tool each node is, plus basic cost, token and latency numbers.
- Let the user click a node or edge to see its inputs, outputs, status and logs. Support zoom, pan, filter by agent, model or tool, and a replay of a finished run.
- Ship it on every surface Sampo has: the local app or CLI-launched view first, then the website. All surfaces share one event source and one graph data model, so they never diverge.
- Treat the visualization as optional. It must not slow down or change how agents run, and the existing views stay available as the default.
- Cover it with tests and checks: graph-model unit tests, a rendering or snapshot check, and a run with several agents and tools that confirms the graph matches what actually happened. Update the docs and screenshots to match.
- Keep working on Genesis (the user's "genesiss") continuously, in parallel with the visualization work and all other running tasks. Don't pause it, drop it or wait for the other work to finish.
- Keep Genesis and the visualization work from interfering with each other: separate branches or workspaces, no shared-file clobbering, and a short status note on each at every checkpoint.
- Act on this instead of proposing it. Make reasonable design choices yourself and report what you did, what you verified and what is still open.
- Keep anything outward-facing or irreversible behind the user's explicit grant. That covers deploying or publishing to the live website, pushing, spending money, and deleting or overwriting data. Build and verify locally until that grant exists.
- Don't ship anything that leaks secrets, prompts or private data into the visualization or the public website. Redact or gate the node details shown there.
- If a surface, the Genesis scope, or a test can't be completed, say so plainly instead of reporting the work as finished.
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
- 2026-11-04T23:44:44Z created
## Follow-ups captured
