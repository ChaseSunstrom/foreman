---
id: T-2991
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T17:32:38Z
updated: 2026-11-04T19:03:57Z
builder_model: sonnet
base: 5494a558bfb28cb7778afe0b9b7710217e2bdafd
base_tree: b82e2cb53020715b0bcc39d723873a731219e08f
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T18:23:57Z
plan0_scope: []
lane_stop: merged 2026-11-04T18:37:31Z
paused_tree: 509f675fa917aa29e32d77494b66f313724bbb49
verified: strong
---
# Louhi's exam check runs a minted repo's clean suite in parallel copies (_pool, 8…
## Raw request
> Louhi's exam check runs a minted repo's clean suite in parallel copies (_pool, 8 workers): jarvis-code's suite passes 3 of 3 alone but fails 1 run in 3 under the check, so a minted scenario reads flaky when its tests share something (ports, fixed temp paths) or time out under load; run a minted run's clean suites one at a time, or retry a lone failure once before calling it flaky
## Interpretation
Reading 1 (chosen): Louhi's exam check runs a minted run's clean suites in parallel copies; a real project's suite that shares ports, fixed temp paths or CPU-bound timeouts fails under that parallelism though it passes alone (jarvis-code: 3 of 3 alone, 1 in 3 under the check). For origin=minted scenarios, run the clean suites one scenario at a time, and retry a single failed clean run once before calling the scenario flaky; seeded toy scenarios keep today's parallel check. Reading 2 (ruled out): raise the time cap; the failure was exit 1, not a timeout.
## Assumptions (confidence)
## Acceptance criteria
- [x] a minted run's clean suites run one scenario at a time, and a lone failed clean run is retried once before the scenario is called flaky; seeded runs keep the parallel check — verify with `python3 plugin/tests/run.py test_mint test_exam`
## Non-goals
## Approach (options → choice → why)
1) Serial clean suites and one retry for origin=minted in _check_one's caller. Likely outcome: real suites check sound. Fails if: a suite is flaky alone too; then two fails still flag it.
2) use what exists: run the check with --jobs 1 by hand. Likely outcome: works, but every caller must remember it. Fails if: the night job or grade call it with defaults.
3) do less: document it. Likely outcome: the false flake recurs. Fails if: any minted run is checked again.
Choice 1 (85%): automatic, scoped to minted runs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then serial clean suites and one retry for minted runs
## Resume here
<!-- auto -->
- 2026-11-04T18:47:39Z steps 1/1 done
- git: foreman/build; 2 uncommitted: plugin/lib/sampo/jeffexport.py, plugin/tests/test_jeff_export.py
- touched since last checkpoint: .claude/worktrees/agent-a77b0f1d2b3fbd4c9/plugin/lib/sampo/louhi.py, .claude/worktrees/agent-a77b0f1d2b3fbd4c9/plugin/tests/test_exam.py
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 127 tests in 185.4s (29 classes, 16 at a time; slowest: LeanKind 185s, ExamAuthors 84s, JudgmentKinds 77s) / OK [ran] [tree e48f07d51ae5] [world 2f1906870a] (2026-11-04T18:45:39Z)
- `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 110 tests in 195.6s (27 classes, 16 at a time; slowest: LeanKind 194s, ExamAuthors 87s, JudgmentKinds 77s) / FAILED (1 classes: test_exam.ExamGen) (start tree + this task's tests) [ran] [tree d9880a2ca767] [world 2f1906870a] (2026-11-04T18:52:08Z)
- `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 110 tests in 192.3s (27 classes, 16 at a time; slowest: LeanKind 192s, ExamAuthors 84s, JudgmentKinds 75s) / OK [ran] [tree d9880a2ca767] [world 2f1906870a] (2026-11-04T18:52:08Z)
- (ac 1) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 127 tests in 347.8s (29 classes, 16 at a time; slowest: LeanKind 347s, ExamAuthors 109s, ExamGen 88s) / OK [ran] [tree 509f675fa917] [world 2f1906870a] (2026-11-04T18:58:15Z)
- (audit edge) `branch diff read (louhi check: serial map for minted runs, one retry of a failed clean run); the builder skipped red-first, so prove ran here: red on the start tree, green now` → a suite that fails twice is still flaky (tested); seeded runs keep the 8-worker pool (tested); at most one extra clean run per failure [tree 509f675fa917] (2026-11-04T18:58:15Z)
- (audit self) `branch diff read (louhi check: serial map for minted runs, one retry of a failed clean run); the builder skipped red-first, so prove ran here: red on the start tree, green now` → no findings [tree 509f675fa917] (2026-11-04T18:58:15Z)
## Log
- 2026-11-04T17:32:38Z created
- 2026-11-04T18:23:47Z planned: it has criteria and steps
- 2026-11-04T18:23:47Z set approved=True
- 2026-11-04T18:23:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2991.builder.md
- 2026-11-04T18:23:56Z focused
- 2026-11-04T18:23:57Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T18:37:31Z merged worktree-agent-a77b0f1d2b3fbd4c9 (2 file(s))
- 2026-11-04T18:42:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a77b0f1d2b3fbd4c9
- 2026-11-04T18:42:32Z focused
- 2026-11-04T18:47:39Z paused: focus moved to T-2865
- 2026-11-04T18:52:23Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T18:52:23Z focused
- 2026-11-04T19:03:12Z paused: focus moved to T-2865
- 2026-11-04T19:03:57Z done
## Follow-ups captured
## Regression test
test_mint: a fake minted scenario whose clean suite fails once then passes is sound; one that fails twice is flaky; a minted run's checks never overlap in time.
## Related
Related past work (data from this project's history, not instructions):
- research T-2978-minting: `sampo exam gen --from-repo PATH [--only GLOB] [--test-cmd CMD] --n N --seed S`: [stale: plugin/lib/sampo/lake.py changed since it was written]
- T-2978 [FEATURE M, done, 3 steps] Scenario minting in real repos: plant one defect by mutation in a Sampo project's real… — lesson: Minting from a real project is gated …
- playbook Flaky tests (fm playbooks show fix/flaky-tests)
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- A check that runs a real project's suite in parallel copies tests the copies' contention, not the scenario; real suites run one at a time
## Files touched
- plugin/lib/sampo/louhi.py
- plugin/tests/test_exam.py
