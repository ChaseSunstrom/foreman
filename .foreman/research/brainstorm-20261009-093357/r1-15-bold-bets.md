# Brainstorm — lens: bold bets

- **Plan the investigation by value of information** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: intake lists "assumptions with confidence", but nothing ranks which unknowns are worth resolving before planning. fm-recon and fm-scout exist and are dispatched ad hoc. Assumption: most rework comes from unresolved unknowns that were cheap to check.
  Done when: for an M/L task the brief contains an unknowns table (cost to resolve, cost if wrong). Scouts are dispatched cheapest-first for the high-ranked rows, and `fm task show` lists each unknown as resolved or accepted.

- **Debug by posterior and discriminating probe** — FEATURE — value 5 — effort M — risk low — category: debugging
  Why: fm-debugger returns ranked hypotheses and `fm task hypo` exists, but ranking is static. Nothing stops a hypothesis being accepted without a probe that separates it from its rivals (premature closure).
  Done when: `fm task hypo` stores a score per hypothesis. Each probe records which hypotheses it rules in or out and the next probe is the one splitting the top two. A FIX cannot close with a cause that no probe discriminated.

- **Give every approach kill-criteria** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: "3 failed attempts → block" is a late, crude trigger. Plans carry 3+ options but no statement of what evidence would prove the chosen approach wrong. Assumption: drift usually shows early in diff shape or a first gate result.
  Done when: each chosen approach has 1–3 machine-checkable tripwires (for example "touches files outside X", "needs a new dependency"). Firing one forces a logged replan event that names the tripwire and the new approach.

- **Select a named problem-solving heuristic when stuck** — FEATURE — value 4 — effort M — risk low — category: reasoning
  Why: debugging.md and planning.md are fixed procedures. When they stall, a retry is the only move (the diverse-retries idea covers variety, not method). Assumption: a small repertoire (bisect, work backwards, solve a simpler analogue, find the invariant, change representation, minimal repro) beats rerolling.
  Done when: a stalled step makes `fm task` pick a heuristic by problem signature, and the ledger records heuristic and outcome. `fm bench` can report win rate per heuristic.

- **Spend deliberation by decision regret** — FEATURE — value 4 — effort L — risk med — category: meta-reasoning
  Why: second opinions, debates and tournaments are available but triggered manually or by tier. Assumption: reversibility × blast radius × uncertainty predicts where deliberation pays, and past rework shows the regret.
  Done when: each plan decision gets a deliberation level (none, second opinion, debate) from a scored rule. Replay over finished tasks shows the rule would have escalated most decisions that were later reworked.

- **Let the user challenge one node of the plan** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the user's steers are corrections like "build it in Tauri", which currently cost a whole replan. Plans are flat step lists with no dependency on claims. Assumption: the user usually disputes one premise.
  Done when: steps declare which brief claims they rest on. `fm task dispute <claim>` marks only dependent steps stale and replans just those, leaving the rest intact.

- **Stop research when novelty saturates** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: recon, `fm ideas` rounds and audits have no principled stopping rule. Rounds repeat until the user stops them (835 ideas, many near-duplicates). Assumption: novelty per round is measurable by similarity to prior findings.
  Done when: each recon, ideas or audit run reports its novelty rate per round and halts when it drops below a threshold, saying why.

- **Run a reframing pass before approaches** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: approaches are listed from the request as stated. Reframing the problem (eliminate it, generalise it, specialise it, invert it, move it to another layer) comes before approaches. Assumption: it catches XY-style misreads cheaply.
  Done when: M/L briefs contain at least 3 reframings, each with a one-line verdict. A rejected reframing records the reason, and `fm recall` finds it later.

- **Quiz Foreman on each subsystem and keep a scored model card** — FEATURE — value 4 — effort L — risk med — category: comprehension — wild
  Why: builders edit unfamiliar modules from reading alone. Assumption: predict-then-run exams ("what will this test print after this edit?") show which areas Foreman misunderstands before it touches them.
  Done when: `fm model <area>` writes a card with an accuracy score from at least 5 scratch-run predictions. Editing an area below the threshold triggers a recon step first.

- **Brainstorm under oblique constraints** — FEATURE — value 3 — effort S — risk low — category: brainstorming — wild
  Why: `fm ideas` varies lenses but not constraints, so ideas cluster. Assumption: forced constraints ("under 30 lines", "no new files", "reversible in one command", "must delete something") surface unconsidered approaches.
  Done when: `fm ideas --constraints` draws N constraints and each idea is tagged with the one that produced it. At least one generated option per run differs structurally from the unconstrained set.

- **Race a hunch lane against systematic debugging** — FEATURE — value 3 — effort M — risk low — category: debugging — wild
  Why: a cheap guess at the cause often wins and costs almost nothing. Systematic investigation currently starts from scratch each time. Assumption: tracking hit rate shows when hunches deserve trust.
  Done when: a FIX spawns a time-boxed fm-scout hunch lane alongside the debugger. Its verdict and later correctness are recorded, and `fm friction` shows the hit rate per task type.

- **Model-check L designs before coding** — FEATURE — value 4 — effort L — risk med — category: design
  Why: the drive has model-check ideas, but L plans reach code with only prose invariants. Assumption: a tiny executable state-machine model finds design flaws that tests find too late.
  Done when: an L plan can attach a Python model with invariants, and `fm task prove` runs it. The model is later reused as a test oracle for the implementation.

- **Distil insights as reframings, not facts** — FEATURE — value 3 — effort M — risk low — category: learning — wild
  Why: lessons record what was true of the code, not what change of viewpoint cracked the problem. Assumption: the "aha" (for example "treat it as a race, not a logic bug") transfers across projects where facts do not.
  Done when: finishing a task after 2+ failed attempts writes an insight (old framing, new framing, trigger cues). `fm recall` surfaces it at plan time for a task matching the cues.
