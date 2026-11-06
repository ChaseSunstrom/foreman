# Brainstorm — lens: unspoken needs

**Answers to earlier questions (my lens):**
- *Outputs the user would only miss after it cost a task:* the "where we were" summary after a crash or compaction, the stop reason, and the list of things only the user can do. None of the three is shown in the pack as a first-class output.
- *Cells that quietly depend on Claude Code:* any cell about hook-driven resume or the status line. Goal state held only in the baton or session memory has no equivalent on codex, gemini or opencode.

---

- **Triage the 58 cells into existing, gap or n/a, with a grep proof, before writing any prose** — CLEAN — value 5 — effort S — risk low — category: coverage
  Why: Lessons from Missions 3-6 say most of #2, #3, #11 and #12 was already built. The templating rule forbids reused phrasing.
  Done when: a triage file has 58 rows, each tagged existing/gap/n/a with a resolvable path, task id or counterexample-search note, and the sweep's templating check passes.

- **Compute "finished" as a verdict with a typed stop reason** — FEATURE — value 5 — effort M — risk med — category: goal-state
  Why: Gen-0 #4 says the goal "knows when it's actually done rather than merely stopped", yet the pack shows no done/stopped distinction in the user's asks.
  Done when: `fm goal status` prints `done` or `stopped:<one of five reasons>` computed from files only. A premature-finish trap fixture, where a row was closed without evidence, yields `stopped`.

- **Print a fixed ten-line "where we were" on resume, reconciled from baton, ledger and repo** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: The blind-spot list names "baton, ledger and repo disagree after a kill". Pillar 7 means nobody is there to ask.
  Done when: after a kill at each of 5 boundaries, resume prints the same ten lines, names any disagreement, and picks the next row as a pure function of the files.

- **Tag every cell with the harness it was probed on and its backtest class** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: Questions left ask which cells depend on Claude Code and which have too little history to backtest. The standing rule says Foreman isn't specific to Claude Code.
  Done when: each cell carries `harness=` and `class=measured|planted|n/a`. The sweep fails any cell with neither.

- **Fail the sweep on a cell whose cited path no session path reaches** — FIX — value 4 — effort M — risk low — category: reach
  Why: The reach steer says a capability must be called by a real session path. Earlier asks also worry about outputs nothing reads.
  Done when: a test cell citing a verb with no caller turns the sweep red, and a real cell stays green.

- **Make the goal's user-only items one running list, predicted at plan time** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: Pillar 7 puts "what only the user can do" in the final report, and the user would otherwise discover it at the end of the run.
  Done when: planning a vague goal writes a `user-only.md` listing predicted items. The final report diffs predicted against actual.

- **Flag goals that finish by shrinking, with a scope ledger** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: Lean-substance and proof-before-presentation steers show the user distrusts self-reported completion. A goal can hit "done" by quietly cutting rows.
  Done when: closing a goal prints rows added, cut and deferred. A fixture that cuts 30% of its rows gets `finished-by-shrinking`.

- **Add a read-only Goal page to the web UI (rows, evidence, stop reason, stale banner)** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: Web UI is the only surface in this mission, and the cell grid has surface columns for it. Goal state currently lives in files.
  Done when: the page renders a fixture goal's rows with evidence, shows an "as of" age, and has empty, loading and error states.

- **Re-run each filled cell's probe at sweep time so rotted cells turn red** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: A question left asks whether the sweep checks that a cell's cited path still fires, not only that the file exists.
  Done when: renaming a cited function in a scratch copy turns that cell, and only that cell, red.

- **Close a goal with a "You said / We built / Not proven" receipt** — FEATURE — value 3 — effort S — risk low — category: finish
  Why: The user keeps asking for proof before presentation. Their own words are the only acceptance text they can judge quickly.
  Done when: finish prints each phrase of the goal beside its row and evidence, with an explicit unproven line.

- **Wild: delete the goal file and rebuild it from git, tasks and the ledger** — FEATURE — value 3 — effort L — risk med — category: crash-safety
  Why: wild. "Across crashes and compactions" is only believable if the file is disposable.
  Done when: a rebuilt goal's rows and next-row pick equal the original's in a test.

- **Wild: nightly canary goal fed by the user's last 40 captured asks as vague goals** — FEATURE — value 3 — effort M — risk med — category: night tick
  Why: wild. It tests decomposition on real vagueness, not on fixtures the tower wrote.
  Done when: the night tick plans 5 asks, scores completeness against the user's actual follow-ups, and logs one digest line.

- **Wild: seal a one-sentence hope at goal start and read it back at finish** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. It surfaces the need behind the ask, which the user rarely states.
  Done when: the sealed sentence is stored hash-stamped at plan time and printed on the finish card beside the verdict.

Next question: Which cells would be satisfied by a harness-neutral goal file, and which require hooks that only Claude Code has?
Next question: When a goal stops, what does the user do first, and does any surface answer that without reading a file?
