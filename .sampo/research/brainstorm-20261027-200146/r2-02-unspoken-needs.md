# Brainstorm — lens: unspoken needs

- **Heal a terminal that doesn't see `fm`** — FIX — value 4 — effort S — risk low — category: install
  Why: The user asked why `fm` wasn't recognized. A terminal opened before the symlink (2026-10-20) still lacks it, and nothing tells the user why. Assumption: the shell's PATH is stale, not the install.
  Done when: running `fm` in a stale shell prints the one command that fixes it (reopen or `export PATH`), and that command works.

- **Flag acceptance criteria pinned to a commit** — FIX — value 4 — effort S — risk low — category: task hygiene
  Why: The "Push foreman/build to main" task was redone because criterion 2 was pinned to 235932b8 and the build had moved to e021641f. Stale pins make done look false.
  Done when: `fm task` warns on any criterion containing a SHA that isn't HEAD or an ancestor, and suggests the branch name.

- **Keep one ledger of what the user declined** — FEATURE — value 5 — effort S — risk low — category: memory
  Why: The user dropped the RETRY_WATCHDOG step and the "recreated" usage-burn task. Brainstorm rounds still re-propose similar ideas, which the user has to reject again. The pack's own "Ideas so far" list shows the repetition.
  Done when: a dropped item is excluded from the next brainstorm pack, and `fm ideas declined` lists it with the reason.

- **Show every silent choice at close** — FEATURE — value 5 — effort S — risk low — category: transparency
  Why: The user said "don't ask me for anything, just go." When Foreman picks without asking, the user can't see what it decided and why, so they can't redirect it.
  Done when: each closed run ends with a list of decisions made without asking (choice, reason, the undo command), and the list is empty only when no choice was made.

- **Restate the goal in one line before a long run** — FEATURE — value 4 — effort S — risk low — category: alignment
  Why: The user has had requests "recreated with interpretation and approach" and steered step order. Restating the goal costs little and catches a misreading before tokens are spent.
  Done when: `fm run` prints a one-line restatement and waits 5 seconds for a correction key (or continues), and a correction is saved as a note on the task.

- **Show whether main, the site and the installed copy agree** — FEATURE — value 4 — effort M — risk low — category: release status
  Why: The user needed to push to main so the site would publish, and a task was marked done before the site matched. The user's real question is "is it live?", not "did the commit land?"
  Done when: `fm ship status` prints three SHAs (main, deployed site, installed `fm`) and says "in sync" or names the one that lags.

- **Batch Foreman's messages into one hourly digest** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: The user wants fewer interruptions ("don't ask me for anything"). Separate notices for each gate or lease event pull attention away from the work.
  Done when: with digest mode on, a 60-minute run emits at most one user-facing message unless a decision is required, and that message lists everything it batched.

- **Match the project's house style before close** — FEATURE — value 3 — effort M — risk med — category: code style
  Why: The system prompt asks code to match the surrounding comment density, naming and idiom. Assumption: the user reviews style by eye; a check would save a round of corrections.
  Done when: a close-time check compares the diff's comment density and naming to the files it touches and reports any outlier with its line number.

- **Wild: one decision card that replaces every prompt** — FEATURE — value 4 — effort M — risk med — category: interaction
  Why: The user wants to be left alone until something needs them. One card, with the single question and a default that proceeds on timeout, replaces scattered prompts. Assumption: the user will accept a default if the card is short.
  Done when: any run that would ask more than one question produces a single card; with no reply within the timeout, it applies the default and records it.

- **Wild: a weekly letter in the user's own words** — FEATURE — value 3 — effort S — risk low — category: reflection
  Why: The pack holds the user's real phrases ("full force, but efficient", "tokens/usage"). A short weekly letter that reuses their words to say what changed, what it cost and what it declined makes the work feel legible without a dashboard.
  Done when: `fm letter` writes a under-200-word summary that quotes at least two of the user's own phrases from the pack and includes one spend figure.

- **Wild: silence unless the next move changes** — FEATURE — value 3 — effort M — risk low — category: focus
  Why: The user wants efficiency and minimal noise. Foreman would show only the line that changes what the user should do next, and hide progress that doesn't.
  Done when: in quiet mode, a run emits output only when the user's next action changes, and a 30-minute run with no decision points produces no output until its close receipt.
