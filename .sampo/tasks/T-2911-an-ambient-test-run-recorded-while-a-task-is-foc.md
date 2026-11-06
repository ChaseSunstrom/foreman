---
id: T-2911
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_ambient.py, plugin/tests/test_hooks.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/tests/test_bookkeeping.py]
depends_on: []
source: discovered
created: 2026-11-04T06:37:23Z
updated: 2026-11-06T14:51:45Z
base: f84d5ed2f6bad2231be4be6faf785b5f5023d235
base_tree: 306a891ce42ffa10d4355b15d769560ec4537b77
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:55:42Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_ambient.py, plugin/tests/test_hooks.py]
builder_returned: 2026-11-06T09:08:21Z
lane_stop: refused 2026-11-06T14:51:45Z
verified: strong
postmerge_red: test_check_paths.CheckSkip, test_claims.Claims, test_diff_gates.DiffGates
postmerge_sha: abca89bd512ddb43e489494fbc2d5a86a8544d80
---
# An automatic criterion run checks off the current step only when the run is about that step, so a drive-test run never proves 'the site rebuilt'
## Raw request
> FIX: an ambient test run recorded while a task is focused must not check off that task's current step unless the command is that step's verify; T-2742 step 7 (the site rebuilt) was checked by a run of the drive tests
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] hooks._auto_evidence (and _runner_evidence) record a passing run as the current step's evidence only when the step's text names the command or shares a subject word with it (a test module's name words, a file it names); otherwise only the criterion gets it and the hook notes 'step N not checked: run its own check'; T-2742's case (step 'the site rebuilt', a run of the drive tests) leaves the step open — verify with `python3 plugin/tests/run.py test_ambient test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: T-2742's case leaves the step open; a step naming test_site_build is checked by that run; the note
2. [x] the subject match in _auto_evidence and _runner_evidence
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping test_ambient test_hooks` → exit 0 · Ran 291 tests in 609.1s (163 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 21s, NoTaskGateQueue 19s, Ambient 13s) / OK [ran] [tree d994e92b7b72] [world 2f1906870a] (2026-11-06T09:07:58Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 1e9db50aa1dd] (2026-11-06T10:48:23Z)
- `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 22 tests in 4.1s (10 jobs, 16 at a time; slowest: CommitOwnFiles 3s, FinishGaps 2s, CommitAfterFocus 2s) / FAILED (1 classes: test_bookkeeping.StepEvidence) (start tree + this task's tests) [ran] [tree 1e9db50aa1dd] [world 2f1906870a] (2026-11-06T10:48:31Z)
- `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 22 tests in 2.4s (12 jobs, 16 at a time; slowest: CommitAfterFocus 2s, FinishGaps 2s, StepEvidence 2s) / OK [ran] [tree 1e9db50aa1dd] [world 2f1906870a] (2026-11-06T10:48:31Z)
- (ac 1) `python3 plugin/tests/run.py test_ambient test_hooks` → exit 0 · Ran 270 tests in 23.3s (197 jobs, 16 at a time; slowest: PreToolUse 15s, Approvals 14s, SessionStart.test_budget_holds_with_large_queue 8s) / OK [ran] [tree 1e9db50aa1dd] [world 2f1906870a] (2026-11-06T10:48:56Z)
- (step 2) `python3 plugin/tests/run.py test_ambient test_hooks` → exit 0 · Ran 270 tests in 23.3s (197 jobs, 16 at a time; slowest: PreToolUse 15s, Approvals 14s, SessionStart.test_budget_holds_with_large_queue 8s) / OK [ran] [tree 1e9db50aa1dd] [world 2f1906870a] (2026-11-06T10:48:56Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 1e9db50aa1dd] (2026-11-06T10:48:56Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 1e9db50aa1dd] (2026-11-06T10:48:56Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 1e9db50aa1dd] (2026-11-06T10:48:56Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 1e9db50aa1dd] (2026-11-06T10:48:56Z)
## Log
- 2026-11-04T06:37:23Z created
- 2026-11-05T03:36:07Z planned from capture
- 2026-11-05T03:36:08Z set approved=True
- 2026-11-05T03:36:08Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_ambient.py', 'plugin/tests/test_hooks.py']
- 2026-11-05T03:36:08Z blocked: approved; waits for a builder slot (after T-3129, which also edits hooks.py)
- 2026-11-06T03:53:16Z unblocked
- 2026-11-06T08:55:40Z focused
- 2026-11-06T08:55:42Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T10:48:20Z merged worktree-agent-a89b5caad42b1031c (2 file(s))
- 2026-11-06T10:48:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a89b5caad42b1031c
- 2026-11-06T10:48:20Z focused
- 2026-11-06T10:48:22Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_ambient.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/test_bookkeeping.py']
- 2026-11-06T10:48:23Z scope: widened at merge to the reviewed lane's own diff (abca89bd5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:49:29Z done
- 2026-11-06T10:49:32Z committed 735341d1e (1 file)
- 2026-11-06T14:51:45Z red after merge: test_check_paths.CheckSkip, test_claims.Claims, test_diff_gates.DiffGates; abca89bd5 reverted (reached by: plugin/lib/sampo/hooks.py, plugin/tests/test_bookkeeping.py)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0994 [FIX M, done, 3 steps] Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994) — lesson: Automatic evidence must …
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-0149 [FIX S, done, 1 steps] A passing criterion check run while a step is current also verifies that step — lesson: Evidence is per step and per criterion; a check tha…
- decision 2026-10-30: [cites: user steer 2026-10-30: have your stuff automatically update the site] [check: python3 plugin/tests/run.py test_genesis.GenesisLive] Standing…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-11-04): plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
