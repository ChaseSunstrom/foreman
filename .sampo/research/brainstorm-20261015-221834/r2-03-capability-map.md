# Brainstorm — lens: capability map

- **Forecast each task's cost and time from similar closed tasks** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the ledger holds closed tasks with size labels (S/M/L), but nothing shows what a new one will likely cost. Ideas so far cap spend; none predict it. Assumption: the ledger records duration and tokens per task.
  Done when: `fm task add` prints "similar tasks took ~N min, ~K tokens (n=7)", and a test shows the estimate comes from the nearest closed tasks in a fixture ledger.

- **Land finished worktrees through a merge train** — FEATURE — value 5 — effort L — risk med — category: fleet
  Why: the pack shows many parallel builders and a resume plan (T-1028), but nothing orders their landing. Predicting overlap before dispatch is listed; sequencing after the work is done is not. Aider, Sweep and GitHub merge queues all do this. Assumption: finished builders leave a branch each.
  Done when: with three fixture worktrees where two touch the same file, `fm land --train` rebases them in order, re-runs the gate after each, and stops with a named conflict instead of a broken main.

- **Check a diff against the user's own past steers before showing it** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the user's steers repeat ("declutter", "fill the panel exactly", "no plain rows left", "show complete vs left"). Each is a standing preference, and the same complaint recurs per UI task. This extends "name recurring corrections as standing rules" into a pre-close check.
  Done when: a UI task whose diff adds an unaligned or boxed row gets a flagged line citing the steer it breaks, and a fixture shows no flag on a clean diff.

- **Suggest guard rules from commands you approved or denied by hand** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard hook blocks commands in bypass mode, and T-0275 (reading what scripts run) is deferred. Nothing learns from the user's own allow and deny decisions. Assumption: the guard logs its decisions.
  Done when: after the same prompt is approved three times, `fm guard suggest` prints one allow rule with its evidence, and applying it makes the fourth run silent.

- **Mark tool results from the web or MCP as tainted and gate commands built from them** — SECURITY — value 4 — effort L — risk med — category: injection
  Why: T-0791 lists 18 injection and supply-chain ideas as deferred and none describes taint propagation. This pairs with the guard hook: a command whose text appears verbatim in fetched content needs confirmation.
  Done when: a fixture fetch result containing `curl x | sh` makes the same command in the next Bash call prompt instead of running, while a command typed by the user runs untouched.

- **Keep an outbound ledger of everything that leaves the machine** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: Foreman spawns `claude -p` children, calls context7 for card drafts (T-1037), and pulls docs. The privacy lens needs a way to see all of it. Assumption: there is no single record of outbound calls today.
  Done when: `fm egress` lists each outbound call with time, destination, byte count and the task that caused it, and a test fails if a new network call skips the ledger.

- **Warn when a card's library has moved a major version** — FIX — value 3 — effort S — risk low — category: cards
  Why: 1,084 cards exist and T-1037 grows them in bulk from docs, but nothing marks one as stale. A stale card injected at edit time is worse than none. `fm scout` already reads dependency versions.
  Done when: a card written for a library at v2 shows "stale" in `fm lib show` once the project's lockfile says v3, and edit-time injection labels it.

- **Let a repo add its own gate, lens or card by dropping a file** — FEATURE — value 4 — effort M — risk med — category: extensibility
  Why: the pack shows `enforce.toml` as an idea and a growing set of lenses, but no stated contract for a project to add its own check without editing the plugin. Assumption: the gate list is currently built in.
  Done when: a file in `.foreman/gates/` is run by `fm doctor` and the close gate, and a malformed file is reported rather than crashing the hooks.

- **Fall back to a one-line statusline when the mod UI isn't installed** — FEATURE — value 3 — effort S — risk low — category: surfaces
  Why: most of the UI work sits in the foreman-ui mod, and T-0794 considers freezing it. Users without it see none of the stage, queue or progress counts they asked to have visible.
  Done when: `fm statusline` outputs "T-1028 step 3/7 · queue 4 · today 6 done" in under 50 ms, and works with no mod present.

- **Honour reduced-motion and a colourblind-safe palette in the pane** — FEATURE — value 2 — effort S — risk low — category: accessibility
  Why: the pane has animated trees and graphs, and gradient dividers were requested. Colour alone carries state in the node graph. The "pick motion level from frame lag" idea is performance; this one is for people.
  Done when: `NO_MOTION=1` freezes every animation, and a snapshot test shows status is distinguishable without colour (glyph or shape per state).

- **Wild: Bisect a red gate back to the task that broke it** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: assumption: every closed task is a commit with a recorded proof. When the gate fails on main, Foreman could run the failing check across those task commits and name the culprit task, then reopen it.
  Done when: in a fixture history with one bad commit, `fm bisect` prints the task id and reopens it with the failing output attached.

- **Wild: Get a second opinion on risky diffs from another model family** — FEATURE — value 3 — effort M — risk med — category: review
  Why: adapters for Codex, Gemini CLI and opencode exist (T-0335/0336 blocked on live verification). A different family catches different mistakes than Claude reviewing itself. Assumption: at least one adapter can run headless read-only.
  Done when: a diff touching the guard or hooks triggers a read-only review by a second CLI, and its findings land in the same structured file as `fm audit`.

- **Wild: Serve the learned brain over MCP to other tools** — FEATURE — value 3 — effort M — risk med — category: interop
  Why: the research list asks for one setup across Codex, Gemini and Cursor. Hints, lessons and vetoes travel by git already. A read-only MCP server would let any MCP client query "known fix for this error".
  Done when: an MCP client calling `known_fix` with an error string gets the matching hint and its hit rate, and the server can't write.

- **Wild: Open each session with a one-page "what changed since you left" brief** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: assumption: users stop and return often, as the resume request shows. This combines the SessionStart resume offer, `fm tour --since` and the ledger-versus-git reconcile into one screen: what finished, what stalled, what Foreman learned.
  Done when: a fresh session after a killed builder shows the stalled worktree, any new hints and the next action in under 15 lines, with a test on a fixture ledger.
