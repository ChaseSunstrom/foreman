# Brainstorm — lens: user value

- **Tell the user why `fm` isn't found, and the one fix** — FIX — value 4 — effort S — risk low — category: install
  Why: The user asked why `fm` wasn't recognized. The answer was a symlink at `~/.local/bin/fm` and a terminal opened before the fix needing a reopen. Foreman could detect that case and say it in one line.
  Done when: In a shell started before `~/.local/bin` was on PATH, `fm` prints the PATH cause and the exact command to run, and in a fresh shell it prints nothing extra.

- **Put blocked-on-you items at the top of `fm status`, with the unblock command** — FEATURE — value 4 — effort S — risk low — category: status
  Why: Several open items are blocked on a human step, such as T-0325 needing `libappindicator-gtk3` via `sudo pacman -S`. They sit in the same list as work that can move now.
  Done when: `fm status` shows a "needs you" section above the queue, and each entry prints the command that clears it.

- **Log every auto-decision to a review list the user reads after the run** — FEATURE — value 5 — effort M — risk med — category: unattended runs
  Why: The user said "don't ask me for anything… just go." Choices are still made silently, so the user can't see them. Each default taken (lens count, model, cut scope) should land in a short list with a one-key undo.
  Done when: After an unattended run, `fm decisions` lists every choice made without a prompt, and reverting one choice re-queues that step.

- **Store "don't ask me" as a standing preference, honored in every project** — FEATURE — value 5 — effort S — risk low — category: preferences
  Why: The user has repeated "don't ask for permission" and "don't ask me for anything" across requests. Foreman does not store that as a setting, so it has to be restated.
  Done when: Setting the preference once in `fm settings` stops confirmation prompts in a new project with no further input, and `fm settings show` displays it.

- **Bounce a new idea that repeats one already in the ledger before filing it** — FEATURE — value 4 — effort S — risk low — category: brainstorm
  Why: The ledger holds about 200 "ideas so far," and every new round has to be checked against it by hand. A title-and-category match at filing time would catch repeats before they reach the user.
  Done when: Filing a round whose ideas repeat ledger entries drops those repeats, reports the count dropped, and keeps the rest.

- **Write every closed task as a one-line change note the user can read** — FEATURE — value 3 — effort S — risk low — category: changelog
  Why: Recent commit subjects read like "lens_rates", "T-1790", "Cut usage burn: compact at 200k". The user has to decode each one to see what changed for them.
  Done when: `fm log --user` prints one plain sentence per closed task, with no task IDs or module names, and the sentence states what the user can now do.

- **Re-run a past request against today's code in one keystroke** — FEATURE — value 4 — effort M — risk low — category: replay
  Why: The user restates requests that were closed earlier (e.g., "Cut Foreman's usage burn" came back and had to be recreated). Replaying the old request as a new task would skip that restatement.
  Done when: Selecting a closed task and pressing one key creates a new task with the original request text, and the new task's first step cites the old task ID.

- **Accept "like last time" and reuse the closed task's plan** — FEATURE — value 4 — effort M — risk med — category: recall
  Why: Requests recur in similar words, such as "fm defer --until reset" appearing twice. Foreman could match a new request to a closed task and offer that task's plan as the starting point. (wild)
  Done when: Typing a request that closely matches a closed task shows that task's plan as a suggestion, and accepting it starts from that plan with the old steps marked.

- **Dictate a request by voice and have it land as a queued task** — FEATURE — value 3 — effort M — risk med — category: intake (wild)
  Why: The user writes many long requests and pastes context into them. Speaking a request while away from the keyboard and filing it on the same queue would remove the typing step.
  Done when: A spoken request transcribed locally becomes a task with the transcript stored verbatim, and the task's first line echoes what was understood.

- **Show which commit the live site serves beside the build** — FEATURE — value 3 — effort S — risk low — category: deploy
  Why: The user asked for a push to main so the site would publish. The task was marked failed because its criterion was pinned to an older commit, and the site's current commit was not visible.
  Done when: `fm site` prints the commit the live site serves and the build's commit, and says "in sync" or names the difference.

- **Show the next usage-reset time and what it unlocks, in the task list** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: The user deferred tasks to the weekly reset, and the reset-time bug moved them two hours early. Showing the reset next to each deferred task makes the time visible before it is relied on.
  Done when: Each deferred task in the list shows its resume time in local time, and that time matches the value the usage source reports.

- **Ask for one number instead of a plan when the user wants a fast answer** — FEATURE — value 3 — effort S — risk low — category: ask mode
  Why: The user asked for answers that don't burn tokens. A mode that returns a single estimate (cost, minutes, or pass/fail) with no plan would serve quick questions.
  Done when: `fm ask --number "<question>"` returns one line with a number and a confidence word, and the reply is under 40 tokens.
