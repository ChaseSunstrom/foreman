---
id: T-2174
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T15:23:57Z
updated: 2026-10-30T16:11:06Z
done_in: T-2176
---
# Prove Foreman works outside Claude Code: an end-to-end test with no claude binary — fm…
## Raw request
> Prove Foreman works outside Claude Code: an end-to-end test with no claude binary — fm code drives a task through brief, evidence and finish on a stub model; fm install for Codex/Gemini/opencode writes working wiring; the guard and drive work without CC hooks; fix whatever breaks (user 2026-10-30: 'make sure it does work outside of CC')
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
- 2026-10-30T15:23:57Z created
- 2026-10-30T15:26:41Z found: install.sh:43 dies when 'claude' isn't on PATH, and lines 102-106 install only the CC plugin; without claude it should skip the CC wiring, put fm on PATH and point at fm agents install / fm code. Default home ~/.claude/foreman is CC-flavoured too (FOREMAN_HOME overrides)
- 2026-10-30T15:32:02Z batched into T-2176
- 2026-10-30T16:11:06Z done in T-2176 (batch)
## Follow-ups captured
