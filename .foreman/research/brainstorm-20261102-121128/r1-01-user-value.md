# Brainstorm — lens: user value

- **List what blocks only the user, with one action each** — FEATURE — value 4 — effort S — risk low — category: unblock
  Why: T-0325, T-0335, T-0352 and T-0418 sit "blocked" and need a package, a grant or an install step. T-0418 is a single foreman-ui update. The user said never to block on questions, so these have likely gone unseen.
  Done when: `fm next --blocked` prints each user-blocked task with the exact command or decision that clears it, and the list is empty after T-0418 is cleared.

- **Mark a check that couldn't run as UNPROVEN, never as pass** — FIX — value 5 — effort S — risk low — category: proof honesty
  Why: an earlier question asks how a receipt says "unproven" when there's no display or browser. Assumption: receipts today collapse "skipped" into a quiet pass.
  Done when: a task finished in headless CI with a UI criterion gets a receipt line `UNPROVEN (no display)`, and `fm outcomes` counts it apart from proven.

- **Record hand overrides as overrides, not proof** — FEATURE — value 4 — effort S — risk low — category: proof honesty
  Why: an earlier question asks who records that an override isn't proof. The user's rule is to trust only signals Foreman didn't author, and a hand override is exactly that gap.
  Done when: closing a task over an unproven row requires `--override "reason"`. The receipt shows "overridden by user", and the held-rate excludes it from proven.

- **Audit "proven" labels that were later reversed** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: an earlier question asks which proven labels were reversed. Outcome survival already exists, and the user wants weakness-finding from signals Foreman didn't author.
  Done when: `fm outcomes --reversed` lists closed tasks later reopened or reverted, with the share that had no run record, and `fm doctor` shows that rate.

- **Publish an honest duel scorecard, losses included** — FEATURE — value 5 — effort L — risk med — category: credibility
  Why: T-0866, T-0867 and T-1231 are deferred. The user's steers require proof before presentation, and a newcomer can't tell if Foreman beats plain Claude.
  Done when: the site shows held-out foreman vs plain pass, cost and time per scenario kind. Every claim links to an exam line, and a kind where plain wins is shown.

- **Drill a host wipe: restore Foreman state on a scratch directory** — FEATURE — value 4 — effort M — risk low — category: resilience
  Why: an earlier question asks what must be rebuilt by hand. The ledgers, bets, timers and steers are all local state. Assumption: no restore test exists.
  Done when: `fm restore --drill` rebuilds a scratch home from the backup. It reports which ledgers, timers and steers came back and which did not.

- **Let each ledger reader declare the record classes it needs** — FIX — value 4 — effort M — risk med — category: ledger integrity
  Why: an earlier question asks which reader would give a wrong answer, not an error, if a record class went missing. Calibration reads were just fixed for exactly this kind of silent skew (T-2610).
  Done when: a test drops each record class in turn. Every reader either errors or prints "N records missing", and none returns a clean number.

- **Add an outside tripwire for ops gauges Foreman wrote itself** — SECURITY — value 3 — effort M — risk low — category: ops trust
  Why: an earlier question names timer liveness, bet settlement and canary state. T-2542 checks systemd, but bet settlement has no outside check.
  Done when: `fm doctor` compares each gauge to an independent source, such as systemd, git or file mtimes. A planted false gauge turns it red.

- **Log the commands the user types to check verdicts via an opt-in `fm run` wrapper** — FEATURE — value 3 — effort S — risk low — category: user model
  Why: an earlier question asks what the user types by hand to check Foreman's verdicts, without reading shell history. Those checks show which verdicts the user doesn't trust.
  Done when: `fm run -- <cmd>` runs the command and records it against the open task. `fm doctor` lists the most re-checked verdict kinds.

- **Ship a trial mode with an eject command (wild)** — FEATURE — value 4 — effort M — risk med — category: adoption
  Why: T-0794 (Lite mode, eject) and T-0862 (newcomer tour) are deferred. Assumption: a newcomer fears lock-in and stays out.
  Done when: `fm eject` removes hooks, timers and the plugin from a repo and leaves its tasks as plain markdown. A fresh clone of a test repo is byte-identical afterward, apart from the kept task files.

- **Replay a past commit overnight, Foreman vs plain, on the user's own repo (wild)** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: the long-horizon tier already replays real repos. Pointing it at the user's repo turns the exam into a personal answer to "is it worth it for me?". It runs at the end of the run, per the user's pause rule.
  Done when: `fm duel --mine` picks a past commit and runs both arms unattended. The morning digest shows pass, cost and time for each.

- **Approve `fm ask` prompts from a phone push (wild)** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: assumption: `fm ask` waits at the terminal. The user wants the work to keep going and wants only the rare question that needs them.
  Done when: a pending `fm ask` sends a push with approve and deny links. Tapping one resolves the ask, and the session continues without a terminal.

- **Show a sealed-prediction hit rate (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: each generation writes a sealed prediction of the user's next three steers. Nothing shows how often it was right, so the user can't judge whether the user model is worth its tokens.
  Done when: `fm genesis predictions` lists each predicted steer against the next real ones, and the hit rate appears in the report.

- **Send a weekly "what Foreman did for you" receipt** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: T-0795 (plain receipts) is deferred. The nightly digest exists, but the user keeps asking for measurements rather than a summary of value delivered.
  Done when: `fm night` writes a one-screen weekly note with tasks closed, claimed fixes reversed, bets settled, cost and time, and any item waiting on the user.

Next question: Which Foreman feature would the user switch off first if the weekly receipt showed its cost beside its measured gain?
Next question: What does a first-time user see in their first 10 minutes, and which step makes them quit?
