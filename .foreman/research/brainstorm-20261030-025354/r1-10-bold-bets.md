# Brainstorm — lens: bold bets

- **Replace the deterministic finders with a read-only model hunter that must attach a repro** — FEATURE — value 5 — effort L — risk med — category: finders
  Why: the exam's regex and secret finders caught 0 of 108 planted defects, while plain Claude found 3/3 on held-out bugs. Mission 3 is graded on never-seen repos. Split the repo into file clusters and give each to a cheap hunter that outputs only a claim plus a runnable reproduction. Drop any claim without one.
  Done when: on a held-out exam repo with a known bug, `fm scout --hunt` files a finding with a repro command that exits non-zero.

- **Discard any finding whose test is not red on the untouched tree** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the exam's `none` kind punishes invented bugs. A finding is filed only after its generated test fails on a clean checkout, in a throwaway worktree, for the stated reason (the assertion message must match the claim).
  Done when: on a clean-repo fixture the pipeline files zero findings and a seeded-bug fixture files exactly one.

- **Make a clean repo a result: print a "nothing proven" receipt** — FEATURE — value 4 — effort S — risk low — category: none-kind
  Why: today an empty hunt is silence. Show what was probed, how many claims were rejected and why, and what was not covered. This lets a trusted "none" be told apart from a hunt that failed to run.
  Done when: a hunt on a clean fixture prints N claims rejected, each with its rejection reason, and exits 0.

- **Require an oracle line for every bug claim** — FEATURE — value 5 — effort M — risk low — category: precision
  Why: assumption: most false positives are the hunter misreading intent. Each finding must cite the README line, docstring, type hint, existing test, or sibling-function behaviour that defines "correct". With no oracle the finding is routed to `ambiguous`, not `bug`.
  Done when: a finding without a cited, resolvable `file:line` oracle cannot be saved as kind `bug`.

- **Run a refuter against each finding before it is ranked** — FEATURE — value 4 — effort M — risk med — category: precision
  Why: a second cold agent sees only the claim and the failing test, and tries to show the test encodes a misreading of the spec. This cuts false positives on `none`. It costs one more call, so run it only on findings that already have a red test.
  Done when: on a fixture where the red test asserts the wrong behaviour, the refuter marks the finding rejected.

- **Mine git history for sibling bugs** — FEATURE — value 4 — effort M — risk low — category: finders
  Why: assumption: real repos repeat their mistakes. Read the project's `fix:` commits, extract the shape of the bug (missing None check, off-by-one slice, unclosed handle), and search the current tree for the same shape elsewhere. Each match goes through the repro gate.
  Done when: on a fixture with one past fix commit and an unfixed twin of the bug, the twin is reported with the fix commit cited.

- **Rank findings by blast radius and learn the weights from survival** — FEATURE — value 4 — effort M — risk med — category: ranking
  Why: the request asks for value ranking. Score = call-graph fan-in × git churn × user-facing path × cost of the fix, then fit the weights against `fm outcomes` 30-day survival so the ranking is checked against something outside itself.
  Done when: `fm findings` lists items in score order, and each row shows the three inputs that produced its score.

- **Cap a hunt at a cost per confirmed finding** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: plain Claude does this at about $0.17 per fix and Foreman's session costs more for the same score. Haiku-class models triage hunks, a stronger model writes tests only for survivors, and the hunt stops when the spend per confirmed finding passes a ceiling.
  Done when: a hunt receipt prints dollars per confirmed finding, and the run halts when that figure exceeds the configured ceiling.

- **Find flakes by perturbing the run** — FEATURE — value 3 — effort M — risk med — category: flake-finder
  Why: the exam lists `flake` as a kind. Rerun the suite with shuffled order, a different seed, parallelism, a skewed clock and a changed TZ. A test that flips is the finding, and bisecting over the perturbations names the cause.
  Done when: a fixture with an order-dependent test is flagged, with the specific perturbation that exposes it.

- **Wild: calibrate the hunter on planted bugs in a scratch copy first** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: wild. Before trusting a hunt in an unfamiliar stack, mutate a throwaway copy (flip a comparison, drop a guard), run the hunter, and measure its recall and precision on that language. Report "caught 4 of 5 planted bugs" with the hunt, and lower the filing threshold if recall is poor.
  Done when: a hunt receipt includes a planted-bug catch rate, and a language where it falls below the floor files nothing.

- **Wild: cross-check a function against a second implementation** — FEATURE — value 3 — effort L — risk med — category: finders
  Why: wild. For pure functions, have a model write an independent reference version, or use the stdlib equivalent, and feed both property-generated inputs. A disagreement is a candidate bug with a minimal counterexample already attached, which makes it a ready-made failing test.
  Done when: on a fixture with a subtly wrong parser, the differential run outputs a minimal input where the two versions disagree.

- **Wild: run a nightly hunter league** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. Several hunters with different personas (security auditor, fuzzer, newcomer misreading the docs) work the same repo in parallel lanes. They are scored on confirmed, non-duplicate findings. Winning prompts are kept per language and the dry ones are dropped.
  Done when: the morning report lists each persona's confirmed-finding count, and the next night's lineup differs based on those scores.

- **Wild: check a report by having a cold agent reproduce it from the text alone** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: wild. A finding passes only if a fresh agent, given just the written report (no test, no code pointers), reaches the same failing behaviour. This catches reports so vague or so specific to the author's context that a human could not act on them either.
  Done when: a finding whose report omits a needed step fails the cold-reproduce check and is not shown to the user.

- **Cap fix size and downgrade big fixes to reports** — FEATURE — value 3 — effort S — risk low — category: fix-lane
  Why: a lane fix should turn only the red test green and leave every other test untouched. If the patch exceeds a set number of lines or touches a second module, file it as a proven report for the user rather than a patch.
  Done when: a fix touching a second module becomes a report, and a one-line fix lands in its lane with the full suite still green.

Next question: Does the repro gate hold on the other exam kinds (vuln, perf, flake), where "red test" means something different, or does each need its own proof form?
Next question: What does the exam's hidden key count as a duplicate when two hunters report one defect from different angles, and how should ranking merge them?
