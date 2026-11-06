# Brainstorm — lens: delight

- **Show the receipt as a one-glance "proof card"** — FEATURE — value 5 — effort M — risk low — category: close-out
  Why: T-0795 (plain receipts, landing ladder) is deferred, and the user keeps asking for proof to be legible ("proven" labels, "unproven can't read as pass"). A card shows what was run, what failed before the fix, and what passed after. Unproven rows get a hatched, grey stamp that can't be mistaken for green.
  Done when: `fm task finish` prints or renders a card where a task with no run record shows the hatched "unproven" stamp, and a snapshot test pins both states.

- **Make the hard hat wink when the guard saves you** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the guard is the product's main promise, but its saves are invisible, since a blocked command just disappears. A small "caught: rm -rf ~ (bypass mode)" line with the logo hat tipping makes the value felt.
  Done when: a blocked command shows a one-line caught note in the terminal and the web UI, and `fm doctor` counts saves for the week.

- **Add a "Friday recap" that tells the week as a story** — FEATURE — value 4 — effort M — risk low — category: digest
  Why: the night digest and the Today charts exist, and bets, calibration and outcomes data are already stored. A 5-line narrative ("you closed 14 tasks, 2 were reversed, your ship bets ran 3 points hot") would be shared more than any chart.
  Done when: `fm recap --week` prints a deterministic narrative built only from ledger numbers, with each sentence linking its task ids.

- **Animate the stage rail so state is felt, not read** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the pane shows a stage rail and the work bar, but it shows progress without telling what is waiting. A pulse on the active stage, a slow-breathing "waiting on usage limit" state and a settle animation when a proof passes would explain state without text. All motion respects reduced-motion.
  Done when: the web UI stage rail has distinct active, waiting, failed and proven animations and a `prefers-reduced-motion` test shows them static.

- **Clickable task ids everywhere** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: T-0796 lists clickable ids and a palette. Every T-2616 in terminal output could be an OSC 8 link that opens the task in the web UI.
  Done when: task ids in `fm next`, `fm task` and the drive log carry OSC 8 links, and disabling them via `NO_COLOR` or non-tty output leaves plain text.

- **Give the first run a 90-second guided win** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: T-0862 and T-0863 (tour, start ladder) are deferred pending evidence, but `fm demo` exists. Assumption: the evidence is thin because first-run polish isn't measured. A planted bug that the user watches Foreman plan, fail, fix and prove would be the share-worthy moment.
  Done when: `fm demo --guided` runs in a temp dir, ends on a closed task with a proof that failed before the fix, and cleans up after itself.

- **Show "what I almost did" on the override** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the pack asks who records that a manual override isn't proof. A small amber "overridden by you at 14:02" badge on that row, kept in later receipts, is honest and a little humbling.
  Done when: an overridden row renders the badge in receipt and web UI, and `fm outcomes` doesn't count it as proven.

- **Play the queue as a train timetable** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the queue is long (30+ open items, many deferred and blocked). A departures-board view, where blocked items show their blocker as a delay reason and deferred ones sit on a "later" platform, makes a long list scannable and pleasant.
  Done when: the web UI has a board view whose rows show status, blocker text and expected next step, with a keyboard shortcut to toggle it.

- **Wild: Let the hard hat have moods from the calibration data** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: wild; the logo is a hard hat with a check mark, and Brier scores and held rates already exist. The hat in the tray and web header looks confident, wary or sheepish depending on the last 20 settled bets. A tiny wink of honesty that people would screenshot.
  Done when: the header icon swaps among three states by a pure function of the calibration numbers, and a test pins the thresholds.

- **Wild: Turn a finished day into a 20-second replay clip** — FEATURE — value 3 — effort L — risk med — category: sharing
  Why: wild; the README already leads with a sped-up SVG demo of a real session. Generate that SVG automatically from any task's recorded tool calls, so the user can post "watch Foreman fix this" without recording anything.
  Done when: `fm task replay T-xxxx --svg` writes an animated SVG from the task's ledger with secrets already redacted, and it matches a golden file.

- **Wild: A "ghost pair" that argues the other side in the pane** — FEATURE — value 3 — effort L — risk med — category: review
  Why: wild; the user already values cold reads by a different model. Showing the cold reader's objection as a small speech bubble beside the stage rail ("Sonnet read this: 'test never failed first'") makes the second opinion feel like a character, not a log line.
  Done when: a failed cold read appears as a quoted bubble tied to its offending line in the web UI, and a pass shows nothing.

- **Quiet the doctor with a "all clear" moment** — FEATURE — value 2 — effort S — risk low — category: polish
  Why: `fm doctor` is the home of many WARNs (timers, canaries, ratchets). When everything is green it should say so with a short, satisfying line and a streak count, instead of a flat list.
  Done when: `fm doctor` with no warnings ends on a one-line summary with the clean-days streak, and a test pins the output.

- **Name a settled bet in the feed as a small celebration** — FEATURE — value 2 — effort S — risk low — category: calibration
  Why: bets settle unattended from the night tick, so the user never sees one land. A feed line when a bet closes ("you said 80%, it held") makes the calibration loop visible without opening a report.
  Done when: each settled bet adds one feed line in the web UI and the next session's start note, with a count capped per day.

Next question: Which moments does the user actually screenshot or paste elsewhere, and does any surface in Foreman today produce them on purpose?
Next question: Of the terminal outputs the user sees every day, which one is longest, and what is the one line they read before skipping the rest?
