---
id: T-3538
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T21:55:04Z
updated: 2026-11-07T00:57:41Z
group: guard refuses legitimate lane and task work
lane: ~/.claude/foreman.lanes/T-3538
lane_branch: foreman/T-3538
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-07T00:38:56Z
plan0_scope: []
---
# Interpreter-code-driving-fm fired 16 times, 10 on a heredoc fed to python whose string…
## Raw request
> FIX: interpreter-code-driving-fm fired 16 times, 10 on a heredoc fed to python whose string literals merely mention plugin module paths (fmguard.py:2126-2138, 250): strip string literals before the internals match, with a FORMS row that passes
## Interpretation
Reading 1 (chosen): a python heredoc whose line isn't the strict unit form (cd DIR; python3 -, other commands chained before python with && or ;, flags like -B) is read as shell text, so an edit script whose string literals or comments merely name Sampo modules is refused; such bodies should get the AST reading units already get, which ignores strings and comments, while real imports, dynamic code and unknown run folders still refuse. Reading 2 (ruled out): strip quoted strings from all shell text, including grep patterns that name sampo imports: a shell string can be code (bash -c, eval, python -c), so it can't be blanked without a proof.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a python heredoc after cd DIR; or a chain of plain commands, or with -B, whose only Sampo mention is in strings or comments passes; one that imports sampo, execs its string or imports anything in an unknown folder is still refused — verify with `nice -n 10 python3 plugin/tests/run.py test_guard`
- [ ] the FORMS corpus and the guard suites stay green — verify with `nice -n 10 python3 plugin/tests/run.py test_guard_diff test_guard_sampo test_guard_overrefusal`
## Non-goals
## Approach (options → choice → why)
1) Blank string tokens of every heredoc body in the shell text before the internals match. Fails if: a bash or data body that tokenizes as python, or exec(s)/subprocess of a string, slips through. 2) Loosen _python_units for every caller. Fails if: _proved_writes and _quoted_paths trust a run folder they can't know. 3) use what exists: an opt-in loose mode of _python_units used only by _drives_fm, so the existing AST proof reads the body (strings and comments never count; exec, subprocess, odd imports refuse) with an unknown run folder (any import refuses). Likely outcome: the edit-script refusals pass, real use still refused. 4) do less: only accept cd DIR; before python. Likely outcome: half the cases (cp ... && python3 - stays refused). Choice 3 (85%): reuses the proof the strict form already has; the lead is checked plain (no quotes, parens, redirects, compound words, PATH/alias/eval, env-sensitive assignment), so it is no riskier than the same commands on an earlier line.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: loose-lead heredocs naming Sampo only in strings pass; real imports, exec and imports in an unknown folder still refuse  <- CURRENT
2. [x] loose mode in _python_units for _drives_fm; _run_dir returns None for a non-plain lead
3. [x] run the guard suites and the FORMS corpus
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k HeredocAfterALead -k the_hint_says_split test_guard_overrefusal test_guard` → ✗ exit 1 · Ran 4 tests in 23.6s (2 jobs, 16 at a time; slowest: HeredocAfterALead 0s, InterpreterWrites 0s) / FAILED (2 classes: test_guard_overrefusal.HeredocAfterALead, test_guard.InterpreterWrites) [ran] [tree 38f8a583e3eb] [world 2f1906870a] (2026-11-07T00:42:31Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k HeredocAfterALead -k the_hint_says_split test_guard_overrefusal test_guard` → exit 0 · Ran 4 tests in 15.5s (2 jobs, 16 at a time; slowest: HeredocAfterALead 0s, InterpreterWrites 0s) / OK [ran] [tree f204f17d644e] [world 2f1906870a] (2026-11-07T00:47:41Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_overrefusal test_guard_cases test_guard_debris test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_hardening test_guard_mine test_guard_pipes test_guard_sampo test_guard_state_key test_guard_try test_guard_latency test_guard_diff` → exit 0 · Ran 346 tests in 34.2s (126 jobs, 16 at a time; slowest: Mutation 12s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 10s, Latency 7s) / OK [ran] [tree f204f17d644e] [world 2f1906870a] (2026-11-07T00:48:24Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_overrefusal test_guard_cases test_guard_debris test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_hardening test_guard_mine test_guard_pipes test_guard_sampo test_guard_state_key test_guard_try test_guard_latency test_guard_diff` → exit 0 · Ran 346 tests in 14.6s (106 jobs, 16 at a time; slowest: Mutation 14s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 9s, GuardAgainstBash.test_every_form_that_runs_a_dangerou [ran] [tree e77bdef391f4] [world 2f1906870a] (2026-11-07T00:57:41Z)
## Log
- 2026-11-06T21:55:04Z created
- 2026-11-07T00:38:35Z planned: it has criteria and steps
- 2026-11-07T00:38:39Z lane: ~/.claude/foreman.lanes/T-3538 on foreman/T-3538
- 2026-11-07T00:38:55Z focused
- 2026-11-07T00:38:56Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-07T00:48:34Z steer: T-3554 folded in (same rule, same lines): the hint says split into two commands when the refusal's write-then-run suffix applies; test_the_hint_says_split_when_the_refusal_does
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1194 [FIX M, done, 2 steps] Guard parses python -c code like quoted heredoc bodies before calling it Foreman-driving — lesson: Loosening a guard rule needs the mined r…
- T-2068 [FEATURE M, done, 3 steps] The interpreter-code guard refusal names the clause that fired: Foreman's module named in shell text, python settings, code that doesn'…
- T-2261 [FIX M, done, 3 steps] Guard (for the user's review, touches the guard): the interpreter-code rule blocks a… — lesson: widen a guard rule by naming the exact read…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
