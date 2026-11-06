# Brainstorm — lens: capability map

- **Map assumptions to the rows that rest on them** — FEATURE — value 4 — effort M — risk low — category: plan integrity
  Why: assumption: the pack has expiring assumptions and per-row proofs, but nothing lists which rows depend on which assumption. A plan resumed after days can't tell what to reopen when one fact changes.
  Done when: flipping a named assumption in a fixture goal reopens exactly its dependent rows and no others.

- **Give goals a parent/child tree with roll-up** — FEATURE — value 3 — effort M — risk med — category: decomposition
  Why: assumption: "best-in-class" goals are often several products. The pack has fork/merge and hoisting shared rows, but no hierarchy. Child goals would carry their own oracle, and the parent's "done" would be the AND of its children.
  Done when: a parent goal with two children reports not done until both child oracles pass, and says which one is holding it up.

- **Add waiting rows with an external clock** — FEATURE — value 4 — effort S — risk low — category: long-running
  Why: assumption: real finishes include waits (a 7-day soak, a store review, DNS, a quota reset). Without a wait status these look like stalls and distort the finish band.
  Done when: a row marked `waits-until <date|predicate>` shows as "waiting", is excluded from the stalled-goal detector, and wakes on the predicate.

- **Pivot a goal with a salvage map** — FEATURE — value 4 — effort M — risk med — category: change handling
  Why: the pack has "close as superseded" and "carry cut rows into a successor", but no way to re-map done rows onto a changed goal. A mid-goal change is the usual way multi-day goals go wrong.
  Done when: `fm goal pivot "<new text>"` lists each done row as kept, reworded or void, and keeps the kept rows' proof.

- **Surface-first contract** — FEATURE — value 4 — effort M — risk low — category: definition of done
  Why: assumption: the pack has a demo script and a press release, but not the finished product's command, API or screen list written up front. That list is what a completeness check can diff against mechanically.
  Done when: finish prints the diff between the contract list and the built surface (added, missing, renamed), and the goal can't close with a "missing" entry unless it is struck with a reason.

- **Run the README as the finish probe** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: assumption: the pack smoke-runs docs commands for triggers, but a goal's own quickstart isn't executed at finish. This is the cheapest way to catch "done but nobody can start it".
  Done when: finish extracts the fenced commands from the product's README in a clean clone, runs them, and a broken command blocks done.

- **Estimate run-cost and quota rows** — FEATURE — value 3 — effort S — risk low — category: product ops
  Why: assumption: the pack budgets Foreman's own spend, not the finished product's monthly bill or API limits. A "finished" tool that costs $400 a month to run isn't finished.
  Done when: a goal that adds a paid service gets a row with an estimate and its source, and finish prints it.

- **Add a data-protection and restore-drill row pack** — FEATURE — value 3 — effort M — risk low — category: row packs
  Why: the pack has a security baseline pack and an egress manifest for Foreman itself. A product that stores user data would still lack a PII inventory and a backup restore test.
  Done when: a goal touching a database or user files gets rows for a data inventory and a scripted restore into a scratch dir, with the restore as a probe.

- **Re-survey the capability map on a clock** — FEATURE — value 3 — effort M — risk med — category: plan freshness
  Why: assumption: a best-in-class list written on day 1 is stale by day 9 when rivals ship. The pack watches upstream for the goal's own feature, but doesn't re-survey the capability list.
  Done when: a goal older than N days gets one re-survey that adds or flags rows, and each is marked "found on re-survey" in the scope ring.

- **Gauge plan churn and block building until it settles** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: the pack tracks scope growth after the fact. A churn rate during planning (rows added, merged or reworded per round) would say when the plan has settled.
  Done when: the planning stage reports churn per round and refuses to hand rows to builders until it falls below a set threshold or the user waives it.

- **Rewind a goal to a wave** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: the pack has day-end git refs and a replayable journal, but no single action that restores plan state and repo together to a past wave after a bad stretch.
  Done when: `fm goal rewind wave-2` in a scratch repo restores the plan file and moves the branch to wave 2's ref, after a preview and a confirm.

- **Mine rivals' removals into an anti-roadmap** — FEATURE — value 3 — effort M — risk low — category: scoping — wild
  Why: assumption: rival tools' changelogs list features they deprecated or removed, and those are known regrets. Rows matching them can be flagged before work starts.
  Done when: a surveyed rival's "removed" entries appear as flagged candidates in the survey, and each is kept or struck with a reason before the plan is accepted.

- **Show the plan as a tech tree in the web UI** — FEATURE — value 2 — effort M — risk low — category: web UI — wild
  Why: assumption: the pack proposes metro, fog-of-war and ghost-outline views. A tech tree whose nodes unlock "you can now…" lines and whose locked nodes name their prerequisites shows dependency and progress at once.
  Done when: the Goal page renders rows as nodes with locked, open and done states, and each locked node names the row that blocks it.

- **Ingest a screen recording of a rival as plan rows** — FEATURE — value 3 — effort L — risk med — category: intake — wild
  Why: assumption: the pack takes PRDs, sketches and whiteboard photos. A short recording of how a rival is used holds capabilities and flows the user would never write down.
  Done when: a recorded clip yields a candidate row list tagged `from-recording`, and the user can strike any row before the plan is accepted.

Next question: Which of the capabilities in this map does a goal over 7 days actually need, and which only matter to goals finished in one sitting?
Next question: When the user changes the goal mid-run, which closed proofs should survive, and who decides?
