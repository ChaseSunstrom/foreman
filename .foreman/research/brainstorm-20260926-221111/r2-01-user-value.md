# Brainstorm — lens: user value

- **Answer state questions in the hook with zero model tokens** — FEATURE — value 4 — effort S — risk med
  Why: the user never runs commands and has burned 20% of a week. "Status?", "what's queued?", "what did you change?" and "how much has this cost?" all have answers in state (`fm status`, `fm cost`, Files touched). Assumption: UserPromptSubmit can block a prompt and show the user a reason without a model turn.
  Done when: a replayed hook trace for "where are we?" returns a state-derived answer with no model call, and the transcript scan shows 0 tokens for that turn.

- **Detect rework after "done" and feed it back** — FEATURE — value 5 — effort M — risk low
  Why: verification grades measure evidence strength, not whether the user was satisfied. Assumption: a later request, correction, or change to the same files within N days is a usable signal. Mechanism: at intake and focus, match new requests and corrections against finished tasks' Files touched; mark that task `reopened`, log the reason, and downgrade its grade and the lessons it produced.
  Done when: a fixture where a follow-up request edits a finished task's files shows `reopened` in `fm digest`, with a weekly first-time-right rate.

- **Resolve "undo that" by description** — FEATURE — value 4 — effort S — risk med
  Why: `fm undo` and checkpoints exist, but the user speaks in phrases such as "revert the login change", not task ids. Mechanism: BM25 over past briefs and Files touched picks the candidate task, then shows one yes/no with the exact files and lines that will revert.
  Done when: the prompt "undo the export button thing" yields a single yes/no naming the right task's files, and yes restores the checkpoint tree.

- **Suppress questions that were already answered** — FEATURE — value 3 — effort S — risk low
  Why: the Stop-hook question nudge and mined corrections exist, but nothing checks whether the answer is already in decisions, corrections, or standing approvals. Mechanism: before the nudge, recall against the question text; on a strong hit, inject "answered: <decision>, cite" so it doesn't reach the user.
  Done when: a test with a recorded decision and a matching question emits an answer note instead of a nudge.

- **Alarm on Foreman's own efficiency trend** — CLEAN — value 4 — effort M — risk low
  Why: cost, usage, and digest each report totals, but nothing catches the tokens per finished task rising after a plugin change. Mechanism: store tokens, turns, and first-try-green per task keyed by plugin version, compare rolling medians, and add one digest line plus a `fm doctor` warning on a regression above 25%.
  Done when: a synthetic history with a 40% jump after a version bump makes `fm doctor` name that version.

- **Map the user's phrases to code entities** — FEATURE — value 3 — effort M — risk med
  Why: requests use vague references ("the sync thing"), and today each one costs exploratory reads. Assumption: request text can be paired with the Files touched of finished tasks. Mechanism: a small phrase→paths glossary is built at record time, and at capture the top match is added as "likely refers to X (confidence)".
  Done when: after one task titled "fix the sync thing", a new request using that phrase lists the same files as the start-here hint before any Read.
