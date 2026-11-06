# Brainstorm — lens: simplicity

- **Make `fm genesis` a resumable state machine with one `next` step** — FEATURE — value 5 — effort M — risk low — category: orchestrator
  Why: the orchestrator (tier 4) is missing, and the existing verbs (`ideas`, `mission`, `exam`, `second`, `evolve`) already do each stage. Assumption: the orchestrator needs no new engine, only a stage pointer in tower storage that calls them in order.
  Done when: killing `fm genesis` mid-generation and rerunning it resumes at the recorded stage without repeating finished stages, shown by a test that counts child calls.

- **Write gen-0 with one tool-less call from a fixed template** — FEATURE — value 5 — effort M — risk med — category: gen-0 writer
  Why: the gap map lists the gen-0 writer from one line or nothing. The simplest version fills the hand-written gen-0's section skeleton (MUSTs, NEVERs, sections) from `fm map`, the user's steers and corrections, and the one line.
  Done when: given an empty one-line input on a fixture repo, the output contains every section heading of the hand-written gen-0 and is stored read-only via `fm genesis put`.

- **Reuse `fm exam gen` as the per-project spec exam** — FEATURE — value 5 — effort S — risk low — category: exam
  Why: the exam already has hidden keys, a held-out third, and quotas. The spec should be a list of capability lines, each mapped to exam scenario kinds. Assumption: the 11 scenario kinds cover most "best-in-class for this project" lines.
  Done when: `fm genesis spec` writes N capability lines and `fm exam gen` produces at least 9 scenarios per line, with at least 3 held out.

- **Derive the coverage grid; don't store it** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: a stored grid can drift from reality. Computing capability × scenario-kind from the spec and exam results on demand means an empty cell is simply a missing scenario, and it shows up as a failing check.
  Done when: deleting one scenario makes `fm genesis status` print exactly one empty cell and exit nonzero.

- **Keep the not-yet ledger as one markdown file with a retry counter** — FEATURE — value 4 — effort S — risk low — category: ledger
  Why: the user's standing rule is "no idea killed for ambition", with ≥2 approaches and then a ledger entry that records the blocker. One line per entry (`id | blocker | tries | last gen`) is greppable and diffable. The start of each generation retries the entries whose blocker text changed or whose age passed a threshold.
  Done when: a seeded ledger entry is retried at gen start and its tries count increments, shown by a test.

- **Select with a single comparison: closed scenarios, tie goes to the parent** — FEATURE — value 4 — effort S — risk low — category: selection
  Why: the spec says a rewrite stays only if it closes more scenarios than its parent. Writing that as one function, with the cost ratio logged beside it and not folded into the rule, keeps lineage.md trivial and hard to game.
  Done when: unit tests cover a win, a tie and a loss; the tie and loss keep the parent and log the reason.

- **Cap every run with one budget line, checked between stages** — SECURITY — value 4 — effort S — risk low — category: guardrail
  Why: inversion risks include running forever and burning a week of usage. One `max_generations` and one spend ceiling, read at each stage boundary, stops the run and writes the stop reason to status.
  Done when: with the cap set to 1 generation, a run stops after gen 1 and `status` shows "stopped: cap".

- **Auto-start as a one-line proposal, never a silent run** — FEATURE — value 4 — effort S — risk low — category: auto-start
  Why: the routing line in rules/foreman.md is protected core, so Genesis needs a candidate edit plus the user's yes. Without the edit, `loop` and `scout` only print "queue is dry: run fm genesis?", which is the smallest honest slice.
  Done when: an empty queue in `fm loop` prints the offer once per session and starts nothing.

- **Delete the drift check as a separate stage; run `fm second` on the gen-0 diff** — CLEAN — value 3 — effort S — risk low — category: drift
  Why: a drift check is a cold review of the new generation's Seed against gen-0. That is what `fm second` already does, so the work is a single call with gen-0's MUSTs and NEVERs as the checklist.
  Done when: a Seed that drops a NEVER is flagged by the check in a fixture test.

- **Make carry-over a single `defaults.json` of winners** — FEATURE — value 3 — effort S — risk low — category: carry-over
  Why: the carry-over (winning Seed and mission templates, lenses that paid off) is just the lens_rates and lineage winners written out. One file read at the next `init` is enough. Assumption: lens_rates already exists, given T-0829.
  Done when: a second project's `init` starts with the first project's top 3 lenses listed.

- **Wild: make `fm genesis` the only verb; the subcommands become stages shown in `status`** — FEATURE — value 3 — effort M — risk med — category: UX
  Why: wild. A user who types "make this great" or nothing should never need `put`, `init`, `export`, `live`, `publish`. Those stay as internals. The command picks up wherever the tower is.
  Done when: running `fm genesis` in a fresh repo and again after an interruption each does the right next thing with no flags.

- **Wild: write gen-0 with no model first, by extracting from README, CLAUDE.md, rules and the user's steers** — FEATURE — value 3 — effort M — risk low — category: gen-0 writer
  Why: wild. A deterministic extraction yields the MUSTs and NEVERs as quoted lines with sources. The model is then only allowed to add, never to rewrite, so the gen-0 can't drift from what the user wrote.
  Done when: every MUST/NEVER in the output carries a source file and line, and a test shows the quoted text matches the source.

- **Wild: a one-screen tower receipt that decides whether to continue** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: wild. At each generation's end it prints a single table: scenarios closed, cost, a held-out delta, and a stop/continue recommendation. The user's request for an in-depth tower view stays on the site, and the terminal gets the short version.
  Done when: the receipt is at most 20 lines and its numbers match `exam.jsonl`.

- **Do less: ship the held-out check as a guard against overfit, not a new exam system** — SECURITY — value 3 — effort S — risk low — category: guardrail
  Why: it compares the held-out pass rate with the visible pass rate, and a gap over a threshold blocks selection. This reuses the existing third, with no new machinery.
  Done when: a fixture where the visible rate rises and the held-out rate stays flat loses selection.

Next question: What is the smallest tower (stages dropped) that still closes planted gaps on a held-out project, and which stage, when removed, changes the result least?
Next question: Which stage of a Genesis run costs the most per scenario closed, and does a cheaper model or a cached stage give the same exam result?
