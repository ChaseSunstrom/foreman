# Brainstorm — lens: unspoken needs

Answers to earlier questions, from my lens:
- **Most ignored trigger:** the one the user never asked for, meaning self-filed work. The dropped ledger already shows this, so weight false alarms above misses.
- **Real timer vs. fake-clock week:** trust the real timer, because only it carries the user's real environment. Record the disagreement in the same ledger.
- **Longest silent gap:** unknown from the pack. Compute it from session timestamps before designing any catch-up.

- **Label every finish by the user's next message** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: the steers say weakness-finding must use signals Foreman didn't author, and "done" is only graded by Foreman's own oracles. assumption: the next user message after a finish is the truest outside label, and a no-model lexical rule can sort it into accept, correct or extend.
  Done when: on a fixture transcript with 3 planted follow-ups, `fm outcomes` shows each finish labelled correctly and reports a held rate by label.

- **Mine the user's hand-edits to Foreman-written files as corrections** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: assumption: when the user edits a goal file, coverage.md or a task's DONE-WHEN by hand, they're saying what they never typed to Foreman. The pack shows steers and "steered:" lines but no feed from file edits.
  Done when: editing a row's wording in a fixture produces a draft steer candidate that names the old and new text. The candidate files nothing until accepted.

- **Scan Foreman's own ledgers and captures for pasted secrets** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: "verbatim capture" (T-0790) and the user-model miner store what the user pasted. `fm genesis live` and `fm ship` publish to main. Earlier ideas scrub outputs, not the stores.
  Done when: a planted fake token in a captured brief makes `fm doctor` WARN with file and line and the token masked, and `fm genesis live` refuses to publish until it's cleared.

- **Give each goal a data-out receipt** — PRIVACY — value 4 — effort M — risk low — category: local-first
  Why: cold reads, brainstorms and exams spawn children that receive diffs, steers and the user's words. The pack has egress fences but no readable account of what left. assumption: a spawn log with model id exists to read from.
  Done when: `fm goal receipt` lists every child spawned for the goal with model, file count and bytes, and its count equals the spawn log's.

- **Pin goal-oracle commands on first sight** — SECURITY — value 3 — effort M — risk med — category: trust
  Why: assumption: the finish oracle runs shell commands from a goal file. If that file arrives by pull, clone or a git ref, it's code the user never reviewed. This is the same trust-on-first-use idea as trigger hashing, applied to goals.
  Done when: a changed oracle command in a pulled goal file makes the verdict "needs review" and does not run it until `fm goal trust` records its hash.

- **Keep resume cost flat with a snapshot and a tail** — PERFORMANCE — value 3 — effort M — risk med — category: resume
  Why: the goal exists to carry over days, and the hooks are size-gated (`bench_hooks.py`). A journal that grows over 30 days taxes every SessionStart.
  Done when: on a synthetic 90-day journal, resume reads within 10% of the bytes and wall time of a 1-day journal and produces the same "where we were" lines.

- **Ratchet start-up time for the verbs the user types most** — PERFORMANCE — value 3 — effort S — risk low — category: CLI speed
  Why: the gates bench hooks, not `fm next`, `fm doctor` or `fm task`. With 131 lib modules, an import creeps in quietly. assumption: the event log can rank the top 10 typed verbs.
  Done when: `fm ship` fails if the median wall time of the top 10 verbs on a loaded bench grows more than 20% over the recorded baseline.

- **Replay the user's real `fm` command history through old and new versions on upgrade** — FIX — value 3 — effort M — risk med — category: regression
  Why: hook-input replay is proposed, but verbs the user actually types (flags, ids, odd habits) are what break silently after a refactor.
  Done when: a fixture history of 30 commands gives identical exit codes and normalised output on two versions, and a deliberately changed flag is reported.

- **Mirror the goal into a sync folder as todo.txt plus a static HTML page** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the user wants the phone and any other machine to show where the goal stands without a server, an account or the cloud. Off until a path is set.
  Done when: with a folder set, closing a row rewrites both files within 5s and the HTML opens offline. With no folder set, nothing is written.

- **Make `fm` a good terminal citizen** — FEATURE — value 2 — effort S — risk low — category: developer experience
  Why: assumption: completion for verbs, task ids and goal rows, plus `NO_COLOR` and a `--plain` mode, is expected of a tool with this many verbs. The pack shows typo tolerance asked for but no completion.
  Done when: generated bash, zsh and fish completions finish `fm task sh` and a real task id in a test shell, and `NO_COLOR=1 fm status` emits no escape codes.

- **List steers whose automatic check has never fired** — CLEAN — value 3 — effort S — risk low — category: steers
  Why: 40+ steers each become a `fm decide --check`. A check that never fires either guards nothing now or is broken. Neither is visible.
  Done when: `fm decide --list` shows fire count and last-fired date per check, and one check with zero fires in 30 days is named in `fm doctor`.

- **Wild: write an absence will for long gaps** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: wild. The user's steers say to never stop for budget and to wait out limits, but nothing says what to do if they vanish for 30 days. Foreman drafts one paragraph from the steers, and the drive obeys it: continue must-rows only, decay the spend ceiling, then park with a postcard.
  Done when: on a fake clock, 30 days of silence parks the goal at the will's stage, with a note saying which rule did it.

- **Wild: print a one-page desk clipboard** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: wild. A print-styled A5 page lists today's rows, the cut line and the user-only items, so the plan can sit beside the keyboard or be taken to a meeting.
  Done when: `fm goal print` writes one page that fits on A5 with every user-only item on it.

- **Wild: replay the day's costly decision with the runner-up overnight** — FEATURE — value 3 — effort L — risk med — category: counterfactual
  Why: wild. Costly decisions are already recorded via `fm decide --kind costly`. On idle hardware, the night job builds the runner-up in a scratch worktree and records whether the outcome would have differed, to learn which gates matter.
  Done when: one recorded decision yields a morning line saying "runner-up same / better / worse on the verify command", with the scratch tree removed.

Next question: Which of the user's own work artefacts (hand-edits, reverts, terminal failures) carry the unspoken corrections that no ledger Foreman writes can see?
Next question: What does Foreman publish or send that the user would be surprised to learn left their machine?
