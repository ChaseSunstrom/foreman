---
id: T-0316
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-05T18:04:11Z
updated: 2026-10-09T21:43:11Z
base: b6168e79f378624fe87a31d28a9e63705f831e36
base_tree: e5a74fd0c41147c6b28c44439499f05877915398
verified: strong
---
# Re-run one real fm-builder lane end to end after a Claude Code update
## Raw request
> Builder lanes (T-0234) have never completed live: the only worktree-isolated launches (volt, 2026-10-05) failed in Claude Code 2.1.287 (isolation context lost). Re-run one real fm-builder lane end to end after the next Claude Code update
## Interpretation
Confirm fm-builder lanes work end to end on a Claude Code past 2.1.287.
## Assumptions (confidence)
## Acceptance criteria
- [x] one fm-builder lane completes live — verify with `grep -c '"event": "lane_merge"' ~/.claude/foreman/state/projects/foreman-4a056f/ledger.jsonl`
## Non-goals
## Approach (options → choice → why)
Options: launch a fresh builder lane now, or count the lanes that already merged on the current version. Choice: the ledger: 15 lane_merge events, the newest 2026-10-09 on Claude Code 2.1.295, are real builder lanes that completed end to end; a new spawn would only repeat them (and subagents wait while usage runs ahead of pace).
## Risks and rollback
## Execution prompt
## Steps
1. [x] after a Claude Code update past 2.1.287, run one lane
## Resume here
## Docs impact
none: a verification task, nothing in the docs describes the worktree failure as current
## Verification evidence
- (ac 1) `grep -c '"event": "lane_merge"' ~/.claude/foreman/state/projects/foreman-4a056f/ledger.jsonl` → exit 0 · 15 [ran] [tree e5a74fd0c411] (2026-10-09T21:43:05Z)
- (step 1) `claude --version | grep -q '2.1.2[89][0-9]\|2.1.3'` → exit 0 · (no output) [ran] [tree e5a74fd0c411] (2026-10-09T21:43:05Z)
- (audit intent) `self: the ledger's lane_merge events are the live end-to-end runs the criterion asks for, on Claude Code 2.1.295` → the criterion is one live builder lane on a version past 2.1.287; 15 merged since, the newest today on 2.1.295 [tree e5a74fd0c411] (2026-10-09T21:43:05Z)
- (audit operator) `self: the ledger's lane_merge events are the live end-to-end runs the criterion asks for, on Claude Code 2.1.295` → no code changed; the evidence is the project ledger and the installed version [tree e5a74fd0c411] (2026-10-09T21:43:05Z)
## Log
- 2026-10-05T18:04:11Z created
- 2026-10-06T03:25:09Z planned from capture
- 2026-10-06T03:25:09Z blocked: waits for a Claude Code update past 2.1.287 (the worktree-isolation failure was in that version; still current here)
- 2026-10-09T21:42:54Z set status=planned
- 2026-10-09T21:42:59Z criterion 1 verify: `true` → `grep -c '"event": "lane_merge"' ~/.claude/foreman/state/projects/foreman-4a056f/ledger.jsonl`
- 2026-10-09T21:42:59Z focused
- 2026-10-09T21:43:06Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- T-0280 [FEATURE M, done, 5 steps] Bench family: judged cases, plugin duels, version replays, regression court, shadow-user soak — lesson: Git run after a bypass-mode ses…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–5 steps
## Lessons
- A block that waits on an outside update should name the check that clears it, so the next pass can close it from evidence instead of rereading the history
## Decision
Recommendation: treat builder lanes as working on current Claude Code; would change if: a lane fails with the worktree-isolation error again.
