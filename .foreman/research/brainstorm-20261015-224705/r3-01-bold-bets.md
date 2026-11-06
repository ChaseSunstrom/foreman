# Brainstorm — lens: bold bets

- **Ratchet any number overnight** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: assumption: the user's repos have a number worth lowering or raising (bench_hooks p99, gate time, bundle size). The pack has gate-speed and pane-cost work, but every optimisation is a hand-run task and nothing hill-climbs for you.
  Done when: `fm ratchet --metric "<cmd>" --budget 5` runs in a lane, commits only attempts that improve the metric, reverts the rest, and ends with a receipt where the kept commits form a monotone curve and every reverted attempt is logged.

- **Rehearse risky commands in a throwaway overlay** — SECURITY — value 4 — effort M — risk med — category: provable safety
  Why: T-0275 (guard reads what scripts run) is still deferred, and text rules can be obfuscated around. Run gray-zone commands (`rm -rf "$X/"`, `curl|sh`, script files) in a no-network bwrap or overlay copy, then judge the observed file effects instead of the command text.
  Done when: `rm -rf "$UNSET/"` is blocked with "would delete N files outside the repo", and a benign script passes the rehearsal and then runs for real.

- **Record the failing run, then query it** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: assumption: FIX tasks still locate the cause by reading and guessing. A Python `sys.monitoring` recorder writing to SQLite gives the agent a deterministic "who last wrote this value" tool.
  Done when: `fm trace record -- pytest tests/x` then `fm trace why <var> --at <file:line>` prints the assignment chain to a seeded bug in under 5 s, and the FIX plan cites it.

- **Diff the upstream source on every dependency bump** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: the planned install check covers age, typosquats and the registry only. Compare the previous and new sdist or tarball for new install scripts, network calls, obfuscation and maintainer change.
  Done when: bumping a fixture package whose new version adds a `postinstall` curl is flagged with the added lines before the lockfile change is accepted.

- **Send explorers through the user's app** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: Foreman's own surface is a web UI and the pack already has screenshots and the UI harness. Persona agents crawl the UI and fuzz the API from its schema. Each finding (console error, dead link, a11y violation) becomes a minimal Playwright regression test.
  Done when: `fm explore` on a fixture app with a planted dead link and a console error emits two failing generated tests that go green once the app is fixed.

- **Search patches as a tree, scored by failure distance** — FEATURE — value 4 — effort L — risk med — category: search
  Why: wild. Hard FIX tasks get one linear attempt. Run beam search over lanes (width 3, depth 3, hard spend cap), scoring each node by failing-test count and error shift, and keep the best leaf.
  Done when: `fm search` writes a tree file with a score per node, and the chosen leaf has the minimum failing count and lands in the main lane.

- **Be a language server for the human's editor** — FEATURE — value 4 — effort M — risk low — category: surfaces
  Why: wild. Foreman's state only reaches the pane and chat. A small stdio LSP server shows ledger facts as editor diagnostics and hovers: "lane T-1040 is editing this function", a failing criterion, a known fix for this error.
  Done when: opening a file claimed by a live lane in any LSP editor shows a diagnostic naming the lane, and a hover shows the matching known fix.

- **Rebuild a module blind to measure accidental complexity** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: wild. A builder in a lane sees only a module's tests and public signatures and re-implements it. A much smaller rebuild that also passes is evidence the original is bloated, and becomes a deletion proposal.
  Done when: `fm rebuild <module>` reports LOC and test-pass ratio against the original, and when the rebuild is under 60% of the size and green, it files a simplify task with the diff attached.

- **Open the ledger as SQL, with watch queries** — FEATURE — value 3 — effort S — risk low — category: self-measurement
  Why: the scoreboard, interventions per task and minutes lost each re-scan the ledger by hand. SQLite views over ledger, corrections, fixes and hook timings give one substrate, and saved queries with thresholds replace ad-hoc reports.
  Done when: `fm sql "select task,count(*) from corrections group by 1"` returns rows, and a saved watch that crosses its threshold adds a line to `fm digest`.

- **Mine architecture boundaries from the import graph** — FEATURE — value 3 — effort M — risk med — category: conventions
  Why: T-1036/T-1037 already build an import index. Layer pairs that have never imported each other become enforced boundaries, so an edit that breaks the layering gets a warning with the precedent.
  Done when: an edit adding the first-ever import across a mined boundary prints a warning citing the layer pair, with under 5% false positives replayed over the last 100 commits.

- **Trial a dependency in a lane before adopting it** — FEATURE — value 3 — effort M — risk low — category: dependencies
  Why: the install check reads metadata only. Install in a throwaway lane, run the project's tests and type check, measure import time and size, and bisect versions across lanes when a bump turns a gate red.
  Done when: `fm trial <pkg>` prints a verdict with test, size and import-time deltas, and `fm bisect dep` names the first breaking release in at most log2(n) lanes.

- **Export the user's rulings as a training set for a local judge** — FEATURE — value 3 — effort M — risk med — category: local-first
  Why: wild. Steers, intake folds, guard overrides and accept/reject labels already exist in the ledger. A scrubbed JSONL export plus an eval harness lets a local small model take over intake and gray-zone judgments, with agreement measured against the user's own history.
  Done when: `fm dataset export` writes secret-free JSONL, and `fm dataset eval --model <local>` prints agreement against the recorded labels.

- **Find twin code across the user's own repos** — FEATURE — value 3 — effort M — risk low — category: cross-repo
  Why: wild. The pack says "any project", and nothing looks across projects for duplicated functions. A minhash scan of local repos turns copied code into extract-to-shared-package proposals.
  Done when: with two fixture repos sharing a 30-line function, `fm twins` lists the pair with a similarity score and drafts an extraction task.
