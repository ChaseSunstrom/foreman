# Brainstorm — lens: user value

- **Show "what you asked vs what landed" at ship** — FEATURE — value 5 — effort M — risk low — category: close-out
  Why: the user's words are one-line asks ("Ship T-1987 to main"); the commit subjects are long, task-id lists (T-1998, T-1999, T-2000). Evidence: they never see whether each ask became a change. Assumption: they skim, not read, commit text.
  Done when: `fm ship Tn` prints one line per original ask in the task (ask → file:line changed → proving test) and flags any ask with no matching change.

- **Collapse follow-up sibling tasks into the parent ask** — FEATURE — value 5 — effort M — risk med — category: queue
  Why: the asks come in runs of near-twins (T-1994/1995/1996, T-1998/1999/2000/2001 around `run.py` -k and docs-impact "did you mean"). Each is a separate ask, task and ship.
  Done when: when a new capture shares a module and a message family with a task closed in the last day, `fm` offers to reopen it as an amendment, and accepting produces one task, one ship.

- **Answer "is Foreman helping me?" with measured numbers** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: T-1231 (beats Claude Code on the duel) and T-0866/0867 (bench, scorecard) are all deferred with "needs cases"; no user-visible proof the ceremony pays off. Assumption: the user's own closed tasks can serve as cases.
  Done when: `fm worth` lists, for the last 30 days, tasks where a gate or proof caught a defect before close, versus time and tokens spent on ceremony, in under 10 lines.

- **Let a failing refusal offer to fix itself** — FEATURE — value 4 — effort M — risk med — category: refusals
  Why: a run of recent FIXes are dead-end messages ("no test matches test_run", docs-impact path, `-k core_integrity` vs `CoreIntegrity`, "commit it through a task" for the task's own scope). Each cost an ask plus a ship.
  Done when: a refusal that has one unambiguous correction prints it as a runnable command (`fm retry --apply`), and the test suite fails if any refusal under test has neither a correction nor a named reason.

- **Cut the cost of a one-line FIX to one cycle** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: many asks are single-file FIXes with a named test, yet each goes through the full plan → prove → gates → ship cycle plus a separate "Ship Tn to main" ask.
  Done when: a FIX scoped to one file with a named failing test closes and ships from one command, with a measured wall time below half the current path (bench output attached).

- **Keep "Ship Tn" from being a separate ask** — FEATURE — value 4 — effort S — risk low — category: ship
  Why: "Ship T-1982/1987/1992/1996/2001 to main" appears five times in the recent asks, each right after the previous task closed; assumption: they always follow a green close.
  Done when: a standing setting `ship_on_green` ships a closed, green task without being asked, and the setting is off by default and logged in the receipt.

- **Park a half-formed ask without losing it** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the asks get cut at 90 characters, drop `@path`-only lines, and mis-capitalize commands; the user's intent is lost at capture. Assumption: they would rather paste loosely and have it kept verbatim.
  Done when: every captured item stores the pasted text verbatim and `fm intake show Tn` prints it byte-identical, whatever title shaping did.

- **Explain a steer the first time it recurs** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: steers ("ignore edits outside the project", "drop `_theirs`", "AND rule fails it") repeat the same class of mistake (scope and ownership of dirty files); the user corrected each one separately.
  Done when: the second steer on the same class makes Foreman name the earlier one and propose a single invariant test covering both.

- **Wild: Give the user a "Friday diff" of what Foreman refused to do for them** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: assumption: refusals that were right feel like friction; seeing the count of bad commands, unproven closes and out-of-scope edits blocked in a week makes the cost visible as value.
  Done when: `fm week` lists each refusal with the command it stopped and whether the user later overrode it.

- **Wild: Let the user type the next ask as a half-sentence and have it autocomplete from the last 20 asks** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: the ask stream is highly patterned ("FIX: … @path> DONE-WHEN: …"). Assumption: the user would take a draft of the template filled from context.
  Done when: typing `fm add "fix: ..."` with a path prints a complete block with a drafted DONE-WHEN the user accepts with one key.

- **Wild: Open a "while you were away" page after any loop run** — FEATURE — value 4 — effort M — risk low — category: return
  Why: the forever loop runs unattended, and stops like "2 dry rounds" give little. Assumption: the user returns to a long log.
  Done when: a stopped loop writes a single page: tasks landed, tasks held and why, what needs the user, and one suggested next ask.

- **Wild: Say "nothing to do" honestly and stop spending** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: the loop's dry-round logic keeps being patched (budget-limited rounds counted dry), implying it spends where nothing is left; drops show most captured ideas are duplicates.
  Done when: when the queue holds only deferred or blocked items, the loop exits with a one-line reason and zero model calls in that round.
