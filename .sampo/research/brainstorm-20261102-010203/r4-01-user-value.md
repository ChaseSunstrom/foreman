# Brainstorm — lens: user value

Most immune mechanisms are already in the ideas list, so these ten stay off it. They either come from a mechanism nobody drew on or fill a gap between listed ideas. Prior art, Better by and Novelty are folded into each Why line.

- **Split mechanical bulk from the semantic hapten in a big diff** — FEATURE — value 4 — effort M — risk med — category: review
  Why: assumption: a small risky edit (a deleted check) hides inside a large rename or format diff, and a cold reader's attention dilutes. Prior art: semantic-diff and tangled-change research, nothing in a harness. Better by: replay the mechanical transform, then show only the residual to the existing cold reader. Novelty 4.
  Done when: a fixture diff with a 1,500-line rename plus one removed guard clause produces a residual of at most 5 hunks that includes the removal.

- **Watch a bad idiom while it is still spreading** — FEATURE — value 4 — effort M — risk low — category: drift
  Why: assumption: agents copy patterns from neighbouring code, so one lane's mistake gets cloned by the next (clonal expansion). Prior art: code-smell dashboards count totals, not growth rate. Better by: count a pattern's new instances per commit window and warn at the second consecutive rise. Novelty 3.
  Done when: replaying a fixture history where a swallowed-exception idiom grows from 1 to 6 instances warns before the 4th.

- **Score each lesson by harm, not hits** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: assumption: a recalled lesson can make related failures more likely (antibody-dependent enhancement). Ablation duels measure features, not individual lessons. Prior art: none found. Better by: a natural experiment comparing failure rates where a lesson matched and was recalled against where it matched and was not. Novelty 4.
  Done when: a planted lesson that causes failures in a fixture history is flagged for retirement, and a neutral lesson is not.

- **Pre-arm the undo for steps that match a past harm** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: pack: risk budget steps autonomy down after harm, but nothing stages the specific undo ahead of time. This is the mast-cell idea: primed before the trigger. Prior art: generic checkpoints. Better by: the snapshot is chosen by the harm signature (a migration step gets a DB copy, an edit to a tower file gets a file copy). Novelty 3.
  Done when: a plan step matching a recorded harm signature has a restorable snapshot created before it runs, and the restore is tested.

- **Add `fm incognito`, a session that teaches nothing** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: pack: the open question "which learner was never tested with poisoned input" plus the dropped captures made while debugging. Peripheral tolerance means a transient signal should not become learned self. Prior art: browser incognito, nothing in coding harnesses. Better by: lessons, user model, calibration ledger, trigger precision and captures all skip the session, and the receipt lists what was skipped. Novelty 3.
  Done when: after an incognito session, no learner's state file changes (hash-compared) and the receipt names each learner skipped.

- **Detect periodic-fever detectors** — FIX — value 3 — effort S — risk low — category: noise
  Why: assumption: some nudges fire on session length or the clock, not content (autoinflammatory, not autoimmune). Prior art: none. Better by: one correlation test on the existing firing logs, with no new arms. Novelty 3.
  Done when: a fixture detector that fires every 40th tool call is flagged, and a content-driven one is not.

- **Refine a near-miss by changing only its failing residual** — FEATURE — value 4 — effort L — risk med — category: repair
  Why: Stack Overflow 2025 survey: 66% cite near-miss AI output and 45% say debugging takes longer. This is affinity maturation applied to code. Prior art: agent retry loops that re-plan from scratch. Better by: a bounded loop that mutates only code touching the failed check and keeps the closest-binding variant, using the verify commands already in the task. Novelty 3.
  Done when: on 5 fixture tasks failing 1 of N checks, the loop passes at least as often as a full retry for less cost, and the lineage is printed.

- **Track the allergic march, where one override breeds more** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: assumption: overriding one rule predicts overriding its neighbours soon after, a sign the user has stopped trusting the guard. Prior art: per-rule override counts. Better by: detect the cascade across rules and offer one "re-tune the guard" yes-card instead of many prompts. This answers the 15+ approval-prompt complaint. Novelty 3. (wild)
  Done when: a fixture log with 4 related overrides in 20 minutes yields one card listing them, not four prompts.

- **Convene an orphan-species court for one-off failures** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: memory cells only help on a repeat, so the first repeat is the costly one. Weekly, cluster failures that never repeated by loose features, looking for a species the signature matcher missed. Prior art: none found. Novelty 4. (wild)
  Done when: a fixture of 12 singleton failures, 5 of them one hidden species, yields a cluster naming those 5.

- **Leave last words when a lane aborts itself** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: pack covers apoptosis and cytokine posts but not a death note. Pyroptosis is a cell that dies and alarms its neighbours. A lane in a loop or with contradictory context stops and writes five lines (tried, signature, files touched, suspected cause) for the next lane and the morning note. Novelty 2. (wild)
  Done when: a forced-loop fixture lane stops within N repeats and the successor's first message quotes the note.

- **Show an immune titer per file** — FEATURE — value 3 — effort M — risk low — category: visibility
  Why: pack lists "show a titer" at repo level and "map dark modules". Per-file overlay combines three signals: how many detectors can see it, past incidents, and how recently a rule fired there. Better by: it ranks where the user should spend review. Novelty 2.
  Done when: `fm doctor --json` returns a ranked list of files with those three fields, and a file with no coverage ranks above a covered one.

Next question: which of Foreman's refusals does the user routinely route around by hand, and does the guard learn from the workaround or only from the block?
Next question: what would the user need to see in one line on resume to stop typing "where were we"?
