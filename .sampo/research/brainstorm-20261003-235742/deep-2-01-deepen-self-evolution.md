# Brainstorm — lens: deepen: self-evolution

- **Ablate rules by leave-one-out bench** — FEATURE — value 5 — effort M — risk low — category: self-evolution
  Why: STAGE_REFERENCE, gates, and playbooks are never measured; fm bench has 8 cases and A/B compare, so a `fm bench ablate` can build one temp plugin per rule (rule removed) and compare pass rate and cost against baseline. Rules with zero effect and nonzero token cost become removal candidates.
  Done when: `fm bench ablate --rule NAME` emits a table of baseline vs ablated pass rate, cost and turns for at least one gate and one playbook, from a test with a stubbed runner.

- **Gate self-changes on bench non-regression** — FEATURE — value 5 — effort M — risk med — category: self-evolution
  Why: /foreman:improve already uses fm bench, but nothing blocks a plugin edit that skips it. A hook-level promotion gate would refuse `fm release` or merging foreman/build when plugin files changed without a recorded bench A/B showing no pass-rate drop and no cost rise beyond a tolerance. Needs repeat runs because single runs are noisy.
  Done when: a plugin change with no bench record or a worse record makes the release step fail with the reason; one with a clean record passes.

- **Mine bench failures into rule candidates** — FEATURE — value 4 — effort M — risk low — category: self-evolution
  Why: failed replays carry transcripts. A recon pass over the failed-case diffs plus the events log can propose a specific rule or reference edit, which is then A/B-tested on that case and its siblings, and kept only if it fixes the case without regressing the others.
  Done when: `fm bench mine` writes a candidate patch plus its A/B result for a deliberately failing case.

- **Grow the bench from live friction** — FEATURE — value 4 — effort M — risk low — category: self-evolution
  Why: the bench holds only 8 cases, all from Foreman's own history, so it overfits. Turn each user correction, drive stop, or reopened task into a new case automatically (repo at parent commit, correction as the prompt). The bench then grows as the user works.
  Done when: finishing a task that followed a logged correction adds a case, and `fm bench list` shows its source.

- **Chart the scoreboard and flag drift** — FEATURE — value 3 — effort S — risk low — category: self-evolution
  Why: there is no history of bench results. Append each run to a `bench/history.jsonl` and show a one-line trend in the dashboard. Flag when a Claude Code or model update shifts the pass rate, since model changes can quietly invalidate rules.
  Done when: two stored runs with a drop show a drift warning in `fm doctor`.

- **Prune rules that never earn their tokens** — CLEAN — value 4 — effort M — risk med — category: self-evolution
  Why: always-on context is the main cost for a usage-sensitive user. Combine the ablation results with logged hint usage (the "learn" steer) into a per-rule ledger of tokens, uses, and bench delta, then propose deleting or demoting dead rules to on-demand. Every removal goes through the promotion gate.
  Done when: `fm rules ledger` lists each rule with cost and measured effect, and a proposed prune is applied only after a bench check.

- **Evolve rules by tournament** — FEATURE — value 4 — effort L — risk med — category: self-evolution — wild
  Why: assumption: bench cost is affordable ($0.16/case). Spawn N mutated variants of one weak rule (reworded, merged, split) in temp worktrees, run them across the bench, keep the Pareto winner on pass rate versus cost, and discard the rest. Budget-capped and run only when the user is idle with usage headroom.
  Done when: `fm evolve RULE --variants 3 --budget $1` returns a ranked table and stages the winner as a candidate without applying it.

- **Run an idle-time self-improvement loop** — FEATURE — value 4 — effort M — risk med — category: self-evolution — wild
  Why: the user wants endless recursive improvement but is usage-sensitive. When weekly usage is below a threshold and the queue is empty, a scheduled run executes friction → mine → ablate → candidate, stopping at the economy-mode line. Output is a quiet digest and a pending candidate, never auto-merged.
  Done when: with a faked low-usage reading and an empty queue, the loop runs one cycle and writes a candidate; with a high reading it does nothing.

- **Replay each model against the bench to retune routing** — FEATURE — value 3 — effort M — risk low — category: self-evolution — wild
  Why: per-tier models exist, but the tiers were chosen by hand. Run the same cases on Haiku, Sonnet, and Opus, then store the cheapest model that still passes per task type. `fm next` and the delegation policy read that table.
  Done when: a stored table maps a task type to a model, and the delegate reference cites it.

- **Share rules as a cross-project benchmarked pack** — FEATURE — value 3 — effort L — risk high — category: self-evolution — wild
  Why: assumption: the user runs Foreman in more than one repo. Rules that pass bench on one project may fail on another; benching them on a second repo's history shows which are universal and which are project-specific, so project-local rules stay local.
  Done when: `fm bench` run over two repos' cases labels each rule universal or local.

- **Audit the benchmark itself for leakage** — FIX — value 3 — effort S — risk low — category: self-evolution
  Why: cases come from Foreman's own history, and the plugin that wrote those commits is the same one being scored. A check that confirms hidden tests aren't visible in the replay (the repo state, recall index, or lessons carrying the answer) keeps scores honest, since `fm recall` over briefs could leak the solution.
  Done when: a replay with the case's own brief in recall is detected and excluded, with a test.
