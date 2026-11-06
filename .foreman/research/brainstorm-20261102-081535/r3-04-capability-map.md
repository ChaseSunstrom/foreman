# Brainstorm — lens: capability map

- **Verify generated output files with real parsers** — FEATURE — value 4 — effort M — risk low — category: artifacts
  Why: assumption: the request lists UI, data and docs but no prover opens the PDFs, CSVs, XLSX files, images or emails a project produces. Percy, Chromatic and pdf diffing cover this elsewhere.
  Done when: a fixture project that exports a PDF and a CSV gets a proof line reporting page count, extracted text, header schema and a raster diff, and a planted blank page turns it red.

- **Re-generate codegen in a scratch copy and diff it** — FEATURE — value 4 — effort S — risk low — category: docs/drift
  Why: the map shows lockfiles, schema dumps and generated clients, and a stale generated file is the commonest "tests pass, repo wrong" case. Nothing in the pack covers it.
  Done when: running the project's generator in a temp checkout and diffing against the committed files reports "stale" on a fixture with one hand-edited generated file.

- **Vet the user's tests before using them as proof** — FEATURE — value 5 — effort M — risk low — category: test trust
  Why: the pack only quarantines Foreman's own flaky probes. A green run from an order-dependent or flaky user suite proves nothing.
  Done when: `fm prove` runs a fixture suite shuffled, parallel and three times, and labels it "order-dependent" or "flaky" when a planted test depends on a previous test.

- **Run a config and flag combination matrix** — FEATURE — value 3 — effort M — risk med — category: coverage
  Why: assumption: the pack has environment and hostile-condition matrices but none over the project's own flags and env options. Pairwise tools like allpairs and PICT do this.
  Done when: flags found in code are pairwise-combined, a smoke command runs per combo, and a fixture bug that only appears with two flags together is named by the pair.

- **Check CI against local gates** — FEATURE — value 3 — effort S — risk low — category: infra
  Why: the repo has a test.yml badge and a local gate list (`fm doctor`, roundtrip, bench). Drift between them is unchecked.
  Done when: actionlint passes on the workflow, and a gate command missing from CI (or the reverse) is reported as parity drift.

- **Regenerate doc screenshots and compare** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: README and the site embed demo/live.svg and other images. The docs-versus-code ideas check flags and defaults, not pictures.
  Done when: every image a doc references that has a recorded `fm shot` or `fm flow` source is retaken and diffed, and a UI colour change flags the stale image.

- **Prove N-1 compatibility** — FEATURE — value 4 — effort M — risk med — category: compatibility
  Why: assumption: replaying recorded inputs through old and new builds exists as an idea, but the pack has no pairing of the previous release tag's client with the new server (and old data with new code).
  Done when: a git worktree of the last tag runs a smoke flow against the new build in both directions, and a planted breaking field rename fails one direction.

- **Run flows across locale, timezone and encoding variants** — FEATURE — value 3 — effort S — risk low — category: UI/data
  Why: assumption: only calendar boundaries are covered. Not covered are TZ shifts, non-UTF-8 locales, right-to-left text, non-ASCII paths and 300-character strings.
  Done when: a fixture flow runs under 4 variants and a hard-coded UTC assumption fails only under a non-UTC TZ.

- **Find the load knee, not just the micro-benchmark** — FEATURE — value 3 — effort M — risk med — category: performance
  Why: the pack's performance proofs are noise-floor A/B and growth-rate checks. None ramps load to the point where p99 or errors break (k6, wrk).
  Done when: a ramp against a fixture server prints the requests-per-second knee and the p99 there, and a planted N+1 query lowers the knee beyond the noise floor.

- **Test alert rules and runbook references** — FEATURE — value 3 — effort M — risk low — category: ops
  Why: assumption: the infra ideas check manifests and live config, not whether an alert rule fires on a known input (promtool-style) or whether every log line or metric a runbook names exists in code.
  Done when: a fixture alert rule has a passing and a failing unit case, and a runbook naming a nonexistent log string is flagged.

- **Grow a standing examples book from confirmed examples** — FEATURE — value 4 — effort M — risk low — category: meant-it
  Why: "turn the user's sentence into example pairs they confirm" is per task. Without persistence the user re-confirms the same domain facts every week.
  Done when: confirmed pairs append to a repo file with the task id and date, later tasks run the relevant ones unprompted, and a change breaking an old example names the confirming task.

- **Wild: have the product write its own docs, then diff them against the real docs** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: wild. This inverts "a docs-only child tries the product": a child that sees only the running product and a `--help` crawl writes the quick start, and the differences are the doc gaps.
  Done when: a child given no docs produces a quick start for a fixture app, and a planted undocumented flag appears in its diff.

- **Wild: run the product on a potato profile** — FEATURE — value 3 — effort M — risk med — category: performance
  Why: wild. A cgroup with 1 CPU, 512 MB and no network checks that the product starts, serves and degrades acceptably on weak hardware, which "works on my machine" never tests.
  Done when: a flow runs under the limits and reports startup time and peak memory, and a planted 2 GB allocation fails the profile.

- **Wild: verify what you can hear** — FEATURE — value 2 — effort M — risk med — category: surfaces
  Why: wild. Earcons, TTS and notification sounds have no prover. A spectrogram and loudness check (silence, clipping, wrong duration) would catch the usual breakages.
  Done when: a fixture sound is checked for duration, peak and non-silence, and an all-zero file fails.

- **Replay signed webhooks into a local sink** — FEATURE — value 3 — effort M — risk med — category: integrations
  Why: assumption: inbound callbacks (GitHub, Stripe-like) have no local prover, though duplicate delivery, bad signatures and out-of-order events are the usual bugs.
  Done when: a fixture handler receives each recorded payload twice, once with a bad signature, and the proof shows idempotent handling and the rejection.

Next question: Which proof kind has the most "unproven" labels in real ledgers today, and what is the cheapest prover that would convert the top three?
Next question: Which of these provers need tools the user's machine lacks (pdftotext, k6, actionlint), and should that be a doctor line or a queued install?
