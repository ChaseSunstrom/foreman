# Brainstorm — lens: unspoken needs

- **Stop re-proposing: add a dedup-against-shipped gate for the brainstorm itself** — FIX — value 5 — effort S — risk low — category: self-improve
  Why: the "ideas so far" list has ~300 entries with many near-duplicates (fsck, flaky, stranger test, shadow-user appear 3-6 times); the user asked for "groundbreaking", and repeats waste budget. `fmideas` could cluster against shipped/inbox/prior ideas by BM25 and drop or merge before presenting.
  Done when: feeding fmideas two near-identical titles yields one cluster line with a count, and a title matching a shipped item is dropped with a reason.

- **Ship a "taste profile" distilled from the user's steers and drops** — FEATURE — value 5 — effort M — risk low — category: preference
  Why: drops ("premise false: measured…") and steers ("criterion widened to a permanent check") show the user prizes measured premises over plausible ones and permanent checks over one-offs. That's a stable preference that is never stated. It could rank ideas and shape briefs (assumption: ledger holds enough of these events).
  Done when: `fm taste` prints ≥5 rules, each citing ledger events, and `fm ideas` ranking cites the rule that moved an item.

- **Require a premise measurement before any PERF or "drop" brief closes** — FEATURE — value 4 — effort S — risk low — category: evidence
  Why: two of five drops died on "premise false: measured 0.14 s vs 6.5 s" and "none named a task already finished". Measuring first would have avoided building them. Task intake could demand a one-line measurement command for performance claims.
  Done when: a PERF brief without a measurement criterion gets a nudge at `fm task new`, and the nudge clears once one is added.

- **Auto-close the drive's "waiting" turns by making the wait a state, not a turn end** — PERFORMANCE — value 4 — effort M — risk med — category: drive
  Why: 18 turn-ends were spent waiting on the reviewer; each costs a resume prompt. Distinct from earlier "bounded wait" ideas: it measures the actual cost per wait and exposes it in `fm cost` so the saving is provable (assumption: Stop hook can hold a short poll).
  Done when: `fm cost` reports waits per task, and a drive with a pending reviewer produces zero extra turn-ends in a replay.

- **Add a "batch the reviewer findings by class" report after each review** — FEATURE — value 3 — effort S — risk low — category: review
  Why: reviews found 3–7 issues each time, mostly new-parser edges and export privacy. Grouping findings by class across tasks shows which class recurs and seeds an intake checklist (not the generic fuzz-seed idea already listed).
  Done when: `fm friction` shows a top-3 recurring finding classes table from at least 5 reviews.

- **Write the guard's false positives as a "teach" step during the block, not afterwards** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: three known false positives (stash list, heredoc editing plugin source, read-only state reads) were found by friction, not at block time. When a block is overridden by the user's grant, record command + grant as a candidate replay case automatically, never loosening the guard itself.
  Done when: granting an approval after a block appends a corpus case and `fm replay` reports it as "pending review".

- **Wild: Let Foreman keep a "things I assumed about you" page the user can correct** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumed-vs-verified exists for code facts, not for the user. Inferences like "prefers permanent checks" or "wants no pushes" are used silently; surfacing them lets the user fix them in one line (wild).
  Done when: `fm me` lists inferred preferences with evidence, and deleting one stops it affecting nudges.

- **Wild: Add a "cost of this conversation to the user's attention" meter** — FEATURE — value 3 — effort M — risk low — category: attention
  Why: the user repeatedly asks for speed without losing quality, yet only tokens and dollars are metered. Count interruptions, questions, and re-explanations per task, and trend them (wild).
  Done when: the task close report shows interruptions, and `fm friction` trends them week over week.

- **Wild: Let a finished pass be "audited by its own next pass" automatically** — FEATURE — value 4 — effort M — risk med — category: self-improve
  Why: the user asked for numerous recursive passes; today each pass's output is judged by the user. At the next pass start, replay the last pass's shipped items against bench and friction to flag any that moved nothing, and propose cutting them (wild).
  Done when: the pass-start report lists each prior item with a before/after metric or "no measurable effect".

- **Cut the open inbox by merging 17 items into three named pipelines, with removals recorded** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: the inbox overlaps heavily (regression court, shadow-user soak, counterfactual ledger, skill duels, bench judge all share a replay-and-judge core; night shift, landscape, release watch share a scheduler). Reducing it lets the user see a real plan. A review of the list suggests `stranger test` and `Foreman MCP server` already appear as asked/done, so the inbox is stale there.
  Done when: `fm inbox` shows ≤6 entries, each a pipeline with its absorbed items listed and each cut item carrying a reason.
