# Brainstorm — lens: inversion

- **Mutation-test every self-written MUST** — FEATURE — value 5 — effort M — risk low — category: spec quality
  Why: assumption: a self-written gen-0 can be satisfied trivially, so "covers every MUST" would pass without testing anything. Nothing in the pack checks that a MUST can fail.
  Done when: for each MUST, a generated mutant of the fixture project violates it, and `fm exam` flags the mutant. MUSTs whose mutants go unnoticed are listed as "unenforced" in `fm genesis status`.

- **Count a coverage cell only if plain Claude fails it** — FEATURE — value 5 — effort S — risk low — category: coverage grid
  Why: "no empty cells" rewards padding. The exam already has empty and plain-session arms, so the data exists to tell a cell that tests something from one that doesn't.
  Done when: a cell whose scenarios are all passed by both the empty arm and the plain-Claude arm shows as "padding", and the grid is not complete while any cell is padding.

- **Pin behavior before anyone says "make this great"** — SECURITY — value 5 — effort M — risk med — category: safety
  Why: assumption: a one-line or empty request is the most ambiguous input Genesis gets, and "great" can justify sweeping rewrites of code that works.
  Done when: before any mission may edit a stranger repo, characterization checks for its current behavior exist. A mission diff that breaks one is rejected, and the exam includes a "nothing that worked broke" scenario.

- **Refuse auto-start unless the tree is safe** — SECURITY — value 4 — effort S — risk low — category: auto-start
  Why: the queue running dry says nothing about whether the repo is mid-rebase, dirty, on a protected branch or shared with other people. The pack only gates auto-start on opt-in and the user's yes.
  Done when: auto-start proposes nothing on a dirty tree, a rebase or merge in progress, a protected branch, or a repo with recent commits by other authors. It prints which check blocked it, and a test covers each case.

- **Charge rewrites a context tax** — PERFORMANCE — value 4 — effort M — risk low — category: selection
  Why: assumption: gen-0 and the spec grow each generation and get injected into every session. A rewrite that closes one more scenario but adds 3k standing tokens quietly slows the whole project.
  Done when: selection records the standing-context token delta per rewrite. A rewrite that raises it without closing at least a set number of extra scenarios loses, and the delta shows on the lineage page.

- **Fence Genesis tasks into their own quota lane** — FIX — value 4 — effort S — risk low — category: queue hygiene
  Why: a self-directing tower that files tasks can flood the queue and bury the user's real asks. The open list already shows many deferred "Later from…" items.
  Done when: Genesis-origin tasks are tagged and capped at N open at once, sorted after user tasks, and `fm genesis status` shows the count against the cap.

- **Expire the self-written spec when the project moves** — FEATURE — value 4 — effort M — risk low — category: staleness
  Why: assumption: gen-0 is written from a snapshot. After a framework migration or a big refactor its MUSTs describe a repo that no longer exists.
  Done when: gen-0 records its commit. When git churn since then passes a threshold (files touched under paths the MUSTs cite), `fm genesis status` shows "spec stale", and the next tower run starts with a re-check of each MUST.

- **Scrub carry-over for source leaks** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: carried-over Seed and mission templates are learned from project A's text and are reused in project B's gen-0, and sometimes on the public site page.
  Done when: carry-over entries are checked against a project-specific denylist (names, paths, secrets, private strings). A fixture with a planted private string never appears in another project's gen-0 or in the exported site.

- **Test the author across languages it has never seen** — FEATURE — value 3 — effort M — risk low — category: overfit
  Why: the self-written gen-0 is judged on projects from 6 generated languages, so tuning to those fixtures is a quiet way to overfit.
  Done when: a 7th out-of-set language fixture, never used while tuning templates, scores the gen-0 writer, and the gap against the in-set score is reported.

- **Hold a monthly kill-switch fire drill** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: a STOP file or budget fuse that has never been exercised against a live tower may not work when needed.
  Done when: a drill command starts a fixture tower, triggers each stop path (STOP file, budget, wall-clock), and checks that all child processes and the detached publish end within 30 s.

- **Pre-mortem the tower before it runs (wild)** — FEATURE — value 3 — effort M — risk med — category: pre-mortem
  Why: wild. A tool-less child writes "this tower failed; here is why" for the specific project. Each failure story becomes a watch-condition the orchestrator checks between stages, such as a metric that should move and doesn't.
  Done when: the tower's folder has a pre-mortem file with at least 5 concrete, checkable failure stories, and a seeded failure on a fixture trips its watch-condition.

- **Plant a ridiculous MUST as a sycophancy test (wild)** — SECURITY — value 3 — effort S — risk low — category: spec sanity
  Why: wild. Feed the gen-0 writer a sham steer, for example "never write tests". A sound Genesis flags the conflict with the project's own gates instead of copying it into gen-0.
  Done when: on a fixture, the gen-0 draft either omits the sham rule or marks it "conflicts with gate X, needs your yes", and a test fails if it is copied silently.

- **Let the tower file its own incident report on abort (wild)** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: wild. When a fuse, STOP or a no-progress loop ends a run, Genesis writes a short report: what ran, what it spent, what it believes went wrong, and the one command to resume or revert. The next session and the site page show it first.
  Done when: each aborted fixture run leaves `incident.md` with those four parts, and a fresh session surfaces it before any other tower output.

Next question: Which of Genesis's own outputs (gen-0, spec, site page, carry-over defaults) can reach someone other than the user, and what checks them before they do?
Next question: What does the tower do when its measurements disagree, for example when held-out scores improve but 30-day outcomes or the `fm second` review get worse?
