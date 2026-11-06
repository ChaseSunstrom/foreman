---
id: T-0948
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:44:24Z
updated: 2026-10-15T21:07:25Z
base: be49e40e65cbccf95241658c4347b7809e6d3807
base_tree: b5a7ea781065bde3d246b9cbb283b234d37b19d8
verified: strong
---
# Enforce: fm lane merge re-runs the lane task's criteria in the worktree and refuses red
## Raw request
> Enforce: fm lane merge re-runs the lane task's criteria in the worktree and refuses red
## Interpretation
Part of T-0942. fmlanes.merge (fmlanes.py ~203) merges a builder's branch on the builder's word. Before git merge, it now runs each criterion's verify command (the brief's '— verify with' lines) with cwd at the lane worktree, under the same timeout fm task evidence uses. A non-zero exit refuses the merge with the command and its last lines. fm lane merge --unverified 'REASON' merges anyway and logs a ledger event with the reason.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane merge runs each criterion's verify command (from the brief, the same runner fm task evidence --run uses, without recording evidence) in the lane worktree before git merge; a non-zero exit refuses with the command and its last 15 lines; a brief with no runnable criterion refuses too ('plan verify commands first') — verify with `python3 plugin/tests/run.py -k test_merge_refuses_red`
- [x] fm lane merge --unverified REASON refuses an empty or blank reason, writes the ledger event before merging, and is refused when run from inside a lane worktree (a builder can't waive its own gate) — verify with `python3 plugin/tests/run.py -k test_unverified_guardrails`
## Non-goals
## Approach (options → choice → why)
Options: (A) the hook or the fm verb does the step itself, so no agent has to remember it (chosen; T-0942 brainstorm research/brainstorm-20261015-154016); (B) stronger instructions in rules and skills (what failed: 19 card writers were told to lint and didn't); (C) a supervising reviewer agent per task (costly, and still an agent); (D) a per-repo enforce.toml policy file (later, if the meta registry outgrows itself). Reuse whatever runs verify commands for fm task evidence --run, so the merge gate and the evidence agree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing LaneMergeGate tests
2. [x] Run criteria in fmlanes.merge before git merge; the escape flag
3. [x] Docs: delegate reference and MASTER
4. [x] Locate the verify runner behind fm task evidence --run; extract a no-record call if it's entangled
## Resume here
## Docs impact
MASTER.md lanes line and plugin/skills/intake/references/delegate.md: merge re-runs criteria, --unverified from the main thread only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k LaneMergeGate` → ✗ exit 1 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / FAILED (1 classes) [ran] [tree 575b100a3481] (2026-10-15T20:51:59Z)
- (step 2) `python3 plugin/tests/run.py -k LaneMergeGate` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / OK [ran] [tree 713077d8fac5] (2026-10-15T20:53:27Z)
- (step 3) `grep -c T-0948 MASTER.md plugin/skills/intake/references/delegate.md` → exit 0 · MASTER.md:1 / plugin/skills/intake/references/delegate.md:1 [ran] [tree 713077d8fac5] (2026-10-15T20:53:27Z)
- (step 4) `grep -n 'c.run_command(wt, cmd, 600)' plugin/lib/fmlanes.py` → exit 0 · 220:        code, out = c.run_command(wt, cmd, 600) [ran] [tree 713077d8fac5] (2026-10-15T20:53:27Z)
- (ac 1) `python3 plugin/tests/run.py -k test_merge_refuses_red` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / OK [ran] [tree e71b6354828e] (2026-10-15T21:07:08Z)
- (ac 2) `python3 plugin/tests/run.py -k test_unverified_guardrails` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / OK [ran] [tree e71b6354828e] (2026-10-15T21:07:09Z)
- `python3 plugin/tests/run.py -k LaneMergeGate` → ✗ exit 1 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e71b6354828e] (2026-10-15T21:07:22Z)
- `python3 plugin/tests/run.py -k LaneMergeGate` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / OK [ran] [tree e71b6354828e] (2026-10-15T21:07:22Z)
- (ac 1) `python3 plugin/tests/run.py -k test_merge_refuses_red` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / OK [ran] [tree e71b6354828e] (2026-10-15T21:07:24Z)
- (ac 2) `python3 plugin/tests/run.py -k test_unverified_guardrails` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: LaneMergeGate 1s) / OK [ran] [tree e71b6354828e] (2026-10-15T21:07:24Z)
- (audit intent) `main-thread review of fmlanes._verify and the --unverified guard; criteria re-run on the merged tree` → ok: a builder's claim no longer decides a merge; the brief's verify commands do, run in the lane worktree [tree e71b6354828e] (2026-10-15T21:07:24Z)
- (audit adversary) `main-thread review of fmlanes._verify and the --unverified guard; criteria re-run on the merged tree` → ok: --unverified needs a non-blank reason, is refused inside a lane, and is ledgered before the merge [tree e71b6354828e] (2026-10-15T21:07:24Z)
- (audit edge) `main-thread review of fmlanes._verify and the --unverified guard; criteria re-run on the merged tree` → ok: a brief with nothing to run refuses; a missing worktree refuses; output cut to 15 lines [tree e71b6354828e] (2026-10-15T21:07:24Z)
- (audit operator) `main-thread review of fmlanes._verify and the --unverified guard; criteria re-run on the merged tree` → ok: the refusal names the command, its exit and the way to waive it [tree e71b6354828e] (2026-10-15T21:07:24Z)
- (audit maintainer) `main-thread review of fmlanes._verify and the --unverified guard; criteria re-run on the merged tree` → ok: reuses c.run_command (the evidence runner), no new runner [tree e71b6354828e] (2026-10-15T21:07:24Z)
## Log
- 2026-10-15T20:44:24Z created
- 2026-10-15T20:49:05Z criterion 1 verify: `python3 plugin/tests/run.py -k LaneMergeGate` → `python3 plugin/tests/run.py -k test_merge_refuses_red`
- 2026-10-15T20:49:05Z criterion 1 text: fm lane merge runs each criterion's verify command in the lane worktree first and refuses with the failing output when one exits non-zero; --unverified REASON merges anyway and logs the reason → fm lane merge runs each criterion's verify command (from the brief, the same runner fm task evidence --run uses, without recording evidence) in the lane worktree before git merge; a non-zero exit refuses with the command and its last 15 lines; a brief with no runnable criterion refuses too ('plan verify commands first')
- 2026-10-15T20:49:05Z criterion 2 verify: `python3 plugin/tests/run.py -k LaneMergeGate` → `python3 plugin/tests/run.py -k test_unverified_guardrails`
- 2026-10-15T20:49:05Z criterion 2 text: A builder that claims green but leaves a red criterion cannot be merged → fm lane merge --unverified REASON refuses an empty or blank reason, writes the ledger event before merging, and is refused when run from inside a lane worktree (a builder can't waive its own gate)
- 2026-10-15T20:49:06Z second read (revise) addressed: criteria source, vacuous case refused, --unverified guardrails, distinct tests; post-merge re-run on main stays the main thread's step
- 2026-10-15T20:50:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0948.builder.md
- 2026-10-15T20:51:01Z focused
- 2026-10-15T21:07:01Z merged worktree-agent-af6f387fbc93d2c55 (5 file(s))
- 2026-10-15T21:07:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af6f387fbc93d2c55
- 2026-10-15T21:07:07Z focused
- 2026-10-15T21:07:25Z done
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Running verify commands in the lane worktree executes arbitrary builder-authored commands (the criteria in the brief, which the builder may have edited) with the merger's privileges, and the code under test is the builder's own. The plan doesn't say whether criteria come from the task record …
- HIGH: The "red" definition is thin. A task with zero parseable verify commands, a criterion with no "— verify with" line, or a command that is unparseable would pass vacuously. That is exactly the "claims green" hole the task is meant to close. — Specify the behavior: a criterion with no verify com…
- MEDIUM: Merge ordering and state. Verification runs in the worktree, but the merge lands on the target branch. If other lanes have merged since, the worktree result may differ from post-merge reality, and the plan doesn't say what is on disk if verification leaves artifacts, a dirty tree, or a time…
- MEDIUM: `--unverified REASON` needs guardrails. The ledger event should be written before the merge, or atomically with it, so a merge cannot happen without its record. An empty or whitespace reason should be rejected. Also, who may pass it? A builder agent could call it itself. — Reject empty reas…
- MEDIUM: "Reuse whatever runs verify commands for `fm task evidence --run`" is unresolved. If that code is entangled with evidence recording, the reuse may either record evidence as a side effect or force a refactor. The plan has no step to locate and extract it. — Add a step 1.5: identify the share…
- LOW: The acceptance criteria both verify with the same `-k LaneMergeGate` command, so the second criterion proves nothing separate, and the tests don't yet exist. Failure output must also show "the command and its last lines," but no test is specified for that. — Name distinct tests per criterion (…
Verdict: revise — the core approach is sound, but the criteria source, the vacuous-pass case, and the `--unverified` guardrails must be decided before the tests are written, or the gate can be bypassed.
## Dissent
- [ ] HIGH: Running verify commands in the lane worktree executes arbitrary builder-authored commands (the criteria in the brief, which the builder may have edited) with the merger's privileges, and the code under test is the builder's own. The plan doesn't say whether criteria come from the task record …
- [ ] HIGH: The "red" definition is thin. A task with zero parseable verify commands, a criterion with no "— verify with" line, or a command that is unparseable would pass vacuously. That is exactly the "claims green" hole the task is meant to close. — Specify the behavior: a criterion with no verify com…
- [ ] MEDIUM: Merge ordering and state. Verification runs in the worktree, but the merge lands on the target branch. If other lanes have merged since, the worktree result may differ from post-merge reality, and the plan doesn't say what is on disk if verification leaves artifacts, a dirty tree, or a time…
- [ ] MEDIUM: `--unverified REASON` needs guardrails. The ledger event should be written before the merge, or atomically with it, so a merge cannot happen without its record. An empty or whitespace reason should be rejected. Also, who may pass it? A builder agent could call it itself. — Reject empty reas…
- [ ] MEDIUM: "Reuse whatever runs verify commands for `fm task evidence --run`" is unresolved. If that code is entangled with evidence recording, the reuse may either record evidence as a side effect or force a refactor. The plan has no step to locate and extract it. — Add a step 1.5: identify the share…
- [ ] LOW: The acceptance criteria both verify with the same `-k LaneMergeGate` command, so the second criterion proves nothing separate, and the tests don't yet exist. Failure output must also show "the command and its last lines," but no test is specified for that. — Name distinct tests per criterion (…
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0234 [FEATURE L, done, 4 steps] Implementation subagents in lane worktrees — a foreman:fm-builder agent (Edit/Write/Bash) — lesson: A contract a subagent must keep nee…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Lessons
- Gate merges on the work's own criteria re-run where the work lives; an agent's report is a hint, the exit code is the fact.
## Plan gaps
- failed first: step 1 Failing LaneMergeGate tests
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/skills/intake/references/delegate.md
