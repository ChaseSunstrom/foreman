# Brainstorm — lens: sci-fi 2030 worked back

- **Write gen-0 from one line or nothing** — FEATURE — value 5 — effort L — risk med — category: genesis core
  Why: gap map #13 tier 3 is missing. The inputs already exist: `fm map`, git co-change history, the user's steers and corrections, and the gap map. Assumption: the existing hand-written gen-0 can serve as the reference grader.
  Done when: on 3 held-out generated projects, given "make this great" or empty input, `fm genesis seed` writes a gen-0 that a checklist grader finds covers every MUST, NEVER and section of the hand-written reference.

- **Run the tower as a resumable state machine** — FEATURE — value 5 — effort L — risk med — category: orchestrator
  Why: the tower orchestrator (tier 4) is missing, and the storage verbs (init/put/status) exist without a driver. Assumption: a step cursor plus an append-only event log in the tower store is enough to resume from.
  Done when: killing `fm genesis run` mid-generation and rerunning resumes at the recorded step with no repeated child spend, and a fresh session reaches the same next step from the tower files alone.

- **Write a per-project capability spec with a held-out exam** — FEATURE — value 5 — effort M — risk med — category: spec/exam
  Why: the gap map names a per-project spec ("complete and best-in-class for this kind of project"). `fm exam gen` already guarantees quotas, with at least 9 scenarios per capability and at least 3 held out.
  Done when: `fm genesis spec` writes spec.md with one capability per line, each linked to at least 9 exam scenarios, and the held-out third is absent from every file the rewriter child can read.

- **Select by exam and record lineage** — FEATURE — value 4 — effort M — risk med — category: selection
  Why: the rewrite rule is already specified: it stays only if it closes more exam scenarios than its parent. lineage.md is missing.
  Done when: a rewrite that ties or loses is rejected, and lineage.md records the parent, the scores, the cost and a one-line reason for the loss.

- **Check drift against gen-0's MUSTs and NEVERs mechanically** — SECURITY — value 5 — effort M — risk low — category: guardrail
  Why: inversion risk: a self-writing harness drifts toward easier exams and weaker rules. gen-0 is read-only, so its clauses can be hashed and each generation diffed against them, with `fm second` as the cold reviewer.
  Done when: a planted generation that drops a NEVER or softens a MUST fails the drift check with the clause cited, and a faithful generation passes.

- **Fill the coverage grid until no cell is empty** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the request names "a coverage grid with no empty cells". `fm exam` has 11 scenario kinds, so the grid is capability × kind.
  Done when: `fm genesis grid` prints the matrix and exits non-zero while any cell has no scenario or an explicit "n/a: reason". The generation does not close until it is clean.

- **Keep a not-yet ledger and retry it every generation** — FEATURE — value 4 — effort S — risk low — category: ledger
  Why: the user's standing steer is that no idea is killed for ambition. A failed spike gets at least 2 different approaches, then a ledger entry with its blocker, retried each generation.
  Done when: each generation start re-attempts every ledger entry, an entry whose blocker has cleared moves into the queue, and entries are only removed for proven harm or an exact duplicate.

- **Stop a generation early on a cost-per-scenario rule** — PERFORMANCE — value 4 — effort M — risk low — category: economics
  Why: the economics-of-a-generation lens. Inversion also warns that it could burn a week of usage on one project. Assumption: `fm exam` already records cost per arm.
  Done when: a generation stops when the marginal cost per newly closed scenario exceeds a set multiple of the running median, and a rewrite that ties at 3× the cost is rejected and logged.

- **Start by itself when the queue runs dry, through a candidate and the user's yes** — FEATURE — value 4 — effort M — risk med — category: auto-start
  Why: gap map #13 says the routing line in rules/foreman.md is protected core, so a candidate patch plus the user's yes is required. It also says `fm loop` and `fm scout` are the triggers.
  Done when: with an empty queue and a gap map above a threshold, the loop proposes `fm genesis run` as a candidate and starts nothing until the user approves. A budget cap applies to the run and the patch is never auto-applied.

- **Carry winning templates over as defaults** — FEATURE — value 3 — effort M — risk low — category: carry-over
  Why: the spec asks that winning Seed and mission templates, lenses that paid off and lineage become defaults. `fm ideas` already tracks lens rates.
  Done when: a second project's gen-0 draft cites at least one carried default, and removing the carry-over store changes the draft.

- **Dream mode: run the tower overnight, then hand over a one-screen morning digest** — FEATURE — value 4 — effort L — risk med — category: autonomy — wild
  Why: assumption: in 2030 the tower runs while the user sleeps. The slice buildable today is waiting for a usage reset, running within a budget, and ending with a digest of what changed, what lost and what needs a yes.
  Done when: a run that hits the usage cap waits and resumes, and the digest lists every self-change with its exam delta and one-keystroke revert.

- **Cartridges: export a tower's genome and cold-start a similar project from it** — FEATURE — value 3 — effort M — risk med — category: portability — wild
  Why: assumption: projects of one kind (CLI, web app, library) share most of their best-in-class spec. A portable bundle of seed, mission templates, lens payoffs and spec skeleton would shorten the stranger's first ten minutes.
  Done when: importing a cartridge from a Python CLI into a new Python CLI cuts the draft spec's unanswered capabilities, as the grader counts them, versus a cold start. No project-specific text leaves the owner's machine.

- **Run a red-team twin that attacks each rewrite and regenerates the exam** — SECURITY — value 4 — effort L — risk med — category: adversarial — wild
  Why: inversion: overfitting the held-out third and rewriting toward easier exams. A tool-less child authors fresh scenarios aimed at the new rewrite's weak points, and a leak detector flags rewrites that mention held-out scenario ids.
  Done when: a planted rewrite that memorises held-out answers scores high on the old exam and fails the regenerated one, and the leak detector flags it.

- **List the cold-start assumptions for one-glance veto** — FEATURE — value 3 — effort S — risk low — category: cold-start
  Why: the cold-start stranger lens. Without memory, a wrong guess about project kind poisons the whole spec. The pack shows the user steering after the fact.
  Done when: `fm genesis seed` on an unseen repo ends with a numbered "I assumed…" list with a confidence for each, and vetoing an item regenerates only the sections that depended on it.

Next question: What does a user's yes look like for a self-change that touches protected core, and how does Genesis prove the change is reversible before asking?
Next question: Where does the tower store its state when a project is a monorepo or has no git history, and does the drift check still have a stable gen-0 to hash?
