# Brainstorm — lens: judgment, taste and decisions

- **Rank decisions by reversibility-weighted stakes before choosing how to decide** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: the pack lists one-way/two-way doors, doubt budgets and "price each decision by cost of being wrong" separately, but nothing joins them into one router. Assumption: a single scorer (reversibility, blast radius, user-visible, cost to undo) is cheaper than separate passes.
  Done when: `fm task decide` records a stakes score and the deliberation depth it chose (default, self-check, second opinion or ask), and a test shows a rename gets default while a schema migration gets a second opinion.

- **Keep a precedent file of the user's past rulings, cited at decision time** — FEATURE — value 5 — effort M — risk med — category: taste
  Why: the user's steers ("cleanup never got done", "limits shouldn't block until 75%", "YAGNI") are rulings, but they live as scattered vetoes and lessons. Case law with the situation, the ruling and the stated reason lets new calls be analogised instead of re-asked. Assumption: steers can be extracted with enough context to match later.
  Done when: planning a task whose situation matches a stored ruling prints that ruling with its date and reason, and the brief's approach line references it.

- **Distinguish a standing preference from a one-off in every steer** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: "feel free to continue with those" and "75%" read as policy, while "build it in Tauri" is project-specific. Without scope, lessons over-generalise or get lost. Assumption: one clarifying line at capture time is acceptable.
  Done when: a steer is stored with a scope (task, project, global) and an expiry, and a test shows a task-scoped steer does not appear in another project's context.

- **Write a "decision memo" that fits on one screen for every ask** — FEATURE — value 4 — effort S — risk low — category: asks
  Why: the user is interrupted with questions, and answering identically is a recorded pattern (the "when to stop asking" idea). Assumption: a fixed template (recommendation, the one deciding fact, cost of the wrong choice, the default if ignored) cuts reply time.
  Done when: every `fm ask` renders that template, and an ask missing a recommendation or default is refused.

- **Score taste calls separately from correctness in reviews** — FEATURE — value 3 — effort M — risk low — category: review
  Why: the audit lenses cover defects, but "this works yet the user will dislike it" (over-building, wrong naming, extra surface) has no lens. Dropped YAGNI items hint at this. Assumption: the user's drops and steers are enough signal for a taste lens.
  Done when: the reviewer has a "taste" lens that cites a prior user drop or steer for each finding, and findings without a citation are discarded.

- **Detect when Foreman is deciding by default and flag the choice as a choice** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: unconsidered defaults (tier, test style, file placement) are the main source of "never got done" and silent drift. Assumption: defaults can be enumerated from the plan and commit diff.
  Done when: `fm task done` lists the choices that were made without an alternative considered, and the list is non-empty on a seeded fixture.

- **Reopen a decision when the evidence behind it changes, with a one-line diff** — FEATURE — value 4 — effort M — risk med — category: decisions
  Why: decisions have revisit triggers, but nothing watches the premises. Assumption: each decision can name one checkable premise (a command or file fact).
  Done when: changing a stored premise makes the sentinel print the decision and what changed, and the decision shows as reopened.

- **Run a "would the user have chosen this" back-test on past decisions** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: the taste-model ideas have no way to measure accuracy. Replaying the last N asks through the precedent file and comparing with the real answers gives a hit rate that gates how much it may pre-answer. Assumption: the history of at least 30 asks exists.
  Done when: `fm taste check` prints a hit rate with a confusion list, and pre-answering is disabled below a configured threshold.

- **Wild: Keep a "reasons ledger" where the user can strike a reason and watch decisions fall** — FEATURE — value 3 — effort L — risk med — category: decisions
  Why: wild. Decisions record why, so striking a reason ("I no longer care about X") can reopen every decision built on it. Assumption: reasons can be normalised to shared tags.
  Done when: striking a reason tag lists the dependent decisions and reopens them as tasks.

- **Wild: Offer a "swap chairs" replay that shows a decision as the user would have made it** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: wild. After a close-out, one view renders the chosen approach beside what the precedent file predicts the user would have picked, making taste drift visible. Assumption: the precedent file is dense enough.
  Done when: the view shows both choices for a finished task, with the matching precedent cited, and flags disagreements.

- **Wild: Grow a "regret tab" where the user taps one button on any shipped choice** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: wild. Outcome labels now come from inferring the next message; an explicit one-tap "I would not have done it this way" on a decision feeds precedent, lessons and the taste back-test cheaply. Assumption: the web UI and pane can host it without noise.
  Done when: tapping it on a decision in the UI writes a regret event linked to that decision, and it shows in `fm friction`.

- **Require the loser's best argument in each plan's chosen-approach line** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: the pack has "kill reasons" and a devil's advocate, but nothing makes the strongest case for the rejected option travel with the decision so a later reader can re-judge it. Assumption: one sentence is enough.
  Done when: M/L briefs fail the plan gate unless each rejected option carries a "best case for it" line distinct from its kill reason.

- **Judge by the user's acceptance glance: predict the first thing they will look at** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: users read close-outs quickly; the first thing they check is usually what they last complained about (cleanup, limits, blocking). Assumption: the last N steers give a usable "watch list".
  Done when: the close-out opens with evidence for the top three watch-list items, and a test shows a cleanup steer puts cleanup evidence first.
