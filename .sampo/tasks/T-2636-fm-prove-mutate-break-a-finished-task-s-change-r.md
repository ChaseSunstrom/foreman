---
id: T-2636
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:40:37Z
base_note: 
builder_model: sonnet
base: b2f5906c3515911577db96e10aebff013c386b55
base_tree: 0f76a45f938e7b96ac012e2a1909a79859f17724
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T20:35:01Z
plan0_scope: []
lane_stop: merged 2026-11-02T20:38:50Z
verified: strong
unproven: [docs, meaning]
---
# fm prove --steer: a user-steer rule's [check: CMD] that also passes on the start tree of the task its row names is vacuous; list each with the task used
## Raw request
> FEATURE: fm prove --mutate: break a finished task's change (revert it, or mutate its DONE-WHEN command) and confirm its proof fails; flag vacuous [check:] steer checks (c02: Guard hardening and security; value 4, effort M, risk med)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
1. (chosen) A user-steer rule's [check: CMD] is vacuous when it also passes on the tree its rule's task started from: it doesn't test the rule. `fm prove --steer` runs each unsettled steer row's check at the start snapshot of the task the row names (fmcli._run_at, as fm task prove --vacuous does per criterion) and lists the rows whose check passes there, with the narrower check to write.
2. Mutate each rule's implementation (revert its hunks) and expect the check to fail. Rejected: that is fm task prove --hunks per task; the start-tree run answers the same question for steer rows in one run each.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --steer flags a steer row whose check passes on its task's start tree, passes one whose check fails there, skips rows naming no task or no snapshot with the reason, and exits 1 when any is vacuous — verify with `python3 plugin/tests/run.py test_prove_steer`
## Non-goals
## Approach (options → choice → why)
1. fm prove --steer in fmprove: for each unsettled steer row (fmcore._decision_rows, STEER, CHECK_TAG, _settled as steer_checks reads them) with a runnable check and a task named in its text (the first T-NNNN whose brief has a start snapshot), run the check via fmcli._run_at at that task's base; passing there is vacuous. Prints one line per row (vacuous / tests its rule / no task named / no start snapshot), exit 1 when any is vacuous; a check shared by rows of one task runs once. Likely outcome: most module-wide checks read vacuous, which is the truth about them. Fails if: a row names several tasks and the first isn't the rule's (the line names the task it used, so a reader can see it).
2. use what exists: fm task prove T-X --vacuous on each rule's task. Fails if: it checks the task's own criteria, not the steer row's check, which is a different command.
3. do less: a static flag on checks that name a whole test module. Fails if: a class-level check can be just as vacuous, and a module check can be exact; only a run says which.
Choice 1 (85%): one run per row on machinery that exists, and its output is a to-do list of checks to narrow.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test with a temp project: two steer rows, one vacuous, one real
2. [x] fm prove --steer in fmprove reusing _decision_rows, _settled, CHECK_TAG and fmcli._run_at
3. [x] CHANGELOG and MASTER (fm prove line)
## Resume here
## Docs impact
CHANGELOG.md and MASTER.md (fm prove line)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove_steer` → ✗ exit 1 · Ran 2 tests in 3.6s (1 classes, 16 at a time; slowest: ProveSteer 2s) / FAILED (1 classes: test_prove_steer.ProveSteer) [ran] [tree 3b85262bd138] [world 2f1906870a] (2026-11-02T20:35:55Z)
- (step 2) `python3 plugin/tests/run.py test_prove_steer` → ✗ exit 1 · Ran 2 tests in 3.8s (1 classes, 16 at a time; slowest: ProveSteer 3s) / FAILED (1 classes: test_prove_steer.ProveSteer) [ran] [tree 45bb9d1b8ebb] [world 2f1906870a] (2026-11-02T20:36:26Z)
- (step 2) `python3 plugin/tests/run.py test_prove_steer` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: ProveSteer 2s) / OK [ran] [tree d5cbc4c5dac3] [world 2f1906870a] (2026-11-02T20:36:39Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_find test_guard_cases test_paused test_prove test_prove_steer test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.42s] [ran] [tree d5cbc4c5dac3] [world 2f1906870a] (2026-11-02T20:37:35Z)
- (step 1) `python3 plugin/tests/run.py test_prove_steer test_prove` → exit 0 · Ran 107 tests in 8.8s (16 classes, 16 at a time; slowest: InfraProof 8s, InfraFinish 5s, DocsProof 5s) / OK [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:39:36Z)
- (step 2) `python3 plugin/tests/run.py test_prove_steer test_prove` → exit 0 · Ran 107 tests in 7.3s (16 classes, 16 at a time; slowest: InfraProof 7s, ReleaseProof 3s, InfraFinish 3s) / OK [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:39:43Z)
- (step 3) `grep -q 'fm prove --steer' CHANGELOG.md && grep -q 'prove --steer' MASTER.md` → exit 0 · (no output) [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:39:44Z)
- (ac 1) `python3 plugin/tests/run.py test_prove_steer` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: ProveSteer 1s) / OK [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:39:46Z)
- (audit intent) `self: reviewed the builder diff; rows are read as steer_checks reads them (settled and pending skipped), each check passes check_argv's allowlist before _run_at runs it in a throwaway worktree, results are cached per (snapshot, check); added the run-consent gate the automated security review asked for, so --steer needs the user's --yes-run like the other modes that run code` → the re-scoped brief asked for vacuous steer checks; a check passing on its rule task's start tree is listed with the task used [tree b0b4477ba78d] (2026-11-02T20:39:46Z)
- (audit adversary) `self: reviewed the builder diff; rows are read as steer_checks reads them (settled and pending skipped), each check passes check_argv's allowlist before _run_at runs it in a throwaway worktree, results are cached per (snapshot, check); added the run-consent gate the automated security review asked for, so --steer needs the user's --yes-run like the other modes that run code` → no run without --yes-run or a kept yes (tested); commands outside check_argv's allowlist are skipped with the reason, never run [tree b0b4477ba78d] (2026-11-02T20:39:46Z)
- (audit edge) `self: reviewed the builder diff; rows are read as steer_checks reads them (settled and pending skipped), each check passes check_argv's allowlist before _run_at runs it in a throwaway worktree, results are cached per (snapshot, check); added the run-consent gate the automated security review asked for, so --steer needs the user's --yes-run like the other modes that run code` → no task named, an unknown task, no start snapshot each skip with a reason (tested); the first T-id in the row is taken as the rule's task and named on the line [tree b0b4477ba78d] (2026-11-02T20:39:46Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T19:56:08Z re-scoped after grounding: reverting a task's change to see its proof fail is fm task prove and fm task prove --hunks (T-0271); what's new is the steer side: a [check:] that also passes on the tree before its rule's task landed is vacuous
- 2026-11-02T20:34:36Z planned from capture
- 2026-11-02T20:34:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2636.builder.md
- 2026-11-02T20:35:00Z focused
- 2026-11-02T20:35:01Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T20:38:50Z merged worktree-agent-aaa3e5e7ae115e4a6 (4 file(s))
- 2026-11-02T20:38:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaa3e5e7ae115e4a6
- 2026-11-02T20:38:51Z focused
- 2026-11-02T20:40:35Z done
- 2026-11-02T20:40:37Z committed 6716f964 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2651 [FEATURE S, done, 3 steps] fm task evidence --bench CMD --under MS: a benchmark that is a pass/fail proof, failing when the median is over the threshold (today --…
- T-2638 [FEATURE M, dropped, 0 steps] fm prove --coverage: report which changed hunks the proof command actually executed…
- T-2637 [FEATURE M, dropped, 0 steps] fm outcomes: per proof kind, how often a proven task was later reverted or corrected…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- the similar finished task took 3 steps
## Lessons
- A new mode of a verb that runs code inherits that verb's consent gate; check the siblings' gates when adding one
## Plan gaps
- failed first: step 1 red test with a temp project: two steer rows, one vacuous, one real
- failed first: step 2 fm prove --steer in fmprove reusing _decision_rows, _settled, CHECK_TAG and fmcli._run_at
## Files touched
- plugin/tests/test_prove_steer.py
- plugin/lib/fmcli.py
- plugin/lib/fmprove.py
- MASTER.md
- CHANGELOG.md
