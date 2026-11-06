# Brainstorm — lens: deepen: coverage

- **Build a cell compiler that emits coverage.md from probes** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: the existing ideas (probe-derived cells, lint, markers, verb tags) are one pipeline. Each of the 61 cells (stage × surface) gets a probe that returns file:line evidence, an exam result or an n/a rule, and a compiler writes the row. Standing rule: "a cell counts only when it names a concrete capability grounded in a file or real gap."
  Done when: `fm genesis coverage --compile` regenerates all 61 cells from probe output alone, and a cell whose probe returns nothing is written as EMPTY, not prose.

- **Gate cell writes on a templating linter with a diff-to-neighbours check** — SECURITY — value 4 — effort S — risk low — category: coverage
  Why: the rule says "no phrasing reused across rows", and that's mechanical. Compute n-gram overlap against row and column neighbours at write time and refuse the write over a threshold, naming the twin cell.
  Done when: writing two cells that differ only by the surface name is refused, quoting the twin.

- **Pair every cell with a lean cost line (bytes, p95 ms)** — FEATURE — value 5 — effort M — risk med — category: coverage × lean
  Why: #12 is "stay lean", yet cells carry no cost. Record injected bytes and hook p95 delta per cell's capability (p95 now 278 ms, context 387k/reply). A cell that grows either without a measurement is marked pending per T-2503.
  Done when: `fm genesis sweep` prints a per-cell delta and goes red on a cell whose hook p95 rose with a measurement attached.

- **Add a deny-class matrix: guard fires on every surface** — SECURITY — value 5 — effort M — risk low — category: coverage × safety
  Why: the guard blocked interpreter-code-driving 42x, yet the cells for Codex, Gemini, opencode, MCP and headless are unproven (T-0335 to T-0337 are blocked). Replay a fixed set of dangerous commands per surface, and mark each surface's result as blocked, bypassed or unreachable.
  Done when: a table of deny classes × 8 surfaces prints, and any "bypassed" cell fails `fm doctor`.

- **Make n/a cells carry an expiry and an adversary probe** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: the standing steer says every Seed retries items a new capability may unblock. An n/a with a blocker (libappindicator, a missing CLI) should be re-probed each generation, and it flips to EMPTY when the probe now succeeds.
  Done when: installing a blocker's missing dependency in a fixture flips its cell from n/a to EMPTY on the next sweep.

- **Reverse-map every verb to a cell and flag orphans** — CLEAN — value 4 — effort M — risk low — category: coverage × subtract
  Why: §6 requires subtraction ("unused verbs and cards"). A verb that maps to no cell and has no session caller is a removal candidate, which turns coverage into the subtraction list.
  Done when: `fm burden --by-verb` shows a "cell" column, and orphan verbs are listed with their last use.

- **Weight cells by user-visible risk, and fill the heavy ones first** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: 61 cells aren't equal. "ship × headless/server" matters more than "learn × site". Rank by outcome-survival data and hand the top ten to the next Seed, since the rule says empty cells go to the next Seed first.
  Done when: the Seed draft opens with the ten highest-weight empty cells and the weights' source.

- **Show a one-screen coverage heatmap on the web UI** — FEATURE — value 3 — effort M — risk low — category: coverage × UI
  Why: the user reads a checklist page. An 8×8 grid coloured by state (probed, prose-only, n/a, empty, rotted) with a click-through to the evidence, and a changed-since marker, makes the rot visible.
  Done when: `fm ui` serves the grid, and clicking a cell shows its probe output and age.

- **Rot detector: re-run each cell's probe on every sweep and turn stale ones red** — FIX — value 4 — effort M — risk med — category: coverage
  Why: a cell grounded in a file breaks silently when the file is renamed (the map is already "as of an older HEAD"). Re-verifying path and symbol existence costs no tokens.
  Done when: renaming a cited function in a fixture turns exactly its cell red.

- **Wild: Let a tool-less child guess each cell blind, then score the gap against reality** — FEATURE — value 3 — effort M — risk low — category: coverage (wild)
  Why: it fits the rule that weakness-finding uses signals Foreman didn't author. The child sees only the stage and surface names and says what a best-in-class tool would have there, and the overlap with the real cell measures what Foreman is missing.
  Done when: a report lists each cell as matched, missed by Foreman or invented by the child.

- **Wild: Treat coverage as a game of cell mutation testing** — FEATURE — value 3 — effort L — risk med — category: coverage (wild)
  Why: delete a feature path a cell cites in a scratch worktree and check that some test or exam fails. A cell whose capability can vanish unnoticed was never really covered.
  Done when: the mutation run reports a survival rate per cell, and surviving cells are marked weak.

- **Wild: Each cell gets a one-line "last time this saved the user" receipt** — FEATURE — value 3 — effort M — risk low — category: coverage (wild)
  Why: tie cells to `fm outcomes` and `fm friction` events, such as a guard block or a held proof. Cells with no receipt in 30 days become candidates for the cut list, which links "pays for itself or gets cut" to the grid.
  Done when: each cell shows a last-fired date and count, and cells with none are listed as unproven.

- **Add a lean budget row to the grid, so cells compete for bytes** — CLEAN — value 4 — effort M — risk med — category: coverage × lean
  Why: the SessionStart note is about 2k chars × 89 and context is 387k/reply, so filling 61 cells could bloat both. Give the grid a total injected-bytes budget, and fail a new cell that would push over it unless it removes something.
  Done when: adding a cell that exceeds the budget fails the sweep and names the cheapest cell to merge.

Next question: Which cells does a real user session ever touch (by trace), and are the other cells measured by anything besides Foreman's own probes?
Next question: When a probe and a cell's prose disagree, which one wins by rule, and does the user see the conflict listed on the page?
