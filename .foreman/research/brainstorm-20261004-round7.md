# Brainstorm round 7 (2026-10-04): bold, measurable — grounded

Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; deepen 2), past every earlier ideas.md. 63 new titles.

## Slate
1. Bench rigor: `fm bench run --runs N` (per-case pass fraction, cost/turns mean±sd) and `fm bench gate A B` (candidate not worse beyond noise; cost not up >15%). Merges 6 ideas (variance floor, promotion gate, held-out split, non-regression gate). fmbench.py has no repeats or gate. V5 · M.
2. Replay diagnostics: keep the replay's own Foreman ledger summary (tasks, steps, evidence, gates, guard blocks) per case; `fm bench show LABEL` — "attribute each failure to a pipeline stage". Results hold only pass/cost/turns today. V3 · S.
3. Bench from any repo's history: `fm bench build --commits RANGE --verify CMD` mines commits that touch tests and source (no brief needed), prompt from the commit message — "mine external benchmarks", "auto-grow bench". build needs finished briefs today. V4 · M.
4. Model routing from data: `fm bench models` replays cases per model and recommends the cheapest that passes per tier for `fm run --models`. fm run --models is manual. V4 · M (saves usage).
5. `fm evolve` (L): bench-gated self-improvement loop — a mutation child proposes one revision (or a deletion: ablation) of one Foreman text component from bench failures + friction; the candidate is built in a worktree, benched, gated; winners land on an evolve branch for the user's yes. Merges GEPA-style prompt evolution, rule ablation, "mine bench failures into rule candidates", "prune rules that never earn their tokens". V5 · L.

## Dropped
- Plan critic before execution: L plans already get adversarial self-critique + optional fm-reviewer (planning.md:14, intake SKILL §3).
- fm slice: fm outline + Read offset covers it.
- MCP server / AGENTS.md export / harness-agnostic: low value for this user.
- fm landscape recurring scout: T-0213 just did it; repeat on demand.
- Shadow-user gauntlet, regression court, stranger test: covered by bench + evals at lower cost.
- fm goal plan-DAG: depends_on + queue + fm run --parallel exist.
- Night-shift/idle loops: usage-sensitive user; fm run exists.
