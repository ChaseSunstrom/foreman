# Brainstorm — lens: user value

- **Show a "what you get" preview before the tower runs** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the user steers hard on "genuinely smarter, not hardcoded" and writes standing rules; a run that spends a week before they see its direction is the main value risk. Earlier ideas cover a gen-0 draft for a yes, but not a *concrete outcome preview*: the 5 to 10 scenarios that will close, in plain words, with cost range and the surfaces touched.
  Done when: `fm genesis plan` prints, with no model spend beyond gen-0, a list of target scenarios, an estimated cost range and the files/surfaces at stake, and a run refuses to start without that plan being recorded.

- **Open every Genesis run with a "what you asked for last time" replay** — FEATURE — value 5 — effort M — risk low — category: memory
  Why: the "asked" list shows the user mostly makes surface-lag asks (favicon, stale fm code section, site motion, docs). Assumption: a self-written gen-0 should pre-load the user's recurring asks as MUSTs, so the first generation covers them unasked.
  Done when: on a fixture project with 10 recorded asks, the self-written gen-0 lists the three recurring classes and a held-out scenario for each.

- **Turn each Genesis generation into a one-line changelog the user can read** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: the user asked for "an in-depth look at everything from each generation", but a person returning after a day needs the 30-second form first: "closed 4 of 9, lost 1, cost $X, next: Y".
  Done when: `fm genesis status` prints a ≤5-line summary per generation, with the closed/open counts matching exam.jsonl.

- **Rank the not-yet ledger by what the user would feel** — FEATURE — value 4 — effort S — risk low — category: prioritisation
  Why: the open work holds about 30 deferred "Later from T-…" items, so the ledger will grow the same way. Retrying all of them each generation burns cost on things nobody feels.
  Done when: each ledger entry carries a user-impact score derived from asks/usage, and the retry order follows it; a test shows a high-impact entry retried before a low one.

- **Let the user veto a scenario in one word** — FEATURE — value 4 — effort S — risk low — category: control
  Why: the drops list shows the user rejects findings with reasons ("already fixed", "by design"). Genesis should learn those as exemptions instead of re-raising them.
  Done when: `fm genesis drop S-12 "by design"` removes the scenario from the grid, records the reason, and a later generation does not recreate it.

- **Write a "done enough" definition per project and stop there** — FEATURE — value 5 — effort M — risk med — category: stopping
  Why: a self-directing harness with no finish line feels like a cost, not a gain. Assumption: users value "Genesis said this is finished, here is why" more than endless generations.
  Done when: when the grid has no empty cells and the not-yet ledger has only blocked items, Genesis halts with a stated completion reason.

- **Route blocked items to the user as one batched ask** — FEATURE — value 4 — effort S — risk low — category: unblocking
  Why: several open tasks are blocked on the user's own system (libappindicator, a live codex/gemini check). Genesis can only unblock what it can say plainly.
  Done when: all blockers in the ledger needing the human appear in one list with the exact command or action each needs.

- **Show before/after on the user's own surfaces** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the user's asks are visual (logo, site, motion). A scenario closed should come with a screenshot or diff of the site/README it changed, not just a score.
  Done when: each closed UI scenario links an automatically captured before/after image on the tower page.

- **Wild: Genesis writes the user a weekly "state of my project" letter** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The tower already has the data (closed gaps, costs, drops); a short plain letter makes the system feel like a collaborator.
  Done when: `fm genesis letter` outputs under 200 words citing real generation figures.

- **Wild: A "regret" button that rewinds and teaches** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: wild. When the user reverts something Genesis shipped, that is the strongest signal of a wrong judgement; it should become a held-out scenario and a lens change automatically.
  Done when: reverting a Genesis commit creates a scenario that the next generation must pass.

- **Wild: Genesis argues the opposite case to the user before a big rewrite** — FEATURE — value 3 — effort M — risk low — category: judgement
  Why: wild. Before spending more than a set budget on one rewrite, a tool-less child writes "why not do this", surfaced in two lines with the cost saved if the user agrees.
  Done when: rewrites above the cost threshold show a counter-case line in the plan, and tests verify it appears.

- **Wild: Compare your project to its best-in-class peers in one table** — FEATURE — value 4 — effort L — risk med — category: orientation
  Why: wild. The user wants "complete and best-in-class"; a plain table of the project against three named peers, per capability, shows where "great" is still missing.
  Done when: the spec page has a peer table with every row labelled sourced or assumed.

Next question: What does the user do in the first minute after Genesis finishes a generation, and does anything in the tower tell them what to do next without reading files?
Next question: Which of the user's past reversions or rewrites of agent work would have been caught by an exam scenario, and what does that say about what the exam is missing?
