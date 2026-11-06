---
id: T-3318
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T04:24:13Z
updated: 2026-11-06T04:24:13Z
steer_method_rate: 0.218
---
# **Meaning of "X of X":** When the user says "kalevala of kalevala" (or any "X of X"),…
## Raw request
> also when I said kalevala of kalevala, I mean where it is another layer on top of kalevala, like the genesis of genesis, and each depth is one of that on one of that, etc. but we will want this to be fast, efficient, and still insane, because otherwise it will take forever, and cost a shit ton of money
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Meaning of "X of X":** When the user says "kalevala of kalevala" (or any "X of X"), they mean recursive layering. Each depth applies Kalevala to the output of the previous depth, like "the genesis of genesis". Depth 1 is Kalevala, depth 2 is Kalevala applied to depth 1, depth 3 is Kalevala applie…
- **Generalize the pattern:** Treat this as a general recursion rule for any named construct in the project, not only Kalevala and genesis. If the user writes "X of X" or "X of X of X", build a depth-parameterized composition where level n takes level n-1 as its input.
- **Make depth a first-class parameter:** Implement depth as an explicit, validated input (with a default and a hard maximum) in code, config, CLI or API, and any prompts or templates. Depth 0 or 1 must behave exactly as the non-recursive version does today.
- **Cover every surface:** Update everything the recursion touches: the core implementation, the entry points that call it, config and defaults, tests, docs and examples, and any logging or reporting that shows per-depth results. Do not leave one surface still assuming a single layer.
- **Keep it fast and cheap:** Design for low latency and low spend from the start. Cache and reuse intermediate per-depth results, avoid recomputing identical layers, and use the cheapest model or method that still preserves quality at each depth. Run independent work in parallel, and prune or stop e…
- **Keep quality high ("still insane"):** Efficiency must not flatten the result. Each deeper layer must visibly add something beyond the previous one, not a rephrase. Check this with concrete comparisons across depths, such as differences, novelty or a quality rubric, and do not treat it as met just…
- **Measure cost and time:** Record per-depth wall time, token or API usage and estimated dollar cost. Show the growth curve across depths so runaway scaling is visible. Report real numbers, and state plainly when a measure was not taken.
- **Bound the blow-up:** Cap depth, fan-out and total spend per run. Make the cost-growth shape explicit: if the naive design is exponential in depth, restructure it to be linear or near-linear, or say clearly why that is not possible.
- **Verify before claiming done:** Run tests at depth 1, 2 and a small higher depth. Confirm that layer n really consumes layer n-1, that caching works, and that cost stays within the cap. Report failures with their output instead of glossing over them.
- **Act, don't advise:** Make the change directly. Where a design choice remains, such as the cache key or the pruning criterion, pick one, state it in a line, and proceed.
- **Spending needs the user's grant:** Run only small, cheap checks without asking. Ask before any large or deep run, paid API batch or other costly operation, and state the estimated cost first. An earlier approval does not cover a bigger run later.
- **Confirm before outward or irreversible steps:** Ask before publishing results, calling external services with project content, or deleting or overwriting existing outputs. Look at the target before overwriting.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:24:13Z created
## Follow-ups captured
