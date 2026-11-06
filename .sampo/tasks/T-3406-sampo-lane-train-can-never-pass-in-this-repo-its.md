---
id: T-3406
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py]
depends_on: []
source: discovered
created: 2026-11-06T08:28:28Z
updated: 2026-11-06T10:17:48Z
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 048e9221710e9a3e8156622651d6ec39b4fdc8f8
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:29:24Z
plan0_scope: []
builder_returned: 2026-11-06T09:05:48Z
lane_stop: merged 2026-11-06T09:45:38Z
verified: strong
unproven: [meaning]
---
# Sampo lane train can never pass in this repo: its gates run in a scratch worktree, where…
## Raw request
> FIX: sampo lane train can never pass in this repo: its gates run in a scratch worktree, where fm doctor FAILs 'statusline' and 'rules symlink' (both compare install wiring to the worktree's plugin path, not the installed checkout's). Doctor run from a git worktree of the installed repo should report install-wiring checks against the installed root (or WARN 'checking a worktree'), never FAIL; test with a real worktree (T-3380 follow-up, 2026-11-06)
## Interpretation
Reading 1: judge wiring against the installed root, WARN when run from a sibling worktree. Reading 2 (ruled out): skip the checks everywhere, since a broken real install must still FAIL.
## Assumptions (confidence)
## Acceptance criteria
- [x] Doctor in a worktree of the installed repo has no FAIL for statusline or rules symlink — verify with `python3 plugin/tests/run.py test_doctor -k worktree`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: doctor already finds the install via settings and link; compare against it. Fails if settings lack a path. 2) WARN when both paths share a git common dir, one helper; likely outcome: both checks WARN in worktrees. 3) Skip checks under any worktree; fails if it hides a real broken install. Choice 2 (80%): smallest, keeps real FAIL.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1473, T-1579, T-1588, T-1589.
## Execution prompt
## Steps
1. [x] test then helper in doctor.py
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 -m unittest plugin.tests.test_doctor -k worktree` → ✗ exit 1 (never ran: the test module test_doctor couldn't import) · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree fe5fd4d706d7] [world 2f1906870a] (2026-11-06T08:29:47Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 115 tests in 47.7s (44 jobs, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Timing 2s) / OK [ran] [tree fe5fd4d706d7] [world 2f1906870a] (2026-11-06T08:31:10Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.19s] [ran] [tree fe5fd4d706d7] [world 2f1906870a] (2026-11-06T08:32:51Z)
- (step 1) `python3 plugin/tests/run.py plugin/tests/test_doctor.py -k worktree_of_installed` → ✗ exit 1 · run.py: no test matches plugin/tests/test_doctor.py with -k worktree_of_installed [ran] [tree c4bd4f81d7b5] [world 2f1906870a] (2026-11-06T08:44:47Z)
- (step 1) `python3 plugin/tests/run.py worktree_of_installed` → ✗ exit 1 · Ran 1 tests in 3.8s (1 jobs, 16 at a time; slowest: Checks 0s) / FAILED (1 classes: test_doctor.Checks) [ran] [tree c710e19c919f] [world 2f1906870a] (2026-11-06T08:44:55Z)
- (step 1) `python3 plugin/tests/run.py worktree_of_installed` → exit 0 · Ran 1 tests in 19.1s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree c9a0221adc5e] [world 2f1906870a] (2026-11-06T08:45:26Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [14.12s] [ran] [tree c9a0221adc5e] [world 2f1906870a] (2026-11-06T08:46:05Z)
- (step 1) `python3 plugin/tests/run.py worktree_of_installed` → exit 0 · Ran 1 tests in 21.4s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree c4f9193c4199] [world 2f1906870a] (2026-11-06T08:58:19Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree c4f9193c4199] [world 2f1906870a] (2026-11-06T08:58:23Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree c4f9193c4199] [world 2f1906870a] (2026-11-06T08:59:02Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 876219905759] (2026-11-06T09:45:41Z)
- (step 1) `python3 -m unittest plugin.tests.test_doctor -k worktree` → ✗ exit 1 (never ran: the test module test_doctor couldn't import) · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree 876219905759] [world 2f1906870a] (2026-11-06T09:45:43Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree b9c0d8bd343b] (2026-11-06T09:56:01Z)
- (step 1) `python3 -m unittest plugin.tests.test_doctor -k worktree` → exit 0 · Ran 2 tests in 0.5s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree b9c0d8bd343b] [world 2f1906870a] (2026-11-06T09:56:03Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor -k worktree` → exit 0 · Ran 2 tests in 0.4s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree b9c0d8bd343b] [world 2f1906870a] (2026-11-06T09:56:05Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree b9c0d8bd343b] (2026-11-06T09:56:05Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree b9c0d8bd343b] (2026-11-06T09:56:05Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree b9c0d8bd343b] (2026-11-06T09:56:05Z)
## Log
- 2026-11-06T08:28:28Z created
- 2026-11-06T08:29:14Z planned: it has criteria and steps
- 2026-11-06T08:29:23Z focused
- 2026-11-06T08:29:24Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T08:43:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a28beeb3c18265626 (branch worktree-agent-a28beeb3c18265626 kept: not merged)
- 2026-11-06T08:44:07Z focused
- 2026-11-06T09:43:36Z criterion 1 verify: `python3 -m unittest plugin.tests.test_doctor -k worktree` → `python3 plugin/tests/run.py test_doctor -k worktree`
- 2026-11-06T09:43:36Z criterion 1 verify moved from a bare 'python3 -m unittest' form (fails from the repo root, where lane merge runs it) to plugin/tests/run.py (T-3411 makes this automatic)
- 2026-11-06T09:45:38Z merged worktree-agent-a0e490b59a572a909 (2 file(s))
- 2026-11-06T09:45:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0e490b59a572a909
- 2026-11-06T09:45:39Z focused
- 2026-11-06T09:45:41Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/doctor.py', 'plugin/tests/test_doctor.py']
- 2026-11-06T09:45:41Z scope: widened at merge to the reviewed lane's own diff (c70f6fb7d), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T09:50:02Z paused: focus moved to T-3411
- 2026-11-06T09:55:58Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T09:55:58Z focused
- 2026-11-06T09:56:29Z done
- 2026-11-06T10:17:48Z not reverted: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_close_gates.CloseGates, test_docs.MapShards, test_docs.PluginFiles already fail on c70f6fb7d's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: pending T-2184] Standing rule: every capability Genesis builds must…
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 test then helper in doctor.py
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/sampo/doctor.py
- CHANGELOG.md
