# Brainstorm — lens: capability map

I found few new gaps: the pack's idea list already covers nearly every standard technique in this space (decision tables, FMEA, EARS, assurance cases, pre-mortems, pairwise covering). The ten below add mechanisms the list lacks, and the last three are wild.

- **Classify each brief as a one-way or two-way door** — FEATURE — value 4 — effort S — risk low — category: rigor scaling
  Why: assumption: the pack scales breadth by task size and autonomy by value-at-risk, but nothing scales Exam strictness by whether the change can be cheaply undone. Amazon's one-way/two-way door split is the missing axis. A reversible doc tweak needs one reading. A ledger-format or grant-spend change needs the full Exam card and a user ask.
  Done when: `fm genesis check` fails a brief with no `door: one-way|two-way` line, and a one-way brief with fewer than two Exam readings.

- **Storyboard the request from first use to removal day** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: assumption: the grid has rows (surfaces, actors) and columns (failure modes) but no time axis. A storyboard walks one user through first run, week one, a bad day, an upgrade and uninstall, and each step becomes a cell. The pack's "old data and time column" is one column, not a walk.
  Done when: a Mission page for a test request lists at least five ordered storyboard steps, and each step is linked to a brief or a stated omission.

- **Name three rabbit holes per L brief and settle them at close** — FEATURE — value 3 — effort S — risk low — category: estimation
  Why: Shape Up's "rabbit holes" are the places effort will blow up. The pack forecasts cost (`forecast duration and cost`) but never names the specific traps. At close, compare the named traps to the files that actually consumed the effort, and record which traps were real.
  Done when: closing an L task prints `rabbit holes: N named, M hit` from the brief and the task's diff stats.

- **Run co-filed Exam readings in shuffled order and flag order dependence** — FIX — value 3 — effort S — risk low — category: measure integrity
  Why: assumption: one Mission files several briefs against shared state (ledgers, task queue). If brief A's fix shifts brief B's baseline, B's reading passes or fails by build order. The pack shuffles test order and runs readings cold vs warm, but never runs a Mission's own readings against each other.
  Done when: a planted pair of briefs whose readings interact is flagged by `fm genesis check`, and an independent pair is not.

- **Lint Mission prose for quantifiers with no denominator** — CLEAN — value 3 — effort S — risk low — category: honesty
  Why: the pack has "print the denominator on every nothing found" for tool output and bans "left out: nothing". It does not lint the Mission page's own words. "All surfaces", "every verb", "never" and "exhaustive" should each cite a count (such as "7 of 7") or be struck.
  Done when: a Mission file containing "every surface" with no `N of N` fails the lint, and the same sentence with `(6 of 6)` passes.

- **Record a Brier score on the Mission's own omissions** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: combination of "settle left-out against later asks" and "seal a drop-rate forecast". Each left-out cell gets a sealed probability that the user asks for it within 30 days. Settlement then scores how well calibrated the Mission's sense of what mattered was, not just whether it was exhaustive. A high hit rate on cells rated "unlikely" is a blind spot in a form that can be measured.
  Done when: `fm outcomes` prints an omission Brier score for a settled Mission, computed from stored probabilities and the ask ledger.

- **Pin the Exam's environment assumptions in the brief** — FEATURE — value 3 — effort S — risk low — category: reproducibility
  Why: assumption: the pack stamps readings with host facts after the fact. It does not make the brief declare up front what it needs (Arch, a hardened kernel, no `claude` on PATH, a given uid). A cold replay can then say "not applicable on this host" rather than failing.
  Done when: a brief declaring `env: needs-systemd` returns "skipped: host lacks systemd" in a container without it, and counts as the third state, not pass.

- **Diff the Mission's claimed reach against the files it touched** — CLEAN — value 3 — effort S — risk low — category: scope integrity
  Why: assumption: briefs name files in prose, but the claimed reach is never checked against the commit. Report files changed that no brief named (scope creep), and named files left unchanged (an unmet claim).
  Done when: closing a Mission prints `unnamed files touched: N; named files untouched: M`, and a planted extra file shows up.

- **(wild) Keep a "second-best interpretation" shadow task per Mission** — FEATURE — value 4 — effort M — risk med — category: ambiguity
  Why: assumption: the pack records which scope width was taken and ranks widths, but never builds the runner-up reading. An unattended Mission could drop the second-most-likely reading of the request into a scratch worktree as a small draft. If the user's next ask matches it, it is waiting; otherwise it expires in 3 days.
  Done when: a Mission with an ambiguous request leaves a `shadow/` branch with a one-line summary, and it is deleted after the expiry with a ledger record.

- **(wild) Let the user grade lenses by the "ah" feeling: one key per idea, trained over generations** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: the pack scores lenses by hindsight and fertility but never by felt surprise. One keypress, "I hadn't thought of that", per idea costs the user a second. After a few generations, the lens budget shifts towards the lenses that surprised them, not the lenses whose ideas shipped.
  Done when: `fm brainstorm` weights next-run lens budgets by the stored "ah" counts, and `fm doctor` shows the per-lens totals.

- **(wild) Quote a Mission's omissions back to the user as a dated letter on the day each cell expires** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: n/a cells already expire, and the expiry is silent. A letter ("on 2026-12-01 you stopped caring about X; still true?") written in the user's own phrasing, with a one-key renew or drop, turns expiry into a check-in.
  Done when: an expired n/a cell produces a card at the next session start with the cell's original reason and two keys, and the keys write ledger records.

Next question: which of these ten has a reading Foreman could take today with no model call, and which depend on a child judging, so that cost per Mission is known before any is built?
Next question: when the user ignores a Mission page for a whole generation, is that trust in the Mission, or too much text to read, and what one existing record would tell the two apart?
