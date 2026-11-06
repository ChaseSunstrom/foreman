# Brainstorm — lens: user value

- **Fall back to the committed guard when the working copy fails** (T-0033) — FIX — value 5 — effort M — risk med
  Why: a half-applied guard edit made every write fail closed today, and recovery needed an unusual command. A lockout stops all of the user's work.
  Done when: with a syntax error injected into the working-copy guard, a safe write still succeeds and a `core` write is still blocked. `fm doctor` warns that the fallback is active. The fallback never allows more than the guard normally would.

- **Cut guard false positives on legitimate edits** — FIX — value 4 — effort M — risk med
  Why: the guard blocked the agent's own edits over quoted paths and "claude plugin" strings inside heredocs.
  Done when: a replay corpus of the observed false positives is allowed. A paired corpus of true positives (core, remote and plugin writes) is still blocked, and both run in the test suite.

- **Add `fm audit prep --note` for round-specific focus** (T-0031) — FEATURE — value 4 — effort S — risk low
  Why: the agent hand-wrote lens briefs to add threat models, and audits found real bugs every round.
  Done when: `--note "…"` appears in every lens brief, is stored with the audit, and shows up in the audit display.

- **Ingest reviewer output with `fm audit record --from-file`** — FEATURE — value 4 — effort M — risk low
  Why: reviewer output files are huge and the agent saves the tail by hand, which is slow and lossy.
  Done when: given a 5k-line reviewer file, fm stores a capped findings section (the verdict and findings list, not the log), and the raw file path is recorded. A file with no parseable verdict is rejected, not silently recorded as clean.

- **Add a "done elsewhere" status for captured requests** (T-0032) — FIX — value 3 — effort S — risk low
  Why: a request finished inside another task can only be marked "dropped", which misreports the outcome to the user.
  Done when: `fm` accepts `done-elsewhere --in T-xxxx`, and status, queue and sync show it distinctly from dropped. Old state still loads.

- **Show umbrella progress by round or slice in the statusline** — FEATURE — value 3 — effort S — risk low
  Why: T-0018 shows only "step 3/6", which hides which of rounds 4–6 is running, so the user can't tell where the work stands.
  Done when: a task with a labeled milestone shows `T-0018 r5 · 3/6` within the existing statusline time budget. Tasks without one look unchanged.

- **Generate the eval copy of the rules from the rules file** — CLEAN — value 3 — effort S — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, the rules and the eval copies of the rules. Rules are near the 60-line budget, and the pack lists doc-drift as a known risk.
  Done when: `fm docs` regenerates the eval copy, and a test fails on drift. Editing the rules file alone leaves `fm doctor` reporting the drift with a one-line fix command. (Assumption: fmdocs can own the generation.)
