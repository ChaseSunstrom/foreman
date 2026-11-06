---
id: T-1327
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:05Z
updated: 2026-10-21T04:04:27Z
base: c2a365a9732c85ea2f30e7abcb2f1e64923e9bcb
base_tree: 153c21041504282b69645f92adaaee32a8491708
plan0_at: 2026-10-21T03:35:31Z
plan0_scope: []
verified: strong
---
# Nested Claude sessions that fm code starts run without Foreman's own session context, drive and request capture; the guard and leases stay
## Raw request
> Nested Claude sessions that fm code starts run without Foreman's own session context, drive and request capture; the guard and leases stay
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every worker and planner CLI fm code starts runs with FOREMAN_QUIET=1, so Foreman's hooks in that nested Claude session run only the guard (no session context, drive, capture or leases); a fake CLI that records its environment proves it for both — verify with `python3 plugin/tests/run.py test_code_worker`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests per event under FOREMAN_WORKER_OF=fm-code-x
2. [x] The hook dispatcher's quiet mode for nested fm code sessions
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | tail -8` → exit 0 · Ran 35 tests in 94.0s (1 classes, 16 at a time; slowest: Worker 93s) / OK [ran] [tree 507e8a3a020f] (2026-10-21T03:39:32Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | tail -8` → exit 0 · Ran 35 tests in 94.0s (1 classes, 16 at a time; slowest: Worker 93s) / OK [ran] [tree 507e8a3a020f] (2026-10-21T03:39:32Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 35 tests in 105.4s (1 classes, 16 at a time; slowest: Worker 105s) / OK [ran] [tree 07b2c5723fb3] (2026-10-21T03:59:33Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 35 tests in 109.3s (1 classes, 16 at a time; slowest: Worker 109s) / OK [ran] [tree 07b2c5723fb3] (2026-10-21T04:01:32Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 35 tests in 109.3s (1 classes, 16 at a time; slowest: Worker 109s) / OK [ran] [tree 07b2c5723fb3] (2026-10-21T04:01:32Z)
- (audit adversary) `self: read the builder's diff (two env dicts gain FOREMAN_QUIET=1; one test each for the worker and the planner path); fmhooks._quiet keeps the PreToolUse guard, so safety in the nested session is unchanged; reworded the merged comment` → the guard still runs in nested sessions (quiet exempts PreToolUse); fewer hooks can only remove context, never permission [tree 07b2c5723fb3] (2026-10-21T04:01:32Z)
- (audit edge) `self: read the builder's diff (two env dicts gain FOREMAN_QUIET=1; one test each for the worker and the planner path); fmhooks._quiet keeps the PreToolUse guard, so safety in the nested session is unchanged; reworded the merged comment` → a user's own --worker template gets the variable too, as intended: any CLI there is a nested session [tree 07b2c5723fb3] (2026-10-21T04:01:32Z)
- (audit self) `self: read the builder's diff (two env dicts gain FOREMAN_QUIET=1; one test each for the worker and the planner path); fmhooks._quiet keeps the PreToolUse guard, so safety in the nested session is unchanged; reworded the merged comment` → no findings [tree 07b2c5723fb3] (2026-10-21T04:01:32Z)
## Log
- 2026-10-21T03:24:05Z created
- 2026-10-21T03:33:37Z grounding: FOREMAN_QUIET=1 (T-0077, fmhooks._quiet) already makes every hook but the guard skip; fm code's worker env (run.work) and planner profile env (choose_profile) never set it. Plan shrinks: set FOREMAN_QUIET=1 in both; test with a fake CLI that records its environment. Leases from the worker stop (PostToolUse is quiet), which also removes T-1294's self-lease conflict at the source; the guard still runs in the worker.
- 2026-10-21T03:35:00Z set tier=S
- 2026-10-21T03:35:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1327.builder.md
- 2026-10-21T03:35:30Z focused
- 2026-10-21T03:53:11Z merged worktree-agent-af890b4d2bebd13c8 (2 file(s))
- 2026-10-21T03:57:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af890b4d2bebd13c8
- 2026-10-21T03:57:44Z focused
- 2026-10-21T03:59:41Z scope: CHANGELOG.md for the release note; plugin/tests/test_code_worker.py holds the tests
- 2026-10-21T04:04:25Z done
- 2026-10-21T04:04:27Z committed 4a0b171a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- T-1242 [FEATURE L, done, 3 steps] Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haik…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- plugin/lib/fmpr.py
- plugin/lib/fmrelease.py
- plugin/tests/test_release.py
