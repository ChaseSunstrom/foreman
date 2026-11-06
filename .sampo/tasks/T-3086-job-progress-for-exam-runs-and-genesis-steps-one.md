---
id: T-3086
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-05T00:45:51Z
updated: 2026-11-05T13:02:04Z
builder_model: sonnet
base: 4205131f6bdb53179cc96a10a49ba1ae2c32d9b5
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-05T04:56:27Z
plan0_scope: []
base_tree: 7c22f501de9d7b6d1622f45ecc04aaf7c40c8970
lane_stop: merged 2026-11-05T12:55:42Z
verified: strong
---
# Job progress for exam runs and genesis steps: one progress call in the exam-run loop and in each genesis step, so the live page's progress bars cover them (T-3044 part 2)
## Raw request
> Job progress for exam runs and genesis steps: one c.progress call in the exam-run loop (louhi/cli) and in rune's step, once T-3053's lane has merged (T-3083 left these out because those files were held)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo exam run and each sampo genesis step write c.progress (done of total scenarios or stage items, with the unit) while they run and end it after; the live page's jobs list shows them with a bar — verify with `python3 plugin/tests/run.py test_exam test_genesis test_live`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a fake exam of 3 scenarios writes 1/3, 2/3, 3/3; a genesis step writes its items
2. [x] the progress calls
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis test_live` → exit 0 · Ran 414 tests in 315.5s (61 classes, 16 at a time; slowest: LeanKind 272s, Page 176s, ExamAuthors 117s) / OK [ran] [tree 0b8e5f275224] [world 2f1906870a] (2026-11-05T05:09:57Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis test_live` → exit 0 · Ran 423 tests in 103.3s (188 jobs, 16 at a time; slowest: LeanKindGateHookDelay 103s, LeanKindGateSessionLine 96s, LeanKindGateGuardAllow 95s) / OK [ran] [tree 285fb151698d] [world 2f1906870a] (2026-11-05T12:57:36Z)
- `python3 plugin/tests/run.py test_exam.ExamRun test_genesis` → ✗ exit 1 · run.py: no test matches test_exam.ExamRun (start tree + this task's tests) [ran] [tree 92b5e8258229] [world 2f1906870a] (2026-11-05T12:57:43Z)
- `python3 plugin/tests/run.py test_exam.ExamRun test_genesis` → ✗ exit 1 · run.py: no test matches test_exam.ExamRun [ran] [tree 92b5e8258229] [world 2f1906870a] (2026-11-05T12:57:43Z)
- `python3 plugin/tests/run.py test_exam.ExamGen.test_an_exam_run_writes_its_place_in_the_scenarios_and_ends_it test_genesis.GenesisExam.test_a_genesis_exam_writes_its_place_in_the_scenarios_and_ends_it` → ✗ exit 1 · Ran 2 tests in 7.0s (2 jobs, 16 at a time; slowest: ExamGen 5s, GenesisExam 0s) / FAILED (2 classes: test_exam.ExamGen, test_genesis.GenesisExam) (start tree + this task's tests) [ran] [tree 92b5e8258229] [world 2f1906870a] (2026-11-05T12:58:04Z)
- `python3 plugin/tests/run.py test_exam.ExamGen.test_an_exam_run_writes_its_place_in_the_scenarios_and_ends_it test_genesis.GenesisExam.test_a_genesis_exam_writes_its_place_in_the_scenarios_and_ends_it` → exit 0 · Ran 2 tests in 5.7s (2 jobs, 16 at a time; slowest: ExamGen 5s, GenesisExam 0s) / OK [ran] [tree 92b5e8258229] [world 2f1906870a] (2026-11-05T12:58:04Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_genesis test_live` → exit 0 · Ran 423 tests in 109.9s (204 jobs, 16 at a time; slowest: LeanKindGateHookDelay 110s, LeanKindGateSessionLine 100s, LeanKindGateGuardAllow 96s) / OK [ran] [tree 92b5e8258229] [world 2f1906870a] (2026-11-05T13:00:00Z)
- (audit edge) `re-ran test_exam + test_genesis + test_live on main after the merge: 423 OK; proved red→green with its two new tests` → progress ends after the loop, so a finished exam leaves no bar; T-3044's branch also touches louhi._run_agent and rune.exam (outer=True and a finally), so its merge must keep both: noted for that merge [tree 92b5e8258229] (2026-11-05T13:00:00Z)
- (audit adversary) `re-ran test_exam + test_genesis + test_live on main after the merge: 423 OK; proved red→green with its two new tests` → progress files hold counts and a note under state/progress/<pid>.json, written by the running process; the live page reads them as data [tree 92b5e8258229] (2026-11-05T13:00:00Z)
- (audit self) `re-ran test_exam + test_genesis + test_live on main after the merge: 423 OK; proved red→green with its two new tests` → no findings [tree 92b5e8258229] (2026-11-05T13:00:00Z)
## Log
- 2026-11-05T00:45:51Z created
- 2026-11-05T04:46:26Z planned from capture
- 2026-11-05T04:46:26Z set approved=True
- 2026-11-05T04:46:27Z blocked: approved; after T-3083's merge (c.progress), then a builder slot
- 2026-11-05T04:56:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3086.builder.md
- 2026-11-05T04:56:26Z focused
- 2026-11-05T04:56:27Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-05T12:55:42Z merged worktree-agent-a40a072b318779679 (4 file(s))
- 2026-11-05T12:55:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a40a072b318779679
- 2026-11-05T12:55:51Z focused
- 2026-11-05T13:02:01Z done
- 2026-11-05T13:02:04Z committed 2b19d1a0 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-3092 [FEATURE M, planned, 4 steps] Live page part 2: modern charts for every panel (time series, stacked GPU memory, a moons funnel, sparklines, job progress bars) fro…
- decision 2026-11-05: builder order once slots free (user asks first): T-3081 Kalevala part 2 (as soon as T-3053 merges), T-3122 moons yield, T-3113 the pane crest, T-310…
## Lessons
- Two lanes that add progress to the same loops will conflict: merge the smaller first and rebase the other
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/louhi.py
- CHANGELOG.md
