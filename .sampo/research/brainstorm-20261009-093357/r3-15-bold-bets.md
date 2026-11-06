# Brainstorm — lens: bold bets

- **Prune the idea pile with a 20-questions interview** — FEATURE — value 5 — effort M — risk low — category: ideation
  Why: The pile has hundreds of ideas, and the user said "I like almost all of those", so a score list won't help them choose. Assumption: forced-choice trade-offs reveal more than approval does.
  Done when: `fm ideas interview` asks ≤8 forced-choice questions, each chosen by how many idea clusters its answer splits, then prints a re-ranked shortlist citing the answers that moved each idea. A fixture pile gives the same ranking for the same answers.

- **Plan the shared prefix of rival interpretations** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: The user's drops and steers show misreads, and "ask only when sampled plans disagree" exists. Nothing yet uses the plan steps that all plausible readings share. Assumption: ambiguous requests usually have a common first third.
  Done when: for a request seeded with two interpretations, Foreman runs the common steps first and asks only at the first divergence. The brief records the divergence point and which interpretation the answer picked.

- **Reroute from the acceptance criterion when a step blocks** — FEATURE — value 4 — effort M — risk med — category: execution
  Why: Today 3 failed attempts end in a block with a diagnosis. Instead, work backwards from the criterion (goal regression): list its necessary conditions and look for another way to satisfy them, rather than retrying the step.
  Done when: a seeded task whose planned step is impossible but whose criterion has another route finishes unblocked. The ledger records the abandoned step and the route taken.

- **Extract the shared primitives behind the idea pile** — FEATURE — value 4 — effort M — risk low — category: roadmap
  Why: Many ideas repeat the same machinery: replay, sandbox, judge panel, dependency graph, hash chain. Building each idea separately re-pays for it. Assumption: a clustering pass can name these primitives from the idea text.
  Done when: `fm ideas keystones` lists the top 10 primitives, the ideas each one unlocks and the cost saved. The output is deterministic on a fixture pile.

- **Distil the project's human reviewers into audit lenses** — FEATURE — value 4 — effort M — risk low — category: review
  Why: audit.md has generic lenses (self, intent, adversary, edge, operator, maintainer). The repo's own review comments and reverted commits hold project-specific taste. Assumption: the repo has usable review history.
  Done when: `fm audit --mine` writes ≥3 project lenses, each citing its source comments or commits. One lens flags a seeded violation that the generic lenses miss.

- **Wild: Drill a six-month-later maintainer on each L diff** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: Assumption: a task is only well built if a cold agent can fix a future bug in it. Plant a plausible bug in the new code, give a cold fm-debugger only the symptom, and measure steps and files read.
  Done when: an L close-out includes a maintainability result. A failed drill files a captured doc, test or naming task that names what the cold agent was missing.

- **Wild: Settle design arguments with a throwaway simulator** — FEATURE — value 3 — effort M — risk med — category: decisions
  Why: Pace limits, lane concurrency and merge-train policy are debated in prose. The ledger holds real duration and failure distributions to feed a small discrete-event simulation. Assumption: ledger timings are rich enough to fit.
  Done when: `fm decide --simulate` builds a disposable simulator for two options, runs both on ledger-fitted inputs, and records the numbers in the decision with a revisit trigger. The simulator is deleted afterwards.

- **Show a what-if view when a brief is edited** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: Briefs, assumptions and criteria are edited, and a checked criterion can't be changed (T-0342). The user can't currently see an edit's effect before committing to it.
  Done when: `fm brief whatif T-x <edit>` prints the changed steps, verify commands, tier and estimate, and writes nothing.

- **Salvage a failed lane's hunks for other queued tasks** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: Abandoned or blocked lanes often contain correct partial work that other captured tasks (T-0439..T-0455) could use. This is hindsight relabelling. Assumption: hunk-level criterion matching is reliable enough.
  Done when: a seeded failed lane's passing hunk is offered to a queued task as candidate evidence for one of its criteria. The task's own verify command confirms it before anything is merged.

- **Process-mine the ledger for the workflow Foreman actually follows** — FEATURE — value 3 — effort M — risk low — category: self-knowledge
  Why: The declared lifecycle and the observed one probably differ in loops, skipped steps and rework. Nothing compares them.
  Done when: `fm mine` prints the observed state graph with counts and highlights the costliest loop. A seeded loop is found in a fixture ledger.

- **Sample a claim several times before trusting it** — FEATURE — value 3 — effort M — risk med — category: epistemics
  Why: Plans and done summaries carry factual claims about the repo. Ask a cheap model the same question k times; disagreement is a cheap signal to probe before relying on the claim. Assumption: the extra calls stay inside the usage pace.
  Done when: a seeded unstable claim triggers a probe before it enters a plan. A stable claim triggers none. The cost shows in the ledger.

- **Wild: Map the repo's traps by quizzing cold agents** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: Where fresh agents answer questions about the repo wrongly, the code, names or docs are misleading, and those spots are likely future failures. Assumption: wrong answers cluster on identifiable files.
  Done when: `fm traps` runs a quiz of ≥20 repo-fact questions and ranks files by wrong-answer rate. The top 3 become captured rename or doc tasks.
