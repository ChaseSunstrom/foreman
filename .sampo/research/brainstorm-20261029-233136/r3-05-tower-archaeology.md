# Brainstorm — lens: tower archaeology

- **Pin a one-line "resume verdict" at the top of every tower** — FEATURE — value 5 — effort S — risk low — category: resume
  Why: assumption: a fresh session opening a tower three generations old spends its first turns guessing the state. The pack shows tower docs filed by shape and per-generation status, but no single "state / next step / blocked on" line.
  Done when: a tool-less reader given only the tower files names the current generation, the next step and the blocker, matching a key the author wrote.

- **Write a "why it lost" card for every rewrite that didn't win selection** — FEATURE — value 5 — effort M — risk low — category: lineage
  Why: the request says selection keeps a rewrite only if it closes more scenarios than its parent, and lineage.md is named. Nothing in the pack says the losing side is recorded with scenarios, margin and cost, so a resumer would retry it.
  Done when: every non-winning child has a card listing scenarios closed against the parent, cost and one reason, and `fm genesis status` links it.

- **Block a new Mission that repeats a dead one** — FEATURE — value 4 — effort M — risk low — category: lineage
  Why: the user's standing rule is that no idea is killed for ambition, with ≥2 different approaches before the ledger. A resumer without chat context cannot tell which approaches were already tried.
  Done when: a mission matching a ledger entry's approach is flagged with the old attempt's link, and passes only when it names how it differs.

- **Stamp each tower claim with the commit and exam run it was true at** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: the tower is storage outside the repo (never in the scratchpad), so it can describe code that has since moved. Recent commits show the tower and the code changing separately.
  Done when: `fm genesis status` marks claims whose cited files changed since the stamped commit as stale, and a fixture proves it.

- **Replay the tower from its journal with no model calls** — FEATURE — value 4 — effort M — risk med — category: integrity
  Why: assumption: tower files are written by many children and sessions, and nothing proves the recorded selection follows from the recorded scores.
  Done when: replaying selection from the stored exam scores reproduces every recorded winner, and a tampered score is reported by name.

- **Add `fm genesis diff gen-a gen-b` showing what changed in meaning** — FEATURE — value 4 — effort M — risk low — category: dev experience
  Why: the user wants an in-depth look at each generation (seed, missions, critiques, exam, decisions), and a resumer needs the delta more than the full text.
  Done when: the diff lists added or removed MUSTs and NEVERs, missions, scenarios closed and decisions between two generations, and stays empty for identical ones.

- **Record the user's steers verbatim inside the tower, ranked above every generated doc** — FIX — value 5 — effort S — risk low — category: charter
  Why: the pack shows steers such as "I don't mean to have foreman be hardcoded to that" and the standing run rules. A cold session reading only the tower can't see them unless they are copied in.
  Done when: the tower has a steers file with dated verbatim quotes, and a resume check fails if a generation's output contradicts one.

- **Make resuming a restate-then-compare handshake** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: assumption: a resumer that only reads files will confidently act on a stale picture.
  Done when: `fm genesis resume` has the session write its understanding, compares it field by field with the tower's verdict and prints the mismatches before any work starts.

- **Wild: Séance — ask a past generation a question and answer only from its files** — FEATURE — value 3 — effort M — risk low — category: lineage
  Why: wild. "Why does this rule exist" is the most common archaeology question, and a child limited to one generation's files shows where the record is silent.
  Done when: asking about a rule returns an answer with file citations, or the explicit line "not recorded", on a fixture tower.

- **Wild: Show the tower as dig strata on the site page, with fossils for dead rewrites** — FEATURE — value 3 — effort M — risk low — category: site UI
  Why: wild. The Genesis page exists and the user wants every generation readable in full. Layered strata with a marker for the "you are here" step would show the history at a glance.
  Done when: the exported page renders one layer per generation, each dead rewrite is clickable to its card, and it works with reduced motion.

- **Wild: Have each generation write three warnings to its successor when it closes** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: wild. Closing a generation is when its knowledge peaks, and the pack's blind-spots work shows unpredicted asks come from knowledge that was never written down.
  Done when: closing a generation fails without three warnings, and the next Seed cites or dismisses each one.

- **Reconcile the tower with the task queue every time it is opened** — FIX — value 4 — effort S — risk low — category: integrity
  Why: tasks are tracked as T-numbers, and the tower may name tasks that were closed, dropped or blocked without the tower noticing.
  Done when: opening a tower lists its referenced tasks whose status differs from the recorded one.

- **Flag contradictions between generations' decisions** — CLEAN — value 3 — effort M — risk med — category: integrity
  Why: assumption: gen-2 can quietly reverse a gen-1 decision with no note, leaving a resumer to pick between two true-looking files.
  Done when: a fixture with a planted reversal is flagged, naming both files, and a reversal with a stated reason passes.

Next question: What does a reader need that no file records because it only lived in the session that wrote it, and how could the tower prove nothing like that remains at close?
Next question: When two sessions resume the same tower, which wins, and where does the loser's work go?
