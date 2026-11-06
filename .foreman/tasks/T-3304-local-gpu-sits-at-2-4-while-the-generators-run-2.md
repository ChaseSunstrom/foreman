---
id: T-3304
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T03:55:57Z
updated: 2026-11-06T03:55:57Z
---
# Local GPU sits at 2-4% while the generators run (2026-11-06): the moons funnel's…
## Raw request
> Local GPU sits at 2-4% while the generators run (2026-11-06): the moons funnel's kill/tier judging and generation call the remote Jarvis 27B, the local Ollama (mimo-v2.6:9b, 100% GPU) serves one request at a time (system service, -np 1), and the generator clients ran at idle CPU priority. Route each funnel stage and the card writer to whichever endpoint is idle (local GPU and Jarvis together, measured by queue depth), add a user-level parallel server (llama-server from the installed Ollama, or Jeff) when Ollama's slot is busy, and show GPU utilisation next to the generators on the live page
## Interpretation
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
- 2026-11-06T03:55:57Z created
## Follow-ups captured
