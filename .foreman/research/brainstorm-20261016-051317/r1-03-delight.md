# Brainstorm — lens: delight

- **Make the first close of the day a sound-free "ding" in text** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the existing ideas cover stamps, grades and celebrations on every close; none mark the day's *first* close, which is the moment a user returns to check on an AFK run.
  Done when: the first task closed after local midnight prints a one-line "first one in the bag" banner; the second close in the same day does not.

- **Name every parallel builder lane with a stable, friendly callsign** — FEATURE — value 3 — effort S — risk low — category: naming
  Why: review notes show 4 builders at once with ids like `lane-<id>` and lease paths that double; the user reads these in the Agents graph. Assumption: a short memorable callsign (e.g. "otter", "kestrel") derived from the lane id makes the fleet readable at a glance.
  Done when: `fm lane list` and the Agents graph show the same callsign for a lane across restarts, and two live lanes never share one.

- **Let the pane show "what changed while you were AFK" as a single line that expands** — FEATURE — value 4 — effort M — risk low — category: return-moment
  Why: the user said "I will be AFK, do everything"; the pack has morning briefings and digests as ideas, but none as a collapsed one-liner on the pane that opens in place without a new verb.
  Done when: after 30+ minutes idle, the pane's top row reads "N closed, M blocked, $X, press → to open" and expanding shows the list.

- **Turn merge conflicts on HELP_TIERS into a self-resolving registry** — FIX — value 4 — effort M — risk med — category: dev joy
  Why: the review says nearly every second merge conflicted because all features edit one HELP_TIERS line in fmcli.py (T-1059, T-1062).
  Done when: a new command registers itself from its own file (decorator or drop-in), HELP_TIERS is generated, and two parallel branches adding different commands merge without conflict in a test.

- **Add `fm guard why "<command>"` that replays a command through the real hook** — FEATURE — value 5 — effort S — risk low — category: debuggability
  Why: the review states the main thread twice wrote scratch scripts to replay a command through the real guard with the real cwd (T-1125, T-1141); there is no verb for it.
  Done when: `fm guard why "rm -rf build"` prints allow or deny, the matching rule and the cwd used, and agrees with the live hook on a recorded corpus of 50 commands.

- **Check a verify command the moment it is added** — FIX — value 4 — effort S — risk low — category: trust
  Why: review: verify commands are often wrong (missing test module, `npm test` with no npm) and are caught only when run.
  Done when: adding a verify criterion with a nonexistent module or missing binary is refused with a "did you mean" suggestion, and a valid one is accepted.

- **Give refused or failed runs a one-sentence apology-free "next move" in the pane's colour of calm** — FEATURE — value 3 — effort S — risk low — category: tone
  Why: the pack's ideas pair refusals with a do-this-instead; this extends it to red gates and failed closes, the places the user feels friction. Assumption: the pane has room for one line.
  Done when: every red gate result in the pane carries a single suggested next command that is runnable verbatim.

- **Show a "new since your installed version" teaser in the pane** — FEATURE — value 3 — effort S — risk low — category: upgrade joy
  Why: review: installed foreman-ui is 0.7.0 while the repo's is 0.17.0; marketplace users lag ten releases and never see what they're missing.
  Done when: when the installed UI is behind, the pane shows one line naming the newest feature it lacks and the update command; it disappears once updated.

- **Wild: Give the queue a "jukebox" — a ranked, playable list of finished diffs to savour** — FEATURE — value 2 — effort M — risk low — category: ceremony — wild
  Why: assumption: after a long AFK run the user faces many closes; stepping through them one at a time with next/prev, each shown as a mini before/after, turns review into a pleasant ritual.
  Done when: `fm jukebox` steps through each closed task from the last absence with its diff, proof and a keep/revert key.

- **Wild: Let the mascot leave a tiny sticky note on a file it was nervous about** — FEATURE — value 2 — effort M — risk med — category: personality — wild
  Why: assumption: the fence-check and hot-file ideas exist, but they speak to the model, not the human; a visible, dismissible one-line note beside the diff ("touched 3 times this week, tests thin") would feel human.
  Done when: closing a task that edits a top-5 hot file shows a one-line note in the close summary, and `fm note dismiss` hides it for 30 days.

- **Wild: Offer `fm postcard` — a single shareable image or SVG of one finished task** — FEATURE — value 3 — effort M — risk low — category: sharing — wild
  Why: the README leads with a demo SVG, so the team already values showable artefacts; users showing others is the delight lens's core. Assumption: one task's red-to-green, diff size and time make a good card.
  Done when: `fm postcard T-xxxx` writes an SVG under 100 KB containing title, stages, time and red→green proof, with no paths or secrets (checked by a scrub test).

- **Wild: Name the release after the thing it fixed most annoyingly** — FEATURE — value 2 — effort S — risk low — category: release joy — wild
  Why: releases 1.2.31 and 1.2.32 are numbered only; the user asks to "push to main" at the end of each. Assumption: a changelog headline drawn from the task with the most user steers makes releases memorable.
  Done when: release notes begin with a one-line headline picked from the closed task with the most linked user requests, and the choice is shown in the release dry run.

- **Make the pane's idle screen show the next three queued tasks as cards you can reorder with a key** — FEATURE — value 4 — effort M — risk low — category: control
  Why: the user steers priority by typing requests; open work lists 30+ deferred tasks. Assumption: reordering visually is faster than re-asking.
  Done when: pressing a key moves a queued task up or down, the queue order in state changes, and `fm state` reflects it.
