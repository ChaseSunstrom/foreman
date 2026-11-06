# Brainstorm — lens: wild: ideas that sound impossible

- **Speculate the edit and roll back on mismatch** — PERFORMANCE — value 4 — effort L — risk med — category: latency
  Why: wild. Assumption: the usage-burn work shows gate waits dominate wall time, so the gate can start on a predicted diff while the model is still replying. A mismatch rolls the predicted diff back, the way a CPU discards a mispredicted branch.
  Done when: on a replayed queue, a predicted diff that matches the model's real diff closes without a second gate run, and the journal logs each hit and miss.

- **Prove a gate passed without showing the code** — FEATURE — value 2 — effort L — risk high — category: private proof
  Why: wild. Assumption: clients of private repos want evidence a gate passed without seeing source. A full zero-knowledge proof of a test run is out of reach, but a commit-reveal receipt (the gate's hash of the diff, the verdict and a salt, signed) is buildable now.
  Done when: a verifier holding only the receipt file confirms "green on diff X" and rejects the receipt after a one-byte change to the diff.

- **Port a module to a second language, with the suite as the oracle** — FEATURE — value 2 — effort L — risk high — category: migration
  Why: wild. Assumption: plugin/tests (368 files) pins behaviour tightly enough to act as a spec for a rewrite.
  Done when: a 200-line lib module is ported in a throwaway worktree and passes its existing tests unchanged.

- **Infer each test's oracle from its name and flag mismatches** — CLEAN — value 2 — effort L — risk med — category: test quality
  Why: wild. Assumption: names like `test_help` or `test_followups` state an intent that the assertion can be checked against.
  Done when: a seeded fixture whose assertion contradicts its name is flagged, and no correct test in the suite is flagged.

- **Batch queued tasks into one prompt-cache window** — PERFORMANCE — value 4 — effort M — risk low — category: cache economics
  Why: the pack's usage-burn work (compact at 200k, Sonnet builders) says spend is the constraint. The cache warning exists, but nothing orders the queue to reuse a warm prefix.
  Done when: a queue of five same-project tasks reports one cache write and four cache reads in `fm cost`.

- **Stamp each rules-file line with the task that earned it** — CLEAN — value 3 — effort S — risk low — category: rules provenance
  Why: the rules file is 6,416 characters against a 6,400 budget (user request), and nothing records why each line exists, so trimming is guesswork.
  Done when: `fm doctor` lists every rule with its T-id and flags any rule that has none.

- **Retire tests that never fail** — CLEAN — value 3 — effort M — risk med — category: suite cost
  Why: assumption: the suite runs 368 test files on every gate, and some have never failed in recent runs. The 15-minute gate wait suggests the cost is real.
  Done when: a test with zero failures across 500 gate runs appears in a review list, and nothing is deleted without a human.

- **Read rate-limit headers in place of estimating usage** — FEATURE — value 4 — effort M — risk low — category: usage truth
  Why: the user asked Foreman to notice its own usage burn; the current `fmbudget` is an estimate. Assumption: responses or limit messages carry remaining quota that hooks can read.
  Done when: the budget readout matches the provider's reported remaining quota within 1% on a recorded session.

- **Predict the next bug from churn and coupling** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: assumption: files that change often and move together with failing tests are the likeliest sites of the next regression. Recent commits (T-1796, T-1802) cluster in the same modules.
  Done when: on a replayed history, the top five predicted files include the files of at least three real later fixes.

- **Fix a failing test by solving for its inputs** — FIX — value 3 — effort L — risk med — category: test diagnosis
  Why: assumption: failures such as the `test_help` position collision and the IndexError on main depend on a small set of inputs, which symbolic execution can enumerate.
  Done when: for the `test_help` collision fixture, the tool names the input values that trigger the failure and a fix that clears them.

- **Run the gate on a time-travelled checkout** — PERFORMANCE — value 2 — effort M — risk low — category: gate reuse
  Why: assumption: many gates re-run on commits that differ from the last green one only in docs. Skipping the unaffected tests would cut wall time.
  Done when: a docs-only commit reports the gate as reused from its parent, with the reason shown.
