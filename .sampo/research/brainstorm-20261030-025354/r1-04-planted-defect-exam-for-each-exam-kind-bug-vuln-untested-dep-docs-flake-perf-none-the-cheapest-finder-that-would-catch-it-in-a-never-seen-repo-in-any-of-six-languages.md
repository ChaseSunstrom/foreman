# Brainstorm — lens: planted-defect exam: for each exam kind (bug, vuln, untested, dep, docs, flake, perf, none) the cheapest finder that would catch it in a never-seen repo in any of six languages

- **Run one cheap read-only pass per file with a bug-shaped question** — FEATURE — value 5 — effort M — risk low — category: bug finder
  Why: the deterministic finders found 0 of 108 planted defects while plain Claude found 3/3 bugs at about 0.17 USD each. Bugs are language-agnostic judgment, so a small model reading each hot file (ranked by recent churn and size) with one question, "what input makes this wrong?", is the cheapest finder across all six languages. Assumption: a Haiku-class pass costs under 0.02 USD per file.
  Done when: on the held-out exam's bug kind, the pass names the planted file and line for at least 2 of 3 repos at under 0.20 USD per repo.

- **Prove every finding with a one-file failing test before it reaches a lane** — FEATURE — value 5 — effort M — risk med — category: proof gate
  Why: the request says findings are proved by a failing test. The exam's none kind punishes false positives, so a finding with no red test or reproduction is dropped, not ranked. Assumption: each language has a detectable test runner (pytest, node:test, cargo test, ruby minitest, a C Makefile target).
  Done when: on a never-seen repo with no planted defects, zero findings survive to a lane, and on a repo with one planted bug the surviving finding's test fails before the fix and passes after.

- **Emit "none" as a first-class verdict with its own evidence** — FEATURE — value 5 — effort S — risk low — category: false positives
  Why: the exam includes a none kind, where a clean repo should produce no work. Every finder pipeline here is rewarded for finding something. Assumption: none is scored as correct when nothing is filed.
  Done when: `fm scout` on a clean fixture prints "no findings" with the list of probes run and the number of candidates each rejected, and files no task.

- **Map vuln candidates with the language's own audit tool, then ask the model only about hits** — FEATURE — value 4 — effort M — risk low — category: vuln finder
  Why: fmsecrets alone found none of the planted vulns. Cheapest per language: bandit (python), npm audit or eslint-plugin-security (js/ts), brakeman (ruby), cargo-audit plus clippy (rust), cppcheck (c). Run whichever is installed, and let the model triage only the hits. Assumption: those tools may be absent, so the finder falls back to a grep list of sinks (eval, exec, system, innerHTML, strcpy, SQL string concatenation).
  Done when: for each of the six languages, a planted injection fixture is flagged by the tool or the sink-grep fallback, and the finding names the sink line.

- **Find untested code by running coverage, not by guessing from filenames** — FEATURE — value 4 — effort M — risk low — category: untested finder
  Why: adopt's "untested hot files" is name-based. Coverage tools exist for all six (coverage.py, c8, simplecov, cargo llvm-cov, gcov), and an uncovered function is a checkable fact with a number. Assumption: the repo's tests run offline.
  Done when: on a fixture with one planted untested function, the finding names that function and its coverage reads 0%.

- **Detect flakes by rerunning the suite N times under shuffled order and CPU load** — FEATURE — value 4 — effort M — risk low — category: flake finder
  Why: adopt reruns once; a flake needs repetition to show. Shuffle (pytest-randomly, --randomize, `cargo test -- --shuffle`) and `taskset` or a stress sibling make order and timing bugs fail. Assumption: the suite takes under a minute.
  Done when: a planted order-dependent test fails in at least 1 of 10 shuffled runs and the finding quotes the failing seed and test name.

