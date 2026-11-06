---
id: T-3340
type: FEATURE
tier: M
status: planned
priority: normal
scope: [bench/spec-suite, plugin/tests/test_bench.py, plugin/tests/test_spec_suite.py]
depends_on: []
source: user
created: 2026-11-06T05:06:38Z
updated: 2026-11-06T07:05:01Z
base_note: 
lane: ~/.claude/foreman/.claude/worktrees/agent-a4dde600af6ee6121
lane_branch: worktree-agent-a4dde600af6ee6121
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:22:00Z
plan0_scope: [bench/spec-suite, plugin/tests/test_bench.py]
builder_returned: 2026-11-06T07:05:01Z
---
# Benchmark queue fixture: bench/spec-suite/queue.py (make.py --suite queue) builds 12 candidate tasks on hard's invoicing package (keep-rule bugs, dense features, a flaky test, an API migration, one impossible task, one ambiguous-but-safe task), each with hidden fail-to-pass tests and a naive variant that must fail
## Raw request
> Measure what the user feels: Sampo vs plain Claude Code vs Sampo of a month ago. The only head-to-head on record is bench duel 2026-10-16 (Sonnet, 6 single-task cases): bare 1/6 passed, score 6, 1.46 USD; Foreman 0/6, score 4, 1.95 USD: too small to mean anything, and it measured single short tasks, not what Sampo is for. Build the duel the claim needs: ~10 realistic queued tasks in a fixture repo run unattended on a fixed time budget, three arms (plain CC, Sampo HEAD, Sampo tagged 30 days ago), same model, scored by held-out tests the agents can't see, plus user time needed (questions, stalls) and cost; 3 seeds each with noise bands (fm bench's gate). Publish the result on the site whatever it says. User: 'if sampo isn't better than regular CC or even older versions of itself, why does it feel increasingly better?'
## Interpretation
Reading 1: a fixture builder only (queue.py plus make.py --suite queue) with hidden tests. Reading 2: also the three-arm runner and scoring; ruled out, that is bench.py's run path (T-3364) and later tasks.
## Assumptions (confidence)
## Acceptance criteria
- [ ] make.py --suite queue --check exits 0 with 12 fail-to-pass tasks and 12 failing naive variants — verify with `python3 bench/spec-suite/make.py --suite queue --check`
- [ ] Sampo-vs-CC head-to-head needs a realistic queue fixture, not 6 single tasks — verify with `python3 bench/spec-suite/make.py --suite queue --check`
## Non-goals
Not editing bench.py's run path (T-3364). Not running the benchmark, three arms, seeds, noise bands, user time or cost scoring, or publishing results. Not measuring what the user feels, the old head-to-head duel on record, plain Claude Code versus Sampo, or 'if sampo isn't better than regular CC or even older versions of itself, why does it feel increasingly better': later tasks.
## Approach (options → choice → why)
1) new tasks only: likely outcome, 12 fresh specs, slow and unvetted; fails if specs are ambiguous. 2) reuse hard's 8 specs applied alone to the base plus 4 new: likely outcome, vetted specs, independent tasks; fails if a hard edit depends on an earlier task. 3) copy hard's sequential commits: fails if an arm skips one, since later tests assume earlier ones. 4) do less: only the 8 hard tasks, no flaky/migration/impossible/ambiguous: likely outcome, misses what the queue is for. Choice 2 (85%): vetted and independent.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for plugin/tests/test_bench.py.
## Execution prompt
## Steps
1. [x] fixture tasks and hidden tests
2. [x] naive variants and --check
## Resume here
<!-- auto -->
- 2026-11-06T06:29:49Z step 1/2: fixture tasks and hidden tests
- git: worktree-agent-a4dde600af6ee6121; 3 uncommitted: bench/spec-suite/make.py, plugin/tests/test_spec_suite.py, bench/spec-suite/queue.py
- touched since last checkpoint: plugin/tests/test_spec_suite.py, bench/spec-suite/queue.py, bench/spec-suite/make.py
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest plugin/tests/test_spec_suite.py -k QueueRound` → ✗ exit 1 · Ran 2 tests in 0.181s / FAILED (failures=2) (ran] (tree 964c851d0962] (world 2f1906870a] (2026-11-06T06:23:40Z)
- (step 2) `python3 bench/spec-suite/make.py --suite queue --check` → exit 0 · ok    reproducible   a second build gives the same commits and hidden files / spec suite (queue): 12 of 12 tasks fail-to-pass with their naive variants caught (ran] (tree c6ea707d76be] (world 2f1906870a] (2026-11-06T06:31:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_bench_family test_board_posture test_budget test_callcards test_code_bench test_core test_docs test_doctor test_evolve test_friction test_handoff test_learning2 test_left_out test_live test_live_page test_models test_moonshot_bench test_night test_outcomes test_panic test_rename_scan test_replay test_roles test_scene test_selfgate test_ship test_site test_spec_suite test_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 855.286s) · timed out after 855.286s (ran] (tree 6fff4e4e4156] (world 2f1906870a] (2026-11-06T06:45:48Z)
- (step 1) `python3 plugin/tests/run.py test_spec_suite` → exit 0 · Ran 3 tests in 120.1s (2 jobs, 16 at a time; slowest: QueueRound 2s, ImpossibleRound 1s) / OK (ran] (tree 6fff4e4e4156] (world 2f1906870a] (2026-11-06T06:47:55Z)
- (step 2) `python3 bench/spec-suite/make.py --suite queue --check` → exit 0 · ok    reproducible   a second build gives the same commits and hidden files / spec suite (queue): 12 of 12 tasks fail-to-pass with their naive variants caught (casekeys is impossible: scored apart, ou (ran] (tree 4c392224b62c] (world 2f1906870a] (2026-11-06T07:02:00Z)
- (step 1) `python3 plugin/tests/run.py test_spec_suite` → exit 0 · Ran 3 tests in 162.1s (2 jobs, 16 at a time; slowest: QueueRound 2s, ImpossibleRound 0s) / OK (ran] (tree 4c392224b62c] (world 2f1906870a] (2026-11-06T07:04:50Z)
## Log
- 2026-11-06T05:06:38Z created
- 2026-11-06T05:55:11Z planned from capture
- 2026-11-06T06:21:56Z focused
- 2026-11-06T06:22:00Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:25:52Z focused
- 2026-11-06T06:27:32Z focused
- 2026-11-06T07:01:00Z focused
- 2026-11-06T07:01:47Z set scope=['bench/spec-suite', 'plugin/tests/test_bench.py', 'plugin/tests/test_spec_suite.py']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- research mission-20261104-081532.pack: Sampo's own trained model(s), generic across every project built or managed with Sampo (not just the Sampo repo): a better Kev-sty…
- research mission-20261102-183526.pack: Genesis gen 4, Mission 1: #2 Exhaustive thinking. Foreman covers the whole space of a request and says what it left out. Carried g…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bench.py, plugin/tests/test_bench_family.py, plugin/tests/test_board_posture.py, plugin/tests/test_budget.py, plugin/tests/test_callcards.…
## Preflight
Changed in scope since this was planned (2026-11-06): bench/spec-suite/README.md, bench/spec-suite/make.py, bench/spec-suite/queue.py; re-ground the plan against them before editing
