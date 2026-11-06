# Brainstorm — lens: approaches

- **Anchor each cell to a public `fmforesight` symbol** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: assumption: gen-0 says to "grow `fmforesight`", so its public functions are the capability's real surface. Cells that cite files can hide behind a path that still exists; a symbol can't.
  Done when: `fm genesis check` lists every public `fmforesight` function with the cell(s) citing it, and fails on a function no cell cites and on a cell whose symbol no longer exists.

- **Write each cell as a three-field form: predicts, read by, backtest** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the standing rules reject templated prose and require a session path, and Mission 3-5's lesson is that a heuristic names its backtest. Three typed fields can be linted, and prose can't.
  Done when: a cell missing any of the three fields, or whose "read by" names no session path, is rejected by `fm genesis put`; a form with all three passes.

- **Check each cell's quoted user phrase as a substring of the asked stream** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: the pack shows ~25 "asked" lines; a cell written as "without this the user would type: <verbatim line>" is mechanically checkable, so no cold read is needed for that part.
  Done when: a cell whose quoted phrase isn't found in the recorded asks is refused, and a cell with a real one passes.

- **Contract-test the foresight JSON that the web UI consumes** — FEATURE — value 3 — effort M — risk med — category: web UI
  Why: the only surface found is the web UI, so many surface columns are really one contract. An open question asks which pages a real session path reaches. Assumption: the UI reads a JSON shape from `fmforesight`.
  Done when: one schema test pins the foresight payload, and every surface-column cell cites a schema field, so renaming the field turns those cells red.

- **Fill in dependency order so later cells cite earlier ones** — CLEAN — value 3 — effort S — risk low — category: process
  Why: user model → signal → forecast → draft → flag → dismissal is a chain. Filling the stages that others depend on first lets later cells cite them instead of restating them. This is a cheap way to avoid duplicated phrasing.
  Done when: the fill order is a stored list, and every later cell cites at least one earlier cell id where its stage reads another's output.

- **Drip-fill three cells per night from the night tick** — FEATURE — value 3 — effort M — risk med — category: unattended
  Why: assumption: `fm night` already ticks (T-2542), and the user asked for no mid-run questions. A slow fill with a cold read per cell spreads cost and surfaces fewer bad cells at once.
  Done when: after two ticks, exactly six new cells exist, each with a passed cold read, and a morning line in `fm status` names them.

- **Count a real gap as a filled cell, only when it is filed with a task** — FIX — value 4 — effort S — risk low — category: coverage
  Why: the coverage rule counts "a real gap" as a cell. The cheapest honest fill for an unbuilt predictor is a deferred task id plus its grounding, not invented prose. The open queue already holds many "Later from" bundles that read like this.
  Done when: a gap cell without a live task id is rejected, and the sweep reports the share of the 58 that are built, gap or n/a.

- **Settle conflicting fills by a blind second filler** — FEATURE — value 3 — effort M — risk med — category: coverage
  Why: "Run two independent fillers" is listed, but only as a diff. Here the tie-break is a third tool-less child that sees the two cells without their authors and picks the one citing a symbol that exists.
  Done when: for a seeded pair of conflicting cells, the verifier selects the one whose citation resolves, and logs the choice.

- **Wild: Feed the 58 cell prompts to `fmforesight` itself** — FEATURE — value 4 — effort M — risk med — category: dogfood
  Why: wild. If the forecaster can't produce even a sentence for "what does the user ask next at the plan stage on the web UI", that cell is a true gap, and what it does produce is real output rather than prose.
  Done when: a run over all 58 prompts records produced or abstained per cell, and every abstained cell becomes a gap row.

- **Wild: Rebuild the API from the grid alone** — FEATURE — value 3 — effort M — risk med — category: coverage
  Why: wild. A tool-less child sees only the filled cells and lists the functions it expects `fmforesight` to have. Functions it invents that don't exist expose cells that promise too much. Real functions it cannot guess expose cells that say too little.
  Done when: a diff of guessed against real symbols is stored, and each divergent cell is flagged vague or overclaiming.

- **Wild: Let filler children bid by confidence and leave low bids as gaps** — FEATURE — value 2 — effort M — risk med — category: coverage
  Why: wild. The mission asks for all 58, but the standing rule forbids padding. Having each filler state a 0-1 confidence in its own cell, and leaving anything under a floor as an explicit gap, makes the unfilled remainder the signal.
  Done when: the report lists cells filled above the floor and cells left as gaps, and no cell under the floor is counted.

- **Do less: file only the cells a past incident touched, and mark the rest "unreached" with an expiry** — CLEAN — value 3 — effort S — risk low — category: process
  Why: Mission 3-5's lesson says most of #2, #11 and #12 was already built, so many Anticipation cells are probably the same. The ledger and decisions.md show which ones had a failure.
  Done when: each cell holds either an incident id, a built path, or "unreached until <date>", and the sweep reds an expired "unreached".

- **Replace the exhaustive grid pass with a shared evidence file each filler appends to** — CLEAN — value 2 — effort S — risk low — category: tooling
  Why: assumption: every filler greps the same repo for the same things. One shared file of grep results, written once, removes the repeated search and gives the cold reader one place to check citations.
  Done when: the fill run makes one repo search per distinct term, and every cell citation appears in the evidence file.

Next question: which of the 58 cells fail if the web UI is the only surface, and which survive only because the columns count one surface several times?
Next question: after the fill, what in the sweep re-runs the cited behaviour on the next generation's code, rather than re-checking that the file exists?
