# Brainstorm — lens: deepen: benchmarks

- **Make every site figure render from a results file** — FIX — value 5 — effort M — risk low — category: benchmarks
  Why: T-1246 says prose figures on the site are hard-coded, and the constraint "every claim on the site must be measured" is the user's own. A stale number is a false claim.
  Done when: a test fails the build if any number in the Benchmarks page prose is absent from `results/*.json`, and changing a result file changes the page.

- **Build a cost-per-verified-pass ledger with a per-hook breakdown** — FEATURE — value 5 — effort M — risk low — category: cost
  Why: Long-session Foreman costs ~60% more ($0.095 vs $0.059) from bookkeeping calls and hook notes that grow context. Cost can't be cut until it is attributed.
  Done when: `fm bench cost RUN` prints tokens and dollars per source (skill listing, hook notes, `fm` calls, compaction re-sends) and the sources sum to within 2% of the run total.

- **Measure the skill-listing tax across compactions** — FEATURE — value 4 — effort S — risk low — category: cost
  Why: Claude Code 2.1.304 re-sends the whole skill list after each compaction. Foreman's 15 skills are ~3,200 of ~9,600 characters, paid again after every one of the marathon's 7 compactions.
  Done when: a benchmark case reports the characters and tokens Foreman's skills add per compaction, and the page quotes that figure with the fix (trimmed descriptions) measured against it.

- **Run an equal-dollar-cap duel and report passes per dollar** — FEATURE — value 5 — effort M — risk med — category: duel
  Why: Foreman is ~10–14% dearer on small tasks and ~60% dearer on long ones, while both sides pass everything on small tasks. A fixed budget (say $0.50 on Haiku) asks how much each side finishes, which is the question the user's "cheaper" goal poses.
  Done when: `fm bench duel --cap 0.50` stops each side at the cap and prints tasks passed, with the cap and runs stated.

- **Bisect the long-session cost gap by removing one Foreman feature at a time** — FEATURE — value 5 — effort M — risk med — category: ablation
  Why: T-1231 (cost parity) is deferred with no cause isolated. Ablation separates the hook notes, the task bookkeeping and the compaction note, so each cut can be measured instead of guessed.
  Done when: a table lists cost and hidden-test pass rate for the full set, then each feature off in turn, with at least one change that cuts cost without losing a pass.

- **Gate every release on a bench regression check** — FEATURE — value 4 — effort M — risk low — category: release
  Why: Releases 1.2.37 to 1.2.40 each shipped benchmark changes by hand, and CI already has CPU-time bounds. A cheap Haiku smoke duel with a dollar cap could catch cost creep before a tag.
  Done when: `fm release-check` runs a capped smoke duel and fails if cost-per-pass rises more than a set threshold above the last published run.

- **Wild: Replay the same session at every Claude Code version** — FEATURE — value 4 — effort L — risk med — category: compatibility
  Why: Foreman was adapted to 2.1.301 while 2.1.304 changed compaction, `tool.check` and subagent behavior. Recorded sessions could find breakage before users do. (wild)
  Done when: a recorded session replays on two Claude Code versions and prints a diff of hook firings, refusals and cost.

- **Test the guard against evasion variants of the 24 dangerous commands** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: The page claims 20 of 24 stopped and 4 saved first, with 0 of 25 everyday commands blocked. Obfuscated forms (variables, base64, `eval`, wrappers) test whether the guard generalizes beyond its published list. It must never weaken, and this is the check for that.
  Done when: a generated variant corpus shows zero false-negatives against the guard's own rules, with failures filed as FIX tasks.

- **Wild: Give each benchmark run a signed receipt anyone can verify** — SECURITY — value 3 — effort M — risk low — category: trust
  Why: Every site claim must be measured, and a skeptical reader can't check that now. A receipt would hold the commit, model, task hashes, transcripts digest and results. (wild)
  Done when: `fm bench verify RECEIPT` re-hashes the stored artifacts and reports match or mismatch for each field.

- **Benchmark Foreman's quality on compaction-heavy tasks across window sizes** — FEATURE — value 4 — effort M — risk low — category: long-session
  Why: `CLAUDE_CODE_AUTO_COMPACT_WINDOW` now takes k/M suffixes, and the long session forced compaction at 40k tokens. Plain Claude's 3 of 6 misses followed compactions. Sweeping the window shows where Foreman's advantage grows or vanishes.
  Done when: a chart of pass rate for Foreman and plain at three or more windows is generated from run files, with run counts shown.

- **Wild: Let the marathon keep score of its own findings** — FEATURE — value 3 — effort M — risk med — category: marathon
  Why: Marathon Foreman found and fixed 3 things over 7 compactions, but "found" is unaudited. Seeded latent bugs would turn it into a recall and precision measure. (wild)
  Done when: a marathon on a repo with N planted bugs reports how many were fixed, how many were broken by fixes, and the spurious changes.

- **Wild: Publish a "Foreman loses here" page from the same runs** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: The user publishes "whichever way it falls", and the 60% long-session cost gap is already on the page. Collecting every case where plain wins or costs less makes the claims credible and gives T-1231 a work list.
  Done when: the page is generated from results and lists each case where plain Claude was cheaper, faster or passed more, with its numbers.

- **Time-box a cheap Haiku calibration run before every costly measurement** — PERFORMANCE — value 3 — effort S — risk low — category: budget
  Why: The user's constraint is that usage matters. A 3-task dry run could estimate cost and variance, then refuse a full run whose projected spend exceeds its cap.
  Done when: `fm bench plan` prints a projected dollar cost and required run count, and a full run aborts before starting if the projection exceeds `--cap`.
