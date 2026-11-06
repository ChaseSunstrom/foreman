# Brainstorm — lens: beautiful UI and motion

- **Subtitle every moving thing on demand** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the pack has dozens of motion ideas (shimmer, flashes, morphs, reflow) and a 2 Hz tick lint, but nothing that lets a confused user ask "why did that move?". The user's recurring complaint is "it just isn't doing anything", and that applies to unexplained motion too.
  Done when: pressing `m` freezes the frame and labels each animating cell with the event id and kind that caused it, and a pty test confirms every animated region has a label.

- **Thread the request's words to the criteria they became** — FEATURE — value 5 — effort M — risk med — category: intake UI
  Why: the pack proposes echoing the request and tracing clauses to criteria as text. The user's verbatim requests are long and multi-clause ("and integrate all of these too, automatically, super enhanced harness, etc."). Nothing draws the mapping.
  Done when: after the plan slot fills, request words highlight, thin lines run to their criterion chips, and any unmapped words stay amber-underlined. A golden frame covers a request with one dropped clause.

- **Make one-way doors feel heavy** — FEATURE — value 4 — effort S — risk low — category: safety UI
  Why: the user said "stop asking me if you can release", and a publish grant exists (T-0335, `--allow publish`). Granted or not, release, push and delete should still look different from routine actions.
  Done when: every action tagged irreversible renders with a thicker border and a slower, distinct settle animation, plus a visible "granted by ..." line when the grant already exists. A test asserts the tag-to-style table covers all irreversible verbs.

- **Play undo backwards** — FEATURE — value 4 — effort M — risk med — category: motion
  Why: "undo and PR from a run" is in the unbuilt slate. A reverse replay of the diff, with files un-writing line by line, lets the user preview the revert before confirming.
  Done when: `u` on a closed run scrubs a reverse replay from the run's event log. Confirming reaches the same tree hash as the real undo, and a test compares the two.

- **Draw handoffs and fallbacks as a baton path** — FEATURE — value 3 — effort M — risk low — category: agents UI
  Why: the pack has runner fallback on classified failure, "hand a stuck run to a live CLI", and race modes. The runner bay idea covers capability lamps but not movement between runners.
  Done when: when a fallback or handoff event fires, a baton glyph travels from the old runner's lane to the new one, labelled with the failure class. Replaying a recorded fallback produces the identical frame sequence.

- **Say why the look is degraded** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: the pack covers many degradation ladders (reduced motion, NO_COLOR, slow links, narrow panes) but never tells the user which one is active. Without that, a plain screen looks like a bug.
  Done when: a dim one-line chip such as "plain: ssh link slow" appears whenever any ladder step is active, and a pty matrix test asserts the chip text for each trigger.

- **Show a keyring of live grants with expiring rings** — FEATURE — value 4 — effort S — risk low — category: trust UI
  Why: standing grants, leases and "earned bypass" appear as ideas, but no single glanceable surface shows what Foreman is currently allowed to do without asking.
  Done when: the band shows one key glyph per active grant, with a ring that drains toward its expiry. Selecting a glyph shows its scope and a one-key revoke. A test creates a grant and checks the glyph appears and then expires.

- **Map read versus write footprint** — FEATURE — value 3 — effort M — risk low — category: attention map
  Why: the pack's repo-treemap idea covers edits only. Showing files read but never edited exposes wasted exploration (the re-read tax) and what the planner actually looked at.
  Done when: the treemap tints reads cool and writes warm, and a finished run lists the top five read-only files. The numbers match the event log.

- **Leave an afterimage on the last-touched element when switching views** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the plan has a lot of view-switching (home, project, run, drawers). Returning to a list and finding your place is a recurring papercut.
  Done when: returning to a view re-focuses the last-touched row with a 400 ms fading outline, and the focus id persists across a restart in a golden-frame test.

- **Wild: sweep a lighthouse beam across the home deck** — FEATURE — value 3 — effort M — risk low — category: ambient
  Why: assumption: the home screen ranks projects by need. A slow single-line sweep that briefly brightens cards needing attention draws the eye without a permanent alert, and it stops when nothing needs the user.
  Done when: with one project blocked, the sweep brightens only that card, and with none blocked the sweep is absent. Both states have golden frames.

- **Wild: print the user's own rules as marginalia next to the thing they constrain** — FEATURE — value 4 — effort M — risk med — category: trust UI
  Why: the user's pushbacks ("no need to ask me, feel free to release", "don't stop until complete") are stored but invisible at the point of effect. Faint margin text such as "you: stop asking about release" appears beside the release step, and clicking it opens the source steer.
  Done when: a stored steer matching an action type renders a one-line margin note beside that action's step, and removing the steer removes the note.

- **Wild: show a ghost of the next action with a one-second veto** — FEATURE — value 4 — effort L — risk med — category: control
  Why: assumption: previews of risky actions help the user, and "preview risky actions as a dry-run" is already on the list. A translucent preview of the next file edit or command, fading in just before it runs, would add a hands-on veto that costs nothing when ignored.
  Done when: before a gated action the preview shows for one second, Esc cancels and logs a veto, and a pty test asserts that a veto stops that action while the run continues.

- **Wild: make the home deck an orrery** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: the home screen is a list of projects with counts. Orbit speed would show activity, body size queue depth, and Enter would zoom into a project's run view.
  Done when: the orrery renders from the same project data as the list, a `--calm` flag falls back to the list, and the zoom transition is covered by frame snapshots.
