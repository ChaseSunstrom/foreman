---
id: T-3484
type: FEATURE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/tests/test_louhi_loop.py]
depends_on: []
source: user
created: 2026-11-06T18:37:51Z
updated: 2026-11-07T00:56:49Z
base_note: 
builder: 2026-11-06T18:39:33Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-aba5ea21d4ee00aff
lane_branch: worktree-agent-aba5ea21d4ee00aff
base: 483ea8c998fcabcdbad613d057b6da06eed34146
base_tree: 8d82ac7ab38937b5a64f2ab3af4b2c2fdfd175da
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T18:40:00Z
plan0_scope: []
builder_returned: 2026-11-06T18:56:49Z
lane_passed: {"tree": "42c91f161f537453ecf91fb6e9eafda96ea391c9", "cmds": ["python3 plugin/tests/run.py test_louhi"]}
lane_stop: merged 2026-11-07T00:04:53Z
inferred_deps: [T-3483]
inferred_why: T-3483: named in its request
group: local-model exam loop
verified: strong
unproven: [meaning]
---
# T-3483 part 1: sampo exam loop: each round runs the smith arm on N unseen scenarios per local profile, then the failure taxonomy, and appends {round, model, class, rate} rows to research/local-loop.jsonl; it skips a round while the moons store lock is held
## Raw request
> T-3483 part 1: sampo exam loop: each round runs the smith arm on N unseen scenarios per local profile, then the failure taxonomy, and appends {round, model, class, rate} rows to research/local-loop.jsonl; it skips a round while the moons store lock is held
## Interpretation
Reading 1 (chosen): a round driver over what exists: each round runs Louhi's smith arm (louhi._smith_arm, louhi.py ~3926) on N unseen scenarios per configured local profile, computes louhi.taxonomy (louhi.py ~4075) over that round's event logs, and appends {round, model, scenario count, class, rate, passed} rows to research/local-loop.jsonl; a round is skipped (with a row saying why) while another round runs. Reading 2 (ruled out): a new exam harness: Louhi already has the arms, holdout split and grading; a second harness would drift from it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a stubbed _smith_arm over two rounds appends rows whose counts match the failure classes — verify with `python3 plugin/tests/run.py test_louhi`
## Non-goals
## Approach (options → choice → why)
1) A sampo exam loop verb calling louhi's existing run and taxonomy per profile; likely outcome: one verb plus a jsonl writer, tested with a stubbed _smith_arm; fails if: the scenarios repeat across rounds (use holdout and a seen set). 2) A night timer job only; fails if: rounds then run once a day, not continuously. 3) Run inside Kalevala rounds; fails if: it couples the exam to the tower's schedule. 4) Use what exists: sampo exam run --agent smith --model P already runs one arm (cli.py ~8161, louhi.py ~4570); the loop wraps it per profile and appends taxonomy rows; likely outcome: ~80 lines. 5) Do less: a shell loop over sampo exam run; fails if: no rows, so nothing re-measures or classifies. Choice 4 (90%): the smallest join of existing parts, each already tested; night.py can call the verb later (T-3487 keeps the GPU fed).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the change
## Resume here
<!-- auto -->
- 2026-11-06T18:45:46Z step 1/1: failing test, then the change
- git: worktree-agent-aba5ea21d4ee00aff; 2 uncommitted: plugin/lib/sampo/louhi.py, plugin/tests/test_louhi_loop.py
- touched since last checkpoint: plugin/tests/test_louhi_loop.py, plugin/lib/sampo/louhi.py
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_louhi_loop` → ✗ exit 1 · Ran 3 tests in 0.9s (1 jobs, 16 at a time; slowest: ExamLoop 0s) / FAILED (1 classes: test_louhi_loop.ExamLoop) [ran] [tree 2ff4eba2da2a] [world 2f1906870a] (2026-11-06T18:45:08Z)
- (ac 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · (no output) [ran] [tree 42c91f161f53] [world 2f1906870a] (2026-11-06T18:50:20Z)
- (step 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 32 tests in 77.5s (13 jobs, 16 at a time; slowest: LouhiModels.test_cap_leaves_rows_out_and_show_says_how_many 2s, LouhiModels.test_no_endpoint_is_named_in_the_code 2s, ModelBenchVisible 2s) / OK [ran] [tree 42c91f161f53] [world 2f1906870a] (2026-11-06T18:52:18Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_exam test_left_out test_louhi_loop test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [28.25s] [ran] [tree 42c91f161f53] [world 2f1906870a] (2026-11-06T18:56:34Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 26dea69e852f] (2026-11-07T00:54:27Z)
- `python3 plugin/tests/run.py test_louhi_loop` → ✗ exit 1 · ^^^^^^^^^^^^^^^^^^^ / AttributeError: module 'sampo.core' has no attribute 'private_terms' (start tree + this task's tests) [ran] [tree 26dea69e852f] [world 2f1906870a] (2026-11-07T00:54:33Z)
- `python3 plugin/tests/run.py test_louhi_loop` → exit 0 · Ran 3 tests in 0.8s (1 jobs, 16 at a time; slowest: ExamLoop 0s) / OK [ran] [tree 26dea69e852f] [world 2f1906870a] (2026-11-07T00:54:33Z)
- (ac 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 35 tests in 2.7s (14 jobs, 16 at a time; slowest: ModelBenchVisible 2s, LouhiModels.test_retrieval_rows_vote_from_the_nearest_train_requests_and_abstain_when_split 2s, LouhiModels.test_the_generat [ran] [tree 26dea69e852f] [world 2f1906870a] (2026-11-07T00:54:39Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 26dea69e852f] (2026-11-07T00:54:39Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 26dea69e852f] (2026-11-07T00:54:39Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 26dea69e852f] (2026-11-07T00:54:39Z)
## Log
- 2026-11-06T18:37:51Z created
- 2026-11-06T18:39:17Z set approved=True
- 2026-11-06T18:39:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3484.builder.md
- 2026-11-06T18:39:58Z focused
- 2026-11-06T18:40:00Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T00:04:53Z merged worktree-agent-aba5ea21d4ee00aff in merge train
- 2026-11-07T00:54:27Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/louhi.py', 'plugin/tests/test_louhi_loop.py']
- 2026-11-07T00:54:27Z scope: widened at merge to the reviewed lane's own diff (8e7b447f1), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T00:56:46Z done
- 2026-11-07T00:56:49Z committed afca369d5 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-2894 [FEATURE M, done, 4 steps] Model bench part 2: every held-out closed task's raw request as data (not only shadow rows), option descriptions for every decision (sy…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
## Lessons
- none: a builder lane; its findings are in the brief
## Plan gaps
- failed first: step 1 failing test, then the change
## Files touched
- plugin/tests/test_louhi_loop.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- scripts/probe-plugin-rename.sh
