# Brainstorm — lens: event and file triggers

- **Tail harness transcript files as the portable event source** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: T-0337 shows Gemini has no Stop hook, and T-0335 and T-0336 show non-Claude hooks are unverified. Tailing each harness's session JSONL with inotify gives "turn ended", "tool failed" and "session died" events without relying on hooks.
  Done when: a recorded Gemini or Codex transcript replayed into the tailer emits `turn_end` and `tool_failed` events, and a Claude run with hooks disabled yields the same events.

- **Fire a resume task on process death via pidfd** — FIX — value 4 — effort S — risk low — category: drive reliability
  Why: T-2900 and T-2901 and the two drive miscounts all come from guessing whether an agent or shell is alive. A pidfd or `/proc` exit event on each tracked child gives a push signal. It removes the 20-minute phantom hold and files "resume lane X" at once.
  Done when: killing a tracked builder makes the drive release its hold and file a resume within 5 s, with no polling tick involved.

- **Run the vocabulary lint on save, scoped to changed files** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user corrected the "jarvis" and "Claude as orchestrator" leaks in scenes by hand. A file trigger on `site/`, `README`, `design/` and `*.svg` saves runs the role-word lint on just that file and files a fix task if it fails.
  Done when: saving an SVG containing a banned name files a task naming the file and line within a debounce window, and a clean save files nothing.

- **Fire a steer's automatic check when the steer store changes** — FEATURE — value 4 — effort S — risk low — category: standing rules
  Why: every steer is stored with a check (`fm decide --check`), but the checks only run in a sweep. A file trigger on the steer store, gen-0 and `standing-intent.md` runs the new or changed check at once, and a failure goes to the next `fm next`.
  Done when: adding a steer whose check fails on the current tree shows a task or warning within one tick, without running `fm genesis sweep`.

- **Rebase and re-verify open lanes when main moves** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: Missions 5–8 run as parallel lanes merged in mission order, and ships go straight to main under the push grant. A "main advanced" event (ref change) rebases each open lane in a scratch worktree and re-runs its Exam. It files a conflict brief only if that fails.
  Done when: pushing a commit to main that conflicts with an open lane produces a conflict task naming the lane. A non-conflicting push yields a "still green" stamp on the lane.

- **Add `.sampo/stop`, `.sampo/pause` and `.sampo/now` sentinel files** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user wants overnight work unattended and also "stop asking me". A plain file that every trigger and the drive checks each tick gives a kill switch and a fire-now switch, usable from a phone via file sync or an SSH `touch`, with no permission prompts.
  Done when: `touch .sampo/pause` stops new trigger firings within one tick and the ledger records "paused by sentinel". Removing it resumes them.

- **Label private path globs and force triggers that touch them onto local runners** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: the pack is thin on privacy, and triggers read file contents unattended. A data-class tag on globs (secrets, mail, personal notes) makes the trigger runner refuse any non-local model for matching payloads. It fails closed and writes an egress line to the ledger.
  Done when: a file event matching a private glob run with only a remote profile configured is refused with a stated reason. With a local profile it runs and the ledger shows `egress: none`.

- **Generate a "what starts without me" doc page from the triggers file** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: docs are listed as thin. A page rendered from the declared triggers (source, glob, debounce, grant tier, last fired, fire count) cannot drift. Its numbers are computed rather than typed, consistent with the earlier computed-claims ideas.
  Done when: editing a trigger changes the rendered page on the next build, and a doc check fails if the page differs from the triggers file.

- **Sync markdown checkboxes with tasks, both ways** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: the user's habit is short typed asks. A `- [ ]` line added to a watched `TODO.md` becomes a filed brief. Ticking it closes the task only when the Exam passes, and unticking reopens it. This gives a no-CLI intake path.
  Done when: appending a checkbox line files a task carrying that line's text. A tick without a passing Exam is reverted with a visible note.

- **Wild: use a named pipe and socket as the universal trigger inbox** — FEATURE — value 3 — effort S — risk med — category: integration — wild
  Why: assumption: scripts, cron, git hooks and other agents can all `echo "brief…" > ~/.sampo/in`. The socket-activated reader tags the payload as untrusted data and applies the loop-breaker depth. It needs no HTTP or HMAC for same-user senders.
  Done when: `echo` into the pipe files one task stamped `origin: pipe` with fenced text, and a flood of 100 lines is coalesced to the configured cap.

- **Wild: a commit trailer `Sampo-next:` in the user's own commits files the follow-up** — FEATURE — value 3 — effort S — risk low — category: intake — wild
  Why: assumption: the user already makes hand commits, and a trailer is the cheapest way to say "and then do X" without leaving the editor. The git-hook source reads it, files a dormant brief, and the morning card lists it.
  Done when: committing with `Sampo-next: port the fix to the site` creates a task with that text, linked to the commit hash.

- **Wild: run a trigger-silence detector that learns each trigger's expected rhythm** — FEATURE — value 3 — effort M — risk low — category: reliability — wild
  Why: "drive stops appeared" and silent failures are the main gap. For each file or event source, learn the usual gap between events. A source that goes quiet well past its norm (a CI watcher dead, a watched dir unmounted) raises one line on the morning card instead of an empty night.
  Done when: killing a watcher that normally fires hourly raises "source quiet" within 3× its median gap, and a legitimately idle weekend does not.

- **Wild: make every trigger carry a one-line "if this fires wrongly, run X" undo hint** — FEATURE — value 3 — effort S — risk low — category: safety — wild
  Why: unattended work needs a cheap reversal, and `sampo unwind` exists only as an idea. Each trigger declares its undo (branch delete, task close, queue drop). The morning card prints it beside each fire, so the user can undo from the card in one command.
  Done when: every fired task in the trigger ledger shows an undo command, and running it for a branch-creating trigger removes the branch and closes the task.

Next question: Which triggers does the user actually want to fire while they are present and working, as opposed to overnight, and does anything in the ledgers show which of the two they ask for?
Next question: When a file trigger and a host-native feature (Claude Code routines, hooks, scheduled tasks) both could start the same work, which one should win, and who records that choice?
