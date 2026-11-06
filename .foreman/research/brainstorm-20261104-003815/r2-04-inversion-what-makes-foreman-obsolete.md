# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Probe each moon against the bare model before it enters the funnel** — FEATURE — value 5 — effort M — risk low — category: moons
  Why: assumption: moons are written as "Today you can't / With this, you can", but the "can't" is never tested against the current model. Add an `assumes-absent:` field and run a free-arm probe on it at funnel stage 0, before the embedding dedupe.
  Done when: a seeded moon whose "can't" is false on the bare model is dropped at stage 0, with the probe output logged against its candidate row.

- **Dedupe candidates against the outside world, not only the catalogue** — FEATURE — value 4 — effort M — risk low — category: moons, funnel
  Why: the funnel dedupes against Sampo's own store, but the pack shows tracked external sources (a `rea` source, anthropics' public repos in T-1382). Embed host docs, release notes and rival plugin READMEs, then flag candidates whose nearest neighbour is already shipped elsewhere.
  Done when: a candidate paraphrasing a documented host feature is tagged `exists-upstream` with the neighbour's URL, and the tag appears in the funnel log.

- **Track a pull ratio for everything the tower produces** — FEATURE — value 5 — effort M — risk low — category: demand
  Why: the user's words are "stop asking me for stuff, keep going", "the moons aren't wild", and they drop most auto-filed items as stale. Count, per source (tower, nudges, self-filed items, drafts, moons), how many the user opened, acted on or dropped. A source whose pull ratio stays low is producing work nobody wants.
  Done when: `sampo doctor` prints the pull ratio per source over 30 days, and a source below a set floor is named as "pushing, not pulled".

- **Compile each steer into a bare-model pass/fail pair** — FEATURE — value 4 — effort M — risk med — category: obsolescence
  Why: about 80 steers are enforced by hooks and checks. For each, build two scenarios, one the steer should block and one it should allow, and run them with only the steer text on the bare model. A steer the bare model already honours moves from hook enforcement to a one-line doc.
  Done when: a table lists each steer as `needs-enforcement` or `model-honours`, and at least one steer changes class with its evidence attached.

- **Check Sampo's lessons and steers against the host's own memory files** — CLEAN — value 3 — effort S — risk low — category: overlap
  Why: Claude Code now keeps persistent memory in files with an index, which overlaps Sampo's recall and lessons. List the entries the host's memory could hold equally well, and keep in Sampo only what needs a checker or a hook.
  Done when: a report splits the lesson store into `memory-holdable` and `needs-sampo`, and the first group has a one-command export.

- **Diff the host's command and tool list on each upgrade into a shadow table** — FEATURE — value 4 — effort S — risk low — category: obsolescence
  Why: `/code-review ultra`, native plan mode and background agents already overlap Sampo's audit, plan and lanes verbs. Detect these at run time from the host's own slash-command and tool list, which is more concrete than watching release notes.
  Done when: after a host version bump, `sampo doctor` lists new host commands next to the nearest Sampo verb and marks each `shadowed`, `adjacent` or `unrelated`.

- **Log overturn rates for the two-tier cold read** — FEATURE — value 3 — effort S — risk low — category: gates
  Why: Haiku reads first and Sonnet decides on any non-pass. If Sonnet never overturns Haiku, or always overturns it, one tier is dead weight. This is an obsolescence test applied to Sampo's own gates.
  Done when: the ledger records Haiku's and Sonnet's verdicts per read, and `sampo doctor` prints the overturn rate with a recommendation once there are 30 reads.

- **Mark the moments you missed a capability during a blind mute week** — FEATURE — value 4 — effort M — risk med — category: felt value
  Why: answers the open question about which capability the user would notice first. Mute one capability per week without telling the model, and give the user a one-key "I missed that" marker. Outcomes can hold steady while the user still feels the loss, so record both.
  Done when: a week-long mute produces a ledger row with the muted capability, the outcome delta and the marker count.

- **Make each capability's retirement a one-key merge** — FEATURE — value 3 — effort M — risk med — category: retirement
  Why: assumption: retirement stays theoretical unless it costs one action. Auto-draft a deletion patch with the capability's exam attached and a revert command ready, and let the standing push grant ship it only when the user's own ledger shows zero pulls.
  Done when: for one dormant capability, the patch plus its exam run green in a lane and a single command applies the removal.

- **Wild: Run a compute time machine on the bare model** — FEATURE — value 5 — effort L — risk med — category: forecasting
  Why: wild. Approximate next year's model by giving today's bare arm best-of-N sampling and long thinking. Any Sampo capability that still beats that arm is a real moat. One that doesn't is on borrowed time.
  Done when: each capability gets a "beats 10× bare" yes or no from held-out scenarios, in a table beside the existing free-arm scorecard.

- **Wild: Open a fossil museum on the site** — FEATURE — value 3 — effort S — risk low — category: delight, retirement
  Why: wild. Each retired capability gets a page with cause of death, the host feature that replaced it, and its lifespan. This makes retirement something to show off and counters the reluctance to delete that the standing "no idea is killed for ambition" rule encourages.
  Done when: one retired capability renders as a museum page on the site and links to the commit that removed it.

- **Wild: Let the tower hibernate unless pulled** — FEATURE — value 4 — effort M — risk med — category: dormancy
  Why: wild. The drive keeps generating, which fits "keep going", but it also fills the queue and ledgers. If the pull ratio stays under the floor for 7 days, the tower switches to maintenance only and wakes on a user message or a failing gate.
  Done when: a simulated week of zero user pulls puts the tower into hibernation and a message wakes it, with both transitions in the ledger.

- **Measure how much of a goal finishes with the host's plan mode and Sampo's critic only** — PERFORMANCE — value 4 — effort M — risk low — category: duel
  Why: assumption: the cheapest survivable Sampo is a critic layered over native planning. Run the long-horizon planted-fault scenarios in a third arm and report which clauses it misses.
  Done when: the scorecard prints three arms (plain, critic-only, full) for the same scenarios, and the clauses where full beats critic-only are listed.

Next question: which of the user's repeated asks are already satisfied by features the host shipped in the last 90 days, and does any ledger record the date a repeated ask stopped?
Next question: if the funnel's bulk model were swapped for a cheap hosted one, which of the 10,000 candidates' kill decisions would change, and who would notice?
