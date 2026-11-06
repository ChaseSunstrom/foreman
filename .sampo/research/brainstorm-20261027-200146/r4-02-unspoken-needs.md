# Brainstorm — lens: unspoken needs

- **Fail any fm command that exits 0 having done nothing** — FIX — value 5 — S — risk low — category: honest exits
  Why: `fm quiet` got a heredoc script on stdin, ignored it, and reported exit 0. A silent no-op looks like success, so the user can't see the failure. Evidence: the stdin report in the user's words.
  Done when: every fm command that receives input it doesn't read exits nonzero and names the bytes it dropped; a test sweeps all commands with piped input.

- **Run the install path from a fresh login shell as a gate** — FIX — value 4 — S — risk low — category: first run
  Why: the tests passed while `fm` wasn't on PATH in terminals opened before the symlink. The user only saw it in their real shell. Assumption: other installs break the same way.
  Done when: `bash -lc 'fm version'` runs in the gate and fails the check with the PATH it saw when `fm` is missing.

- **Echo a deferral's firing time back before accepting it** — FEATURE — value 4 — S — risk low — category: trust in timing
  Why: `defer --until reset` fired at midnight, two hours before the 02:00 reset. The user has to trust the time without seeing what it resolved to.
  Done when: `fm task defer` prints the absolute local time and zone it will fire at, and a test checks that the reset deferral prints 02:00 in the user's zone.

- **Answer "does Foreman already do this?" before a build starts** — FEATURE — value 4 — S — risk low — category: duplicate asks
  Why: several recent asks repeat things that exist or were already filed (the `fm` lookup, the headless probe, the rules trim). Asking for a feature the product has wastes a run.
  Done when: `fm has <request>` matches the words against the command table, the open backlog and recent closed tasks, and prints the existing id or "none" in one line.

- **Blame a line to the request and proof that wrote it** — FEATURE — value 4 — M — risk low — category: provenance
  Why: the journal already links tasks to commits and proofs, so the user's "why is this here" question has the data but no single answer.
  Done when: `fm blame FILE:LINE` prints the task id, the user's request text, and the proof id that passed before the line landed.

- **Receipts tag every claim with how it was checked** — CLEAN — value 5 — S — risk low — category: trust in reports
  Why: the user keeps re-checking Foreman's claims by hand. Each close message should separate "ran", "read" and "assumed", so the user knows what needs looking at.
  Done when: a receipt with a "tested" claim and no matching logged command fails `fm check`, and the close message shows the three labels.

- **Stop after the third correction in a day and say what it misread** — FEATURE — value 4 — S — risk low — category: correction loops
  Why: the user has corrected the same kind of thing several times ("I shouldn't have had to tell you", "don't ask me"). Each repeat costs a run and hurts trust.
  Done when: on the third correction in one category within 24 hours, Foreman writes a three-line misread summary, stores the preference, and applies it before the next task starts.

- **Decode terse pushback into one named reading and act on it** — FEATURE — value 3 — S — risk med — category: short messages
  Why: the user's messages are fragments ("dropped", "steered", "pushed back"). Asking what they meant adds a round trip, and the user has said they don't want that.
  Done when: given a short correction and the last diff, Foreman states the reading it acted on in one line, and one undo word reverts it.

- **Carry the user's intent in their words and score each diff against it at close** — FEATURE — value 4 — M — risk med — category: intent drift — wild
  Why: a finished change can pass every gate and still miss what the user asked. Assumption: the request text is kept in the task, so drift can be measured against it.
  Done when: each close lists the request's sentences beside the diff hunks that address them and flags any sentence with no matching hunk.

- **A one-key "this is wrong" button that files itself** — FEATURE — value 4 — S — risk low — category: feedback without words — wild
  Why: the user sends terse corrections, so the report cost should be near zero. A single key can capture the last 60 seconds of state and file it as a task.
  Done when: one key during a run or after close writes a task with the last command, the diff and the active task id, and it needs no typed text.

- **A walk-away light above the prompt** — FEATURE — value 3 — S — risk low — category: ambient status — wild
  Why: the user keeps asking whether it's safe to leave a run. One colour, computed from unpushed work, failing gates, budget near cap and stalled runs, answers that without a report.
  Done when: `fm status` prints green, amber or red with a reason of ten words or fewer, and a test covers each state.
