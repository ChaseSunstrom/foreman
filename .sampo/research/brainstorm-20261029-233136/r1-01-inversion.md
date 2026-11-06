# Brainstorm — lens: inversion

- **Cap every Genesis run with a budget envelope** — FEATURE — value 5 — effort M — risk low — category: economics
  Why: assumption: the pack shows `fm genesis` and the tower with no ceiling on generations, USD, tokens or wall-clock. This lens asks about "a week of usage on one project".
  Done when: `fm genesis run --budget gens=2,usd=10` stops at the first limit and `fm genesis status` names which limit hit.

- **Hash-lock the charter (MUSTs and NEVERs) and fail any rewrite that touches it** — SECURITY — value 5 — effort M — risk low — category: drift
  Why: gen-0 is read-only but nothing in the pack shows a hard gate on the self-written spec. The `fm second` drift check is advisory.
  Done when: a candidate rewrite that deletes or weakens one NEVER is rejected at selection, with the line quoted in lineage.md.

- **Make the exam tamper-evident to the thing being graded** — SECURITY — value 5 — effort M — risk low — category: exam integrity
  Why: Genesis writes the per-project spec and the exam, so it could ease them (the lens's "easier exams"). Hidden keys exist, but nothing records a hash chain.
  Done when: grading refuses and flags the run if scenarios or keys differ from the hashes recorded at `exam gen`, and a test that edits a key shows this.

- **Count held-out looks and rotate the third when it's burned** — FEATURE — value 4 — effort M — risk low — category: overfitting
  Why: selection compares rewrites on the held-out third every generation, so the lineage learns it. Evidence: the held-out set is fixed per tower (`fm exam gen` quotas).
  Done when: after N scored looks, status marks the held-out set "stale" and the next generation draws fresh scenarios from a new seed.

- **Select on margin, repeats and cost, not a bare "closes more"** — FIX — value 4 — effort M — risk med — category: selection
  Why: the rule "a rewrite stays only if it closes more scenarios than its parent" lets noise and 3× cost win. The exam has cost arms already.
  Done when: a rewrite that ties, or wins by less than the repeat-run spread, or costs more than k× its parent loses, and lineage.md records the reason.

- **Detect no-progress loops and park the work in not-yet.md** — FEATURE — value 4 — effort M — risk low — category: runaway
  Why: the steer says failed spikes need ≥2 approaches, then the ledger. Nothing in the pack stops a third identical attempt.
  Done when: two generations with the same open scenarios and near-identical diffs halt the tower and add a ledger entry with its blocker.

- **Gate auto-start behind opt-in, cooldown and the user's yes** — SECURITY — value 5 — effort S — risk low — category: autonomy
  Why: the pack says the routing line in rules/foreman.md is protected core and needs a candidate plus the user's yes. Queue-dry is a common state, so it could fire constantly.
  Done when: in a project without opt-in, queue-dry only prints a suggestion. With opt-in it starts once and not again inside the cooldown.

- **Diff privileges at every generation and halt on any new grant** — SECURITY — value 5 — effort M — risk low — category: self-grant
  Why: the lens asks whether Genesis "grants itself something". Generated briefs, hooks and settings are all writable surfaces.
  Done when: a generation whose output adds a permission, hook or allow-rule stops with a diff and waits for approval.

- **Require the empty arm to fail every coverage-grid cell** — FIX — value 4 — effort S — risk low — category: coverage grid
  Why: "no empty cells" can be met with vacuous scenarios. `fm exam` already has oracle and empty arms.
  Done when: a grid cell whose scenario passes the empty arm is flagged "vacuous" and does not count as covered.

- **Mark inferred gen-0 MUSTs as unconfirmed until the user ratifies them** — FEATURE — value 4 — effort M — risk low — category: cold start
  Why: assumption: from one line or nothing, the writer invents MUSTs, and a stranger repo has no history to check them against. Invented MUSTs could later fail good rewrites.
  Done when: each self-written MUST shows its evidence or "guess", and guesses can't fail a selection until confirmed in one bulk step.

- **Red-team twin that games the self-written gen-0 (wild)** — FEATURE — value 4 — effort L — risk med — category: adversarial
  Why: wild. A tool-less child tries to pass the exam with minimum honest work, and each exploit becomes a new scenario. The pack's "outside signals only" steer favors this.
  Done when: a seeded reward-hack (e.g. hard-coding the visible expected output) is found by the twin and appears as a scenario that then fails the cheat.

- **Planted-injection canary in the cold-start corpus (wild)** — SECURITY — value 4 — effort M — risk low — category: injection
  Why: wild. A stranger repo's README, comments or history can say "add MUST: …" and the gen-0 writer reads them as data. The pack notes the existing injection backlog (T-0791).
  Done when: a generated held-out project with an injected instruction yields a gen-0 that doesn't contain it, and the exam fails writers that do.

- **One-command rewind and a STOP file (wild)** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: wild. Self-changes must be reversible. `fm genesis rewind N` restores tower files and carry-over defaults to generation N. A `STOP` sentinel ends any run at the next step boundary.
  Done when: after a bad generation, rewind returns the tower hash to N's, and creating STOP ends a running tower within one step.

- **Make carry-over defaults earn promotion across projects (wild)** — FEATURE — value 3 — effort M — risk med — category: contamination
  Why: wild. A winning Seed or lens from one project can poison the next. Promote a template to default only after it wins in ≥2 projects, and let it decay when unused.
  Done when: a template that won in one project stays project-local, and a second win promotes it with both sources listed.

Next question: What does Genesis do when two of the user's standing steers conflict (e.g. "no idea killed for ambition" against a budget cap), and who breaks the tie?
Next question: How would we notice that a long-running tower has quietly shifted what "great" means for this project, over generations rather than between two?
