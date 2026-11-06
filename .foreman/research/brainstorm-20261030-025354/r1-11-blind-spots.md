# Brainstorm — lens: blind spots

**Blind-spot pattern.** Each unpredicted ask (T-2093 to T-2113) falls into one of these classes: check the artifacts, resume after a kill, start from nothing, select by exam, detect drift, offer itself, be graded on held-out data, protect its own charter. Applying those questions to Initiative gives the ideas below. Mission 3 is graded on the `none` and `bug` kinds, so what Foreman does when there is nothing to find matters as much as recall.

On the earlier question about a finished project versus a dry queue: a repeatable, evidence-carrying "nothing found" result from the finders is the best signal (idea 1).

- **Make "nothing found" a scored, evidenced result** — FEATURE — value 5 — effort M — risk med — category: precision
  Why: the exam's `none` kind is graded, and finders that report 0 of 108 can't tell clean from blind. Blind-spot question: "what does it do when there is nothing to do?"
  Done when: on a seeded clean repo, `fm find` exits 0 with a list of what each probe covered and no filed tasks; on a repo with one planted bug it files exactly one.

- **Drop any finding whose repro fails for the wrong reason** — FIX — value 5 — effort M — risk low — category: proof
  Why: the pipeline proves with a failing test, but a test that fails on an import error or a typo proves nothing. Assumption: the current proof only checks red, not why it is red.
  Done when: a finding whose test fails with an error unrelated to the claimed symbol is auto-demoted to "unproven" and never reaches a lane.

- **Make `fm find step` resumable like `fm genesis step`** — FEATURE — value 4 — effort M — risk low — category: resilience
  Why: T-2095 had to be asked for. A find, prove, fix, rank pipeline has the same kill-mid-way problem. Question: "what happens after a kill at each stage?"
  Done when: killing the pipeline between prove and fix, then rerunning, resumes at the fix with no re-scan and no duplicate task.

- **Validate the findings ledger with `fm find check`** — FEATURE — value 4 — effort S — risk low — category: validation
  Why: T-2093 shows the user wanted a checker for the tower's own files. Findings carry file:line claims and repro commands that rot.
  Done when: the check fails on a finding whose cited line no longer exists or whose repro command no longer runs, and passes on a fresh ledger.

- **Fingerprint findings and let the user settle them** — FEATURE — value 4 — effort S — risk low — category: dedup
  Why: sweeps re-file the same item; the user already dropped duplicates by hand ("dropped" rows). Assumption: scout lacks stable finding ids.
  Done when: a finding marked settled is not re-filed across three consecutive scans, even after unrelated edits to the file.

- **Tag findings with their owner and keep Foreman's own setup out of user projects** — FIX — value 4 — effort S — risk low — category: scope
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks in user projects. Question: "whose problem is this finding?"
  Done when: a failed Foreman probe in a non-Foreman repo appears only in `fm doctor`, never in that project's backlog.

- **Report "cannot prove here" for stacks with no runnable tests** — FEATURE — value 4 — effort M — risk med — category: language coverage
  Why: the exam spans python, js, ts, ruby, rust and c, but the finders are Foreman-only. Unfamiliar stacks are a class the genesis hidden-key question already raised.
  Done when: on a repo where tests can't be run, a finding is filed as "unproven, suspected" with a stated reason, and is not fixed.

- **Have Foreman offer a scan itself, with cost shown and a "no" path** — FEATURE — value 3 — effort S — risk low — category: consent
  Why: T-2105 had to be asked for. Idle Foreman should offer `fm find` with an estimated cost, never run it silently.
  Done when: an empty queue prints one offer line with a dollar estimate and a one-key decline that persists.

- **Check the ranking against what survives later** — FEATURE — value 4 — effort M — risk med — category: ranking
  Why: the pack asks whether exam deltas predict `fm outcomes` 30-day survival. Value ranks are unvalidated guesses.
  Done when: `fm find report` shows rank against 30-day survival for closed findings and flags a rank signal with no correlation.

- **Seal finder prompts and flag score drops after any edit** — SECURITY — value 3 — effort M — risk low — category: drift
  Why: T-2104 and T-2113 did drift checks and sealing for gen-0, and finders are the next artifact that can silently change.
  Done when: editing a finder prompt without rerunning the exam makes `fm find check` fail.

- **Wild: Foreman plants bugs in a throwaway copy of the user's own repo and measures its recall there** — FEATURE — value 4 — effort L — risk med — category: self-exam
  Why: wild. The exam only covers never-seen repos, not this one. Done when: a nightly job reports recall on N planted mutants in a copy, and the live tree is untouched.

- **Wild: a cold second model tries to refute each finding before a lane starts** — FEATURE — value 4 — effort M — risk med — category: adversary
  Why: wild. The `none` kind punishes false positives, and a cheap refuter is a precision gate. Done when: a seeded false finding is refuted and dropped, and a true one survives.

- **Wild: a weekly one-page "what I found" digest with a one-key yes per finding** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. It turns scanning into a visible habit the user can approve in one sitting. Done when: one file lists the top five ranked findings with cost, and a keypress queues each.

Next question: Does the exam's hidden key ever mark a defect that a competent reviewer would call correct code, and how would a wrong key be noticed before it penalises a good finder?
Next question: What does one scan-prove-fix cycle cost per accepted fix compared with plain Claude's roughly $0.17, and where does the first stage that loses on cost sit?
