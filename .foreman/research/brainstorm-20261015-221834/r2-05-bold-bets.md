# Brainstorm — lens: bold bets

- **Make Foreman a git-native "brain" that merges like code** — FEATURE — value 5 — effort L — risk med — category: portability
  Why: the user steered that fixes must travel with git for any project; ideas so far cover hints and bundles but not conflict-free merging of two clones' learnings. Assumption: hints are per-file, so merge conflicts are the real teammate blocker.
  Done when: two clones each learn a different fix, both push, and `git pull` on a third clone yields both hints with no manual merge and `fm doctor` reports them active.

- **Replay any past failure as a runnable scenario** — FEATURE — value 5 — effort L — risk med — category: evals
  Why: T-0035 (eval capture) is deferred and the "dojo" and replay ideas are only wilds. A scenario is a failing task's repo snapshot, prompt, and the check that failed. Evidence: the folder-trust stall and the shot.py Stop-hook capture were both found by accident.
  Done when: `fm scenario run <task-id>` rebuilds the repo state in a temp worktree, runs the recorded check against current Foreman, and prints pass/fail.

- **Ask the model to prove a hint before it's trusted** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: hints pulled from git are an injection path (T-0791 deferred, only "untrusted input" mentioned). Assumption: hints can contain commands. Each hint should declare an allowlisted action type (env var, flag, file edit) and never free-form shell.
  Done when: a hint containing an undeclared shell command is rejected at load with a named reason, and a test covers it.

- **Show "what Foreman would have done" on the first run in a new repo** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: T-0861 to T-0864 (lite mode, tour, start ladder) are all deferred for lack of evidence; a dry-run preview produces that evidence. Assumption: newcomers fear bypass-mode surprises.
  Done when: `fm preview` on a fresh clone lists the gates, guard rules and cards that would fire, from its map, with no state written.

- **Give every worktree agent a signed-off exit report** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: resume (T-1028) covers restart; the pack has no unified "what I did, what's left, what I'm unsure of" artifact when a builder stops cleanly or not. The report would be the first thing resume reads.
  Done when: a builder killed mid-step leaves a report generated from the ledger and git diff, and `fm resume` prints it before continuing.

- **Auto-write the regression test for each blocker you solved** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: the user's "dropped" items repeatedly say "catch it earlier: no test covered this". That is a recurring pattern. Closing a task that hit an obstacle should draft a test that fails without the fix.
  Done when: closing an obstacle-fix task creates a test file that fails when the fix is reverted, verified by Foreman's mutation check.

- **Rank Foreman's own roadmap by user corrections** — FEATURE — value 4 — effort S — risk low — category: self-improvement
  Why: the user asked "why have you not really improved". 30 deferred "Later from" tasks sit unranked. Count how often each theme appears in steers and drops and surface the top three at SessionStart.
  Done when: `fm next --why` shows each queue item's count of matching user requests, and ordering changes when a new correction is logged.

- **Provide a "team mode" so several people's Claude sessions share one queue** — FEATURE — value 4 — effort L — risk high — category: collaboration
  Why: steer asks for teammates and clones to benefit; queue and locks are local today. Assumption: tasks live in files that can sync via a git branch.
  Done when: two clones claim different tasks from a shared `foreman-queue` branch and neither can claim the other's.

- **Make the pane a flight recorder you can scrub** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: the pane work is a heavy user focus (graphs, tree, Agents); a past-session scrubber builds on the same ledger. Wild.
  Done when: `fm ui --at <time>` renders the pane exactly as it looked at that moment from the ledger.

- **Let Foreman write its own pull request against itself from field failures** — FEATURE — value 5 — effort L — risk high — category: self-improvement
  Why: the user wants it to "genuinely improve itself". When a hint recurs three times across projects, draft a patch to the plugin and its test in a worktree for human review. Wild.
  Done when: a repeated obstacle produces a branch with a failing-then-passing test and a PR body citing the sessions that hit it.

- **Run a "second opinion" model on every guard allow in bypass mode** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: T-0275 (guard reads what scripts run) is deferred, so indirect commands escape pattern matching. A cheap Haiku judge on ambiguous commands only could catch what regex can't. Assumption: cost is acceptable if limited to unparsed scripts.
  Done when: a bash invocation of a script containing `rm -rf ~` is blocked while a benign script runs unimpeded, with the judge called only for the script case.

- **Wild: Let projects publish their Foreman brain as a package others can install** — FEATURE — value 3 — effort L — risk med — category: ecosystem
  Why: with portable hints and cards, a popular repo's learnings (e.g., "Tauri on Arch needs libappindicator") could be installed by anyone who adds that dependency, scrubbed and versioned. Wild.
  Done when: `fm brain add <repo-url>` imports that repo's hints and cards under a quarantine label until reviewed.

- **Wild: Have a pocket "bug-bounty" run where Foreman attacks its own guard** — SECURITY — value 3 — effort M — risk low — category: red-team
  Why: the guard stops commands in bypass mode; no adversarial corpus is mentioned. A nightly agent tries to get dangerous commands through, and each success becomes a guard test. Wild.
  Done when: a seeded bypass gets found, filed as a task and covered by a new guard test within one run.

- **Wild: Turn the idle pane into a morning briefing** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user cares about no empty space in the pane. When nothing is running, show what changed since last session, what's stuck, and the one thing to do next. Wild.
  Done when: opening the pane after a 12-hour gap shows a briefing with completed, blocked and next items instead of empty lanes.
