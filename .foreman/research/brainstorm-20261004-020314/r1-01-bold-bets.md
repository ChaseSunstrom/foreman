# Brainstorm — lens: bold bets

- **Make the brief a typed contract that hooks enforce at edit time** — FEATURE — value 5 — effort L — risk med — category: enforcement
  Why: the guard blocks by shell/edit category, but criteria and steps are prose; reviewers keep finding scope drift and edge cases afterward. Assumption: the brief's "files in scope" and step boundaries can be extracted at plan time.
  Done when: an edit outside the active step's declared paths yields a PreToolUse note naming the step, and a test shows an in-scope edit passes with no note.

- **Add a plan-time red-team that attacks the plan, not the diff** — FEATURE — value 4 — effort M — risk low — category: review
  Why: every review pass found 3–7 issues, and the second focused adversary pass found a whole class the first missed. That is late, expensive discovery. Assumption: a tool-less child can list likely failure classes (parser edge cases, export privacy, exec channels) from the brief alone.
  Done when: fm task plan on an M/L task writes a "attack surface" section, and bench shows fewer reviewer HIGH/MEDIUM findings on replayed tasks with it than without.

- **Build a known-bad-class library that seeds every new parser and guard task** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the git exec-channel class was missed once, and the guard tests passed for the wrong reason. Past findings are not reusable beyond lessons. Assumption: findings can be tagged by class (quoting, channels, truncation, privacy).
  Done when: creating a task touching fmguard surfaces the class checklist, and a test fails if a channel test's payload is catchable by the word scan alone.

- **Add mutation testing for the tests Foreman requires as evidence** — FEATURE — value 5 — effort M — risk low — category: evidence
  Why: the tests passed for the wrong reason, which means green evidence was weak. Inconclusive runs exist, but nothing measures whether a test can fail. Assumption: simple AST mutations (flip a condition, drop a branch) are enough in stdlib.
  Done when: fm task evidence on a new test runs mutants of the touched lines and records the kill ratio, and a test that kills none is recorded as inconclusive.

- **Run a post-crash reconciliation at every session start** — FIX — value 4 — effort S — risk low — category: resilience
  Why: a crash left four zero-byte objects that fm doctor missed, and pass 1 added doctor checks only on request. Assumption: a cheap check (empty objects, truncated JSON) costs under 100 ms.
  Done when: a session start after a simulated truncation prints a one-line repair offer, with hook latency p95 still under 50 ms.

- **Make the guard emit a verdict receipt with an allow-once path** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: three guard false positives (stash list, python heredoc, state-read) cost user friction, and the guard must never be weakened. Assumption: each block can carry a stable reason code.
  Done when: a blocked command prints a reason code and the precise rule, `fm allow <code> --once` permits exactly that one command, and replay over the 5,000-command corpus shows no new passes.

- **Wild: Let Foreman bet on its own briefs and settle with evidence** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: tiers S/M/L are guessed, and an S task touching 3+ files is already re-tiered. A recorded prediction (tier, steps, first-time close) compared at close builds a calibration curve. Wild, assumption: the history is rich enough to learn from.
  Done when: fm friction reports predicted vs actual tier hit-rate over the last 30 tasks.

- **Wild: Run a canary brief at session start through the real hook path** — FEATURE — value 3 — effort S — risk low — category: assurance
  Why: Foreman's value is that hooks refuse unbriefed edits, yet a broken hook fails silently. Wild, assumption: a throwaway sandbox edit can be attempted without touching the user's tree.
  Done when: disabling the edit hook makes the canary fail and the pane shows a red "enforcement off" badge.

- **Wild: Add a shadow-user soak that plays the user's verbatim steers against a candidate build** — FEATURE — value 4 — effort L — risk med — category: self-test
  Why: the user's steers (corrected verifies, "never X", widened criteria) are the real acceptance rubric, yet no release is judged against them. Wild, assumption: a child can stay in character within the $6/command cap.
  Done when: a candidate build runs a ten-request queue under the soak and a report lists every moment a steer would have been violated.

- **Wild: Offer "undo this task" as one verified rollback** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: the user denied a removal and a crash corrupted the repo, so trust in reversibility matters. Assumption: each task has commit boundaries per step.
  Done when: fm undo T-ID reverts the task's commits on a branch, reruns the pre-task gates, and shows they match the starting results.
