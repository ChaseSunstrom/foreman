# Brainstorm — lens: bold bets

- **Ship a "contract-first" worker protocol, not adapters** — FEATURE — value 5 — effort M — risk med — category: workers
  Why: assumption: per-tool adapters (codex, gemini, opencode) are blocked on live verification (T-0335/6/7) because those CLIs aren't installed. A spec where any worker is "a command that reads a brief JSON on stdin and leaves a diff plus evidence file" can be tested with a fake worker today.
  Done when: a test runs a 20-line fake worker script through `fm worker run` and the lane merges only if the gates pass.

- **Make the gate the product: `fm verify` as a standalone referee for any agent's diff** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: Foreman's real moat is evidence, guard and done-gates (recent commits are all guard/gate work). Letting people point it at a diff made by Cursor, Aider or a human widens reach without writing an agent loop.
  Done when: `fm verify --diff <(git diff)` against a fixture brief exits non-zero with named unmet criteria, and zero when they're met.

- **Add a "proof receipt" every task emits: signed, portable, replayable** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumption: users distrust "done" claims from weaker models; evidence is already recorded by `fm` as sole state writer. Bundle brief, commands run, outputs, diff hash into one file anyone can re-run with `fm receipt check`.
  Done when: `fm receipt check R.json` re-executes the recorded verify commands in a clean checkout and reports match/drift.

- **Run a nightly "foreman on foreman" self-improvement lane with a local model** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: pack shows 30+ deferred "Later from" briefs and the user's habit of queueing small S/M briefs with exact DONE-WHEN lines; those are the ideal size for a small model. Wild-adjacent: it proves the harness claim on itself.
  Done when: an overnight `fm run --model local` closes at least one deferred S brief through all gates, with the transcript attached.

- **Wild: Publish a public leaderboard of models scored by Foreman's own conformance suite** — FEATURE — value 4 — effort L — risk med — category: community
  Why: wild; the user dropped "published held-rate scorecard" (T-0867) only for lack of cases. A fixed corpus of briefs with DONE-WHEN checks, which the user already writes in that form, becomes a "SWE-bench for discipline" for small and local models.
  Done when: `fm bench --model X` runs ≥20 fixture briefs offline and emits a table of first-pass, held and escalated rates.

- **Wild: "Foreman Code pocket edition": one `fm` binary on a USB stick with a quantized model manifest** — FEATURE — value 3 — effort L — risk high — category: portability
  Why: wild; stdlib-only Python plus local OpenAI-compatible endpoints already fits offline. A manifest pointing at a user-chosen local model, never auto-downloading, makes an air-gapped harness.
  Done when: on a machine with no network and only Python, `fm code --brief T-1` completes a fixture task against a stub local server.

- **Wild: Let the guard learn from `fm guard mine` and propose its own new rules as reviewable briefs** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: wild; mining refusals with replay labels (abandoned vs rewritten) already exists in the asks. Closing the loop turns false-positives and misses into queued, test-backed guard changes.
  Done when: running mine over a fixture corpus captures one brief naming a refused-then-abandoned command pattern, with a failing guard case attached.

- **Add a failure-class router: classify why a step failed and pick the remedy** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: assumption: failures like malformed JSON, wrong file, test never ran, and loop/stall need different fixes (repair, re-read, force run, escalate). One table beats generic retries and costs no tokens.
  Done when: replaying four recorded failures produces four distinct, logged remedies.

- **Treat criteria quality as a gate: lint briefs before any worker starts** — FIX — value 4 — effort S — risk low — category: intake
  Why: T-1208 and the "test_lease" steer show verify commands naming nonexistent modules; a weak model wastes a whole run on that. Dry-run each DONE-WHEN command and reject unrunnable ones at intake.
  Done when: `fm task add` with a verify command naming a missing test module refuses with the missing path.

- **Add a worker "cost of being wrong" budget: cheap models get small blast radius** — SECURITY — value 4 — effort M — risk low — category: safety
  Why: assumption: the less proven a model, the fewer files, lines and commands it may touch per lease. Foreman already has leases and a guard, so scope shrinks automatically from the capability profile.
  Done when: a fixture low-trust worker editing beyond its lease file cap is blocked while a trusted one passes.

- **Wild: A spectator view where you watch two models race the same brief, live, in the web UI** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; builds on the race-mode idea but makes it visible: split panes, gate lights turning green, winner merged. Doubles as a demo for the GitHub Pages site (T-1206).
  Done when: the web UI shows two lanes with live step and gate status for one brief and marks the merged winner.

- **Generate the Pages site's demo from real recorded `fm code` sessions** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: T-1206 (website) and T-1207 (Foreman Code) are queued together; demo/live.svg already comes from a real session. Reusing replay transcripts keeps the site honest.
  Done when: the site build renders a session replay from a stored transcript with no network access.
