# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Resolve state from the git common dir so evidence and lease work in any worktree** — FIX — value 5 — effort S — risk low — category: reliability
  Why: the pack says evidence and lease commands fail inside the builder worktree the harness put the agent in. When the host changes the cwd, Foreman's verbs stop working and the host effectively replaces it.
  Done when: in a linked worktree, a detached HEAD and a symlinked path, `fm evidence` and `fm lease` return the same task state as in the main checkout, covered by a red-first test.

- **Run a worktree and cwd parity matrix over every verb the goal path calls** — FIX — value 4 — effort M — risk low — category: reliability
  Why: the one worktree bug probably isn't alone. Assumption: other verbs also read `./.sampo` or the repo toplevel.
  Done when: a test calls each goal-path verb from five cwd shapes, and any divergence from the main-checkout output fails the build.

- **Score every goal against a "plain host plus one paragraph" arm** — FEATURE — value 5 — effort M — risk med — category: necessity
  Why: Foreman is obsolete the moment a bare host with a short prompt finishes the 6 long-horizon scenarios as well. The pack shows 0/6 true done, so the real gap to the bare model has never been shown to be positive.
  Done when: a free-arm report prints true-done counts for Foreman, plain, and plain+distilled-prompt on the same replayed scenarios, and flags any scenario where Foreman doesn't lead.

- **Compile a goal into a standalone `done.sh` the repo owns** — FEATURE — value 5 — effort M — risk med — category: false-done
  Why: false dones come from the done check living inside the session that wants to finish. A plain executable check, written by a cold author who never sees the plan, survives Foreman's removal and can't be argued with.
  Done when: `done.sh` runs in a fresh clone with no Foreman installed, fails on the 6 known false-done states, and passes on a true done.

- **Mutate each goal clause away and require the done check to notice** — FEATURE — value 4 — effort M — risk low — category: false-done
  Why: a done check that passes after its feature is deleted can't tell true done from false done. This extends per-brief mutation to every clause of a multi-day goal.
  Done when: for each clause, removing its code in a scratch copy turns `done.sh` red, and unflagged clauses are listed.

- **Measure what Foreman's resume adds over the host's own compaction summary** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: resume is the worst area, with 2 of 6 needing a later fix. If a child given only the host's compaction summary resumes as well as one given Foreman's resume card, that card is dead weight.
  Done when: a kill-and-resume drill runs both arms at every step boundary and prints which steps need Foreman's state, with failures listed.

- **Mirror the plan into the host's native task list and make the ledger a view** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: assumption: the host now persists its own tasks across resume and compaction. Foreman's separate plan store then becomes a second source of truth that can drift.
  Done when: killing Foreman's state dir leaves a resumable plan in the host list, and the two copies are diffed with zero drift after a forced compaction.

- **Rebuild goal state from git plus one GOAL.md alone** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: if everything Foreman knows can be re-derived from files in the repo, a crash or an uninstall never loses the goal.
  Done when: deleting the state dir and running `fm resume` reproduces the open-step list with the same ids, checked on a recorded multi-day goal.

- **Keep a retire-when counter on each goal-path capability, fed by the long-horizon tier** — FEATURE — value 3 — effort S — risk low — category: necessity
  Why: the necessity corpus idea is generic. Here each of plan, lease, evidence and resume gets its own count of runs where the bare arm did equally well, and a threshold that files a retire task.
  Done when: `fm doctor` shows each of the four with a bare-arm tie count and flags any at the threshold.

- **Wild: add `fm goodbye --rehearse` to price leaving Foreman for one goal** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. Showing the user exactly what would break if Foreman vanished mid-goal makes the exit cost a number and keeps the product honest.
  Done when: the command removes Foreman in a scratch copy of a live goal, runs the goal to its end, and prints the steps that failed or were lost.

- **Wild: shrink Foreman to a verdict endpoint any agent can call** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: wild. If hosts absorb planning, resume and loops, the one thing a model can't do for itself is independent judgement of its own done claim. Accept `claim.json` by file drop and return a signed pass/fail/unmeasured with the evidence.
  Done when: a Codex or Gemini session submits a claim with no Foreman hooks installed and gets a verdict file, with a false claim rejected.

- **Wild: hold a monthly "native-parity week" where the host's goal feature drives and Foreman only audits** — FEATURE — value 3 — effort M — risk med — category: necessity
  Why: wild. Hosts will ship their own goal loops, and Foreman's best case then is an auditor. Running this week once shows whether its checks still catch what the native loop misses.
  Done when: one replayed multi-day goal runs under the native loop with Foreman read-only, and the report lists each false done Foreman's audit caught.

Next question: which of the six false dones would a cold, different-model acceptance author have caught before any building started?
Next question: what exactly does the host's own resume and goal machinery do today, and which Foreman goal verbs duplicate it?
