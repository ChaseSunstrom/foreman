# Brainstorm — lens: self-modification

- **Reject self-changes whose evidence came from untrusted text** — SECURITY — value 4 — effort S — risk low — category: self-mod guard
  Why: the pack lists "treat the stranger repo's own text as data" and "scrub carry-over", but nothing checks the evidence behind a proposed change. assumption: proposals cite a source today only informally.
  Done when: a self-change citing only repo prose or README text, with no outside signal (outcomes, `fm second`, plain-arm delta), is refused in a test, and one citing a 30-day survival drop is accepted.

- **Trace every self-change to a quote from the user** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user steered "I don't want foreman hardcoded, I want it smarter", and their steers and drops are the real spec. A change that removes no pain they've voiced is churn.
  Done when: `fm genesis` rejects a self-change with no linked ask, steer, drop or outside-signal id, and `status` shows the linked quote for each change.

- **Score each exam scenario by how well it discriminates** — FEATURE — value 4 — effort M — risk med — category: exam self-tuning
  Why: exam runs already have oracle, empty, finders and foreman and plain arms, so every scenario has a score for each. Scenarios that every arm passes or fails carry no signal for selection. assumption: per-arm results are stored per scenario in exam.jsonl.
  Done when: a discrimination index (oracle pass, empty fail, arms spread) is computed per scenario, and a flat scenario is flagged for replacement at the next generation.

- **Gate self-changes on a legibility read** — FEATURE — value 4 — effort M — risk med — category: self-mod guard
  Why: "predict effect, then score" has the proposer grade itself. A tool-less child given only the diff and a probe list predicts which behaviors change, and a mismatch with the measured probe diff shows the change is too opaque to trust.
  Done when: a change whose reader predictions miss more than a set share of the measured probe diffs is held, and a test covers a deliberately obscure diff.

- **Re-audit self-written rules when a new steer arrives** — FEATURE — value 4 — effort M — risk low — category: charter drift
  Why: steers keep arriving (the hardcoding correction, the "tower files only in genesis storage" rule). Existing items cover steer-vs-steer conflicts, not what a fresh steer does to rules Genesis already wrote.
  Done when: filing a steer re-runs `fm second` on the self-authored rules that share its vocabulary, and contradicted rules are listed as candidates for removal.

- **Fall back to a safe-mode vintage when the evolved Genesis fails to start** — FIX — value 4 — effort M — risk low — category: reliability
  Why: Genesis rewrites its own templates, and a bad rewrite that breaks parsing would disable the very verb that could fix it. The `fm genesis` self-test runs at open.
  Done when: a corrupted self-authored template makes `fm genesis status` load the pinned minimal vintage and print one line saying so, and a test proves it.

- **Let Genesis author project skills and playbooks within the listing budget** — FEATURE — value 4 — effort L — risk med — category: capability
  Why: the user asked for "many more skills" and playbooks "within the skill-listing budget". A project's own tower is the natural source of grounded, project-specific ones.
  Done when: a tower run on a fixture proposes at least one skill that passes the description lint and trigger test, and one that busts the budget is refused.

- **Ship self-changes through stable and next channels** — FEATURE — value 3 — effort M — risk med — category: rollout
  Why: assumption: the user cannot tell a vetted improvement from one a single tower likes. A `next` channel runs in opted-in projects and promotes to `stable` only after N generations and M projects without regression.
  Done when: a change lands in `next` only, `fm genesis channel` shows each vintage's soak count, and promotion needs the threshold.

- **Anneal the self-change budget** — FEATURE — value 3 — effort S — risk low — category: self-mod guard
  Why: a fixed cap treats a young tower and a plateaued one alike. Shrink the allowed edit size as selection wins flatten, and widen it after a regression exposes a real gap.
  Done when: the cap, in lines changed, falls after three flat generations and rises after a regression, and a test pins both.

- **Wild: Run a naked generation every Nth round** — FEATURE — value 3 — effort S — risk low — category: cruft control
  Why: accumulated carry-over defaults may add cost without helping. One generation runs with all of them off, on the same held-out scenarios, and the gap says if they pay. wild
  Done when: the naked run's closed count and cost are logged beside the normal run's, and defaults that fail to beat it are flagged.

- **Wild: Weight proposer lenses by forecast calibration** — FEATURE — value 3 — effort M — risk med — category: self-mod allocation
  Why: each proposer states the expected exam delta, and a Brier-style score decides how many changes it may land next generation. Honest forecasters get more room and boasters get less. wild
  Done when: a proposer that overstates twice sees its quota fall, shown in `status`.

- **Wild: Quine check on the genome** — TEST via FEATURE — value 3 — effort M — risk low — category: reproducibility
  Why: export Genesis's templates and lens weights as a single Seed, cold-start a fresh Genesis from it, and compare probe behavior. A large gap means the self-changes live in hidden state. wild
  Done when: the round-trip's probe diff is under a threshold on a fixture, and a hidden-state change makes it fail.

- **Make the shared defaults file merge-safe across concurrent towers** — FIX — value 3 — effort M — risk med — category: carry-over
  Why: assumption: towers on several projects write one carry-over `defaults.json` that loop and scout may touch at the same time. Use an append-only log with compaction and a lock.
  Done when: two concurrent writers lose no entry in a test, and compaction replays to the same defaults.

Next question: What does an accepted self-change cost in the user's own attention (reviews, vetoes, reverts), and is that falling over time?
Next question: Which self-changes survive a model upgrade unchanged, and does Foreman know before it spends a generation relearning them?
