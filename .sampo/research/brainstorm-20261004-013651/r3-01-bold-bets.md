# Brainstorm — lens: bold bets

- **Compile the brief into an executable contract the hooks enforce** — FEATURE — value 5 — effort L — risk med — category: enforcement
  Why: criteria already carry verify commands, but "done" is still assembled by prose and evidence checks. Assumption: criteria can be machine-typed (exit code, file exists, output regex) so the Stop hook computes done from a contract, not from the model's claim.
  Done when: a brief whose criterion is edited after evidence was recorded is flagged stale by `fm check`, and a Stop with an unmet typed criterion is refused with the criterion's id.

- **Dedupe the inbox by merging overlapping items into three pipelines** — CLEAN — value 4 — effort S — risk low — category: planning
  Why: the inbox lists ~20 items (bench judge, regression court, shadow-user soak, counterfactual ledger, skill duels, sentinel) that all replay the past against a candidate. Assumption: they share one replay harness in fmbench. Cut the three least separable.
  Done when: `fm next` lists at most 3 replay-family items, each naming the cut items it absorbed.

- **Detect and quarantine git object corruption at session start** — FIX — value 4 — effort S — risk low — category: reliability
  Why: four zero-byte loose objects broke `git diff` and `fm doctor` passed. Cheap check: find zero-size files under .git/objects, plus `git fsck --connectivity-only` at SessionStart.
  Done when: a test repo with an empty loose object makes `fm doctor` fail naming the file and the move-aside command.

- **Add an interrupt-safe "turn budget" so the drive stops for the user only on real decisions** — FEATURE — value 4 — effort M — risk med — category: drive
  Why: 18 drive turns ended only to wait on a reviewer. Assumption: the Stop hook can return a block-with-reason while background_tasks is non-empty.
  Done when: replaying a recorded session with a pending reviewer yields zero turn-ends before the report arrives.

- **Turn each guard false positive into a precision corpus entry before fixing it** — FIX — value 4 — effort S — risk low — category: guard
  Why: `git stash list`, read-only python on state files, and a source-editing heredoc were blocked. The guard must only get more precise, so each needs an allow and a still-block twin case.
  Done when: the three commands pass and their mutating twins (`git stash drop`, python writing state) still block, in test_guard.

- **Wild: Let the user type "bet" on any plan and have Foreman wager a measurable outcome** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Briefs state a tier, and reviews find 3–7 issues each time, so estimates are untested. Foreman records predicted tier, steps and review findings, then scores its own calibration per task type and shifts tiers.
  Done when: `fm calibration` prints predicted vs actual tier hit rate over the last 20 tasks.

- **Wild: Build a "reviewer's memory" so audits stop rediscovering the same edge cases** — FEATURE — value 4 — effort M — risk low — category: review
  Why: wild. Findings are mostly parser edge cases and export privacy. Cluster past findings into a checklist injected into the reviewer prompt only when the diff touches a matching file type, so reviewers start from known failure shapes.
  Done when: a diff adding a parser gets a review prompt containing prior parser-finding classes, and `fm friction` shows a falling findings-per-batch count.

- **Wild: Make a cold-open "Foreman explains itself to a newcomer" mode inside the pane** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: wild. The stranger test finds stalls offline. A live version lets the pane answer "why was I blocked" from a stable reason code with the exact allow command and its cost.
  Done when: every guard block prints a reason code, and `fm why CODE` returns the rule, the evidence behind it and the narrowest allow.

- **Add a load-aware gate scheduler with a flake ledger** — PERFORMANCE — value 3 — effort S — risk low — category: gates
  Why: a flaky test class failed once under load and passed on rerun, so reruns hide real signal. Assumption: the loadavg is readable. Record each failure with the load figure, and rerun only when load exceeded a threshold at the time.
  Done when: a failure recorded at high load is marked "load-suspect" and reruns once, while a failure at low load is not rerun.

- **Wild: Spend the research cache as a shared team knowledge pack** — FEATURE — value 3 — effort L — risk high — category: research
  Why: wild. Verified research notes with quote checks are a reusable asset across projects. A redacted, signed export other installs may import with a trust tier. Needs the secret and path scan first, and nothing leaves the machine without the user's yes.
  Done when: `fm export research` writes a bundle that fails to build if any path or secret pattern remains, and `fm import` marks every claim as "foreign, unverified" until it re-checks.

- **Cut or merge: drop "second-Foreman daily review" into the reviewer's memory** — CLEAN — value 2 — effort S — risk low — category: planning
  Why: both read past transcripts for recurring misses. One feedback store is enough.
  Done when: the inbox shows one item, with the merged scope in its criteria.
