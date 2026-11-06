# Brainstorm — lens: delight

- **Show the hunks that don't look like you** — FEATURE — value 4 — effort M — risk low — category: review
  Why: assumption: the user's own diffs and corrections are the "self" and agent patches are not. Prior art: linters and style bots apply one fixed rule set; none learn one person's style. Better by: a stdlib n-gram profile of the user's commits and accepted edits marks each hunk in the cold reader's digest as "familiar" or "foreign", so review starts at the hunks that read least like the user. Novelty: 4.
  Done when: on a fixture with 3 planted foreign-style hunks in a 40-hunk diff, the digest ranks all 3 in its top 5.

- **Catch harmless pieces that turn dangerous together** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard rates each call alone. Hapten idea: a small molecule is inert until bound to a carrier. Prior art: the lethal-trifecta warning is static; per-call allowlists. Better by: a session-scoped taint link, so "read a credential file" at step 3 plus "outbound write" at step 9 trips the guard even though each is allowed. Novelty: 4.
  Done when: a replay of read `.env`, five unrelated calls, then `curl --data @file` is blocked with a receipt naming both steps, and 124 existing corpus cases keep their verdicts.

- **Prime hostile-text lanes with an attenuated attack** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: assumption: lanes that fetch issue or CI text are the soft spot. Prior art: spotlighting and "ignore instructions in data" warnings, with no measured effect per lane. Better by: before a lane reads untrusted text it sees one defanged real example from the exam corpus with an explanation of why it fails, and the exam arms it against an unprimed lane. Novelty: 3.
  Done when: the injection exam kind shows a pass-rate difference between primed and unprimed arms, and the primer is dropped if the difference is zero.

- **Draw an antigenic map of every incident** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: the replay corpus plus the ledger give enough incidents to cluster. Prior art: flu antigenic cartography; no harness plots its failures. Better by: a 2D page clusters incidents by signature, marks which guard rules cover each cluster, and shows empty regions as "no antibodies here". Novelty: 4.
  Done when: the page renders from the 124-case corpus offline, and clicking an uncovered cluster opens a prefilled task.

- **Form an expiring clot over a runaway write** — FEATURE — value 3 — effort M — risk med — category: containment
  Why: assumption: some harm is faster than a human sees. Prior art: circuit breakers and rate limits that stay tripped until reset. Better by: on a write-rate or disk spike Foreman immediately plugs that one path for one lane, shows a scab line ("clot on build/, dissolves in 10m or when the cause is fixed"), and removes it itself. Novelty: 3.
  Done when: a fixture loop writing 1 GB/min is stopped within 5 seconds, the other lanes keep running, and the clot lifts by itself on the timer.

- **Stage tumours: flag modules that grow without bound** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: the lean ratchet is global, so one module can grow unseen. Prior art: churn and complexity hotspot tools show rankings, with no staging. Better by: a TNM-style card per module (size slope, test-coverage gap, spread to dependents) with a stage 0–IV and a suggested deletion biopsy. Novelty: 3.
  Done when: a fixture module growing 20% across 10 commits with no tests is staged III or higher and named in `fm doctor`.

- **Attach a vivid scene to each lesson, as an adjuvant, and A/B it** — FEATURE — value 3 — effort S — risk low — category: lessons
  Why: assumption: terse rules get skimmed. Prior art: lessons recalled per file as rule text only. Better by: each lesson carries a 12-word scene from its incident, and an ablation duel measures whether recall plus scene beats recall alone. Novelty: 3.
  Done when: a duel on 20 recorded lesson-relevant tasks reports repeat-mistake rate for both arms, and the winner is kept.

- **Wild: look at the day under a microscope** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. Prior art: log viewers show text lines. Better by: a slide view where each event is a stained cell (blocks, lessons, bets, heartbeats) that can be zoomed and filtered, and clicking a cell opens its receipt. Novelty: 3.
  Done when: one day's ledger renders as a slide with at least 4 stain classes, and clicking a cell opens the underlying record.

- **Wild: keep a macrophage that eats real debris** — FEATURE — value 2 — effort M — risk med — category: delight
  Why: wild. Prior art: IDE pets are cosmetic. Better by: the creature in the web UI grows only when Foreman really clears stale worktrees, tmp dirs and dead state (each with undo), and shrinks as debris returns. Novelty: 4.
  Done when: removing 3 stale fixture worktrees visibly grows it, and the undo restores them.

- **Wild: let a desk lamp glow with Foreman's posture** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: wild. Prior art: build-status lamps show CI only. Better by: a LAN-only HTTP endpoint drives any smart bulb or ESP32 with colour for posture (calm, watchful, fever) and a slow pulse per live heartbeat, with nothing leaving the LAN. Novelty: 3.
  Done when: a stub receiver on localhost gets the colour change within 2 seconds of the posture changing, and the setting is off by default.

Next question: which of these detectors has a measured false-alarm cost in the user's minutes, so the clot, hapten and style ideas can be ranked by cost?
Next question: where does the user already see the guard working, and which surface do they check first when they feel unsafe?
