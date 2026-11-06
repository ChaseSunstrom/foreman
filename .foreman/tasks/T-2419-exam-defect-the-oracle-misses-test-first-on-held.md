---
id: T-2419
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T15:07:30Z
updated: 2026-10-31T15:56:44Z
builder_model: sonnet
base: 522e9dd53ab6507baf531a51d2139c699e81546c
base_tree: 578cdd0254ad3a975eda61b3981c00ba54f4597e
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-10-31T15:35:50Z
plan0_scope: []
verified: strong
---
# Exam defect: the oracle misses test-first on held-out slow-c-18f793 and slow-c-6bc211 (s70-010): a slow C defect put back doesn't fail the suite, so 2 held-out scenarios no arm can close
## Raw request
> Exam defect: the oracle misses test-first on held-out slow-c-18f793 and slow-c-6bc211 (s70-010): a slow C defect put back doesn't fail the suite, so 2 held-out scenarios no arm can close
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the oracle closes every s70-010 scenario, the two slow C ones included — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce: put the slow defect back into the oracle's work for slow-c-18f793 and time its suite; find why it neither times out nor fails (the C template's slow check, the timeout, or the putback); red test in test_exam with a C slow render; fix the template or the timing
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen.test_putback_anchors_on_the_arms_file_not_on_what_an_earlier_region_planted` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: ExamGen 0s) / OK [ran] [tree 5b0612e0a338] (2026-10-31T15:42:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_exam && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [34.22s] [ran] [tree 5b0612e0a338] (2026-10-31T15:45:25Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 44 tests in 94.1s (11 classes, 16 at a time; slowest: ExamAuthors 93s, ExamGen 72s, ExamRust 24s) / OK [ran] [tree 5b0612e0a338] (2026-10-31T15:45:50Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 44 tests in 77.4s (11 classes, 16 at a time; slowest: ExamAuthors 77s, ExamGen 59s, ExamRust 22s) / OK [ran] [tree a5a98249928c] (2026-10-31T15:50:16Z)
- `python3 plugin/tests/run.py test_exam -k anchors_on_the_arms_file` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: ExamGen 0s) / FAILED (1 classes: test_exam.ExamGen) (start tree + this task's tests) [ran] [tree a5a98249928c] (2026-10-31T15:50:29Z)
- `python3 plugin/tests/run.py test_exam -k anchors_on_the_arms_file` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: ExamGen 0s) / OK [ran] [tree a5a98249928c] (2026-10-31T15:50:29Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 44 tests in 72.3s (11 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 57s, ExamRust 18s) / OK [ran] [tree ad8c70119d95] (2026-10-31T15:51:42Z)
- (audit edge) `self-review of the merged lane: putback finds every region's anchors in the arm's file as it is, then splices last to first, refusing out-of-order or overlapping regions; red→green on a three-region fixture shaped like slow-c's unique(); 44 exam tests OK; the oracle regrade on s70-010 runs next` → regions that overlap or come out of order in the arm still credit nothing (LookupError), as before [tree ad8c70119d95] (2026-10-31T15:51:42Z)
- (audit self) `self-review of the merged lane: putback finds every region's anchors in the arm's file as it is, then splices last to first, refusing out-of-order or overlapping regions; red→green on a three-region fixture shaped like slow-c's unique(); 44 exam tests OK; the oracle regrade on s70-010 runs next` → no findings [tree ad8c70119d95] (2026-10-31T15:51:42Z)
## Log
- 2026-10-31T15:07:30Z created
- 2026-10-31T15:35:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2419.builder.md
- 2026-10-31T15:35:49Z focused
- 2026-10-31T15:35:50Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-10-31T15:48:56Z merged worktree-agent-a8f8a2bfebeb9173e (2 file(s))
- 2026-10-31T15:48:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8f8a2bfebeb9173e
- 2026-10-31T15:48:57Z focused
- 2026-10-31T15:50:29Z scope: plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md
- 2026-10-31T15:53:08Z done
- 2026-10-31T15:53:11Z committed c9f6b96c (1 file)
- 2026-10-31T15:56:44Z verified: s70-010 oracle regrade after merge: test-first 203/203 (was 201/203), every scenario closable
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2401 [FIX S, done, 1 steps] #4 exam defect: the oracle misses test-first on goal-rust-860eab (s0-011), so it closes 17/18 and a #4 held-out scenario no arm can close —…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
## Lessons
- Splicing changes the text later anchors are looked up in: find all anchors first, then edit from the end
## Files touched
- .fm-scratch/pb.py
- .fm-scratch/dbg.py
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
