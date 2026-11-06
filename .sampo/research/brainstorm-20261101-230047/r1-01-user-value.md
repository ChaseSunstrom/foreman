# Brainstorm — lens: user value

- **Add a heartbeat so silence means "alive"** — FIX — value 5 — effort S — risk low — category: reliability
  Why: the pack says the night tick "logs only when something happens", so a dead timer and a quiet night look identical. Assumption: a laptop asleep or a disabled unit can go unnoticed for days.
  Done when: with the timer stopped for 48h, the next session's first note says "night tick last ran <date>, here's the one command to restart it". With it healthy, the note is absent.

- **Catch up missed runs once, coalesced** — FEATURE — value 4 — effort S — risk low — category: schedules
  Why: assumption: user hardware sleeps and powers off, and timers either skip runs or fire a burst on wake.
  Done when: a simulated 3-day gap fires each scheduled job at most once on wake, and the log says "ran 1 of 3 missed".

- **Answer PR review comments in a lane** — FEATURE — value 5 — effort M — risk med — category: watchers
  Why: `fm ci-watch` and `fm pr train` exist, but nothing reacts to a reviewer's comment. Assumption: review round-trips are the biggest idle gap after CI.
  Done when: a fixture PR comment ("rename X to Y") produces a branch commit with a red-first test and a draft reply, and the user's tree is never touched.

- **Reproduce-first issue watcher** — FEATURE — value 4 — effort M — risk med — category: watchers
  Why: assumption: the issue watcher is a stated Mission 4 goal, and a draft fix on an unreproduced issue wastes the morning.
  Done when: for a fixture issue the lane either attaches a failing test, filed as a task, or writes "could not reproduce: tried A, B". Issue text is fenced as untrusted data.

- **Fire onto a worktree, never the user's tree** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: assumption: self-started work will collide with the user's uncommitted edits sooner or later, and that's the first thing that would make someone uninstall the timer.
  Done when: with a dirty tree and a checked-out branch, a triggered lane runs in a separate detached worktree. A test asserts `git status` in the user's tree is byte-identical after the run.

- **Add a drop folder as a file trigger** — FEATURE — value 4 — effort S — risk low — category: file triggers
  Why: file triggers are in the request. Assumption: a screenshot, log or URL file dropped into `~/fm-inbox/` is the lowest-friction way to start work from a phone sync or browser download.
  Done when: a file dropped there becomes a verbatim capture with its path, and the original is moved to `done/`, never deleted.

- **Show a trigger inventory with cost and fire record** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: `fm triggers` has precision for captures only, and the user must say yes to every unit, so they also need to see what is running. Assumption: no single view lists timers, units, git hooks and watchers.
  Done when: `fm triggers list` prints each installed trigger with last fire, next fire, acted-on rate and a one-line disable. A test installs two fixtures and finds both.

- **Switch branches and resume that branch's goal** — FEATURE — value 4 — effort M — risk low — category: git triggers
  Why: assumption: users switch branches often, and the open goal and baton belong to a branch the session no longer matches.
  Done when: a post-checkout hook makes the next session's first note name the goal tied to that branch, or say none, without a model call.

- **Test the project against new upstream releases** — FEATURE — value 4 — effort M — risk med — category: dependency watch
  Why: assumption: the user learns of a breaking dependency release when CI turns red. The `fm lib` cards already name each project's stack.
  Done when: a fixture release of a pinned dependency triggers a scratch-lane run of the suite, and the result is filed as "bump ok" or "breaks N tests" with no change to the lockfile.

- **Wild: Offer to schedule what you do by hand every week** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: wild. Assumption: the shell and session logs show the same command sequence every Monday, and the user hasn't thought to automate it.
  Done when: a fixture log with one sequence repeated across 4 weeks yields a single proposed trigger card, and nothing is installed without the yes.

- **Wild: Hold fires while the user is mid-flow** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Assumption: a lane starting a build while the user compiles, or a notification during a call, is the next complaint. Signals could be input idle time, an optional local ICS file, and battery state.
  Done when: with the idle signal under 2 minutes, a triggered lane defers and logs "held: user active". It runs at the next idle window.

- **Wild: Commit triggers to the repo as reviewable standing orders** — FEATURE — value 3 — effort M — risk med — category: team
  Why: wild. Assumption: a `.foreman/triggers.toml` lets a teammate or future self see and review "what runs without me", instead of state hidden in the user's home directory.
  Done when: a changed triggers file shows as a diff, and no new trigger activates until the yes-queue lists it.

- **Send a one-line weekly receipt per trigger** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user pays attention for every install, so each trigger should justify itself. Assumption: "fired 9, acted on 7, ~40 min saved" keeps good triggers and exposes noisy ones.
  Done when: the weekly note shows fired, acted-on and ignored counts per trigger from the existing log, and flags any trigger with 0 acted on in 14 days.

Next question: which of the 59 empty cells would a real user hit within a week of first install, and which exist only so the grid reads as complete?
Next question: what is the user's actual failure story with a self-starting tool (a surprise bill, a changed file, a noisy notification), and does any trigger here guard against that?
