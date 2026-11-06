# Brainstorm — lens: verification reasoning

- **Require a check that tells interpretations apart** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: `fm oracle` already lists ambiguities in a spec, but nothing ties them to the criteria's verify commands. T-0342 shows a verify that passed without testing anything.
  Done when: for an M/L brief with 2+ recorded interpretations, `fm task done` refuses unless each criterion's verify passes under the chosen interpretation and a recorded run shows it failing under a rival one.

- **Match the FIX repro to the reported symptom** — FEATURE — value 4 — effort S — risk low — category: debugging
  Why: `fm task prove` checks red→green but not that the red is the user's red. A test can fail for a different reason than "login times out on slow wifi" and still go green. Assumption: the symptom text is stored in the brief.
  Done when: `fm task prove` on a FIX compares the failure signature (error text, exception type, timing class) of the red run with the reported symptom, and flags a mismatch with both side by side.

- **Track where each expected value came from** — FEATURE — value 4 — effort M — risk med — category: test oracles
  Why: assumption: agents often write the expected value by copying the implementation's own output, so the test is circular. Nothing in `writing-good-tests.md` or `verification.md` records an oracle's source.
  Done when: new assertions and goldens in a diff carry a source tag (spec, prior behaviour, hand-derived, or captured from the new code). A test whose only source is the new code's output is flagged at done.

- **Make verdicts three-valued: pass, fail, not evaluated** — FEATURE — value 4 — effort M — risk low — category: evidence
  Why: skipped gates, missing services and zero-test runs currently read as green or as noise. Quarantined flaky gates (T-0424) need a home for "unknown".
  Done when: the ledger stores `not_evaluated` with a reason, the done summary lists those criteria separately, and a task with any unresolved one can't be closed as "verified".

- **Write semantic mutants aimed at the brief's risks** — FEATURE — value 4 — effort M — risk med — category: test strength
  Why: the stdlib mutation script (C101) flips operators. It misses the plausible wrong answers the brief's own risk list names, such as off-by-one windows or a retry that never backs off. A read-only agent could produce those mutants.
  Done when: a lane generates at least 5 risk-targeted mutants per M/L task, applies each in a scratch worktree, and reports survivors by risk. A surviving mutant must be either killed with a new test or waived with a reason.

- **Type every claim and require its proof shape** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "works", "never", "faster" and "no other callers" need different proof (example, property or exhaustive search, benchmark with variance, a search with recorded coverage). The existing ideas strengthen proof generally but don't route by claim type.
  Done when: each criterion gets a claim type at intake. `fm task done` rejects a universal claim backed only by one example, and a performance claim without repeated runs.

- **Ablate the diff hunk by hunk** — FEATURE — value 3 — effort M — risk low — category: causal check
  Why: this goes past reverting the whole fix. Reverting one hunk at a time shows which hunks the green depends on and which are unexplained extras, which feeds scope-drift detection.
  Done when: for a task with N hunks, the report maps each hunk to the criteria that go red without it. Hunks with no mapping are listed as "unproven change".

- **Audit evidence for independence** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: assumption: three green checks that share a fixture, a code path or a mock count as one. A "multiple confirmations" count overstates confidence.
  Done when: the done card groups evidence by shared dependencies, such as the same fixture file, the same mocked module or the same command. It shows the number of independent confirmations per criterion and requires 2 for L tasks.

- **Declare frame conditions: what must not change** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: non-goals exist in the brief but are prose, and no verification reads them. Behaviour-preservation work (C010) covers only CLEAN tasks.
  Done when: a brief can list frame conditions with commands (for example "`fm help` output unchanged", "guard verdicts on corpus X unchanged"). They run at done for every task type, and a change to one needs an explicit waiver.

- **Show a done-confidence meter built from check track records** — FEATURE — value 3 — effort L — risk med — category: calibration
  Why: each check type has a measurable history of passing while the claim was false (rework, reverts, escapes). Using that rate as a weight gives a calibrated number instead of a binary done. Assumption: the bench and rework data are rich enough.
  Done when: `fm task show` prints a confidence figure derived from each check's historical false-pass rate. A backtest over finished tasks shows the figure ranks reworked tasks lower than clean ones.

- **Pre-write the user's next bug report (wild)** — FEATURE — value 4 — effort M — risk low — category: foresight
  Why: wild. Before closing, a read-only agent drafts the most likely complaint the user will send after this lands, using their dialect and past steers (T-0317 "new bug feedback" shows the pattern). Each guess becomes a probe that must pass.
  Done when: a task closes with 3 predicted complaints and their probes recorded, and later real bug feedback is scored against the predictions.

- **Rebuild the brief from the tests alone (wild)** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: wild. A cold agent sees only the new tests and writes the requirements they imply. The gap between that and the real acceptance criteria shows untested intent (missing) and over-specified tests (extra).
  Done when: `fm audit` prints requirements implied by the tests but not in the brief, and brief criteria no test implies, with one concrete example for each.

- **Give verified claims a half-life (wild)** — FEATURE — value 3 — effort M — risk low — category: evidence aging
  Why: wild. A claim proven last month may be false after other merges. Cheap proofs get re-run on a schedule that depends on how much the touched files have since changed. Night sentinel runs exist but don't age individual claims.
  Done when: each closed criterion shows a freshness age. Re-running its proof after related file churn either renews it or reopens the task with the commit that broke it.
