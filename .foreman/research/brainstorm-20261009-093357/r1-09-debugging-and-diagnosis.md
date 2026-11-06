# Brainstorm — lens: debugging and diagnosis

- **Run a differential-diagnosis table for FIX tasks** — FEATURE — value 5 — effort M — risk low — category: debugging
  Why: fm-debugger returns ranked hypotheses and `fm task hypo` exists, but nothing forces competing causes to be killed by a discriminating probe before a fix is written. 3 failed attempts → block is the only backstop. Assumption: hypotheses are free text today with no link to the probe that eliminated them.
  Done when: `fm task done` on a FIX refuses unless one hypothesis is marked confirmed and every other ranked hypothesis is marked eliminated with a recorded probe command and its output.

- **Bisect the cause automatically, not just the regression** — FEATURE — value 4 — effort M — risk med — category: bisect
  Why: the pack lists bisecting sentinel regressions, but a FIX with no known-good commit never gets one. Assumption: the repro command from intake is runnable and deterministic enough to drive `git bisect run`.
  Done when: given a FIX with a repro command and a lane worktree, `fm bisect` names the first bad commit, or reports "no good commit in range", with the repro exit codes logged.

- **Classify the failure before touching code** — FEATURE — value 4 — effort S — risk low — category: triage
  Why: debugging.md assumes the bug is in the code. Many failures are environment, flaky test, stale install, or wrong-version. Assumption: no pre-step distinguishes these today (the first-brainstorm "pin gate environments" idea covers only gates).
  Done when: a FIX brief records a failure class (code / env / flake / stale-install / data / harness) with the one probe that established it, and the plan differs per class in a bench case.

- **Rerun-to-classify flakes with statistics** — FEATURE — value 4 — effort S — risk low — category: flaky
  Why: "Verify intermittent bugs statistically" is listed, but nothing diagnoses *why* a test flakes. Assumption: runs can be repeated under varied seed, order, load and time.
  Done when: `fm flake <test>` runs N times under 4 perturbations and prints which perturbation changes the failure rate, with the rate per condition.

- **Keep a symptom-to-cause casebook** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: fm recall indexes briefs and lessons by BM25, but a new error message is not matched on its normalised signature (paths, ids, and timestamps stripped). Assumption: failure output is stored in evidence.
  Done when: pasting a stack trace into intake surfaces prior tasks with the same normalised signature and their confirmed root cause, in a test with two fixtures.

- **Minimise the failing input before diagnosing** — FEATURE — value 4 — effort M — risk low — category: reduction
  Why: "Shrink every FIX repro" and "minimise a failing diff by hunks" exist, but not the third axis: environment and config (which settings, env vars, and files matter). Assumption: repro is scriptable.
  Done when: `fm shrink --env` outputs the smallest set of env vars/config keys whose removal makes the repro pass, verified by rerun.

- **Demand a "why did the test not catch this" finding on every FIX** — FEATURE — value 4 — effort S — risk low — category: escape analysis
  Why: regression-test.md writes the test, but the existing suite's blind spot goes unrecorded. Escape analysis is listed only as a post-hoc gate proposal. Assumption: the done brief has a free-form field to hold it.
  Done when: a FIX cannot close without a one-line escape cause chosen from a fixed set (no test, wrong assertion, mocked away, untested path, env difference), checked in test_task.

- **Trace a bad value backwards through the ledger of runtime probes** — FEATURE — value 3 — effort L — risk med — category: tracing
  Why: root-cause tracing is prose in debugging.md; nothing automates it. Assumption: Python and TS projects can accept a temporary tracer that logs one named variable's writes.
  Done when: `fm trace <expr> -- <cmd>` prints the call chain of the writes to that value and the first line where it went wrong, on a fixture project.

- **Detect thrashing from edit patterns** — FEATURE — value 3 — effort S — risk low — category: stuck detection
  Why: the only stuck signal is three failed attempts. Editing the same hunk back and forth, or patching symptoms across 5 files, shows earlier. Assumption: the ledger records edits per step.
  Done when: a fixture session with an edit/revert cycle on one hunk triggers a "thrash" note forcing a hypothesis restatement before the next edit.

- **Wild: Keep a rubber-duck cross-examiner that asks the builder "what would you bet this isn't?"** — FEATURE — value 3 — effort M — risk low — category: reasoning
  Why: wild. Assumption: a cheap read-only Haiku child can be fed the hypothesis and evidence and return the single most embarrassing alternative.
  Done when: a FIX's hypothesis step records the challenger's alternative and the probe run to rule it out.

- **Wild: Rebuild the bug in a minimal synthetic repo and hand it to a fresh agent** — FEATURE — value 3 — effort L — risk med — category: isolation
  Why: wild. If a cold agent with only the reduced repo cannot reproduce or diagnose it, the cause is hidden in context, which is itself a finding. Assumption: shrink produces a self-contained directory.
  Done when: a command emits a standalone repro directory plus a pass/fail on whether a cold fm-debugger finds the same root cause.

- **Wild: Run a "what changed since it last worked" detective across everything, not just git** — FEATURE — value 4 — effort L — risk med — category: diff of the world
  Why: wild. Real regressions come from a Claude Code update, a dependency, a Python version, or an env var, not from the repo. Assumption: snapshots of tool versions and lockfiles can be stored per green gate run.
  Done when: after a gate flips red, `fm whatchanged` lists differences in tool versions, deps, env, and config since the last green run, ranked by plausibility.

- **Wild: Post-mortem a misdiagnosis, not just a bug** — FEATURE — value 3 — effort M — risk low — category: meta-debugging
  Why: wild. When a hypothesis was confirmed wrong after a fix attempt failed, the wrong belief and what misled it are the real lesson. Assumption: `fm task hypo` stores refuted hypotheses.
  Done when: each refuted hypothesis produces a recall-indexed "misleading signal" record, and a later similar FIX surfaces it in a test.

- **Separate "the fix works" from "the diagnosis is right"** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: a red→green proof shows the symptom stopped, not that the cause was removed (a retry or sleep may mask it). Assumption: the hypothesis names a testable mechanism.
  Done when: for a FIX, a second probe tied to the confirmed mechanism (for example the bad value is now never produced) must pass at done, separate from the repro.
