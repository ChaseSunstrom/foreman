# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Capture evidence passively from the PostToolUse hook and transcript** — FIX — value 5 — effort M — risk med — category: goal evidence
  Why: evidence and lease commands fail inside the builder worktree, because the agent has to call a verb that resolves state from the wrong cwd. If hooks record every command, exit code and output hash as the tool call finishes, the agent never calls `fm evidence`. The path is also host-native, so it survives a stronger model that stops calling verbs.
  Done when: in a harness-created worktree, a goal clause is proven by an ordinary test run and the clause shows evidence in the main ledger, with no `fm evidence` call anywhere in the transcript.

- **Use a git ref as the lease** — FIX — value 4 — effort M — risk med — category: crash resume
  Why: leases fail in worktrees and crashes leave them stale. Refs live in the common git dir, so `git update-ref` with an expected old value works from any worktree and is atomic. The ref's commit date can serve as the heartbeat.
  Done when: two worktrees race for one task and exactly one wins. After a SIGKILL of the winner, a third worktree takes the lease once the heartbeat is stale and never before.

- **Render the "done" message from the clause ledger** — FIX — value 5 — effort M — risk med — category: false done
  Why: the long tier shows 0/6 true done, with the 6 false dones unchanged since gen 2. The model's prose is where "done" gets asserted. The Stop hook can instead build the final status line from clause states and block any model text claiming completion that the ledger doesn't back. A stronger model then has no more authority to declare done than a weaker one.
  Done when: replaying the six false-done transcripts, none ends with a completion claim the rendered line contradicts.

- **Keep a sealed holdout acceptance check the builder can't read** — SECURITY — value 4 — effort M — risk med — category: done gate
  Why: assumption: some false dones are tests bent to pass. A different-model child writes the acceptance check from the goal words alone, outside the worktree, and only its hash is recorded. It runs at close, and the builder sees pass or fail plus the failing clause names, never the test body.
  Done when: a builder given a goal with a planted shortcut can't pass the holdout without the real work, and the check file is unreadable from the builder's cwd.

- **Build a cheapest-catcher table for each false done** — CLEAN — value 4 — effort M — risk low — category: obsolescence
  Why: this is the inversion in practice: for each of the six false dones, find the cheapest intervention that still catches it. The ladder is one prompt line, then a hook regex, then a cold child, then the full gate. Anything the prompt line catches on the current model gets its heavy mechanism demoted.
  Done when: a table maps six incidents to a tier. At least one mechanism is removed or demoted on evidence, or the table says none could be.

- **Mine plain-host sessions as a natural control** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: the ledgers show spans where Foreman was off or the hooks failed open, and the user's own re-asks and "continue" prompts there are free data. Compare true-done and re-ask rate for goals run on and off, at zero tokens, instead of building more synthetic tiers.
  Done when: one command prints re-ask and reopen rates for on-spans against off-spans, with counts and the caveat that the spans weren't randomised.

- **Require a "most likely still wrong" line in every done claim** — FEATURE — value 3 — effort S — risk low — category: false done
  Why: a pre-mortem is a prompt-level mechanism that works on any host and any model. The Stop hook requires the line and the verifier checks that item first. If the model's guess is often right, that shows it knew the claim was weak.
  Done when: a done claim without the line is bounced. Over 20 goals, the share of lines the verifier confirmed as real gaps is logged.

- **Go dormant when the host's compaction rate drops** — PERFORMANCE — value 3 — effort S — risk low — category: obsolescence
  Why: much of the resume machinery exists because compaction loses the goal. Count compactions and resumes per goal from transcripts. When a new model or host makes them rare, stop injecting the resume card and re-arm it if the rate climbs.
  Done when: a rolling-window threshold in `fm doctor` shows the resume card as dormant or armed. A synthetic compaction burst re-arms it within one session.

- **Lint plan steps for restartability with pre- and post-checks** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: the best resume is no resume. Each step carries a shell post-condition. Resume runs the post-conditions from cold and starts at the first one that fails, so any fresh session can restart from repo state alone. Steps with no checkable post-condition are flagged at filing.
  Done when: after killing a session mid-goal, a fresh session reaches the same first unmet step as an uninterrupted run, with no memory of the dead session.

- **Add a critic-only profile for hosts with a native goal loop** — FEATURE — value 4 — effort M — risk med — category: role inversion
  Why: if hosts take over planning and carrying a goal, the part left is independent judgement. In this profile Foreman doesn't plan or lease. It only attacks done claims and renders unmet clauses, and it is much smaller than the full goal path.
  Done when: with the planning and lease verbs disabled, the Stop-gate still bounces the six false dones and `fm doctor` reports the profile.

- **Wild: Cut a real transcript at a random turn and replay the continuation** — FEATURE — value 4 — effort M — risk low — category: long tier
  Why: the long tier is expensive and planted faults are artificial. Real finished goals give unlimited resume scenarios. Cut one at a random turn, hand a fresh plain host only Foreman's resume card, and score whether it reaches the same end state.
  Done when: one command samples 10 past goals and cut points, runs them, and prints matches with the cut turn for each miss.

- **Wild: Have each new model interview the harness** — FEATURE — value 3 — effort S — risk low — category: obsolescence
  Why: when a new model ID is seen, give it MASTER.md's goal section and ask which rules it would never need and which it would break. Then test each claim against the replay arms. Cheap, and it aims the next removals.
  Done when: a model-ID change writes a one-page list of claimed-unneeded rules, each marked confirmed, refuted or untested.

- **Wild: Earn the veto with a shadow Foreman** — FEATURE — value 3 — effort L — risk med — category: trust
  Why: assumption: a plain host drives while Foreman only predicts "done" or "not done" from the transcript. It may block only after beating the plain host's own verdict on 30 goals, and it loses the veto when precision drops. If it never earns it, that is itself the obsolescence verdict.
  Done when: a ledger of predictions against later outcomes exists, and the veto flips on or off by the stated rule on replayed history.

Next question: which of the goal path's mechanisms did the user ever notice by effect, as opposed to Foreman reporting them, and would they have asked for those mechanisms by name?
Next question: if the host shipped a native goal loop tomorrow, which single Foreman output would the user still open, and does the pack show anyone opening it?
