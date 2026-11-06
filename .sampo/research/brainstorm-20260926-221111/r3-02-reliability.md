# Brainstorm — lens: reliability

- **Journal compound commands so a crash can't half-finish them** — FIX — value 4 — effort M — risk med
  Why: per-file writes are already crash-safe, but `fm task done`/`finish`/`focus` touch the brief, lessons, decisions, recall index and queue. A kill between writes leaves them inconsistent. Assumption: no multi-file intent log exists.
  Done when: killing `fm task done` after each write step (fault-injection test) makes the next `fm` call roll it forward or back to a consistent state, and `fm doctor --fsck` is clean.

- **Mutation-test Foreman's own gates** — CLEAN — value 4 — effort M — risk low
  Why: 474 tests pass, but nothing shows they'd catch a gate silently weakened (for example `>=` flipped, an audit check skipped). The gates are the product.
  Done when: a stdlib script flips each gate condition in `plugin/lib`, and every mutant fails at least one test. Survivors are listed and each gets a test.

- **Journal edits per hunk and undo only Foreman's own** — FEATURE — value 4 — effort M — risk med
  Why: `fm undo` restores a checkpoint at focus, so it could wipe the user's concurrent manual edits. Outside edits are detected but can't be separated at undo time. Assumption: undo restores the whole tree.
  Done when: with a user-edited file and a Foreman-edited file, `fm undo` reverts only Foreman's hunks and reports the user-touched file as left alone.

- **Track gate false positives and record audited waivers** — FEATURE — value 3 — effort M — risk low
  Why: heuristic gates (scope drift, verify-command lint, security lens) will sometimes be wrong, and the only way past is to game them. Assumption: no waiver path exists.
  Done when: `fm waive GATE --reason` lets one done pass, lists the waiver at done and in the digest, and `fm doctor` flags any gate waived on more than 30% of its firings.

- **Reap orphaned worktrees, temp files and stale locks** — CLEAN — value 3 — effort S — risk low
  Why: `fm improve`, `fm run` and parallel worktrees create resources that a crash or an abandoned task can leave behind. The uninstall residue check doesn't cover mid-life leaks.
  Done when: resources are registered at creation, and `fm tidy` removes any whose owner task or session is dead, leaving the live ones. A test with a killed run confirms this.

- **Canary the transcript format behind cost and usage** — FIX — value 3 — effort S — risk low
  Why: cost, usage and digest all parse Claude Code transcripts, an undocumented format that can drift. Hook payloads are validated, but transcripts aren't.
  Done when: the scanner counts unparsed or unknown-shape lines, and `fm cost` prints "partial: N% unparsed" instead of a wrong total. A fixture with an altered schema shows the warning.

- **Run the suite across interpreter, locale, timezone and encoding variants** — FIX — value 3 — effort S — risk low
  Why: stdlib-only code still varies by Python minor version, `LANG=C`, non-UTF-8 filesystems and DST. Odd repo shapes are tested, but the environment isn't varied. Assumption: tests run in one environment.
  Done when: one command runs the suite under the oldest and newest available Python plus `LC_ALL=C` and `TZ` shifts, and all pass.
