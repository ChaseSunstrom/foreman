# Brainstorm — lens: delight

- **Flag what's missing, not what's foreign (missing-self)** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: assumption: every guard rule and learner looks for bad things, but a task commit with no task trailer, a FIX with no red-first test, or a lane report with no probe is invisible to all of them. NK cells kill exactly the cells that lack the self marker.
  Done when: a fixture commit missing its task trailer gets a one-line friendly flag, and the same commit with the trailer gets none.
  Prior art: none found (linters check for presence of bad patterns; commit-msg hooks are the nearest thing).
  Better by: the marker list comes from what the user's own accepted work always carries, not from a config.
  Novelty: 4

- **Itch before pain: `fm scratch`** — FEATURE — value 4 — effort M — risk low — category: foresight
  Why: assumption: files near past harm get no sign until they fail again. An itch is a faint status-line count ("3 itches") for files with old scars and fresh edits. `fm scratch` runs the cheapest check that relieves each one and the itch clears.
  Done when: editing a file touched by a past FIX adds one itch, and `fm scratch` clears it only if the named check passes.
  Prior art: none found (coverage-hotspot tools exist but don't act).
  Better by: it is a felt, cheap, user-initiated action, not a warning wall.
  Novelty: 4

- **Re-awaken a muted nudge when its warning comes true (checkpoint release)** — FEATURE — value 4 — effort S — risk low — category: noise control
  Why: the pack's "mute a signature after two dismissals" has no way back. T-cell exhaustion has a release: when the thing a muted nudge warned about actually happens, it returns once, saying "I warned about this on <date>".
  Done when: a muted signature whose predicted failure occurs fires one reinstated note and the mute is lifted for 14 days.
  Prior art: none found (alert-fatigue mutes are one-way).
  Better by: the mute becomes a hypothesis the next failure can overturn.
  Novelty: 4

- **Tissue-type every graft before merge** — FEATURE — value 4 — effort M — risk med — category: review
  Why: assumption: lane patches, imported stack cards and lessons from another repo are foreign tissue. Compute a match score on naming, error handling, test style and import habits versus the host repo, and show "match 91%, mismatches: 2".
  Done when: a patch written in a deliberately foreign style scores lower than one in repo style, and the mismatching traits are named.
  Prior art: style linters and Aider's repo map, which don't score a patch against its host.
  Better by: it gates grafts on the repo's own conventions, mined from neighbouring files, with no config.
  Novelty: 4

- **Draw idle lanes toward damage (chemotaxis)** — FEATURE — value 3 — effort M — risk med — category: scheduling
  Why: assumption: night lanes pick work from a queue. A damage gradient from reopens, CI red, flaky reruns and itches would pull spare lanes toward the hottest module first.
  Done when: with two fixtures differing only in recent reopens, the night tick assigns the first lane to the one with more reopens.
  Prior art: none found (queues order by priority, not by local damage density).
  Better by: it uses signals Foreman already records, and it needs no user ranking.
  Novelty: 3

- **Name sanctuary zones (immune privilege)** — FEATURE — value 3 — effort S — risk low — category: calm
  Why: assumption: scratch dirs, spikes and generated code draw the same nudges as the core. The user names zones where Foreman stays quiet, and the status line dims there.
  Done when: an edit inside a sanctuary produces zero notes and the guard's destructive-verb rules still fire.
  Prior art: ignore files (.gitignore-style), which skip scanning but not nudges.
  Better by: quiet is explicit and reversible, and it never touches the hard guard.
  Novelty: 3

- **Stamp lessons with a class switch (IgM to IgG)** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: lessons are recalled per file, but none shows how proven it is. A lesson starts as a loose note, switches class after prevented repeats, and ends as a fixed rule, with a one-line stamp "seen 3×, blocked 2×".
  Done when: a lesson that blocks two repeats is shown with the stamp and is offered for compile-to-rule.
  Prior art: none found.
  Better by: the user watches a note earn its place.
  Novelty: 3

- **Say "immunity confirmed" on the first repeat prevented** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the guard's saves aren't tied to the incident that created the rule. The first time a rule built from an incident stops a recurrence, print one line quoting the original incident's date and task.
  Done when: a fixture rule created from T-X blocks a repeat and the message names T-X exactly once, never again for that rule.
  Prior art: none found.
  Better by: it closes the loop between pain and protection in one line.
  Novelty: 3

- **Wild: take nightly biopsies** — FEATURE — value 4 — effort M — risk low — category: assurance
  Why: wild. Every night a patrol samples three random things from the day (a command, a diff hunk, a skipped test) and hands them to a cold reader. The morning shows "biopsy results", mostly boring, occasionally damning.
  Done when: the nightly digest lists three sampled items with a verdict each, and a planted bad item gets caught within a week of nights.
  Prior art: none found (random audit sampling exists in QA, not in harnesses).
  Better by: random sampling catches the failures no detector was written for.
  Novelty: 4

- **Wild: consolidate memory in sleep** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: wild. The night tick replays the day's incidents; only those that recur in replay become lessons, and the morning card lists "what I kept: 3, what I let go: 9".
  Done when: a one-off oddity is not kept and a twice-seen incident is kept, shown in the morning list.
  Prior art: none found (memory features append; none forget on purpose).
  Better by: it keeps memory small and every kept item earned.
  Novelty: 4

- **Wild: let a patrol cell wander the status line** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: wild. A one-glyph cell whose pose shows state: strolling when calm, huddled during a fever, asleep when idle, with a spark on a catch. Reduced-motion users get a static word.
  Done when: the glyph changes between three states for three fixture situations, and a static word shows under reduced motion.
  Prior art: none found; the hard hat is the nearest.
  Better by: state at a glance, with no text spend.
  Novelty: 3

- **Wild: flag lookalikes of past failures (cross-reactivity)** — FEATURE — value 3 — effort M — risk med — category: recall
  Why: wild. A plan gets "this resembles T-1234: both change parsing without fixtures". A "not alike" tap trains it, because false cross-reactivity is the disease.
  Done when: a plan matching a past failure's traits shows the lookalike card, and a "not alike" tap suppresses that pair.
  Prior art: error-signature recall in some trackers, but it matches only identical failures.
  Better by: it matches on traits and learns from the rejections.
  Novelty: 3

Next question: which of these flags can the user turn off with one word, and has any of them ever been checked against what the user actually did next?
Next question: what would an immune-style layer do to Foreman's own idle cost, and who would notice if it cost more than it saved?
