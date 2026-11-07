---
id: T-3582
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T02:54:09Z
updated: 2026-11-07T04:49:44Z
lane: ~/.claude/foreman.lanes/T-3582
lane_branch: foreman/T-3582
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T04:25:16Z
plan0_scope: []
---
# The UserPromptSubmit hook (hooks.py ~1568) holds the project lock across load_briefs,…
## Raw request
> PERF: the UserPromptSubmit hook (hooks.py ~1568) holds the project lock across load_briefs, _reconcile and state_dict/regen_views on every prompt, and ~50 other regen_views callers (cli capture, task new, hooks SessionStart) still regenerate under it; T-3558 moved mutate and focus out (regen_views now has its own views lock, the sync export is core.export_mirror under the project lock): move these the same way (found in T-3558)
## Interpretation
Reading 1 (chosen): the UserPromptSubmit hook, which runs on every prompt, holds the project lock across load_briefs, the rewind check and state_dict/regen_views; move the load, state and view regen out of the lock as T-3558 did for focus/mutate, plus the call sites the request names (SessionStart, cli capture, task new). Reading 2 (ruled out for this task): convert all ~57 regen_views callers now; that is L-tier churn across 20 files with no measurement saying the rare ones matter, so it is captured as a follow-up instead.
## Assumptions (confidence)
## Acceptance criteria
- [ ] UserPromptSubmit and SessionStart load briefs, build state and regenerate views with the project lock free, approvals/overrides/rewind still applied — verify with `nice -n 10 python3 plugin/tests/run.py test_prompt_lock`
- [ ] existing hook behaviour unchanged — verify with `nice -n 10 python3 plugin/tests/run.py test_nudges test_focus_lock`
## Non-goals
## Approach (options → choice → why)
1) use what exists: T-3558's pattern at each call site: under the lock only the meta/gate/brief writes plus core.export_mirror; regen_views(mirror=False) / state_dict after it; the rewind check reads the active brief alone (active_brief_fast). Likely outcome: UPS lock hold drops to the meta/gate writes (ms). 2) A deferral inside core.lock that runs regen_views when the outermost lock releases (all 57 callers at once). Fails if: a second mechanism the brief forbids; regen return values used under the lock break. 3) do less: only the UserPromptSubmit hook. Fails if: SessionStart and capture/task new keep queueing lanes behind full loads. Choice 1 (80%): reuses the landed mechanism, covers the hot hook paths and the named cli ones; the rest captured.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: spy load_briefs/state_dict/regen_views lock-held in UserPromptSubmit and SessionStart
2. [x] Move the loads and regen out of the lock (export_mirror stays under it); capture/task new the same
3. [x] Measure lock hold and wall time before/after with 8 concurrent sampo calls
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_prompt_lock` → ✗ exit 1 · Ran 3 tests in 1.3s (1 jobs, 16 at a time; slowest: PromptLock 1s) / FAILED (1 classes: test_prompt_lock.PromptLock) [ran] [tree 6193bec457a6] [world 2f1906870a] (2026-11-07T04:27:35Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_prompt_lock` → exit 0 · Ran 4 tests in 19.2s (1 jobs, 16 at a time; slowest: PromptLock 2s) / OK [ran] [tree 11f6659755bf] [world 2f1906870a] (2026-11-07T04:45:05Z)
- (step 3) `scratchpad upsbench/bench.py: 2,400 copied briefs, 8 concurrent sampo task log loops, /proc/locks sampled each 1 ms, 15 UserPromptSubmit runs per side` → no proof: lock hold median 0.152 -> 0.036 s (max 0.400 -> 0.095), wall 0.593 -> 0.536 s; active task with a tree proof: hold 0.406 -> 0.157 s (max 3.021 -> 0.872), wall 1.669 -> 1.947 s (load 40-43, noise); 0 not-recorded either side [tree 11f6659755bf] (2026-11-07T04:45:21Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_prompt_lock test_rewind test_nudges test_focus_lock` → exit 0 · Ran 26 tests in 274.0s (11 jobs, 16 at a time; slowest: QuietHints 5s, Rewind.test_files_taken_back_to_between_the_steps_reopen_only_the_later_one_on_the_next_prompt 3s, PromptLock 3s) / OK [ran] [tree 11f6659755bf] [world 2f1906870a] (2026-11-07T04:49:44Z)
## Log
- 2026-11-07T02:54:09Z created
- 2026-11-07T04:24:44Z planned: it has criteria and steps
- 2026-11-07T04:24:49Z lane: ~/.claude/foreman.lanes/T-3582 on foreman/T-3582
- 2026-11-07T04:25:16Z focused
- 2026-11-07T04:25:16Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3558 [PERFORMANCE M, active, 3 steps] Sampo focus holds the project lock 1.8-7.3 s (sampled from /proc/locks while 8 lanes…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
- similar finished tasks took 3–4 steps
