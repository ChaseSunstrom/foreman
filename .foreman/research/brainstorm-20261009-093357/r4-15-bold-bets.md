# Brainstorm — lens: bold bets

- **Invalidate plans by belief dependency** — FEATURE — value 5 — effort L — risk med — category: planning
  Why: the pile has assumption registers, stale plans, mid-task steer rebasing and truth-maintenance graphs, but each acts alone and reopens whole plans. Assumption: plan steps can record the beliefs (assumptions, lessons, decisions, probe results) they depend on. When one belief falls, only the dependent steps are invalidated and re-derived.
  Done when: in a fixture plan, failing one assumption's re-check marks exactly its 2 dependent steps stale, leaves the other steps untouched, and `fm task` shows the replan diff.

- **Find spec ambiguity by blind-implementation divergence** — FEATURE — value 4 — effort L — risk med — category: intake
  Why: `fm oracle` finds ambiguities by reading the spec; "ask only when sampled plans disagree" compares plans, not behaviour. Assumption: a cheap model can build 3 criteria-only implementations of a small spec in throwaway worktrees. Generated inputs where their outputs differ become the targeted question for the user.
  Done when: on a seeded ambiguous brief, 3 blind builds diverge on at least one generated input, and intake asks exactly that question with the divergent outputs shown.

- **Judge calls by case law** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: vetoes, decisions, steers, panel rulings and precedent files are all separate ideas in the pile. Merge them into one precedent store. At decision time, retrieve the nearest precedent and require "follows" or "distinguishes because…". An explicit "overrules" event (with the user's words) retires the old ruling.
  Done when: a fixture decision that matches a stored veto cannot be recorded without a follow/distinguish/overrule line, and an overruled precedent no longer shows up in recall.

- **Relabel failed attempts with hindsight** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the pile mines blocked tasks, reverts and abandoned lanes for lessons, but only for the goal they missed. Assumption: a cold agent can ask "what task did this diff actually solve?" Each answer becomes a new bench case (brief plus verify) and, where useful, a contrastive lesson. Every failure then yields a passing eval.
  Done when: running the relabeler on 5 blocked tasks yields at least 3 new bench cases that the original diffs pass and an unrelated diff fails.

- **Think with me: `fm think` partner mode** — FEATURE — value 4 — effort M — risk low — category: brainstorming
  Why: the request names planning, brainstorming and thought process, yet every method is wired to a task. A conversational mode keeps a persistent whiteboard of questions, options, objections and decisions, and can run lenses, second opinions and recon on demand. `fm think --to-brief` turns the board into briefs, and the board survives `/compact`.
  Done when: a session with no task produces a whiteboard file that resumes after a fresh session and converts to a valid brief.

- **Keep investigations as re-runnable notebooks** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: the debugger returns ranked hypotheses with probes, and the pile has hypothesis ledgers and runtime-trace grounding. Assumption: the case file can be an ordered list of probe commands plus their expected readings. `fm task rerun-case` replays them on a new commit and shows which conclusions flipped, so "is the diagnosis still true?" costs one command.
  Done when: after a commit that changes one probe's output, the rerun flags the conclusions that depended on it and leaves the others untouched.

- **Race a lazy baseline against the plan** — FEATURE — value 4 — effort M — risk low — category: approaches
  Why: the pile has "do less", simplifiers and gold-plating tripwires, but all argue in prose. Assumption: for M/L features, a builder lane implements the laziest thing that could satisfy the criteria. If it passes every criterion, either ship it or tighten the criteria, so the race doubles as a test of whether the criteria are sufficient.
  Done when: on a fixture where the lazy baseline passes all criteria, the brief records "criteria insufficient or over-build" and offers the baseline as the option.

- **Score decomposition by what the seams cost** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: the pile cuts lane seams by co-change and sizes steps from history, but doesn't close the loop. Assumption: after merge, measure per-seam rework, conflicts and re-edits, and feed that back so the next decomposition of a similar task avoids seams that hurt.
  Done when: `fm bench` shows a seam-cost table for 10 finished multi-lane tasks, and the planner cites it in one new plan.

- **Wild: Keep the user's nightmare list as a standing exam** — FEATURE — value 3 — effort S — risk low — category: evals
  Why: the failure museum holds Foreman's own failures. Assumption: the user has horror stories from other agents (deleted the wrong dir, "fixed" a test by weakening it, claimed done unrun). Each story becomes a short staged scenario that runs on every instruction change and model upgrade.
  Done when: adding a one-sentence nightmare creates a runnable scenario, and a weakened guard or done-gate turns it red in `fm bench`.

- **Wild: Turn the top brainstorm ideas into watchable spikes** — FEATURE — value 4 — effort L — risk med — category: brainstorming
  Why: the idea pile has hundreds of entries, and the user says they like "almost all of those", which means reading is the bottleneck. After a brainstorm, discard-guaranteed spike lanes build the top 5 as 20-second recorded demos or transcripts, and the user chooses by watching. Spikes are never merged.
  Done when: `fm ideas --spike 3` leaves 3 recordings and an unchanged main branch, and picking one creates a brief that links its recording.

- **Wild: Run a pre-registered prediction duel between lanes** — FEATURE — value 3 — effort M — risk low — category: reasoning
  Why: the pile has many calibration and prediction ideas, but they score one agent at a time. Assumption: before a hard step, two cheap lanes each commit to a prediction of the gate result and the likely failure site, and the result scores both. The better predictor gets the next reasoning-heavy step, and persistent disagreement flags a step to split.
  Done when: for 5 fixture steps, predictions are written before the gate runs, scored after, and the scores are readable in `fm friction`.

- **Wild: Let Foreman explain its plan to a skeptic who may only ask "so what?"** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: plan reviews check correctness, not stakes. Assumption: a no-tools child asks "so what?" up to 3 times of each L plan's rationale. Every answer must reach a user-visible outcome, and a plan that can't is flagged as internal busywork.
  Done when: a seeded plan with a purely internal step is flagged, and a user-facing step passes in 3 or fewer rounds.
