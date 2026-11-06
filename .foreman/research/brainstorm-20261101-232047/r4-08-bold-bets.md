# Brainstorm — lens: bold bets

- **Compile the 58 cells from live deliberation traces** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: the user's rule says a cell counts only if it names a concrete capability grounded in a file, with no reused phrasing. The pack's prior ideas keep proposing prose fills; a trace-driven compiler removes the templating risk at the source.
  Done when: `fm genesis coverage --compile` writes every Exhaustive-thinking cell from recorded plan-gate/race/blast traces, each citing a file and symbol, and the templating lint passes on all 58.

- **Gate irreversible steps on a door ledger the model can't write** — SECURITY — value 5 — effort M — risk med — category: deliberation safety
  Why: gen-0 #2 asks for failure modes and blast radius; the pack shows door-gate logic (fmdoors, "irreversible AND ambiguous") but the model could still edit its own classification. Assumption: the ledger is currently model-writable.
  Done when: a test where the model tries to downgrade a one-way step's class in the ledger is refused, and the step runs only with a user-signed or table-derived class.

- **Run a blind rival planner and show only the disagreements** — FEATURE — value 5 — effort L — risk med — category: planning
  Why: "Choose by evidence, not first instinct" needs an independent reading; the writer and judge are both Foreman's own models, which the user's steer on non-self-authored signals warns against.
  Done when: for an M/L task, `fm plan` runs a different-family tool-less child on the request alone and prints a three-column diff (user's words, plan, rival); disagreement on tier or options raises depth.

- **Pre-register every confidence and score it at close** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: plan "Choice N (NN%)" and ship bets already exist; the gap is a write-once row per assumption with a resolver named at placement.
  Done when: `fm outcomes --judgment` prints a reliability table by evidence class, and a bet whose resolver is its own author is flagged.

- **Backtest every gate threshold on closed tasks before it can refuse** — FEATURE — value 4 — effort L — risk med — category: gate tuning
  Why: thresholds (distinct-options check, tier floor, race trigger) are hand-set; the user's steers demand outcome signals Foreman didn't author.
  Done when: a proposed knob change shows, on the last N closed tasks, how many plans it would have refused and how many of those were later reopened; enforcement needs a shadow period.

- **Judge races by minimax regret across readings, with a fragility score** — FEATURE — value 4 — effort M — risk low — category: race
  Why: the race exists but picks by pass/fail; the readings list is already required by the plan gate and unused when choosing.
  Done when: the race receipt shows each finalist's worst-case result across readings and a "pick flips if X" line, tested on a fixture where pass/fail ties.

- **Make "unknown" the blast-radius answer when the graph is blind** — FIX — value 4 — effort S — risk low — category: blast radius
  Why: assumption: `fm graph blast` returns "none" for files outside its parsed languages, which reads as safe.
  Done when: a task touching a file type the graph can't parse yields "Risks: unknown (graph blind to .X)" and the plan gate treats it as non-empty.

- **Shadow-fill the grid with two independent fillers and treat disagreement as the gap** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the "58 empty cells" must be real, not templated; disagreement between two blind writers marks cells that are really unknown.
  Done when: running both fillers yields a report listing cells where they cite different files, and those cells stay unfilled.

- **Wild: Replay the user's last 20 corrections through today's plan gate nightly** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: wild; the "asked/steered" stream is a ready-made test corpus of first-instinct plans the user rejected. Done when: `fm night` reports how many of the 20 would now be caught, and a drop files a task.

- **Wild: Pre-mortem child told the change already failed in production** — FEATURE — value 4 — effort M — risk low — category: edge cases
  Why: wild; edge-case lists written by the planner share its blind spots, while a child given the failure as a premise must explain it. Done when: for L tasks the plan gets a "how it failed" list, and at close each item is marked checked or not.

- **Wild: A "trap" exam kind where the obvious fix is wrong** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: wild; tests whether exhaustive thinking changes outcomes versus plain Claude, measured on a tool-less-child-authored corpus per the user's exam steer. Done when: `fm exam` includes trap scenarios and the scorecard shows foreman vs plain pass rate on them.

- **Wild: Refuse the 59th cell unless one is retired** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: wild; the pack shows grid growth (58→61 cells across briefs) against the lean ratchet. Done when: the coverage linter rejects a net-new cell without a retirement or merge entry.

- **Fail visibly when a deliberation child dies or answers on the wrong model** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: a killed rival/blast/race child currently degrades to a shorter plan silently; the pack's trend is silent fallbacks.
  Done when: killing a child mid-run leaves a "deliberation incomplete: stage X" line in the finish receipt and `fm doctor`.

Next question: Which of the 58 cells are cheapest to prove by a probe that fails on the parent of the feature commit, and which have no such probe?
Next question: When no user is present, what does each deliberation stop-and-ask default to, and where is that written down?
