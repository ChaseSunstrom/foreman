# Brainstorm — lens: unspoken needs

Answering the earlier question my lens can: the 59 empty cells are mostly cells for triggers nobody has ever seen fire. The need behind them is trust in work the user didn't start. They need to see it, stop it and tell it apart from their own work.

- **Add a dead-man heartbeat to the timer** — FEATURE — value 5 — effort S — risk low — category: reliability
  Why: the night tick "logs only when something happens", so a dead timer and a quiet night look identical. A user who installed timers can't tell them apart.
  Done when: with the timer unit stopped in a test, `fm doctor` reports "tick stale N h"; with it running and idle it reports "alive, nothing to do".

- **Explain why a trigger did not fire** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: `fm triggers` groups captures by precision, but only for runs that happened. Assumption: users distrust automation more over silence than over noise.
  Done when: `fm triggers why-not <name>` prints the last evaluation time, the event seen, and the rule or guard that declined it.

- **Stamp every self-started artifact with its origin** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: the drive already separates Foreman-filed items (ci, self, discovered). Tasks, branches and commits don't carry "started by ci-watch run 123", so the user can't separate their work from the machine's.
  Done when: a task, branch and commit made from a trigger each carry the trigger id and event, and `fm status` filters on it.

- **Fire a trigger on a fake event for a drill** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the 59 cells have no way to be proven live short of waiting for a real CI failure. Assumption: users want to see a trigger do its thing once before trusting it.
  Done when: `fm triggers fire <name> --fake` runs the full path in a scratch worktree, prints what it would have changed, and leaves the real tree untouched.

- **Defer triggers while the user is working in the repo** — FIX — value 4 — effort M — risk med — category: safety
  Why: assumption: a lane starting under a dirty tree or an open session is the quickest way to lose trust. Foreman already knows session locks and tree state.
  Done when: with a dirty tree or a live session lock, a due trigger logs "deferred: user active" and runs after the tree is clean, in a test.

- **Run missed schedules once on wake, not N times** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: a laptop that slept through three nights should catch up once. Timers installed through the one-yes queue need that policy written down.
  Done when: simulating three missed ticks yields one catch-up run, and the unit text carries the catch-up setting.

- **Show the exact unit text, the enable command and the uninstall line on the install card** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: installs are "queued for one yes", but a yes to a name isn't informed. Assumption: the user wants to read what runs at 3am before consenting.
  Done when: the card embeds the unit file body plus its removal command, and `fm eject` removes exactly those units.

- **Declare triggers in a committed repo file** — FEATURE — value 3 — effort M — risk med — category: configuration
  Why: assumption: triggers kept only in machine state vanish on a new box and can't be reviewed. A repo file survives a fresh install and is reviewed like code. The activation still goes through the one yes.
  Done when: a triggers file in the repo is parsed, listed by `fm triggers`, and nothing installs until the yes is given.

- **Watch other repos' default branches and review requests** — FEATURE — value 3 — effort M — risk med — category: watchers
  Why: `fm ci-watch` only settles ship bets and `--last-ship`. Assumption: the user's other repos and PRs awaiting them also go red unseen.
  Done when: `fm ci-watch --repo owner/name` opens one deduplicated task per new red run on that branch.

- **Compile "whenever X, do Y" typed in chat into a trigger draft** — FEATURE — value 4 — effort M — risk med — category: authoring (wild)
  Why: wild. The user states these rules in conversation (their steers) and never writes trigger config. The rule is parsed into a draft, shown as a diff, then queued for a yes.
  Done when: the sentence "after CI fails on main, draft a fix lane" yields a valid trigger draft with an event, an action and a budget, unactivated.

- **Turn a drop folder into an inbox** — FEATURE — value 3 — effort M — risk med — category: surfaces (wild)
  Why: wild. A file dropped in `~/fm-inbox` (a log, a PDF, a screenshot of an error) becomes a captured task through a file trigger, with content fenced as untrusted data.
  Done when: dropping a text file creates one task quoting it verbatim, and a second drop of the same bytes is deduplicated.

- **Offer a trigger after a failure streak in the user's terminal** — FEATURE — value 3 — effort L — risk high — category: habits (wild)
  Why: wild. A shell hook sees the same command fail three times and offers a watcher or a task. It is opt-in and local, and the user never has to say what they want automated.
  Done when: three failures of one command produce one suggestion line with a one-word accept, and nothing is recorded without opt-in.

Next question: Which of the 59 cells would a user ever see fire, and what is the first evidence a self-started run gives them that it was theirs to stop?
Next question: What does a trigger do when two of them want the same repo, the same budget or the same yes at once, and who arbitrates?
