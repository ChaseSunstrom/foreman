---
id: T-2983
type: RESEARCH
tier: L
status: blocked
priority: normal
scope: []
depends_on: [T-2878, T-3093]
source: followup
created: 2026-11-04T14:20:37Z
updated: 2026-11-05T02:04:33Z
base_note: Calibration: this plan states Choice 75% where all closes (only 6 RESEARCH L) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
---
# Model brainstorm cluster M (wild research): a learned world model of tool results to…
## Raw request
> Model brainstorm cluster M (wild research): a learned world model of tool results to rehearse plans before acting, a ledger language model that flags surprising events, a readable rulebook distilled from a model, an Elo ladder of models and scenarios, a time-travel backtest of the decider on past generations (research brainstorm-20261104-model)
## Interpretation
Reading 1 (taken): five wild research ideas from the model brainstorm, each tested by the cheapest experiment that could kill it before anything is built: (a) a learned world model of tool results that rehearses a plan before acting, (b) a language model over the ledger that flags surprising events, (c) a readable rulebook distilled from a model, (d) an Elo ladder of models against scenarios, (e) a time-travel backtest of the decider on past generations; each kept only if its kill test passes, else filed as not-yet with the numbers. Reading 2 (ruled out): build all five: the user's rule is that models advise and proof decides, so each must earn its place first.
## Assumptions (confidence)
## Acceptance criteria
- [ ] World model: trained on Louhi journals' (state, tool call) → result, it predicts a held-out tool result's pass or fail at least 15 points better than the majority class; else not-yet — verify with `sampo research show T-2983-world-model`
- [ ] Ledger surprise: a small model over the ledger flags held-out events that a person later reverted or re-fixed at a precision of at least 0.5 at 10% recall; else not-yet — verify with `sampo research show T-2983-ledger-surprise`
- [ ] Rulebook: rules distilled from the best decider reproduce its held-out decisions within 5 points of its accuracy in under 40 readable rules; else not-yet — verify with `sampo research show T-2983-rulebook`
- [ ] Elo ladder: models and scenarios rated from the bench and exam rows; the ladder's top model wins its held-out matchups at least 60% of the time — verify with `sampo research show T-2983-elo`
- [ ] Time-travel backtest: the decider replayed on each past generation's held-out rows shows whether it improved; the curve filed, with any generation where it got worse named — verify with `sampo research show T-2983-backtest`
## Non-goals
## Approach (options → choice → why)
1) use what exists: Louhi's exam runs and their journals (tool results to predict), the ledger (events to score), research/models/bench.jsonl (rows for a ladder and a backtest), jeff-train for small fits; one kill test per idea, run on local models at no cost: likely outcome: one or two survive with numbers, the rest filed honestly. 2) build the most exciting one fully: fails if: it doesn't survive its kill test. 3) a literature survey only: fails if: nothing measured on Sampo's own data. 4) do less: the two cheapest ((d) and (e) on existing rows): fails if: the wilder three never get their first experiment. Choice 1 (75%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Elo ladder and the time-travel backtest on existing rows  <- CURRENT
2. [ ] ledger surprise kill test
3. [ ] world model kill test on Louhi journals
4. [ ] rulebook distillation kill test
5. [ ] file each result; survivors become briefs
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T14:20:37Z created
- 2026-11-05T02:04:29Z set depends_on=['T-2878', 'T-3093']
- 2026-11-05T02:04:31Z planned: it has criteria and steps
- 2026-11-05T02:04:33Z set approved=True
- 2026-11-05T02:04:33Z blocked: waits on T-2878's measurement (journals and rows for the world model and ladder) and T-3093's frozen held-out set for the backtest
## Follow-ups captured
