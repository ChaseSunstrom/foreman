---
id: T-3180
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T08:37:39Z
updated: 2026-11-05T10:42:33Z
builder_model: haiku
base: 30d6dffe77da68a6f2d71bbef2b4eb16eb62fe73
base_tree: 29d1fc95539fa92ffc68ac15e51ab16555d04b18
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T09:38:45Z
plan0_scope: []
builder_returned: 2026-11-05T09:55:24Z
lane_stop: merged 2026-11-05T10:37:53Z
verified: strong
---
# Smith refuses done while the plan's verify is red and no edit was made: the model gets the failing check back and keeps going; early-done stops are counted per model
## Raw request
> Smith on the local 27B often reads a file or two then calls done without editing (T-3160 pilot: 1/10 exam passes): refuse done while the plan's verify is red and no edit was made, feed back the failing check, and count these early-done stops per model
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A Smith run whose model calls done with no edit made while a plan criterion's verify command fails gets that failure back as its next turn instead of ending, at most twice, then ends as stopped-early; the run's journal and the model scorecard count early-done stops — verify with `python3 plugin/tests/run.py test_smith`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a scripted model that calls done after one read gets the failing verify back and must edit
2. [x] the refusal and the count in Smith
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_smith_early_done` → exit 0 · Ran 3 tests in 11.2s (1 classes, 16 at a time; slowest: EarlyDone 10s) / OK [ran] [tree 14736501efd0] [world 2f1906870a] (2026-11-05T09:44:27Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_code_close_scaffold test_code_hardening test_code_worker test_core test_doctor test_left_out test_models test_rename_scan test_smith_early_done && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [17.85s] [ran] [tree 3b90c857fd1c] [world 2f1906870a] (2026-11-05T09:49:13Z)
- (step 2) `python3 plugin/tests/run.py test_smith` → exit 0 · Ran 9 tests in 3.0s (3 classes, 16 at a time; slowest: EarlyDone 3s, Fit 1s, Smith 0s) / OK [ran] [tree c097cc1b98bd] [world 2f1906870a] (2026-11-05T09:52:23Z)
- (step 1) `python3 plugin/tests/run.py test_smith_early_done` → ✗ exit 1 · Ran 4 tests in 7.3s (1 classes, 16 at a time; slowest: EarlyDone 7s) / FAILED (1 classes: test_smith_early_done.EarlyDone) [ran] [tree 1877a200da75] [world 2f1906870a] (2026-11-05T09:53:05Z)
- (step 2) `python3 plugin/tests/run.py test_smith` → exit 0 · Ran 10 tests in 4.9s (3 classes, 16 at a time; slowest: EarlyDone 4s, Fit 1s, Smith 0s) / OK [ran] [tree dbf3c6a2745b] [world 2f1906870a] (2026-11-05T09:55:16Z)
- (step 1) `python3 plugin/tests/run.py test_smith_early_done test_code` → exit 0 · Ran 521 tests in 82.9s (110 classes, 16 at a time; slowest: Worker 82s, CodeFakes 37s, OutcomeEscalation 31s) / OK [ran] [tree d9aa0141a462] [world 2f1906870a] (2026-11-05T10:39:26Z)
- `python3 plugin/tests/run.py test_smith_early_done` → ✗ exit 1 · Ran 4 tests in 6.2s (1 classes, 16 at a time; slowest: EarlyDone 5s) / FAILED (1 classes: test_smith_early_done.EarlyDone) (start tree + this task's tests) [ran] [tree d9aa0141a462] [world 2f1906870a] (2026-11-05T10:39:38Z)
- `python3 plugin/tests/run.py test_smith_early_done` → exit 0 · Ran 4 tests in 5.0s (1 classes, 16 at a time; slowest: EarlyDone 5s) / OK [ran] [tree d9aa0141a462] [world 2f1906870a] (2026-11-05T10:39:38Z)
- (ac 1) `python3 plugin/tests/run.py test_smith` → exit 0 · Ran 10 tests in 10.7s (3 classes, 16 at a time; slowest: EarlyDone 10s, Fit 1s, Smith 1s) / OK [ran] [tree fe6cec8df65b] [world 2f1906870a] (2026-11-05T10:39:59Z)
- (audit edge) `self: read the merged Smith change (done refused while a plan criterion's verify is red and no edit, incl. edits via run like sed -i; at most twice; journal + scorecard count early-done) and test_smith_early_done (4) + test_code (fakes made to edit); 521 tests green; proved red on the start tree` → a run with no plan criteria, or a verify that can't run, is never refused; the third early done ends as stopped-early, so a stuck model can't loop forever [tree fe6cec8df65b] (2026-11-05T10:39:59Z)
- (audit intent) `self: read the merged Smith change (done refused while a plan criterion's verify is red and no edit, incl. edits via run like sed -i; at most twice; journal + scorecard count early-done) and test_smith_early_done (4) + test_code (fakes made to edit); 521 tests green; proved red on the start tree` → T-3160's pilot showed the 27B quitting early (1/10 called a card); this makes the harness hold it to the red check, the precondition for T-3181 [tree fe6cec8df65b] (2026-11-05T10:39:59Z)
- (audit self) `self: read the merged Smith change (done refused while a plan criterion's verify is red and no edit, incl. edits via run like sed -i; at most twice; journal + scorecard count early-done) and test_smith_early_done (4) + test_code (fakes made to edit); 521 tests green; proved red on the start tree` → no findings [tree fe6cec8df65b] (2026-11-05T10:39:59Z)
## Log
- 2026-11-05T08:37:39Z created
- 2026-11-05T08:38:07Z planned from capture
- 2026-11-05T08:38:08Z set approved=True
- 2026-11-05T08:38:22Z blocked: planned and approved; a builder takes it when host load lets a lane in (28.5 now); the main checkout stays quiet for the T-3053 merge chain
- 2026-11-05T09:38:24Z unblocked
- 2026-11-05T09:38:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3180.builder.md
- 2026-11-05T09:38:44Z focused
- 2026-11-05T09:38:45Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T10:37:53Z merged worktree-agent-a4b0c67e492335013 (4 file(s))
- 2026-11-05T10:37:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4b0c67e492335013
- 2026-11-05T10:37:56Z focused
- 2026-11-05T10:41:56Z lens correction: a verify command that can't run counts as failing, so a done with no edit is refused there too (twice, then stopped-early); only a run with no plan or read-only is never refused. Acceptable: such a run can't pass anyway
- 2026-11-05T10:42:30Z done
- 2026-11-05T10:42:33Z committed 9ff3d861 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3181 [FEATURE M, blocked, 3 steps] Calling cards part 1b: the harness drives the cards, not the model: before the first turn Sampo runs the read cards a task needs (fa…
- research T-2878-taxonomy: Source: the 15 Smith exam runs on local or self-hosted models kept in this project's exam answers (s0-001 seeded across 6 languages, s4-018 and…
- T-3152 [FIX S, done, 2 steps] Moons' local-only fill names why no local model answered and tries the next local model (this box's GPU) before it stops — lesson: A sweep …
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
## Plan gaps
- failed first: step 1 failing test: a scripted model that calls done after one read gets the failing verify back and must…
## Files touched
- plugin/tests/test_smith_early_done.py
- plugin/lib/sampo/smith.py
- plugin/lib/sampo/smithbench.py
- plugin/tests/test_code.py
- CHANGELOG.md
