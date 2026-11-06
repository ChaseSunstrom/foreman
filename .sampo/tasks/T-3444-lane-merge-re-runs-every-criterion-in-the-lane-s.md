---
id: T-3444
type: PERFORMANCE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T14:57:44Z
updated: 2026-11-06T14:58:15Z
lane: ~/.claude/foreman.lanes/T-3444
---
# Lane merge re-runs every criterion in the lane serially while the merge queue waits (4…
## Raw request
> PERF: lane merge re-runs every criterion in the lane serially while the merge queue waits (4 min at load 15, 16 min at load 100, per lane, 80 lanes queued). Record each criterion pass keyed by the lane's clean tip tree, reuse it at merge when the tree is unchanged, and add a precheck action (sampo lane precheck ID...) a queue runner can run ahead in parallel for the next lanes, so the serial merge only does git merge + the close
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] merge reuses a criterion pass recorded on the same clean lane tree and re-runs it after the lane changes or with tracked edits; sampo lane precheck ID records passes without merging — verify with `python3 plugin/tests/run.py test_lanes.LanePrecheck`
## Non-goals
## Approach (options → choice → why)
Complete version: a criterion pass is recorded on the brief keyed by the lane's tip tree and the command, only when the lane has no tracked changes; merge reuses a pass on the same clean tree (saying so) and re-runs anything else; sampo lane precheck ID runs the same verify ahead and records, so a queue runner can check the next lanes in parallel while one merge lands. Rivals: (1) reuse the builder's own evidence runs (no extra run, but evidence is per step and its command often differs from the criterion's); (2) a separate state file of passes (more code, no gain over the brief's meta); (3) merge trains (one gate for N, but bisecting on load reds made them slower tonight). Chosen: the brief record plus precheck; (1) captured as a later gain.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] _verify records and reuses passes keyed by tree; lane precheck action; tests red first  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T14:57:44Z created
- 2026-11-06T14:58:13Z set tier=M
- 2026-11-06T14:58:14Z planned: it has criteria and steps
- 2026-11-06T14:58:15Z lane: ~/.claude/foreman.lanes/T-3444 on foreman/T-3444
## Follow-ups captured
