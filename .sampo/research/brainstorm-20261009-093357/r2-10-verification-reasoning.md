# Brainstorm — lens: verification reasoning

- **Check quantifiers against an enumeration** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: criteria like "all hooks", "never writes", or "every command" are usually proven by a few examples. The existing proof-shape and vacuous-verify ideas don't look at the quantifier word itself.
  Done when: a criterion containing all, every, never or any is rejected at intake unless its verify command enumerates the population from a recorded source (grep, `fm map`, a registry) and fails when a planted extra member is unchecked.

- **Make the unverifiable observable first** — FEATURE — value 5 — effort M — risk low — category: planning+verify
  Why: assumption: the pack shows gates and verify commands but no step that asks whether the repo can show the behaviour at all. Plans end up with weak checks (grep, manual look) when the real gap is a missing log line, seam or fixture.
  Done when: a criterion with no cheap executable oracle makes intake insert a prerequisite "instrument" step (seam, fixture or log hook), and that step's red-to-green is recorded before the feature step starts.

- **Index evidence by what it read, and stale it on touch** — FEATURE — value 4 — effort M — risk med — category: evidence
  Why: a hash on the whole tree is too coarse. A later task that edits one function should invalidate only the earlier proofs that exercised it.
  Done when: each recorded evidence item stores the files and functions its run touched (coverage or trace), and a later diff touching one marks the old task's claim "stale: re-run" in `fm status`, with a test using two tasks that share a function.

- **Require a reproducer on every reviewer finding** — FEATURE — value 4 — effort S — risk low — category: review
  Why: fm-reviewer lens findings are prose. Precision-weighting exists as an idea, but nothing forces a finding to carry its own proof, so false positives cost main-thread time.
  Done when: a finding without a failing command, a quoted file:line, or a stated input/output is auto-labelled "unproven" and excluded from the blocking set, and the review report shows the proven/unproven counts.

- **Detect tests that only assert their own doubles** — FEATURE — value 3 — effort S — risk low — category: test quality
  Why: assumption: builders working test-first in worktrees commonly mock a collaborator and assert the mock's configured return. That passes mutation checks only by luck, and a static check is far cheaper than running mutants.
  Done when: a lint flags a new test whose assertions depend only on values set up in the same test by a mock or stub, and a fixture test with such an assertion makes `fm task done` warn.

- **Make the builder name its weakest link** — FEATURE — value 4 — effort S — risk low — category: self-check
  Why: Foreman already makes the builder declare what it did not verify. It doesn't ask where the builder thinks it is most likely wrong, or spend a probe there.
  Done when: done requires a "most likely wrong at X" line, a dedicated probe against X is recorded, and the outcome is logged so the hit rate of those self-declared spots is queryable.

- **Treat verification as sequential testing** — FEATURE — value 4 — effort L — risk med — category: verification reasoning
  Why: the pack has a done-confidence meter and gate ordering, but each gate is a boolean. Per-check likelihood ratios learned from bench history would let Foreman choose the next check by information per second and stop when the posterior is high enough.
  Done when: `fm bench` replays show the adaptive order reaching the same pass/fail verdicts as the full run on at least 95% of cases while running at least 30% less gate time.

- **Triangulate criteria, tests and observed behaviour** — FEATURE — value 4 — effort M — risk low — category: consistency
  Why: criteria, tests and implementation are checked pairwise today. A three-way check would catch a test that passes for the wrong reason.
  Done when: for a task, a read-only pass maps each criterion to its tests and to an observed run output, and any criterion where two of the three disagree is listed, tested with a fixture where the test is right and the code wrong.

- **Verify the need, not just the request** (wild) — FEATURE — value 4 — effort M — risk med — category: intent
  Why: wild; assumption: the user's steers ("cleanup never got done", "shouldn't block until 75%") show the stated request and the underlying need diverging. Acceptance criteria encode the request.
  Done when: intake writes one scenario from the user's root need (a sentence in their words), and done runs it through a cold agent that reports whether the user would still be annoyed, with the answer stored beside the proof.

- **Test the documentation with a cold user** (wild) — FEATURE — value 3 — effort M — risk low — category: docs as test
  Why: wild; Foreman keeps MASTER.md and skills, and a feature is real only if someone can use it from what's written.
  Done when: a no-repo-context agent is given only the generated usage note for a new `fm` command and must produce a working invocation, and a failure blocks done with the confusing sentence quoted.

- **Run a builder confessional** (wild) — FEATURE — value 3 — effort M — risk low — category: honesty calibration
  Why: wild; reviewer lenses are scored on precision, but nobody measures whether reviewers find the shortcuts the builder knew it took.
  Done when: the builder privately logs up to three shortcuts, the reviewer reports blind, and `fm friction` shows the overlap rate per lens and flags lenses that miss confessed shortcuts.

- **Verify under a paraphrased brief** — FEATURE — value 3 — effort M — risk med — category: ambiguity
  Why: assumption: wording sensitivity is hidden until a user is surprised. Having a cold agent write checks from a paraphrase exposes ambiguity before the build.
  Done when: for M and L briefs, two paraphrases yield test sets, and assertions that diverge from the builder's are shown as ambiguities that need a decision before editing begins.
