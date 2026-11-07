---
id: T-3600
type: SECURITY
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:47:35Z
updated: 2026-11-07T05:16:07Z
lane: ~/.claude/foreman.lanes/T-3600
lane_branch: foreman/T-3600
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-07T04:30:25Z
plan0_scope: []
---
# The guard reads a sampo verb before shell variables: V=serve; sampo $V (and V=cpu; sampo…
## Raw request
> SECURITY: the guard reads a sampo verb before shell variables: V=serve; sampo $V (and V=cpu; sampo $V cap 10) skip the remote/system refusal, as does any verb-gated row (_fm_subcommand gets the raw words). Resolve the command's known variables in fm_args before _fm_subcommand, and treat an unresolvable verb word as the strictest gated verb; probe rows in test_guard_cpu (found in T-3592 review)
## Interpretation
Reading 1 (chosen): the Ward reads the sampo verb and the words its gates key on (serve, pause off, rule rm, plugins install, agents uninstall, night --install, --allow core) as raw words, so one the shell fills in at run time (V=serve; sampo $V, sampo $(echo serve), sampo {serve,}, echo serve | xargs sampo, an alias or computed path for sampo, env -S 'sampo serve') runs a gated verb unrefused: resolve the line's known variables, refuse a verb or gated word still not literal as text the guard can't read. Reading 2 (ruled out): refuse every sampo call holding any computed word: sampo task show $T and --run "$CMD" are ordinary and key no category, so that over-refuses for no safety.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Every bypass shape (computed verb or option word, gated word, --allow value, xargs, alias, env -S, computed path) is refused and literal calls pass — verify with `nice -n 10 python3 plugin/tests/run.py test_guard_verb`
- [ ] Existing guard suites stay green — verify with `nice -n 10 python3 plugin/tests/run.py -p 'test_guard*.py'`
## Non-goals
## Approach (options → choice → why)
1) per-verb patches (serve, cpu) for $V. Likely outcome: those two close; fails if: the next gated verb or shape (xargs, alias, braces) repeats the bug. 2) use what exists: the fm block already resolves names for T-0587 (_with_vars, known) and the guard's can't-read refusal (_unread, unliftable): resolve fm words through known vars (split as bash splits), feed xargs stdin as an unknown word, and refuse any non-literal word at or before the verb, among a gated verb's words, or as an --allow value; plus env -S unwrapped in _strip_wrappers, an alias whose value names sampo or isn't literal, a computed program word read as sampo when the line names sampo. Likely outcome: every shape refused, literal calls unchanged; fails if: a real command with a computed word before the verb now refuses (checked by replaying real commands old vs new). 3) do less: refuse any sampo call holding any non-literal word. Likely outcome: closes all; fails if: ordinary sampo task show $T, --run "$CMD" calls refuse. Choice 2 (80%): one root-cause rule where every fm call routes, literal calls untouched, built from helpers already there.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing test per bypass shape (test_guard_verb.py)  <- CURRENT
2. [x] Fix in fmguard: resolve fm words, non-literal verb/gated word refusal, xargs, env -S, alias, computed name
3. [x] Run all guard suites, replay real commands old vs new, measure PreToolUse latency
4. [x] Review fixes test-first: nameref, words a verb runs or stores, a computed command word on a line naming sampo elsewhere, source <(…)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard_verb` → ✗ exit 1 (never ran: the test module test_guard_verb couldn't import) · Ran 1 tests in 152.8s (1 jobs, 16 at a time; slowest: ComputedVerb 0s) / FAILED (1 classes: test_guard_verb.ComputedVerb) [ran] [tree 0d682c0b89e5] [world 2f1906870a] (2026-11-07T04:37:58Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard_verb` → exit 0 · Ran 8 tests in 193.8s (1 jobs, 16 at a time; slowest: ComputedVerb 1s) / OK [ran] [tree 80d57db27070] [world 2f1906870a] (2026-11-07T04:41:29Z)
- (step 1) `cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/base/plugin/tests && nice -n 10 python3 -m unittest test_guard_verb` → ✗ exit 1 · Ran 8 tests in 0.272s / FAILED (failures=59) [ran] [tree c35035f87016] [world 2f1906870a] (2026-11-07T04:41:58Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard_verb` → exit 0 · Ran 10 tests in 0.6s (1 jobs, 16 at a time; slowest: ComputedVerb 0s) / OK [ran] [tree 216b30cb49b4] [world 2f1906870a] (2026-11-07T04:57:38Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 339 tests in 16.6s (95 jobs, 16 at a time; slowest: Mutation 17s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 10s, GuardAgainstBash.test_every_form_that_runs_a_dangerou [ran] [tree 216b30cb49b4] [world 2f1906870a] (2026-11-07T04:57:58Z)
- (step 4) `cd plugin/tests && nice -n 10 python3 -m unittest test_guard_verb` → ✗ exit 1 · Ran 13 tests in 1.095s / FAILED (failures=19) [ran] [tree 3743c5c50ed2] [world 2f1906870a] (2026-11-07T05:08:28Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 342 tests in 47.5s (119 jobs, 16 at a time; slowest: Mutation 47s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 20s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 0e007d8275f7] [world 2f1906870a] (2026-11-07T05:16:07Z)
## Log
- 2026-11-07T03:47:35Z created
- 2026-11-07T04:30:00Z planned: it has criteria and steps
- 2026-11-07T04:30:05Z lane: ~/.claude/foreman.lanes/T-3600 on foreman/T-3600
- 2026-11-07T04:30:25Z focused
- 2026-11-07T04:30:25Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-07T05:00:55Z lane commit 690c6be27. Replay of 46,197 real Bash commands (14 days of session logs) old vs new guard: 14 changed (0.03%), all stricter, none looser: 3 loops over 'serve --help' now read as sampo serve (same as typed literally), 2 shell functions wrapping sampo decide "$1", 6 python heredocs spawning sampo with a computed verb (*args, a loop var), 2 quote-blind readings of 'fm [a-z]' grep patterns, 1 loop whose words include 'source'. Guard check latency (median of 100, loaded box): sampo next 0.25 -> 0.26-0.32 ms, task show T-1 0.27 -> 0.29-0.35 ms, evidence --run 1.25-1.34 -> 1.24-1.27 ms (noise). Captured T-3619 for out-of-scope gaps (alias for rm, watch, a computed --run flag word, unquoted $( ) command word).
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
