# Brainstorm — lens: planted-defect exam: for each exam kind (bug, vuln, untested, dep, docs, flake, perf, none) the cheapest finder that would catch it in a never-seen repo in any of six languages

- **Run the repo's own test command once and read the red** — FEATURE — value 5 — effort S — risk low — category: bug finder
  Why: the exam found 0 of 108 planted defects with deterministic finders; a failing test on an untouched tree is the cheapest bug witness in any of the six languages. Assumption: some planted bugs already fail the repo's suite.
  Done when: on three never-seen repos with a red test, `fm find` prints each failing test name as a finding with the exact command that reproduced it.

- **Ask one cheap model per file "what input breaks this?" and demand a one-file failing test** — FEATURE — value 5 — effort M — risk med — category: bug finder
  Why: plain Claude finds 3/3 at about 0.17 USD each, so the model must be the finder and the test the judge. Assumption: a per-file question costs under a tenth of a whole-session run.
  Done when: on a repo with a planted off-by-one, the hunt emits a test that is red on the untouched tree and green after the fix, at under 0.10 USD.

- **Return "none" with its evidence as a first-class verdict** — FEATURE — value 5 — effort S — risk low — category: none kind
  Why: Mission 3 is graded on `none` and `bug` kinds, so a clean repo must not produce invented findings. Assumption: the `none` kind scores false positives harshly.
  Done when: on a clean repo the output is "nothing proven", listing files read, suites run and finders that stayed silent, and files zero tasks.

- **Map vulnerability candidates with the stack's own audit tool, then ask the model only about hits** — FEATURE — value 4 — effort M — risk low — category: vuln finder
  Why: fmsecrets found no planted vulns; each of the six languages ships a cheap signal (pip-audit, npm audit, bundler-audit, cargo audit, tsc strict, compiler warnings and sanitizers for C). Assumption: tools may be absent, so grep for sinks such as eval, exec, string-built SQL and shell=True is the fallback.
  Done when: each planted vuln in a six-language fixture is flagged by a tool hit or a sink match, and the model is called only for those hits.

- **Find untested code by running coverage, not by name matching** — FEATURE — value 4 — effort M — risk low — category: untested finder
  Why: the `untested` kind needs a measured zero-hit function, not a missing test filename. Assumption: coverage.py, c8, simplecov, tarpaulin and gcov cover the six languages.
  Done when: a fixture function with zero covered lines is reported with its coverage figure, and the proof is a generated test that covers it.

- **Check deps against the lockfile and the registry, offline first** — FEATURE — value 3 — effort S — risk low — category: dep finder
  Why: fm deps covers only 3 ecosystems and the exam includes the `dep` kind in ruby and c. Assumption: planted deps are stale, vulnerable or unpinned.
  Done when: a planted outdated or advisory-listed dependency is found in each of the six manifest formats, with the registry lookup skipped when offline.

- **Run docs' code blocks and commands to find stale docs** — FEATURE — value 3 — effort S — risk low — category: docs finder
  Why: fmdocs.scan checks paths and commands only and missed all planted docs defects. Assumption: planted docs defects are wrong flags, missing files or broken examples.
  Done when: a README example that errors is reported with its exit code and output, and an example that works is not.

- **Detect flakes by reruns under shuffled order and CPU load** — FEATURE — value 4 — effort M — risk low — category: flake finder
  Why: adopt's single flake rerun is too weak for the `flake` kind. Assumption: planted flakes depend on order, time or a seed.
  Done when: a planted order-dependent test is reported with a pass rate over N runs and the seed that failed.

- **Prove perf findings with a doubling-input scaling test** — FEATURE — value 3 — effort M — risk med — category: perf finder
  Why: no probe exists for the `perf` kind. Assumption: planted perf defects are quadratic loops or repeated I/O.
  Done when: a planted O(n²) function is flagged with a measured ratio near 4 when the input doubles, and a linear function is not.

- **Rank findings by value per dollar with a shown formula** — FEATURE — value 4 — effort S — risk low — category: ranking
  Why: the mission asks for ranking, and a visible formula can be checked. Assumption: kind weight times proof strength times reach, divided by cost, is a usable first rule.
  Done when: `fm find` prints a score for each finding with its factors, and the order matches the formula on a test fixture.

- **Stop probe_doctor from filing Foreman's own setup failures in user projects** — FIX — value 3 — effort S — risk low — category: scout noise
  Why: the pack's Noticed line says probe_doctor may queue Foreman setup failures as tasks in user projects, which is noise the `none` kind would penalise.
  Done when: a scout run in a fresh project with a broken Foreman setup files zero tasks in that project's backlog.

- **Wild: Plant canary bugs in a scratch copy of the repo and require the finders to catch them before trusting a "none"** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild — it turns an empty result into a measured recall figure for this repo and language. Assumption: a mutation tool or a small model can plant defects that fail a test.
  Done when: the "nothing proven" receipt states the share of planted canaries found.

- **Wild: Hold a trial for each finding, with a prosecutor and a defender model** — FEATURE — value 3 — effort L — risk med — category: false positives
  Why: wild — a cold refuter cuts the false positives that `none` repos punish. Assumption: a second call costs less than the wasted fix lane.
  Done when: a seeded false finding is refuted and dropped, and a real one survives, on a test fixture.

- **Wild: Turn each missed planted defect from the exam into a new probe** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: wild — the 108 misses of run s0-001 are free training signal, and the held-out third guards against overfitting. Assumption: misses cluster into repeatable patterns.
  Done when: a probe mined from the exam's visible two thirds raises recall on the held-out third without raising false positives on `none`.

Next question: Which of the six languages have no runnable test command in a fresh checkout, and what does the finder report when it cannot prove anything there?
Next question: What do the exam's `none` repos contain that tempts a finder to invent a bug, such as TODO comments or odd-looking but correct code?
