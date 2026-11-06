---
id: T-3398
type: FEATURE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/bus.py, plugin/lib/sampo/cli.py, plugin/tests/test_bus.py]
depends_on: []
source: discovered
created: 2026-11-06T07:11:49Z
updated: 2026-11-06T10:42:05Z
base: 3efd1dced8ac2fa7cc7b72284209d58ea489679c
base_tree: e864306cb1b8cad4202b56cab8dca94a52415123
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T08:46:00Z
plan0_scope: []
builder_returned: 2026-11-06T09:13:54Z
lane_stop: merged 2026-11-06T10:41:20Z
verified: strong
---
# Sampo task finish releases the task's leases (today they wait 20 min to expire, holding…
## Raw request
> FEATURE: sampo task finish releases the task's leases (today they wait 20 min to expire, holding hub files from other lanes) (T-3371 review)
## Interpretation
Reading 1: release in the shared status-change path (cli.mutate). Reading 2: per verb. Chose 1: all close verbs share it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a closed task's leases are released at once; another task's stay — verify with `python3 plugin/tests/run.py test_bus -k closing_a_task`
## Non-goals
## Approach (options → choice → why)
1) release in cli.mutate when status enters a closed state; fails if: a verb bypasses mutate 2) use what exists: bus.release per verb; fails if: a verb is missed 3) do less: only finish; fails if: done/drop leak. Choice 1 (85%): mutate + bus.release, failure logged
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then release in mutate
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 -m unittest plugin.tests.test_bus.Lease.test_closing_a_task_releases_its_leases_at_once_and_leaves_another_tasks 2>&1 | tail -3` → ✗ exit 1 · FAILED (errors=1) / fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hides the exit), so it counts as a failure [ran] [tree 9602ae97dddc] [world 2f1906870a] (2026-11-06T08:46:19Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_bus.py` → exit 0 · Ran 24 tests in 7.365s / OK [ran] [tree e5bd163a0cdd] [world 2f1906870a] (2026-11-06T08:46:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_bus test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.28s] [ran] [tree e5bd163a0cdd] [world 2f1906870a] (2026-11-06T08:48:56Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_bus.py` → exit 0 · Ran 27 tests in 14.355s / OK [ran] [tree 367a0ea891c3] [world 2f1906870a] (2026-11-06T08:58:03Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 367a0ea891c3] [world 2f1906870a] (2026-11-06T08:58:09Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 367a0ea891c3] [world 2f1906870a] (2026-11-06T08:58:18Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree d4e495c56c3a] (2026-11-06T10:41:22Z)
- (ac 1) `python3 plugin/tests/run.py test_bus -k closing_a_task` → exit 0 · Ran 1 tests in 0.8s (1 jobs, 16 at a time; slowest: Lease 0s) / OK [ran] [tree d4e495c56c3a] [world 2f1906870a] (2026-11-06T10:41:25Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree d4e495c56c3a] (2026-11-06T10:41:25Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree d4e495c56c3a] (2026-11-06T10:41:25Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree d4e495c56c3a] (2026-11-06T10:41:25Z)
## Log
- 2026-11-06T07:11:49Z created
- 2026-11-06T08:45:53Z planned: it has criteria and steps
- 2026-11-06T08:45:59Z focused
- 2026-11-06T08:46:00Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T09:43:37Z criterion 1 verify: `python3 -m unittest plugin/tests/test_bus.py -k closing_a_task` → `python3 plugin/tests/run.py test_bus -k closing_a_task`
- 2026-11-06T09:43:37Z criterion 1 verify moved from a bare 'python3 -m unittest' form (fails from the repo root, where lane merge runs it) to plugin/tests/run.py (T-3411 makes this automatic)
- 2026-11-06T10:41:20Z merged worktree-agent-ae9883e0f088bf929 (3 file(s))
- 2026-11-06T10:41:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae9883e0f088bf929
- 2026-11-06T10:41:21Z focused
- 2026-11-06T10:41:22Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/bus.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_bus.py']
- 2026-11-06T10:41:22Z scope: widened at merge to the reviewed lane's own diff (29f07d618), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:42:02Z done
- 2026-11-06T10:42:05Z committed a846d5717 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- T-2870 [FIX S, done, 1 steps] Sampo lease drop run from a builder lane drops every lease the session holds (16 at once…
- decision 2026-11-05: Hold main-checkout test runs and closes after T-3151's close until the queued merges (T-3087, T-3108, then T-3053's chain) land
- similar finished tasks took 1–9 steps
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 test then release in mutate
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/bus.py
- CHANGELOG.md
