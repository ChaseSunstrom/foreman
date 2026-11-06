# Brainstorm — lens: simplicity

- **Send the filter, not the pile** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: this pack carries thousands of "ideas so far" lines and still produces repeats. Assumption: a pile that long mostly costs tokens without preventing duplicates.
  Done when: `fm ideas` sends children only cluster names plus the shipped and dropped lists, then drops any returned idea whose keyword fingerprint overlaps the stored pile by 60% or more, and a test shows a known repeat is rejected and the pack is under 5k tokens.

- **Scale lens count down as the pile saturates** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: round 3 fills "thin" categories while the pile has thousands of entries. Assumption: later rounds' marginal lenses mostly repeat earlier ones.
  Done when: with a pile over 2,000 ideas, `fm ideas` runs at most 3 lenses, chosen from the thin categories, and prints which lenses it skipped and why.

- **Collapse agents to a builder and a checker** — CLEAN — value 4 — effort M — risk med — category: agents
  Why: round 1 added effort and maxTurns per agent, and the repo has reviewer, recon and other agent files. Assumption: most agents differ only in prompt text and tool list.
  Done when: the agent directory holds at most 3 files, each former role is a parameter or skill reference, and the existing agent tests pass unchanged.

- **Generate every agent file from one role table** — CLEAN — value 3 — effort S — risk low — category: agents
  Why: per-agent model, effort and maxTurns are now repeated frontmatter that can drift. Assumption: the files share boilerplate.
  Done when: `fm doctor` fails if any agent file differs from its generated form, and editing the table alone changes all agents.

- **Make one 10-line NOW file the only thing resume reads** — PERFORMANCE — value 4 — effort M — risk med — category: resume
  Why: the user's core promise is "resumes at the exact step", and the step pointer drifts (T-0759). Assumption: resume currently reads several state files.
  Done when: after `/compact` in a test session, resume restores task, step and next action from `NOW` alone, and deleting every other state file still resumes correctly.

- **Default every task verb to the active task** — FEATURE — value 3 — effort S — risk low — category: cli
  Why: T-ids are repeated in nearly every `fm` call. Assumption: users and agents mostly act on the active task.
  Done when: `fm task done`, `plan`, `set` and `show` work without an id, and an ambiguous case errors with the id to use.

- **Make successful `fm` verbs silent** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: output is already a measured token cost (compact output, whisper caps). Assumption: write verbs echo more than the caller needs.
  Done when: write verbs print one line or nothing on success, `-v` restores the old text, and golden-output tests show the saved bytes.

- **Tie scratch artifacts to a round's lifetime** — CLEAN — value 3 — effort M — risk low — category: state
  Why: round 1 left brainstorm files, spilled outputs and catalogue pages, and a retention table is still an open idea. Assumption: these have no use after the round's receipt is written.
  Done when: `fm round close` (or the nearest existing close step) deletes that round's scratch files, keeps a one-page receipt, and a test confirms nothing referenced by an open task is removed.

- **Wild: Configure Foreman by deleting lines from `fm.lock`** — FEATURE — value 4 — effort M — risk med — category: config
  Why: opt-ins like compact output and the monitor are separate toggles, and the user asked for fewer decisions. Assumption: a visible file of enabled features is easier to reason about than flags.
  Done when: removing a feature's line from `fm.lock` disables it at the next session start, `fm doctor` reports the diff, and re-adding the line restores it.

- **Wild: Mint a paste-in resume token** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: resume today needs the same machine and session state. Assumption: the user sometimes moves between sessions or devices.
  Done when: `fm token` prints one line containing task id, step and a state hash, and pasting it into a fresh session restores the same position or says exactly what differs.

- **Wild: Fail any feature that can't be explained in one generated sentence** — CLEAN — value 3 — effort M — risk low — category: legibility
  Why: the surface keeps growing (about 73 skills and 48 lib modules). Assumption: a feature a cheap model can't summarise in 15 words is probably too tangled.
  Done when: a CI check asks a cheap model for a one-sentence summary of each verb and skill, and flags any it can't write or that exceeds 20 words.

- **Wild: Offer a three-line `fm status --haiku` as the default status** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: statuses are already many surfaces and long strings. Assumption: a fixed three-line shape (task, step, needs-you) is enough most of the time.
  Done when: `fm status` prints at most 3 lines under 60 characters each, and `--full` prints the old output.
