# Brainstorm — lens: planted-defect exam: for each exam kind (bug, vuln, untested, dep, docs, flake, perf, none) the cheapest finder that would catch it in a never-seen repo in any of six languages

- **Run the repo's own test command once and read the red** — FEATURE — value 5 — effort S — risk low — category: bug finder
  Why: exam s0-001 found 0/108 planted defects with deterministic finders; a repo's own suite is the cheapest oracle across all six languages. Assumption: most exam repos ship a runnable suite.
  Done when: on a never-seen repo with one planted failing test, `fm find` lists that test's name and the failing assertion with no model call.

- **Ask one cheap model per hot file "what input breaks this?" and demand a one-file failing test** — FEATURE — value 5 — effort M — risk med — category: bug finder
  Why: plain Claude finds 3/3 bugs at about 0.17 USD each; Foreman's finders find none. The test is the judge, so the model can be wrong cheaply.
  Done when: on a held-out repo with 3 planted bugs, at least 2 are reported with a test that is red on the untouched tree.

- **Make "clean" a first-class verdict with evidence** — FEATURE — value 5 — effort S — risk low — category: none kind
  Why: the exam grades `none` repos, and any hunter that always finds something fails them. Assumption: `none` is scored as no filing.
  Done when: on a planted-clean repo, `fm find` exits 0 with a receipt listing files read, tests run and probes tried, and files no task.

- **Map vulnerabilities with the language's own audit tool, then ask the model only about hits** — FEATURE — value 4 — effort M — risk med — category: vuln finder
  Why: the exam covers python, js, ts, ruby, rust and c, and each has a cheap native signal (bandit, npm audit, brakeman, cargo audit, a compiler with -Wall and sanitizers). Assumption: the tools may be missing, so a missing tool must report "cannot prove here".
  Done when: a planted `eval(user_input)` in the python repo and a planted `strcpy` overflow in the C repo each yield a finding naming file and line.

- **Find untested code by running coverage, not by matching file names** — FEATURE — value 4 — effort M — risk low — category: untested finder
  Why: `untested` is an exam kind, and name matching misses it in six layouts. Coverage gives the uncovered functions directly.
  Done when: on a repo with one planted untested function, the finding names that function and not its tested neighbours.

- **Check dependencies against the lockfile and the registry, offline first** — FEATURE — value 3 — effort M — risk low — category: dep finder
  Why: fm deps covers only 3 ecosystems and the exam spans 6 languages (including ruby and c). Assumption: the planted `dep` defects are stale, vulnerable or missing pins.
  Done when: a planted pin to a known-vulnerable version is reported in each language's manifest format, and a project with no manifest says so.

- **Verify docs by executing their code blocks and commands** — FEATURE — value 4 — effort S — risk low — category: docs finder
  Why: fmdocs.scan checks paths and commands but missed all planted `docs` defects. Running the example is a direct test.
  Done when: a README snippet that raises on a planted wrong function name is reported with the failing line, with execution sandboxed and time-boxed.

- **Detect flakes by rerunning the suite under shuffled order and CPU load** — FEATURE — value 3 — effort M — risk med — category: flake finder
  Why: `flake` is an exam kind; the existing rerun is one pass. A reproduction rate (for example 3 of 20) is the proof.
  Done when: a planted time-dependent test is reported with its failure rate over N runs, and a stable suite reports 0 of N.

- **Flag the test whose runtime grows with input size** — FEATURE — value 3 — effort M — risk med — category: perf finder
  Why: `perf` is an exam kind with no probe. Assumption: the planted perf defect is an accidental quadratic with a scalable input.
  Done when: a planted nested-loop dedupe is reported with timings at two input sizes and a growth ratio above a set threshold.

- **Reject any finding whose test is not red on the untouched tree** — FIX — value 5 — effort S — risk low — category: admission
  Why: the request says "proves each finding with a failing test", and the none kind punishes false positives.
  Done when: a finding whose test passes, or fails on a syntax error rather than the claimed assertion, never reaches the ranked list.

- **Score every finder on planted-clean repos before it may file anywhere** — SECURITY — value 4 — effort M — risk low — category: precision
  Why: the exam's `none` kind makes precision the first gate. Assumption: a clean corpus of a few small repos per language is cheap to keep.
  Done when: a finder that files on a clean fixture fails `fm doctor` and is muted.

- **Wild: Plant canary bugs in a scratch copy of the repo and require recall before trusting a "clean"** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild; a "clean" claim means little unless the finder shows it can see a known bug in that repo.
  Done when: the clean receipt states "caught k of n canaries" and refuses to say clean below a set recall.

- **Wild: Turn every missed exam defect into a new probe, then rerun the exam** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild; s0-001 produced 108 misses, and each is a labelled example. Held-out scenarios keep the probes from overfitting.
  Done when: the held-out score rises after probes are added, and no clean fixture regresses.

- **Wild: A cold refuter model must reproduce each finding from its text alone** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: wild; a finding another reader cannot reproduce is likely a hallucination or too vague to act on.
  Done when: findings that the refuter cannot reproduce are dropped, and the drop rate appears in the run receipt.

Next question: Which language-specific single-test runner does each of the six exam stacks need, and how does the finder discover it in the first minute without a model?
Next question: What cost per confirmed finding makes plain Claude cheaper than the finders-plus-model route, and where should the hybrid cut over?
