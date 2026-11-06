# Brainstorm — lens: approaches

Answering one earlier question first: the cells that are really one capability are probably the ones where the `fmforesight` code never branches on stage or surface. Idea 2 finds them mechanically.

- **Set-cover the 58 cells over MASTER.md's module clauses** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: `fmrecall.covered` already splits MASTER.md clauses at semicolons with their task ids, and the lessons say most of #2, #11 and #12 was already built. A script maps each clause to the cells it plausibly serves, then picks the smallest clause set that covers the most cells. What stays uncovered is the gap list. Trade-off: keyword mapping can over-claim, so each hit still needs a grep of the cited symbol.
  Done when: running the script prints, per cell, `clause + task id` or `UNCOVERED`, and a unit test with a planted uncovered cell reports it.

- **Collapse cells by signature analysis before writing anything** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: assumption: many `fmforesight` functions take no stage or surface argument. An AST pass lists each public function's parameters and callers. Cells whose cited function has no stage branch merge into one capability with one probe. Trade-off: it undercounts when stage behavior lives in the caller.
  Done when: the pass outputs groups such as "N cells → function X", and each group has exactly one probe.

- **Pivot the grid by signal source, then project back to stages** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: Anticipation consumes a handful of ledgers: the asked stream, friction, outcomes bets, intake, ci-watch, git co-change and `fm doctor`. A row per source (6–8) is more honest than 58 stage cells. Each stage cell then points at a source row plus a delta. Trade-off: the grid shape changes, and gen-0's grid rule must permit it.
  Done when: the sweep accepts the pivoted table and every original cell id resolves to a source row.

- **Fill only evidenced cells this generation and hand the rest to the next Seed** — CLEAN — value 3 — effort S — risk low — category: process
  Why: the standing rule says empty cells go to the next Seed, and "no empty cells" ends the run, not a generation. Padding to reach 58 invites templated prose. Trade-off: it leaves the headline count short.
  Done when: the report lists filled cells, each with a grounded citation, and unfilled cells, each with a reason. No cell is filled without a citation.

- **Stamp stage and surface at the call site and fill from the trace** — FEATURE — value 4 — effort M — risk med — category: observability
  Why: assumption: cells are checked against file existence, not behavior. `fmforesight` entry points would write `{stage, surface, function}` to a trace file when `FM_TRACE` is set. Running the exam scenarios and `fm drive` then fills the cells that actually ran. Trade-off: it only fills cells the scenarios reach, and the gaps are the point.
  Done when: a run produces a trace, and a cell with no trace row stays empty.

- **Cite the founding commit for each cell with git pickaxe** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: `git log -S<symbol>` gives the task id that introduced each predictor, and its message gives the failure it answered. Cells then cite a task id instead of prose. Trade-off: squashed history loses the id.
  Done when: each filled cell carries a `T-nnnn` that `git log` confirms touched the cited symbol.

- **Sample-audit the filled cells with lot-acceptance rules** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: the open question is whether a filled cell's cited file still behaves as claimed. Running all 58 behavior probes is expensive. Run a random 8, and if one fails, rerun the whole lot. Trade-off: it gives statistical rather than certain assurance.
  Done when: the sweep runs a seeded sample, and a planted broken cell is caught.

- **Reverse-map the dropped-as-built ledger onto cells** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the "dropped: built" entries are asks Foreman already served. Each names a file, such as the `fmexam.py:2893` guard-arm drop. Mapping them to cells gives free, user-evidenced fills. Trade-off: it covers only past asks.
  Done when: every "dropped as built" entry tagged Anticipation maps to at least one cell or a stated reason.

- **Crawl the web UI as the probe for its surface columns** — FEATURE — value 3 — effort M — risk med — category: web UI
  Why: web UI is the only surface in the pack. A headless crawl of each page lists the elements and routes that show forecasts, heads-ups or "already built". Routes map to stages, so the web-UI cells come from the DOM. Trade-off: it needs a browser dependency, and it is blind to features that never reach the UI.
  Done when: the crawl outputs route → forecast elements, and a page with none leaves its cells empty.

- **Wild: Pickaxe the plain-vs-foreman exam transcripts for anticipation moments** — FEATURE — value 3 — effort L — risk med — category: evidence
  Why: assumption: exam transcripts exist and record when Foreman flagged something before it happened. Scanning them for early flags gives real, outcome-linked evidence for the flag-before-it-happens cells. Trade-off: the exam is deferred to the end of the run, so this fills later.
  Done when: each cell filled this way cites a transcript line number.

- **Wild: Fill cells by deletion order** — CLEAN — value 2 — effort M — risk med — category: coverage
  Why: in a scratch copy, remove `fmforesight` functions one at a time, run the fast tests, and record which cells' claims break. A function whose removal breaks nothing means its cells are decorative. Trade-off: slow, and it needs good tests.
  Done when: each cell is tagged "load-bearing" or "decorative" with the removed symbol named.

- **Wild: Let the empty cells compete for the user's attention** — FEATURE — value 2 — effort M — risk low — category: prioritisation
  Why: rank the cells by how often their column's stage appears in the user's asked stream. This is a "do less" cut that fills the top 15 in depth and leaves the rest as one-line stubs. Trade-off: it risks rarely-used but high-harm cells.
  Done when: the ranked list is generated from the asked stream, and the top cells have behavior probes.

Next question: Which of the 58 cells does a path that is not `fm next` or the drive reach, such as the SessionStart note, and are those cells reached only when the user opens a session?
Next question: If the grid were pivoted by signal source (idea 3), which source has no predictor at all?
