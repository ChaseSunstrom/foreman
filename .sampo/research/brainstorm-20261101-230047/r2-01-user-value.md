# Brainstorm — lens: user value

- **Wake deferred tasks on their revisit date** — FEATURE — value 4 — effort S — risk low — category: schedules
  Why: T-2541 now records a revisit date when a Mission task is deferred, and about 30 deferred "Later from T-07xx" rows have no clock. Nothing reads the date.
  Done when: a deferred task with revisit date D is re-offered by `fm next` on D (tested with a faked clock), with no session open at the time.

- **Arm a ship with one yes** — FEATURE — value 5 — effort M — risk med — category: ship, CI
  Why: the push grant exists, and each push already goes through `fm ship` and `fm ci-watch --last-ship`. The user still has to be present at the moment of the push. Assumption: an explicit "arm" is a fresh, task-scoped grant, so it respects "approval doesn't extend".
  Done when: `fm ship --arm T-N` queues one push that fires once, only when the full check is green and the tree hash is unchanged. It is spent on use, and a changed tree disarms it with a stated reason.

- **Triage bot PRs in a lane** — FEATURE — value 4 — effort M — risk med — category: watchers
  Why: `fm pr train` already runs the self-change gate on each PR head before merging (T-2430). Nothing starts it when a dependency-bot PR appears. Assumption: the user gets these PRs.
  Done when: a fixture bot PR is picked up by the watcher, run through the gate in a worktree, and a verdict card is left (merge-ready or the failing gate). Nothing is merged without the user's yes.

- **Run `fm night undo` for a whole night** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: the pack's self-start ideas cover branches and stamps but not one command that reverses everything a night created (tasks, captures, notes, branches). The user installed the timers, so the "what if I dislike it" cost is theirs.
  Done when: after a simulated night that filed 3 tasks and 1 branch, `fm night undo <date>` removes exactly those, lists them, and leaves the user's own edits alone.

- **Fire a lane when a test is saved red** — FEATURE — value 4 — effort M — risk med — category: file triggers
  Why: file triggers are on the Mission, but the pack proposes only generic ones (drop folder, git events). The concrete need is a failing test saved by the user. Assumption: the repo has a fast per-file test command from `fm map`.
  Done when: saving a red test in a fixture repo drafts a fix diff in a worktree within N seconds and shows it as a card. The user's tree is untouched, and a second save inside the debounce window doesn't start a second lane.

- **Read `fm:` marker comments as triggers** — FEATURE — value 3 — effort S — risk low — category: file triggers
  Why: assumption: users already leave TODOs. A line such as `# fm: when CI green, bump this` is the cheapest way to say "do this later" without leaving the editor.
  Done when: a marker in a committed file yields one capture with its file:line, and removing the marker withdraws the capture.

- **Add `fm away 3d` as one verb** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the steers say the work shouldn't stop for the user's absence, but the pack proposes charter, budget, stop file and autonomy dial as separate pieces. The user wants to say "I'm gone" once.
  Done when: `fm away 3d` writes a charter, a spend cap and a stop file path, shrinks autonomy, and queues the return briefing. `fm back` shows what ran and what waits for a yes.

- **Answer why a trigger fired or didn't** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: `fm triggers` shows precision after the fact, and the night tick "logs only when something happens", so silence is ambiguous. A user can't tell "nothing to do" from "broken".
  Done when: `fm triggers why NAME` prints the last evaluation (time, event seen, rule matched, skip reason) for a trigger that didn't fire, from a log written by the tick itself.

- **Show a yes inbox page in the web UI** — FEATURE — value 4 — effort M — risk med — category: web UI
  Why: the web UI is the only surface in this mission. Queued installs, arms and merges need one place with y/n keys, the exact unit text, enable and uninstall lines, and an empty state. Assumption: the endpoint writes through a user-run path the model cannot call.
  Done when: a queued timer shows its unit text. Pressing y installs it once, pressing n records a reason, and an empty queue shows an intentional empty state. A model-side write to the queue file is refused.

- **Rebase onto teammates' pushes in a scratch tree** — FEATURE — value 3 — effort M — risk low — category: git events
  Why: assumption: the user shares repos. A foreign push is the event that most often silently invalidates a branch.
  Done when: a push to the tracked remote branch triggers a scratch-worktree rebase and a one-line card ("clean", or "conflicts in X, Y"). The user's branch is never moved.

- **Wild: Turn a sentence into a trigger** — FEATURE — value 4 — effort L — risk med — category: natural language
  Why: wild; the user reasons in "whenever CI goes red on main, brief me." `fm triggers` already stores trigger kinds, so the missing piece is compiling a sentence into one reviewable row.
  Done when: five sentences compile to rows that each show their kind, source, action, budget and expiry. An unsupported one is refused with the nearest supported form.

- **Wild: Let a failed lane stand in for the user's morning** — FEATURE — value 3 — effort M — risk low — category: briefing
  Why: wild; a morning note that reads as ranked decisions with the minutes each unlocks, not a log. The aim is for the user to answer three yeses in under a minute.
  Done when: a fixture night with 6 parked items yields one note sorted by minutes unlocked, each with a one-word answer. The answers are applied on the next tick.

- **Wild: Offer a rehearsal week before any timer installs** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: wild; the user's one yes to an install is hard to judge blind. Replaying their last seven days' commits, CI runs and captures against the proposed trigger shows what would have fired.
  Done when: the install card lists would-have-fired events from recorded history, with a count and the first three. If history is empty the card says "no history" instead of a fake zero.

Next question: Which of the 59 empty cells are about the web UI surface itself (inbox, toggles, fire log), and which are really tick or CLI cells wrongly assigned to it?
Next question: What does a user who installed the timers actually do the morning after a self-started lane lands (accept, ignore, undo), and is that logged anywhere?
