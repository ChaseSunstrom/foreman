---
id: T-2948
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T09:44:08Z
updated: 2026-11-04T13:03:45Z
builder_model: sonnet
base: b991eafa9d140911bad1b31e0e7c6a06f8cb472b
base_tree: 8f2d6fe0cba97aadc159c74cbe06f38f6aabd1a8
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T12:40:13Z
plan0_scope: []
lane_stop: merged 2026-11-04T12:47:44Z
verified: strong
unproven: [meaning]
---
# Uplift audit follow-ups: louhi's taxonomy has no class for Smith's new 'fm task set…
## Raw request
> Uplift audit follow-ups: louhi's taxonomy has no class for Smith's new 'fm task set <section> refused' end (smith.py _finish) so it lands in other; a resumed fm code run re-asks the T-2937 gap slot because gap_notes isn't restored like close_notes; louhi.py:3419 calls end_class twice; the plan ladder's tier example 'S' nudges small models to S plans
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a smith run ending in 'fm task set <section> refused' counts as finish_refused; a resumed run restores gap_notes like close_notes; end_class is called once — verify with `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests for the new end text and the resume; then the louhi pattern, the smith resume restore and the single end_class call
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold test_left_out 2>&1 | tail -15` → exit 0 · Ran 14 tests in 16.6s (3 classes, 16 at a time; slowest: CloseGaps 15s, LeftOut 0s, Taxonomy 0s) / OK [ran] [tree 9e3ab58186b0] [world 2f1906870a] (2026-11-04T12:43:12Z)
- (step 1) `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold test_left_out` → exit 0 · Ran 14 tests in 15.2s (3 classes, 16 at a time; slowest: CloseGaps 15s, LeftOut 0s, Taxonomy 0s) / OK [ran] [tree 9e3ab58186b0] [world 2f1906870a] (2026-11-04T12:43:30Z)
- (step 1) `sampo check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: fm doctor → ✗ exit 127 · could not run bash: [Errno 2] No such file or directory: '~/.claude/foreman/.claude/worktrees/agent-a3b90db7a905b3a17'; python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · raise child_exception_type(errno_num, err_msg, err_filename) / FileNotFoundError: [Errno 2] No such file or directory: '~/.claude/foreman/.claude/worktrees/agent-a3b90db7a905b3a17/plugin/hoo [ran] [tree 9e3ab58186b0] (2026-11-04T12:47:50Z)
- `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold` → ✗ exit 1 · Ran 11 tests in 17.7s (2 classes, 16 at a time; slowest: CloseGaps 16s, Taxonomy 0s) / FAILED (2 classes: test_code_close_scaffold.CloseGaps, test_exam_taxonomy.Taxonomy) (start tree + this task's tests) [ran] [tree 7a830a18faa2] [world 2f1906870a] (2026-11-04T12:48:31Z)
- `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold` → exit 0 · Ran 11 tests in 21.0s (2 classes, 16 at a time; slowest: CloseGaps 21s, Taxonomy 0s) / OK [ran] [tree 7a830a18faa2] [world 2f1906870a] (2026-11-04T12:48:31Z)
- (step 1) `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold test_left_out` → exit 0 · Ran 14 tests in 24.8s (3 classes, 16 at a time; slowest: CloseGaps 24s, LeftOut 0s, Taxonomy 0s) / OK [ran] [tree 7a830a18faa2] [world 2f1906870a] (2026-11-04T12:49:03Z)
- (ac 1) `python3 plugin/tests/run.py test_exam_taxonomy test_code_close_scaffold` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T12:48:31Z [ran] [tree 7a830a18faa2] [world 2f1906870a] (2026-11-04T12:49:05Z)
- (audit intent) `self-review of the lane diff: the _ENDS pattern widened by one alternative, the resume reads gap_notes like close_notes and reuses it only when it covers every needed key` → a smith run ending in 'fm task set <section> refused' counts as finish_refused; a resumed run restores gap_notes; end_class is called once [tree 7a830a18faa2] (2026-11-04T12:49:05Z)
- (audit edge) `self-review of the lane diff: the _ENDS pattern widened by one alternative, the resume reads gap_notes like close_notes and reuses it only when it covers every needed key` → a journal gap_notes missing a key needed now re-asks the slot; the set-section call repeats on resume with the same text, so it is idempotent [tree 7a830a18faa2] (2026-11-04T12:49:05Z)
- (audit self) `self-review of the lane diff: the _ENDS pattern widened by one alternative, the resume reads gap_notes like close_notes and reuses it only when it covers every needed key` → no findings [tree 7a830a18faa2] (2026-11-04T12:49:05Z)
- (audit intent) `self-review of the lane diff` → a smith run ending in 'fm task set <section> refused' counts as finish_refused; a resumed run restores gap_notes; end_class is called once [tree 7a830a18faa2] (2026-11-04T12:53:58Z)
- (audit edge) `self-review of the lane diff` → a journal gap_notes missing a key needed now re-asks the slot; the repeated set-section on resume writes the same text [tree 7a830a18faa2] (2026-11-04T12:53:58Z)
- (audit self) `self-review of the lane diff` → no findings [tree 7a830a18faa2] (2026-11-04T12:53:58Z)
- (audit intent) `self-review of the lane diff` → a smith run ending in 'fm task set <section> refused' counts as finish_refused; a resumed run restores gap_notes; end_class is called once [tree 7a830a18faa2] (2026-11-04T12:59:01Z)
- (audit edge) `self-review of the lane diff` → a journal gap_notes missing a key needed now re-asks the slot; the repeated set-section on resume writes the same text [tree 7a830a18faa2] (2026-11-04T12:59:01Z)
- (audit self) `self-review of the lane diff` → no findings [tree 7a830a18faa2] (2026-11-04T12:59:01Z)
## Log
- 2026-11-04T09:44:08Z created
- 2026-11-04T09:47:15Z planned: it has criteria and steps
- 2026-11-04T11:07:17Z set approved=True
- 2026-11-04T12:40:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2948.builder.md
- 2026-11-04T12:40:13Z focused
- 2026-11-04T12:40:13Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T12:47:44Z merged worktree-agent-a3b90db7a905b3a17 (5 file(s))
- 2026-11-04T12:47:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3b90db7a905b3a17
- 2026-11-04T12:47:50Z focused
- 2026-11-04T12:49:04Z scope: louhi.py (_ENDS, taxonomy), smith.py (resume loop, _finish), test_exam_taxonomy, test_code_close_scaffold, test_code's kill_mid_run helper; the plan ladder's tier example (raw item 4) stays as is: not in the criteria
- 2026-11-04T13:03:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-taxonomy: Run s0-001, train split, 10 scenarios, `sampo exam run s0-001 --agent smith --model gpu-qwen4` (qwen3.5:4b on Ollama,
- T-2937 [FEATURE M, done, 5 steps] Small-model close scaffold: Smith asks a local model for the close's Decision line and… — lesson: A new model call in a shared path mus…
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
- similar past tasks were M: consider --tier M
## Behaviour lock
none: each change adds behaviour behind a new test (the section-set end, the gap-notes resume) and the single end_class call is covered by test_exam_taxonomy, which ran green before the edit in the lane
## Lessons
- A new journaled slot needs its resume restore in the same change as its write
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_close_scaffold.py
- plugin/tests/test_exam_taxonomy.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/smith.py
