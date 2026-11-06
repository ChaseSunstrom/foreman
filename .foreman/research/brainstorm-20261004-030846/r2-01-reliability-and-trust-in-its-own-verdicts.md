# Brainstorm — lens: reliability and trust in its own verdicts

- **Stamp every "done" with the verdict's own dependencies** — FEATURE — value 5 — effort M — risk low — category: verdict freshness
  Why: assumption: a green run can outlive the files, verify command, fm version or env it ran against. Existing ideas cover tree stamps on runs. This extends them to the whole verdict: criterion text, verify command hash, touched-file hashes, guard and fm version, and the model ID of any judge. `fm check` reports "stale because X changed" rather than re-running everything.
  Done when: editing a file a passed criterion depends on, or the verify command, marks that criterion stale in `fm task show`, and closing is refused until it is re-run.

- **Probe every verify command with a known-broken twin** — FEATURE — value 5 — effort M — risk med — category: vacuous checks
  Why: the pack has hunk mutation proof and silent no-op detection, but only per diff. This keeps a standing "negative control": before a brief is approved, run its verify against the pre-change tree (it must fail) and against a trivially broken tree such as an emptied function (it must fail). It catches checks that pass on anything, including ones written after the fact.
  Done when: a brief whose verify is `true`, or a grep that matches either version, is rejected at approval with the named control that passed.

- **Give each verdict-producing component a track record** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: findings graded MEDIUM/LOW by the in-loop reviewer were later found serious by the background security review. Record, per source (reviewer lens, bench judge, guard rule, second model), what it said and what later happened: escaped defect, reopened task, user correction, or false-positive teach. `fm trust` shows a precision/recall estimate per component, and `fm next` discounts components with poor records.
  Done when: after a seeded escape, the component that passed it shows a lowered score and `fm trust` lists the task that exposed it.

- **Report "unverified surface" at close, not only evidence** — FEATURE — value 4 — effort S — risk low — category: honest reporting
  Why: the pack has the negative-space idea (what the diff didn't touch) but no explicit statement of what was *not* checked. The done report would list criteria that rely on [assumed] facts, inconclusive runs, single-source research, skipped lenses and children that hit a budget cap. The user sees the confidence boundary in one block.
  Done when: closing a task with one assumed fact and one skipped lens prints both under "not verified", and `fm proof` carries the same block.

- **Run verdicts twice on divergent paths and flag disagreement** — FEATURE — value 4 — effort M — risk med — category: judge variance
  Why: assumption: LLM judges (bench judge, reviewer) are non-deterministic and a single sample can flip. For high-stakes verdicts only (tier L, security lens), re-run the judge with a shuffled criterion order and a different seat or model. A disagreement becomes "contested", not pass or fail, and goes to the user.
  Done when: a stub judge that flips on order produces a "contested" verdict, and a stable judge costs no extra run.

- **Fail closed on enforcement that silently didn't run** — FIX — value 5 — effort S — risk low — category: silent failure
  Why: the friction log shows the stub `claude` falling through to the real one with no signal. The general class is a check or hook that exits early, finds no tests, or resolves the wrong binary and still reports green. Add a "ran N items, resolved binary X, exit class Y" receipt to every gate. Zero items collected, or a path outside the expected root, is "inconclusive", never "passed".
  Done when: a gate whose test runner collects zero tests reports inconclusive, and the shadowed-binary case is flagged with the resolved path.

- **Wild: Hold a seeded-liar drill for Foreman's own claims** — FEATURE — value 4 — effort L — risk med — category: self-audit
  Why: wild. Nightly, a child sabotages a copy of a finished task (reverts a hunk, weakens a test, forges an evidence line), then the normal close path runs. Any sabotage that still reads "done" is a hole. This differs from judge calibration with fixtures because it attacks the whole pipeline, including the ledger.
  Done when: a planted forged evidence entry is caught by `fm doctor` or close, and the drill report lists survival rate per sabotage kind.

- **Wild: Print a confidence interval with every done** — FEATURE — value 3 — effort M — risk med — category: calibrated claims
  Why: wild. Combine the track records, verify strength (mutation-proven or not), assumption count and judge agreement into a plain "likely holds / probably holds / thin" label, backtested against reopened tasks. If the label doesn't predict reopens, the label itself is retired by the next pass.
  Done when: over a replay of past tasks, tasks labelled "thin" reopen measurably more often than "likely holds", or the feature reports it has no signal.

- **Separate the author's evidence from the verifier's** — CLEAN — value 4 — effort M — risk med — category: independence
  Why: assumption: the same session that wrote the code also writes the verify commands. Verify commands written in the same turn as the implementation are labelled "author-written". For tier M/L, a fresh no-tools child reads only the request and criteria and proposes one extra check the author did not. Disagreement between the two sets is shown at close.
  Done when: a tier-M close shows both check sets, and an author-only set carries a visible "unreviewed checks" mark.

- **Wild: Let verdicts expire like leases** — FEATURE — value 3 — effort M — risk low — category: decay
  Why: wild. Reuse the "proofs decay with churn" idea but go further: a passing verdict carries a TTL scaled to the churn and dependency fan-out of the files it covers (via the impact map). `fm doctor` re-validates only expired leases at session start, cheaply, and surfaces the ones that now fail.
  Done when: after a later commit to a heavily imported module, a covered old task shows an expired lease and is re-run, while a lease on an untouched leaf stays valid.

- **Quarantine verdicts made during a degraded environment** — FIX — value 3 — effort S — risk low — category: environment trust
  Why: hook p95 is fine, but there is no record of the load, clock, disk or network state under which gates ran, and flakes are keyed only by test ID. Tag each verdict with an environment snapshot (load, free disk, timeouts hit, offline research). Verdicts made under timeouts or an offline fallback are "provisional" until re-run clean.
  Done when: a gate that hit its timeout closes as provisional, and a clean re-run upgrades it, with both entries visible in the ledger.
