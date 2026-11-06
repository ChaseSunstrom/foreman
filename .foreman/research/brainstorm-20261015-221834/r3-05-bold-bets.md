# Brainstorm — lens: bold bets

- **Make `.foreman/` a git-merge-aware brain with a custom merge driver** — FEATURE — value 5 — effort M — risk med — category: portability
  Why: the user steered "fixes must travel with git"; T-1032 ships hints in git, but the ideas so far (content-addressed files, bundles) don't say what happens when two clones learn different things about the same obstacle. Assumption: concurrent edits to hint/lesson files will conflict today.
  Done when: two branches each add a different outcome score to the same hint, `git merge` resolves without conflict markers, and `fm doctor` shows the merged score as the sum of both.

- **Resume a builder by replaying its intent journal into a fresh worktree** — FEATURE — value 5 — effort L — risk med — category: resume
  Why: T-1028 (resume stopped worktree builders) is only planned; the user asked "resume easily if a session was stopped". A branch alone loses the brief, step state and the "why" of the last edit. Assumption: tool intents are journaled per step.
  Done when: after `kill -9` of a builder mid-task, `fm resume T-xxxx` creates or reuses the worktree, restores the brief and step rail, and the builder's first message names the last completed step.

- **Gate "learned" hints behind a replayable scenario that must go red→green** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: hints pulled from git are untrusted, and the user complained Foreman doesn't genuinely improve. A hint with no proof it fixes anything is a prompt-injection vector and noise. Assumption: obstacle transcripts can be reduced to a runnable repro.
  Done when: a hint without a repro that fails before and passes after is refused by `fm hints import`, with the reason printed.

- **Add `fm improve`: a weekly self-experiment with A/B holdout** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: the user asked "why have you not really improved all that much?" Many scorecard ideas exist, but none does a controlled test. Assumption: ~20% of eligible tasks can run without a new rule.
  Done when: after N tasks, `fm improve report` shows per-rule pass-rate and interventions with vs. without it, and auto-proposes retiring rules whose difference is not significant.

- **Let the user's corrections become rules the moment they say them** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the steered list shows repeated corrections ("no gaps", "fills the dock exactly", "include wants from other people"). Each took multiple rounds. Assumption: a layout/style correction can be encoded as a testable check.
  Done when: after a "still cluttered" style steer, a new check appears in `fm rules` and the next UI task fails its gate if the check breaks, citing the user's quote.

- **Run a persistent supervisor that adopts orphan agents across sessions** — FEATURE — value 4 — effort L — risk high — category: fleet
  Why: stopped sessions strand worktree agents and `claude -p` children (orphan-reaping and heartbeat ideas exist, but nothing owns them after the session dies). Assumption: a small user-level daemon or systemd timer is acceptable.
  Done when: killing the parent session leaves its builder running to a checkpoint, and the next session's pane lists it as "adopted" with its progress.

- **Pre-register a task's success test before building, then score the builder against it** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the user's "proof by commands it ran" ethos, and the T-0990 incident where tests silently reached the paid binary shows tests can be wrong. A second agent writes the acceptance check without seeing the implementation.
  Done when: for an L task, an acceptance test file written by a separate lane exists with a commit earlier than the implementation, and close fails if it was edited afterwards.

- **Publish a project's brain as a signed pack with trust levels** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: the user wants fixes to travel "transferable in git or something". Machine-wide fixes live in Foreman state, so they can't be shared. Assumption: a pack is a directory plus a manifest hash.
  Done when: `fm pack export` yields a directory; `fm pack import` on a clean machine shows each item with its origin and requires `--trust` before any hook-affecting item is active.

- **Wild: Dream-time dojo that mutates past failures to find unprevented variants** — FEATURE — value 4 — effort L — risk med — category: self-improvement — wild
  Why: assumption: replaying exact failures only proves what was fixed. Mutating them (different path, tool, wording) finds where a hint is too narrow.
  Done when: an overnight run writes a report listing at least one variant of a recorded obstacle that the current hints fail to catch, with a drafted widening.

- **Wild: Foreman interviews the repo's git history on adoption and drafts the first brain** — FEATURE — value 4 — effort M — risk low — category: onboarding — wild
  Why: assumption: reverts, "fix" commits and CI-red-then-green sequences hold obstacle→fix pairs already. A new project then starts with a brain rather than empty.
  Done when: `fm adopt` on a repo with 200+ commits proposes at least 5 reviewable hints, each citing the commit pair that produced it.

- **Wild: Let two machines' Foremen negotiate a task split through a shared branch** — FEATURE — value 3 — effort L — risk high — category: team
  Why: assumption: a `foreman/queue` ref with leases lets a laptop and a desktop work one queue without a server. Builds on the lease and team-mode ideas.
  Done when: two clones run `fm next` simultaneously and receive different tasks, with the lease visible in both panes.

- **Wild: Show a "ghost" of the previous attempt in the pane on resume** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: assumption: when resuming, the user wants to see where the stopped agent got to. A dimmed Gantt/diff overlay of the earlier run, with a marker where it died, beats a text summary.
  Done when: after a resume, the Agents graph shows the old run's nodes dimmed, with a "stopped here" marker, and they fade once the new run passes that point.

- **Prune Foreman's own rule set by deletion tasks driven by the A/B data** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: backlog is 30+ deferred items and ideas list is huge. Growth without retirement is the risk. Assumption: `fm improve` data exists.
  Done when: each week one rule/hook with no measurable effect is opened as a deletion task with its evidence attached.
