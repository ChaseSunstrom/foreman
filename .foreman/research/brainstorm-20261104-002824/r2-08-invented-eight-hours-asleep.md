# Brainstorm — lens: invented: eight hours asleep

- **Seal a night plan before sleep** — FEATURE — value 5 — effort M — risk low — category: unattended
  Why: the user is asleep and wants major progress by morning; "Compare the night's spend and progress against a sealed plan" is only a one-liner above. Assumption: no single artifact says what the night will attempt, in what order, with what stop conditions.
  Done when: `fm night plan` writes a file listing ordered tasks, the local model each needs, the cost cap and stop rules, and the morning card shows each line as done, skipped or failed.

- **Batch the night by loaded model** — PERFORMANCE — value 4 — effort S — risk low — category: local models
  Why: the user said a llama-swap switch costs about 3 minutes with no detection; qwen3.8-27b should run first and the MoE only late.
  Done when: a 20-task night queue makes at most one model switch, and the receipt prints the switch count.

- **Add a wake-nobody pager policy** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: "stop asking me for stuff, keep going" and "never interrupt mid-run". Assumption: nothing separates a true emergency (red main after a push, disk full) from a question.
  Done when: during a night window `fm ask` writes to the morning sheet, and only the listed emergency classes may break the quiet.

- **Reserve the last 90 minutes for re-proof of merged main** — FIX — value 5 — effort M — risk low — category: verification
  Why: lanes land in parallel and main has gone red after merges (T-2851 WIP merges). Assumption: nothing proves the final tree as one whole before the user wakes.
  Done when: at the night's tail a full suite and `fm doctor` run on merged main, and any red leaves a revert-or-fix task at the top of the morning card.

- **Fall back to the local model during a usage-limit wait** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: the rule says wait out real limits; eight idle hours are wasted if the limit hits at 2am. Assumption: the 27B can take S-sized, Exam-gated tasks.
  Done when: a simulated limit at 02:00 makes the drive pick an S task the local arm can close, with its Exam, and resume the frontier path afterwards.

- **Review the day's landed commits overnight with a different model** — FEATURE — value 4 — effort M — risk low — category: review
  Why: standing steers want signals Foreman didn't author and cold reads by another model. Assumption: today's landings (T-2848…T-2863) were only read by their builders.
  Done when: each landed commit gets a cross-family read by morning, with findings filed as tasks.

- **Run a bedtime preflight canary** — FIX — value 4 — effort S — risk low — category: unattended
  Why: the drive misjudged running subagents three times (T-2873, T-2900, T-2901) and could hold phantom-wait for hours. Assumption: nothing checks a clean start.
  Done when: `fm night start` fails with a named cause if the local endpoint, disk, grant, clean tree or drive heartbeat is missing.

- **Release a phantom-held drive after 20 quiet minutes** — FIX — value 5 — effort S — risk low — category: unattended
  Why: those same bugs made the drive wait on dead agents; overnight that costs the whole night. Assumption: a wait with no ledger or transcript activity can be released safely.
  Done when: a planted dead agent holding the drive is released within 20 minutes, with a ledger line naming it.

- **Print the morning card from the sealed plan** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the user returns to a long ledger. Assumption: a short plain card (landed, red, waiting on you, spend, one Next line) is what they read first.
  Done when: bare `fm` after a night shows that card and every number matches the ledger.

- **Wild: Hold a nightly ghost-user that predicts the morning's asks** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild; the anticipation Mission needs scoring. A local model writes three likely first asks at bedtime, sealed; the morning shows hits.
  Done when: the card prints the sealed predictions beside what the user typed first.

- **Wild: Run a night league of local models on closed tasks** — FEATURE — value 3 — effort M — risk low — category: local models
  Why: wild; spare hours cost no frontier tokens. The user wants local models scaffolded to frontier results, and the data comes from replaying closed tasks.
  Done when: by morning a table shows pass rate and minutes per model per task kind on at least 10 replays.

- **Wild: Show the night as a dial on the astrolabe** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; the Kirjokansi look, the turning sky. A sleeping-lamp ring on the web UI moves from dusk to dawn, with each landed task as a star and red ones dimmed.
  Done when: the UI draws the night's tasks as marks on the ring, honours reduced motion, and reads from `--json` only.

- **Run a self-shrinking spend plan** — SECURITY — value 3 — effort S — risk low — category: budget
  Why: a $200 cap; a night with no progress burns money. Assumption: a stall limit exists but isn't tied to the sealed plan.
  Done when: a night with two lanes making no diff survival for an hour stops those lanes and says which one cost what.

Next question: when the user wakes, which single line do they read first, and does the ledger contain enough to write it with no model?

Next question: what did the last unattended night actually lose, and has anyone replayed it to see which of these ideas would have saved it?
