# Brainstorm — lens: capability map

- **Keep a living capability matrix of best-in-class tools** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: a one-time survey goes stale on a multi-day goal, and the "ideas so far" list has no feature-by-tool artifact. It has parity tables only at finish. The matrix has features as rows and Linear, Taskmaster, Spec Kit, Kiro and Devin-style planners as columns, each cell cited. It is re-surveyed at the midpoint and the diff files new rows.
  Done when: `fm goal matrix` lists at least 3 tools with a cited source per cell, and a re-survey on a fixture with one planted new feature adds exactly that row.

- **Import standards clauses as rows** — FEATURE — value 4 — effort M — risk low — category: completeness
  Why: assumption: many goals sit in a domain with a spec (WCAG, OpenAPI, RFC, XDG). Nothing in the pack turns external normative text into rows, and each clause needs its own conformance probe.
  Done when: a goal naming a standard gets one row per MUST clause, each with a probe, and an unprobed clause blocks "done".

- **Differential-test against a reference tool** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: a finish oracle written by the builder shares the builder's blind spots. Running the same inputs through an installed best-in-class tool is a signal Foreman didn't author, which fits the standing weakness-finding rule.
  Done when: a fixture goal runs 10 inputs through both tools and reports the divergences as candidate rows.

- **Decide build, adopt or skip for every row** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: `fm lib` and `fm scout` exist, but no plan row records whether a library already covers it. Each row would carry candidates, a licence and a verdict.
  Done when: no row enters the plan without a build/adopt/skip verdict, and an adopt row names a package that `fm lib show` resolves.

- **Add rubric rows for subjective quality** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: look and feel, tone and docs clarity have no probe, so they are either skipped or self-declared done. A row carries a scored rubric, with screenshots or text judged cold by a different model and kept as an artifact.
  Done when: a rubric row can't close without a score file from a non-builder model, and a planted bad screenshot fails it.

- **Add a distribution and day-2 template** — FEATURE — value 4 — effort S — risk low — category: completeness
  Why: the pack covers a clean-clone build and an uninstall rehearsal, but not install, upgrade-from-previous, versioning, release notes or support path as a standard set of rows. Foreman is itself a product with `install.sh` and a marketplace.
  Done when: planning a shippable goal emits the 6 rows, and an upgrade-from-N-1 probe runs against a fixture.

- **Catalogue the failure experience** — FEATURE — value 3 — effort M — risk low — category: completeness
  Why: plans list happy-path capabilities. Empty, loading, error and offline states, plus the error-message wording, the troubleshooting page and the bug-report path, are what a best-in-class product also has.
  Done when: each user-facing surface in the plan has a row per state, and a surface missing its error state is flagged.

- **Hoist rows shared between live goals** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: "arbitrate between two live goals" resolves a clash but doesn't find common prerequisites such as auth, config or CI. Duplicate rows in separate goals mean the work is done twice.
  Done when: two fixture goals with a common prerequisite show one shared row, and closing it marks both.

- **Add import and export rows for rival formats** — FEATURE — value 3 — effort M — risk low — category: completeness
  Why: the pack mentions Spec Kit and Kiro plan export, but a finished product usually also reads and writes the formats its competitors use. Each format becomes a row with a round-trip probe.
  Done when: a goal naming a rival yields a migrate-in and migrate-out row, and the round-trip probe passes on a sample file.

- **Ship seed data and a demo path as rows** — FEATURE — value 3 — effort S — risk low — category: demo
  Why: "finished" is unprovable to a stranger without sample content. A row requires fixtures to exist and a scripted demo to run clean from a fresh clone.
  Done when: `fm goal demo` replays the scripted path in a temp directory and exits 0.

- **Order rows by the sequence reference projects shipped them** — FEATURE — value 3 — effort M — risk med — category: ordering — wild
  Why: assumption: an open-source tool's git history shows which capabilities came first and which were added late. That is an empirical ordering prior for the plan, beyond critical path alone.
  Done when: for 2 reference repos the plan's row order correlates with first-introduction commit order at a stated threshold, or the plan states why not.

- **Have a child write the one-star review of the finished build** — FEATURE — value 3 — effort S — risk low — category: completeness — wild
  Why: a tool-less child reads only the finish diff and the cells and writes the angriest honest review. Each complaint becomes a candidate row, and a complaint that echoes a cut row confirms the cut was costly.
  Done when: the finish card lists at least 3 complaints, each traced to a row or tagged "new".

- **Weight rows by public demand evidence** — FEATURE — value 3 — effort M — risk med — category: ranking — wild
  Why: assumption: issue thumbs-up counts, stars and docs page weight on reference tools show which capabilities users actually use. That could set must/should/could tiers on evidence, not guesswork.
  Done when: each row's tier shows a demand citation or "no evidence", and the user can see the ranking input.

- **Require a deliberate-omissions list from the survey** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: the matrix will show features the finished version won't have. Each one needs a one-line reason, or the omission looks like a gap at finish.
  Done when: every matrix feature with no row has a written reason, and the finish card prints the list.

- **Ship the goal's matrix as a shareable one-page HTML** — FEATURE — value 2 — effort S — risk low — category: ui — wild
  Why: a static page of features by tool by status, with rows filling in as they close, is something the user can show a teammate without Foreman installed.
  Done when: `fm goal matrix --html` writes one self-contained file that opens offline and matches the live matrix.

Next question: Which of these capability sources, such as standards, rival formats and reference-repo history, can a stock install actually reach offline, and which silently depend on network access the privacy rules forbid?
Next question: For a goal whose best-in-class bar moves weekly, what is the rule for when the plan is allowed to grow, versus when a new capability goes to a successor goal?
