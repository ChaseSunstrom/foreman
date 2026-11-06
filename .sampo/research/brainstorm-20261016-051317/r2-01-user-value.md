# Brainstorm — lens: user value

- **List what was not verified on every close** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: assumption: the review shows builders returning "done" and reviewers finding real defects. The pane was never screenshot-verified, and some verify commands were wrong. A close that says only "verified" can overstate what was checked.
  Done when: closing a task whose UI change had no screenshot or browser run prints "Not verified: UI rendering". A task with a full proof prints "Not verified: nothing known".

- **Treat questions as questions, not tasks** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: assumption: the user sends a mix of asks, bug reports and "why does X…" questions. Opening a task and plan ceremony for a question is pure overhead.
  Done when: a recorded "why is the band blank?" prompt gets an answer with no task id created. The same prompt phrased as "fix the band" creates one.

- **Detect the user's hand edits and treat them as protected steers** — FEATURE — value 4 — effort M — risk med — category: collaboration
  Why: assumption: "two sessions edit the same file" is covered, but a human saving a file mid-lane is not. A builder that overwrites it loses work and trust.
  Done when: editing a file in a lane's worktree outside Claude makes the next builder write to that file stop and ask. The ledger records the event.

- **Provide a `fm batch` transaction: plan, preview, apply, undo** — FEATURE — value 4 — effort M — risk med — category: batch tools
  Why: the user asked for "more tools and stuff to batch edit files/whatever/everything". Assumption: single edits and `fm edit` exist, but a cross-file transaction with one undo may not.
  Done when: `fm batch rename Foo Bar --dry-run` prints a diff across files. Applying it makes one checkpoint, and `fm batch undo` restores every file byte for byte.

- **Write the PR body from the task's proofs** — FEATURE — value 4 — effort S — risk low — category: shipping
  Why: assumption: "ship to a PR" exists in the ideas, but a teammate reading the PR sees none of the red→green runs, criteria or not-verified list.
  Done when: the PR opened for a closed task has Summary, Proof (the commands and results actually run) and Not verified sections, all filled from the brief and ledger.

- **Watch the merge after shipping and open a FIX task on red** — FEATURE — value 4 — effort M — risk med — category: shipping
  Why: assumption: the user said "push to main when you get a chance", so pushes happen unattended. The only check is the local gate before the push, not CI afterwards.
  Done when: after a push, `fm` polls CI for N minutes. A deliberately failing workflow produces a FIX task that names the pushed commit.

- **Show before and after for every setting change** — FEATURE — value 3 — effort M — risk low — category: settings
  Why: assumption: many toggles exist (postures, caps, palette, motion, off-files). A user can't tell what a setting will change.
  Done when: `fm set <key> <value> --preview` prints the next three hook outputs under the old and new value. A setting with no visible effect says so.

- **Scale ceremony to measured blast radius per request** — FEATURE — value 4 — effort M — risk med — category: proportionality
  Why: the Lite mode and "two-minute rule" tasks are deferred (T-0861), so every change gets the full plan and proof flow. The right depth depends on the diff's reach, not on a global mode.
  Done when: a one-line doc typo closes with a single proof line. An edit to the guard files triggers full review with no flag set.

- **Wild: Hold a Paper-cut Friday, where Foreman fixes the user's most-repeated annoyance behind a flag** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: wild. The user's steers are full of small repeats (gap between session and chat, release lag, crashes on subagent outline lists). Foreman clusters them, picks the top one weekly, and ships it opt-in with an undo line.
  Done when: running `fm friday` names one annoyance with its supporting steer quotes and produces a flagged branch with a passing proof.

- **Wild: Bring-your-own-stakeholder view, a static "where are we" page for people who don't use Foreman** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild. The user's collaborators and future self read GitHub, not the pane. A single self-contained HTML (queue, shipped this week, what is blocked on whom) generated with `fm status --html`, sanitised of paths and secrets.
  Done when: the generated file opens offline, shows the three sections, and a scan finds no absolute home paths or tokens in it.

- **Wild: Offer a "second life" for rejected diffs, an archive of reverted or skipped work that resurfaces when relevant** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: wild. The user says "skip" and revert often, and the work vanishes. Keeping the diff as a stat-keyed patch and surfacing it when a new task touches the same files saves rebuild time.
  Done when: reverting a task stores its patch. Opening a new task on the same file prints "an earlier attempt exists: T-xxxx" with the patch path.

- **Wild: Render a "state of the union" on bare `fm` after any gap of more than a day** — FEATURE — value 4 — effort S — risk low — category: return
  Why: wild. The user goes AFK for long stretches and wants no questions. Show only what changed in plain words: shipped, blocked on you, and the first thing to do, with a single command to accept the default.
  Done when: running `fm` after 24 or more idle hours prints at most 12 lines ending in one copy-pasteable command. Run again within an hour it prints the normal output.
