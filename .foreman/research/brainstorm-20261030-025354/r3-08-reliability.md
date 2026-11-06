# Brainstorm — lens: reliability

- **Pin the failure signature before the fixer runs** — FEATURE — value 5 — effort M — risk low — category: proof integrity
  Why: the exam showed 0/108 found, and a proof that goes red for the wrong reason (import error, missing fixture, wrong cwd) would let a lane "fix" nothing. Several earlier ideas touch this ("Reject proofs that fail for the wrong reason"); this one stores the exact assertion/exception text and line at red time and requires the same signature to flip green, and a different red after the fix counts as unproven.
  Done when: a test where the proof's failure changes from AssertionError to ImportError after the "fix" is reported as unproven, not fixed.

- **Run each proof three times on the untouched tree and once on a fresh clone** — FIX — value 5 — effort S — risk low — category: flake guard
  Why: flake is an exam kind, and a flaky red admits a phantom finding. Assumption: a fresh clone catches proofs that depend on untracked files or local state.
  Done when: a proof that fails 1 of 3 runs, or fails only in the working tree, is filed as "unstable" and never reaches a lane.

- **Put every find→prove→fix stage behind a resumable checkpoint file** — FEATURE — value 4 — effort M — risk low — category: resumability
  Why: `fm genesis step` already resumes from files alone after any kill; the user asked for exactly that there (T-2095). The finder pipeline is a longer chain (find, prove, lane, re-prove, rank) with no such record.
  Done when: killing the process at each stage in a test and rerunning continues at that stage with no duplicate task or lane.

- **Give every child model call a hard budget envelope with a salvage path** — FIX — value 4 — effort M — risk med — category: cost containment
  Why: Foreman's session costs more than plain Claude (about 0.17 USD per fix) for the same score, and T-0831 (salvage partial results from capped children) is deferred. A capped finder that returns nothing wastes its spend. Assumption: partial output usually contains a usable hypothesis.
  Done when: a finder killed at its cap leaves a partial-hypotheses file, and the pipeline proves or drops each entry without a rerun.

- **Treat toolchain absence as its own verdict, "cannot run here"** — FIX — value 4 — effort S — risk low — category: false negatives
  Why: the exam spans python, js, ts, ruby, rust and c, and a missing compiler or runner looks identical to "clean". Distinguishing the two keeps the `none` kind honest.
  Done when: in a repo whose test runner isn't installed, the receipt says "could not run: <tool>" rather than "nothing found".

- **Stop scout filing Foreman's own setup failures in user projects** — FIX — value 4 — effort S — risk low — category: noise
  Why: the pack notes `probe_doctor` may queue Foreman setup faults as tasks in user projects. These are false findings that cost trust and the first-run impression.
  Done when: with a deliberately broken Foreman hook install, a scout run in a scratch project queues nothing and prints the fault to the doctor output only.

- **Revert a fix lane automatically when any previously green check flips** — FEATURE — value 4 — effort M — risk med — category: regression safety
  Why: a lane that fixes one bug and breaks another is worse than no finding. The baseline gate result is taken before the lane starts and compared after.
  Done when: a fixture fix that turns a green test red is rolled back, and the receipt names the flipped test.

- **Fence a lane's edits to the finding's declared files** — SECURITY — value 3 — effort M — risk low — category: blast radius
  Why: unasked work in a user's repo needs a smaller footprint than asked work. Assumption: the proof names the files it exercises, and the fence is those plus their direct tests.
  Done when: a lane that edits a file outside the fence is stopped, and the attempt appears in the journal.

- **Replay the exam's planted defects as a nightly canary for the pipeline itself** — CLEAN — value 4 — effort M — risk low — category: self-check
  Why: the 0/108 result went unnoticed until an outside exam; a pipeline regression should surface the same night. Uses existing held-out repos, so no new authoring.
  Done when: a deliberately broken finder makes the nightly canary exit non-zero and name the missed defect kinds.

- **Wild: Kill-switch chaos at every stage of a night shift** — FEATURE — value 3 — effort M — risk low — category: chaos testing
  Why: wild. Randomly SIGKILL the pipeline at each checkpoint in CI and assert that no lane, branch or backlog row is orphaned or duplicated.
  Done when: 100 random kills over a fixture run leave zero orphaned worktrees and a consistent ledger.

- **Wild: A null finder that must lose to the real one** — CLEAN — value 3 — effort S — risk low — category: baseline
  Why: wild. A finder that reports random plausible-looking claims runs through the same prove gate; if the null finder gets any finding past the gate, the gate is leaking.
  Done when: the null finder's pass-through rate is zero across the exam's `none` repos.

- **Wild: Dead-man receipt written before the shift starts** — FEATURE — value 3 — effort S — risk low — category: accountability
  Why: wild. Write the morning card in advance as "shift started, nothing finished", then overwrite it as stages complete, so a crash or limit hit leaves an honest card rather than a missing one.
  Done when: killing a shift mid-run leaves a card listing the stage reached and the lanes still open.

- **Keep a flaky-infra quarantine so a network or disk error never counts as a finding** — FIX — value 3 — effort S — risk low — category: false positives
  Why: a proof run that fails on a timeout or a full disk looks like a red test. Classify those exit signatures as infra and retry, not file.
  Done when: a proof that fails with ENOSPC or a connection reset is retried and, if it persists, parked as "environment" and not ranked.

Next question: What fraction of the 108 planted defects are even reachable by a read-only static pass, versus needing the project run, and does the pipeline's reliability depend on that split?
Next question: When a proof is red for the right reason but the fix lane can't turn it green within its cap, who owns the leftover failing test, and does it stay in the user's suite?
