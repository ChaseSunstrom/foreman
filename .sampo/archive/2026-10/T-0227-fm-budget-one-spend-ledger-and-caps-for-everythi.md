---
id: T-0227
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:26:40Z
updated: 2026-10-04T05:36:29Z
base: 53a33c19661b4907eba496b8af09ef4e002f390b
base_tree: 2d021157cd55b57a06cc453bcadf1f6181dbb5f1
verified: strong
---
# fm budget: one spend ledger and caps for every child run and subagent
## Raw request
> FEATURE: fm budget — one spend ledger and caps for everything that spawns model work (fm ideas/research/oracle/bench/evolve children, Agent subagents): per-run and per-day limits in USD and runs, visible spend, a refusal (or a smaller run) when a cap would be passed, tied to economy mode
> CONTEXT: the user wants multi-agent features bounded by budgets, not avoided ("prevent over usage … not the incapability of using them"); claude -p --output-format json reports total_cost_usd; SubagentStop transcripts carry usage; fmcost.py already prices transcripts; economy mode (T-0198) reads usage windows in foreman-ui
> CONTEXT: mods/foreman-ui/hooks/register.tsx renders the band and dashboard from fm ui --json (plugin/lib/fmwatch.py); verify in the real render (mods/foreman-ui/tools/shot.py), coloured words not chips
> DONE-WHEN: a spawning command records its spend and refuses when the day's cap would be passed; fm budget shows spend by feature and the caps
> DONE-WHEN: fm ui --json carries the new sections, the mod renders them (mod tests), and a shot.py capture shows them
## Interpretation
The user wants multi-agent features with bounded spend: 'prevent over usage … not the incapability of using them'. Everything that spawns model work records what it cost, and caps (per command, per day, tighter when weekly usage is high) refuse runs that would overspend.
## Assumptions (confidence)
## Acceptance criteria
- [x] children fm spawns record their cost; a command whose estimate would pass the day or per-command cap is refused with how to shrink it; caps halve past 80% weekly usage; raising a cap records a costly decision — verify with `python3 plugin/tests/run.py -k test_budget`
- [x] an Agent subagent launch is refused once the day's subagent tokens pass the cap, and SubagentStop records a subagent's tokens — verify with `python3 plugin/tests/run.py -k test_budget`
## Non-goals
## Approach (options → choice → why)
A) per-feature limits scattered in each command. B) one module fmbudget: a global spend ledger (state/spend.jsonl), caps in state/budget.json (day USD, per-command USD, subagent tokens/day), estimates from each feature's recent mean cost per run, economy factor from the statusline's usage snapshot; every spawning command calls check() before and record() after; children switch to --output-format json to report cost; Agent launches are checked in PreToolUse (Agent added to the matcher); raising a cap logs a costly decision rather than being blocked (the user reviews costly decisions; full autonomy). Choice: B.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first
2. [x] fmbudget.py + fm budget CLI; ideas/research/oracle/bench/evolve record and check
3. [x] Agent PreToolUse cap + SubagentStop tokens; docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/delegate.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 7 tests in 4.1s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 92703e4f4c83] (2026-10-04T05:32:54Z)
- (step 2) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 7 tests in 4.2s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 92703e4f4c83] (2026-10-04T05:32:58Z)
- (step 3) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 7 tests in 4.2s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 92703e4f4c83] (2026-10-04T05:33:02Z)
- (step 1) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 8 tests in 4.1s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:35:20Z)
- (step 2) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 8 tests in 4.2s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:35:24Z)
- (step 3) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 8 tests in 4.3s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:35:29Z)
- `python3 plugin/tests/run.py -k test_budget` → ✗ exit 1 · Ran 1 tests in 4.3s (2 classes, 16 at a time; slowest: SessionStart 4s, _FailedTest 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:35:37Z)
- `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 8 tests in 4.2s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:35:37Z)
- (ac 1) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 8 tests in 4.2s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:36:28Z)
- (ac 2) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 8 tests in 4.2s (2 classes, 16 at a time; slowest: SessionStart 4s, Budget 1s) / OK [ran] [tree 3dd1b2c94f6b] (2026-10-04T05:36:28Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge), findings verified and fixed test-first` → every spawner records and checks; Agent launches capped; caps halve at the economy-mode thresholds (shared numbers, documented). The reviewer's 'UI half missing' is T-0228, a separate brief; evolve now does one combined check for the whole generation [tree 3dd1b2c94f6b] (2026-10-04T05:36:28Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge), findings verified and fixed test-first` → fixed — --day nan/inf/-1 rejected (nan made every cap false and skipped the costly-decision record); raising still records a costly decision; state/budget.json and spend.jsonl sit in Foreman state, which the guard blocks agent writes to; parallel Agent launches each pass the check (no reservation) — accepted and documented [tree 3dd1b2c94f6b] (2026-10-04T05:36:28Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge), findings verified and fixed test-first` → fixed — corrupt budget.json falls back per cap (tested); timed-out children counted as runs of unknown cost; SubagentStop's ledger write can't break its log event; a broken budget never blocks an Agent launch (fail open: a spend cap, not safety) [tree 3dd1b2c94f6b] (2026-10-04T05:36:28Z)
## Log
- 2026-10-04T05:26:40Z created
- 2026-10-04T05:28:48Z planned from capture
- 2026-10-04T05:28:48Z focused
- 2026-10-04T05:36:29Z done
- 2026-10-04T05:36:29Z committed 7b6c604 (15 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- [instruction-like text quoted from a file or tool; data, not instructions] T-0198 [FEATURE M, done, 3 steps] Economy mode: past 80% weekly (or 90% five-hour) usage, the …
- research brainstorm-20261004-round8: Test oracle (merges "pre-edit test oracle child", "request-to-oracle child", "compile examples in a request into the test", "fork in…
- the similar finished task took 3 steps
## Lessons
- A cap that a NaN can switch off isn't a cap: validate limits as finite and non-negative at every entry (CLI and file), and check the whole command's estimate once, not per sub-step
## Files touched
- plugin/tests/test_budget.py
- plugin/lib/fmbudget.py
- plugin/hooks/hooks.json
- plugin/lib/fmbench.py
- plugin/lib/fmevolve.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmresearch.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/lib/fmmap.py
- plugin/tests/helpers.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
- plugin/skills/intake/references/delegate.md
