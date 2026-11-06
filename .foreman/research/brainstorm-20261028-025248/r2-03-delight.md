# Brainstorm — lens: delight

- **Colour each task id from its slug** — FEATURE — value 3 — effort S — risk low — category: recognition
  Why: assumption: ids appear on the pane, web UI, desk and History, so the same task is hard to spot across surfaces. A stable colour per slug makes it recognisable at a glance.
  Done when: the same slug gets the same colour in the pane, web UI and desk output, and every colour meets 4.5:1 contrast on the dark and light backgrounds.

- **Peek a task in place with space** — FEATURE — value 4 — effort S — risk low — category: navigation
  Why: assumption: the terminal UI lists tasks, and opening a receipt currently means leaving the list. Space would show the receipt under the row without moving the selection.
  Done when: space expands a six-line receipt under the selected row, esc collapses it, and the selected row is unchanged after both.

- **Let removed lines fall and added lines rise when a fix lands** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the diff is the proof, and motion can show what changed without a word of text. This follows the rule that motion should explain state.
  Done when: with motion on, the transition plays once in under 600 ms; with reduced motion or NO_COLOR set, the final diff is shown with no animation.

- **Fold the close receipt into a paper crane on a pass** — FEATURE — value 2 — effort M — risk low — category: close ritual (wild)
  Why: (wild) the close receipt is already the end of each task, so a short fold animation can mark the pass without adding a new step.
  Done when: a passing close plays a fold in the web UI and pane, a failing close plays nothing, and reduced motion shows the finished crane as a still image.

- **Typewriter-reveal the close receipt at reading pace** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: assumption: receipts are dense, and revealing them at a reading pace keeps the eye on the first line. Any key skips the reveal, so input is never delayed.
  Done when: a six-line receipt finishes within 1.5 s, any keypress completes it at once, and the text is fully present in the copied output.

- **Pin your favourite verbs to the top of help** — FEATURE — value 2 — effort S — risk low — category: discoverability
  Why: the help positions come from one shared list, and two commands already collided on position 306. Pinning a verb's position by use makes the help match real habits.
  Done when: a verb used five or more times in a week appears first in `fm help`, and `fm help --reset` restores the default order.

- **Give each touched file a three-line tour from its last diff** — FEATURE — value 4 — effort M — risk med — category: docs
  Why: assumption: the map lists entry points and layout, but no file says what it is for. Each receipt already names the file it changed, so the tour can come from the last diff to touch it.
  Done when: `fm tour FILE` prints at most three lines and the task id that wrote them, and says plainly when a file has no receipt yet.

- **Hide two easter-egg verbs that print one line each** — FEATURE — value 1 — effort S — risk low — category: delight
  Why: assumption: the CLI is large and easy to dismiss, so a few hidden verbs reward curious users. They should stay out of help and completion.
  Done when: `fm tea` and `fm hush` each print one line and exit 0, and neither appears in `fm help` or shell completion output.

- **Draw the repo as a city of modules** — FEATURE — value 3 — effort L — risk med — category: visualization (wild)
  Why: (wild) each module becomes a building whose height is its recent churn and whose lit windows are its closed fixes. The map already groups files by layout, so the city can reuse that grouping.
  Done when: `fm map --city` renders every top-level directory in the map with a height matching its churn over the last 30 days, and it fits in 80 columns.

- **Sketch the diff in ink that firms up as tests pass** — FEATURE — value 2 — effort M — risk low — category: motion (wild)
  Why: (wild) a rough, hand-drawn look for a diff that is still unproven, sharpening as each proof passes. It makes the proof's progress visible without a progress bar.
  Done when: an unproven diff renders in the sketch style, each passing proof sharpens it one step, and a closed task renders in the final crisp style.
