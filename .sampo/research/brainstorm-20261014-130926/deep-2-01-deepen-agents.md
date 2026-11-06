# Brainstorm — lens: deepen: agents

- **Build one agent-run ledger that every child writes to** — FEATURE — value 5 — effort M — risk low — category: agents
  Why: the list has trace timelines, spend gating, retuning of maxTurns, salvage and payoff history. All of them need the same per-child record: role, tier, effort, turns used, cap, cost, outcome and cache hit. Round 1 added effort, maxTurns and `--max-budget-usd` with no record of how they performed. Assumption: today these numbers only live in transcripts.
  Done when: after any `fm agents` or lane run, `fm agents ledger` lists each child with role, turns used/cap, USD spent/cap and outcome, and a test confirms a killed child still gets a row.

- **Salvage and resume capped children from their own transcript** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: this merges "salvage children that die on budget or turn limits", "continue a turn-limited agent" and "kill and salvage stalled subagents". Round 1 made caps hard (`--max-budget-usd`, `maxTurns`), so more children will now end at a cap. On a cap hit, Foreman extracts the findings so far, writes them as a partial result, and offers a continuation brief that starts from that partial result with a fresh cap. Assumption: the child's transcript or stream-json output is readable after death.
  Done when: a test child stopped at maxTurns=2 leaves a `partial` result file, and `fm agents resume <id>` starts a child whose brief contains that file.

- **Learn caps from the ledger and propose changes as a diff** — PERFORMANCE — value 4 — effort M — risk low — category: agents
  Why: this combines "retune maxTurns and effort from observed turn use", "child contracts: declare an estimate, enforce twice that" and "gate spend by payoff history". Foreman proposes cap changes and never silently applies them. For each role it reports p90 turns and cost, the cap-hit rate, and the yield, meaning findings that were later accepted. A role with a high cap-hit rate and good yield gets a higher cap. A role with low yield and high spend gets a lower cap or is dropped.
  Done when: `fm agents tune` prints a per-role table and a patch to the agent files, and applying it changes only the cap fields.

- **Generate all agent files and lane briefs from one role table** — CLEAN — value 4 — effort M — risk low — category: agents
  Why: this combines "generate every agent file from one role table" and "collapse the fm-* specialists, let bench decide". The role table holds tools, tier, effort, maxTurns, omitClaudeMd and contract text. Round 1 added effort/maxTurns/omitClaudeMd in several places (agents and `fmlanes.py:163-165`), and that drift is the risk. A bench run compares merged roles with specialists on the eval cases, and the table keeps whichever scores better.
  Done when: `fm doctor` fails if any generated agent file differs from the table, and a bench report compares the merged and specialist variants.

- **Preflight a child's tools, budget and cwd before spawning** — FIX — value 4 — effort S — risk low — category: agents
  Why: this combines "preflight an agent's required tools", the headless-drive incident drill, and the doctor's CC-version checks. Before spawn, check that the required tools exist, that the CC version supports the frontmatter fields used, that the remaining budget covers the cap, and that the child won't drive the queue (the 2026-10-14 incident). Failures are named and cost nothing. Assumption: spawn goes through one function (`fmideas.child_cmd`, `fmresearch._child`).
  Done when: a child whose role needs a missing tool is refused with the tool's name, and no `claude` process starts.

- **Inject the user's vetoes and steers into every brief with a "contradicts" check** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: this combines "put the user's vetoes into every brief" and "flag diffs that undo recent closed work". The user's "dropped" and "steered" entries are real data. Examples are the delta-reads steer and the refused `$_` heredoc relaxation. Each brief gets the relevant vetoes. At review, a checker agent compares the diff with the vetoes and with closed tasks that touched the same files, and flags a revert.
  Done when: a seeded diff that re-adds the dropped delta-read hook is flagged at review, naming the steer it contradicts.

- **Pair a regression hunter with every PERF builder** — FEATURE — value 4 — effort M — risk med — category: agents (wild)
  Why: wild. Round 1 PERF work was judged on measured numbers: bench by CPU time, 1.04M tokens saved, and the Read-hook dropped on measurement. A second agent reads the PERF diff and the bench output and tries to produce a counter-measurement, such as another path that got slower or output that lost a failure line. The PERF task closes only when both agree.
  Done when: a PERF task with a seeded regression on a non-targeted path is blocked at close with the hunter's measurement attached.

- **Fork a hunch lane that races the plan on each FIX** — FEATURE — value 3 — effort L — risk med — category: agents (wild)
  Why: wild. For a FIX, a cheap read-only lane writes a root-cause guess and a failing-test sketch while the planner works. If the guess's test fails on the start tree and the planner's plan matches it, execution starts sooner. If they disagree, that goes in the plan as an open question. The cost cap comes from the ledger, and the lane is dropped when its payoff history is low.
  Done when: a seeded FIX shows both outputs, and the disagreement case appears in the plan.

- **Run a user-voice shadow that reads only the user's words and grades the close** — FEATURE — value 4 — effort M — risk med — category: agents (wild)
  Why: wild. This extends "a hot second opinion that reads only the user's words". At close, a child sees only the request text plus the dropped and steered history, never the plan or the diff summary. It answers "does the receipt say the thing they asked for?". Round 1 recorded real mismatches, such as "said the full suite never failed" and the catch-rate matching bug. Assumption: those are the failure shape the shadow would catch.
  Done when: closing a task whose receipt omits the asked-for outcome produces a shadow flag containing the missing phrase.

- **Run per-role canary evals when Claude Code or a model changes** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: this builds on the doctor's version check and the open T-0035 eval capture. When `fm doctor` sees a new CC version or a new model ID, it re-runs a small frozen set of past child tasks per role, using the ledger cap. It compares turns, cost and findings against the stored baseline. This turns "integrate with new CC features" into measured evidence.
  Done when: changing the recorded CC version in a test makes `fm doctor` schedule the canary, and the report shows a per-role delta.

- **Hand findings between agents as typed records, not prose** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: T-0760's native-review idea says findings come back as prose. A shared record schema (file, line, severity, evidence, confidence) serves audit reviewers, the regression hunter, the shadow and the lane checkers. It also feeds `fm page` and ReportFindings. The schema is shared with T-0034.
  Done when: a reviewer's output validates against the schema, and `fm page` renders it with file:line links.

- **Auto-split roles that repeatedly hit their cap, with a bench gate** — FEATURE — value 3 — effort L — risk high — category: agents (wild)
  Why: wild. This builds on the cap-hit rate in the ledger. When a role keeps hitting its cap on two or more distinct sub-goals, such as a reviewer that reads and then runs tests, Foreman proposes two narrower roles and bench-tests the pair against the original. It keeps the split only when the pair scores better on cost and yield.
  Done when: a synthetic role that always hits its cap yields a proposed split, and the bench report shows the comparison.

- **Hedge slow read-only children with a cheaper second attempt** — PERFORMANCE — value 2 — effort M — risk med — category: agents (wild)
  Why: wild. This comes from the idea list as written. If a read-only child passes its p90 latency from the ledger, a cheaper-tier twin starts. The first valid answer wins and the other is stopped, and the saving or waste is recorded in the ledger. It only runs on roles whose payoff history shows spend is worth it.
  Done when: a test with one stalled child and one fast twin returns the twin's answer, and the ledger records the cancelled child's cost.
