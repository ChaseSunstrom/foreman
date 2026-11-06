---
id: T-3098
type: FIX
tier: S
status: planned
priority: normal
scope: [models.json]
depends_on: []
source: user
created: 2026-11-05T02:56:26Z
updated: 2026-11-06T03:52:28Z
base: 01efe2f47203ca5bc96c047078c7834e8c6bc86a
---
# mimo-v2.6:9b is back and answers; gpu-lfm3 is dropped until Ollama loads the lfm3 architecture
## Raw request
> mimo-v2.6:9b is back and answers; gpu-lfm3 is dropped until Ollama loads the lfm3 architecture
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] mimo-v2.6:9b is in Ollama and answers a one-line prompt; models.json has no gpu-lfm3 profile (Ollama 0.40.11: unknown model architecture 'lfm3'; the GGUF stays listed for a later Ollama) — verify with `curl -sf -m 180 localhost:11434/api/generate -d '{"model":"mimo-v2.6:9b","prompt":"Say ok.","stream":false,"think":false,"options":{"num_predict":8}}' | grep -q response && ! grep -q gpu-lfm3 ~/.claude/foreman/models.json`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] drop the gpu-lfm3 line from models.json; check mimo answers  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T02:56:26Z created
- 2026-11-05T02:56:26Z redo of T-3013: takes over its start point and edited files
- 2026-11-05T02:56:30Z set approved=True
- 2026-11-05T02:56:30Z set scope=['models.json']
- 2026-11-05T02:56:30Z blocked: after T-3006's close (one close at a time); a one-line models.json edit
- 2026-11-06T03:52:28Z unblocked
## Follow-ups captured
