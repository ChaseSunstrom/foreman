---
id: T-3387
type: SECURITY
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:54:31Z
updated: 2026-11-06T09:43:38Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aa22e7ac5895ddb7c
lane_branch: worktree-agent-aa22e7ac5895ddb7c
base: 1e1c29e31cc159395ca6ac04cedb714d3fb14c89
base_tree: c52b066e571b19f07ff3d5cc92292ff201c55ec1
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T07:43:22Z
plan0_scope: []
builder_returned: 2026-11-06T08:21:48Z
---
# fmguard.py:~4186 reads '#!/usr/bin/env -S python3' as interpreter '-S', so kind is None…
## Raw request
> SECURITY: fmguard.py:~4186 reads '#!/usr/bin/env -S python3' as interpreter '-S', so kind is None and a script run by path (./x) is never read: an agent could write an env -S script holding a blocked command and run it. Skip env flags (-S, -i, -u NAME) and NAME=val words when finding the interpreter; test (T-3363 review)
## Interpretation
Reading 1: env's own options and NAME=val words precede the interpreter, so skip them. Reading 2 (ruled out): reject any env shebang with options; it would break legit scripts.
## Assumptions (confidence)
## Acceptance criteria
- [ ] env -S/-i shebang scripts are read like plain ones — verify with `python3 plugin/tests/run.py test_guard_exec_vectors.Review.test_env_shebang_options_are_skipped`
## Non-goals
## Approach (options → choice → why)
1) Regex on the head line; fails if: options like -S carry args it misreads. 2) One helper _shebang_interp skipping env options and NAME=val; likely outcome: exact, one call site. 3) use what exists: nothing parses shebangs elsewhere (grep), so extend the single site; fails if: none. 4) do less: only skip -S; fails if: -i/-u still hide it. Choice 2 (80%): small, exact; unparseable env reads as sh so it is still read.
## Risks and rollback
## Execution prompt
## Steps
1. [x] helper + test
## Resume here
<!-- auto -->
- 2026-11-06T08:20:40Z steps 1/1 done
- git: worktree-agent-aa22e7ac5895ddb7c; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard_exec_vectors.py
- touched since last checkpoint: .fm-scratch/replay_usrbin.py, plugin/lib/fmguard.py, plugin/tests/test_guard_exec_vectors.py
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest plugin.tests.test_guard_exec_vectors.Review.test_env_shebang_options_are_skipped plugin.tests.test_guard_exec_vectors.Review.test_executable_with_a_shebang_is_read` → ✗ exit 1 (never ran: the test module test_guard_exec_vectors couldn't import) · Ran 2 tests in 0.000s / FAILED (errors=2) [ran] [tree 8fffc2ec7bb7] [world 2f1906870a] (2026-11-06T07:43:38Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_guard_exec_vectors.py -k env_shebang -k executable_with_a_shebang` → exit 0 · Ran 2 tests in 0.049s / OK [ran] [tree 8fffc2ec7bb7] [world 2f1906870a] (2026-11-06T07:43:44Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_doctor test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_overrefusal test_guard_pipes test_guard_sampo test_left_out test_models test_rename_scan test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [23.60s] [ran] [tree 8fffc2ec7bb7] [world 2f1906870a] (2026-11-06T07:44:48Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 341 tests in 221.9s (100 jobs, 16 at a time; slowest: Mutation 20s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 9s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 9024e68a2fbc] [world 2f1906870a] (2026-11-06T07:59:01Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_doctor test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_overrefusal test_guard_pipes test_guard_sampo test_left_out test_models test_rename_scan test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [24.93s] [ran] [tree 9024e68a2fbc] [world 2f1906870a] (2026-11-06T08:00:14Z)
- (step 1) `python3 plugin/tests/run.py test_guard_exec_vectors` → exit 0 · Ran 51 tests in 5.6s (7 jobs, 16 at a time; slowest: ScriptCache 2s, ScriptHook 1s, Review 0s) / OK [ran] [tree e1920601cd4d] [world 2f1906870a] (2026-11-06T08:12:50Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 343 tests in 27.8s (100 jobs, 16 at a time; slowest: Mutation 16s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 7s, Latency 6s) / OK [ran] [tree e1920601cd4d] [world 2f1906870a] (2026-11-06T08:13:39Z)
- (step 1) `python3 plugin/tests/run.py test_guard_exec_vectors` → exit 0 · Ran 52 tests in 1.9s (7 jobs, 16 at a time; slowest: ScriptCache 1s, ScriptHook 0s, Review 0s) / OK [ran] [tree 94dd8f4b609a] [world 2f1906870a] (2026-11-06T08:20:40Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 344 tests in 11.0s (100 jobs, 16 at a time; slowest: Mutation 11s, Latency 5s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 5s) / OK [ran] [tree 94dd8f4b609a] [world 2f1906870a] (2026-11-06T08:20:51Z)
## Log
- 2026-11-06T06:54:31Z created
- 2026-11-06T07:43:10Z planned: it has criteria and steps
- 2026-11-06T07:43:21Z focused
- 2026-11-06T07:43:22Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T09:43:38Z criterion 1 verify: `python3 -m unittest plugin.tests.test_guard_exec_vectors.Review.test_env_shebang_options_are_skipped` → `python3 plugin/tests/run.py test_guard_exec_vectors.Review.test_env_shebang_options_are_skipped`
- 2026-11-06T09:43:38Z criterion 1 verify moved from a bare 'python3 -m unittest' form (fails from the repo root, where lane merge runs it) to plugin/tests/run.py (T-3411 makes this automatic)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1553-review: Verdict:** changes needed. This is a read-only review, so I did not run any of the reproducers. Each finding comes from reading the code. [stale:…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
