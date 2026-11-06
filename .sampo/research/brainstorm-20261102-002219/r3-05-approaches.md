# Brainstorm — lens: approaches

Answers first. The questions earlier brainstorms left can be settled by choosing an approach that doesn't depend on the harness. Coverage contexts and static reachability (ideas 1 and 2) run under plain Python on any harness, whereas probes that replay sessions depend on Claude Code. Assumption: the goal engine lives in `plugin/lib` and has stdlib-runnable tests.

- **Measure which goal code each stage runs** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: assumption: the goal test suite and the `roundtrip.py` e2e already exercise the goal engine. Earlier ideas fill cells from prose or grep, not from execution. Run them under coverage.py with dynamic contexts tagged by stage and surface, and fill each cell with the functions that actually executed. An empty context is a gap, and a cell can't be templated because its text is a measured function list.
  Done when: a script prints, per cell, the functions executed in that context, and the 58 cells split into measured, unmeasured and n/a without any prose.

- **Fill cells from static reachability off the goal verbs** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: `fm graph blast` and `fm map` exist. Walk the call graph from each goal entry point (the goal verb, session start, `fm next`) and bucket reached modules by stage. A stage with no reached non-trivial module is a real gap. This works on files alone, so it needs no model tokens and no session.
  Done when: for each cell the walker names one entry→function path or reports "unreached", and the output is identical on two runs.

- **Seed gaps from rival tools' public "agent forgot the goal" complaints** — FEATURE — value 4 — effort M — risk med — category: external signal
  Why: the standing rule asks for weakness signals Foreman didn't author. Issues and forum posts about lost goals after compaction, premature "done" and drift each map to a stage×surface cell. Assumption: research tasks may fetch public pages; otherwise use a cached local snapshot. Nothing is sent out.
  Done when: each gap cell cites one dated external complaint (URL and a quoted line) and a Foreman file that handles it, or a filed task.

- **Diff foreman and plain transcripts on goal scenarios** — FEATURE — value 3 — effort M — risk low — category: evidence
  Why: the exam already records both arms. Every event type the foreman arm emits that plain doesn't (plan, checkpoint, done-check, resume note), tagged with stage and surface, is a cell backed by observed behaviour. Event types seen in neither arm point at gaps. Recorded transcripts cost no tokens.
  Done when: a table lists foreman-only events, each mapped to a cell, and unmapped events are listed as candidate new cells.

- **Write each cell as a Given/When/Then executed by a stdlib runner** — FEATURE — value 3 — effort M — risk med — category: cell format
  Why: prose cells can be templated and fail the real-coverage rule. A scenario cell needs a distinct Given (fixture), When (verb call) and Then (observable), run against a throwaway state dir. It is the executable form of "cell = probe" and needs no new dependencies.
  Done when: `fm genesis check` runs every filled cell's scenario and none repeats another's Given/When.

- **Pair every filled cell with an anti-cell** — FEATURE — value 3 — effort M — risk low — category: falsification
  Why: the user's capability text says "knows when it's actually done rather than merely stopped", so false-done is the failure that matters. For each positive cell, name one situation where the capability would wrongly fire (premature done, a plan that grew), and where the code stops that. Cells that can only say "n/a" mark where the done-detector is untested.
  Done when: each filled cell has an anti-cell citing a test or a gap task, and the sweep goes red on a missing pair.

- **Start from the site's and README's public goal claims** — FEATURE — value 3 — effort S — risk low — category: proof before presentation
  Why: the "proof before presentation" rule compares claims to exam lines. Extract each sentence about plans, resuming and done from `site/` and the README, and turn each into a cell whose probe checks the claim. This is the one fill source organised around what the user was promised.
  Done when: every extracted claim is either bound to a cell with a passing probe or filed as a gap task.

- **Run the user's last 40 captured asks as vague goals (wild)** — FEATURE — value 3 — effort M — risk med — category: real workload
  Why: assumption: the capture inbox and `fm intake` history hold enough vague asks. Push them through the decomposer in a scratch state. Stages and surfaces that never fire across real asks are the user-relevant gaps, ranked by how often their asks would have used them.
  Done when: a report lists the cells exercised by n of 40 asks and the cells hit by zero.

- **Fill the cells as the kill-and-resume drill itself (wild)** — FEATURE — value 3 — effort M — risk med — category: dogfood
  Why: the dogfood idea already exists, but nobody ties it to a crash. Run the filling as a goal, kill the session at a random boundary, resume from files, and let the journal of the run supply evidence for the cells it passes through. Cells for crash, compaction and resume get filled by the thing they describe.
  Done when: a kill mid-fill resumes with no repeated or lost cell, and the journal cites it.

- **Do less: fill 15 measured cells and ledger-hold the rest with a re-entry rule** — CLEAN — value 2 — effort S — risk low — category: scope
  Why: Lessons 3–6 say most of the earlier capabilities' items were already built, so many cells are existing. Fill only cells that ideas 1 and 2 prove, and record the rest as held with the blocker. A held cell names the capability that would unblock it and is retried at each Seed, as the standing rule requires.
  Done when: every non-filled cell has a blocker line and a retry trigger, and none is called filled without a measurement.

- **Cold-read only the cells the tools can't resolve (wild)** — PERFORMANCE — value 2 — effort S — risk low — category: cost
  Why: after ideas 1 and 2, only prose-only cells need a Haiku read, and a Sonnet read after a non-pass. Everything the tools resolved skips model review, so the token cost drops and the check stays mechanical.
  Done when: the log shows cold reads run on fewer than half the cells, with zero on tool-resolved ones.

- **Let a tool-less stranger score the finished grid (wild)** — FEATURE — value 2 — effort S — risk low — category: blind check
  Why: a child never shown Foreman's code gets only the capability text and the final 58 cells, then lists the best-in-class goal behaviours the grid still doesn't name. This is a held-out signal Foreman didn't author, and it comes after the fill so it cannot steer it.
  Done when: the child's list is saved, and each item is mapped to an existing cell or filed as a gap.

Next question: which of the 58 cells did ideas 1 and 2 leave as prose-only, and what do they have in common?
Next question: does the goal engine have enough test and e2e coverage that measured contexts would fill more than half the cells?
