# Brainstorm — lens: user value

- **Walk-away check** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: the user wants Foreman to run unattended, but nothing answers "is it safe to leave now?". Assumption: the signals (hooks installed, guard on, queue non-empty, disk and auth fresh, no live lease conflicts) already exist in `fm doctor` and the ledger.
  Done when: `fm away` prints one green/amber/red line with the first failing reason, and a test with a missing hook flips it to red.

- **Pace unattended work to the rate-limit window** — FEATURE — value 5 — effort M — risk med — category: scheduling
  Why: assumption: overnight and brainstorm fan-outs run `claude -p` children, and a plan limit hit mid-run would stall the queue with partial results (see T-0831 on capped children).
  Done when: with a simulated limit-reset time, the dispatcher parks new children until the reset and logs "parked until HH:MM"; a test covers it.

- **Make every guard block suggest the safe alternative** — FEATURE — value 4 — effort M — risk low — category: security
  Why: the guard stops commands in bypass mode, but a bare denial makes the model retry variants. A rewrite such as "use `git clean -n` first" or "target a path inside the repo" would end the loop on the first turn.
  Done when: blocked-command messages for at least the top 10 guard rules include a concrete safe command, and a test asserts the suggestion is itself allowed by the guard.

- **Snapshot before risky-but-allowed commands** — SECURITY — value 4 — effort M — risk med — category: safety net
  Why: the guard only has allow or deny. Commands that are allowed but destructive in scope (mass `sed -i`, `git checkout .`, `rm` inside the repo) have no undo. This is separate from "undo a closed task". Assumption: a cheap `git stash create` ref or a tmp copy is enough.
  Done when: such a command leaves a `refs/foreman/pre/<ts>` ref, and `fm restore` returns the tree to it in a test.

- **Keep secret file contents out of the transcript** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the pack has outbound-ledger and commit-scan ideas but nothing about reads. A `cat .env` or Read of a key file puts the secret in the context and the transcript. Assumption: a PreToolUse hook can rewrite or deny such reads.
  Done when: Read of `.env` returns key names with values masked, and an allowlist flag restores the raw read.

- **Make Agents graph nodes actionable** — FEATURE — value 4 — effort M — risk low — category: pane
  Why: the user asked for the graph and for easy resume (T-1023, T-1026, T-1028). A stopped node in the graph should offer resume, open diff and kill as keypresses instead of requiring a verb.
  Done when: selecting a stopped builder node and pressing `r` runs the resume path, verified by a pane test.

- **Rank obstacles by minutes lost** — FEATURE — value 5 — effort M — risk low — category: self-improvement
  Why: the user's complaint, "why have you not really improved", needs a measurable answer, and the pack's scorecards count fixes shipped, not cost. Ranking recurring obstacles by wall-clock and turns lost sends the next self-improvement task to the costliest one.
  Done when: `fm obstacles` lists the top 5 by time lost from the ledger, and `fm next` can seed a task from the top row.

- **Park questions as assumptions and continue** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: an unattended builder that stops to ask idles the queue. Assumption: it can record "assumed X" in an assumptions ledger, proceed, and have the user's later answer flag only the tasks that depended on it.
  Done when: answering a parked question with a different value reopens exactly the tasks tagged with that assumption.

- **Try a hook against recorded stdin** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: authors of gates, guards and cards have no quick way to see what a hook would decide. Related to the shadow-diff idea but human-facing.
  Done when: `fm hook try <hook> <recorded.json>` prints the decision, injected text and elapsed time without touching state.

- **Wild: Hand off a session to a teammate through git notes** — FEATURE — value 4 — effort L — risk med — category: collaboration — wild
  Why: the user wants fixes and state to travel with git. A capsule (task, brief, decisions, assumptions) attached as a git note on the branch lets a teammate's Foreman resume with context, going past local resume.
  Done when: after `git fetch` on a second clone, `fm resume <branch>` shows the capsule and the first plan step.

- **Wild: Speak status hands-free** — FEATURE — value 2 — effort M — risk low — category: voice/devices — wild
  Why: assumption: a local TTS (piper) can say "blocked on T-0412, needs your call" or "queue done, 7 closed", covering car, kitchen and away-from-desk use. Nothing is sent off the machine.
  Done when: `fm say` speaks the pane's headline through the local engine, and no network call is made (asserted by a test).

- **Wild: Learn gates from the user's own terminal** — FEATURE — value 3 — effort L — risk high — category: learning — wild
  Why: assumption: an opt-in shell hook sees which test and lint commands the user runs by hand. Foreman could propose them as the repo's gates, which is better than guessing from `fm map`.
  Done when: after the same command is run 3 times, `fm doctor` offers it as a gate. The shell hook is off by default and logs nothing else.
