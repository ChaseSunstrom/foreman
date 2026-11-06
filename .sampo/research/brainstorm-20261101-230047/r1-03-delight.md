# Brainstorm — lens: delight

- **Write a morning note that reads like a person left it** — FEATURE — value 5 — effort M — risk low — category: night shift
  Why: the user installed `fm night`, and the tick "logs only when something happens", so the user returns to silence or a log. Triggers that start work unattended need a payoff moment. A three-line note ("ran 2 things, 1 landed on branch night/1101, 1 needs a yes") is what makes self-triggering feel like help.
  Done when: after a night tick that ran at least one trigger, the first `fm next` or SessionStart shows a note under 400 chars naming what ran, what landed and what waits for a yes.

- **Show every queued install as one card with one-word answers** — FEATURE — value 5 — effort M — risk low — category: yes queue
  Why: the mission says installs (timers, units) are "queued for one yes". Several separate asks get ignored. Each card shows the unit text, what it will fire on, and what it unblocks; the user answers `yes`, `no` or `later`.
  Done when: with 3 queued installs, `fm yes` prints one screen with 3 cards, and `fm yes 2 yes` installs only the second and records the answer.

- **Preview a trigger on last week before it can install** — FEATURE — value 4 — effort M — risk low — category: trigger preview
  Why: a user afraid of surprise starts work will say "no" to a bare schedule. "This would have fired 4 times last week, on these commits" turns a leap into a visible choice. assumption: git log and CI history are enough to replay file and CI triggers.
  Done when: `fm trigger preview <spec>` lists the real past events it would have matched, and the install card quotes that count.

- **Give each trigger a name and a one-line receipt when it fires** — FEATURE — value 4 — effort S — risk low — category: trigger log
  Why: `fm triggers` already groups captures with precision, so names and receipts extend it. "ci-red on main → drafted fix in lane 3 (T-2551)" lets the user see cause and effect, and the quiet night tick gets an audit trail.
  Done when: each fired trigger appends one line with name, cause, action and task id, and `fm triggers --recent` prints the last 10.

- **Make the stage rail show a trigger as the first step** — FEATURE — value 3 — effort S — risk low — category: web UI
  Why: the web UI has a stage rail and Activity lanes. Work that started itself should look different from work the user typed, or the user cannot tell who began it. A small "started by ci-red" tag with a gentle fade-in on the lane does that.
  Done when: a task created by a trigger shows a "started by <name>" chip in the web UI Activity lane, and a typed task does not.

- **Offer a "quiet hours" dial that slides, not a cron string** — FEATURE — value 3 — effort S — risk low — category: night shift
  Why: users who install timers rarely want to hand-write schedules. A dial from "only when I'm asleep" to "anytime" with plain labels is the delightful way to set the shift. assumption: most users want 2–3 presets.
  Done when: `fm night --hours sleep` sets a window and `fm doctor` prints it in words ("works 23:00–07:00 when idle").

- **Tell the user, kindly, when a trigger has never helped** — FEATURE — value 3 — effort S — risk low — category: trigger hygiene
  Why: precision is already measured per trigger. A trigger with 0 acted-on runs after 10 fires gets a friendly "shall I retire this one?" in the morning note, not a silent drain.
  Done when: a trigger with 10 fires and 0 acted-on outcomes appears in the morning note with a one-word retire answer.

- **Wild: Let the night shift leave a postcard from the lane** — FEATURE — value 3 — effort M — risk low — category: night shift
  Why: wild. A multi-hour unattended fix should end with something you would show a friend: one screenshot or a three-line before/after, saved as `night/<date>/postcard.md` and shown in the web UI.
  Done when: a night lane that closes a task writes a postcard file with the ask, the change in one line and the proof command output, and the web UI links it.

- **Wild: Play the night back as a ten-second timelapse in the web UI** — FEATURE — value 3 — effort L — risk low — category: web UI
  Why: wild. Lanes, triggers and gates become dots on a night-long strip that plays fast: lights come on when a trigger fires, a lane turns green when its gate passes. It makes unattended work visible and easy to share.
  Done when: the web UI's Night page plays the last shift from the event log in under 15 seconds and pauses on any red lane.

- **Wild: Knock twice to cancel everything** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. Self-triggering is scary until stopping is trivially easy. A `~/.fm-stop` file you can `touch` (or a button in the web UI) halts every trigger and lane, and the next note says "stopped by you at 02:14, nothing lost".
  Done when: creating the stop file makes the next tick run nothing, and the morning note names the stop time and what was paused.

- **Celebrate the first self-started success exactly once** — FEATURE — value 2 — effort S — risk low — category: first run
  Why: the first time a trigger's work lands and the user accepts it is the moment trust is earned. A one-time line ("your first self-started fix landed: ci-red → T-2551") marks it without noise afterward.
  Done when: the first accepted trigger-started task prints the line once and a flag stops it repeating.

- **Show "what would wake me" as a tiny list on the status line** — FEATURE — value 2 — effort S — risk low — category: status line
  Why: assumption: users forget which triggers they have. A compact "3 watching: ci, issues, src/**" on the pane's status row keeps the system legible.
  Done when: the pane shows the count and names of active triggers and updates within 5 seconds of an install or retire.

Next question: What does the user do in the first five minutes after reading a morning note, and which of those actions has no single command yet?
Next question: Which triggers would the user be embarrassed to have fired in front of someone (a noisy PR comment, a push, a message), and does an outward-action class exist that triggers can never spend?
