# Brainstorm — lens: blind spots

Each idea below comes from one class of ask the user had to make themselves. The question that would have caught it is in the Why line.

- **Treat a repeated ask as a failed close** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the favicon "still" shows the old logo, the fm code section is stale again, and the Genesis page had to be made to "match the site". Question: "Which asks are second asks?"
  Done when: two near-duplicate asks 14 days apart on a fixture make Foreman write a root-cause note naming the surface that was missing from the drift list, and add it.

- **Render a contact sheet of every site page in a headless browser as a gate** — FEATURE — value 4 — effort M — risk low — category: site QA
  Why: favicon, shared header and footer, and stale fm code screenshots were all visible at a glance and invisible to the linters. Question: "What can only be seen by eye?"
  Done when: changing the icon on one fixture page fails the gate, with an image showing each page's tab icon, header and footer at 1280px and 375px.

- **Track every clause of an attached document until it maps to a task or exam scenario** — FEATURE — value 4 — effort M — risk med — category: traceability
  Why: SEED_PROMPT.md was attached and the user then asked for "Missions 2-8, critiques, lineage, sweep" one step at a time. Question: "Which sentences of what they gave us have no owner?"
  Done when: a fixture attachment with 12 clauses shows 12 rows in `fm genesis status`, and an unmapped row turns red.

- **Hash and watch external source documents** — SECURITY — value 3 — effort S — risk low — category: provenance
  Why: gen-0 rests on an absolute path outside the repo (`~/.claude/foreman/SEED_PROMPT.md`). If that file changes, the tower silently drifts. Question: "What does the tower depend on that it doesn't own?"
  Done when: editing the source file makes the next `fm genesis status` report "source changed since gen-0" with a diff.

- **Run the test suite with perturbed volatile inputs** — FIX — value 3 — effort S — risk low — category: test hygiene
  Why: test_ship failed because a commit hash ended in "add". Question: "Which tests depend on values that vary between runs?"
  Done when: a mode that randomises hashes, dates, ids and temp paths runs the suite twice, and an injected hash-dependent test fails in one of the two runs.

- **Run `fm ship` and genesis publish across a matrix of git topologies** — FIX — value 4 — effort M — risk low — category: ship reliability
  Why: fm ship needed a patch for merged builder lanes, and auto-publish now pushes on every tower change. Question: "Which repository shapes haven't we tried?"
  Done when: fixtures covering merge commits, squash, rebased lanes, detached HEAD, dirty tree and shallow clone all pass for both verbs, or refuse with a one-line reason.

- **Log zero-hit library lookups as shelf demand** — FEATURE — value 3 — effort S — risk low — category: catalogs
  Why: the user keeps asking to grow shelves (24 web cards, eight more looks, many more playbooks and skills). Question: "Where did a lookup come back empty?"
  Done when: `fm lib show` on a missing name appends to a demand log, and `fm lib gaps` lists the top misses by count.

- **Probe for hardcoding with a novel member** — CLEAN — value 4 — effort M — risk low — category: generality
  Why: the user said "I want foreman to just genuinely be smarter". The exam has fixed lists (6 languages, 11 scenario kinds). Question: "What happens when a list grows by one?"
  Done when: adding a fake scenario kind and a fake language through config only is accepted by `fm exam gen` and `fm genesis`, with no code edit.

- **Eval whether the entry phrases actually route to Genesis** — FEATURE — value 4 — effort S — risk low — category: routing
  Why: the feature must start from "make this great", a sweeping request or nothing, within the skill-listing budget. Question: "Does the user's phrasing reach the verb?"
  Done when: a tool-less child, given 30 phrasings, picks the Genesis skill for at least the agreed share of true cases and for none of the 10 decoys.

- **Publish only on top of green CI** — SECURITY — value 3 — effort S — risk low — category: publish safety
  Why: a standing grant pushes to main on every tower change, and the repo carries a test badge. Question: "What's the worst thing a silent push can sit on?"
  Done when: with the last workflow run red or pending, the publish is held and a retry is queued, and `status` shows "publish held: CI".

- **Add a Genesis tab to the web UI with a single inbox** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the only surface listed is the web UI, yet the tower page is a separate public export. Questions the tower raises and approvals it needs are scattered. Question: "Where does the user answer it?"
  Done when: the tower's pending questions, auto-start proposals and held publishes all appear in one list in `plugin/templates/web`, and answering one unblocks the state machine.

- **Build a nouns-by-surfaces matrix and fill the empty cells** — FEATURE — value 3 — effort M — risk low — category: visibility
  Why: the user asked for every doc "readable in full on the page" with per-generation detail. Question: "Which stored thing is invisible on which surface?"
  Done when: the matrix of exam.jsonl, lineage, not-yet, steers and critiques against CLI, web UI, site and statusline is generated, and each blank cell is queued.

- **Show fog of war on the tower page** — FEATURE — value 3 — effort M — risk low — category: tower page — wild
  Why: assumption: the user wants to see what Genesis has not examined as clearly as what it has. Question: "What are we blind to, drawn?"
  Done when: the page shades grid cells and repo areas with no exam coverage, and clicking a cell shows why it is dark.

- **Quiz a stranger on each public page** — FEATURE — value 3 — effort S — risk low — category: legibility — wild
  Why: the user kept fixing what a first-time reader sees (logo, section freshness, chrome). Question: "Could a stranger answer five basic questions from this page alone?"
  Done when: a tool-less child with only the page text answers five fixed questions, and a failed answer is filed as a task before publish.

- **Enforce the user's own vocabulary with a glossary** — CLEAN — value 2 — effort S — risk low — category: consistency — wild
  Why: the user's terms (tower, gen, held-out, Seed, Mission) drive their asks, and the pack uses "tower" and "tower page" loosely. Question: "Does every surface use the user's words the way they do?"
  Done when: `fm glossary` is built from steers and the docs, and the lint flags a page that uses a synonym where a glossary term exists.

Next question: Which of the user's repeated manual follow-ups (re-ship, re-record, re-match the site) have no trigger at all, and what would a hook-level "after X, always Y" register look like?
Next question: When the user attaches an outside document, who owns keeping it in sync with the tower?
