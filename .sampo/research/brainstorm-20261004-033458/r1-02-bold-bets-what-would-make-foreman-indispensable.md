# Brainstorm — lens: bold bets: what would make Foreman indispensable

- **Compile a project "constitution" from history** — FEATURE — value 5 — effort M — risk med — category: memory
  Why: the user's steers ("never X", corrections, drops, widened criteria) are scattered across ledger, lessons and vetoes. Assumption: nobody has merged them into one reviewable, versioned document.
  Done when: `fm constitution` prints rules each cited to the originating ledger entry, and a test shows a new "never X" correction appears as a rule with its citation and is enforced by the veto check.

- **Run the review in the background of the next task** — PERFORMANCE — value 5 — effort M — risk med — category: latency
  Why: friction says each batch idles 1–2 min and 31+ drive stops waited on a reviewer. Parking is proposed, but the real gain is useful work: the drive starts the next independent brief in a separate lane while the reviewer reads the last one, and only merges findings back as new steps.
  Done when: with two independent queued briefs, a test shows brief B's first edit occurring before brief A's review returns, and A's findings still block A's close.

- **Add a harness-neutral verdict kernel** — FEATURE — value 5 — effort L — risk med — category: portability
  Why: the user wants better compatibility and "the best plugin possible". Assumption: the gate/evidence/ledger core can be separated from the Claude Code hook layer. A small `fm verify --event` JSON contract plus a read-only MCP surface would let any harness ask "is this done?".
  Done when: a non-Claude shim script sends a done-claim JSON and gets the same verdict as the hook path, checked by a suite test.

- **Mine other people's skills for patterns, then offer adoption** — FEATURE — value 4 — effort M — risk med — category: research
  Why: the user asked to "research other great plugins/things people want and add them". `fm landscape` only diffs wants. Add `fm landscape adopt`: reads installed or public skill manifests, extracts capabilities Foreman lacks, and drafts a brief per candidate with a cost, risk and overlap note.
  Done when: running it against two fixture skill dirs yields briefs naming the missing capability and the Foreman verb it would overlap.

- **Give the user a one-screen "state of the project" brief** — FEATURE — value 4 — effort M — risk low — category: orientation
  Why: users returning to long drives have open tasks, escapes, spend and surprises across separate verbs. Assumption: the return-card idea exists but not as a project-health synthesis with a ranked "what to do next".
  Done when: `fm status --project` outputs at most 25 lines covering open work, top risk by escape history, spend vs. caps and the single recommended next ask, from fixtures.

- **Auto-minimize every failure into a bench case** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: reviews find 3–8 real issues per batch and escapes are logged, yet each stays prose. Turning each confirmed finding or escape into a fail-to-pass case in `fm bench` makes every mistake permanently self-testing.
  Done when: closing a finding that has a repro creates a bench case that fails on the pre-fix commit and passes on the fix.

- **Wild: Let Foreman negotiate scope with the user's wallet** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: the user wants no capability loss, only prevention of runaway spend. Wild: at brief time, Foreman proposes three plans with token, time and confidence estimates (cheap/standard/thorough) calibrated from history, and the user picks with one key.
  Done when: `fm task new` prints three costed options and the chosen one sets the brief's review depth and child caps.

- **Wild: Build a "Foreman for Foreman" shadow fork that applies passes on a branch and auto-benches them** — FEATURE — value 5 — effort L — risk high — category: self-improvement
  Why: the user asked for recursive self-improvement across multiple passes. Assumption: `fm evolve` only mutates instruction files. A fork lane could apply a pass's code changes, run `fm bench versions` against the prior build, and present a keep/revert verdict with numbers.
  Done when: a pass run in a lane produces a bench comparison report, and a regression forces an automatic revert recommendation.

- **Wild: Offer "Foreman radio" ambient narration for long drives** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: long unattended drives leave the user guessing. Wild: a single rolling pane line in plain words ("fixing parser edge, 2 of 5 criteria green, reviewer parked") that updates from ledger events, with no model calls.
  Done when: the UI view model emits the sentence from fixture events and a UI test checks it changes on a criterion going green.

- **Wild: Turn the research store into a queryable "what we know" wiki that agents consult before searching** — FEATURE — value 4 — effort M — risk med — category: research
  Why: the user wants better research and finding information. Cached pages, claims and quote checks exist, but answers are not reused. A pre-search step checks stored claims (with age and single-source marks) so repeat questions cost zero fetches.
  Done when: asking a question already answered within its half-life returns the stored claim with citations and makes no network call, verified with a fake fetcher.

- **Add a pre-flight "will this brief actually finish?" simulation** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: failures are often visible in the brief itself (unrunnable verify commands, missing files, over-wide steps). A cheap static pass using the map and impact data scores feasibility before any edits.
  Done when: a brief with a nonexistent verify target is flagged with the reason before the first edit, from a test fixture.
