# Brainstorm — lens: unspoken needs

- **Calibrate the benchmark suite to where plain Claude fails** — FEATURE — value 5 — effort M — risk low — category: benchmarks
  Why: on small specified tasks both sides pass everything, so those suites can't show a quality gap. Plain Claude Code only missed on the long session (3 of 6).
  Done when: a generated difficulty ladder runs plain Claude on candidate tasks, keeps those it fails 30–70% of the time, and `fm bench` reports the pass rate for each rung.

- **Interleave Foreman and plain runs in pairs and publish intervals** — FEATURE — value 4 — effort M — risk low — category: benchmarks
  Why: the cost and time deltas (+10%, +14%, "time about equal") come from 3 runs, and API speed drifts over the day. Pairing the sides on the same seed and hour cancels that drift.
  Done when: `fm bench duel --paired` alternates sides per case, and the Benchmarks page shows a bootstrap interval for each delta and says "inside noise" when it spans zero.

- **Decompose the long-session premium into its causes** — PERFORMANCE — value 5 — effort M — risk low — category: cost
  Why: Foreman costs about 60% more there ($0.095 vs $0.059). The pack guesses at bookkeeping calls, hook notes and extra compactions but doesn't say which dominates.
  Done when: one command reads the recorded transcripts and prints dollars per source (hook notes, `fm` calls, skill relisting after compaction, extra compactions), and the biggest source is the next task.

- **Build the everyday-command corpus from real history** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: "0 of 25 everyday commands stopped" is a thin false-positive claim. 33 real refusals were already mined, so the user's own sessions can supply hundreds of allowed commands.
  Done when: a local-only corpus of at least 500 commands from past transcripts replays through `fm guard try`, the false-positive count and rate are published, and any new refusal fails CI.

- **Show the four "saved first" commands in a table with reasons** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: the safety headline is 20 of 24 stopped, 4 saved first. A reader will ask why those four weren't refused, and the guard must not weaken.
  Done when: the Benchmarks page lists all 24 commands with verdict and reason, and a test fails if the page's count differs from the replay result.

- **Add a "Where Foreman loses" section generated from results** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: the user said results are published "whichever way it falls", and the long session is already a cost loss.
  Done when: the section is built from the results files, lists every case or metric where Foreman is worse or equal, and an empty list renders as "none measured" rather than being hidden.

- **Park unrequested fixes on a side branch** — FEATURE — value 3 — effort M — risk med — category: unattended
  Why: the marathon "found and fixed 3 things" after the asked work. Those are unrequested diffs landing unattended, which is exactly what a returning user wants to review first.
  Done when: in a drive or marathon, fixes outside the request go to a branch named `foreman/extra-*` with a one-line reason each, and the close report lists them separately from the asked work.

- **Scan benchmark artifacts for identity and secrets before commit** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the repo is public, and bench results and transcripts get committed. The assumption is that they can contain the user's email, home paths or tokens.
  Done when: a pre-commit check fails on the user's email, `/home/<user>` paths and token-shaped strings in `results/` and `site/`, and a seeded test file trips it.

- **Keep unattended waits inside the prompt-cache window** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: assumption: drives that poll CI or sleep past the cache lifetime pay a full cache write on the next turn. This fits the user's "without burning usage" constraint.
  Done when: the drive's waits are chunked or skipped to stay under the cache TTL, and a recorded session with a long wait shows fewer cache-write tokens than before.

- **Report cost as a share of the plan window** — FEATURE — value 3 — effort M — risk med — category: usage
  Why: assumption: the user's worry is usage limits, not dollars, yet every figure on the page is in dollars.
  Done when: `fm cost` and the close line show approximate percent of the 5-hour window used, with the conversion shown, and say "unknown" when the plan can't be read.

- **Make `fm continue` pick the weakest scored axis** — FEATURE — value 4 — effort M — risk med — category: direction
  Why: "continue, super improve" has no target, and the real goals are scattered across pass rate, cost, time, safety and context tax.
  Done when: `fm continue` prints each axis against its target, names the furthest-behind one, and queues the highest-evidence open task for it, or says why none exists.

- **Quarantine the UI mod when it breaks and test it against the newest Claude Code** — FIX — value 4 — effort M — risk low — category: reliability
  Why: foreman-ui patches Claude Code, which is now at 2.1.304 and was last adapted to 2.1.301. The pane background mismatch is open (T-1217), and the installed mod is stale (T-0418).
  Done when: a mod crash at startup disables only the mod and writes one line to the log, and a release check loads the mod against the newest Claude Code and fails on a changed API.

- **Wild: Publish a failure reel of plain Claude's post-compaction miss** — FEATURE — value 4 — effort M — risk low — category: showcase
  Why: plain Claude Code's 3 misses "were written after a compaction". A short annotated replay of the forgotten sub-request is more convincing than a table. Wild.
  Done when: the Benchmarks page embeds one recorded miss with the line the model lost, taken from a real run and linked to its result file.

- **Wild: Let a hostile reviewer try to falsify every sentence on the site** — SECURITY — value 4 — effort M — risk low — category: honesty
  Why: the constraint is "every claim on the site must be measured", and prose figures are hard-coded (T-1246). A cold Haiku child can check each sentence against the results files. Wild.
  Done when: a release-time command lists each numeric or comparative sentence with its backing file, or "unbacked", and the release is blocked while any are unbacked.

- **Wild: Spar nightly on small real public issues at a hard dollar cap** — FEATURE — value 3 — effort L — risk med — category: benchmarks
  Why: the toy suites are neutral but synthetic. Assumption: a few capped runs on real open-source issues would show where the gap appears in practice. Wild.
  Done when: an opt-in nightly job runs both sides on one chosen issue in a throwaway clone, caps spend at $1, sends nothing outward, and appends pass, cost and time to a private log.
