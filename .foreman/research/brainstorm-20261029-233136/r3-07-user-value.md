# Brainstorm — lens: user value

- **Open every Genesis run with a one-line deal the user can say yes to** — FEATURE — value 5 — effort S — risk low — category: consent
  Why: the user's steers (standing grants, "genuinely smarter") show they delegate broadly but want to know what they delegated. Existing ideas cover budget and draft previews separately; this fuses them into a single sentence: "I'll spend ≤$X over ≤N hours on <goal>, touching <surfaces>; say 'go', or edit one word."
  Done when: `fm genesis run` prints a deal line containing budget, wall-clock, surfaces and goal, and refuses to start without a recorded yes or a standing grant naming Genesis.

- **Answer "what did Genesis do while I was away" in five lines** — FEATURE — value 5 — effort S — risk low — category: digest
  Why: the user's last five asks are all about Genesis visibility (site page, live publish, in-depth per-generation view). The next need is a returning-user summary: closed scenarios, spend, shipped commits, what needs me.
  Done when: a session start after a tower change shows ≤5 lines with scenarios closed, dollars, commits shipped and a "needs you" count, drawn from tower files.

- **Turn the user's past steers into Genesis's first MUSTs and NEVERs, shown with the quote** — FEATURE — value 5 — effort M — risk med — category: gen-0 writer
  Why: steered items ("not hardcoded", "tower files live only in genesis storage", "no idea killed for ambition") are already durable preferences. The cold gen-0 should inherit them with the original quote attached so the user can strike one.
  Done when: on a fixture with 5 recorded steers, the self-written gen-0 lists each as a MUST/NEVER with its verbatim source, and striking one removes it from later generations.

- **Ship a "stale surface" bundle as Genesis's first deliverable** — FEATURE — value 4 — effort M — risk low — category: user outcomes
  Why: the user repeatedly files stale-site/stale-demo/stale-favicon FIXes after the code moves (fm code section, favicon, shader cards). Genesis's most felt win is catching these unasked, before any exam theory.
  Done when: on a fixture where code changed and site/docs lag, a Genesis run queues and closes one task per stale surface with a before/after.

- **Let the user rate a finished generation with one keystroke and learn from it** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: assumption: user opinion is the only ground truth the exam can't fake. A 👍/👎 on each generation's summary, stored in lineage, weights future selection and mission choice.
  Done when: `fm genesis rate gen-2 down` writes to lineage.md and the next Seed cites the rating.

- **Offer "make this great" as a ranked menu of three outcomes, not a tower** — FEATURE — value 4 — effort M — risk low — category: scoping
  Why: a sweeping line from the user is ambiguous; the tower is heavy. Show three concrete finish lines (e.g. "close 6 gaps in ~$4", "full spec + exam ~$15") with the expected visible change; the pick sets the depth.
  Done when: running with one line and no history prints three priced options, and choosing one sets the budget and mission count.

- **Show only the diff the user will feel in the final report** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: dropped items show the user rejects noise (repeat nudges, generic notes). A report that lists user-visible changes (commands, pages, behaviors) and hides internal churn matches that taste.
  Done when: the tower receipt lists changes classified user-visible vs internal, and defaults to showing only user-visible.

- **Detect that a project is "done enough" and say so** — FEATURE — value 4 — effort M — risk med — category: stopping
  Why: queue-dry auto-start could keep inventing work. A user-facing "this project is at best-in-class for its kind on 23/24 cells; the last one needs your decision" is more valuable than another generation.
  Done when: when the grid has no closable cells, Genesis stops, prints the remainder as user decisions, and does not auto-start again until something changes.

- **Pre-answer the questions Genesis would ask, from the user's history** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: blocked items pile up (T-0325, T-0335, T-0352, T-0418 need the user). Batch them and propose a default answer for each drawn from past decisions.
  Done when: Genesis produces one card with every user-blocked item and a proposed answer; accepting applies them all.

- **Wild: Genesis writes the README's "what's new this week" from the tower** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: the user polishes site and README constantly; the tower already knows what changed and why. assumption: they'd rather approve a draft than write it.
  Done when: a generated changelog section appears in a draft PR/commit citing tower generations.

- **Wild: A "second opinion" mode that runs the tower on the user's competitor** — FEATURE — value 3 — effort L — risk med — category: strategy — wild
  Why: capability-map thinking ("best-in-class for this kind of project") naturally invites comparing against a named rival repo; assumption: read-only, local.
  Done when: given a rival repo path, Genesis outputs a table of capabilities it has that this project lacks, with no writes to the rival.

- **Wild: Voice of the user — a pinned persona rebuilt from their steers that vetoes ideas** — FEATURE — value 3 — effort M — risk med — category: taste — wild
  Why: the user's drops show consistent taste (reject repeat noise, reject unreproducible baselines). A persona prompt built from steers/drops could pre-filter missions before they cost anything.
  Done when: on 10 past ideas, the persona's veto agrees with the user's recorded keep/drop on ≥8.

Next question: What does the user do in the first 60 seconds after Genesis finishes a generation — what do they look at, and what would make them stop trusting it?
Next question: Which of the user's recurring FIX asks (stale site, stale demo) were caused by a code change Genesis itself made, and can Genesis refuse to finish until it has updated those surfaces?
