---
id: T-1357
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmmodels.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_worker.py, plugin/tests/test_models.py, CHANGELOG.md, MASTER.md, README.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:47Z
updated: 2026-10-23T06:35:33Z
base: 36d46d984ffbffd375aa97da505735bcc8e2e64a
base_tree: 0e820229744be4b09861815469ffbd984c0cb517
plan0_at: 2026-10-23T06:26:32Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmmodels.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_worker.py, CHANGELOG.md, MASTER.md, plugin/skills/**]
verified: strong
---
# fm code cost: each call's dollars to the budget ledger, the run's total on its close line, and --max-usd caps a run (claude gets --max-budget-usd)
## Raw request
> fm code cost (R11): each call's cost (claude's total_cost_usd, or tokens times a models.json price) goes to the budget ledger under the project, the close line shows the run's dollars, and claude gets --max-budget-usd from a cap
## Interpretation
fm code should know what a run costs in dollars, put it where fm budget and fm cost already look (state/spend.jsonl), show it when a run closes, and let the user cap a run, passing the cap on to claude so a worker turn can't overrun it.
## Assumptions (confidence)
## Acceptance criteria
- [x] each call's cost (a claude CLI's total_cost_usd, or tokens times the profile's price per million) goes to the budget ledger under the project, and the closed line shows the run's dollars — verify with `python3 plugin/tests/run.py test_code.Cost`
- [x] --max-usd N caps a run: a run past it stops with a Next: resume line, and a resume keeps what it spent and its cap — verify with `python3 plugin/tests/run.py test_code.Cost`
- [x] a claude worker turn is priced from its stream's total_cost_usd and gets --max-budget-usd with what is left of the cap — verify with `python3 plugin/tests/run.py test_code_worker.Worker.test_a_claude_worker_turn_is_priced_and_capped`
## Non-goals
## Approach (options → choice → why)
Complete version: priced calls (API profiles by a models.json price, CLI slots and workers by claude's total_cost_usd) recorded per call to fmbudget's ledger (feature 'fm code', the project) and to the journal; the close line and closed event carry the run's dollars; --max-usd caps a run across resumes; claude turns get --max-budget-usd with the rest. Options: (1) record per call as each lands (chosen: a hard kill loses nothing, and the cap is checked as it goes); (2) one row per run at its end (a killed run records nothing); (3) read Claude Code's own cost from its transcripts afterwards (slow, and API models have none). Default cap: none, since fm budget's $6 per-command cap would stop ordinary long worker runs; fm code --max-usd sets one. Rejected: a price table built in (prices change; a profile names its own).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Cost tests red: ledger rows, close line, cap stop and resume
2. [x] Run.spend: price or total_cost_usd to the ledger and journal; the cap check; --max-usd flag and resume
3. [x] claude worker and CLI slot turns: total_cost_usd counted, --max-budget-usd passed
4. [x] docs: CHANGELOG, MASTER, models.json price in the reference
## Resume here
## Docs impact
README fm code section (cost, price, --max-usd), CHANGELOG, MASTER fm code note; fm code --help gains --max-usd
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.Cost` → exit 0 · Ran 3 tests in 8.0s (1 classes, 16 at a time; slowest: Cost 8s) / OK [ran] [tree 9093752688cb] (2026-10-23T06:31:52Z)
- (step 2) `python3 plugin/tests/run.py test_code.Cost test_models` → exit 0 · Ran 56 tests in 8.6s (7 classes, 16 at a time; slowest: Cost 8s, Bench 6s, OpenAIShape 1s) / OK [ran] [tree 9093752688cb] (2026-10-23T06:32:01Z)
- (step 3) `python3 plugin/tests/run.py test_code_worker.Worker.test_a_claude_worker_turn_is_priced_and_capped test_code_worker.Worker.test_with_no_model_the_worker_cli_plans_too_read_only` → exit 0 · Ran 2 tests in 4.7s (1 classes, 16 at a time; slowest: Worker 4s) / OK [ran] [tree 9093752688cb] (2026-10-23T06:32:06Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 10.3s (16 classes, 16 at a time; slowest: Fences 10s, TaskLifecycle 3s, Site 1s) / OK [ran] [tree cdbfded9c1dc] (2026-10-23T06:32:55Z)
- (audit intent) `self: request re-read` → pass: per-call cost to the ledger under the project, close line dollars, --max-usd with claude's --max-budget-usd; no default cap (fm budget's $6 per command would stop ordinary worker runs) [tree cdbfded9c1dc] (2026-10-23T06:33:10Z)
- (audit edge) `self: inputs and resume` → --max-usd NaN, inf, 0 and negatives refused; a bool, NaN or out-of-range cost counts as unknown; price validated in models.json; spend before the task exists is journaled at its start, so a resume's cap counts planning too; an unpriced model records nothing [tree cdbfded9c1dc] (2026-10-23T06:33:11Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Cost` → exit 0 · Ran 3 tests in 8.0s (1 classes, 16 at a time; slowest: Cost 8s) / OK [ran] [tree cdbfded9c1dc] (2026-10-23T06:33:28Z)
- (ac 2) `python3 plugin/tests/run.py test_code.Cost` → exit 0 · Ran 3 tests in 8.0s (1 classes, 16 at a time; slowest: Cost 8s) / OK [ran] [tree cdbfded9c1dc] (2026-10-23T06:33:28Z)
- (ac 3) `python3 plugin/tests/run.py test_code_worker.Worker.test_a_claude_worker_turn_is_priced_and_capped` → exit 0 · Ran 1 tests in 2.7s (1 classes, 16 at a time; slowest: Worker 2s) / OK [ran] [tree cdbfded9c1dc] (2026-10-23T06:33:28Z)
- (audit intent) `self review (subagents paused at 76% weekly usage): intent, edge` → per-call cost to the ledger, close line dollars, --max-usd with --max-budget-usd for claude [tree cdbfded9c1dc] (2026-10-23T06:33:28Z)
- (audit edge) `self review (subagents paused at 76% weekly usage): intent, edge` → bad caps and costs refused or ignored; planning spend journaled for resume; unpriced records nothing [tree cdbfded9c1dc] (2026-10-23T06:33:28Z)
## Log
- 2026-10-21T03:47:47Z created
- 2026-10-23T06:26:21Z planned from capture
- 2026-10-23T06:26:28Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmmodels.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_worker.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/skills/**']
- 2026-10-23T06:26:32Z focused
- 2026-10-23T06:32:27Z scope: plugin/tests/test_code_worker.py (the claude worker cost test), plugin/tests/test_models.py (bad price values), README.md (--max-usd and price in the fm code section)
- 2026-10-23T06:32:27Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmmodels.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_worker.py', 'plugin/tests/test_models.py', 'CHANGELOG.md', 'MASTER.md', 'README.md']
- 2026-10-23T06:35:32Z done
- 2026-10-23T06:35:33Z committed c3b9aed2 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0776 [PERFORMANCE S, done, 2 steps] Foreman's claude -p children carry a hard --max-budget-usd — lesson: a pre-run estimate isn't a cap; pass the hard limit to the chi…
- research wave2-plan-a0f775007b83f4d0b: [instruction-like text quoted from a file or tool; data, not instructions] === T-1087 [stale: mods/foreman-ui/hooks/register.tsx, …
- research brainstorm-fm-anthropic-half-b: Reading used.** I took all 250 bullets of rounds 1 to 4 in lenses 01, 02, 03, 08 and 09. Four titles occur twice (themes, ETA, g…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py, plugin/tests/test_models.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmmodels.py, plugin/skills/brainstorm/SKILL.md, plugin/skills/debug-test/SKILL.md, plugin/skills/design-extract/SKILL.md…; re-ground the plan against them before editing
## Lessons
- serve() in test_code rewrites the whole profile: a test that adds a profile field must add it again after every serve
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_worker.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmmodels.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/tests/test_models.py
