# Brainstorm — lens: user value

- **Reject duplicate or false-premise briefs at capture** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: Four recent drops were "already covered" or "premise false on replay", so cycles went into briefs a quick check would have stopped. `fm task new` would grep the code, open and dropped briefs and the verify paths, then print the nearest match and the evidence before filing.
  Done when: capturing a brief whose idea matches an existing dropped one prints that brief's id and drop reason and asks for `--force` to file it.

- **Run the tests mapped to the diff for in-loop proofs, the full suite at close** — PERFORMANCE — value 4 — effort M — risk med — category: verification
  Why: `fm map` already holds a tests→src map, and CI timing was just a problem (T-1277 and the CPU-bound fix). Mid-task proofs on a 229-file test tree don't need the whole suite.
  Done when: editing `fmagents.py` makes the step proof run `test_agents.py` only, the close gate runs everything, and a bench log shows the saved seconds.

- **Quarantine flaky verify commands before they count as evidence** — FIX — value 4 — effort M — risk low — category: trust
  Why: assumption: with CI red on timing bounds and macOS differences, a proof that passes once may not pass again. A first-pass verify that later fails undermines "proved with commands it actually ran".
  Done when: a verify that flips between pass and fail across two runs is marked `flaky`, can't close a criterion alone, and the note names the flipping test.

- **Learn from the user's post-close edits** — FEATURE — value 5 — effort L — risk med — category: learning
  Why: Today lessons come from Foreman's own failures (T-0217). When the user hand-edits lines a closed task touched, that is the clearest signal Claude missed what they wanted. Assumption: the closing commit and the next human commit are separable by author or by trailer.
  Done when: editing lines from a closed task's commit proposes a one-line lesson candidate in `fm lessons`, tied to that task id, and it is dropped if the user rejects it.

- **Check the diff against the plan's declared files at close** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: The user asks for "one task at a time". Edits outside the plan's files are the usual way that rule breaks silently. It is cheap to compute from the plan and `git diff --name-only`.
  Done when: closing a task that touched an undeclared file lists it and requires either a plan amendment or `--park` to a side note.

- **Explain any note: `fm why-note`** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: Edit-time notes reached 130 KB in one session, with recall notes and ambient test lines the biggest parts. A user or model who sees a note can't tell which rule, lesson or hook fired it. Assumption: hook notes can carry a short source tag cheaply.
  Done when: `fm why-note` on the latest note prints its source rule, trigger and the task or lesson behind it.

- **Promote lessons that recur across the user's repos to a global lesson set** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: Lessons are per project. Assumption: the same mistakes (tests named wrongly, piped output, guard collisions) recur across the user's repos. A lesson seen in three repos would be offered once as global, with consent.
  Done when: a lesson recorded in 3 repos is offered by `fm lessons --promote`, and a fourth repo's recall includes it with its origin shown.

- **Add a plain-text pane mode (no color, no motion, screen-reader order)** — FEATURE — value 3 — effort M — risk low — category: accessibility
  Why: Open item T-1217 (pane background color) and the terminal-colour ideas show the pane is tuned to a single look. A mode that follows `NO_COLOR` and prints stable, linear lines also helps dumb terminals and logs.
  Done when: with `NO_COLOR=1` the pane prints no escape codes except cursor control, and the stage and work-bar information is present as text.

- **Post a proof-carrying PR description and a CI check that re-runs it** — FEATURE — value 4 — effort M — risk med — category: collaboration
  Why: The tests badge shows CI exists, and `fm ship` is already proposed. Teammates still can't see why a change was trusted. The PR body would list each criterion with its recorded command, and a small Action would re-run those commands.
  Done when: a PR from a closed task carries a criteria table, and the Action fails if any recorded verify no longer passes on the PR head.

- **Wild: Red-team each close with a hostile test writer** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: wild. A read-only sub-agent gets the diff and the criteria and a capped budget. It tries to write one failing test, and the close either survives or opens a follow-up. This fits the "harder tasks where verification matters" push and the T-0034 audit idea. Assumption: it costs about a few cents on Haiku.
  Done when: seeded bugs in three fixture tasks are each caught by a generated failing test, and clean fixtures produce "no break found" in at least 9 of 10 runs.

- **Wild: A session scrubber in the web UI** — FEATURE — value 3 — effort L — risk low — category: replay
  Why: wild. The hook replay already exists for tests. A timeline slider in the web UI would show the plan, each proof, the notes injected and the cost at that point, so a user can read a three-hour unattended run in minutes.
  Done when: dragging the slider to any event shows the task state, the injected bytes and the cumulative cost, and matches `fm cost` at the end.

- **Wild: A brief court that cross-examines each new brief before it is built** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: wild. The same pattern of dropped briefs (false premise, already built, wrong test name) suggests a cheap adversary. One Haiku call would try to argue "this is already done or won't help", citing paths. Assumption: the call can be capped at a few cents and skipped for small briefs.
  Done when: replayed against the last 20 dropped briefs, it flags at least 12 of them with a correct reason while passing the last 20 built ones.
