# Brainstorm — lens: 2030 worked back

- **Version the user-model as a portable file** — FEATURE — value 5 — effort M — risk low — category: durability
  Why: assumption: the predictor's tables (follow-ups, rituals, estate, pushbacks) are spread across ledgers and code. A model swap or machine move in the next four years would lose them. The standing rule that the orchestrator can be any agent points the same way.
  Done when: `sampo anticipate export` writes one file with a schema version and per-field source ledger ids, and `import` on a scratch home reproduces the same predictions for a frozen day. A v1 file migrates to v2 in a test.

- **Gate model swaps on an inheritance exam** — FEATURE — value 5 — effort M — risk low — category: models
  Why: the steers say local models are scaffolded to frontier results, and the endpoint changes models at a cost of ~3 min. By 2030 the model ID will have changed many times. Replay about 100 historical asks (cutoff-split) through the incumbent and the newcomer, and promote only on a tie or better.
  Done when: a new model id on a profile gets a one-line verdict (promote, hold or retire scaffold X) from a zero-network replay, and a planted worse model is held.

- **Harvest every draft and the user's edit as preference pairs** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: assumption: drafted briefs are the best labelled data Sampo will ever have on the user's taste. The user's rewrites and drops (`dropped:` lines) are the labels, and they stay local (privacy lens).
  Done when: a local JSONL of (context hash, draft, final, verdict) grows per draft. A command lists the count per task kind and refuses to leave the machine without an explicit setting.

- **Backcast a dated 2030 ladder, and make rung one the Mission** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: the request is a long arc ("predicts the next request, flags problems before they happen"). Write six milestones from 2027 to 2030, such as "drafts land unedited for kind X" and "predictor beats the host's own suggestion". Each gets a live-state Exam, which is the carried gap.
  Done when: `research/genesis` holds the ladder, each rung names an `fm … --json` key path that reads true or false today, and `fm doctor` prints which rung is current.

- **Defer to the host's native next-prompt suggestion when it beats ours** — FEATURE — value 4 — effort M — risk low — category: retirement
  Why: assumption: hosts will ship their own suggestions. The steers say Sampo is the discipline layer and does not duplicate what the host does. Score both on the same real follow-ups and mute ours where it loses.
  Done when: a shadow log records both suggestions and the user's actual next ask, and the lower scorer per task kind is muted automatically with a ledger line.

- **Freeze monthly predictor vintages and score them all forever** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: no single hit rate says whether the predictor is improving over years. Keeping every vintage and scoring each on new asks gives a curve, and a vintage that beats current is a regression alarm.
  Done when: `sampo anticipate vintages` prints a table of vintage × last-30-day hit rate, and a planted bad update shows as a dip.

- **Re-baseline after a long absence or regime change** — FIX — value 3 — effort S — risk low — category: drift
  Why: assumption: a predictor trained on a busy autumn will confidently predict stale habits after a 30-day gap or a new repo family. Detect the gap, drop the weights to a recency baseline, and show "re-learning" on the card.
  Done when: with a 30-day gap in a fixture ledger, the first card says "re-learning" and the prediction weights match the baseline test.

- **Promote drafts by per-kind trust** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user wants major progress by morning and also gave a standing push grant. Ladder: draft → lane branch → probation ref → main, climbing after N unedited accepts for that kind and falling on any revert.
  Done when: a fixture with 5 unedited accepts moves a kind up one rung, a revert moves it down, and nothing reaches main without the existing `fm ship` gate.

- **Rebuild the estate from probes on a new machine** — FEATURE — value 3 — effort M — risk low — category: machines
  Why: assumption: the 27B server and the Arch box will be replaced before 2030. One command should re-probe endpoints, models, toolchains and resident-model switch cost, then diff against the old estate.
  Done when: `sampo estate rebuild` on a scratch home yields the same estate file as the live one, with differences listed.

- **Wild: Summarise a "what you are building" paragraph from years of asks** — FEATURE — value 4 — effort M — risk med — category: understanding
  Why: wild. A cold local model reads only the asks and drops and names the unspoken through-line, which anchors the predictor and is shown to the user to strike through. Score it by whether next quarter's asks fit it.
  Done when: the paragraph is stored with its source ask ids, the user can strike a clause, and a struck clause lowers the weights of its sources.

- **Wild: Let the user write a north-star sentence and score drift from it** — FEATURE — value 3 — effort S — risk low — category: intent
  Why: wild. A sentence about where they want the project in 2030, used as a weak prior. A quarterly line says how much of the actual asks served it versus wandered, with no verdict, just a mirror.
  Done when: `fm north set "…"` stores it, and a card reports its share of the last 30 days of asks it matched.

- **Wild: Make the predictor keep a "letter to the 2030 me" of its own known weak spots** — CLEAN — value 3 — effort S — risk low — category: honesty
  Why: wild. Every time a confident prediction misses, it appends one line of cause. A year on, a cold child groups those lines into failure classes and each class becomes a canary near the idea.
  Done when: the file grows on a planted miss, and a grouping pass produces at least one named class from a fixture of 20 lines.

- **Cap user-model growth with epoch summaries** — PERFORMANCE — value 3 — effort M — risk low — category: scale
  Why: assumption: four years of ledgers will slow session-start reads and bloat the card. Keep raw for 90 days and compress older data into weekly, monthly and yearly epochs, with a diff between epochs.
  Done when: a synthetic 5-year ledger keeps the anticipation read under the hook bench bar, and predictions on the last 90 days are identical before and after compaction.

Next question: which of the user's habits have been stable for over a year, and which would a 2030 predictor wrongly freeze in?
Next question: what would the user need to see on one screen to trust an unedited landed draft without opening the diff?
