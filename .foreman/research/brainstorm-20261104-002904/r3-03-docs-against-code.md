# Brainstorm — lens: docs against code

- **Bind each doc claim to a code anchor and fail on drift** — FEATURE — value 5 — effort M — risk low — category: docs
  Why: 421 docs flag claims no run has checked; README says "proves its work with commands it really ran" and MASTER.md has anchors, but nothing ties a sentence to the symbol it describes.
  Done when: a doc sentence carrying `{claim: plugin/lib/sampo/cli.py::main}` fails `sampo doctor` once that symbol is renamed or deleted, and the failure names the sentence.

- **Run every fenced `sampo` command in docs against a scratch home** — FEATURE — value 5 — effort M — risk low — category: docs verification
  Why: MASTER.md, README and skills quote many verbs; the rename (Foreman→Sampo, shims) is exactly where quoted commands silently rot. Assumption: most fences are runnable read-only.
  Done when: a nightly pass executes each fenced command in a temp HOME, and a planted nonexistent verb in a doc turns the pass red with file:line.

- **Diff `--help` against MASTER.md per verb** — CLEAN — value 4 — effort S — risk low — category: docs/code parity
  Why: the verb table lives in code and prose in MASTER.md; two sources of truth drift (one idea here asks for a "use when" lint, not flag-level parity).
  Done when: adding a flag in cli.py without a doc mention, or documenting a flag the parser rejects, fails the check and names both.

- **Make every number in docs a computed placeholder** — FIX — value 4 — effort M — risk low — category: docs
  Why: README/site cite counts (files, tests, stats); "2358 files" style figures go stale on each commit and the site already wires "real stats".
  Done when: a hard-coded count matching a known probe's recent output is flagged, and `docs render` rewrites it from the probe.

- **Add a doc-only reader exam: quickstart in a scratch home** — FEATURE — value 5 — effort M — risk med — category: docs usability
  Why: the user pushes back on wording and what surfaces claim; a tool-less child that follows only the README tells us what the docs fail to say.
  Done when: the child's run reaches `sampo doctor` green, and each step it had to guess is filed as a doc fix with the sentence quoted.

- **Lint public docs for role words instead of vendor or host names** — SECURITY — value 4 — effort S — risk low — category: docs lint
  Why: steer: never show "jarvis", never name Claude as orchestrator; README itself names Claude Code, Codex, Gemini CLI (allowed as supported harnesses) but scenes/benches must say "the orchestrator". Assumption: allowlist needed for harness lists.
  Done when: a scene caption or bench label containing "jarvis" or "claude" as orchestrator fails the ship gate; the compat table passes.

- **Show a claim ledger: proven, unproven, stale per doc file** — FEATURE — value 4 — effort M — risk low — category: docs/web UI
  Why: the mission wants unproven labelled; doc claims have no status anywhere.
  Done when: `sampo claims` lists each doc claim with last run id and cited-file hash, and a cited file change flips it to stale.

- **Check CHANGELOG lines against their commits** — FIX — value 3 — effort S — risk low — category: docs
  Why: a CHANGELOG ship was just requested; entries naming task ids (T-2848…) can be matched to commit subjects and diffs.
  Done when: an entry citing a task id with no matching commit, or a file the commit never touched, is reported.

- **Find code surface no doc mentions** — CLEAN — value 3 — effort S — risk low — category: docs coverage
  Why: 259 files in plugin/lib and many verbs; the reverse of drift is undocumented capability, and the user asked for sessions to actually reach every capability.
  Done when: a report lists verbs and hooks absent from MASTER.md and skills, and adding the doc clears the row.

- **Wild: Let docs fail the build only on sentences a test can falsify** — FEATURE — value 4 — effort L — risk med — category: docs
  Why: assumption: absolute words ("always", "never", "every") are the riskiest; wild.
  Done when: each such sentence has a probe id or a hatched "unproven" label, and a new one without either fails ship.

- **Wild: Cold child guesses the orchestrator from the rendered site** — FEATURE — value 3 — effort S — risk low — category: docs/site
  Why: steer demands any-orchestrator neutrality; a reader test measures leakage better than grep. Wild.
  Done when: the child, shown rendered pages and SVG text, cannot name a specific vendor or machine across 10 runs.

- **Wild: Record each mechanical doc claim as a replayable terminal cast** — FEATURE — value 3 — effort M — risk low — category: docs/delight
  Why: demo/live.svg already exists; casts make "it really ran" visible. Wild.
  Done when: clicking a claim on the site plays the cast from the run that last proved it, with its date.

- **Expire a "proven" doc claim when its cited files change** — FEATURE — value 4 — effort M — risk low — category: docs freshness
  Why: proof that outlives the code is the false comfort the mission targets. Assumption: claim records store file hashes.
  Done when: editing a cited file turns the claim "stale" in the next `sampo claims` without any manual step.

Next question: which of the 421 flagged claims are about behaviour a user can see versus internals, and does the user read either?
Next question: after the Sampo rename, which docs still quote Foreman-era verbs that only work through shims?
