---
id: T-2871
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T02:11:35Z
updated: 2026-11-04T02:18:16Z
base: b59945b05f10e8ab13d1b92cd1ec1d93f26695b4
base_tree: 972b1ddda90f15319b56eb7b90b44a2fc8e099fa
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T02:15:23Z
plan0_scope: []
verified: strong
---
# The per-command budget cap is checked per model call, so a command looping over many…
## Raw request
> FIX: the per-command budget cap is checked per model call, so a command looping over many small calls (moons grow, ideas rounds, exam runs) can spend past it; cap each command run's total as moonscale's _ask now does (T-2868)
## Interpretation
Reading 1 (chosen): budget.check compares one call's estimate with the per-command cap, so a command making many small calls (moons grow, ideas rounds, exam runs) can spend many times the cap. Every caller is a one-shot CLI command (auditrun, bench, evolve, ideas, moonscale, long, playbooks, louhi, research; no long-lived server), so one process is one command: record() adds each spend to the process's running total and check() refuses the call that would carry that total past the cap. Reading 2 (ruled out): a run id threaded through every caller; the process already is the run, and threading touches nine modules.
## Assumptions (confidence)
## Acceptance criteria
- [x] check() refuses the call that would carry this command's recorded spend past the per-command cap, each call under it alone — verify with `python3 plugin/tests/run.py test_budget`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then the process total in record and check
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_budget` → ✗ exit 1 · Ran 12 tests in 16.6s (2 classes, 16 at a time; slowest: SessionStart 14s, Budget 3s) / FAILED (1 classes: test_budget.Budget) (start tree + this task's tests) [ran] [tree 538627ce5873] [world 2f1906870a] (2026-11-04T02:16:19Z)
- `python3 plugin/tests/run.py test_budget` → ✗ exit 1 · Ran 12 tests in 14.4s (2 classes, 16 at a time; slowest: SessionStart 14s, Budget 3s) / FAILED (1 classes: test_budget.Budget) [ran] [tree 538627ce5873] [world 2f1906870a] (2026-11-04T02:16:19Z)
- (step 1) `python3 plugin/tests/run.py test_budget` → exit 0 · Ran 12 tests in 13.7s (2 classes, 16 at a time; slowest: SessionStart 13s, Budget 3s) / OK [ran] [tree fe4dcd933de5] [world 2f1906870a] (2026-11-04T02:17:04Z)
- `python3 plugin/tests/run.py test_budget` → ✗ exit 1 · Ran 12 tests in 15.2s (2 classes, 16 at a time; slowest: SessionStart 13s, Budget 3s) / FAILED (1 classes: test_budget.Budget) (start tree + this task's tests) [ran] [tree fe4dcd933de5] [world 2f1906870a] (2026-11-04T02:17:35Z)
- `python3 plugin/tests/run.py test_budget` → exit 0 · Ran 12 tests in 14.6s (2 classes, 16 at a time; slowest: SessionStart 14s, Budget 3s) / OK [ran] [tree fe4dcd933de5] [world 2f1906870a] (2026-11-04T02:17:35Z)
- (ac 1) `python3 plugin/tests/run.py test_budget` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T02:17:35Z [ran] [tree fe4dcd933de5] [world 2f1906870a] (2026-11-04T02:17:36Z)
- (audit edge) `self-review: record() adds each recorded USD to the process total; check() refuses the call that would carry it past the per-command cap; every budget.check caller is a one-shot command (auditrun, bench, evolve, ideas, moonscale, long, playbooks, louhi, research), so the process is the command; tests reset it per test (helpers), since one test process runs many` → a long run (fm long) now has its whole run capped at --run, which is what 'per command' says; a user hitting it raises --run as the message says [tree fe4dcd933de5] (2026-11-04T02:17:36Z)
- (audit adversary) `self-review: record() adds each recorded USD to the process total; check() refuses the call that would carry it past the per-command cap; every budget.check caller is a one-shot command (auditrun, bench, evolve, ideas, moonscale, long, playbooks, louhi, research), so the process is the command; tests reset it per test (helpers), since one test process runs many` → only adds a refusal; nothing new spends [tree fe4dcd933de5] (2026-11-04T02:17:36Z)
- (audit self) `self-review: record() adds each recorded USD to the process total; check() refuses the call that would carry it past the per-command cap; every budget.check caller is a one-shot command (auditrun, bench, evolve, ideas, moonscale, long, playbooks, louhi, research), so the process is the command; tests reset it per test (helpers), since one test process runs many` → no findings [tree fe4dcd933de5] (2026-11-04T02:17:36Z)
## Log
- 2026-11-04T02:11:35Z created
- 2026-11-04T02:15:21Z set tier=S
- 2026-11-04T02:15:22Z planned: it has criteria and steps
- 2026-11-04T02:15:22Z focused
- 2026-11-04T02:15:23Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T02:18:13Z done
- 2026-11-04T02:18:16Z committed 151e9a23 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-0776 [PERFORMANCE S, done, 2 steps] Foreman's claude -p children carry a hard --max-budget-usd — lesson: a pre-run estimate isn't a cap; pass the hard limit to the chi…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
the cap was written for one-call commands; looping commands came later
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_budget.py
- plugin/lib/sampo/budget.py
