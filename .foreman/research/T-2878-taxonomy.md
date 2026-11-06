# T-2878 failure taxonomy, first cut (2026-11-04)

Source: the 15 Smith exam runs on local or self-hosted models kept in this project's exam answers (s0-001 seeded across 6 languages, s4-018 and s5-019 minted from a real Python project). Small sample; the rates will move.

| Class | Runs | Rate | What it looks like |
|---|---|---|---|
| Out of steps | 6 | 40% | used all 40 turns before the step was done; most were reading and re-running, not editing |
| Plan refused by the plan gate | 3 | 20% | `fm focus` refused the model's plan (a request clause had no criterion) and the run ended instead of repairing it |
| Reasoning ate the budget | 1 | 7% | the 27B with thinking on wrote no text in its token budget |
| Endpoint timeout | 1 | 7% | a local endpoint timed out under host load |
| Answered without a fix | 2 | 13% | docs and untested scenarios, answer only |
| Closed | 2 | 13% | vague-js and vuln-js closed green |

The grader's view on the minted bugs: the 27B fixed 1 of 4 with the failing command named and thinking off (T-3004), 0 of 4 before.

Where the levers point:
- Steps and wasted reads (40%): T-3006's compact state and check-before-edit, and a higher exam step cap.
- Plan refusals (20%): feed the refusal back to the planner for one repair (captured).
- Reasoning budget (7%): thinking off by default, deliberate turns only (T-3006).
