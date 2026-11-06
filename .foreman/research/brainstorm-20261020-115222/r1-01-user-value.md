# Brainstorm — lens: user value

- **Close every task with a one-paragraph "what you got" receipt** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: the user keeps asking for cost and correctness evidence on the site, but nothing shows it to them at the moment of close; the closed-task output is bookkeeping, not a result they can read in ten seconds.
  Done when: closing a task prints at most 5 lines: what changed (files, diff size), which command proved it, its pass/fail summary, and Foreman's token share for that task; a test asserts the format.

- **Add `fm why-slow` for the last session** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the pack shows a ~60% per-session premium on long runs and 10-50% on short ones, but the user can't see where their own session paid it. Round 1 gives the by-source share but not by-turn causes.
  Done when: `fm why-slow` lists the three costliest turns of the latest session with source (hook note, fm output, re-read, subagent) and a one-line suggestion; a fixture-session test pins the output.

- **Let a request say "quick" to skip ceremony for one task** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: short, fully specified tasks pass either way but cost Foreman 10-50% more; the benefit is on long, multi-request work. assumption: users hit the cheap-task tax often and currently can't opt out per request.
  Done when: a prompt starting with `quick:` creates a task with no plan stage and a single verify, and `fm cost` shows lower injected bytes for it than the same prompt without the prefix.

- **Show "needs you" first at session start** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the open-work list has many blocked and deferred items (T-0335, T-0352, T-0418, T-0325) that sit waiting on a human action; the user said "no need to ask me", so unblocked items should run and only real human-only steps should surface.
  Done when: SessionStart prints at most 3 lines listing blocked tasks with the exact command or action each waits on, and nothing when none are blocked.

- **Turn blocked-on-human items into copy-paste steps** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: T-0325 names `sudo pacman -S libappindicator-gtk3` and T-0418 an update to foreman-ui 0.6.1; these linger because they need a person once, not because they're hard.
  Done when: `fm blocked` prints each blocked task's single command, and running it then marking done re-queues the dependents.

- **Make "continue" pick work by value, not by order** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the user's most frequent request is "continue, super improve foreman", and ~35 deferred briefs sit there; the choice of what is next is currently implicit.
  Done when: `fm continue` prints its chosen task with one line of why (value, effort, evidence) and the alternatives it passed over, and a test pins the ranking on a fixture queue.

- **Warn at request time when Foreman will cost more than it returns** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: measured results say Foreman wins on long multi-request sessions (6/6 vs 3/6 correct) and loses on cost for short ones. assumption: a cheap heuristic (request count, estimated files) predicts which case a prompt is.
  Done when: a single-file, single-request prompt gets a one-line note suggesting `quick:`, a multi-request prompt gets none, and both are tested.

- **Release notes written for the user's own repo, not Foreman's** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user asks for releases constantly (1.2.37–1.2.41) and the titles are internal task names; a user reading the change wants what's different for them.
  Done when: `fm release` output has a "what changes for you" section with at most 5 bullets derived from closed tasks' user-visible criteria.

- **Wild: Offer an "undo the last hour" button** — FEATURE — value 5 — effort L — risk high — category: user value — wild
  Why: assumption: the biggest fear in bypass mode is a session that went off course; the ledger already knows each task's edits and proofs.
  Done when: `fm rewind --to T-NNNN` restores files edited after that task's close, shows the diff first, and leaves a branch with the discarded work.

- **Wild: Let the user hand Foreman a dollar amount and a deadline** — FEATURE — value 5 — effort L — risk med — category: user value — wild
  Why: the user wants it better than Claude Code and cheaper; unattended runs have no stated budget, only per-benchmark caps.
  Done when: `fm run --budget 3 --until 07:00` stops cleanly at either limit, closes or parks the current task, and prints what finished, what's left and the spend.

- **Wild: Morning-after digest as a single page** — FEATURE — value 4 — effort M — risk low — category: user value — wild
  Why: unattended queues are central to the pitch, yet the user comes back to a ledger; the web UI could answer "what happened while I slept" at once.
  Done when: opening the web UI after an unattended run shows one page listing tasks finished, tasks stuck with the reason, spend, and refusals by the guard, each linking to its proof.

- **Detect and re-ask when a request is ambiguous before planning** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: steer evidence shows a criterion named a test module that didn't exist; a wrong premise cost a task. Catching it at intake is cheaper than at verify.
  Done when: a task whose criterion references a missing file, command or module is flagged at creation with the nearest existing match suggested, in a test.

- **Keep a "things you told me twice" list** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: repeated asks ("release and push", "continue, super improve") and a pushback ("no need to ask me") are standing preferences the tool should hold rather than relearn.
  Done when: a repeated steer is saved as a standing preference visible in `fm prefs`, applied to later tasks, and removable with one command.
