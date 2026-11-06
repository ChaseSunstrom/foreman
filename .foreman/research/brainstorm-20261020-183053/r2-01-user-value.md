# Brainstorm — lens: user value

- **Show a "while you were away" digest on return** — FEATURE — value 5 — effort M — risk low — category: unattended
  Why: the user asks for long unattended runs (marathon showcase, overnight routines T-0793). The ideas so far cover alerts and a finale, but not coming back to a run hours later. Assumption: the TUI can tell when input has been idle.
  Done when: after 10 idle minutes in a test run, the next keypress shows a one-screen digest of tasks closed, guard refusals, spend, and the first item that needs a decision, and any key dismisses it.

- **Add a claims-vs-proof ledger view** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: Foreman's promise is "prove its work with commands it actually ran". A view that lists each claim the model made beside the command and exit status backing it, with unbacked claims in a warning color, puts that promise on screen. Assumption: the proof records already link claims to commands.
  Done when: a fixture run with one unproved criterion shows that row flagged and the other rows linked to a command and result.

- **Let the user steer mid-run from a note box** — FEATURE — value 5 — effort M — risk med — category: control
  Why: the user steers constantly ("no need to ask me", "the TUI looks like crap"). Today that means interrupting. A note box queues text as a pending chip that the harness delivers at the next turn boundary.
  Done when: a note typed during a fake-model run appears as a pending chip, then in the next model request, and the chip clears.

- **Forecast finish time and cost for the whole queue** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the pack shows dollar caps and a long open-work list, but the gauge ideas only show the current burn. Per-task cost and time history can project "queue done in about 2h10, about $3.40, 80% band".
  Done when: with a seeded history of 10 tasks, the header shows a range for the queued tasks, and the range moves after a task finishes.

- **Explain a guard refusal with a one-key fix** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: recent commits (T-1288, T-1289) added "how to go on" hints to refusals. The TUI could expand a flashed verdict into the rule, the reason, and the hint, with a key to send the hint to the model.
  Done when: selecting a refusal in a fixture shows its rule and hint text, and the send key queues exactly that hint.

- **Edit the queue from inside the TUI** — FEATURE — value 4 — effort M — risk med — category: queue
  Why: the open work list has more than 40 items, mostly deferred. Reordering, deferring, or dropping a task needs a trip out to `fm`.
  Done when: moving a task up and dropping another in the TUI changes `fm task` order and state, and the harness picks the new next task.

- **Copy out a proof-built commit message and PR text** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: the user releases often and the commit subjects are consistent, so the finished task's criteria and evidence are enough to generate the text. Assumption: the criteria and evidence are stored per task.
  Done when: one key on a closed task puts a message on the clipboard (or writes it to a file) that names each criterion and its evidence command.

- **Take over: pause into a shell, then resume** — FEATURE — value 4 — effort M — risk med — category: control
  Why: the guard refuses commands in bypass mode, so a person sometimes has to step in by hand. A pause key could drop to a shell in the run's worktree, then resume with leases and state intact. Assumption: worker leases (T-1294) survive a pause.
  Done when: pause, a manual file edit, and resume leaves the run continuing, and the judge counts the manual edit as the user's.

- **Ask the run** (wild) — FEATURE — value 4 — effort L — risk med — category: observability
  Why: assumption: people won't read event logs. A side prompt answers "why did step 3 fail?" or "what did it spend on?" from the run's event log, with a cheap model and citations to event ids.
  Done when: a question about a seeded failing step returns an answer that cites the event id of the failing command.

- **Race a ghost of your best run** (wild) — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the Gantt and `fm code bench` exist, and the stated goal is faster and cheaper than Claude Code. Drawing the median previous run on the same task as a faint ghost track turns every run into a benchmark. This differs from the replay scrubber, which looks backward at one run.
  Done when: a rerun of a task with a stored baseline shows a ghost marker, and the end card says ahead or behind in seconds and dollars.

- **Write the end-of-day shift report** (wild) — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: the release asks list batches of work (1.2.38 to 1.2.44). A Markdown report of what shipped, what was dropped and why, and what is blocked would feed release notes and a standup. Assumption: the drops and steers are already recorded with reasons, as the pack's "dropped" entries show.
  Done when: `fm code` exits with a report file listing closed, dropped, and blocked tasks with reasons, and it matches the task store in a test.

- **Heat-tint the touched files by risk** (wild) — FEATURE — value 3 — effort M — risk low — category: review
  Why: the pack mentions blast-radius ideas (T-0788). In the diff list, tint each file by churn, missing tests, or size of change, so a reviewer opens the risky ones first.
  Done when: on a fixture repo, a file with no test and high churn ranks above a tested, stable one in the diff list.
