# Brainstorm — lens: the irreversible door (invented): it stops for the user only when a step is irreversible and ambiguous; everything else is decided, recorded and reversible

- **Derive the door class from the command's effect, not its name** — FEATURE — value 5 — effort M — risk med — category: doors
  Why: earlier ideas propose a "verb table" for reversibility; a table misses `git push` wrapped in a script, `fm ship` or a migration. assumption: guard already parses commands (it blocks bypass-mode commands), so it can also resolve what a command touches (remote, db, shared file, outside the worktree).
  Done when: a fixture of 30 wrapped or aliased one-way commands (script calling push, make target running a migration) is classed one-way by an effect probe, and 30 local-only ones are classed two-way, with zero misses on the first set.

- **Undo-or-nothing line is required before any one-way step runs** — FEATURE — value 5 — effort M — risk low — category: doors
  Why: the open list has "pair every one-way step with its undo line" only as an idea, but the Mission 5 request says Foreman stops "only when something is irreversible and ambiguous"; without a stated undo the first half can't be checked. assumption: plan rows can carry a field.
  Done when: focusing a task whose step is one-way with no `undo:` (or an explicit `undo: none`) is refused, naming the row; `undo: none` forces the ask path.

- **Auto-decision receipts live in a file the model can't write** — SECURITY — value 4 — effort M — risk low — category: ledger
  Why: "Everything else it decides and records" has no stated writer; steer "bind every consent to a channel the model can't write" shows the user cares about this. The recorder must not be the party being audited.
  Done when: a test where a session tries to edit or delete a decision receipt via Bash/Edit is denied by the guard, and `fm decisions` lists every receipt with its undo command.

- **`fm undo N` replays the receipt's undo line** — FEATURE — value 5 — effort M — risk med — category: recovery
  Why: recording a decision without a one-command reversal makes "reversible" a claim. Existing receipts idea stops at text. assumption: most two-way steps can name a git or file-restore command.
  Done when: for 5 sample receipts (file edit, config change, task close, lane merge, dependency bump), `fm undo` restores the prior state and a test compares the tree hash before and after.

- **Re-class a door when the world changes mid-task** — FEATURE — value 4 — effort M — risk med — category: doors
  Why: a step reversible at plan time (local branch) becomes one-way after a push, a publish grant is spent, or a shared DB is touched. Listed as "detect doors that became one-way" but with no trigger point. assumption: hooks see tool calls before they run.
  Done when: a task that was local-only, after a `git push` in a lane, has its remaining rows re-classed and the next one-way row asks; a test shows the reclass event.

- **Make "ambiguous" a measured fork, not a feeling** — FEATURE — value 4 — effort M — risk med — category: ambiguity
  Why: only two readings that disagree *on the effect of the one-way step* matter; earlier ideas count any reading disagreement and would stop on harmless forks. assumption: readings are stored per plan (T-2269 gate requires 2+ for L).
  Done when: a task with two readings that differ only in naming does not stop; one whose readings differ on which table is dropped does, and the stop message quotes that difference.

- **Ask once, with a deadline and a safe default, for irreversible-and-ambiguous steps** — FEATURE — value 4 — effort S — risk low — category: asking
  Why: steer 3 says don't stall; a blocking ask for the user being away conflicts with waiting out limits. assumption: `fm ask` exists and can carry a default.
  Done when: a stop on a one-way step posts one `fm ask` with the two outcomes, runs everything else that it doesn't block, and on silence takes the declared no-op default (never the one-way action).

- **Rehearse one-way steps on a copy and attach the diff to the ask** — FEATURE — value 4 — effort L — risk med — category: dry-run
  Why: `fm prove --migration` (T-2288) already does this for databases; generalize so the user answers a concrete diff instead of an abstract question. assumption: a throwaway worktree or db copy is cheap.
  Done when: a push, a migration and a bulk file rewrite each produce a "would change" summary in the ask; a test shows the real target untouched.

- **Score every stop: did the answer change the plan?** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: no way now to know which asks were necessary; "log every stop" is listed but not its scoring. assumption: the answer is stored beside the ask.
  Done when: `fm triggers`-style output lists ask classes with count, answer-matched-default rate, and a class at ≥90% default over 5+ asks is offered as a standing answer.

- **Fail closed when the door classifier errors or times out** — SECURITY — value 4 — effort S — risk low — category: doors
  Why: the classifier runs in hooks with a latency budget (bench_hooks); a timeout silently treated as "reversible" would defeat the lens. assumption: current hooks fail open on slow paths.
  Done when: a test that forces the classifier to raise or exceed its limit makes a one-way-looking command ask rather than run.

- **Wild: Hold a nightly "regret drill" that replays the day's auto-decisions to a cold child** — FEATURE — value 3 — effort M — risk low — category: audit
  Why: wild; the cold-read pattern already exists for tower files. assumption: a Haiku child can judge "would a user have wanted to be asked?"
  Done when: the morning digest lists decisions the child flagged, each with its `fm undo` line, and flags are scored against later reversals.

- **Wild: A "last-look" window with a visible countdown on cheap-to-redo doors** — FEATURE — value 3 — effort M — risk med — category: asking
  Why: wild; between silently-run and asked lies a window where the user may veto but need not answer. assumption: web UI or notification can show a timer.
  Done when: a flagged step shows a 60 s countdown on the web UI, cancelling aborts it, and silence proceeds only for steps classed redo-cheap.

- **Wild: Door map of the repo — every file, remote and service tagged by how hard a mistake there is to undo** — FEATURE — value 4 — effort L — risk med — category: doors
  Why: wild; `fm graph blast` already maps co-change, so a second layer of "undo cost" per path would feed the plan's Risks. assumption: undo cost can be inferred from git remotes, publish scripts, CI deploy paths.
  Done when: `fm graph doors PATH` prints a class and reason, and focusing a task with scope paths adds the one-way ones to Risks.

- **Wild: Let a cold child try to talk the builder through a one-way door** — SECURITY — value 3 — effort M — risk med — category: adversary
  Why: wild; tests whether the door holds under persuasion, not just under direct commands. assumption: a tool-less child can write plausible justifications.
  Done when: in a fixture run, 20 persuasive justifications produce zero one-way executions without a user-owned grant.

Next question: Which of Foreman's existing outward-facing actions (ship, publish, genesis live, mail) run today without passing through any door check at all?
Next question: When the user is away for hours, what is the longest queue of non-blocked work Foreman can safely do, and does it know?
