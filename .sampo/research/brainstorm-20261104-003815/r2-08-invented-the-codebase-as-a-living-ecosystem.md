# Brainstorm — lens: invented: the codebase as a living ecosystem

- **Estimate unseen defects by capture-recapture** — FEATURE — value 4 — effort M — risk low — category: quality
  Why: Cold reads, `fm find` and the canary already produce independent finder sets, but nothing says how many faults or stale doc claims remain unfound. Ecologists count unseen animals from the overlap between two independent trap-lines.
  Done when: on a scratch repo with N planted faults, the Lincoln-Petersen estimate from two independent finders lands within 25% of N, and `sampo doctor` prints "estimated unfound: k ± range".

- **Route data by photic zone** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: The pack has many separate privacy asks (scan before a non-local model, tmpfs for sensitive intermediates, egress receipts) but no single depth model. Give every state class a zone: sunlit may go to frontier models, twilight to local models only, abyssal never leaves disk. Each endpoint carries a depth rating, and the router refuses any send deeper than the endpoint's rating.
  Done when: a planted abyssal string never appears in any outbound request body across a full test run, and a twilight string appears only in requests to local endpoints.

- **Track biomagnification of untrusted text** — SECURITY — value 4 — effort M — risk med — category: injection
  Why: T-0791 lists injection defenses, but summaries and compaction concentrate whatever they read. A fetched page's instruction can come out of a lane's summary stripped of its origin. Carry a "dose" counter that rises with each summary hop, and treat high-dose text as data the Ward will not let drive an action.
  Done when: a planted instruction in a fetched page, passed through three summary hops, is still tagged untrusted and cannot trigger an outward action without confirmation.

- **Fit a metabolic scaling curve for task spend** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: T-1231 (the duel on cost and time) and `fm outcomes` hold per-task cost, but no baseline says what a task of a given size should cost. Fit a power law of tokens and seconds against diff size per repo and model, and flag a live task that sits well above the curve as probably thrashing.
  Done when: replayed on closed tasks, the curve flags known thrash runs at ≥70% recall with ≤20% false flags, and `fm next` shows "2.3× the usual for this size" on a live outlier.

- **Leave exploration patches by marginal value** — PERFORMANCE — value 4 — effort M — risk low — category: scouts and funnel
  Why: The 10,000-candidate funnel and scout subagents search until a fixed cap. The marginal value theorem says to leave a patch when the instantaneous yield falls below the long-run average. The existing rarefaction idea stops a whole lens; this applies the rule per patch (per directory, per cluster, per source).
  Done when: on a replayed scout run, the leave-rule keeps ≥90% of findings at ≤60% of the tokens.

- **Lay decaying pheromone trails on files** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: File-conflict forecasts and claims exist, but nothing records what a lane touched or failed on and then fades. Each lane drops a mark (touched, tests red, abandoned) with a half-life. A later lane's Read hook surfaces fresh marks, and old ones evaporate with no cleanup job.
  Done when: two lanes on overlapping files show a mark on first Read; the mark is gone after its half-life with no manual action; the merge-conflict rate on a replay drops.

- **Score lane risk by island biogeography** — FEATURE — value 3 — effort S — risk low — category: lanes
  Why: Worktree failures and base drift are recurring (the "show base drift" idea). Species-area theory says big, distant islands go extinct more often. Score a lane by diff size (area) and commits behind main (isolation), and warn or rebase before the score crosses the line where lanes have historically died.
  Done when: the score predicts which of the last 50 lanes needed a conflict-resolving rebase better than chance (AUC ≥ 0.7), and the pane shows it.

- **Publish a Red List field guide of capabilities** — FEATURE — value 3 — effort M — risk low — category: docs and UI
  Why: There are many ideas for a needed-share line, retire-when predicates and a claims ledger, but no single readable surface. Write one plate per capability with habitat (surfaces), diet (tokens per turn), predators (what disables it), and an IUCN-style status computed from ledgers: least concern, vulnerable, dormant, extinct-in-the-wild.
  Done when: `sampo guide` and a site page render every capability with a computed status and sources, and a cold child can name the three most endangered from the page alone.

- **Test for Allee-effect capabilities** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: Lessons recall (T-0217) and the user model only help above a minimum amount of data, while the dormancy ideas only look at decline. Detect capabilities with a minimum viable population and show "needs ≥N records, has k" instead of injecting noise; seed from the nearest repo (not a repeat of the inoculation idea) only when k is below N.
  Done when: a capability under its threshold stays silent and shows its k/N gauge; crossing N switches it on, and a replay shows no outcome loss from the silence.

- **Play the dawn chorus aloud** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: The morning card, night egress receipt and pulse ideas only target a screen. Compose a 30-second spoken or notification digest where each lane or agent "sings" one line, ordered by what needs the user, generated locally and delivered to phone or speaker.
  Done when: `sampo morning --voice` produces under 30 seconds of audio from the sealed night plan, with the "waiting on you" lines first, and nothing leaves the machine.

- **Wild: draw a sediment core of the project** — FEATURE — value 3 — effort M — risk low — category: UI
  Why: wild. Tower, ledgers and commits hold years of strata with datable events (the rename, generation shifts, the first false done). Render one vertical core in the web UI. Layers are coloured by activity type and event markers are tied to ledgers, and clicking a layer opens its records.
  Done when: the web page shows a scrollable core with at least 5 labelled event markers, and clicking a layer lists the underlying ledger rows.

- **Wild: hold a mast-year tournament** — FEATURE — value 3 — effort L — risk med — category: moons
  Why: wild. Trees fruit in synchronized mass years so predators can't eat everything. Once a month, fire every dormant or not-yet proposal at once into a scratch estate. The funnel can't kill them all, so survivors are chosen by outcome rather than by one cheerleader.
  Done when: a mast run files results for ≥100 candidates in one night against a scratch clone, and ≥1 dormant item with a flipped predicate is promoted with its evidence.

- **Wild: inject a keystone-absence drill into the tower** — FEATURE — value 3 — effort M — risk med — category: resilience
  Why: wild. Nightly in a clone, a "poacher" lane silently disables one randomly chosen verb. The drill measures whether the next session notices, through failures, wrong Next lines or silent regressions, and files each unnoticed absence as a missing-signal task. The existing keystone-by-removal idea scores importance; this measures detectability of loss.
  Done when: a drill run reports, per disabled verb, "noticed by X after N steps" or "unnoticed", and every unnoticed one becomes a filed task.

Next question: which of these ledgers would show the user a meaningful change within one week of install, so the ecosystem metaphor earns its place?
Next question: where does the metaphor mislead, and which ecological intuition would push Sampo into a worse choice than plain engineering?
