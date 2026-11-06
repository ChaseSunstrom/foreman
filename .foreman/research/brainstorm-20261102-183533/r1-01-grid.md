# Brainstorm — lens: grid

**Cells left empty:** web UI × unattended × unsafe (the UI only reads, and the stale-tab and retype-to-confirm ideas already cover its actions). Also user × slow (the 10k-task render budget is already listed) and other agents × unsafe (spawn-depth, capability-token and credential-allowlist ideas cover it). Phone, voice and car cells are empty because the pack's surfaces line names only the web UI.

- **Score every dissent against the task's outcome** — FEATURE — value 5 — effort M — risk low — category: calibration
  Cell: CLI × agent × wrong.
  Why: the Mission names "dissents scored against outcomes" as a carried gap. Cold reads and lenses dissent, but nothing joins a dissent to what the task did later. Assumption: dissents are recorded as text with a task id.
  Done when: `fm outcomes --dissents` prints per-source counts of dissents confirmed (a reopen or a revert on the same task), refuted, or still open at 14 days. A planted fixture with one of each prints three different rows.

- **Refuse a brief whose Exam lacks `outcome:` and `live:` lines** — FEATURE — value 5 — effort S — risk low — category: intake
  Cell: brief × agent × unclear.
  Why: the Mission says every brief's Exam names an outcome measure and a live-state reading. Today that's prose, so the check is easy to skip.
  Done when: intake of a brief missing either line exits nonzero and prints the missing key with an example line. A brief with both lines files.

- **Snapshot the live-state reading at filing and diff it at close** — FEATURE — value 4 — effort M — risk med — category: proof
  Cell: brief × unattended × wrong.
  Why: an outcome measure that reads the same before and after proves nothing. Assumption: the live reading is a command with a printable value.
  Done when: filing stores the reading's value, and the close receipt prints before → after. A planted no-op change prints "unchanged: measure may be vacuous".

- **Classify Exam live-state commands as read-only through the guard before filing** — SECURITY — value 4 — effort S — risk low — category: guard
  Cell: agent × unsafe.
  Why: a "live reading" is a command the unattended drive will run, and a brief could smuggle a mutating one into it. Assumption: the guard can already classify read-only shapes.
  Done when: a brief whose `live:` is `rm -r x` or `git push` is refused with the guard's reason. `fm status --json` is accepted.

- **Print the three nearest existing things as a canary beside every "not built" claim** — FEATURE — value 4 — effort M — risk low — category: grounding
  Cell: agent × wrong.
  Why: the Mission's "canaries near the idea" gap. The user keeps dropping ideas as "already built" (see the dropped list). The idea list holds an exact-grep canary, but no neighbour search by the idea's own nouns.
  Done when: each brief's grounding block lists up to three file or verb hits from the idea's nouns and their stems, plus the command that found them. A planted already-built idea surfaces its twin in that list.

- **Show the request's grid on its web page: rows are surfaces and actors, columns are failure modes, with filled, empty and n/a cells** — FEATURE — value 5 — effort M — risk low — category: web UI
  Cell: web UI × user × missing.
  Why: "says what it left out" has no home. The user can't see what was covered without reading the Mission file. Assumption: coverage.md cells are machine-readable.
  Done when: the Mission page renders the grid, each empty cell shows its reason, and a screenshot test shows a cell going from empty to filled when a brief lands.

- **Write a left-out receipt at the end of every unattended Mission** — FEATURE — value 5 — effort S — risk low — category: reporting
  Cell: unattended × missing.
  Why: the user is away, and the only record of omissions is whatever the run chose to say. Assumption: the drive can enumerate empty cells at close.
  Done when: the run's final report ends with "Left out (N)", one line per cell with a reason code (out of scope, blocked on user, dry, unreached). A run with a planted unreached cell lists it.

- **Carry each left-out cell into the next Mission's pack as an aged seed** — FEATURE — value 4 — effort S — risk low — category: continuity
  Cell: other agents × missing.
  Why: the Mission itself is built on "carried gaps", but they are handed over by hand. This is the same rule as the "Seeds retry items a new capability may unblock" steer.
  Done when: opening Mission N+1 lists unfilled cells from Mission N with their age in generations. Filling one removes it.

- **Show each left-out item on the Genesis site with a plain reason and who can unblock it** — FEATURE — value 3 — effort S — risk low — category: site
  Cell: site × user × unclear.
  Why: omissions with reasons only the tower understands read as neglect. Assumption: site data already carries per-Mission fields.
  Done when: the published Mission page has a "What this left out" section, and a cold-read check finds no tower-only jargon in it.

- **Mark an Exam reading "stale" when it exceeds a deadline instead of passing or failing** — FIX — value 3 — effort S — risk low — category: proof
  Cell: brief × agent × slow.
  Why: a live-state command that hangs on an unattended night either blocks the drive or gets skipped silently.
  Done when: a `live:` command that sleeps past its limit records "stale (timed out Ns)" in the receipt, and the task does not close as proven.

- **File a dissent pair automatically when two lenses recommend opposite things about the same cell** — FEATURE — value 3 — effort M — risk med — category: brainstorm
  Cell: other agents × wrong.
  Why: opposite ideas are currently deduplicated or merged, which hides a real disagreement. Assumption: ideas are tagged with a cell.
  Done when: two fixture ideas that conflict on one cell produce a single dissent record linking both, and `fm outcomes --dissents` lists it.

- **Watch what you left out (wild)** — FEATURE — value 4 — effort L — risk med — category: tripwire
  Cell: unattended × missing.
  Why: assumption: an omission is only dangerous if something later touches that cell.
  Each left-out cell gets a zero-token tripwire: a keyword, file or verb that, when it appears in a later user ask or diff, resurfaces the omission with its reason.
  Done when: a planted omission fires on a matching later ask and stays silent on an unrelated one.

- **Write an angry user review for each empty cell, ranked by sting (wild)** — FEATURE — value 3 — effort M — risk low — category: prioritisation
  Cell: web UI × user × unclear.
  Why: assumption: ranking omissions by the user's likely annoyance beats ranking by effort.
  A tool-less child writes a one-line complaint per empty cell from the user's words alone, and a second child scores the sting.
  Done when: the grid page sorts empty cells by sting, and two runs agree on the top three.

- **Replay the last Mission with its overruled dissent applied (wild)** — FEATURE — value 4 — effort L — risk high — category: counterfactual
  Cell: CLI × agent × wrong.
  Why: assumption: scoring a dissent by outcome is slow, and a replay shows what it would have changed.
  Take a dissent that was overruled, re-run the Mission's brief set with it applied on a scratch copy, and diff the resulting slate.
  Done when: `fm dissent replay D-N` prints a slate diff, and an unrelated dissent yields an empty diff.

Next question: which carried gaps does a Mission close mark as met without an outcome reading, and what would each one have shown?
Next question: when the grid page and the left-out receipt disagree about an empty cell, which does the user trust, and is that written down anywhere?
