---
id: T-3029
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T22:06:49Z
updated: 2026-11-04T23:32:44Z
builder_model: haiku
route_probe: 1
base: c1069ca0bfcb705fe55b5cd3d2da38759d6954c4
base_tree: c2010f2ad01abca459bc6d55ab686ae0be681a8d
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T22:17:24Z
plan0_scope: []
lane_stop: merged 2026-11-04T23:13:09Z
verified: strong
---
# Sampo exam run on the same run id from two processes (two --model at once) writes the…
## Raw request
> sampo exam run on the same run id from two processes (two --model at once) writes the same answers/smith/<scenario> files, so each score line mixes models: lock the run's answers dir per agent, or key answers by model (found running T-3006's arms in parallel)
## Interpretation
Two sampo exam run processes on the same run id and agent (e.g. two --model arms at once) write the same answers/<agent>/<scenario> files, so each score line mixes models. The second run should be refused up front, naming the first, so arms run one after another.
## Assumptions (confidence)
## Acceptance criteria
- [x] a second sampo exam run of the same run and agent while one holds it is refused before any scenario runs, naming the holder; after the first ends a run goes ahead — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) An exclusive non-blocking flock on answers/<agent>/.lock for the whole of run_agent; a second run of the same run and agent is refused at once with the holder's pid and model. Likely outcome: no mixed scores, no layout change. Fails if: a run is killed and the lock stays (flock is released by the kernel when the process dies, so it can't).
2) Use what exists: key answers by model (answers/<agent>/<model>/). Likely outcome: arms can run in parallel. Fails if: every reader of answers (scorecard, taxonomy, traces, grade) must learn the new layout: wide change for a rare case.
3) Do less: document 'one at a time'. Fails if: it's easy to miss (I did).
Choice 1 (85%): smallest change that makes the mistake impossible.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a held lock refuses the second run_agent
2. [x] the flock in run_agent
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- `python3 plugin/tests/run.py test_exam.ExamAuthors.test_a_second_run_of_the_same_run_and_agent_is_refused_while_one_holds_it` → ✗ exit 1 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: ExamAuthors 1s) / FAILED (1 classes: test_exam.ExamAuthors) (start tree + this task's tests) [ran] [tree 524905d6653f] [world 2f1906870a] (2026-11-04T23:17:41Z)
- `python3 plugin/tests/run.py test_exam.ExamAuthors.test_a_second_run_of_the_same_run_and_agent_is_refused_while_one_holds_it` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: ExamAuthors 1s) / OK [ran] [tree 524905d6653f] [world 2f1906870a] (2026-11-04T23:17:41Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors.test_a_second_run_of_the_same_run_and_agent_is_refused_while_one_holds_it` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: ExamAuthors 0s) / OK [ran] [tree 524905d6653f] [world 2f1906870a] (2026-11-04T23:17:46Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 111 tests in 229.2s (27 classes, 16 at a time; slowest: LeanKind 229s, ExamAuthors 89s, JudgmentKinds 77s) / OK [ran] [tree 524905d6653f] [world 2f1906870a] (2026-11-04T23:21:36Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 111 tests in 269.0s (27 classes, 16 at a time; slowest: LeanKind 268s, ExamAuthors 96s, JudgmentKinds 78s) / OK [ran] [tree acb212806428] [world 2f1906870a] (2026-11-04T23:26:22Z)
- `python3 plugin/tests/run.py test_exam.ExamAuthors.test_a_second_run_of_the_same_run_and_agent_is_refused_while_one_holds_it` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: ExamAuthors 1s) / OK [ran] [tree acb212806428] [world 2f1906870a] (2026-11-04T23:26:22Z)
- (audit edge) `self: read the builder's run_agent/_run_agent split against the race I hit (two --model arms on s5-019): the flock is non-blocking, held for the whole run and released by the kernel when the process dies; the answers wipe keeps .lock; readers list only *.json/*.events.jsonl` → a run dir or agent that doesn't exist skips the lock and refuses as before; a holder killed mid-run frees the lock; a very quick second run may see an empty holder line but is still refused [tree acb212806428] (2026-11-04T23:26:22Z)
- (audit adversary) `self: read the builder's run_agent/_run_agent split against the race I hit (two --model arms on s5-019): the flock is non-blocking, held for the whole run and released by the kernel when the process dies; the answers wipe keeps .lock; readers list only *.json/*.events.jsonl` → the lock file is in the project's own state dir; its text is only shown, never parsed for anything but the message [tree acb212806428] (2026-11-04T23:26:22Z)
- (audit self) `self: read the builder's run_agent/_run_agent split against the race I hit (two --model arms on s5-019): the flock is non-blocking, held for the whole run and released by the kernel when the process dies; the answers wipe keeps .lock; readers list only *.json/*.events.jsonl` → no findings [tree acb212806428] (2026-11-04T23:26:22Z)
## Log
- 2026-11-04T22:06:49Z created
- 2026-11-04T22:08:30Z planned: it has criteria and steps
- 2026-11-04T22:08:31Z set approved=True
- 2026-11-04T22:16:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3029.builder.md
- 2026-11-04T22:17:22Z focused
- 2026-11-04T22:17:24Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T23:13:09Z merged worktree-agent-ab469c29eb34a2003 (2 file(s))
- 2026-11-04T23:13:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab469c29eb34a2003
- 2026-11-04T23:17:36Z focused
- 2026-11-04T23:32:42Z done
- 2026-11-04T23:32:44Z committed e4141438 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- decision 2026-10-30: [revisited: until the end-of-run exam, selection] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pytho…
## Lessons
- Two processes writing one results directory mix silently: a run that owns a directory should take a lock on it and name the holder when it refuses
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/sampo/louhi.py
- CHANGELOG.md
