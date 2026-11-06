# Brainstorm — lens: deepen: exam

- **Build one exam spine that every Genesis step reads** — FEATURE — value 5 — effort M — risk med — category: exam spine
  Why: the pack lists ~14 exam ideas (baseline, mutation, history-mined, black-box, checklist, persona bots) that would each become their own verb. assumption: `fm exam gen` already has a scenario-kind registry that can take new sources.
  Done when: `fm exam gen --source history|mutation|checklist|blackbox` all emit the same scenario schema, and `fm exam run` grades a mixed set with no per-source code path.

- **Record the do-nothing baseline before any tower run** — FEATURE — value 5 — effort S — risk low — category: exam baseline
  Why: "Measure the baseline before planting any gap" combined with the existing empty, oracle and plain-session arms; without a pre-Genesis score, "the tower closes gaps" can't be told apart from "the exam was easy".
  Done when: `fm genesis init` stores a gen-0 baseline row in exam.jsonl (empty, plain Claude, current Foreman arms) and `fm genesis status` shows each later generation as a delta against it.

- **Split held-out by hash and seal it with a commit hash** — SECURITY — value 5 — effort S — risk low — category: held-out integrity
  Why: inversion lens risks (rewriting toward easier exams, overfitting the held-out third) are the pack's own worry. assumption: a scenario's holdout status is currently stored, not derived.
  Done when: holdout membership is `hash(scenario id + project salt) mod 3`, the held-out set's digest is logged at init, and any later change to it is flagged by `fm genesis status`.

- **Turn the hand-written gen-0 into a checkable checklist exam** — FEATURE — value 5 — effort M — risk med — category: #13 exam
  Why: the #13 exam is "covers every MUST, NEVER and section of the hand-written one", which is a coverage test, not a behavior test. assumption: gen-0.md uses a parseable MUST/NEVER/section layout.
  Done when: `fm exam gen --from gen-0.md` yields one item per MUST/NEVER/section, a tool-less grader marks a self-written gen-0 against it, and a planted missing NEVER fails the exam.

- **Mint scenarios from the project's own fix and revert commits** — FEATURE — value 4 — effort M — risk med — category: history exam
  Why: the repo has 2000+ files and a rich commit log (e.g. T-2069, T-2073 fixes). Each fix commit gives a pre-fix tree, a failing test and a hidden key for free. assumption: a fix commit typically carries its own test.
  Done when: running it on this repo produces ≥5 scenarios where the pre-fix tree fails the commit's test, and the oracle arm passes all of them.

- **Grade the cold-resume tower with a tool-less reader** — FEATURE — value 4 — effort M — risk low — category: tower archaeology
  Why: "tower archaeology" requires files alone to say what's next and why a rewrite lost. A tool-less child given only the tower dir answers 6 fixed questions (next step, tried, why lost, open ledger items, MUSTs, budget) against a key written at save time.
  Done when: `fm exam run --kind resume` scores a 3-generation tower, and deleting lineage.md makes the score drop below its pass line.

- **Mutate the repo to plant gaps and score by kill rate** — FEATURE — value 4 — effort M — risk med — category: mutation exam
  Why: "the tower it runs closes the planted gaps" needs gaps that are real and checkable. Planted removals (a deleted guard, a stubbed verb, a dropped doc section) in a scratch copy are graded by the project's own gates.
  Done when: on a scratch copy, N planted gaps are applied, Genesis runs, and the report gives gaps closed/N with a regression check that no unplanted test went red.

- **Fall back to a black-box CLI/HTTP exam for unknown stacks** — FEATURE — value 3 — effort M — risk med — category: cold-start exam
  Why: the cold-start stranger lens: a repo in a language `fm exam gen` doesn't cover (it has 6) would get no exam and Genesis would run blind. assumption: such repos still have a runnable entry point.
  Done when: on a fixture repo in an unsupported language, the generator emits ≥9 scenarios as run-this-command/expect-this-output pairs, ≥3 held out, and the oracle arm passes them all.

- **Price each scenario and stop a generation when marginal cost beats value** — PERFORMANCE — value 4 — effort S — risk low — category: exam economics
  Why: economics lens, plus the $35 budget visible here. Exam rows already carry cost per arm; a rewrite that ties at 3× cost shouldn't win selection.
  Done when: `fm genesis status` shows cost and seconds per scenario closed per generation, and selection prefers the cheaper of two rewrites that tie on scenarios closed.

- **Let a failed held-out scenario be shrunk into a new regular scenario (wild)** — FEATURE — value 3 — effort M — risk med — category: exam growth
  Why: wild. Combines "shrink property failures into new scenarios" with held-out secrecy: when the held-out set catches a regression, a tool-less child writes a smaller, different scenario of the same weakness for the visible set, so the answer isn't leaked but the weakness gets trained on.
  Done when: a planted held-out failure produces a visible scenario that fails the same way, shares no files or strings with the held-out key, and passes after the fix.

- **Run persona bots that use the product and mint scenarios from what breaks (wild)** — FEATURE — value 3 — effort L — risk high — category: exam discovery
  Why: wild. Tool-less personas (a novice, an impatient maintainer, a hostile user) drive the web UI or CLI through scripted steps; every crash, dead end or confusing output becomes a candidate scenario, deduplicated against the grid.
  Done when: on the Genesis site page, three personas produce ≥3 distinct, reproducible failing scenarios, each replayable without the persona.

- **Judge web UI scenarios by screenshot against a design rubric (wild)** — FEATURE — value 3 — effort L — risk med — category: UI exam
  Why: wild. Foreman ships a web UI and the user keeps asking for site polish (favicon, motion, shader cards), but no scenario kind checks how it looks. A screenshot plus rubric (reduced-motion, empty state, contrast) scored by a tool-less judge covers it.
  Done when: a planted broken favicon and a missing reduced-motion rule each fail a screenshot scenario, and the fixed page passes.

- **Make every coverage-grid cell name the scenario that proves it** — FEATURE — value 4 — effort S — risk low — category: coverage grid
  Why: the request says "a coverage grid with no empty cells"; today a cell can be filled by assertion. Cell = capability × scenario kind, filled only by a scenario that the oracle passes and the empty arm fails.
  Done when: `fm genesis status` lists each cell with its scenario id, and removing a scenario turns its cell red and blocks the sweep from finishing.

- **Rotate the held-out set between generations and track exam drift (wild)** — FEATURE — value 3 — effort M — risk med — category: held-out integrity
  Why: wild. A fixed held-out third gets overfit across generations; retiring part of it into the visible set each generation and refilling with freshly authored scenarios keeps it honest, while a fixed anchor subset measures real drift.
  Done when: after 3 generations the held-out set has ≥50% new scenarios, the anchor subset is unchanged, and score trends are reported separately for each.

Next question: What does a passing exam actually predict — do exam deltas correlate with `fm outcomes` 30-day survival of the work, and if not, which scenario kinds are measuring nothing?
Next question: Who authors and audits the exam's hidden keys when the stack is unfamiliar, and how does a wrong key get noticed before it wrongly rejects a good rewrite?