- **Time each test and flag the one whose cost grows with input size** — FEATURE — value 3 — effort M — risk med — category: perf finder
  Why: no perf finder exists in the pack. A planted perf defect is usually a quadratic loop. Run the suite with per-test timing, then rerun the slowest test's fixture at 1x and 4x input and flag superlinear growth. Assumption: the planted perf defect is reachable from a test or a single entry point.
  Done when: a planted O(n²) function is flagged with its measured 1x vs 4x times, and a linear one is not.

- **Check dependencies against the lockfile and the registry, per ecosystem, offline first** — FEATURE — value 3 — effort S — risk low — category: dep finder
  Why: fm deps covers pypi, npm and crates, but the exam has ruby and c. Add Gemfile.lock and vendored-C (bundled zlib/openssl version strings) parsing against a cached advisory list. Assumption: planted deps are an old pinned version with a known advisory or an unused import.
  Done when: a Gemfile.lock with a known-vulnerable pinned gem and a C tree with an old vendored library version each yield a finding with the advisory id.

- **Verify docs by executing their code blocks and commands** — FEATURE — value 3 — effort S — risk low — category: docs finder
  Why: fmdocs.scan checks paths and commands but found 0 planted docs defects. A README example that raises, or names a flag the CLI does not have, is a checkable mismatch. Assumption: planted docs defects are wrong flags, stale signatures or broken examples.
  Done when: a README with one broken example and one nonexistent flag yields two findings, each quoting the line and the actual error output.

- **Rank findings by value per dollar with a kind-weighted score** — FEATURE — value 4 — effort S — risk low — category: ranking
  Why: the mission asks for value ranking. Score = proof strength (failing test > reproduction > static hit) × severity × reach (caller count) ÷ estimated fix cost. Assumption: the user prefers proved bugs above unproved smells.
  Done when: given 6 mixed findings, the ranked list puts the proved bug above an unproved lint hit, and each row shows its score parts.

- **Wild: Plant defects in the repo's own code and require the finders to catch them before trusting the scan** — FEATURE — value 4 — effort M — risk med — category: self-calibration
  Why: wild. Mutation-test the finders in place: insert a random off-by-one, a swapped condition or an eval into a copy, run the scout, and report its recall on that repo. A scout that misses its own mutants says so and lowers its confidence. Assumption: a mutation tool or a small AST rewriter exists per language.
  Done when: the scout prints "caught 4 of 6 mutants in this repo" before listing findings, and a finder disabled on purpose lowers that number.

- **Wild: Compare against the sibling that behaves differently** — FEATURE — value 3 — effort M — risk med — category: bug finder
  Why: wild. Many planted bugs are the one function in a family that skips a check its siblings do (five handlers validate, the sixth does not). Cluster similar functions by structure and flag the outlier. Assumption: planted bugs are often local inconsistencies.
  Done when: in a fixture with five validating handlers and one that skips the check, the outlier is the top finding.

- **Wild: Hold a trial for every finding with a prosecutor and a defender model** — FEATURE — value 3 — effort M — risk med — category: false positives
  Why: wild. The none kind rewards restraint. One cheap model argues the input that breaks it, the other argues why it cannot happen; only a finding whose prosecutor produces a runnable input survives. Assumption: a second call costs less than a wasted lane.
  Done when: on a clean repo the defender rejects every candidate, and on a planted bug the prosecutor's input reproduces the failure.

- **Wild: Learn from the exam's misses by turning each missed planted defect into a probe** — FEATURE — value 3 — effort M — risk low — category: learning loop
  Why: wild. After each exam, the diff between the hidden key and the findings names what the finders missed; a task writes a new narrow probe for that shape. The mission's own exam, not the user's repo, supplies the labels. Assumption: the held-out third is never used to write probes.
  Done when: after a run, each missed visible-set defect has a new probe that finds it, and the held-out score is reported separately.

Next question: What does a false positive cost the user in review time, so the proof gate and the "none" verdict can be tuned to a number rather than a feeling?
Next question: Which of the six languages has no test runner that the scout can detect without running arbitrary repo code, and is it safe to execute an unseen repo's tests at all?
