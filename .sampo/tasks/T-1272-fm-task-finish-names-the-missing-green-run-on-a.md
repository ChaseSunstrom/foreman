---
id: T-1272
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-20T14:29:02Z
updated: 2026-10-20T18:32:51Z
base: c7239b58bd3ac05cfb38267a3cb4608ef9135b56
base_tree: 7663d52b7c85aa09b4b0a96a3fde65f2cb6aba03
plan0_at: 2026-10-20T18:18:29Z
plan0_scope: []
verified: strong
---
# fm task finish names the missing green run: a step whose last run failed says so and how to record a passing one
## Raw request
> fm task finish names the missing green run on a red step: a step whose last run failed says 'its last run failed; record a passing run (fm task evidence ID --step N --run CMD)' instead of 'no verify command or evidence' (fmcli.py:928-943)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finish refused over a step whose only or latest run failed names that step as 'its last run failed' with the fm task evidence --step N --run command, while a step with no evidence at all keeps today's message — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a red-only step's refusal names the failed run and the command
2. [x] Split missing steps by has_evidence in fmcli's finish gaps (around fmcli.py:928-943); changelog
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping 2>&1 | grep -B3 -A8 Error | head -30` → ✗ exit 1 · FAILED (failures=1) / Ran 14 tests in 6.0s (8 classes, 16 at a time; slowest: StepEvidence 6s, CommitOwnFiles 5s, CommitAfterFocus 4s) [ran] [tree cfe03a655b3e] (2026-10-20T18:19:11Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 14 tests in 6.5s (8 classes, 16 at a time; slowest: StepEvidence 6s, CommitOwnFiles 5s, CommitAfterFocus 4s) / OK [ran] [tree 72158fc6721d] (2026-10-20T18:21:18Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 14 tests in 3.0s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree e7a64136a453] (2026-10-20T18:29:22Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 14 tests in 3.0s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree a79995174c3e] (2026-10-20T18:29:31Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 14 tests in 3.0s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree a79995174c3e] (2026-10-20T18:30:38Z)
- (audit intent) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → a red step says its last run failed with the evidence command; a bare step keeps 'no verify command or evidence' (FinishGaps test) [tree a79995174c3e] (2026-10-20T18:30:38Z)
- (audit adversary) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → message text only; the brief is read, nothing written [tree a79995174c3e] (2026-10-20T18:30:38Z)
- (audit edge) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → red means evidence present and closes() false; a red run followed by a pass of the same command closes as before [tree a79995174c3e] (2026-10-20T18:30:38Z)
- (audit operator) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → the message names both ways to close it: fm task evidence --step N --run CMD, or finish with --run CMD [tree a79995174c3e] (2026-10-20T18:30:38Z)
- (audit maintainer) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → one comprehension per kind of gap; the step text fitted to 50 chars [tree a79995174c3e] (2026-10-20T18:30:38Z)
- (audit self) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → no findings [tree a79995174c3e] (2026-10-20T18:30:38Z)
- `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 14 tests in 3.5s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a79995174c3e] (2026-10-20T18:31:48Z)
- `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 14 tests in 3.0s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree a79995174c3e] (2026-10-20T18:31:48Z)
- (audit intent) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → a red step says its last run failed with the evidence command; a bare step keeps 'no verify command or evidence' (FinishGaps test) [tree a79995174c3e] (2026-10-20T18:31:53Z)
- (audit adversary) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → message text only; the brief is read, nothing written [tree a79995174c3e] (2026-10-20T18:31:53Z)
- (audit edge) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → red means evidence present and closes() false; a red run followed by a pass of the same command closes as before [tree a79995174c3e] (2026-10-20T18:31:53Z)
- (audit operator) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → the message names both ways to close it: fm task evidence --step N --run CMD, or finish with --run CMD [tree a79995174c3e] (2026-10-20T18:31:53Z)
- (audit maintainer) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → one comprehension per kind of gap; the step text fitted to 50 chars [tree a79995174c3e] (2026-10-20T18:31:53Z)
- (audit self) `one fm-reviewer pass over the branch (intent, adversary, edge, operator, maintainer): merge as is; its two nits applied (finish --run named as the other way, a test spacing)` → no findings [tree a79995174c3e] (2026-10-20T18:31:53Z)
## Log
- 2026-10-20T14:29:02Z created
- 2026-10-20T17:26:02Z planned from capture
- 2026-10-20T18:18:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1272.builder.md
- 2026-10-20T18:18:29Z focused
- 2026-10-20T18:29:08Z merged worktree-agent-aa12e7f2c7db1d305 (2 file(s))
- 2026-10-20T18:29:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa12e7f2c7db1d305
- 2026-10-20T18:29:15Z focused
- 2026-10-20T18:32:50Z done
- 2026-10-20T18:32:51Z committed a3d32d04 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- T-0165 [FEATURE S, done, 3 steps] A step whose newest run failed closes when the same command passed later (the red run of red→green) — lesson: Evidence rules should fol…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Lessons
- A refusal that names the failing thing and the command to fix it saves a round trip; a generic 'no evidence' when there is red evidence sends the agent the wrong way
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/lib/fmsecrets.py
- plugin/tests/test_secrets.py
