# Brainstorm — lens: user value

- **Make Foreman detect its own usage burn and act on it** — FEATURE — value 5 — effort M — risk med — category: usage budget
  Why: the user said "foreman should've figured it out itself" after they had to point out the burn. Context per reply is already measured (`fm cost`), and the 200k compact threshold exists, so the missing piece is acting on the measurement without being asked.
  Done when: a session whose replies cross the per-reply context threshold gets a Foreman notice and a compact with no user prompt, and `fm cost` shows the event.

- **Release a model run's edit leases when the run ends** — FIX — value 5 — effort S — risk low — category: runs
  Why: "a model run's edit leases outlive it (drop_session ran only for worker runs), so the next run on the same code is refused for 20 minutes."
  Done when: a test runs two sequential model runs on the same code, the second is accepted, and the first run's leases are gone after exit on success, failure and timeout.

- **Stop affected and evidence checks from queueing behind the machine-wide gate** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: `fm check --affected` and `--evidence` step runs take the global gate lock, so every builder's affected run waits behind the others; a full check already gets a 15-minute cap.
  Done when: two `fm check --affected` runs in different projects both start within 2 seconds of each other.

- **Show the next usage reset in `fm status` and resolve `defer --until reset` to it** — FEATURE — value 4 — effort S — risk low — category: usage budget
  Why: deferrals came back at midnight, two hours before the 02:00 reset (T-1802). The fix works, but the user cannot see when the reset is.
  Done when: `fm status` prints the next reset time, and `fm task defer --until reset` sets the same timestamp.

- **Run `fm doctor` fixes that are safe without asking** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user said "don't ask me for anything either … just go." The rules file was 6,416 characters, over the 6,400 budget, and needed a manual trim.
  Done when: an over-budget rules file is trimmed automatically, the change is reported in one line, and a `fm undo` reverts it.

- **Let `fm quiet` read stdin** — FIX — value 4 — effort S — risk low — category: CLI
  Why: "fm quiet runs its command with no stdin, so a heredoc script fed to it does nothing and reports exit 0."
  Done when: `fm quiet <<'EOF' … EOF` runs the script, and with no stdin and no command it exits nonzero with a message.

- **Queue a `g` pressed mid-run instead of telling the user to press it later** — FIX — value 3 — effort S — risk low — category: TUI
  Why: "g pressed during a run waits for it, then works the queue (T-1779 said it waits; it only told you to press g later)."
  Done when: pressing `g` during a run shows "queued behind <run>" and starts the queue when that run ends, with no second keypress.

- **Explain a stuck run in one command** — FEATURE — value 4 — effort S — risk low — category: diagnostics
  Why: the user asked for `fm code why ID` (T-1373), covering status, where it stopped, a stall's cause and the next command.
  Done when: `fm code why <id>` prints those four fields for a stalled run in under 2 seconds.

- **Skip the "catch it earlier" follow-up when the why-not-caught is "new work"** — FIX — value 2 — effort S — risk low — category: task close-out
  Why: `fm task finish` creates a follow-up for "new playbook" and "n/a", which have nothing to catch; "none" is already skipped.
  Done when: finishing a task with why-not-caught "n/a" or "new playbook" creates no follow-up.

- **Undo a whole run in one command** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: the user can inspect and undo edits, but there is no single command to revert a Foreman run's edits as a unit.
  Done when: `fm undo <run>` restores the tree to its pre-run state in a test repo, and it refuses when the user has uncommitted edits in the same files.

- **Wild: sleep through the reset, wake to a finished queue** — FEATURE — value 4 — effort L — risk med — category: overnight — wild
  Why: `defer --until reset` and the USAGE_LIMIT wait already exist, so queued work can run unattended across the weekly reset.
  Done when: a queue deferred to the reset runs at the reset time with no input, and the morning receipt lists what landed and what failed.

- **Quote the cost of a queue before you start it** — FEATURE — value 4 — effort M — risk low — category: usage budget — wild
  Why: assumption: the duel data and `fm cost` history are enough to predict a queue's token range, so the user can see the budget before spending it.
  Done when: `fm queue` prints a token range, and in the bench's past queues the actual cost lands inside that range in at least 8 of 10 cases.

- **Wild: read the morning receipt aloud in under 20 seconds** — FEATURE — value 2 — effort S — risk low — category: voice — wild
  Why: assumption: a spoken summary of overnight work lets the user catch up without opening a terminal, and fits the "no questions" workflow.
  Done when: `fm say-morning` speaks a summary of overnight results in 20 seconds or less, and it can be disabled with one setting.
