# Brainstorm — lens: bold bets

- **Run the suite and entry points under the strictest runtime mode** — FEATURE — value 4 — effort M — risk low — category: finders
  Why: the exam covers python, js, ts, ruby, rust and c, and the finders scored 0 of 108. A sanitizer or strict-mode report is a proof by construction. Examples: ASan/UBSan for C, Miri and `-race`-style checks for Rust and Go, `python -X dev -W error`, `ruby -w`, and node's `--trace-warnings` with unhandled-rejection-as-error.
  Done when: on a planted C out-of-bounds read and a Rust UB fixture, `fm find` files each finding with the sanitizer line as its proof, and a clean twin of each files nothing.

- **Give every "clean" verdict an upper bound on remaining bugs** — FEATURE — value 5 — effort M — risk low — category: none-kind
  Why: Mission 3 is graded on the exam's `none` kind, and a bare "nothing found" can't be told from "didn't look". After k independent hunt attempts with zero proven hits, report the rule-of-three bound (about 3/k) next to the ground inspected.
  Done when: a clean fixture's receipt reads "0 proven in 12 attempts, bug rate ≲ 25% per attempt, ground: 14 of 31 files", and the numbers change when k changes.

- **Wild: build a never-seen bug corpus from package version pairs** — FEATURE — value 5 — effort L — risk med — category: calibration
  Why: the grade is on never-seen repos, and Foreman only tunes on its own. Take version N of a package already on the machine or on a registry, and the tests added in N+1 whose changelog line says "fix". Those tests are a failing test on N, so the corpus has real bugs with real oracles. Assumption: registry downloads are allowed, and packages and changelogs are consistent enough to pair.
  Done when: `fm find corpus build` yields at least 30 pairs across 3 ecosystems, each with a test that is red on N and green on N+1, and the finders are scored against them.

- **Learn the report/abstain threshold from a ROC curve on held-out repos** — FEATURE — value 4 — effort M — risk med — category: ranking
  Why: nothing in the pack sets how confident a finding must be before it's shown. The `none` and `bug` kinds pull in opposite directions, so choose the operating point from exam scores per stack, not by hand.
  Done when: `fm find calibrate` writes a per-stack threshold file, and the exam score at that threshold is at least the score at the fixed default on the held-out third.

- **Apply a catalog of metamorphic relations by signature shape** — FEATURE — value 4 — effort M — risk low — category: finders
  Why: the finders have no oracle on repos with no tests. Detect pairs (encode/decode, parse/format, sort, dedupe, normalize) and test round-trip, idempotence, permutation-invariance and monotonicity. A violation is a failing test without any spec.
  Done when: on a fixture with a lossy `encode`/`decode` pair, the round-trip violation is filed with a one-file test that is red on the untouched tree.

- **Synthesize tests for uncovered branches, with the oracle taken from docs** — FEATURE — value 4 — effort L — risk med — category: finders
  Why: "untested" was a planted kind, and name-matching can't find it. Run coverage, take each uncovered branch, and ask a model for a test asserting the documented behaviour. A test that fails is a candidate bug, and one that passes is kept as new coverage.
  Done when: on an exam-style `untested` repo, at least one uncovered branch gets a generated test, and a planted bug in it surfaces as a red test.

- **Wild: mine the user's own Claude Code transcripts for bugs they corrected by hand** — FEATURE — value 3 — effort M — risk med — category: personal patterns
  Why: the user's steers and drops are ground truth about what they consider wrong. Collect the spots where a session was corrected ("that's wrong", reverts), cluster them into local probe patterns, and run those first. Assumption: transcripts are readable and stay on this machine.
  Done when: a pattern mined from at least 3 corrections finds a seeded repeat in a fixture repo, and no transcript text leaves the machine.

- **Wild: replay the user's shell history against HEAD** — FEATURE — value 3 — effort M — risk med — category: regression
  Why: the user's real build, run and test commands are a regression corpus nobody wrote. Re-run the safe, idempotent ones and flag any whose exit code or output shape changed since it last worked. The guard filters the replay.
  Done when: a fixture history containing a command broken by a recent commit yields a finding with a one-line repro, and no destructive command from the history is ever executed.

- **Wild: estimate remaining bugs by capture–recapture between two independent hunters** — FEATURE — value 4 — effort M — risk low — category: stopping rule
  Why: two hunts with different prompts or models give a Lincoln–Petersen estimate of how many bugs exist, and so when to stop paying. This answers "how do I know a repo has truly finished" without the gap map.
  Done when: on a fixture with 6 planted bugs, the estimate lands within ±2 of 6 in at least 4 of 5 runs.

- **Reproduce the repo's own open issues as failing tests** — FEATURE — value 3 — effort M — risk low — category: initiative
  Why: `fm inbox gh` is manual and never attempts reproduction. A reproduced issue is an asked-for finding with the strongest proof, and one that can't be reproduced says so.
  Done when: given 3 fixture issues, 2 become red tests and 1 is marked "cannot reproduce", with the attempts logged.

- **Re-hunt cleared repos when a new model id appears** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: a "clean" result only holds for the model that produced it. Record the model id in the receipt and queue a cheap rematch when a newer one is available, diffing against the old verdict.
  Done when: bumping the recorded model id in a fixture ledger queues exactly one re-hunt, and its receipt lists findings new since the old verdict.

- **Infer invariants from the suite's traces and re-check them on every later commit** — FEATURE — value 3 — effort L — risk med — category: finders
  Why: tests only cover the inputs their author thought of. Daikon-style inference over traced test runs produces a persistent invariant ledger, and perturbed inputs that violate an invariant become findings.
  Done when: a fixture function whose return is always non-negative in tests gets that invariant recorded, and a perturbed call that returns -1 is filed with a red test.

- **Forecast bug hotspots from git and score the forecast against what happens** — FEATURE — value 3 — effort M — risk low — category: ranking
  Why: the finders use name heuristics. Churn, recent fixes and complexity give a ranked file forecast, scored 30 days later against fix commits through `fm outcomes`, and the hunt budget follows the forecast's track record.
  Done when: `fm find forecast` prints a ranked list, and a replay on a repo's older history shows the top 10% of files contain more later fixes than a random 10%.

Next question: What does the held-out exam's `none` kind look like for repos where the toolchain can't run at all, and should that score as abstention or as failure?
Next question: Which of these probes survive when the finder model is a cheap `fm code` model, and at what cost per proven finding?
