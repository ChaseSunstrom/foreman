# Brainstorm — lens: bold bets

- **Issue a done-warranty with sentinels** — FEATURE — value 4 — effort M — risk low — category: finish
  Why: the goal says it must know when it is "actually done". Soak and maintenance ideas exist, but none makes "done" expire. Assumption: the night tick can re-run probes on a schedule.
  Done when: a closed goal records a 14-day warranty, and a dependency bump planted on day 3 reopens it as a warranty claim row with the cause named.

- **Ask by value of information** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the pack caps questions at three but doesn't rank them. Assumption: two cheap plan drafts per candidate answer are affordable. Ask only when the drafts differ by more than a set number of rows.
  Done when: on a fixture goal with 6 candidate questions, only those whose answers change at least 3 rows are asked, and the log shows the diff counts.

- **Calibrate taste with a paired-output deck** — FEATURE — value 4 — effort M — risk low — category: quality
  Why: subjective rows like "polished" or "feels fast" have only a rubric idea behind them. Assumption: the user will do about 8 quick A/B picks once per goal.
  Done when: after 8 picks, a subjective row gains rubric lines quoted from the picks, and a cold child scores 2 held-out pairs in agreement with the user.

- **Compile an unattended-safe shift from the plan** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the lens's central ask is carrying a plan across days. Charters and branches exist, but no per-row classifier of probe-able, reversible and budgeted rows picks the overnight set. Assumption: row metadata can carry those three flags.
  Done when: at day-end, `fm goal shift` lists only rows with all three flags, and a planted row lacking a probe is excluded with the reason shown.

- **Keep an obligations ledger across every stop** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: "merely stopped" is the failure the goal names. A typed stop reason says why, but nothing forces the next resume to discharge what was left unverified. Assumption: stops write structured obligations, not prose.
  Done when: killing a session mid-row leaves an obligation, and the next resume refuses to mark that row done until it is discharged or restated.

- **Add non-code goal kits** — FEATURE — value 3 — effort L — risk med — category: scope
  Why: assumption: users bring migrations, docs sites, data pipelines and releases, not only features. Each kit ships a finish-oracle template such as row counts match, links resolve or the tag artifact verifies.
  Done when: a "migrate DB X to Y" goal gets a plan with a row-count parity probe and closes only when it passes on a fixture.

- **Gate pushes on row coverage** — FEATURE — value 3 — effort S — risk low — category: scope control
  Why: assumption: scope creep is invisible in commits. Block or warn when a commit maps to no live row, naming the nearest row or offering to add one.
  Done when: committing an unrelated edit during a goal prints "maps to no row" and logs a growth entry.

- **Run a nightly model league that learns row routing** — FEATURE — value 3 — effort L — risk med — category: cost
  Why: duel data exists (T-1231, T-1266). Three cheap models attempt tomorrow's row in sandbox lanes, and an Elo table per row type picks the builder. Assumption: sandboxed lanes cost under a set dollar cap.
  Done when: after 10 nights the table routes a row type to a model and the report shows pass and cost per model.

- **Wild: backcast the finished state into history** — FEATURE — value 3 — effort M — risk low — category: plan completeness
  Why: wild. A tool-less child is given only the finished-version description and writes the commit sequence that would reach it. Rows it invents that the plan lacks become gap candidates. This differs from reverse-planning an existing repo because it needs no finished code.
  Done when: on a fixture goal with 2 deliberately omitted rows, the backcast names at least 1 of them.

- **Wild: let the goal die publicly in a post-mortem if it stalls** — FEATURE — value 2 — effort S — risk low — category: honesty
  Why: wild. After 7 idle days a goal writes its own one-page post-mortem, giving what ran, what was proven, what blocked and the cheapest restart, then archives itself. The user can revive it with one word.
  Done when: a goal idle for 7 fake-clock days produces the page and moves to archived, and `fm goal revive` restores it.

- **Wild: replay a stranger's repo history as a goal exam** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Why: wild. Take an open-source repo at a tagged release, set the next release's changelog as the vague goal, and score the plan's rows against what actually shipped. Foreman's own captured and Foreman-authored data is not used, which fits the steer to rely on signals Foreman didn't author.
  Done when: for 5 public repos, the plan reports row recall and precision against the next release's changelog, with the denominators printed.

- **Show a one-line "what would change this plan" on every goal page** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: the user trusts plans more when the plan names its own tripwires, such as a changed dependency, a failed spike or a new steer.
  Done when: a goal page lists at least 2 tripwires, and simulating one marks the plan stale with that cause.

Next question: Which kind of goal has the user actually started with a vague sentence, and how did each finish: closed, shrunk, abandoned?
Next question: What does a returning user need within 10 seconds of resuming after a long gap, and which of these ideas delivers it?
