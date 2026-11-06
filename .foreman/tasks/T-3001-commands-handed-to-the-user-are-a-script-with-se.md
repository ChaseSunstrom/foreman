---
id: T-3001
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-04T18:52:01Z
updated: 2026-11-06T03:53:05Z
---
# A reply that hands the user a shell block with an irreversible step is held once unless it is a set -euo pipefail script with a check before that step
## Raw request
> Commands handed to the user are a script with set -euo pipefail and a check before every irreversible step, never a paste block that ends in rm: the Ollama move's paste block ran with rsync missing, moved the store aside and its last line deleted it (72 GB of models lost, re-pullable); a lesson for the firewall (T-2992's classes) and a Ward-style lint on suggested commands
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the Stop hook holds once (per reply) a reply whose fenced shell block has an irreversible step (rm, a mv or rsync --delete of a directory, dd, mkfs, git reset --hard, git clean, DROP) without set -euo pipefail at its top or without a test/check line before that step, naming the step and the script shape; a block that is that script, or has no irreversible step, passes — verify with `python3 plugin/tests/run.py test_hooks`
- [ ] the lesson is a standing rule: decisions.md carries 'commands handed to the user are a script with set -euo pipefail and a check before every irreversible step, never a paste block that ends in rm' (T-3001) — verify with `grep -q 'never a paste block that ends in rm' ~/.claude/foreman/state/projects/foreman-4a056f/decisions.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: the Ollama-move block (rsync then rm -rf) held; the same as a set -euo pipefail script with a test -d check passes; a block with no irreversible step passes; held once  <- CURRENT
2. [ ] the paste gate in hooks.py beside _claims_gate, and the standing decision
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T18:52:01Z created
- 2026-11-05T02:41:07Z planned from capture
- 2026-11-05T02:41:08Z set approved=True
- 2026-11-05T02:41:08Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-11-05T02:41:08Z blocked: planned and approved; waits for a builder slot
- 2026-11-06T03:53:05Z unblocked
## Follow-ups captured
