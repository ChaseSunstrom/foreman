# Brainstorm — lens: unspoken needs

**Answers to earlier questions (unspoken-needs view):**
- *Offline proofs:* The guard corpus, hook-latency bench, context-size count and eject round trip need no network or secrets. Mark these the default tier. Everything else is labelled "needs outside".
- *Skipped proofs:* The user's steers keep asking for automatic checks (`fm decide --check`), not reports, so a proof they never open should become a gate or be deleted.
- *Docs vs code:* The code is the bug unless a steer says otherwise. The user is told in one line, not asked.

---

- **Print a steer receipt with queue impact** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: The user sends numbered steers (#1/#2/#3) and then has to add "T-2462 waits with T-2441" and "T-2450, T-2444… wait for round 1" by hand. Nothing showed which open tasks each steer moves.
  Done when: after a message carrying 3 steers, `fm` prints each steer, its stored rule, its automatic check and the task ids whose order or state it changes. A test uses the round-first steer and expects T-2450 to be named.

- **Add a tower runaway breaker** — SECURITY — value 4 — effort M — risk low — category: tower
  Why: The standing rule says a red sweep files its own fix tasks and re-runs when they close. Nothing shown caps the filing or catches the same row going red again after its fix closed.
  Done when: a fixture sweep that re-reds the same row twice stops filing, records one `fm decide --kind costly`, and keeps going on other rows.

- **File sweep fix tasks already planned** — FIX — value 4 — effort S — risk low — category: tower
  Why: The user's own words: "Sweep fix tasks are filed unplanned (tier M, no criterion, no regression test), so each needs re-planning and a typed red before it can close."
  Done when: a task filed from a red sweep row carries a tier, a criterion copied from the row's check, and a red-test stub. `fm task finish` accepts it without a re-plan.

- **Show held-back items with age and release condition** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: `--round-first` hides Foreman-filed items (ci, self, discovered) and the drive holds T-2462. The pack shows no view of what is held, since when, or what frees it. Starvation would be silent.
  Done when: `fm next --held` lists each held item with its age and the exact event that releases it. An item held past N days is flagged.

- **Require every coverage cell to name a session path that calls it** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: A standing rule says every capability must be called by a real session path, not only exist as a verb. The 61 cells are at risk of being filled with verbs nothing calls.
  Done when: `fm genesis check` fails a cell whose named verb is not invoked by a hook, a skill, `fm next` or the drive, and prints the cell and the missing caller.

- **Default headless and server installs to a core profile** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: T-0794 (Slim Foreman, Lite mode) sits deferred. The headless/server column is among the empty cells, and the SessionStart note costs about 2k chars × 89. Server users likely want the guard and the done-gate only. (assumption: they do not need the pane or UI hooks)
  Done when: `install.sh --profile core` registers only the guard and Stop hooks. The p95 and injected bytes in `fm doctor` are lower than the full profile, and the guard corpus still passes.

- **Add a user-minted one-shot allow for a guard block** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42 times in 7 days. A user in bypass mode who is blocked wrongly will want an escape that doesn't mean editing the guard. (assumption: some of the 42 were legitimate)
  Done when: a user-run `fm allow-once <rule>` writes a grant to a channel the agent cannot write. It permits the next matching call only and expires after 10 minutes. The use is logged and surfaced in the final report.

- **Cap scratch use under the tmpfs children directory** — FIX — value 3 — effort S — risk low — category: reliability
  Why: Brainstorm children run in `/run/user/1000/fm-children-1000`, which is tmpfs and so RAM-backed. (assumption: children and packs accumulate there)
  Done when: a stale-child sweep removes directories older than N hours, and a test fills the cap and shows new children refused with a clear message, not killed.

- **Charge the tower's own cost to a ledger** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: The user cares about lean growth and has a $100 budget. Cold reads, sweeps and critiques per generation are never totalled against what shipped. (assumption: the cost is non-trivial)
  Done when: `fm genesis` prints tokens and dollars per generation split into product work and tower overhead, and the lean row cites it.

- **Wild: Generate "letter defeats intent" scenarios for each steer** — FEATURE — value 3 — effort M — risk low — category: steers
  Why: wild. Several steers can collide in the letter: "don't stop for budget" against the fm budget cap and the risk budget, or "never block on the user" against "outward actions need the user". A tool-less child could write the situation where obeying the letter harms the user, and the record then settles which wins.
  Done when: for 5 chosen steers, each gets a stored scenario and a recorded resolution that `fm decide` can cite.

- **Wild: Plot growth rings on the Genesis site** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. The lean weigh-in exists as numbers. A cross-section where each generation is a ring, with width as growth and cuts as bark scars for deletions, would make "subtract as you add" something the user could show people.
  Done when: `site/genesis` renders a ring per generation from the lean data. A test checks that the ring count equals the generation count.

- **Wild: Forecast the date the lean ratchet will bite** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: wild. Hook p95, injected context and verb count are tracked as snapshots. A fitted trend would say "at this rate p95 breaks the budget in about 3 generations", so the cut is planned instead of forced.
  Done when: `fm doctor` prints one line with each metric's projected crossing generation, or "no trend yet" when there are fewer than 4 points.

- **Wild: Let each generation write its own obituary list for cells** — CLEAN — value 2 — effort S — risk low — category: coverage
  Why: wild. The rule says "no cell is ever removed from frame.md", but a filled cell can go quietly unused. A short list of cells whose path has not fired in a generation, shown as "sleeping" and never deleted, keeps the grid honest without breaking the rule.
  Done when: the sweep prints sleeping cells with their last-fired generation. A test confirms no cell is removed from `frame.md`.

Next question: Which of the 61 empty cells have no plausible measurement at all (for example, "learn" × "site"), and should they be recorded n/a with an expiry instead of filled?
Next question: What does the user do in the first 10 minutes after a long unattended run, and which of today's outputs does that first look depend on?
