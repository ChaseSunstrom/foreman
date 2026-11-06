---
id: T-1824
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:14:33Z
updated: 2026-10-28T09:09:25Z
base: aadb1cb71bf10651f196cad81fe755f4384665d9
base_tree: c8f84b39f0c7e41796a83ec7731a7c77586b9ffb
plan0_at: 2026-10-28T09:01:58Z
plan0_scope: []
verified: strong
---
# FEATURE: fm cost shows the retry tax per task: tokens spent on failed attempts (a step's g
## Raw request
> FEATURE: fm cost shows the retry tax per task: tokens spent on failed attempts (a step's gate failing, then the same step again) beside the task's total (T-1798 usage-efficiency lens)
## Interpretation
Retry tax: tokens a task spent between a step's failing evidence (result ✗) and that step's next passing evidence (✓); fm cost --task ID names it beside spent with its share, and the by-task line adds it for tasks that have one. A step that never passes counts to now (or the task's close).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm cost --task ID shows retry tax = tokens between a step's ✗ evidence and its next ✓, with its share of spent; JSON has retry — verify with `cd plugin/tests && python3 -m unittest -q test_cost`
## Non-goals
## Approach (options → choice → why)
Options: (a) windows from the ledger's evidence events (data.step, result ✗/✓), tokens per window from the same scan task_costs uses; (b) count failed check_run events × the task's mean cost per turn (rough, no time); (c) a new retry event written at evidence time (only future tasks). Choice: (a): exact for every past task, reuses _timelines/scan, no new events.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a task with a ✗ then ✓ on step 1 and turns in and out of the window: retry counts only the window's turns
2. [x] retry_windows + retry tax in task view and by-task line
3. [x] Gates and review
## Resume here
<!-- auto -->
- 2026-10-28T09:05:22Z step 3/3: Gates and review
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcost.py, plugin/tests/test_cost_forecast.py
- touched since last checkpoint: plugin/lib/fmcost.py, plugin/tests/test_cost_forecast.py, CHANGELOG.md, MASTER.md
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_cost_forecast.RetryTax` → ✗ exit 1 · FAILED (errors=2) / T-0001 waits on the user (cost cap hit); skipped [ran] [tree d83f58a0aa9d] (2026-10-28T09:02:10Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_cost_forecast test_cost` → exit 0 · OK / T-0001 waits on the user (cost cap hit); skipped [ran] [tree 678dd3ade38f] (2026-10-28T09:03:16Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_cost_forecast test_cost` → exit 0 · OK / T-0001 waits on the user (cost cap hit); skipped [ran] [tree 59138b7f2329] (2026-10-28T09:04:25Z)
- (audit intent) `self-review` → retry = tokens between a step's ✗ evidence and its next ✓ on the same step, per task, in fm cost --task, the by-task line and JSON; checked on real tasks (T-1821 838k of 1.5M, T-1822 none) [tree f186e3685c41] (2026-10-28T09:05:10Z)
- (audit edge) `self-review` → TDD red run dropped when a later step's evidence lands (tested); still-failing step runs to now (tested); retry ⊂ spent so no divide by zero; auto evidence without result counts as a pass; cache refresh path unchanged [tree f186e3685c41] (2026-10-28T09:05:10Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcost.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.4    42.4     150  [0] / SessionEnd                  35.1    37.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree f186e3685c41] (2026-10-28T09:08:45Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_cost_forecast.TaskCostCap` → exit 0 · OK / T-0001 waits on the user (cost cap hit); skipped [ran] [tree f186e3685c41] (2026-10-28T09:09:06Z)
- (step 3) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 09:08 UTC); cached (fm check --fresh reruns) [ran] [tree f186e3685c41] (2026-10-28T09:09:07Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_cost` → exit 0 · Ran 5 tests in 2.155s / OK [ran] [tree f186e3685c41] (2026-10-28T09:09:13Z)
## Log
- 2026-10-28T08:14:33Z created
- 2026-10-28T08:14:56Z set status=planned
- 2026-10-28T09:01:57Z focused
- 2026-10-28T09:09:23Z done
- 2026-10-28T09:09:25Z committed ffbddc08 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-115157: Request: continue, super improve foreman, with latest claude code: round 1 shipped (cost per correct session on the page, Claude Code v…
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- research T-1798-triage: Source: research/brainstorm-20261028-025248 (4 rounds × 14 lenses, 626 distinct ideas; the simplicity lens failed in round 3).
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Lessons
- A TDD red run is failing evidence too: count retries from a step's failure to its own next pass, and drop an open failure once a later step has evidence, or every red→green task reads as mostly retry
## Plan gaps
- failed first: step 1 Failing test: a task with a ✗ then ✓ on step 1 and turns in and out of the window: retry counts onl…
## Files touched
- plugin/tests/test_cost_forecast.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md
