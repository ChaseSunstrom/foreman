# Brainstorm — lens: simplicity

Answers first, from the simplicity lens:
- **Steers that assume a live session:** the simplest fix is one `defaults` line per ask class, applied when no one is present. It is cheaper than a new ask path for each steer.
- **Silent unattended failures:** one file the next session reads beats a per-failure channel for every failure class.

Much of what a simplicity lens would propose is already in the list. The ideas below are the ones I don't see there.

- **Derive the stage columns from the plan gate's own headings** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: assumption: the plan gate already names its stages (readings, approaches, outcomes, blast radius). Hand-typed columns can drift from them and leave cells empty that no code path could fill.
  Done when: a test reads the plan gate's headings and fails if `coverage.md` for #2 has a column that matches no heading, or the reverse.

- **Make a cell one resolvable reference and ≤140 characters** — FEATURE — value 5 — effort S — risk low — category: coverage
  Why: the standing rule says a cell counts only when it names a concrete capability with no reused phrasing. Short `path::symbol — what it does` lines are hard to template and easy to check.
  Done when: the linter rejects a cell whose path or symbol doesn't resolve or whose text exceeds 140 characters, and all 58 filled cells pass.

- **Add one read-only Plan page to the web UI** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the only surface found is the web UI, and no idea so far shows the plan there as one page. A single page fills a whole column with one real capability instead of ten n/a entries.
  Done when: a test loads `/plan/<task>` and finds the readings, options and blast radius from the plan file, with an empty state when the task has no plan.

- **Grep once and share the result with every filler** — PERFORMANCE — value 3 — effort S — risk low — category: tower
  Why: the lesson from Missions 3 and 4 is that most items were already built. Each lane re-grepping MASTER.md and `plugin/lib` is wasted tokens and gives different answers.
  Done when: one `built-index` file is written per fill, every filler lane's brief names it, and a lane that claims "gap" for a verb present in the index is flagged.

- **Use a 20-line shingle overlap as the whole templating test** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the "no phrasing reused across rows" rule needs a mechanical check. A word-shingle comparison against neighbouring cells in the row and column is smaller than any semantic check.
  Done when: planting two cells that share a 5-word shingle makes the sweep fail, and the 58 new cells pass.

- **Run cold reads only on cells the linter can't resolve, one read per file** — PERFORMANCE — value 3 — effort M — risk med — category: tower
  Why: assumption: a model reading pointer cells that already resolve adds cost and little signal. The steer requires a cold read on every tower file, so this keeps the per-file read and drops only the per-cell reads.
  Done when: the Haiku read is invoked once per file and skips pointer-only cells, and a planted fake cell is still caught.

- **Make the unattended default for each ask class one line in one file** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: the open question about steers that assume a session, plus the rule never to block on the user. One `defaults` file is simpler to audit than defaults spread through the code.
  Done when: with no TTY, every ask class resolves from the file and logs a `decide --kind costly` entry, with a test per class.

- **Stop the fill when a full column pass adds no distinct capability** — CLEAN — value 2 — effort S — risk low — category: tower
  Why: a fill that reads 58 cells as 58 jobs invites padding. Many cells will collapse to the same existing feature.
  Done when: a pass that yields only cells matching an existing reference marks the column done and writes the rest as "see <ref>".

- **Wild: Compute the grid live and store only exceptions** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: wild; assumption: most cells are "this verb covers this stage". `coverage.md` would then hold only n/a entries and gaps, with the rest read from the verb index each time.
  Done when: deleting a verb from a scratch copy turns exactly its cells red without anyone editing `coverage.md`.

- **Wild: Have a tool-less child compress the 58 cells to the distinct capabilities they really are** — FEATURE — value 3 — effort S — risk low — category: tower
  Why: wild; assumption: padding shows up as many cells collapsing into a few clusters. The count of true capabilities is more honest than the count of cells.
  Done when: the report gives the cluster count and names the cells that collapsed, and each collapsed cell gets "see <ref>" or an expiring n/a.

- **Wild: Refuse the 59th cell unless one is retired** — FEATURE — value 3 — effort S — risk med — category: lean
  Why: wild; assumption: it fits the lean-ratchet steer (pay for growth with deletion). It is in tension with the standing rule that grid areas are never removed from `frame.md`, so retired cells would move to n/a with a reason rather than disappear.
  Done when: adding a cell at the cap fails the sweep until another cell is marked n/a with an expiry.

- **Wild: Make the plan page the one place anything about thinking is shown** — CLEAN — value 3 — effort M — risk med — category: web UI
  Why: wild; assumption: the deliberation tallies, the decision receipts and the race result are scattered across `fm status`, close receipts and `fm doctor`. One page with three sections replaces three renderers.
  Done when: the close receipt, `fm status` and `fm doctor` link to the page instead of printing their own copies, and a test confirms each link resolves.

Next question: which of the 58 empty cells belong to rows or columns that no session path calls, so the reach check would rule them out before any filler spends a token?
Next question: when two cells point at the same file, should they count as one capability or two, and does the lean ratchet need to see that rule before the fill starts?
