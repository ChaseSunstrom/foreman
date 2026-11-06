# Brainstorm — lens: bold bets

- **Race fixes in worktrees and merge the proven smallest** — FEATURE — value 5 — effort L — risk med — category: best-of-n
  Why: assumption: Foreman already has lanes and `fm task prove`, so two strategies can run side by side and only the one whose proof passes is kept. Two fixes that both pass are a tie, so pick by smaller diff.
  Done when: on a seeded bug, two strategies run in separate worktrees, the passing one with the smaller diff is merged, and the other worktree is removed.

- **Write acceptance tests from the request before any edit** — FEATURE — value 5 — effort M — risk low — category: spec-first
  Why: the user's pushback ("I want any and ALL ideas implemented") shows that what was asked and what was built drift apart. Tests written from the request text, before implementation, make that drift visible.
  Done when: a task with request text gets a read-only test file, and the guard hook refuses an edit to that file.

- **Turn each rules-file line into a test or hook, then delete the prose** — CLEAN — value 4 — effort L — risk med — category: rules enforcement
  Why: the rules file has been over the doctor's 6,400-char budget since T-1520 (6,416), so prose isn't holding. Rules a test or hook enforces don't need to be read by the model.
  Done when: the rules file is under 6,400 chars, and every deleted line maps to a named test or hook that fails when the rule breaks.

- **Close each task only after a different model family signs off** — FEATURE — value 4 — effort M — risk low — category: cross-model verify
  Why: assumption: a second CLI adapter can run a read-only review. Same-model red-teaming shares the builder's blind spots, and T-0335 shows adapters are already a planned surface.
  Done when: a close needs a verdict from a second CLI, and the verdict and its model appear in the receipt.

- **One event journal that every surface reads** — CLEAN — value 4 — effort L — risk med — category: single source of truth
  Why: assumption: the web UI, the desk card, the pane and `fm status` each render run state separately, which is why the pack shows drift between them (T-1615, T-1217). One journal, many readers, removes that class of bug.
  Done when: `fm status`, the pane and the desk card print the same run state from one journal file, verified by a test that changes the journal and checks all three.

- **Move a half-finished run to another machine as a git bundle** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: assumption: a user who starts on one machine may want to finish on another. A bundle carries the branch, journal and leases, so resume works without the original host.
  Done when: `fm run export` on machine A and `fm run import` on machine B resume the run at the same step, with leases released on A.

- **Wild: distil a small local triage model from closed tasks** — FEATURE — value 4 — effort L — risk high — category: local model
  Why: wild. Assumption: closed tasks with outcomes label good and bad routing decisions. A small local model could pick playbooks and gates with zero API tokens, which is the pack's core cost goal.
  Done when: on held-out closed tasks, the local model matches the recorded playbook choice at least 90% of the time with no network calls.

- **Wild: a code ping-pong where the test suite keeps score** — FEATURE — value 2 — effort S — risk low — category: play
  Why: wild. Two agents trade a fix and a break, and the tests referee each round. It turns the adversarial loop into something watchable, and the scoreboard is a joy to share.
  Done when: a 10-round match ends with a green suite and a score line recorded in the journal.

- **Wild: a nightly dream pass that proposes rules edits from your corrections** — FEATURE — value 4 — effort M — risk med — category: self-tuning
  Why: wild. The pack lists many user corrections that recur across runs. The dream pass drafts rule changes, each citing the correction it came from, and the user accepts or rejects them in the morning.
  Done when: each morning proposal carries the source correction, and no rules change lands without an accept.

- **Stop a run the moment its estimated cost passes the task's budget** — FEATURE — value 3 — effort S — risk low — category: budget guard
  Why: assumption: the pack already tracks tokens per reply (`fm cost`). A pre-check against a per-task estimate catches a run that's going over before it burns the budget.
  Done when: a task with a 50k-token budget is stopped at the estimate and returns a receipt showing the stop point.

- **Give every closed task a re-run button from a clean checkout** — FEATURE — value 3 — effort M — risk low — category: reproducibility
  Why: assumption: "it passed on my machine" is the failure to catch. Re-running a closed task from a clean checkout and diffing the result proves the proof holds.
  Done when: `fm task rerun <id>` in a clean clone reports pass or fail and the diff from the original result.
