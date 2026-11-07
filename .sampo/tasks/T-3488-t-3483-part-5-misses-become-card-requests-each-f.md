---
id: T-3488
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T18:37:56Z
updated: 2026-11-06T19:10:50Z
builder_model: haiku
lane_branch: foreman/T-3488
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T18:50:45Z
plan0_scope: []
builder_returned: 2026-11-06T18:58:15Z
lane: ~/.claude/foreman.lanes/T-3488
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
inferred_deps: [T-3483, T-3484]
inferred_why: T-3483: named in its request; T-3484: files misses from the loop's failed scenarios
group: local-model exam loop
---
# T-3483 part 5: misses become card requests: each failed local-model scenario files a callcards request naming its failure class, authored and admitted by the existing gates, and bench rows record whether a fix card was applied
## Raw request
> T-3483 part 5: misses become card requests: each failed local-model scenario files a callcards request naming its failure class, authored and admitted by the existing gates, and bench rows record whether a fix card was applied
## Interpretation
Reading 1 (chosen): each failed local-model exam scenario (Louhi smith arm, callcards bench rows) files a callcards request (callcards.requests_path, callcards.py ~1092) naming its failure class (louhi.FAILURE_CLASSES) and the scenario, so the existing authoring and admit gates (smallcards.admit, smallcards.py ~125) turn misses into cards; bench rows record whether a fix card was applied (T-3393's ask). Reading 2 (ruled out): write the cards directly from the failure: skips the admit gates that keep a bad card out of 30,000.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a failed scenario yields a request row and bench rows carry fix_card_applied — verify with `python3 plugin/tests/run.py test_callcards`
## Non-goals
## Approach (options → choice → why)
1) A request row per failed scenario, filed where bench() writes its rows (callcards.py ~1018-1046); likely outcome: one append plus a field on bench rows; fails if: a scenario failing every round files a request each time (dedupe by scenario and class). 2) A nightly sweep over bench.jsonl; fails if: misses wait a day. 3) A new card queue; fails if: it duplicates requests_path. 4) Use what exists: callcards.requests_path and its readers already take requests, and smallcards.admit gates what is added; file into them, mark fix_card_applied from the card the run called (rank/pick, callcards.py ~1070/1096); likely outcome: ~40 lines and a test. 5) Do less: log the failure class only; fails if: nothing turns a miss into a card. Choice 4 (85%): joins existing parts; the dedupe keeps the request list honest.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the change
## Resume here
<!-- auto -->
- 2026-11-06T18:53:27Z step 1/1: failing test, then the change
- git: worktree-agent-af42997e40f756e6d; 2 uncommitted: plugin/lib/sampo/callcards.py, plugin/tests/test_callcards.py
- touched since last checkpoint: plugin/tests/test_callcards.py, plugin/lib/sampo/callcards.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_callcards` → ✗ exit 1 · Ran 55 tests in 9.8s (10 jobs, 16 at a time; slowest: Confinement 8s, Apply 7s, Calls 5s) / FAILED (1 classes: test_callcards.Misses) [ran] [tree 971f432b6075] [world 2f1906870a] (2026-11-06T18:53:09Z)
- (ac 1) `python3 plugin/tests/run.py test_callcards` → exit 0 · Ran 55 tests in 33.7s (36 jobs, 16 at a time; slowest: Confinement.test_a_process_left_behind_cant_change_the_checked_output 4s, Apply.test_a_runaway_generator_times_out_and_a_flood_is_capped 4s, Call [ran] [tree 6e821d278e89] [world 2f1906870a] (2026-11-06T18:54:51Z)
- (step 1) `python3 plugin/tests/run.py test_callcards` → exit 0 · Ran 55 tests in 149.3s (36 jobs, 16 at a time; slowest: Apply.test_a_runaway_generator_times_out_and_a_flood_is_capped 4s, Confinement.test_a_process_left_behind_cant_change_the_checked_output 4s, Cal [ran] [tree 6e821d278e89] [world 2f1906870a] (2026-11-06T18:57:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_callcards test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [24.46s] [ran] [tree 6e821d278e89] [world 2f1906870a] (2026-11-06T18:57:55Z)
## Log
- 2026-11-06T18:37:56Z created
- 2026-11-06T18:50:12Z set approved=True
- 2026-11-06T18:50:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3488.builder.md
- 2026-11-06T18:50:44Z focused
- 2026-11-06T18:50:45Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T19:09:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af42997e40f756e6d (branch worktree-agent-af42997e40f756e6d kept: not merged); dropped: relocated beside the repo: the train left it out on a conflict and the Ward refuses git merge under .claude/worktrees; its branch is kept and merged into the new lane
- 2026-11-06T19:09:38Z lane: ~/.claude/foreman.lanes/T-3488 on foreman/T-3488
- 2026-11-06T19:10:50Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3484 [FEATURE M, active, 1 steps] T-3483 part 1: sampo exam loop: each round runs the smith arm on N unseen scenarios per local profile, then the failure taxonomy, and…
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- T-2995 [FEATURE M, done, 3 steps] Exam keeps green Smith run journals and sampo exam models --traces exports them: the first piece of the distilled actor (T-2971) — less…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
