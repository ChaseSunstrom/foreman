---
id: T-0228
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:26:40Z
updated: 2026-10-04T05:50:40Z
base: f46aa688d8765e866a02b4494008eed6e18a5bb0
base_tree: 934fe121192e9463b9bcc5ae8d3206ecfc16540b
verified: strong
---
# foreman-ui catch-up: budget, bench and evolve, research asks, and the task's hypotheses, oracle and batch in the pane
## Raw request
> FEATURE: foreman-ui catch-up — the dashboard shows what the last session added: bench results and gate verdicts, evolve branches, research notes with ✓/✗/? claim counts, the active task's hypotheses ledger and oracle, the skill hints fm next names, and budget spend
> CONTEXT: the user wants multi-agent features bounded by budgets, not avoided ("prevent over usage … not the incapability of using them"); claude -p --output-format json reports total_cost_usd; SubagentStop transcripts carry usage; fmcost.py already prices transcripts; economy mode (T-0198) reads usage windows in foreman-ui
> CONTEXT: mods/foreman-ui/hooks/register.tsx renders the band and dashboard from fm ui --json (plugin/lib/fmwatch.py); verify in the real render (mods/foreman-ui/tools/shot.py), coloured words not chips
> DONE-WHEN: a spawning command records its spend and refuses when the day's cap would be passed; fm budget shows spend by feature and the caps
> DONE-WHEN: fm ui --json carries the new sections, the mod renders them (mod tests), and a shot.py capture shows them
## Interpretation
The user wants foreman-ui to match what Foreman can do. The last session added budgets, bench/evolve, research asks, a hypotheses ledger, the oracle and batches, none of which the pane shows. Surface each where the person looks, in the existing card style (coloured words, no chips).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ui --json carries budget, bench (with evolve generations), research asks and the active task's hypotheses, oracle and batch — verify with `python3 plugin/tests/run.py -k test_ui`
- [x] the pane renders those cards and lines (mod tests) — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
A) a new pane tab: more navigation, against the 'cards in one pane' design. B) extend the view model (fmwatch.view) and add three small cards (Budget, Bench, Research) that only appear when there is something to show, plus lines in the task card for its hypotheses, oracle questions and batch members. Choice: B.
## Risks and rollback
## Execution prompt
## Steps
1. [x] View model + its tests
2. [x] Mod: types, cards and task-card lines + mod tests
3. [x] Sync the dev copy and check a real snapshot
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_ui` → exit 0 · Ran 12 tests in 4.9s (2 classes, 16 at a time; slowest: UiView 5s, SkillRoute 0s) / OK [ran] [tree 9be89774f598] (2026-10-04T05:47:01Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.66s] [ran] [tree e9d3653424f7] (2026-10-04T05:49:17Z)
- (step 3) `grep -c 'Spend today\|Bench\|Research' /tmp/claude-1000/-home-<user>--claude-foreman/2bb9323b-b323-4901-bb61-924ab8371253/scratchpad/pane3.txt` → exit 0 · 3 [ran] [tree 66852f6e74f9] (2026-10-04T05:50:27Z)
- (ac 1) `python3 plugin/tests/run.py -k test_ui` → exit 0 · Ran 12 tests in 8.0s (2 classes, 16 at a time; slowest: UiView 8s, SkillRoute 1s) / OK [ran] [tree 28edbc2d4c32] (2026-10-04T05:50:40Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 62 tests across 1 file. [4.84s] [ran] [tree 28edbc2d4c32] (2026-10-04T05:50:40Z)
- (audit intent) `self review against the live render (shot.py: all three cards and the age fix seen in a 70-column pane)` → everything added since the last UI work is visible where the person looks — spend, bench/evolve, research, hypotheses, oracle questions, batches; quiet days show no extra cards (tested) [tree 28edbc2d4c32] (2026-10-04T05:50:40Z)
- (audit edge) `self review against the live render (shot.py: all three cards and the age fix seen in a 70-column pane)` → each new view section is built through _guarded, so a broken budget file or results dir drops that card, never the view; long names truncate; keys on Text aren't findable so texts are asserted instead [tree 28edbc2d4c32] (2026-10-04T05:50:40Z)
## Log
- 2026-10-04T05:26:40Z created
- 2026-10-04T05:46:08Z planned from capture
- 2026-10-04T05:46:08Z focused
- 2026-10-04T05:48:30Z hypothesis: one find() in the new test misses because a Text whose children are split JSX expressions (interpolated parts) doesn't match the regex as one string; probe: report which pattern is missing
- 2026-10-04T05:48:44Z ruled out: every text matched; only find({key}) misses keys on Text elements (keys are found on Box). Key checks for the two Text lines dropped; their texts are asserted
- 2026-10-04T05:50:40Z done
- 2026-10-04T05:50:40Z committed 96a4f50 (7 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0227 [FEATURE M, done, 3 steps] fm budget: one spend ledger and caps for every child run and subagent — lesson: A cap that a NaN can switch off isn't a cap: validate l…
- research T-0227-review: HIGH, missing: the UI half of the request is not built. [stale: plugin/lib/fmbudget.py, plugin/tests/helpers.py, plugin/tests/test_budget.py chan…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- the similar finished task took 3 steps
## Lessons
- Look at the real render even for additive cards: the snapshot showed an old wrap bug ('to/da/y') no unit test could see, and a mod's JSX factory named h makes any loop variable h a crash
## Files touched
- plugin/tests/test_ui.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
