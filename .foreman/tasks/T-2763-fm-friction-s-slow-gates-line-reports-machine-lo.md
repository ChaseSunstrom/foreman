---
id: T-2763
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/friction.py, plugin/lib/sampo/cli.py, plugin/tests/test_friction.py]
depends_on: []
source: self
created: 2026-11-03T04:14:00Z
updated: 2026-11-03T14:54:49Z
builder_model: sonnet
base: bea61f7e01fd4dd41ed0014c2626ee9fef4c2a77
base_tree: 89a75a51ac7a9bad9d5eee6921a98222e2815072
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T04:19:01Z
plan0_scope: [plugin/lib/sampo/friction.py, plugin/lib/sampo/cli.py, plugin/tests/test_friction.py]
lane_stop: merged 2026-11-03T04:32:30Z
verified: strong
---
# fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slow under load (or several gates slow in the same run) becomes one 'slow together under load' line
## Raw request
> CLEAN: fm friction's slow-gates line reports machine load as regression when several gates slow together (fmfriction.py:220-222: doctor, roundtrip, bench_hooks all 3-6x): say 'N gates slow together: likely machine load' as one line
## Interpretation
Reading 1 (chosen): the friction digest's 'slow gates (latest vs usual)' section (plugin/lib/sampo/friction.py:213-222) flags every gate whose latest run is over 1.5x its median. On 2026-11-03, doctor, roundtrip and bench_hooks all slowed 3-6x together because the machine was at load 30-47 on 16 cores, so the digest read load as three regressions. check_run (plugin/lib/sampo/cli.py:4982) records no load. Fix: record load per core in check_run's data. Then, in friction, slow gates from a run whose load per core was over 1, or two or more slow gates in the same run, become one line: 'N gates slow together under load (a, b, c): likely the machine, not the code'. Events without a load field fall back to the 'together' rule. Reading 2 (ruled out): drop the slow-gates section. It still catches a real single-gate regression.
## Assumptions (confidence)
## Acceptance criteria
- [x] a gate slow in a run whose load per core was over 1, or one of two or more gates slow in the same run, is reported as one machine-load line naming them; a lone slow gate on a quiet machine is still its own line — verify with `python3 plugin/tests/run.py test_friction`
- [x] check_run records the load per core, and the other gate suites stay green — verify with `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: os.getloadavg() / os.cpu_count(), as bench_hooks.load_per_core does, stored in check_run data; group runs[cmd] entries by their event so friction knows which slowed together. Likely outcome: about 20 lines plus two tests. Fails if: a check_run's results come from a reused pass at 0.0 s; those are already skipped.
2. Read load from the hook_ms events instead. Fails if: they aren't tied to a gate run.
3. Do less: a note when 2+ gates are slow, without recording load. Fails if: a lone gate slowed by load still reads as a regression.
Choice 1 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_friction: three gates slow in one loaded run make one load line; one slow gate on a quiet run stays a slow-gate line
2. [x] cli.py's check_run event carries load (getloadavg/cpu_count); friction.py groups the slow ones by run and load
## Resume here
<!-- auto -->
- 2026-11-03T04:47:32Z step 1/2: red tests in test_friction: three gates slow in one loaded run make one load line; one slow gate on a quiet run stays a slow-gate line
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/BRIEF.md
- failures met: timed out after 0s
## Docs impact
none: fm friction's own line is the doc
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength 2>&1 | tail -6` → exit 0 · Ran 53 tests in 24.5s (9 classes, 16 at a time; slowest: VerifyStrength 24s, Friction 18s, Repeat 12s) / OK [ran] [tree 01e6f05690b4] [world 2f1906870a] (2026-11-03T04:22:22Z)
- (step 2) `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength 2>&1 | tail -6` → exit 0 · Ran 53 tests in 24.5s (9 classes, 16 at a time; slowest: VerifyStrength 24s, Friction 18s, Repeat 12s) / OK [ran] [tree 01e6f05690b4] [world 2f1906870a] (2026-11-03T04:22:22Z)
- (step 2) `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength` → exit 0 · Ran 53 tests in 23.3s (9 classes, 16 at a time; slowest: VerifyStrength 23s, Friction 16s, Repeat 10s) / OK [ran] [tree 01e6f05690b4] [world 2f1906870a] (2026-11-03T04:22:48Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 124 (timed out after 600s) · timed out after 600s [ran] [tree 498cab0133aa] [world 2f1906870a] (2026-11-03T04:31:30Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 23 tests in 14.6s (5 classes, 16 at a time; slowest: Friction 14s, UserPromptSubmit 2s, BoardIdeas 1s) / OK [ran] [tree 255e2fab14f1] [world 2f1906870a] (2026-11-03T04:33:45Z)
- (ac 2) `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength` → exit 0 · Ran 53 tests in 21.6s (9 classes, 16 at a time; slowest: VerifyStrength 21s, Friction 15s, Repeat 10s) / OK [ran] [tree 255e2fab14f1] [world 2f1906870a] (2026-11-03T04:34:08Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 23 tests in 7.2s (5 classes, 16 at a time; slowest: Friction 7s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:48:23Z)
- (ac 2) `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength` → exit 0 · Ran 53 tests in 18.5s (9 classes, 16 at a time; slowest: VerifyStrength 18s, Friction 11s, Repeat 8s) / OK [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:48:23Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 124 (timed out after 600s) · Ran 153 tests across 4 files. [62.74s] / timed out after 600s [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:48:23Z)
- (step 1) `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength` → exit 0 · Ran 53 tests in 17.8s (9 classes, 16 at a time; slowest: VerifyStrength 17s, Friction 12s, Repeat 9s) / OK [ran] [tree 61be19e30b99] [world 2f1906870a] (2026-11-03T14:28:47Z)
- (audit intent) `self: read the merged diff; slow gates group by run and by load per core` → a slow gate under machine load reads as load, not a regression [tree 61be19e30b99] (2026-11-03T14:28:47Z)
- (audit edge) `self: read the merged diff; slow gates group by run and by load per core` → one gate under load reads '1 gate slow under load'; a lone slow gate on a quiet run stays its own line; runs without a load field read as quiet [tree 61be19e30b99] (2026-11-03T14:28:47Z)
- (audit adversary) `self: read the merged diff; slow gates group by run and by load per core` → no input crosses a trust boundary: load comes from os.getloadavg in check_run [tree 61be19e30b99] (2026-11-03T14:28:47Z)
- (audit self) `self: read the merged diff; slow gates group by run and by load per core` → no findings [tree 61be19e30b99] (2026-11-03T14:28:47Z)
- `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength` → exit 0 · Ran 53 tests in 13.8s (9 classes, 16 at a time; slowest: VerifyStrength 14s, Repeat 7s, Friction 7s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:53:42Z)
- (audit intent) `self: read the merged diff; slow gates group by run and by load per core` → a slow gate under machine load reads as load, not a regression [tree 1b964dd8dbe8] (2026-11-03T14:53:42Z)
- (audit edge) `self: read the merged diff; slow gates group by run and by load per core` → one gate under load reads '1 gate slow under load'; a lone slow gate on a quiet run stays its own line; runs without a load field read as quiet [tree 1b964dd8dbe8] (2026-11-03T14:53:42Z)
- (audit adversary) `self: read the merged diff; slow gates group by run and by load per core` → no input crosses a trust boundary: load comes from os.getloadavg in check_run [tree 1b964dd8dbe8] (2026-11-03T14:53:42Z)
- (audit self) `self: read the merged diff; slow gates group by run and by load per core` → no findings [tree 1b964dd8dbe8] (2026-11-03T14:53:42Z)
- `python3 plugin/tests/run.py test_friction test_gate_friction test_verify_strength` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T14:53:42Z [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:54:16Z)
- (audit intent) `self: read the merged diff; slow gates group by run and by load per core` → a slow gate under machine load reads as load, not a regression [tree 1b964dd8dbe8] (2026-11-03T14:54:16Z)
- (audit edge) `self: read the merged diff; slow gates group by run and by load per core` → one gate under load reads '1 gate slow under load'; a lone slow gate on a quiet run stays its own line; runs without a load field read as quiet [tree 1b964dd8dbe8] (2026-11-03T14:54:16Z)
- (audit adversary) `self: read the merged diff; slow gates group by run and by load per core` → no input crosses a trust boundary: load comes from os.getloadavg in check_run [tree 1b964dd8dbe8] (2026-11-03T14:54:16Z)
- (audit self) `self: read the merged diff; slow gates group by run and by load per core` → no findings [tree 1b964dd8dbe8] (2026-11-03T14:54:16Z)
## Log
- 2026-11-03T04:14:00Z created
- 2026-11-03T04:18:39Z planned from capture
- 2026-11-03T04:18:50Z set approved=True
- 2026-11-03T04:18:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2763.builder.md
- 2026-11-03T04:18:59Z focused
- 2026-11-03T04:19:01Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T04:32:30Z merged worktree-agent-a9de79219f8f43976 (3 file(s))
- 2026-11-03T04:32:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9de79219f8f43976
- 2026-11-03T04:32:50Z focused
- 2026-11-03T04:50:01Z paused: focus moved to T-2756
- 2026-11-03T05:37:54Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T05:37:54Z focused
- 2026-11-03T05:37:55Z scope: files outside the scope since focus came from other lanes' merge commits, not this task's edits
- 2026-11-03T05:48:23Z paused: focus moved to T-2758
- 2026-11-03T14:28:25Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T14:28:25Z focused
- 2026-11-03T14:43:49Z paused: focus moved to T-2791
- 2026-11-03T14:53:26Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T14:53:26Z focused
- 2026-11-03T14:54:49Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2748 [CLEAN M, active, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_friction.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/lib/sampo/friction.py, plugin/tests/test_friction.py; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out at 600 s under machine load ~55 on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- Group symptoms by their shared cause before reporting each
## Plan gaps
- failed first: step 1 red tests in test_friction: three gates slow in one loaded run make one load line; one slow gate on…
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/sampo/friction.py
- plugin/lib/sampo/cli.py
