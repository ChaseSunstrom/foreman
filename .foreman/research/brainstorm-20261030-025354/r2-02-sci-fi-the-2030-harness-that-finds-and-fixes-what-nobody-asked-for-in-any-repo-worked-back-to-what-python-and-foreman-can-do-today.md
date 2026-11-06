# Brainstorm — lens: sci-fi: the 2030 harness that finds and fixes what nobody asked for in any repo, worked back to what Python and Foreman can do today

- **Run the previous release's tests against HEAD** — FEATURE — value 4 — effort M — risk low — category: regression finder
  Why: the 0/108 exam result shows pattern finders see nothing. A tagged release's own tests are an oracle already in the repo, and a failure there is a candidate bug that arrives already red. Assumption: most never-seen repos have tags or a usable `HEAD~N`.
  Done when: on a fixture where a commit silently changes a function's behaviour, `fm find regress` files one finding whose repro is the old test, and files nothing when the changelog or tests changed deliberately.

- **Pin a single-test runner per exam stack** — FIX — value 5 — effort S — risk low — category: proof plumbing
  Why: the exam covers python, js, ts, ruby, rust and c, and "failing test first" needs a run-one-test command in each. Assumption: today's `fm check` is Python-leaning and unknown stacks fail silently.
  Done when: for each of the six languages a hello-world fixture goes red then green through the table, and an unknown stack prints "cannot prove here" rather than a finding.

- **Keep security findings out of the published tower** — SECURITY — value 4 — effort S — risk low — category: disclosure hygiene
  Why: Genesis re-exports `site/genesis` and pushes to main on every tower change under a standing grant. A proven vuln in a user project that lands in a finding note could be published. Assumption: findings will be stored where the export can read them.
  Done when: a test seeds a `kind=vuln` finding and the export output contains neither its text nor its fingerprint, and the finding is shown only to the local user.

- **Gate advisories on call-site reachability** — FEATURE — value 4 — effort M — risk med — category: dependency finder
  Why: `fm deps` covers three ecosystems but reports versions, not exposure. An advisory names a vulnerable function, and a grep for it in the repo cuts false positives, which matters for the `none` kind. Assumption: advisory data names symbols often enough to be useful.
  Done when: a fixture pins a vulnerable version whose function is never called and gets no finding, while the same pin with a call site gets one that cites the file and line.

- **Abstain when findings exceed the repo's prior** — FEATURE — value 5 — effort S — risk low — category: none-kind guard
  Why: the mission is graded on `none` in unseen repos, and a finder that always finds something fails that kind. Assumption: findings per KLOC from past scans give a usable prior.
  Done when: a clean fixture where a noisy probe raises more than 5x the prior makes the scan halt with "probable false-positive storm, 0 filed", and the receipt shows the prior and the count.

- **Record repo vitals at every scout and file anomalies** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: scout is one-shot. Test count, suite time, flake rate, dependency age and file churn cost nothing to log, and a sudden jump is a lead that needs no code reading. Assumption: `fm map` and gate timings already expose these numbers.
  Done when: two scouts on a repo whose suite time tripled between commits produce one "suite 3.1x slower since <sha>" lead, and a flat repo produces none.

- **Emit a stdlib-only repro bundle per finding** — FEATURE — value 4 — effort M — risk low — category: proof portability
  Why: a finding is only as credible as its repro, and the cold-reproducer and refuter ideas need something a stranger can run. One file that exits 1 on the bug serves the user, a second model and a bug report.
  Done when: `python3 -I repro_F-12.py` exits 1 on the untouched tree and 0 after the fix, with no imports outside the stdlib.

- **Synthesize property tests for typed pure functions** — FEATURE — value 4 — effort L — risk med — category: bug finder
  Why: the exam's bug kind needs a machine-checkable oracle where no test exists. Round-trip, idempotence and order-invariance properties come from signatures and docstrings, and a shrunk counterexample is itself the failing test. Assumption: a stdlib `random` fallback is acceptable when Hypothesis is missing.
  Done when: on a fixture with an off-by-one in a `parse`/`format` pair, the property run yields a minimal counterexample, and clean pairs yield none over 1000 cases.

- **Carry a proven fix across the user's other local repos** — FEATURE — value 3 — effort M — risk med — category: local-first reuse
  Why: the same author tends to repeat the same bug, and everything stays on the owner's disk. Assumption: repos are discoverable from the existing project registry.
  Done when: after a kept fix in repo A, `fm find siblings` greps repo B for the pattern, files a candidate with a red test or says "no match", and reads nothing outside registered repos.

- **Prefilter files with a local small model** — PERFORMANCE — value 3 — effort M — risk med — category: privacy, cost
  Why: plain Claude finds and fixes at about 0.17 USD per bug, and Foreman's session costs more for the same score. A local ranker that sends only the top-k files to the paid model closes the gap and keeps the rest private. Assumption: a local engine such as ollama is optional.
  Done when: with the engine on, a scan sends at most k files to the paid model and logs the rest as "kept local". With it off, behaviour is unchanged.

- **Wild: run nightly parallel universes of the repo** — FEATURE — value 3 — effort L — risk med — category: perturbation finder
  Why: assumption: a bug that exists in only one universe, with TZ shifted, dependencies rolled back one minor, or Python bumped, is one that normal runs never see. Each universe is a throwaway copy and only divergence from baseline becomes a lead.
  Done when: a fixture with a TZ-dependent bug reports it as "differs only under TZ=Pacific/Auckland", and a clean fixture reports identical results across all universes.

- **Wild: reconstruct the author's intent from blame** — FEATURE — value 2 — effort L — risk high — category: intent check
  Why: assumption: commit messages and blame state what a function was meant to do, and a quiet divergence is the unasked-for bug. It must pair with the abstain guard because it is speculative.
  Done when: on a fixture where a refactor drops a documented boundary case, the finding quotes the original commit message and a red test, and drops any claim lacking both.

- **Wild: keep a flight recorder for every hunt** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: assumption: an ordered log of files read, hypotheses made and refutations is the corpus for tuning probes and for answering why a finding was or wasn't raised. It is local and redacted.
  Done when: `fm find replay <id>` prints the hunt step by step offline, and a test confirms a secret in a read file is redacted in the log.

Next question: do the exam's `none` repos share traits (size, test density, language) that predict where a finder over-reports?
Next question: what does a clean verdict cost per repo, compared with the 0.17 USD plain-Claude baseline?
