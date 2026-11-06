# Brainstorm — lens: reliability

- **Make cell fills atomic and resumable via a fill journal** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the 58-cell fill runs across parallel lanes and many hours; the pack shows kills, compactions and usage-limit pauses as standing concerns, and coverage.md is one shared file with concurrent writers (assumption: lanes append to it directly).
  Done when: killing the fill at a random point and re-running yields a coverage.md with no half-written row, no duplicate cell, and the same final count as an uninterrupted run (test kills at 5 boundaries).

- **Fail the sweep on a cell whose cited path no longer resolves or runs** — FIX — value 5 — effort M — risk med — category: coverage integrity
  Why: the user's rule says "a cell counts only when it names a concrete capability grounded in a file"; later generations can rename or delete a file and the cell stays green (the pack asks this verbatim: "can the sweep check that a cited path still fires").
  Done when: deleting or renaming a cited function in a scratch copy turns exactly that cell red in `fm genesis sweep`, naming the cell.

- **Tag each cell with its harness and backtest class** — FEATURE — value 4 — effort S — risk low — category: coverage integrity
  Why: the pack's open questions ask which cells silently depend on Claude Code and which have too little history to measure. Without a tag, a planted-only cell reads as measured.
  Done when: every filled cell carries `harness: any|claude-only` and `backtest: measured|planted|none`, and the sweep lists counts per class and fails on an untagged cell.

- **Reject collateral edits from a filler lane** — SECURITY — value 3 — effort S — risk low — category: lane safety
  Why: a lane told to fill cells can edit rows it doesn't own; assumption: lanes get write access to the whole coverage.md and nothing diffs what changed.
  Done when: a merge step compares the lane's diff to its assigned cell ids, and a test with a lane that edits a neighbouring row is refused with the row named.

- **Make the empty-cell definition a tested corpus** — FIX — value 4 — effort S — risk low — category: coverage integrity
  Why: "58 empty" is a parser's count; placeholders like "TBD", "-", "n/a" with no reason, CRLF endings or an escaped pipe can flip a cell between empty and filled and silently change the target.
  Done when: a fixture file of 20 placeholder and malformed shapes gives a fixed empty/filled/n-a verdict per cell, and the parser's count equals the corpus's expected count.

- **Dead-letter cells that fail the cold read twice** — FEATURE — value 3 — effort S — risk low — category: fill loop
  Why: the cold-read rule sends failures back to the writer; with no cap a bad cell can loop forever and burn budget (assumption: no retry cap exists for cells; the budget is $100).
  Done when: a cell failing two reads is moved to a dead-letter list with its quotes, the fill proceeds, and the final report lists the dead letters.

- **Make oracle and probe outcomes three-valued: pass, fail, could-not-run** — FIX — value 4 — effort M — risk med — category: gauge honesty
  Why: the pack repeats a pattern of gauges that report a green when the check could not run (form-only gauges, "forecaster says abstained or failed, never empty"); a cell probe that errors must not count as filled.
  Done when: a probe that crashes, times out or lacks a harness reports `could-not-run`, which the sweep counts as unfilled and prints separately from fail.

- **Run each cell probe hermetically, three times** — PERFORMANCE — value 3 — effort M — risk low — category: flakiness
  Why: probes reading `fmforesight` and the asked stream may depend on time, host state or tmpfs space (the children directory is on a tmpfs under /run/user); a flaky probe makes the sweep flip red and file spurious fix tasks.
  Done when: three runs with a frozen clock and a temp HOME give identical verdicts for all probes, and a deliberately nondeterministic probe is flagged unstable.

- **Add a tmpfs and disk runway check before the fill spawns lanes** — FIX — value 3 — effort S — risk low — category: environment
  Why: children and lane scratch live under /run/user/1000, a size-limited tmpfs; a full tmpfs mid-fill would produce truncated cell files that look like successes (assumption: no pre-flight exists).
  Done when: the fill refuses to start lanes below a stated free-space floor and a test with a nearly full fake mount exits with the numbers.

- **Replay the journal with one record torn** — FIX — value 3 — effort S — risk low — category: crash safety
  Why: goal and fill state are append-only files; a kill mid-write leaves a partial last line, and the reader must skip it rather than crash or drop earlier rows.
  Done when: truncating the last record at every byte offset leaves the reader returning all earlier records and flagging the torn one.

- **Wild: Run an adversary lane that tries to pass the sweep with 58 cheap cells** — FEATURE — value 4 — effort M — risk low — category: metric gaming
  Why: wild; the standing rules fear templating and metric-gaming, and the best test of the linter and cold read is a hostile filler told to maximise the count.
  Done when: the adversary's grid is rejected by the sweep (templating, duplicates or unresolved citations), and each rejection names the rule that caught it.

- **Wild: Kill the lanes at a random second every run, until the fixpoint holds** — FEATURE — value 3 — effort M — risk low — category: chaos
  Why: wild; the fill must survive usage-limit pauses, killed sessions and forced compaction, which the pack names as planted faults. A chaos loop proves resume instead of assuming it.
  Done when: a seeded run killing lanes at random times converges to the same 58 filled cells as a clean run within three restarts.

- **Wild: Keep a shadow ledger rebuilt from git and compare it to the live one** — FEATURE — value 3 — effort L — risk med — category: state integrity
  Why: wild; the pack shows baton, ledger and repo disagreeing after a kill. A second source rebuilt from commits reveals silent divergence in cell state.
  Done when: a command rebuilds cell status from git history alone and exits non-zero with a diff when it differs from the live coverage.md.

Next question: Which probes in the 58 cells would still pass if the lane that wrote them were run on a harness without hooks?
Next question: What is the state of coverage.md if two lanes finish at the same instant and one is later reverted, and does any test cover that merge order?
