---
id: T-1358
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code_worker.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:48Z
updated: 2026-10-23T07:18:19Z
group: runner checks, routing and config
base: f9d13124966203b2117f76980dd72a19e8a1a56f
base_tree: bcc3eadabd7cc2b3b235812d2e4ff9888aa52489
plan0_at: 2026-10-23T07:11:26Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code_worker.py, README.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code routing by record: fm code runners shows each runner's record per request kind from past runs, and runner = auto picks for the work the cheapest runner that's green on the plan's kind (3 or more runs), saying why
## Raw request
> fm code routing by record (R12, after T-1328): fm code runners shows each runner's record per request kind from its journals, and runner = auto picks the cheapest runner that's green on that kind (3+ runs), saying why
## Interpretation
With several runners installed, fm code should learn from its own past runs which one does each kind of work (FIX, FEATURE, …) well and cheaply, show that record, and when told runner = auto, hand the work to that runner and say why.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code runners lists each runner's record per kind (runs, closed, mean dollars a closed run) from every project's past runs — verify with `python3 plugin/tests/run.py test_code_worker.Routing`
- [x] with runner = auto, once the plan's kind is known the work goes to the cheapest runner with 3 or more runs of that kind and two thirds of them closed, with a note saying why; with none, the planning runner keeps it and the note says so — verify with `python3 plugin/tests/run.py test_code_worker.Routing`
## Non-goals
## Approach (options → choice → why)
Complete version: runner_records() reads every project's code/*.events.jsonl (its first 64 KB for the start's worker and the plan's type, its last 16 KB for how it ended and the closed event's usd) into {runner: {kind: {runs, closed, usd}}}; fm code runners prints and returns it; runner = auto (code.toml or the project's) plans with the runner pick_runner's fallback would use, then route() picks the work runner for the plan's type: 3+ runs, 2/3 closed, lowest mean dollars a closed run (unknown cost sorts last, then the most closed), with a note naming the numbers; with no such runner the planner keeps it. Options: (1) events files, read at head and tail (chosen: they already hold worker, plan, end and usd, and history() reads them the same way); (2) the journals (they hold the same, but spend is spread through them, so each is read whole); (3) a separate records ledger appended at each close (one more file to keep in step, and no history for runs before it). Kind is the plan's type, known after planning, so auto picks only the work runner.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: records from event files, the runners listing, auto picking and keeping
2. [x] fmcode: runner_records, auto in pick_runner and after the plan
3. [x] docs: README, CHANGELOG, MASTER
## Resume here
## Docs impact
README fm code section, CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker.Routing` → exit 0 · Ran 3 tests in 3.3s (1 classes, 16 at a time; slowest: Routing 3s) / OK [ran] [tree e24814565f26] (2026-10-23T07:15:17Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 75 tests in 71.5s (4 classes, 16 at a time; slowest: Worker 71s, Failover 8s, Routing 3s) / OK [ran] [tree e24814565f26] (2026-10-23T07:16:29Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 8.6s (16 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree b17e92a270c4] (2026-10-23T07:16:39Z)
- (audit intent) `self: request re-read` → pass: records per runner and kind in fm code runners; auto picks the cheapest green runner on the plan's kind and says why, or keeps the planner [tree b17e92a270c4] (2026-10-23T07:16:48Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker.Routing` → exit 0 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: Routing 3s) / OK [ran] [tree b17e92a270c4] (2026-10-23T07:16:52Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker.Routing` → exit 0 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: Routing 3s) / OK [ran] [tree b17e92a270c4] (2026-10-23T07:16:52Z)
- (audit intent) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → both criteria met [tree b17e92a270c4] (2026-10-23T07:16:52Z)
- (audit adversary) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → records come only from Foreman's own state files (never a repo); a routed name must be a registry or code.toml runner that is installed, so a planted record can't name a command [tree b17e92a270c4] (2026-10-23T07:16:52Z)
- (audit edge) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → a run with no end yet isn't counted; unpriced closed runs sort after priced ones and never skew the mean (priced counts separately); a resume keeps the routed runner unless --worker is given; no green runner keeps the planner and says so [tree b17e92a270c4] (2026-10-23T07:16:52Z)
## Log
- 2026-10-21T03:47:48Z created
- 2026-10-21T17:28:59Z round 2 (A27) adds: the plan header names which of pick_runner's three rules chose the runner
- 2026-10-23T07:09:53Z planned from capture
- 2026-10-23T07:10:02Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code_worker.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:11:24Z focused
- 2026-10-23T07:18:17Z done
- 2026-10-23T07:18:19Z committed 98f2b194 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1356 [FEATURE M, done, 3 steps] fm code limits and failover: a worker turn's failure is sorted (usage limit with its reset, sign-in, crash, timeout); a limit within th…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- similar finished tasks took 3–6 steps
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcode.py, plugin/tests/test_code_worker.py; re-ground the plan against them before editing
## Lessons
- Attribute a run to the runner that did the work, not the one that started it: a routed note carries the name the records read
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- MASTER.md
- README.md
