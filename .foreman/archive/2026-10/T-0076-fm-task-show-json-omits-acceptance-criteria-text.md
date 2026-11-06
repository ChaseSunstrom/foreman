---
id: T-0076
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-09-27T06:30:08Z
updated: 2026-10-02T19:01:08Z
done_in: T-0088
---
# fm ui --json: one view-model snapshot for every surface (incl. steps, criteria, depends)
## Raw request
> fm task show --json omits acceptance criteria (text+verify), steps and depends; an external orchestrator (jarvis-code) must parse the brief markdown — evidence: jarvis-code src/tasks.ts readBrief()
## Interpretation
Surfaces (the new mod, fm watch, external orchestrators like jarvis-code) each re-derive Foreman state; give them one JSON snapshot from one fm call, and make fm task show --json carry steps, criteria and depends.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm ui --json emits project, mode, active (steps, criteria with checked, audits, gates), next, queue, inbox, approvals, recent, health; fm task show --json includes steps/criteria/depends — verify with `python3 -m unittest discover -s plugin/tests -p test_ui.py -q`
- [ ] outside a Foreman project fm ui --json exits 0 with project null — verify with `python3 -m unittest discover -s plugin/tests -p test_ui.py -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) new fm ui --json built on fmwatch.gather + a shared brief_json(b) helper; (b) extend fm state --json with everything. Choice: (a). Why: state --json is a stable contract others parse; ui is a render model that can grow; gather() already collects most of it (one source).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red contract tests  <- CURRENT
2. [ ] brief_json helper (steps/criteria/depends) used by task show and ui
3. [ ] fm ui command reusing fmwatch.gather
4. [ ] docs: MASTER CLI line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-09-27T06:30:08Z created
- 2026-10-02T18:34:56Z planned from capture
- 2026-10-02T19:01:08Z done in T-0088
## Follow-ups captured
