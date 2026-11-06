# Brainstorm — lens: bold bets

- **Run the whole waiting-out of usage limits from a timer, not a live session** — FEATURE — value 5 — effort M — risk med — category: scheduling
  Why: steer 2026-10-31 #3 says to wait out real limits and resume where stopped, but that waiting is session-bound (assumption: no unit wakes a stopped drive at the reset time). A one-shot timer set to the reset moment resumes the drive with no user present.
  Done when: in a test with a faked limit-reset time, a transient timer is created and fires `fm drive --resume` at that time with no session open, and the run log shows the resume.

- **Make the issue label the consent channel for an issue watcher** — FEATURE — value 5 — effort L — risk med — category: watchers
  Why: `fm ci-watch` exists and settles ship bets, but issues are untouched. The user's own `foreman` label is a channel the model cannot write, so the watcher only acts on issues the user labelled. It opens a lane in a worktree, pushes a draft branch, and never merges. The issue text is fenced as untrusted data.
  Done when: against a recorded GitHub issues fixture, a labelled issue produces a draft-branch lane and an unlabelled one produces nothing; an injected "ignore rules" body changes no lane behaviour.

- **Add a git-hook and filesystem trigger family behind one yes** — FEATURE — value 4 — effort M — risk low — category: event triggers
  Why: the mission names file and event triggers, and `fm triggers` has precision stats but the pack shows no path or git-event source. Generate post-merge, post-checkout and systemd `.path` units. All are queued together as one install card and diffed against what is actually installed.
  Done when: `fm triggers add --path 'plugin/lib/*.py'` queues a unit, one yes installs it, and touching a matching file starts exactly one debounced lane.

- **Write a heartbeat for every installed timer and trigger** — FIX — value 4 — effort S — risk low — category: reliability
  Why: the night tick "logs only when something happens", so a dead timer and a quiet one look identical. This is the same gap as the open question about a guard that never fires. Record the expected next fire per unit; `fm doctor` goes red on a missed fire or a failed unit.
  Done when: stopping a test timer makes `fm doctor` name that unit as missed within one period; a healthy idle one stays green.

- **Offer a drop folder as a universal trigger** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: assumption: the user wants to hand Foreman work without opening a session. A watched `~/foreman-drop/` takes a note, URL or screenshot and files a capture. Syncthing or a phone share sheet pointing at it turns the phone into a surface. Content is treated as untrusted.
  Done when: a text file dropped in the folder becomes a capture with its source recorded within the debounce window; a file containing a prompt-injection string runs no command.

- **Define a watcher contract so a watcher is a 30-line script** — FEATURE — value 4 — effort M — risk med — category: extensibility
  Why: CI and issue watchers are separate one-offs. Define one contract (emit JSON events, declare effects, carry a self-test) and let stack cards ship watchers for GitHub, GitLab, Forgejo, PyPI advisories and host-CLI releases.
  Done when: a new sample watcher is added with no change to core code and passes the contract's self-test; one that omits its effects declaration is refused.

- **Trigger a compatibility run when a host CLI or dependency changes** — FEATURE — value 4 — effort M — risk low — category: event triggers
  Why: earlier ideas want a guard corpus re-run on host updates, but nothing starts it. A watcher on `claude --version`, `codex --version` and lockfile hashes fires the hook-import check, guard corpus and `fm doctor` on change, filing a FIX only if one fails.
  Done when: faking a version bump runs the corpus once and logs the result; no bump runs nothing.

- **Replace `fm every` with plain-English schedules compiled to units** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: the user installed `fm night`, so schedules are wanted. `fm every "weekdays 7am: sweep"` compiles to an `OnCalendar` unit with `Persistent=true` (a missed run catches up) and jitter. It shows the unit text and the next five fire times before the yes.
  Done when: the command prints correct next-fire times for three phrasings and refuses an ambiguous one with a question.

- **Hold a trigger budget market that pays by precision** — FEATURE — value 3 — effort M — risk med — category: budget
  Why: `fm triggers` already measures precision per trigger, but nothing spends it. Divide the nightly cost cap across triggers in proportion to their trailing precision and starve those below a floor, so a noisy watcher cannot eat the shift.
  Done when: in a simulated night, a trigger with 10% precision gets under its proportional share and a 90% one gets over, and the total stays under the cap.

- **Wild: Fire a lane from a production log signature** — FEATURE — value 3 — effort L — risk med — category: incident watcher
  Why: wild. Tail `journalctl -u SERVICE` or a log file for a normalised error signature. On a new one, open a FIX capture with the repro lines, then reopen the old task if the signature matches a closed fix. This turns "fix recurred" into an automatic event.
  Done when: replaying a log fixture with a new error files one capture, and a repeat of a previously fixed signature reopens that fix instead of filing a new one.

- **Wild: Relay a trigger between the user's machines over a private git ref** — FEATURE — value 3 — effort L — risk high — category: multi-device
  Why: wild. A watcher on the VPS (CI, issues) writes an event to `refs/foreman/events` and the desktop's path-style poll wakes the lane there. This needs no webhook endpoint or tunnel, and the machine with the model access does the work.
  Done when: an event pushed from machine A starts a lane on machine B within one poll interval, and a forged unsigned event is ignored.

- **Wild: Propose schedules from the user's own habits** — FEATURE — value 3 — effort M — risk low — category: unspoken needs
  Why: wild. Mine session start times, weekly repeated verbs (`fm ship` Fridays, say) and idle gaps to propose a schedule or pre-warm trigger, with a back-test against the last 30 days. It shows the proposal as one sentence and installs nothing without the yes.
  Done when: on a recorded history with a weekly Friday ship, a proposal appears with its hit rate, and rejecting it is remembered.

- **Add `fm wake --dry` to preview tomorrow's shift** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: installs are queued for one yes, but the user cannot see what the combined triggers would do. A command lists every trigger, its next fire, expected lane count and cost ceiling, and flags overlaps.
  Done when: with three triggers installed it prints three rows and flags two that fire at the same minute.

Next question: Which triggers would the user refuse to leave unattended even with a draft-branch-only landing, and has anyone asked them?
Next question: What happens to queued yeses and parked lanes when the machine is suspended across a scheduled fire, and is that tested?
