# Brainstorm — lens: user value

- **Ship on green by standing permission** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: nearly every recent ask is a fix followed by "Ship Tn to main". That is a manual gate on every task. The user would set a durable rule (kind FIX, at most N files, all gates and proof green, no sensitive paths) and Foreman would ship and report. Assumption: the user trusts proof strength enough to pre-authorize.
  Done when: with the rule on, a qualifying FIX closes and lands on main with no further prompt, and a task that breaks any condition stops and asks. Both are tested.

- **Give overlapping tasks their own worktrees by default** — FEATURE — value 4 — effort L — risk med — category: isolation
  Why: T-1968 and the `_theirs` steers show the same bug class fixed one check at a time (scope check, sensitive-file check, ambient runs, test overlap). They all come from tasks sharing one tree.
  Done when: two open tasks editing different files never appear in each other's scope, dirty, or affected-test results. A test covers `fm task finish` with the other task dirty.

- **Rank closed tasks by how much review they need** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the user ships many small tasks and can't read every diff. Assumption: they would skim a ranked list. Score each task on proof strength (failed-without-change shown or not), diff size, protected core touched, and first-time pass.
  Done when: `fm review` lists the last N closed tasks with "skim" or "read" and one reason each. A task touching core with no failing-first proof ranks above a docs-only one.

- **Draft the DONE-WHEN from a bare request** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the user hand-writes `FIX: … > @path > DONE-WHEN: …` for every ask. Foreman could propose the path and a runnable check from the repo map and test layout, and the user edits only if wrong.
  Done when: a one-line ask with no DONE-WHEN yields a task with a proposed scope and a verify command that exists. The user's edit replaces the proposal.

- **Reproduce the reported bug before editing** — FIX — value 4 — effort M — risk low — category: waste
  Why: dropped items include "done in another task", "no change needed" and "researched: already handled". For a FIX, Foreman would first write or run a failing check and, if it passes, close the task as already fixed with the evidence.
  Done when: a FIX whose symptom doesn't reproduce closes as "not reproducible at HEAD" with the command output and no edits. The test uses a stale-bug fixture.

- **Estimate time and cost before starting a task** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: tasks carry sizes (S/M/L), and cost and time data already exist per task. Assumption: the user would like to know whether a task is a 3-minute or a 40-minute job before queueing it.
  Done when: `fm task start` prints "typically 4–9 min, $0.30–0.80, from N similar tasks". With fewer than 5 similar tasks it says "no estimate".

- **Protect the user's own edits** — FIX — value 4 — effort M — risk low — category: pair work
  Why: steers show a scratchpad write triggering a note, and another task's dirty files blocking a close. A human editing in the same tree is the same problem. Foreman would mark files it didn't write as the user's and never stage, revert or count them.
  Done when: a hand-edited file stays out of the commit, scope and test selection of the agent's task, and the close receipt lists it as "yours, untouched".

- **Search past decisions with `fm why <path or phrase>`** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: task records, DONE-WHENs, steers and drops hold the reasons behind the code (for example "dropped: conflicts with never-idle design"). Today they surface only by digging through history.
  Done when: `fm why fmambient` returns the tasks that changed it, each with its one-line rationale and any related dropped idea. Results are ordered newest first.

- **Carry lessons across projects** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: T-0217 gives lessons a confidence score but they stay in one repo. A user running Foreman on several projects relearns the same habits. Assumption: they have several projects. Only lessons above a confidence threshold would be shared, with an opt-in setting.
  Done when: a new project's first session recalls a user-level lesson that was learned elsewhere, and it is marked as imported. With the setting off, nothing crosses projects.

- **Undo a shipped task in one command** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: shipping is the user's most frequent action and nothing in the open work lets them back one out. Assumption: shipped tasks are merge or squash commits that revert cleanly. `fm unship Tn` would revert exactly that task's commits and reopen the task with the reason.
  Done when: after `fm unship T-x`, main no longer holds T-x's change, the gates are green, and T-x is open with a note.

- **Batch questions into one sitting (wild)** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: assumption: mid-task questions stall work. Foreman would park the asking task, move to unblocked ones, and collect every question into one list the user answers in a minute (for example choosing from numbered options). Each answer resumes its task.
  Done when: three tasks that each need an answer produce one question sheet. Answering it resumes all three, and unblocked tasks progressed in between.

- **Run a ten-minute paper-cut scan on a repo that hasn't adopted Foreman (wild)** — FEATURE — value 3 — effort L — risk med — category: onboarding
  Why: the pack shows a mature queue, but the first minutes in a new repo decide whether someone keeps it. A read-only scan would run the repo's own tests and linters and file the top five proven problems as ready-to-run tasks. It changes nothing in the repo.
  Done when: running it on a sample repo outputs five tasks, each with a failing command shown, and `git status` is clean afterward.

- **Turn issues into tasks automatically once published (wild)** — FEATURE — value 3 — effort L — risk high — category: community
  Why: T-0352 plans a public GitHub release with CI. Assumption: that brings external issues. Foreman would triage each into a draft task with a reproduction attempt and reply with the result only after the owner approves the wording.
  Done when: a labelled issue yields a draft task with a reproduction log. Nothing is posted to GitHub until the owner approves it.
