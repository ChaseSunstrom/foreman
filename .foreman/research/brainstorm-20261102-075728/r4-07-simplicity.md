# Brainstorm — lens: simplicity

- **Cap each borrowed metaphor at two rounds** — CLEAN — value 4 — effort S — risk low — category: brainstorm hygiene
  Why: the "Ideas so far" list holds hundreds of immune-system variants (thymus, fever, T-regs, antibodies, titer) and near-identical clock/tick variants. They crowd out the goal-planning ideas the request is about.
  Done when: the idea filer tags each idea with its borrowed-domain word, and a third round of ideas sharing one tag is refused with a "metaphor spent" line. A test feeds 3 rounds of "immune" ideas and sees round 3 rejected.

- **Drop pack sections that yielded nothing** — PERFORMANCE — value 4 — effort M — risk low — category: pack budget
  Why: the pack is mostly the 1,000+ line "Ideas so far" list plus 40+ steers. Nothing shows which sections ever produced an accepted idea. Assumption: accepted ideas can be traced to the section that inspired them.
  Done when: after 5 brainstorms, `fm ideas --pack-report` lists each section's accepted-idea count and its token cost. A section with zero yield over 5 rounds is shrunk to a count line in the next pack.

- **Carry at most five open questions between rounds** — CLEAN — value 3 — effort S — risk low — category: brainstorm hygiene
  Why: "Questions earlier brainstorms left" is 8 long questions repeated across rounds, and each is answered in prose by every lens.
  Done when: the pack builder keeps at most 5 questions, ages out any question answered in two rounds, and a test shows the oldest unanswered question evicted.

- **Refuse task titles over 72 characters** — CLEAN — value 3 — effort S — risk low — category: legibility
  Why: recent commit and task lines such as T-2610 and T-2611 run to paragraph length. The user cannot scan them, and they inflate every pack and status view.
  Done when: `fm task new` and `fm capture` reject a title over 72 characters and print the detail-in-body form. The existing open tasks are exempt.

- **Reject a steer over 200 characters at store time** — CLEAN — value 4 — effort S — risk low — category: steers
  Why: the steers are cut off mid-sentence ("…") in the pack, so a child may act on half a rule. Assumption: the full text lives elsewhere and the short form can be derived.
  Done when: `fm decide --check` refuses a steer over 200 characters unless it is given a short form. The verbatim text goes to a side file, and the pack carries only short forms.

- **Add a "shrink" goal kind where done is a measured drop** — FEATURE — value 4 — effort M — risk med — category: goal engine
  Why: the lean-ratchet work shows growth is measured but removal has no goal shape. The deferred "Slim Foreman" bundle (T-0794) and the 1,388 files under `plugin/skills` are unplanned subtraction.
  Done when: `fm goal new --shrink files<=1000` creates rows that are all deletions. The goal reaches done only when the metric passes and the test suite is unchanged. A test closes a shrink goal on a fixture.

- **Stop a brainstorm capability once a round is mostly repeats** — PERFORMANCE — value 4 — effort M — risk med — category: brainstorm hygiene
  Why: rounds keep re-proposing "heartbeat the tick", "replay a week", "null arm" and "dry-run before arming" in new words. Brainstorm spend continues past saturation.
  Done when: if at least 80% of a round's ideas match earlier cluster titles, the round ends with "saturated: N repeats" and no new tasks are filed. A fixture round of paraphrases triggers it.

- **Cut the plan to five rows and make each extra row earn its place** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: goal plans grow by default (the 58-59 cell grids and the thousands of "complete" capability items). Nothing forces a row to justify itself against a minimal plan.
  Done when: the planner first writes a plan of at most 5 rows, and every additional row carries a one-line "without this, the user would notice ___". A row with no such line is dropped from the plan.

- **Wild: run a diet week where only net-negative changes merge** — FEATURE — value 3 — effort S — risk low — category: subtraction
  Why: wild. The lean ratchet only trips on growth that has already shipped. Nothing shows what Foreman does when it cannot grow.
  Done when: `fm diet 7d` makes `fm ship` refuse any diff with more added than deleted lines (excluding tests). At the end it prints which asks went unmet because of it.

- **Wild: build a one-file goal that works with only grep and sed** — FEATURE — value 3 — effort M — risk low — category: goal engine
  Why: wild. The standing rule that Foreman works with no `claude` on PATH points the same way, towards fewer moving parts. The goal file is the only state, and "done" is a shell loop over its backticked commands.
  Done when: a 30-line `sh` script resumes a goal (prints the next unchecked row and runs its check) with no Python. A test shows its verdict matches `fm goal` on 10 fixtures.

- **Wild: delete the feature the user touched least each month** — CLEAN — value 3 — effort S — risk med — category: subtraction
  Why: wild. Over 40 deferred "Later from" bundles and 2,125 mapped files show everything is added and almost nothing is retired. Retirement needs a ritual.
  Done when: on the 1st of each month `fm doctor` proposes one verb or skill with the fewest local calls in 60 days, and a one-word answer deletes it or exempts it for 90 days.

- **Make the finish card list only what the user can now do** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: close-out text is currently a mix of gauges and receipts (T-0795 is deferred). A user checking "is it done" wants capability lines.
  Done when: closing a goal prints at most 5 "you can now…" lines, each tied to a closed row. Any gauge text goes behind `--detail`, and a snapshot test pins the 5-line limit.

Next question: Which five Foreman outputs would the user not miss if they vanished tomorrow, and what evidence besides "nobody complained" shows it?
Next question: Does a goal planned under a five-row cap finish with fewer reopens than one planned without, and where is that measured?
