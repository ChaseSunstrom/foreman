# Brainstorm — lens: grid

- **Run each live-state reading cold and warm, and flag a mismatch** — FIX — value 4 — effort S — risk low — category: proof
  Why: cell CLI × agent × wrong. The carried gap says every Exam needs a live-state reading, but a reading that hits a cache or a stale tmpfs file can pass on old state. Assumption: some readings go through cached readers.
  Done when: a test plants a stale cache and a brief whose live reading differs cold versus warm is rejected, with both outputs printed.

- **Detect orphan cells between the grid and the brief set** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: cell lanes × planner × missing. A grid can be complete and its briefs still skip a cell, because the briefs were written from the ideas rather than the grid. The pack shows the grid lens but no check that joins grid to briefs.
  Done when: `fm` lists every grid cell that has no brief and no recorded n/a, and a Mission with one orphan fails its filing check.

- **Give every n/a cell a falsifier command and sample them** — SECURITY — value 4 — effort M — risk med — category: honesty
  Why: cell web UI × user × unsafe. An n/a is the easiest way to hide a gap, and the user cannot tell a true n/a from a lazy one. The steers already demand "a recorded n/a" per cell, so the audit belongs there.
  Done when: each n/a stores a one-line command that would show it applies. A nightly sample runs 5 of them, and a planted false n/a is caught.

- **Cap exhaustiveness by a named budget and list cells skipped for it** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: cell unattended run × agent × slow. "Cover the whole space" has no stopping rule, and the user's standing rule is not to stop for budget. Cells skipped must therefore appear as "unreached (budget)" rather than vanish.
  Done when: a Mission run with a tiny cell cap emits an "unreached" list whose count equals grid cells minus cells handled.

- **Show the nearest non-match beside every "already built" hit** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: cell canary × agent × unclear. Canaries "near the idea" are a carried gap, and a hit alone does not show why a near thing counts as the same. Seeing the closest miss lets the reader judge. The dropped-ideas list shows many "already built" drops.
  Done when: a canary report prints a hit and the closest rejected neighbour with a one-line reason, for 5 of 5 sampled drops.

- **Record which scope width a request was taken at** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: cell CLI × user × unclear. The user's phrasing like "#2 Exhaustive thinking" admits narrow, typical or broad readings, and nothing records which was chosen. A disagreement later can't be located.
  Done when: each filed Mission carries a "width: narrow|typical|broad, because …" line, and `fm` shows it with the left-out list.

- **Promote a left-out cell to a task in one key** — FEATURE — value 4 — effort S — risk low — category: capture
  Why: cell CLI/web × user × missing. A left-out list the user has to retype into a task is a list they won't act on. Assumption: the receipt already names cells with stable ids.
  Done when: `fm omit take <cell>` files a task prefilled with the cell's context, and the receipt marks that cell as taken.

- **Cap tasks filed from left-out cells per day** — SECURITY — value 3 — effort S — risk low — category: loop control
  Why: cell unattended run × agent × unsafe. Left-out cells flowing back as seeds could grow the queue without bound in an autonomous run. The steers say the tower advances itself.
  Done when: with a cap of 3, a run with 10 left-out cells files 3 and shows 7 as "later", and a test confirms it.

- **Re-run each closed brief's live reading on a schedule and flip its cell back** — FEATURE — value 4 — effort M — risk med — category: regression
  Why: cell site/web × user × wrong. A filled cell stays filled even after the live state it measured drifts, so the grid goes quietly out of date. Assumption: live readings are cheap and read-only.
  Done when: a planted regression turns a cell from filled to "regressed" within one scheduled pass, and the Genesis page shows it.

- **(wild) Let the user drag cells on a phone-sized board** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. Cell web UI × user × missing. A 2D board of surfaces by failure modes, where a drag marks a cell now, later or never, would turn the omission list into a conversation. Assumption: the user would use it.
  Done when: dragging a cell writes a decision record, and the next Mission pack reads it.

- **(wild) Add a hostile "other agent" column to the grid** — SECURITY — value 4 — effort M — risk med — category: adversary
  Why: wild. The actor list usually stops at user, agent, lanes and unattended. A fifth actor, an injected instruction in pasted content, crossed with each surface would show which cells it can reach. The pack's own `<pasted_content>` rule shows the threat is real.
  Done when: the grid has an "injected text" row, and each cell there has a brief, an n/a with a falsifier, or an "unreached" mark.

- **(wild) Settle each left-out cell against what the user later asked** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: wild. The "dissents scored against outcomes" gap has a twin: omissions. If the user typed about a left-out cell within 30 days, Foreman missed it. That gives a precision and recall number for deciding what to leave out.
  Done when: a settled report lists left-out cells as asked, not asked or unknown, and a seeded user ask matching a cell is counted.

- **Shade grid cells by how often the user's real sessions touch them** — FEATURE — value 3 — effort M — risk low — category: prioritisation
  Why: cell web UI × user × unclear. Equal-weight cells hide that some surfaces (the CLI) see far more use than others. Usage counts exist in the ledgers.
  Done when: each cell on the grid page carries a 30-day touch count, and the empty cells are sorted by it.

Cells I left empty: site × other agents (nobody but the user reads it, and the leak scan covers the unsafe case), fm code × user × slow (no evidence the pack gives of slow here), and hooks × user × missing (hooks are invisible to the user by design).

Next question: which of the grid's actor columns has never had a real event in the ledgers, so its cells are all guesses?
Next question: when a Mission's grid and the user's own typed ask disagree about what the surfaces are, which one wins and who is told?
