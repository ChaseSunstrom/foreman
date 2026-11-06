# Brainstorm — lens: deepen: planning

- **Unify the plan as one living graph object** — FEATURE — value 5 — effort L — risk med — category: plan-core
  Why: the list has ~55 plan ideas (step graph, pivot table, revision history, staleness, criteria trace, assumption binding) that would each bolt a separate field onto the brief. Assumption: today's brief is flat text plus steps. Make a single typed `plan.json`: nodes (steps) with pre/postconditions, criteria links, assumption bindings, kill-criteria, footprint, and revisions. Every other planning idea becomes a pass over this one structure.
  Done when: `fm plan show T-xxxx --json` returns nodes, edges, criteria links and assumption bindings, and `fm doctor` fails a plan with a step that has no criterion or an orphan criterion.

- **Run a plan compiler with named passes** — FEATURE — value 5 — effort L — risk med — category: plan-core
  Why: the list already has "optimiser passes", "prune steps whose postcondition holds", "hoist prerequisites", "lint granularity", "check order against dependency graph". Treat them as compiler passes (parse brief → graph → lint → reorder → prune → emit) that each emit a diff and a reason. Assumption: passes are deterministic where possible and use a child `claude -p` only where judgment is needed.
  Done when: `fm plan build T-xxxx` prints each pass with its diff, and rerunning on an unchanged brief produces identical output.

- **Score plans against replayed history** — FEATURE — value 5 — effort L — risk low — category: plan-learning
  Why: fm bench already replays finished tasks, and "make plan templates earn their place" and "learn step size per task type" lack a measuring source. Join each finished task's plan (steps, estimate, risks) with its outcome (retries, blocks, steers, real time) to learn which plan shapes succeed. Assumption: finished briefs retain their original plan versions.
  Done when: `fm plan calibrate` prints per-task-type step-count, estimate-error and first-pass-rate tables, and a new plan shows its percentile against them.

- **Hold a plan court with a prosecutor and a defender** — FEATURE — value 4 — effort M — risk low — category: plan-review
  Why: combines reverse brainstorming, loser's best argument, naive table-read, simplifier and pre-mortem into one adversarial run for L plans. Two tool-less children argue, a third judges against the criteria, and the verdict is written into the brief with the objections that survived. Assumption: fm second's debate mode is the base.
  Done when: `fm plan court T-xxxx` writes a verdict file listing upheld and dismissed objections, and an L task can't start execute while an upheld objection lacks a resolution line.

- **Forecast the plan's blast radius from co-change history** — FEATURE — value 4 — effort M — risk low — category: plan-grounding
  Why: "ground every plan against the repo" and "mark plans stale when footprint changes" need a footprint source. Mine git co-change plus fm map test links to predict files a plan will really touch, flag unplanned ones, and warn when two queued plans' footprints overlap.
  Done when: `fm plan footprint T-xxxx` lists predicted files with confidence, and two queued tasks with overlapping footprints get a sequencing warning.

- **Checkpoint a plan with a surprise budget** — FEATURE — value 4 — effort M — risk med — category: replanning
  Why: re-plan at checkpoints and on surprises exist as ideas, but with no trigger rule. Give each plan a surprise budget (unplanned files, steps over estimate, failed probes); crossing it forces a pause that diffs actual vs. plan and opens a revision rather than silently pushing on. Task T-0429-style drive already knows step state.
  Done when: a test task that touches 3 unplanned files triggers a forced revision entry in the plan history before the next step starts.

- **Offer the user a plan counter-proposal at the one risky node** — FEATURE — value 4 — effort S — risk low — category: plan-collab
  Why: the user steers often and drops or corrects work after the fact ("cleanup requests never got done", "re-ask of dropped work"). Instead of showing the whole plan, surface only the single highest-uncertainty or highest-irreversibility node with the recommended choice and one alternative. Assumption: a node's risk score comes from the graph.
  Done when: the intake output for an L task contains exactly one "decision needed" node with a default that proceeds if unanswered.

- **Ensure cleanup is a planned obligation** — FEATURE — value 4 — effort S — risk low — category: plan-obligations
  Why: the user said cleanup requests (repo, docs, briefs, dead code, replaced functionality) never got done. Verb-expansion should add a "replaced thing removed" step whenever a plan says replace, move, or supersede, with a verify that greps for the old symbol.
  Done when: a plan containing "replace X with Y" gets an auto-added step whose verify fails while X is still referenced.

- **Wild: Dream the plan overnight in a sandbox and keep the survivors** — FEATURE — value 4 — effort L — risk med — category: speculative-planning
  Why: wild; builds on fm night and the C022 idle-time ask. For queued L tasks, night spawns a throwaway worktree, executes the first spike steps, and records what actually broke. The morning plan arrives with real findings, not guesses.
  Done when: after `fm night`, a queued L task's brief holds a "rehearsal findings" section naming at least one measured fact, and the worktree is gone.

- **Wild: Cast the plan as a debate between persistent personas with memory** — FEATURE — value 3 — effort M — risk med — category: plan-review
  Why: wild; a skeptic, a minimalist and an operator that carry their own lessons across tasks (they remember which objections turned out right). Their weight grows with hit rate, so the useless voices fade.
  Done when: `fm plan court` shows each persona's historical hit rate and a persona with a hit rate under a set threshold is skipped.

- **Wild: Let the plan be a playable timeline the user can scrub** — FEATURE — value 3 — effort M — risk low — category: desktop-ui
  Why: wild; Foreman Desktop already exists with animation as a priority. Show the plan graph as a timeline with predicted vs. actual progress, drag a step to see what-if consequences on order and risk, then accept the edit back to the brief.
  Done when: the desktop plan view renders the graph, and dragging a step updates the brief's order after a validation pass.

- **Detect when a plan's problem-class is novel and escalate effort** — FEATURE — value 4 — effort M — risk low — category: plan-routing
  Why: "plan by recognition before enumeration" and "route to a named method" both need a novelty signal. Use fm recall similarity to past briefs: a high match reuses that plan, a low match means a novel problem, which triggers spikes, recon and a second opinion rather than a confident-looking plan.
  Done when: intake records a novelty score, and a task with score below the threshold gets a recon step added automatically.

- **Write plans as falsifiable predictions and grade them at finish** — FEATURE — value 5 — effort M — risk low — category: plan-learning
  Why: score-the-risks-against-what-happened and regret scoring only work if the plan says something checkable. Each plan states predictions (files touched, step count, which step will be hardest, which test will fail first); finish grades them and feeds a running calibration score into intake's confidence language.
  Done when: `fm task done` prints a prediction scorecard, and `fm plan calibrate` aggregates the hit rates.
