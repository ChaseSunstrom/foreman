# Brainstorm — lens: unspoken needs

Answering earlier questions first. Which outputs would the user only notice missing after it cost them a task? The commit-to-goal link, the steers added mid-goal and the promises made in old reports. Do the cells' probes run on other harnesses? Assumption: most lean on Claude Code hooks, so a cell should say so.

- **Stamp goal and row trailers on every commit** — FEATURE — value 4 — effort S — risk low — category: recovery
  Why: assumption: ledger, baton and repo disagree after a kill ("Reconcile baton, ledger and repo" is listed). A `Goal: G-n Row: r` trailer lets `git log` rebuild which rows landed, with no extra state.
  Done when: deleting the goal's progress file and running resume rebuilds the closed-row list from trailers, matching the original.

- **Show steers added since the plan was written** — FEATURE — value 4 — effort S — risk low — category: multi-day goals
  Why: the steers list is long and grows during a multi-day goal (several are dated 2026-10-31 and 2026-11-01). A plan made on day 1 can quietly break a day-3 steer.
  Done when: resuming a goal whose plan predates a new steer prints that steer and the plan rows it touches, in a test with a planted steer.

- **Track promises made in past final reports** — FEATURE — value 4 — effort M — risk med — category: follow-through
  Why: Foreman's "later", "follow-up" and "next" lines in reports and commit messages are only read by the user. The 28 "Later from T-07xx" bundles show promises piling up unowned. Assumption: they are parseable with a simple phrase pass.
  Done when: a fixture report containing "I'll follow up on X" files a deferred item for X, once, and it appears in the next `fm next`.

- **Learn the user's good-enough point** — FEATURE — value 3 — effort M — risk med — category: finish line
  Why: the user's steers repeatedly shift effort to "finish round 1" and away from optional work. Their historical stopping points (the share of contents rows done when they moved on) could set the default must/should cut line. Assumption: enough closed goals exist; if not, say "too few".
  Done when: `fm goal` prints a suggested cut line with the N closed goals it came from, or abstains when N < 5.

- **Keep in-flight child output off tmpfs-only paths** — FIX — value 3 — effort S — risk low — category: durability
  Why: this very run works in `/run/user/1000/fm-children-1000`, which a reboot wipes. A multi-day goal's running lanes should not lose output that way. Assumption: lane outputs can live there for hours.
  Done when: a simulated wipe of the children dir during a lane leaves a recoverable copy under state, and resume names the lost lane.

- **Back out a whole goal with one gated revert** — FEATURE — value 4 — effort M — risk med — category: reversibility
  Why: goals land as many commits. Per-ship revert is already listed, but the user's real undo is "this whole goal was wrong". Trailers (idea 1) make the set computable.
  Done when: `fm goal revert G-n` prints the revert plan for exactly the trailer-tagged commits and refuses to run without a grant.

- **Record estimate versus actual per row** — FEATURE — value 3 — effort M — risk low — category: planning accuracy
  Why: no idea above feeds actual row effort back into S/M/L sizing, so decomposition never improves. A heuristic ships only behind a backtest (Lesson from Missions 3-6), so state the bar first.
  Done when: finished goals write minutes and tokens per row, and a held-out check shows the size label predicts the cost order better than chance.

- **Make an overrun row decide for itself** — FEATURE — value 3 — effort S — risk low — category: scope control
  Why: assumption: a row can run for hours past its estimate. The user wants no mid-run asks, so at 3× estimate Foreman should split or drop the row itself and log it with `fm decide --kind costly`.
  Done when: a planted row exceeding 3× estimate produces a split or drop decision record and no question to the user.

- **Hand a goal to a person as one page** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: handoff between harnesses is listed, but not to a human colleague or the user's later self. Assumption: teams or future-me read it without the ledger.
  Done when: `fm goal brief` outputs a ≤1-page markdown with done rows, open rows, user-only items and how to resume, free of Foreman jargon.

- **Measure the cost of resuming** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: crash and compaction survival is the capability's promise, but only correctness is checked, not what a resume costs. A resume that re-reads 200k tokens is a hidden tax.
  Done when: the kill-and-resume drill records tokens and seconds to the first useful action, and the lean ratchet carries it.

- **Wild: price each row by its salvage value** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild. Beyond "order so any stopping day leaves something runnable", each row records what stays useful if the goal stops now, so a cut is chosen by value left, not by order.
  Done when: the plan page lists rows with a salvage line, and a simulated stop at row k reports the usable state.

- **Wild: seal a regret list at goal start and score it at finish** — FEATURE — value 3 — effort M — risk med — category: blind spots
  Why: wild. A tool-less child that sees only the goal text writes three things the user will wish were included. At finish they are scored against the user's actual first follow-up ask, which gives an external signal Foreman didn't author.
  Done when: the sealed file's hash is recorded at start, and the finish report shows the hit or miss against the next ask.

- **Wild: read the night aloud locally** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. The night tick's one-line digest is spoken by a local text-to-speech tool with nothing sent out, so the user hears the goal's state while making coffee. Assumption: a local TTS engine exists; otherwise it prints.
  Done when: with the setting on and an engine present, a tick produces an audio file from the digest; with it off, nothing is generated.

Next question: Which fields of the goal file would a human ever need to edit by hand, and does any verb let them without breaking the checks?
Next question: When two of the 58 cells turn out to be the same capability, who decides which survives, and is that decision itself recorded?
