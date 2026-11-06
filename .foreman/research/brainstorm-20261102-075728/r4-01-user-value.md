# Brainstorm — lens: user value

Most of the obvious ground is already in the "ideas so far" list, so these are second-order. Each one prices, grades or checks something the list only counts or announces. All of them are assumptions unless I name evidence.

**Earlier question my lens can answer:** which jobs need to run on time? The ones the user reads before they type: the morning note and the finish-date band. Settled bets can arrive eventually. (assumption: based on the standing steers, none of which mention bet settling.)

- **Price every mid-goal change before accepting it** — FEATURE — value 4 — effort M — risk low — category: scope
  Why: the pack has a scope-growth ledger and slack reserves, but nothing quotes the cost of one change. The user's steers show repeated re-scoping (T-2341, T-2583). Assumption: they'd rather see "+1.5 days, +$6, pushes the band to Thu" than a bare yes/no.
  Done when: a new ask or a revised answer mid-goal prints days, dollars and the new finish band, and accepting it records those numbers on the goal.

- **Grade the user's overrides by outcome** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: vetoes are persisted, but nothing records whether the user turned out right. The steers show the user correcting Foreman's own criteria. Assumption: "you were right on 7 of 9 cuts" lets Foreman defer more on the kinds of call they win.
  Done when: after 30 days an override has a verdict (user right, Foreman right, unclear), and `fm doctor` shows the per-class tally.

- **Split "done" into done-here and proven-elsewhere** — FEATURE — value 4 — effort S — risk low — category: honest finish
  Why: T-0335, T-0336 and T-0337 are blocked on real codex, gemini and opencode. A goal touching them can only be partly proven on this machine. Assumption: the user would rather see "done here; unproven on gemini, needs the CLI installed" than a plain done.
  Done when: a goal row with an unproven venue closes as "done here", the finish card names the missing venue, and the goal isn't called finished while any must-row is unproven.

- **Show the ship forecast on the finish card** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: T-2611 prints the ship chance, and the user's push grant is spent per task. A finished goal already knows its diff and the tests it touched. Assumption: the user wants to know "will this ship cleanly?" at the moment of finishing.
  Done when: a goal finish prints the ship chance, the gates most likely to trip, and whether a publish grant is set.

- **Add a publish-readiness row pack** — FEATURE — value 3 — effort M — risk low — category: release
  Why: T-0352 (publish Foreman Desktop with CI and release pipelines) is blocked. Licence audits and artifact checks exist in the list, but community files do not. Assumption: public goals need SECURITY.md, issue templates, a dry-run release and an install test from the tagged artifact.
  Done when: a goal whose text says "publish" gets those rows automatically, each with a probe, and none appear for private goals.

- **Check names and namespaces before naming anything public** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: a goal that mints a package, binary or repo name can burn a day on a rename. Foreman can check npm, PyPI, crates, GitHub and the domain without installing anything.
  Done when: a goal that names a new public artifact lists name availability across those registries before the first build row, and a taken name is flagged.

- **Count rows proven by checks the user wrote or ran** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the steers say weakness-finding must use signals Foreman didn't author. Assumption: the user trusts "11 of 14 rows proven by something you ran" more than a green bar.
  Done when: the finish card shows the share of rows whose evidence came from a user-authored or user-run command, and that share is stored per goal.

- **Quote the user's first complaint class at plan time** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: the user keeps filing gauge-honesty and false-done asks (T-2583, T-2606, T-2566). Assumption: for each plan, the three complaints most likely from their history should be answered inside the plan.
  Done when: a plan carries a "you'd probably object to…" block with 3 items, each tied to a past correction, and each is answered or dismissed.

- **Draft a build-log post from the ledger (wild)** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: assumption: a finished goal already holds the story (decisions, dead ends, numbers). A local, unpublished draft for the user to edit would be a keepsake.
  Done when: finishing a goal writes a markdown draft whose every number links to a ledger row, and nothing is sent anywhere.

- **Show a wage meter (wild)** — FEATURE — value 2 — effort S — risk low — category: value
  Why: assumption: the user will judge Foreman by "cost $14, saved about 6 hours by my own guess". They enter the hours once at finish, and Foreman keeps a running dollars-per-hour-saved figure.
  Done when: the finish card asks one question for the hours, and `fm doctor` shows the median across goals with the count.

- **Run a "regret rehearsal" before the last row (wild)** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the user pushes back on false dones. Assumption: before closing, a cold child is told "the user will reject this tomorrow" and must name the likeliest reason from the user's own past rejections. Foreman then fixes it, or lists it as a known gap on the card.
  Done when: each finish card has a "likeliest rejection" line with the fix or the named gap, and over 30 days the match rate with real reopens is shown.

- **Rank blocked work by days the user's single action would free (wild)** — FEATURE — value 3 — effort S — risk low — category: unblocking
  Why: T-0325 needs `sudo pacman -S libappindicator-gtk3`, and several other items are blocked on live CLIs. Assumption: "this one command frees 3 days of rows" gets done, while a flat list gets ignored.
  Done when: the blocked list shows each unblock's freed row-count and days, ordered by that, and updates when one closes.

Next question: which finish card line has the user actually read, and which is dead text they scroll past?
Next question: for each past reopen or "done" the user disputed, what could Foreman have seen or priced at finish that it didn't?
