# Ideas by round (deduplicated titles; details in the lens files; "near T-…" names a finished task that shares most of an idea's words)

## Round 1
- Mine external benchmarks into `fm bench`
- Run a variance-aware promotion gate for self-changes
- Build a reflexive "improve the improver" cycle — near T-0125 (done): Recursive self-improvement loop: fm friction digests Forema…
- Add a skill-as-hypothesis tournament — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv…
- Compile the user's standing preferences into the bench judge
- Add `fm landscape`, a recurring harness-feature scout — near T-0213 (done): Research other great plugins and what people want agent har…
- Wild: Let Foreman ship its own releases through a shadow-user gauntlet
- Wild: Synthesize new tasks from adversarial mutation of finished ones
- Wild: Make Foreman a harness-agnostic MCP skill server — near T-0016 (done): Approved plugin/marketplace installs on demand; conflict-fr…
- Add a "skill diet" ablation via bench
- Bench the rules: ablate each Foreman rule/gate/playbook against fm bench — near T-0047 (done): Smarter fm check — rerun a failing gate once (flaky), label…
- Measure bench noise with repeats and a variance floor — near T-0209 (done): Evals for /foreman:improve: paired, repeated runs with a va…
- Auto-grow bench from every finished task, with a held-out split
- Add a promotion gate: no self-change ships without bench non-regression
- Mine bench failures into targeted rule candidates
- Bench the models and tiers: pick cheapest model per task type from data
- Wild: Run a nightly bench "tournament" of rule-set variants that spends leftover weekly quota
- Wild: Synthesize adversarial bench cases from the user's pushback
- Wild: Race two competing candidate fixes on bench and keep the winner automatically for low-risk categories
- Track the bench scoreboard over time and alarm on drift
- Bench plugin interop: replay cases with each third-party plugin enabled — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Add `fm spec` executable-spec intake with EARS-style requirements — near T-0208 (done): fm ideas marks each new idea with the finished task it most…
- Expose Foreman as an MCP server of read-only state and recall tools — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv…
- Add session-trace distillation into reusable skills (`fm distill`)
- Add a continuous-learning instinct store with confidence decay
- Make long-horizon runs resumable via a plan-DAG with checkpoint commits (`fm goal`)
- Add an LLM-as-judge rubric grader to `fm bench` for non-test tasks
- Wild: Run a competing-harness shootout inside `fm bench`
- Wild: Self-evolving prompts via bench-gated mutation (GEPA-style)
- Add an AST-aware context compressor for reads (`fm outline`/`fm slice`)
- Wild: Add a "shadow reviewer" that critiques every plan with a different model before execution
- Add cross-harness export of briefs and lessons as AGENTS.md
- Turn "user said X" into a bench case at capture — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Gate every self-improvement merge on a bench delta with a variance floor
- Mine what other harnesses ship, as a diffable feature census
- Add a skill-adoption trial: run a foreign skill on 3 bench cases before routing it
- Wild: Build a "regression court" that replays the user's past corrections on every Foreman release
- Wild: Let Foreman fork itself into two candidate strategies for an L task and keep whichever passes verify cheaper
- Add a "what would make this task unnecessary" pre-check using recall plus map
- Compile a per-project "playbook lift" table from bench runs
- Wild: Run a "stranger test": a fresh Claude with only the README tries to use Foreman on a toy repo and logs where it stalls
- Auto-generate a `fm bench` case from every unresolved friction cluster
- Wild: Let a night-shift lane tackle the top research-debt question and leave a cited note by morning

## Deepened: measurement
- Score every bench run with a preference-weighted rubric, not just pass/fail — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Run each bench case N times and report variance and confidence — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Ablate one skill, playbook or hook at a time and report its marginal value
- Log read-playbook and routed-skill usage per task and join it to bench outcomes
- Gate self-improvements on a held-out bench split
- Mine external repos' fixed issues into bench cases — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Wild: Mutate finished tasks adversarially to grow the bench
- Wild: Replay real past sessions as counterfactuals against a candidate guard and drive loop
- Wild: Run a continuous self-bench that grades Foreman nightly and plots the trend
- Wild: Make a "best-of-bench" leaderboard comparing Foreman against bare Claude Code and other harness plugins
- Attribute each bench failure to a pipeline stage

## Deepened: self-evolution
- Ablate rules by leave-one-out bench
- Grow the bench from live friction — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Chart the scoreboard and flag drift
- Prune rules that never earn their tokens — near T-0153 (done): Guard: an fm command's own arguments are data, not interpre…
- Evolve rules by tournament
- Run an idle-time self-improvement loop — near T-0212 (done): Fm bench — Foreman's own SWE-bench: every finished task wit…
- Replay each model against the bench to retune routing
- Share rules as a cross-project benchmarked pack
- Audit the benchmark itself for leakage — near T-0009 (done): Autonomy: plain-chat approvals, Claude runs everything, mul…

## New ideas per lens
- bold bets: 10
- measured self-evolution with fm bench: 11
- state-of-the-art agent harness gaps: 11
- unspoken needs: 11
