# Brainstorm — lens: capability map

- **Add a Foreman extension SDK** — FEATURE — value 4 — effort L — risk med — category: extensibility
  Why: assumption: gates, review lenses, task types and classifiers are built in, and `fm plugins` only manages Claude plugins. Projects can't add their own without forking.
  Done when: a project drops a manifest into `.foreman/ext/` declaring a new gate type and a new review lens, and `fm gates` and `fm audit` run both with no Foreman code change.

- **Run triggers and flows (`fm flow`)** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: the pack shows night, run, drive and serve as separate hard-coded loops. A declarative "on event → DAG of fm verbs" layer would generalise them (on push, cron, file change, issue label, usage below X%). Assumption: no user-defined workflows exist.
  Done when: a flow file "on cron 02:00 → sentinel → bench → notify" runs unattended and leaves one ledger trace.

- **Check products that aren't web UIs** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: `fm smoke` covers only the web UI in a headless browser, yet Foreman Desktop (Tauri) and CLI tools like `fm` itself are products. Add adapters: CLI transcript replay, API contract probes, TUI via pty, desktop via WebDriver, mobile emulator.
  Done when: `fm smoke` on a Tauri project launches the app, clicks through one journey, and saves a screenshot as evidence.

- **Record and replay external services in product checks** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: assumption: smoke against real backends is flaky or needs credentials. HTTP cassettes make journeys hermetic and diffable per task.
  Done when: a smoke journey passes offline from a cassette, and fails when a changed request no longer matches it.

- **Differential-test against a reference implementation** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: the existing ideas cover mutation, red-first checks and invariants, but not N-version checking. An independent agent writes a naive spec-only implementation of the changed function and fuzz-compares it with the real one, with no access to the real code.
  Done when: a seeded off-by-one in a pure function is caught by a counterexample from the differential run.

- **Synthesize property and fuzz tests for the diff** — FEATURE — value 3 — effort M — risk med — category: testing
  Why: assumption: gates run only existing tests. New pure functions in a diff get example tests at best.
  Done when: a diff adding a parser yields a committed property test that fails when the parser is mutated.

- **Run codemod campaigns** — FEATURE — value 4 — effort L — risk med — category: refactoring
  Why: `fm batch` and lanes handle a few tasks. A mechanical change across hundreds of files or many repos needs an AST codemod that is first proved on a sample, then applied in shards. Each shard gets its own gate run, and the campaign keeps a progress ledger that survives resume.
  Done when: a rename across 50 files lands as 5 verified shards, and one failing shard is quarantined without stopping the rest.

- **Gate human commits with git hooks** — FEATURE — value 3 — effort M — risk low — category: discipline
  Why: assumption: the discipline layer only applies inside Claude sessions. The user also edits by hand, and "tell the user's edits from the agent's" doesn't enforce anything. Add pre-commit and pre-push hooks that run gates and the cleanup obligation, with a one-line override.
  Done when: a hand commit that breaks a gate is refused with the failing output, and `--no-verify` is recorded in the ledger.

- **Ask the ledger in plain language** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the ledger, briefs, cost and digest data exist, but only as fixed reports. Questions like "why did T-0278 take three hours?" or "which tasks did the guard slow down most?" should return an answer with cited event ids.
  Done when: `fm ask-ledger "<question>"` returns an answer where every claim links to a real ledger line.

- **Export traces over OpenTelemetry** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: assumption: timing and cost data stays in Foreman's own files. Emitting spans per task, step, gate and hook lets people use Grafana or Honeycomb, and it's opt-in and local by default.
  Done when: with an OTLP endpoint set, one task produces a trace with gate and hook child spans, and with no endpoint nothing is sent.

- **Research with provenance** — FEATURE — value 3 — effort M — risk low — category: research
  Why: `fm research` and `fm landscape` save summaries, but claims aren't tied to sources. Store each claim with its URL, quote hash and fetch date, and flag it stale for re-check.
  Done when: a research file claim shows its source quote, and `fm docs` flags it once the page content hash changes.

- **Run spike lanes for what-if questions (wild)** — FEATURE — value 4 — effort M — risk low — category: exploration
  Why: wild. Ask "what if we dropped Redis?" and a throwaway lane tries the migration, with real build and test numbers. It returns a feasibility report and never merges.
  Done when: a spike ends with a report listing broken tests, files touched and estimated effort, and the main checkout is untouched.

- **Map comprehension debt (wild)** — FEATURE — value 4 — effort L — risk low — category: human factors
  Why: wild. The agent writes much of the code, so the user's understanding decays. Track per module how much changed since the user last read or approved it. Offer short guided walkthroughs with spaced repetition, built from `fm tour`.
  Done when: `fm ui` shows a per-directory "unread churn" heat, and finishing a walkthrough resets that directory's count.

- **Keep a dead-end atlas (wild)** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: wild. Store failed approaches and hypotheses by code region, each with why it failed. When an edit lands in that region, the atlas warns "this was tried in T-0xxx; it failed because …".
  Done when: editing a file with a recorded dead end prints the warning once per task, citing the original task.

- **Run a user-defined rehearsal of the product (wild)** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: wild. The user writes journeys as short plain-language scripts such as "sign up, pay, cancel". These are compiled once into smoke steps and replayed after every release, with a recorded clip for the digest.
  Done when: editing one script line changes the replayed journey, and the clip appears in `fm digest`.
