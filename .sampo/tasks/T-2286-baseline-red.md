---
id: T-2286
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T06:36:26Z
updated: 2026-10-31T06:39:16Z
baseline: true
---
# Baseline red:…
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_genesis.GenesisCheck.test_a_verb_whose_module_a_reached_verbs_module_imports_is_reached. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
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
- 2026-10-31T06:36:26Z created
- 2026-10-31T06:39:16Z dropped: same failure as T-2283 (fixed there), filed by fm ship's scratch run with the interpreter's full path, so the dedupe by command text missed it
## Follow-ups captured
