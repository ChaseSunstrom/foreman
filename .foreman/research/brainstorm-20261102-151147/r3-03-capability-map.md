# Brainstorm — lens: capability map

Most of the capability space here is already on the list, so these 12 sit at its edges. Where an item is close to an existing one, the Why line says what differs.

- **Add a debugging hypothesis ledger (`fm hypo`)** — FEATURE — value 4 — effort M — risk low — category: thinking
  Why: The list has bisect, last-green delta and a lone sceptic. It has no stored hypothesis tree for a bug, with each cause, the evidence for and against, and which hypotheses are tested or untried. Cline, Devin and Aider have none either, so this is a place to lead.
  Done when: A fixture bug with three planted wrong causes ends with `fm hypo` showing all three refuted with a cited command and one confirmed. Closing the task refuses while any hypothesis is untested without a reason.

- **Load repo-local lens files** — FEATURE — value 4 — effort S — risk low — category: brainstorm
  Why: Lenses are fixed in the system prompt, and T-0829 only scales them by `lens_rates`. Assumption: a project owner wants a lens such as "our compliance auditor" or "the on-call engineer".
  Done when: A `.foreman/lenses/oncall.md` makes `fm ideas` spawn one more child using that text. Its results appear in `lens_rates`, and removing the file removes the child.

- **Run a time-boxed or constrained brainstorm** — FEATURE — value 3 — effort S — risk low — category: brainstorm
  Why: Slates are ranked by effort S/M/L, but the user can't ask for ideas that fit one evening, under $5, or with no new files. Assumption: constraints sharpen output more than a longer list does.
  Done when: `fm ideas --fits "one evening, no new verbs"` returns only ideas the grader rates as satisfying that constraint, and it prints the rejected count.

- **Normalise value scores across lenses** — CLEAN — value 3 — effort S — risk low — category: ranking
  Why: Each child scores value 1–5 on its own scale, so a lens that inflates ends up on top. Pairwise tournaments exist for plan rows only, not for merged slates. Assumption: score inflation varies by lens.
  Done when: Merged slates rank by per-lens z-score blended with a pairwise judge. A planted lens that scores everything 5 no longer fills the top three.

- **Brainstorm omissions on a diff at finish** — FEATURE — value 4 — effort M — risk low — category: review
  Why: Recent asks arrived as follow-ups: the clock injection that should have come with the windowed readers, and the boundary tests (T-2656–T-2659 era). A tool-less child given only the ask and the diff would list what's missing (error paths, config, docs, rollback, boundaries). This is not the same as an enumeration-parity check, because it generates omissions rather than comparing two lists.
  Done when: On a replayed past diff that was later followed by a fix-up ask, the omission list names that fix-up. The finish receipt prints at most 5 omissions, each as a one-line question.

- **Draw the unlock graph between slate ideas** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: The 900+ ideas so far are flat. Ideas like "one clock" or "one egress ledger" enable others, and flat ranking hides that. The list has dependency ordering for plan rows and ranking for blocked tasks, but not for ideas. Assumption: enabler ideas are under-ranked.
  Done when: `fm ideas --graph` prints enables/conflicts edges for an accepted slate. An idea that unlocks 3 or more others is ranked above its standalone score.

- **Treat unanswered slate lines as soft drops** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: Drops are recorded only when the user says them, and the user's dropped lines show how much they had to re-ground by hand. Silence for N days on a line is a weaker signal that no ledger currently reads. Assumption: most unaccepted ideas are never explicitly dropped.
  Done when: After 14 days, an untouched slate line is booked as `soft_drop` and counted in intake precision, with a flag separating it from explicit drops.

- **Pin one omission-and-counterexample per accepted idea as an exam item** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: Kill probes are pre-registered, but the smallest scenario where an idea makes things worse is not kept as a durable negative exam item. Assumption: harm cases get re-run more often than arguments do.
  Done when: Accepting an idea writes a `harm-scenario` exam entry. It fails if the shipped feature violates it, as proven by a planted violation.

- **Deal Oblique-Strategies provocation cards to lenses (wild)** — FEATURE — value 2 — effort S — risk low — category: brainstorm
  Why: Wild. Provocations such as "remove the most important part" or "do it backwards" are drawn at random per child. Hit rate is tracked per card, so weak cards get retired and strong ones are reused.
  Done when: Each idea records its card. After 5 rounds `fm ideas --cards` ranks cards by accepted-idea yield.

- **Write the README for one year ahead and diff it (wild)** — FEATURE — value 3 — effort S — risk low — category: foresight
  Why: Wild. A child sees only the open and deferred task titles and writes the README Foreman would have if all of them shipped. The gap against today's README shows what the open work still fails to describe.
  Done when: The command outputs a section-level diff of at least 3 undescribed capabilities. It is shown alongside the slate and never filed as tasks automatically.

- **Run an idea séance with the ledger's last dissent (wild)** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: Wild. It shows one dropped idea per week, its drop reason and the evidence that has changed since, and asks "still dead?". It is not a task wake-up. It is a ten-second human prompt.
  Done when: `fm ideas --seance` picks a dropped idea whose cited files changed since the drop. A yes or no is recorded. If the user answers "revive", the idea is refiled with a link to the original.

- **Mirror the slate to a shared offline file for other agents** — FEATURE — value 2 — effort S — risk low — category: interop
  Why: Other harnesses can't read Foreman's catalogue before they brainstorm, so they re-propose built ideas. An `IDEAS.md` index, written only from titles and statuses, lets a plain agent check it by `grep`. This builds on the "already built" checks without needing Foreman installed. Assumption: users run more than one agent.
  Done when: A fixture agent with no Foreman, given `IDEAS.md`, avoids re-proposing 3 of 3 planted built ideas that it otherwise repeats.

Next question: Which of the 900+ listed ideas has the user actually opened in the last 30 days, and does that set differ from the ideas the grounding step scored highest?
Next question: When two lenses independently propose the same idea, does the user accept it more often, and should that count as evidence in the ranking?
