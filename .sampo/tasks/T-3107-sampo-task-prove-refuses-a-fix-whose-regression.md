---
id: T-3107
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_verify_strength.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-05T03:07:29Z
updated: 2026-11-06T16:29:48Z
base: fe5138e95ef19b4432555545e84eee4cc68828d2
base_tree: 905bf469abae626cb969ef4e99f7bf8c00c2ccf4
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:47:02Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_verify_strength.py, CHANGELOG.md]
builder_returned: 2026-11-06T13:08:00Z
lane_stop: merged 2026-11-06T13:53:06Z
verified: strong
lane_verified: d99caf544ce23b0d7b917fa4839f60e7c9a539ca
---
# sampo task prove accepts a regression test that already existed: with no changed test file it runs the check on the start tree as it was and now
## Raw request
> sampo task prove refuses a FIX whose regression test already existed and was red ('changed no test files: write the test first'), though the start tree vs now with that test is the proof; T-2943 needed a 'Regression test: none' section instead: prove should accept an existing test that is red on the start tree
## Interpretation
prove with no changed test file runs CMD on the start tree as-is (red) and now (green)
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo task prove ID --run CMD on a task that changed no test file runs CMD on the start tree (its own tests as they were) and on the current tree: red then green is proved, green on both says it passes without the change; a task with no start commit still refuses — verify with `python3 plugin/tests/run.py test_verify_strength`
## Non-goals
## Approach (options → choice → why)
Drop the no-tests refusal in cli.task_prove; empty tests list means nothing is copied. Existing verdicts cover green-on-both.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_verify_strength: an existing test red on the start tree and green after a code-only fix is proved; 'true' with no changed test says it passes without the change (replacing the 'changed no test files' refusal test)
2. [x] drop the refusal in cli.task_prove: no changed tests means nothing is copied over
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 19 tests in 46.5s (2 jobs, 16 at a time; slowest: VerifyStrength 13s, Repeat 8s) / OK [ran] [tree a9448a915ce8] [world 2f1906870a] (2026-11-06T12:48:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_strength test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [19.75s] [ran] [tree a9448a915ce8] [world 2f1906870a] (2026-11-06T12:52:20Z)
- (step 2) `python3 plugin/tests/run.py test_verify_strength` → ✗ exit 1 · Ran 21 tests in 109.9s (21 jobs, 16 at a time; slowest: VerifyStrength.test_a_timed_out_check_kills_its_whole_process_group 5s, Repeat.test_timed_out_runs_stay_out_of_the_numbers 3s, VerifyStrength.te [ran] [tree c91b9abee3e4] [world 2f1906870a] (2026-11-06T13:04:57Z)
- (step 2) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 21 tests in 168.1s (21 jobs, 16 at a time; slowest: VerifyStrength.test_a_timed_out_check_kills_its_whole_process_group 5s, VerifyStrength.test_cached_pass_depends_on_the_environment_and_slow_gate [ran] [tree a4e35e8ee665] [world 2f1906870a] (2026-11-06T13:07:49Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c4d1f13676e6] (2026-11-06T13:53:11Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 21 tests in 45.7s (21 jobs, 16 at a time; slowest: VerifyStrength.test_a_timed_out_check_kills_its_whole_process_group 5s, VerifyStrength.test_cached_pass_depends_on_the_environment_and_slow_gates [ran] [tree c4d1f13676e6] [world 2f1906870a] (2026-11-06T13:54:01Z)
- (step 1) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 21 tests in 45.7s (21 jobs, 16 at a time; slowest: VerifyStrength.test_a_timed_out_check_kills_its_whole_process_group 5s, VerifyStrength.test_cached_pass_depends_on_the_environment_and_slow_gates [ran] [tree c4d1f13676e6] [world 2f1906870a] (2026-11-06T13:54:01Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c4d1f13676e6] (2026-11-06T13:54:01Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c4d1f13676e6] (2026-11-06T13:54:01Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c4d1f13676e6] (2026-11-06T13:54:01Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree c4d1f13676e6] (2026-11-06T13:54:01Z)
## Log
- 2026-11-05T03:07:29Z created
- 2026-11-05T03:10:33Z planned from capture
- 2026-11-05T03:10:33Z set approved=True
- 2026-11-05T03:10:33Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md']
- 2026-11-05T03:10:33Z blocked: after T-3087's merge (cli.py); then a builder slot
- 2026-11-06T03:53:51Z unblocked
- 2026-11-06T12:47:01Z focused
- 2026-11-06T12:47:02Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T13:53:06Z merged worktree-agent-a2e1950bb28a78198 (2 file(s))
- 2026-11-06T13:53:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2e1950bb28a78198
- 2026-11-06T13:53:07Z focused
- 2026-11-06T13:53:10Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T13:53:10Z scope: widened at merge to the reviewed lane's own diff (d99caf544), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T13:57:17Z done
- 2026-11-06T13:57:20Z committed beec10300 (1 file)
- 2026-11-06T16:29:48Z verified: the full suite is green on 1078ed22d, which contains d99caf544
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-01: [cites: user steer 2026-11-01: unmeasured growth waits instead of filing a subtraction task] [check: python3 plugin/tests/run.py test_genesis.LeanSu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_sca…
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md, plugin/lib/sampo/cli.py, plugin/tests/test_verify_strength.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_verify_strength.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
