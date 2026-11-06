# Brainstorm — lens: capability map

- **Prove LLM-powered features with repeated-run evals** — FEATURE — value 4 — effort M — risk med — category: LLM evals
  Why: assumption: the projects Foreman verifies increasingly call models themselves. The pack has no prover for nondeterministic output, and T-0035 covers only Foreman's own eval capture. Promptfoo and Inspect are the reference tools.
  Done when: `fm prove llm` on a fixture with 5 cases runs each case 5 times and prints a pass rate per case. Fewer than the minimum runs prints "unproven: too few runs".

- **Detect mock and fixture drift against the real service** — FEATURE — value 4 — effort M — risk med — category: test validity
  Why: assumption: the pack's "replay real inputs" and "unproven" ideas assume the test doubles are honest. Pact and VCR-style tools check that recorded responses still match the provider.
  Done when: a recorded fixture whose live stub returns a changed shape is flagged. A proof that relies on a mock is labelled "mocked, drift unchecked" until the check runs.

- **Prove terminal apps through a pty screen snapshot** — FEATURE — value 3 — effort M — risk low — category: TUI/CLI
  Why: `fm shot` and `fm flow` cover web only, yet Foreman itself is a CLI plus a TUI mod (`demo/live.svg`, foreman-ui). Tools like expect, pexpect and VHS drive terminals.
  Done when: a fixture curses app is driven with keys and its screen text asserted at 80x24 and at 40x10. A red fixture fails.

- **Make `fm flow` fail on console errors, bad network responses and logged errors** — FEATURE — value 3 — effort S — risk low — category: web UI proof
  Why: assumption: a flow can pass visually while the console shows an uncaught error or a 404. Playwright and Cypress both expose these signals.
  Done when: a fixture page that logs `console.error` and loads a missing asset fails the flow with both lines named. An allowlist suppresses known noise.

- **Audit install and postinstall scripts before a proof runs them** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: assumption: verify commands run in repos the user may have just cloned. `npm install`, `pip install` and build scripts execute arbitrary code, and the pack's pinning and sandbox ideas don't cover the install step itself.
  Done when: a fixture package with a `postinstall` that calls curl is listed. The install is refused or run network-off until the user consents once.

- **Define a prover plugin contract** — CLEAN — value 4 — effort M — risk low — category: simplicity/DX
  Why: the pack proposes many prover kinds (shot, data, infra, perf, docs) and each would otherwise be bespoke code. An executable in `.foreman/provers/` that answers `--describe` and exits 0/1/77 keeps the core small, the way git subcommands and pre-commit hooks work.
  Done when: two built-in provers are re-expressed as plugins with byte-identical `fm prove` output. A user-written 10-line prover runs through the same path.

- **Add `fm prove --watch`** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: proofs are run at the end of a task, so feedback is slow. Watchexec and jest `--watch` show the habit.
  Done when: saving a file re-runs only the provers whose covered files changed, and the first result prints in under 5 seconds on a fixture.

- **Prove concurrency claims with race detectors and stress repeats** — FEATURE — value 3 — effort M — risk med — category: concurrency
  Why: the pack's lock and concurrent-writer ideas test Foreman's own state, but nothing proves a user project's thread-safety claim. Go `-race`, TSAN and loom exist.
  Done when: a fixture with a planted data race is caught by the race-enabled run. A clean fixture passes 50 shuffled repeats.

- **Round-trip migrations up, down, up and diff the schema dumps** — FEATURE — value 3 — effort M — risk low — category: data
  Why: the pack's data ideas cover invariants and scratch-clone rehearsal, not reversibility. Atlas and sqitch verify schema state this way.
  Done when: a fixture migration whose down step drops the wrong column fails with a schema diff. A correct one passes.

- **Detect resource leaks by slope across repeated flow runs** — PERFORMANCE — value 3 — effort M — risk med — category: perf/leaks
  Why: the pack's perf ideas compare A/B timing and growth rate. A leak shows up only as a trend in memory or file descriptors over many iterations.
  Done when: a fixture handler that leaks a file descriptor per call is flagged after 200 iterations. A fixed one reports "inconclusive" or "pass", never a false alarm.

- **Pin the prover environment in a prover lockfile** — FEATURE — value 3 — effort S — risk low — category: reproducibility
  Why: assumption: pixel baselines and timings depend on the browser, fonts and tool versions. A version change would otherwise read as a regression.
  Done when: a changed browser version makes the shot compare report "environment changed, rebaseline?" instead of "regression".

- **Wild: counterfactual claim test** — FEATURE — value 4 — effort M — risk med — category: proof quality
  Why: wild. A child proposes the nearest false claim that the same evidence would also appear to support. If it can, the proof is non-discriminating. This tests the claim, where the pack's planted-break idea tests the code.
  Done when: a proof saying "the page loads" with only an HTTP 200 as evidence is flagged non-discriminating. A proof that asserts the changed text passes.

- **Wild: reproduce a bug from its report with a cold child before any fix** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: wild. A child that sees only the issue text and the running build tries to reproduce it. If it can't, the task is marked "unreproduced" and the fix can't be called proven. The pack's red-first covers tests, not report-level reproduction.
  Done when: on a fixture bug, the child's repro script fails on the parent commit and passes on the fix. An unreproducible report sets the "unreproduced" label.

- **Wild: screen-scrape prover for GUI apps with no API, using a local OCR or vision model** — FEATURE — value 2 — effort L — risk high — category: local-first
  Why: wild. Foreman Desktop and other native apps have no DOM. A local model reading screenshots keeps the proof on the owner's hardware, which fits the local-first rule.
  Done when: a fixture GTK window with a known label is verified by OCR with no network calls. A wrong label fails.

Next question: Which of these provers does the user's real project set (languages, UI, data, ops) actually need in a typical week, according to their past `fm` command history?
Next question: What do the existing provers (`fm shot`, `fm flow`) report today when the environment, not the code, changed?
