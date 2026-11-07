---
id: T-3483
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T18:34:00Z
updated: 2026-11-06T18:37:57Z
---
# Keep using the small local models on real work, analyse where they fall short of the…
## Raw request
> Keep using the small local models on real work, analyse where they fall short of the frontier model and keep improving Sampo until their abilities match it completely (user 2026-11-06): a standing loop that runs the local models (jarvis qwen/gemma/mimo) on real tasks and exams every round, classifies each failure, builds the scaffold that closes it (calling cards, playbooks, decompositions, verifiers), and re-measures; GPU busy, never idle
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
- 2026-11-06T18:34:00Z created
- 2026-11-06T18:37:57Z steer: split into T-3484..T-3488 from the recon: Louhi's smith arm, FAILURE_CLASSES and taxonomy, the cards bench and admit gates exist; missing are the round driver, the class→scaffold registry, the n>=30 re-measure gate, the GPU-idle fix (bench_night blocks on the moons store lock) and misses→card requests
## Follow-ups captured
