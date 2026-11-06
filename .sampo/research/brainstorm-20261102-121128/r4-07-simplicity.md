# Brainstorm — lens: simplicity

- **Run a prose-only arm in the duel** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: assumption: nothing in the pack shows how much of the gain comes from code rather than from the rules text. The guard-only arm and ablations remove pieces, but none of them replaces the code with a one-page prompt of the same rules.
  Done when: `fm bench duel --agent prose` runs on the same scenarios, and `fm doctor` shows its pass-rate gap to the full foreman arm per kind.

- **Cap the vocabulary with a glossary lint** — CLEAN — value 4 — effort S — risk low — category: legibility
  Why: the pack uses Mission, Seed, tower, steer, bet, lesson, card, round, brief, ask and inbox item. A newcomer meets all of them. Assumption: some are synonyms.
  Done when: a lint fails when a coined term in README, MASTER.md, or a verb's help text has no glossary entry, and the glossary lists each term once with one sentence.

- **Find modules no session path reaches** — CLEAN — value 4 — effort M — risk low — category: dead code
  Why: the standing rule says every capability must be called by a real session path, and `fm genesis check` only names verbs. The map counts 131 lib files. Assumption: an import-graph walk from `bin/fm` and the hooks would find modules only tests import.
  Done when: `fm check --reach` lists lib modules unreachable from `bin/fm` and the hook entries, and the first run's output becomes deletion tasks or reasoned exceptions.

- **Allow one check per task** — FEATURE — value 4 — effort S — risk med — category: task model
  Why: the lines "T-2583's criterion says 8+ characters but its own example '4% lost' has 7" and "a criterion whose runs matched no test" show multi-part criteria drifting. Assumption: a single DONE-WHEN command is easier to verify and to prove.
  Done when: `fm task new` refuses a DONE-WHEN with more than one verify command and offers to split it into linked tasks.

- **Classify every state file as source or derived, then rebuild derived ones nightly** — CLEAN — value 4 — effort M — risk med — category: state
  Why: the pack shows many ledgers (bets, outcomes, lessons, steers, exam runs), and the earlier question is "which reader would answer wrong if a record class were missing". Assumption: some files are caches kept like records.
  Done when: a manifest tags each file under the Foreman state directory, a nightly job deletes the derived ones in a scratch copy, and a byte-compare shows they rebuild identically.

- **Print one next command on every nonzero exit** — FEATURE — value 3 — effort S — risk low — category: errors
  Why: the dropped `fm night --print-timer` flag ("removed on purpose in T-2475") and the refusals from `fm exam long run`, `fm genesis put` and the finish gate all leave the user to work out the fix. Assumption: refusals vary in how much guidance they give.
  Done when: a test calls every refusing verb with bad input and asserts the last stderr line is a runnable `fm …` command or `fix: <path>`.

- **Ratchet function length and nesting, starting with `register.tsx`** — CLEAN — value 3 — effort M — risk low — category: code size
  Why: T-0166 is deferred because `register.tsx` holds stateful helpers. The lean ratchet counts lines per module but not the longest function or the deepest nesting.
  Done when: `fm doctor` records the longest function per file, `fm ship` fails when a function grows past its recorded length, and `register.tsx` drops below an agreed length.

- **Table-drive near-duplicate tests** — CLEAN — value 3 — effort M — risk low — category: tests
  Why: the map counts 404 test files, and the commits show many one-clause tests such as "pinned by test_serve and test_gate_friction". Assumption: many tests share a setup and differ only in an input.
  Done when: a finder reports test files whose bodies differ only in literals, and merging one cluster keeps the suite green with fewer lines.

- **Set a reading budget per doc** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the README opens with a 960px demo and eight anchors, and MASTER.md holds clauses for all 131 modules. Assumption: nobody has set a ceiling for either.
  Done when: a ratchet records the words in the README before its first heading break and in each MASTER.md clause, and `fm ship` fails when either grows without a named cut.

- **Wild: Probe legibility with a cold reader** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: wild. A tool-less Haiku child reads one lib module and writes three sentences on what it does and who calls it. A wrong or vague answer marks the module as hard to follow, which is evidence for a rename or split.
  Done when: `fm check --legible` grades each module, and the lowest five become CLEAN tasks.

- **Wild: Keep a one-page napkin contract** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: wild. A 12-line "what Foreman is" the user signs. A feature whose clause doesn't trace to a napkin line is a candidate for removal, and any change to the napkin shows as a diff the user reviews.
  Done when: `fm napkin` prints the 12 lines, `fm ship` flags new MASTER.md clauses that cite no napkin line, and the user's sign-off is stored with the commit.

- **Wild: Hold a weekly one-key "Delete Tuesday"** — FEATURE — value 4 — effort M — risk med — category: subtraction
  Why: wild. Once a week a cold agent proposes the one deletion with the most lines removed and the least measured effect, runs the full suite on it, and shows the user a single accept key. This goes beyond the pack's ablation-to-removal item by fixing a cadence and one-key acceptance.
  Done when: after the weekly run, `fm next` shows one removal card with its lines saved and suite result, and accepting lands it through `fm ship`.

- **Wild: Fold the Genesis files into one readable page** — CLEAN — value 3 — effort M — risk low — category: legibility
  Why: wild. The tower has spec.md, coverage.md, lineage.md, not-yet.md, frame.md, missions and seeds, plus site/genesis data. Assumption: nobody can hold that in their head. A generated single page says where the run is, what blocks it, and what the user must decide.
  Done when: `fm genesis page` prints under 60 lines covering generation, red sweeps, blocked items and pending decisions, and it is the first thing `fm doctor` links to.

Next question: Which Foreman feature would the user not notice missing for a month, and what test could show that without asking them?
Next question: What does a first-time reader of the README still not know after five minutes, and which of the 131 modules does that gap point at?
