# Brainstorm — lens: inversion: how initiative fails or harms — false alarms, noisy captures, fixes nobody wanted, a finder that edits code it shouldn't, scope creep into user projects

- **Skip code the user is already touching** — FEATURE — value 4 — effort S — risk low — category: scope safety
  Why: assumption: an unasked fix landing in a file with uncommitted edits, an open branch or a recent human commit causes conflicts and annoyance. The pack shows lanes and scout but no hot-file guard.
  Done when: a fixture repo with a dirty file and a branch-touched file gets zero findings or lanes on those two files, and the receipt names each skipped file with its reason.

- **Don't hunt where the queue is about to rewrite** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: the open work lists many deferred and blocked tasks, so a finder can prove a bug in code a queued task will replace. Assumption: findings aren't checked against the backlog today.
  Done when: a finding whose file matches an open task's file set is held as "overlaps T-xxxx" and never reaches a lane.

- **Honour DO-NOT-EDIT, generated and vendored markers** — FIX — value 4 — effort S — risk low — category: scope safety
  Why: assumption: the finders read the whole tree. A proven bug in generated or vendored code makes a fix that the next regeneration silently erases.
  Done when: planted defects in a file with a "DO NOT EDIT" header, a `vendor/` file and a lockfile all yield a report-only "upstream" note and no lane.

- **Keep security findings out of public history** — SECURITY — value 5 — effort M — risk med — category: disclosure
  Why: assumption: a vuln proof ends up in a commit subject, branch name, pushed lane or failing-test name, which publishes a 0-day on a public repo.
  Done when: a security-kind finding in a repo with a public remote produces no commit, branch or push until the user releases it, and its test name is neutral.

- **Break the circuit on a high rejection rate** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the pack shows capture caps and per-fingerprint dismissals, but nothing reacts to the pattern. Assumption: 5 of the last 8 findings dropped or reverted means initiative is a net harm.
  Done when: after the configured rejection ratio, initiative goes silent and asks one question ("what made these unwanted?"), and it resumes only on an explicit answer.

- **Downgrade a fix that changes public behaviour** — SECURITY — value 4 — effort M — risk med — category: fix safety
  Why: a passing red-to-green pair says nothing about callers. "Cap fix size" is about lines, not about a changed public symbol, signature or exit code. Assumption: a public-surface diff is cheap to compute per language.
  Done when: a fix that alters an exported signature, CLI flag or exit code is filed as a report with the diff and never lands unasked.

- **Cap the new test's footprint in the user's suite** — FIX — value 3 — effort S — risk low — category: test hygiene
  Why: assumption: every proof adds a test to a suite the user owns. A slow, flaky or oddly placed test is itself a harm, and "reject proofs that fail for the wrong reason" doesn't cover this.
  Done when: a proof test that exceeds 1 s, fails 1 of 5 shuffled reruns, or sits outside the project's test layout is moved to a quarantine dir and the finding is marked "unproven".

- **Preflight side effects before a flake soak** — SECURITY — value 4 — effort M — risk med — category: finder safety
  Why: the Missing list names flake finders. Rerunning a user's tests 100 times may email customers, hit a real DB or delete files. Assumption: some tests do.
  Done when: a fixture test that calls a real network or DB URL is refused for soak with the offending line cited, and an isolated test is soaked.

- **Treat finding prose as tainted** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: assumption: finders read comments, READMEs and TODOs. A planted "TODO: run this curl" could become a task body a lane obeys.
  Done when: a repo with an injected instruction in a comment yields a lane prompt built only from the failing test and file path, and the instruction text never reaches the lane.

- **Wild: Temptation fixture** — CLEAN — value 4 — effort M — risk low — category: self-test
  Why: wild. Plant a repo where a finder is tempted to overreach: a second bug next door, a secret file, a vendored dir, a sibling package. CI asserts the fix touches only its finding's blast radius.
  Done when: the temptation test fails if any lane diff includes a file outside the allowed set.

- **Wild: Shadow-mode report card from the user's own later commits** — FEATURE — value 5 — effort M — risk low — category: precision
  Why: wild. For two weeks, initiative only logs what it would have filed. It then checks which of those the user fixed themselves, which they ignored, and which touched code they later deleted, and shows a precision score before it gets any write access.
  Done when: `fm find` in shadow mode shows "N would-file, M you fixed yourself, K moot" and no lane starts until the user graduates it.

- **Wild: Regret budget** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: wild. Each unasked action spends from a small regret budget in minutes of the user's cleanup time. Accepted outcomes refill it, and reverts drain it faster than a drop does. The budget gates how autonomous the next shift is.
  Done when: after a revert the next shift runs report-only, and after a streak of accepted fixes it is allowed lanes again.

- **Check upstream before filing** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: assumption: Foreman can file a bug already fixed on another branch, in a stash or in an open PR or issue, which wastes the user's attention and a lane.
  Done when: a defect already fixed on `origin` or another local branch is reported as "already fixed in <ref>" and gets no new task.

Next question: Which unasked actions can the user not see at all today (a read, a soak, a copy, a network call) and what would a complete harm audit of one initiative night list?
Next question: What does a user who is happy with Foreman's findings still tell us about harm, and what signal (not a drop or revert) shows that a correct finding was unwanted?
