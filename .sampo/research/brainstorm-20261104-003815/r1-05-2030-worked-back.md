# Brainstorm — lens: 2030 worked back

- **Backcast every moon to a dated 2030 sentence** — FEATURE — value 5 — effort M — risk low — category: moons
  Why: assumption: 10,000 candidates need a pull from the future, not just novelty scoring. Each candidate must name the 2030 sentence it makes true ("In 2030 Sampo can…"). The funnel ranks by the gap that sentence leaves versus what the host will natively do by then.
  Done when: `candidates.jsonl` rejects rows without a `2030:` field, and the funnel prints a gap-ranked top 20.

- **Run succession stages for candidates** — FEATURE — value 5 — effort M — risk low — category: funnel
  Why: the brief asks for a cheap-first funnel and local models for bulk. Pioneer stage means a local model drafts a cheap, many-per-cell candidate. Mid-succession means dedupe and survival. Climax means a frontier cold read. A candidate must survive each stage before it can displace the cell's current occupant.
  Done when: every candidate row carries a `stage` and a promotion reason, and a cell shows its pioneer-to-climax history.

- **Find keystone moons by removal** — FEATURE — value 4 — effort M — risk med — category: ecology
  Why: assumption: candidates depend on one another (shared sub-capabilities). Delete each family in a dry run and count how many other candidates' scores or dependencies collapse. High-impact families get the expensive funnel stage.
  Done when: `sampo moons keystone` prints the top 10 families by cascade size, with a replayable removal log.

- **Re-score the grid after each build (niche construction)** — FEATURE — value 5 — effort M — risk med — category: moons
  Why: a landed capability changes which candidates are still novel or newly possible. This also feeds the standing rule that every Seed retries items a new capability may unblock. On landing, re-run the cheap funnel stages over the neighbouring cells.
  Done when: closing a moon's task triggers a re-score. A test shows a candidate's score changed because of it.

- **Gate advancement on quorum, not on one cheerleader** — FEATURE — value 4 — effort S — risk low — category: funnel
  Why: assumption: local models echo each other. A candidate advances only when N proposals from different model families converge on the same capability (an autoinducer count). Same-family agreement counts once.
  Done when: the funnel log records `quorum=k/N, families=[…]`, and a test shows a duplicate-family pair does not clear the threshold.

- **Track a monoculture index for the 10,000** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: bulk local generation tends to collapse onto a few themes (the user already said earlier moons "aren't that moon-y"). Compute a Shannon diversity index per cell and per family. Fail the generation check when a cell is over-dominated.
  Done when: `fm genesis check` reports diversity per cell and fails on a planted monoculture fixture.

- **Cull the candidate store on a schedule (controlled burn)** — CLEAN — value 3 — effort S — risk med — category: funnel
  Why: assumption: an append-only store of 10,000 grows litter. Nightly, archive the bottom decile by survival and wildness to a compressed pack with an undo. The standing rule forbids killing ideas for ambition, so culled rows go to `not-yet.md` with their blocker, not away.
  Done when: a burn moves rows with their reasons recorded, and `undo` restores byte-identical rows.

- **Keep a seed bank with germination cues** — FEATURE — value 4 — effort M — risk low — category: moons
  Why: failed spikes go to `not-yet.md` with a blocker. Add a machine-checkable germination predicate to each, such as "a native `sampo embed` exists" or "the local reranker is installed". Check the predicates every Seed.
  Done when: flipping a fixture predicate makes the next Seed list that row as "germinated".

- **Classify moons as mutualist, commensal or parasite toward the host** — FEATURE — value 4 — effort M — risk low — category: 2030
  Why: the open questions ask who retires a verb when the host catches up. Tag each moon by whether it depends on host features, rides on them, or competes with them. Parasites get a sunset watch.
  Done when: every shipped moon has a symbiosis class, and the check fails on an unclassified one.

- **Wild: Let moons trade parts through a mycorrhizal graph** — FEATURE — value 4 — effort L — risk med — category: ecology
  Why: wild. Candidates that share a missing sub-capability get linked. The funnel can then lend one family's built part to another, so a stalled moon is rescued by a neighbour's landed work.
  Done when: a graph file lists donor-to-receiver edges, and one stalled fixture candidate is unblocked via a donor.

- **Wild: Run a 2030 pre-mortem forest** — FEATURE — value 3 — effort M — risk low — category: moons
  Why: wild. A tool-less child writes the 2030 obituary of the top 20 moons ("died because the host shipped X"). The funnel re-ranks by how many ways each could die.
  Done when: each top-20 row carries an obituary line, and rank order changes against a control run.

- **Wild: Walk the canopy view in the web UI** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: wild. Draw the 10,000 as a forest. Canopy height is wildness, colour is stage, and dead cells are dark. Hovering shows the 2030 sentence and the quorum.
  Done when: the page renders from `candidates.jsonl` with no JS-only content, and an empty cell shows a hatched "unexamined" state.

- **Cap each cell with a carrying capacity** — FEATURE — value 3 — effort S — risk low — category: funnel
  Why: assumption: funnel cost must stay bounded at 10,000. Each grid cell holds at most K live candidates, with logistic admission, so a hot cell can't consume the expensive-stage budget.
  Done when: admission beyond K requires displacing a lower-scored row, and a test shows the budget per cell stays flat as input grows 10x.

Next question: Which moons in the catalogue would still be wild if the host shipped its own planner, verifier and memory by 2028?
Next question: Does the cheap-first funnel measure whether local-model bulk candidates are actually less wild than frontier ones, or does the cost split just assume they are?
