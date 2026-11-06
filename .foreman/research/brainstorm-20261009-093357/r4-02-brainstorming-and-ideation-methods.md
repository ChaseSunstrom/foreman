# Brainstorm — lens: brainstorming and ideation methods

- **Backtest the ideator on the project's own past** — FEATURE — value 5 — effort M — risk low — category: ideation eval
  Why: The pack shows 835+ ideas and several rounds, but nothing measures whether `fm ideas` finds what turns out to matter. The git history and task ledger show what was later built or kept. Assumption: old packs can be rebuilt from a commit plus the ledger up to that point.
  Done when: `fm ideas --backtest <commit>` rebuilds the pack as of that commit, runs one round, and prints what share of tasks the user actually opened in the next 30 days were anticipated, with the missed ones listed.

- **Invent the lenses per project** — FEATURE — value 4 — effort M — risk low — category: lenses
  Why: The lens list is fixed (unspoken needs, delight, and so on), while the pile shows the user's real concerns are specific: guard, pace, taste, cleanup. Assumption: a tool-less child can propose lenses from the pack that the fixed set misses.
  Done when: a round-0 step proposes 3–5 project-specific lenses, each tied to a quoted pack line, and the user can see which new lenses produced ideas that survived dedupe.

- **Flip every assumption in the brief** — FEATURE — value 4 — effort S — risk low — category: reframing
  Why: Intake already records assumptions with confidence, but brainstorming never uses them. Negating each one is a classic way to open new options. Assumption: the brief's assumptions are readable as a list.
  Done when: `fm ideas --flip <task>` emits one candidate approach per listed assumption, each labelled with the assumption it negates, and the approach options for an M/L brief can cite one.

- **Generate "How might we" questions before ideas** — FEATURE — value 4 — effort S — risk low — category: question-storming
  Why: Rounds go straight from pack to ideas, and the user's own words ("genuine intelligence… all of it") are broad. Ranking questions first aims later rounds at the real problem. Assumption: a question round costs less than the idea rounds it improves.
  Done when: a round-0 artifact lists 20+ questions with the top 5 marked, and later lens children are given only those 5 as their focus.

- **Use TRIZ-style contradiction prompts** — FEATURE — value 3 — effort M — risk low — category: ideation method
  Why: The pack shows recurring trade-offs (more safety vs less friction, more rigor vs less surface, speed vs verification). A contradiction pair ("improve X without worsening Y") is a method none of the listed ones covers. Assumption: about 20 inventive principles can be stored as a small data file.
  Done when: for a task with a stated tension, `fm ideas --contradiction "guard strictness vs friction"` returns at least 5 ideas each citing a named principle.

- **Balance each round by horizon and require a stop-doing idea** — FEATURE — value 3 — effort S — risk low — category: portfolio
  Why: The pile is mostly M-effort FEATUREs rated 3–4 and is heavy on additions. The user also steered toward cleanup that "never got done". Assumption: a quota in the child prompt is enough to shift the mix.
  Done when: each round's output contains at least one quick win (S), one big bet (L) and one removal idea, and `fm ideas` reports when a round misses the mix.

- **Borrow from fields that already solved it** — FEATURE — value 3 — effort S — risk low — category: analogy
  Why: Ideas now come from the product space only. An analogy lens (air-traffic control, hospital checklists, kitchen brigades, newsroom desks) maps naturally to lanes, handoffs and escalation. Assumption: children handle named-field prompts well without tools.
  Done when: a lens can be run as `field:<name>` and each idea states the source practice and what it maps to in Foreman.

- **Run a shortlist through fixed thinking hats** — FEATURE — value 3 — effort M — risk low — category: convergence
  Why: Scoring currently collapses to value, effort and risk. A fixed sequence (facts, risks, upside, feelings, creativity) per idea would surface the cost to the user's attention. Assumption: five short child calls per shortlisted idea are affordable.
  Done when: each top-10 idea carries a five-line hat card, and the ranking can be re-sorted by the risks hat.

- **Run the speed round against the slow round** — FEATURE — value 3 — effort S — risk low — category: ideation eval
  Why: The same lens could be run with a hard cap of about 150 output tokens and again at full length. Comparing what the user keeps shows whether depth or first instinct pays. Assumption: kept and dropped history is recorded per idea.
  Done when: `fm ideas --speed` tags ideas by mode, and a later report shows keep rate for speed vs full.

- **Wild: Cross-pollinate with a sibling project's pack** — FEATURE — value 3 — effort M — risk med — category: cross-project
  Why: wild. The user runs several projects (`fm projects`, cross-project sweeps captured). Feeding another project's recent friction as stimulus, with redaction, can give ideas neither pack would produce. Assumption: a per-project redacted summary can be produced locally.
  Done when: `fm ideas --stimulus <project>` adds a redacted summary of that project's top 10 friction items to the pack, and the output says which ideas used it.

- **Wild: Draw three cards: capability × surface × user moment** — FEATURE — value 2 — effort S — risk low — category: provocation
  Why: wild. The pile has a "constraint-inversion deck", but no deck built from Foreman's own axes. A random draw such as "undo × statusline × just after a refusal" forces combinations nobody listed. Assumption: three small lists of 15–20 entries are enough.
  Done when: `fm ideas --draw 5` prints five random triples and gets one idea per triple, and a rerun with the same seed gives the same cards.

- **Wild: Dig up ideas from the graveyard on schedule** — FEATURE — value 3 — effort M — risk low — category: idea lifecycle
  Why: wild. Dropped and deferred items (T-0034, T-0035, T-0214) sit idle. A periodic pass could ask what has changed since each was shelved that makes it cheaper or more valuable now. Assumption: deferral reasons are stored.
  Done when: a weekly pass lists deferred items whose stated blocker no longer holds, with one line on what changed, and at most 3 are offered.

- **Wild: Interview the user with five rapid idea cards** — FEATURE — value 3 — effort M — risk med — category: taste sensing
  Why: wild. The user has kept or skipped most ideas ("I like almost all of those"). One keystroke per card gives finer signals than a bulk "continue". Assumption: a web or terminal card UI is cheap to add.
  Done when: `fm ideas taste` shows 5 cards, records keep/skip/not-now for each, and the next round's ranking visibly reuses the answers.
