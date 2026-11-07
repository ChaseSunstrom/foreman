---
id: T-3612
type: CLEAN
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-07T04:30:02Z
updated: 2026-11-07T04:42:49Z
lane: ~/.claude/foreman.lanes/T-3612
lane_branch: foreman/T-3612
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 1
predict_attempts: 1
plan0_at: 2026-11-07T04:34:05Z
plan0_scope: []
---
# Guessed sampo verbs with no hint cost retries: events.jsonl unknown_word counts 21x…
## Raw request
> CLEAN: guessed sampo verbs with no hint cost retries: events.jsonl unknown_word counts 21x version/--version, 18x models, 11x task scope, 5x where, plus lane awaiting and affected; add a hint for each in the TOMBSTONES/ALIASES tables (cli.py ~6513, ~8958): task scope -> sampo task set ID --scope, --version prints the plugin version, models -> the verb that lists local models (self-improvement pass)
## Interpretation
Agents guess sampo verbs that don't exist (state/events.jsonl unknown_word: --version/version 21, models 18, task scope 11, where 6, task approve 7, lane awaiting 3, affected 1) and each costs a retry with only an edit-distance guess. Each top guess should either run what it meant or name the real verb in one line.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo --version and sampo version print the plugin version; models, where, task scope, scope, lane awaiting, affected and task approve each name the real verb — verify with `nice -n 10 python3 plugin/tests/run.py test_gate_friction`
## Non-goals
## Approach (options → choice → why)
Options: (1) aliases for every guess; (2) a new GUESSES hint table; (3) reuse what exists: a real root --version (reads plugin.json via doctor._version only when asked), version as an ALIASES entry to it, and FOLDED's did-you-mean hint for the rest (models -> code models, where -> wiring, scope -> task set ID scope+=a,b, awaiting -> next, affected -> check --affected, approve -> task set ID approved=true). Choice: 3. Why: aliases would be wrong for models (code models list would run a Sampo Code request) and task scope (task set takes scope+=, not --add); FOLDED already prints the hint on the parser's error path; no new verb does new work.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: --version/version print plugin.json's version; each guess names its real verb  <- CURRENT
2. [x] Root --version, version alias, FOLDED hints for the guesses
3. [x] Run test_gate_friction, test_tombstones and the CLI speed/help tests
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_gate_friction.Typos.test_version_prints_the_plugin_version test_gate_friction.Typos.test_guessed_verbs_name_the_real_one_and_run_nothing` → ✗ exit 1 · Ran 2 tests in 370.3s (1 jobs, 16 at a time; slowest: Typos 1s) / FAILED (1 classes: test_gate_friction.Typos) [ran] [tree b66ca9eabd4e] [world 2f1906870a] (2026-11-07T04:40:27Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 14 tests in 20.4s (2 jobs, 16 at a time; slowest: Typos 5s, Flakes 2s) / OK [ran] [tree 23500b4ca1a3] [world 2f1906870a] (2026-11-07T04:41:13Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_tombstones test_help test_cli_speed test_gate_friction` → exit 0 · Ran 33 tests in 105.1s (10 jobs, 16 at a time; slowest: ForkServer 10s, Typos 4s, Flakes 3s) / OK [ran] [tree 23500b4ca1a3] [world 2f1906870a] (2026-11-07T04:42:49Z)
## Log
- 2026-11-07T04:30:02Z created
- 2026-11-07T04:33:55Z set tier=S
- 2026-11-07T04:33:56Z planned: it has criteria and steps
- 2026-11-07T04:34:01Z lane: ~/.claude/foreman.lanes/T-3612 on foreman/T-3612
- 2026-11-07T04:34:05Z focused
- 2026-11-07T04:34:05Z predicted from its closes: 1 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3555 [FEATURE S, active, 2 steps] Cli: unknown verbs 'lane awaiting', 'where', 'task scope' got no suggestion…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- decision 2026-11-04: [costly] [confidence: 85%] Sampo's trained models learn only from outcomes, user-written text and labels, and local-model traces graded by tests, ne…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
