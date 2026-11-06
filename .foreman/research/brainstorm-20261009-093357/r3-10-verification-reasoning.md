# Brainstorm — lens: verification reasoning

- **Run a verification-method selector at plan time** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: criteria today carry a verify command but nothing chooses the *kind* of check (unit, differential, property, observed behaviour, human glance) by what could be wrong. The prior ideas cover mutation, vacuity and ladders but not picking the method per claim.
  Done when: `fm task plan` on a FEATURE brief emits, per criterion, a chosen proof shape plus a one-line reason it fits the claim's risk, and a criterion whose verify command is of a weaker shape than selected is flagged.

- **Keep a failure-mode checklist per verify command** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: T-0342 shows a checked criterion used `-k a or b` that ran no tests; the bad verify was only found by accident. assumption: a per-command "how this can pass falsely" list (zero tests collected, wrong cwd, swallowed exit codes, skipped markers) is cheap to mine from ledger history.
  Done when: a verify that collects zero tests, exits 0 with no assertions, or ignores its own flags is rejected at `fm task criterion add`, with the named false-pass mode in the message.

- **Verify the verification of the last fix with a "would the old bug have failed this?" replay** — FEATURE — value 4 — effort M — risk med — category: regression proof
  Why: fm task prove does red→green, but nothing checks that the final regression test exercises the *same* path as the originally reported symptom after later edits.
  Done when: at done, the proof is rerun against the pre-fix tree in a scratch worktree, and a task closes only if it fails there for the recorded reason (matching error text or assertion), not any failure.

- **Add a verdict taxonomy for "done" claims with per-claim residuals** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: users receive close-outs; assumption: they can't tell "proved", "observed once", "inferred from code" and "not checked" apart. Prior ideas list what wasn't verified but don't bind each sentence to a class.
  Done when: every claim line in a close-out begins with one of four fixed tags, and a close-out with an untagged claim fails the done-gate.

- **Cross-validate verifiers against each other** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: assumption: gates rarely disagree visibly; when unit tests pass but `fm smoke` fails (or vice versa) that disagreement is the strongest bug signal and is discarded after a retry.
  Done when: a task where two independent checks of the same criterion give different results is blocked with a disagreement record naming both, and the record is visible in `fm friction`.

- **Detect verification that tests the wrong layer** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: UI/guard bugs reported by the user (guard missed `bash -lc`, desktop issues) were caught by real usage, not unit tests on helpers. assumption: criteria that name a user-visible behaviour often get verified by an internal-function test.
  Done when: a criterion phrased as user-visible behaviour whose verify command only imports internal modules is flagged and requires an end-to-end verify or an explicit waiver note.

- **Track a verification-cost ledger and spend it by risk** — PERFORMANCE — value 3 — effort M — risk low — category: verification
  Why: gates like roundtrip.py and bench_hooks take real time; assumption: effort is spent uniformly rather than where the diff is risky.
  Done when: `fm task done` prints seconds spent per proof class versus a risk score for the diff, and a high-risk diff with a below-floor proof budget is refused.

- **Re-verify old closed criteria when their dependencies change** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: closed criteria are never re-run (T-0342: checked criteria cannot be edited). assumption: later tasks silently break earlier guarantees outside the test suite's coverage.
  Done when: each closed criterion records the files it read; a later diff touching those files queues its verify rerun and reopens the task if it now fails.

- **Wild: Hold a "verdict auction" where verifiers stake credibility** — FEATURE — value 2 — effort L — risk med — category: verification
  Why: wild. Each reviewer lens and gate stakes a score on pass/fail before running; stakes are settled against later rework, so persistently overconfident verifiers lose weight in the done-confidence number.
  Done when: after 20 closed tasks, `fm verify weights` lists per-verifier weights that changed from the default, and the done-gate uses them.

- **Wild: Play the user's acceptance glance as an automated screenshot test** — FEATURE — value 4 — effort M — risk med — category: UI verification
  Why: wild. The user judges work by looking at a UI and asking for "beautiful, smooth" (Tauri steer). A model-free pixel-and-layout check can't judge taste, but a stored reference of the user's last-approved screenshots, compared per task, can surface "this looks different from what you approved".
  Done when: finishing a UI task attaches a before/after approved-baseline diff image and asks one yes/no, whose answer becomes the new baseline.

- **Wild: Run a "lying tests" pass where a model rewrites the product to fake each test** — FEATURE — value 4 — effort M — risk low — category: proof strength
  Why: wild. Mutation shows tests catch broken code; this shows whether tests can be satisfied by cheating. A cheap agent tries to make the verify pass with hardcoded outputs; success means the test is trivially fakeable.
  Done when: for each new test, a sandboxed agent attempt to pass it with special-casing is reported; any success marks the criterion "fakeable" and blocks done until strengthened.

- **Verify that docs and help text claims still match behaviour after each task** — CLEAN — value 3 — effort M — risk low — category: docs verification
  Why: user steer that cleanup, docs and replaced functionality "never got done"; MASTER.md is the single doc. assumption: commands referenced in it drift from `fm help`.
  Done when: every `fm …` example in MASTER.md and skills is executed in dry/help mode at done, and a nonexistent command or flag fails the gate.

- **Score each criterion's "surprise value" to prioritise review attention** — FEATURE — value 2 — effort S — risk low — category: reviewing
  Why: assumption: the reader of a close-out has limited attention; criteria that passed first try with no red phase are least informative.
  Done when: the close-out lists criteria sorted with ones that never failed first-run flagged "unchallenged", and the reviewer lens targets those first.
