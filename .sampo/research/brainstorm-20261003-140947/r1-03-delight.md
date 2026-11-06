# Brainstorm — lens: delight

- **Animate every in-flight row with one shared spinner clock** — FIX — value 5 — effort M — risk low — category: motion
  Why: the user said the `$` in shell commands "isn't animated like the Running" and asked to "animate your messages better"; rows animate unevenly.
  Done when: a mod test renders a running command, edit and agent row at two tick values and all three glyphs advance in step, and they settle to one static glyph on completion.

- **Give diffs a palette tuned to the panel theme** — FIX — value 4 — effort S — risk low — category: color
  Why: the user called the green/red diffs "weird in contrast"; panel colors were also a complaint.
  Done when: a snapshot test shows diff add/remove lines with a background tint (not raw green/red text), and every diff color has a contrast ratio ≥ 4.5 against the panel background in dark and light themes.

- **Add a panel conformance linter for the mod** — CLEAN — value 4 — effort M — risk low — category: consistency
  Why: repeated steers: "everything still doesn't match", "some things aren't in panels", "duplicated things". Each fix was found by eye.
  Done when: one test renders a fixture of every row type (reply, prompt, command, edit, agent, question, band, dashboard) and fails if any lacks the shared border, title position, padding or color token, or appears twice.

- **Show a one-line "turn receipt" footer on every reply panel** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: the user is usage-sensitive and wants each message to look finished; the reply panel already settles on ●. A footer (time, tools used, files touched) makes the settling visible.
  Done when: a finished reply panel shows a dim footer such as `4 tools · 2 files · 12 s`, and it is absent on in-progress panels.

- **Collapse long tool output into a peek-and-expand panel body** — FEATURE — value 4 — effort M — risk med — category: formatting
  Why: the user says output "doesn't look right", especially Update and Bash rows. Long output makes panels ragged and pushes the chat around.
  Done when: a command with >12 lines renders its first 5 and last 3 lines with a `+N lines` rule, and a test confirms the full text is retained for expansion.

- **Make the mascot's face and the panel border reflect task state** — FEATURE — value 3 — effort S — risk low — category: personality
  Why: assumption: the user likes the Foreman identity. The border color and header glyph are the cheapest ambient signal of working / waiting on you / blocked / done.
  Done when: a test renders the header in four states and each has a distinct glyph and border token, with a text fallback when color is off.

- **Wild: Play a short "task closed" flourish** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: `fm task finish` is the moment of reward and today it is silent text. A 600 ms border shimmer sweep plus a one-line receipt (criteria passed, commit hash) would be what users show others. (wild)
  Done when: finishing a task triggers the sweep once in the mod, is suppressed with a reduced-motion setting, and costs no model turn.

- **Wild: Let the dashboard show a live "lane map" of parallel runs** — FEATURE — value 4 — effort M — risk med — category: parallel
  Why: the user worried that parallel work causes context, speed or quality issues. Each worktree lane appears as a small bar with step, ETA and a collision warning when two lanes touch near files. (wild)
  Done when: with `fm run --parallel 2`, the dashboard lists two lanes, each updating independently, and a fixture with overlapping files shows a warning chip.

- **Wild: Add a "screenshot this panel" command that exports a clean card** — FEATURE — value 2 — effort M — risk low — category: sharing
  Why: the user is evidently showing off and checking appearance. A command that renders the last reply or task card to a plain-text or SVG file, with no private paths and with secrets masked via fmsecrets, makes it shareable. (wild)
  Done when: running it writes a file containing the panel borders and text, and a test shows a planted fake token is masked.

- **Hold a golden-frame visual regression set for the mod** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: appearance has been the top complaint across rounds, yet the 58 mod tests didn't catch the duplicated dashboard or mismatched AC and audits rows.
  Done when: committed frame snapshots for the dashboard, the task card and each row type are compared in `fm check`, and a one-column change to any of them fails the gate with a readable diff.

- **Keep a "looks wrong" capture that records the offending frame** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: the user describes visual problems in prose each time ("looks weird"). One key to save the current frame plus the row types on screen to the inbox lets the RSI loop fix the exact thing.
  Done when: triggering the capture creates an inbox item with the frame text attached, and `fm inbox` shows it with the row types listed.
