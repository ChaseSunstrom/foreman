# Brainstorm — lens: approaches

- **Ground every cell in a cited file before writing prose** — FIX — value 5 — effort M — risk low — category: coverage
  Why: the Missions 3-4 lesson says most of what looked missing was already built, and the "real coverage" steer rejects any cell not tied to a file or a recorded gap. Assumption: many of the 58 cells already have a plan gate, race, blast-radius or `fm decide` path behind them. Trade-off: it is the cheapest route and the most honest one, but it exposes the true gaps, which then become build tasks.
  Done when: each of the 58 cells holds a `path:line` or verb that exists (checked by script), and any cell with no match is filed as a task, not worded around.

- **Make each cell a named red-first test** — FEATURE — value 5 — effort L — risk med — category: coverage proof
  Why: the cold-read steer fails templated cells, and a test name cannot be templated. Assumption: the plan-gate and race code already have tests that can be mapped to cells. Trade-off: it is strongest against rot, but it is slow and may need new tests for the real gaps.
  Done when: for 10 sampled cells, deleting the cited behaviour in a scratch copy turns the named test red.

- **Fill from the user's "asked" stream, not from the grid** — FEATURE — value 4 — effort M — risk low — category: coverage evidence
  Why: the pack's asked/steered lines show where the exhaustive-thinking gates failed in practice (T-2341 door gate, the fifth BEYOND row, "docs-unknown proof"). Assumption: ask history maps onto stage × surface cells. Trade-off: it is grounded in real use, but cells with no ask history stay empty and need another method.
  Done when: each filled cell cites at least one T-id from the asks or steers, and the report lists the cells that have none.

- **Generate one blind scenario per cell and record what the gate does** — FEATURE — value 5 — effort L — risk med — category: coverage observation
  Why: standing rule: exam scenarios come from a tool-less child that never sees Foreman's code. Assumption: the plan gate can be run on a request without side effects. Trade-off: it measures behaviour instead of describing it, but it costs child calls and needs a dry-run mode.
  Done when: each cell holds a scenario id plus the gate's observed output (readings listed, options distinct, blast radius named), and the zero-token arms replay them.

- **Run two independent fillers and treat disagreement as the gap** — FEATURE — value 4 — effort M — risk low — category: coverage method
  Why: a single writer produced the templating the steers forbid. Assumption: two different model families would word cells differently when the evidence is real. Trade-off: it is cheap duplicated effort, and where the two disagree the cell is probably a real gap, but agreement can still be shared hallucination.
  Done when: a diff of the two fills lists the disagreeing cells, each resolved by evidence (a grep or a run), and none by a vote.

- **Mark n/a only after a recorded counterexample search comes back empty** — CLEAN — value 4 — effort S — risk low — category: coverage honesty
  Why: "doing less" is legitimate for surfaces that have no such stage (the web UI has no edit step), but the steers forbid unsupported n/a cells. Assumption: some of the 58 are web-UI-by-stage combinations that really do not exist. Trade-off: it is quick and shrinks the work, but weak searches could hide real gaps.
  Done when: each n/a cell stores the search command and its empty result, and `fm genesis sweep` reruns them and reds any that now match.

- **Replay the last 30 closed tasks and mark which cells they exercised** — FEATURE — value 4 — effort M — risk low — category: coverage evidence
  Why: assumption: the ledger and `fm outcomes` hold plans with readings and options. Trade-off: it gives a frequency weight so the heavy cells get depth first, but cells nobody exercised stay unknown, not proven absent.
  Done when: each cell shows a use count from the ledger, and the build order is sorted by that count.

- **Show readings, options and the race on a web UI "deliberation" page** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the surface list is the web UI only, and the pack's own ideas ask for scrubbing a decision tape and photo-finish replays, so the web UI × plan and × race cells are likely real gaps, not n/a. Assumption: plan data is stored in a form the UI can read. Trade-off: it is a visible deliverable, but it adds UI weight against the lean ratchet.
  Done when: opening a finished task in the web UI shows its readings, options, the chosen option's falsifier and any race result, with empty, loading and error states screenshotted.

- **Fill in batches of ten, rotating writer and cold reader** — CLEAN — value 3 — effort S — risk low — category: coverage process
  Why: the templating lint has to compare against neighbouring rows, and a 58-cell single pass drifts into shared phrasing. Trade-off: it costs more calls, but each failure stays small and goes back to the writer, as the cold-read steer requires.
  Done when: five batches are each filed only after a Haiku-then-Sonnet read passes, and a n-gram check against all earlier cells shows no reused phrase.

- **Wild: let a stubborn-reader child try to prove each cell false** — FEATURE — value 4 — effort M — risk med — category: coverage adversary
  Why: assumption: a child with only the cell text and the repo's verb list can find a counterexample faster than a human review. Trade-off: it is a strong check, but the child may produce false positives that waste tasks.
  Done when: every cell has a "tried to falsify" line with the child's best attempt, and any cell it falsified is rewritten or turned into a task.

- **Wild: make the grid a by-product of running the plan gate** — FEATURE — value 3 — effort L — risk high — category: coverage design
  Why: assumption: if every plan emitted which stage and surface it touched, cells would fill from real use and a cell stays empty until a real task hits it. Trade-off: it is always current and unfakeable, but it is slow to fill and cannot finish a generation on its own.
  Done when: finishing a task appends its stage × surface hit to a ledger, and the sweep marks the cell filled from the ledger.

- **Wild: delete the cited feature in a scratch copy and watch what survives** — FEATURE — value 3 — effort M — risk med — category: coverage mutation
  Why: cell mutation testing exists only as a one-line wild idea in the pack. Trade-off: it is a direct test that a cell is real, but it is slow and fragile across a repo of 2072 files.
  Done when: for a sample of 10 cells, the scratch copy with the cited path stubbed fails fm check, and the script prints which cells did not.

Next question: Which of the 58 cells are web UI × stage combinations that can only be filled by a visible page, and which are only filled by a gate in a hook, where the user never sees it?
Next question: When a cell's grounding file is later renamed or deleted, who notices, and does the sweep turn the cell red the same day?
