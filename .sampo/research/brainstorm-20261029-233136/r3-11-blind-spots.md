# Brainstorm — lens: blind spots

Each miss below is the question a brainstorm should have asked, followed by the ideas that question surfaces now.

**Misses and the questions that catch them**
- T-2080/2087/2088/2090 (tower page, styling, auto-publish): *What public artifact does this feature emit, and who sees it?* The ideas below cover rendering safety, size, devices and head metadata.
- T-2073/2076: *Which published claims can silently go stale?* Hence the claims linter and the orphan-state check.
- T-2077/2079: *What does the user have to re-type to continue?* Hence the acceptance echo.

- **Sanitize the tower page's markdown and set a CSP** — SECURITY — value 4 — effort S — risk low — category: site security
  Why: the page renders every tower doc in full (the user's steer), and those docs are model output, possibly echoing repo text, and auto-published to a public site. Assumption: the renderer uses innerHTML-style injection.
  Done when: a tower doc containing `<script>` and `<img onerror>` renders as inert text, and a test fetches the page headers or meta and finds a CSP with no `unsafe-inline` script.

- **Lint numeric and named claims in docs against the code** — CLEAN — value 4 — effort M — risk low — category: doc truth
  Why: pages and README state counts like "6 languages, 11 scenario kinds", and surface lag was already a surprise ask (T-2073).
  Done when: `fm doctor` extracts those claims from README, MASTER.md and site/, compares them with the exam generator's registries, and fails on a seeded mismatch.

- **Flag state files no page or status view renders** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the user had to ask for "every doc readable in full, per-generation detail", so some storage had no view. Assumption: exam.jsonl, lineage and the not-yet ledger are among the unrendered pieces.
  Done when: adding a new file kind under the tower storage without a renderer fails `fm genesis export --check`.

- **Make the tower page work at 375px with keyboard navigation** — FEATURE — value 4 — effort M — risk low — category: devices, accessibility
  Why: devices are thin in the pack, and the tower graph is interactive. Assumption: it is only desktop-tested.
  Done when: a headless screenshot at 375px shows no horizontal scroll, and every node and doc is reachable by Tab and Enter with a visible focus ring.

- **Add full-text search and permalinks to the tower page** — FEATURE — value 4 — effort M — risk low — category: tower page
  Why: "every doc readable in full" implies lots of text. Without anchors and search, a reader cannot cite or find a MUST.
  Done when: typing a phrase highlights matches across all generations, and `#gen-2/missions` opens at that doc after reload.

- **Budget the exported page payload and lazy-load per-generation docs** — PERFORMANCE — value 3 — effort S — risk low — category: site performance
  Why: the export inlines whole towers, and the tower grows with every generation and every put.
  Done when: the initial page transfer stays under a set budget on a 10-generation fixture, and the test fails if it grows past it.

- **Generate a synthetic 3-generation tower for page development** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: iterating on the page (T-2080, 2087, 2090) needed a real tower and real publishes. A fixture also lets the empty, loading and error states be tested.
  Done when: `fm genesis demo` writes a fake tower to a temp dir with a lost rewrite and a not-yet entry, and the export renders from it with no network.

- **Lint head metadata on every site page** — CLEAN — value 3 — effort S — risk low — category: brand consistency
  Why: the favicon was still the old logo after the redesign, and the genesis page needed a later pass to match the shared chrome. Chrome lint exists in the pack, but favicon, title, og:image and canonical are not covered.
  Done when: a page with a stale favicon href or a missing og:image fails the site lint.

- **Echo each ask as a testable acceptance list before building** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: asks like "keep the site live on its own" and "matches the site" each hid sub-requirements (debounce, standing grant, shared tokens) that were asked for in separate turns.
  Done when: for a steer, the task opens with a numbered list of checks, each mapped to a command or test, and closing the task requires each to pass or be struck out with a reason.

- **Wild: Publish a surprise-rate curve** — FEATURE — value 3 — effort M — risk low — category: self-measurement
  Why: wild. Each ask no idea predicted is counted against the asks that arrived in that period, giving a per-week miss rate on the site, so the blind-spots lens has a visible number to push down.
  Done when: the page plots the rate for at least 4 weeks from the existing missed-ask records.

- **Wild: Render a social card per generation** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Sharing the tower page is a likely next step. Each generation gets an SVG card (seed line, scenarios closed, held-out score) used as og:image.
  Done when: the generation permalink serves an og:image whose text matches that generation's status line.

- **Wild: Live README badge from the latest exam result** — FEATURE — value 3 — effort S — risk low — category: delight, trust
  Why: wild. README already carries a test badge. A static badge file regenerated by the auto-publish step would say "gen 2 · 14/18 closed · held-out 3/3".
  Done when: after `fm exam` writes results, the badge file updates in the same publish, and a stale badge fails the claims linter.

- **Keep a "built but never run" ledger for new verbs** — CLEAN — value 3 — effort M — risk low — category: usage evidence
  Why: assumption: some of the many fm genesis subcommands were shipped without any real session using them. `live` was added after `publish` existed.
  Done when: `fm genesis status` lists each subcommand with its last real invocation date, and one with none for 30 days is flagged.

Next question: Which of the user's recent asks were really "make this surface match that one", and which other surface pairs (site vs. CLI help, README vs. skills, demo vs. TUI) have no check tying them together?
Next question: When the tower page is public, what does a first-time visitor with no Foreman context need to understand in 30 seconds, and has anyone tested that?
