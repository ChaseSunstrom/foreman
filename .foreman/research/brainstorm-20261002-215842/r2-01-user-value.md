# Brainstorm — lens: user value

- **Make every ignored "Next:" hint measurable** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumption: the pack says hints "can be ignored, only gates are enforced" and drive stopped on a "Next: back to the queue" line. Nobody can see how often hints are followed, so rules can't be pruned by evidence (T-0085).
  Done when: `fm report hints` shows, per hint type over the last 50 tasks, the count issued vs. followed within 3 turns, and the lowest-followed hints are flagged as candidates for a gate or deletion.

- **Add "ask once, answer for the whole queue" approvals** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: protected-core edits need a yes per task and plugin updates need their own yes, which stalls unattended runs while the user wants full autonomy. Wild neighbors exist ("batch yeses at session start"), but the missing piece is scoped, expiring grants, not a batch.
  Done when: the user can grant "protected-core edits under path X until the queue empties or N hours pass". A grant is recorded in the ledger, shown in the band, revocable in one key, and an edit outside the scope still prompts.

- **Show a plain-language "what changed for you" at task close** — FEATURE — value 5 — effort S — risk low — category: output clarity
  Why: the user said "clean up your output" and "L, T, M mean nothing". They are usage-sensitive and away for hours, so they need outcomes (behavior now different, what to try, what was left undone), not the evidence trail.
  Done when: `fm task finish` ends with ≤ 4 lines: what you can now do or see, what was deliberately not done, and anything that needs a decision. A test confirms no stage or tier jargon appears.

- **Detect and surface "work the user probably wants next" from their pushback patterns** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: the user repeats complaint themes (slow, stale, ugly output, tokens). A mining pass over the inbox and request history could cluster them into standing preferences ("always quiet", "never burn tokens") that become checked acceptance criteria on every plan.
  Done when: `fm prefs` lists ≥ 5 inferred standing preferences with the quoted source requests. A new plan that violates one (e.g. adds a full-suite gate per task) gets a visible warning before approval.

- **Give each gate a cost-per-catch score** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: gates cost 18.8 hours total and one project's `cargo test` runs about 8 min per task. Nothing says which gates ever caught a real failure, so the speedups proposed so far (caching, affected-tests) are guesses about where to cut.
  Done when: `fm gates --worth` prints, per gate, minutes spent vs. failures caught and later fixed. A gate with zero catches over 30 runs is suggested for demotion to once-per-queue.

- **Estimate hours before a plan is approved** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: the user complains tasks take hours, but the plan card shows only steps. Medians from 287 tasks make a range estimate cheap. (Per-task budgets were proposed in a wild idea; this is the visible estimate, not the enforcement.)
  Done when: the plan card shows "typically 20-50 min for tasks like this (n=…)", and the task close line compares actual vs. estimate.

- **Warn when a long task's context holds facts older than the docs** — FIX — value 3 — effort M — risk low — category: freshness
  Why: the user asked about context rot and out-of-date information. Compaction at 40% helps, but nothing compares recorded claims to the files they came from.
  Done when: on resume, any recorded fact citing a file changed since it was written is listed as "stale: re-check", and a test shows a changed file flagging the fact.

- **Wild: Let Foreman interview the user for 2 minutes at project start** — FEATURE — value 4 — effort S — risk low — category: unspoken needs — wild
  Why: the user says brainstorms miss "things I want but don't know how to say". A short A/B questionnaire ("which of these two outputs do you prefer?") with real screens from their own sessions could extract taste more directly than inference from words.
  Done when: `fm taste` runs ≤ 8 paired-choice questions built from the project's past output, saves a profile, and the next brainstorm's ideas cite which answers shaped them.

- **Wild: Run a "red team the user's day" pass** — FEATURE — value 3 — effort M — risk low — category: foresight — wild
  Why: assumption: with long unattended runs, the likeliest regrets are things like a surprise bill, an overnight force-push, or a silently skipped task. A pre-flight pass could list the three most likely regrets for a run and offer a one-key guard for each.
  Done when: starting drive mode prints ≤ 3 risks with a guard toggle each, and choosing one makes the matching gate or limit active in the ledger.

- **Wild: Let the queue negotiate its own order** — FEATURE — value 3 — effort L — risk med — category: queue intelligence — wild
  Why: the queue is processed in order, but tasks differ in cost and in how much they unblock. Reordering by (value ÷ expected time) and by shared files, so related tasks batch together and share one full gate run, could cut the hours the user complains about.
  Done when: `fm queue --suggest` proposes a reorder with the reason for each move. Accepting it measurably reduces full-suite runs on a replay of the last 20 tasks.
