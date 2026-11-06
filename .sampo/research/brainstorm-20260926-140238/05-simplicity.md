# Brainstorm — lens: simplicity

- **Give the guard its own tiny grants file** — FIX — value 5 — effort M — risk med
  Why: T-0037 (self-lockout #2). A bug in fmcore made the hook unable to load the active task, so core grants vanished and the fix was refused. The committed fallback covers only fmguard.
  Done when: a test that makes `import fmcore` raise still lets the guard honour an existing core grant (read from a separate stdlib-only JSON file), and `fm doctor` reports the degraded mode.

- **Generate the eval copies of the rules from one source** — CLEAN — value 4 — effort S — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, the rules file and the eval copies of the rules, and the rules file is at its ~60-line budget.
  Done when: editing only the plugin rules file and running `fm docs` regenerates the eval copies, and a test fails if they differ byte-for-byte.

- **Replace the guard's text heuristics with a table of rules, one fixture each** — CLEAN — value 4 — effort M — risk med
  Why: the guard blocked the agent's own legitimate edits (quoted paths, "claude plugin" strings), and the rules have grown across rounds 4–6 (persistence, tree writes, core.hooksPath spellings).
  Done when: each rule is a table row (category, matcher, positive and negative fixtures). The previously false-blocked edits are negative fixtures that pass. All 389 tests still pass.

- **Store reviewer results with `fm audit add --from-agent`** — FEATURE — value 3 — effort S — risk low
  Why: reviewer output files are huge and the agent saves the tail by hand. `fm research add --from-agent` already solves this for research (assumption: the same code path can be reused).
  Done when: a finished reviewer's final report is stored as the lens result, with no transcript, and the audit gate reads it.

- **Park T-0034 and T-0035 with explicit revisit triggers** — CLEAN — value 3 — effort S — risk low
  Why: both are L items that would add code to a ~6,700-line codebase, and this session has 30 commits of growth with no evidence that either blocks anything. Assumption: `fm audit prep` plus `--from-agent` covers most of T-0034 today.
  Done when: both inbox items are marked parked with one-line triggers (for example "3 rounds where hand-run reviewers cost more than X"), and no L item is open in the queue.

- **Merge overlapping skills from 11 to about 7** — CLEAN — value 3 — effort M — risk med
  Why: skill descriptions are always-on context, and status, next and resume overlap, as do reflect, tidy and doctor, and improve and brainstorm. Assumption: the overlap is real for users, not only in the file list.
  Done when: the skill count is ≤7, the total description characters are lower, and the evals and the install/uninstall roundtrip still pass.

- **Remove the dormant TaskCompleted gate** — CLEAN — value 2 — effort S — risk low
  Why: MASTER §10 says it is dormant on current models, so it is dead code with tests and docs attached.
  Done when: the hook, its tests and its docs are gone and the roundtrip is updated. `fm doctor` has 0 fail, and line count and hook wiring are smaller.
