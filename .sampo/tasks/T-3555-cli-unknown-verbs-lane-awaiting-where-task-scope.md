---
id: T-3555
type: FEATURE
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-07T00:39:14Z
updated: 2026-11-07T00:42:12Z
lane: ~/.claude/foreman.lanes/T-3555
lane_branch: foreman/T-3555
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-07T00:41:09Z
plan0_scope: []
---
# Cli: unknown verbs 'lane awaiting', 'where', 'task scope' got no suggestion…
## Raw request
> cli: unknown verbs 'lane awaiting', 'where', 'task scope' got no suggestion (cli.py:6478-6509 suggests only difflib near-matches or FOLDED): add FOLDED entries (lane awaiting → lane list, where → focus/status, task scope → task set ID scope=)
## Interpretation
sampo lane awaiting, sampo where and sampo task scope fail with no 'did you mean': the unknown-word handler only offers difflib near-matches or FOLDED hints. Give each a FOLDED hint naming the real verb that does the job.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo lane awaiting, sampo where and sampo task scope each exit 2 naming the real verb (did you mean …) — verify with `nice -n 10 python3 plugin/tests/run.py test_gate_friction -k test_guessed_words_name_the_real_verb`
## Non-goals
## Approach (options → choice → why)
1) FOLDED entries (flat word -> hint), 2) ALIASES that run the real verb, 3) a per-parser hint table keyed (verb, word). Choice: 1 — the existing hint path, one line per word; aliases would run a guess silently (task scope has no single meaning to run), and no FOLDED key collides with a real choice. awaiting -> next (it names finished lanes waiting on a merge; lane list does not), where -> status, scope -> task set ID scope+=PATH.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing test: each of the three guesses names its real verb  <- CURRENT
2. [x] Add the three FOLDED entries
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_gate_friction -k test_guessed_words_name_the_real_verb` → ✗ exit 1 · Ran 3 tests in 37.2s (1 jobs, 16 at a time; slowest: Typos 1s) / FAILED (1 classes: test_gate_friction.Typos) [ran] [tree c210467cbdf7] [world 2f1906870a] (2026-11-07T00:41:56Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_gate_friction -k test_guessed_words_name_the_real_verb` → exit 0 · Ran 3 tests in 6.6s (1 jobs, 16 at a time; slowest: Typos 1s) / OK [ran] [tree a59158a5b3d7] [world 2f1906870a] (2026-11-07T00:42:12Z)
## Log
- 2026-11-07T00:39:14Z created
- 2026-11-07T00:40:59Z set tier=S
- 2026-11-07T00:41:00Z planned: it has criteria and steps
- 2026-11-07T00:41:04Z lane: ~/.claude/foreman.lanes/T-3555 on foreman/T-3555
- 2026-11-07T00:41:07Z focused
- 2026-11-07T00:41:09Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2735 [FIX S, done, 2 steps] an unknown action that means 'list' (list, ls) points at the parser's listing action (fm exam list → did you mean runs?), since difflib alo…
- T-2461 [CLEAN L, done, 5 steps] Lean: fold six verbs into the verbs that already hold their job (proof → prove --rollup, triggers → outcomes --triggers, calibration → ou…
- playbook CLI errors and argument shape (fm playbooks show fix/cli-errors)
- decision 2026-11-05: [check: python3 plugin/tests/run.py test_models] A setting the user gives once is checked from every context Sampo runs in (login shell, hook, night…
- similar finished tasks took 2–5 steps
- start here (files T-2735 touched): plugin/tests/test_gate_friction.py, plugin/lib/fmcli.py
