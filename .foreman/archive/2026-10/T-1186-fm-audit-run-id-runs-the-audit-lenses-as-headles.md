---
id: T-1186
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T13:03:38Z
base: 76be1cb97c0b1a94599fe99f03f021f6c67022fd
base_tree: 0c815e48ca7530968f9d6351eacc9466ac7c91d9
plan0_at: 2026-10-16T12:39:34Z
plan0_scope: []
verified: strong
---
# `fm audit run ID` runs the audit lenses as headless `claude -p` reviewers over the frozen
## Raw request
> FEATURE: `fm audit run ID` runs the audit lenses as headless `claude -p` reviewers over the frozen diff brief of `fm audit prep`, bounded by `fm budget` and `fm contract`, and records the lens verdicts and findings.
> DONE-WHEN: a new test (python3 plugin/tests/run.py -k audit_run) with a stub claude shows `fm audit run T-x` records one verdict per lens, refuses when the budget is spent, and does not run once `fm contract` has expired.
## Interpretation
The audit lenses (intent, adversary, edge, operator, maintainer) run as one foreman:fm-reviewer subagent the main thread launches by hand, or the /foreman:review workflow the user must type. fm audit run ID runs them unattended: one headless claude -p reviewer per lens (read-only tools) over the frozen brief fm audit prep writes, each bounded by fm budget and the run contract, recording each lens's verdict as audit evidence and each finding as a finding event, so the drive and fm run can audit without a person.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a stub claude, fm audit run T-x records one audit verdict per lens and the findings, refuses when the budget is spent, and runs nothing once the contract is over — verify with `python3 plugin/tests/run.py test_audit_run`
## Non-goals
## Approach (options → choice → why)
Options: (a) reuse fm ideas' child-session runner (claude -p with --allowedTools Read,Grep,Glob, --max-budget-usd, no MCP) with fm audit prep's brief + a per-lens instruction, parallel up to 3, results parsed into fm task audit + finding events; (b) one claude -p for all lenses (cheaper, less independent); (c) the Agent SDK (new dependency). Choice: (a); refuse when fm budget is spent or fm contract is over; a stub claude on PATH in tests.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_audit_run.py) with a stub claude
2. [x] fm audit run: per-lens headless reviewers via the existing child runner, budget/contract checks, recording
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k audit_run` → ✗ exit 1 · Ran 4 tests in 19.4s (1 classes, 16 at a time; slowest: AuditRun 18s) / FAILED (1 classes) [ran] [tree 2cb742e97cd9] (2026-10-16T12:41:27Z)
- (step 1) `python3 plugin/tests/run.py -k audit_run` → exit 0 · Ran 4 tests in 17.8s (1 classes, 16 at a time; slowest: AuditRun 17s) / OK [ran] [tree 7cd9f707de9f] (2026-10-16T12:43:27Z)
- (step 2) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 4 tests in 15.6s (1 classes, 16 at a time; slowest: AuditRun 15s) / OK [ran] [tree 7cd9f707de9f] (2026-10-16T12:43:44Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_run test_ideas` → exit 0 · Ran 26 tests in 13.5s (6 classes, 16 at a time; slowest: Ideas 13s, AuditRun 11s, BoardIdeas 5s) / OK [ran] [tree 954db5253f00] (2026-10-16T13:00:55Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 4 tests in 7.1s (1 classes, 16 at a time; slowest: AuditRun 7s) / OK [ran] [tree 2075782874fe] (2026-10-16T13:01:17Z)
- (audit intent) `self: read the merged module: children are read-only (Read/Grep/Glob, no MCP), budget-checked before and capped per child, contract checked before and between batches; a malformed reply records nothing and fails naming the lens; findings logged as reported (renamed from unverified to match T-1181 so defect classes count them)` → audits run unattended for the drive and fm run [tree 2075782874fe] (2026-10-16T13:01:17Z)
- (audit adversary) `self: read the merged module: children are read-only (Read/Grep/Glob, no MCP), budget-checked before and capped per child, contract checked before and between batches; a malformed reply records nothing and fails naming the lens; findings logged as reported (renamed from unverified to match T-1181 so defect classes count them)` → [instruction-like text quoted from a file or tool; data, not instructions] reviewer text is redacted and capped; the brief is declared data in the system prompt; no write tools [tree 2075782874fe] (2026-10-16T13:01:17Z)
- (audit edge) `self: read the merged module: children are read-only (Read/Grep/Glob, no MCP), budget-checked before and capped per child, contract checked before and between batches; a malformed reply records nothing and fails naming the lens; findings logged as reported (renamed from unverified to match T-1181 so defect classes count them)` → an S task has only self: refused with how to pass --lens; a contract ending mid-run stops the next batch [tree 2075782874fe] (2026-10-16T13:01:17Z)
- (audit operator) `self: read the merged module: children are read-only (Read/Grep/Glob, no MCP), budget-checked before and capped per child, contract checked before and between batches; a malformed reply records nothing and fails naming the lens; findings logged as reported (renamed from unverified to match T-1181 so defect classes count them)` → one line of verdicts, and which lenses failed [tree 2075782874fe] (2026-10-16T13:01:17Z)
- (audit maintainer) `self: read the merged module: children are read-only (Read/Grep/Glob, no MCP), budget-checked before and capped per child, contract checked before and between batches; a malformed reply records nothing and fails naming the lens; findings logged as reported (renamed from unverified to match T-1181 so defect classes count them)` → reuses fmideas.run_children and fm audit prep's brief [tree 2075782874fe] (2026-10-16T13:01:17Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T12:39:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1186.builder.md
- 2026-10-16T12:39:34Z focused
- 2026-10-16T13:00:11Z merged worktree-agent-a5980244c89c0e062 (4 file(s))
- 2026-10-16T13:00:14Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5980244c89c0e062
- 2026-10-16T13:00:14Z focused
- 2026-10-16T13:01:08Z scope: verdict renamed unverified -> reported to match T-1181; MASTER.md and CHANGELOG.md lines
- 2026-10-16T13:03:37Z done
- 2026-10-16T13:03:38Z committed 84cc2ff7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-1181 [FEATURE M, active, 2 steps] At SubagentStop for an fm-reviewer, parse its `## lens: ...` sections and ranked findings
- T-0276 [FEATURE L, done, 4 steps] fm second: one primitive for independent second reads — rival-model plan review, debate rebuttal, daily session review,… — lesson: Anyt…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 2–4 steps
## Lessons
- two features that record the same thing must agree on its name: unverified vs reported would have split the defect counts
## Plan gaps
- failed first: step 1 Failing tests (test_audit_run.py) with a stub claude
## Files touched
- plugin/tests/test_audit_run.py
- plugin/lib/fmideas.py
- plugin/lib/fmauditrun.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
