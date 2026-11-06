# Brainstorm — lens: brainstorming and ideation methods

- **Mine the brainstorm's own ledger for saturation** — FEATURE — value 4 — effort M — risk low — category: ideation
  Why: 835 ideas plus three rounds with heavy repetition (e.g., "Race competing attempts," "Race competing approaches per task," "Race competing builder lanes" all appear). Assumption: no dedup of near-identical ideas across rounds exists beyond "show every idea."
  Done when: `fm ideas --merge` collapses a seeded set of 20 near-duplicate ideas into ≤8 clusters, each listing member titles, and a test asserts known duplicates land together.

- **Feed prior-round gaps back as a "holes" brief** — FEATURE — value 4 — effort M — risk low — category: ideation
  Why: Round 3 says "propose only NEW ideas," yet children receive a 900-line flat list and can't see where coverage is thin. Assumption: the pack is a plain list.
  Done when: before each round, `fm ideas` computes per-capability-axis counts and passes the three emptiest axes as a "go here" hint; a test shows the hint changes when the idea set changes.

- **Run a SCAMPER pass on each shipped capability** — FEATURE — value 3 — effort S — risk low — category: ideation
  Why: Ideas so far are mostly additive; none systematically ask what to substitute, combine, eliminate or reverse in existing Foreman features (guard, drive, recall). Assumption: this method isn't a lens today.
  Done when: `fm ideas --lens scamper --target <module>` outputs ≥7 ideas, one per SCAMPER verb, each citing the module's real commands.

- **Brainstorm from the user's complaint log, not the project description** — FEATURE — value 5 — effort M — risk low — category: ideation
  Why: The user's steers ("cleanup requests never got done," "budget limits shouldn't block until 75%") are the strongest signal, yet the pack's project text dominates. Assumption: friction/steer events are structured in the ledger.
  Done when: a `complaints` lens receives only steers/drops/corrections and the project's one-line purpose; a test confirms its pack excludes the README body and includes every steer from the last 30 days.

- **Add a "jobs to be done" reframing lens** — FEATURE — value 3 — effort S — risk low — category: ideation
  Why: Requests arrive as features ("C089 Fast hooks"); the underlying job (user never waits on Foreman) is unstated, so ideas cluster around mechanisms. Assumption: no JTBD framing exists.
  Done when: each captured request gets a "when I… I want to… so I can…" line, and the lens prompts on those lines produce ideas whose Why cites a job statement.

- **Score ideas by user-keep prediction using the captured/skipped history** — FEATURE — value 4 — effort M — risk med — category: ranking
  Why: The punch list shows many C-items marked skip versus captured; the user said "I like almost all of those," so a naive value score misleads. Assumption: skip/keep flags are stored per idea.
  Done when: `fm ideas --rank` shows a predicted-keep score per idea and a backtest on the past rounds reports rank correlation against actual keeps.

- **Split divergent from convergent into separate agents with different temperatures** — FEATURE — value 3 — effort M — risk low — category: agent types
  Why: Same child both invents and self-scores value/effort/risk, mixing the modes. Assumption: scoring currently happens in the generating child.
  Done when: generators emit unscored ideas, a separate scorer agent rates them, and a bench case shows score variance across reruns falls versus the current format.

- **Run reverse brainstorming on every L plan** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: Pre-mortem ideas exist, but not "how would we guarantee this task fails?" as a generated checklist that becomes acceptance criteria. Assumption: not covered by the pre-mortem entries.
  Done when: an L brief gains a "ways to guarantee failure" section of ≥5 items and at least one converts into a verify command.

- **Wild: Let ideas carry a stake that decays unless someone defends them** — FEATURE — value 3 — effort M — risk med — category: ideation
  Why: assumption: huge idea piles rot unseen. Each idea has a half-life; the user or an agent must cite fresh evidence to renew it, otherwise it archives itself.
  Done when: ideas older than N days without a renewal vanish from the default view yet remain searchable, and a test shows renewal resets the clock.

- **Wild: Brainstorm in a persona of the project's three worst past bugs** — FEATURE — value 3 — effort M — risk low — category: ideation
  Why: The ledger holds real failures (guard bypass via `bash -lc`, no-op `-k` verify). Asking "what idea would have prevented me?" from each incident's viewpoint grounds ideas in scars. Assumption: incident summaries are retrievable via recall.
  Done when: a lens takes the top 3 recalled failures and every produced idea names the failure it would have prevented.

- **Wild: Hold an idea tasting where the user reacts in one keystroke per card** — FEATURE — value 4 — effort M — risk low — category: ideation UI
  Why: Reviewing hundreds of ideas in text is the bottleneck; the user already bulk-approves ("I like almost all"). Swipe-style keep/drop/later feeds the taste model directly.
  Done when: the web UI shows one idea card at a time with keyboard keys for keep/drop/later, and each choice is written to the ledger with the idea id.

- **Detect when an idea is a rename of something already built** — FIX — value 3 — effort S — risk low — category: ideation
  Why: Ideas like "Run the edit-time test sentinel" appear alongside T-0214 already in the open work. Assumption: no check against the open task list and shipped features is done at proposal time.
  Done when: `fm ideas` flags any idea whose title matches an open or done task above a similarity threshold, with the task id attached, and a test covers the T-0214 case.
