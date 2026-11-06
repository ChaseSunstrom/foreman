# Brainstorm — lens: public surfaces honest

- **Gate public text through a role vocabulary lint at ship** — FEATURE — value 5 — effort M — risk low — category: honesty gate
  Why: the request says public surfaces must name models by role and the orchestrator as any agent; the user pushed back on "jarvis" and on naming Claude as orchestrator. Many past ideas propose a lint, but none ties it to `fm ship` as a blocking step with an allowlist of explicit role words (planner, judge, router, embedder, generator, orchestrator).
  Done when: a planted "jarvis", a hostname and "Claude plans" in site/, README.md and demo SVG text each make the ship gate fail, naming file:line and the role word to use.

- **Render scene captions from a role table, not hand-typed text** — CLEAN — value 4 — effort M — risk low — category: single source
  Why: the model-kind animation (T-2888) was hand-written with names the user then corrected; assumption: captions are typed directly into SVG/HTML.
  Done when: swapping the orchestrator parameter in one role-table file regenerates the README and site scenes, and grepping built output finds no vendor or endpoint names.

- **Extract text from SVGs, rendered scenes and alt attributes into the lint corpus** — SECURITY — value 4 — effort S — risk low — category: leak coverage
  Why: logo/README header/demo are SVGs (`demo/live.svg`, `design/sampo/logo`); a text-only grep misses `<text>`, `<title>`, `aria-label` and alt.
  Done when: a planted forbidden name inside an SVG `<title>` is caught by the same lint run.

- **Scrub genesis/site data at publish with a planted canary** — SECURITY — value 4 — effort S — risk low — category: publish gate
  Why: `fm genesis live` publishes steers and tower data to main on every change; the steers contain "jarvis", local endpoints and the user's words verbatim.
  Done when: a canary string seeded in a steer never appears in published site/genesis data, and the publish aborts naming it if it does.

- **Turn spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort L — risk med — category: meaning proof
  Why: the request names meaning as the largest unproven class (599); examples in specs ("With this, you can") are the cheapest oracle.
  Done when: a plan whose spec holds three `$ cmd` → output examples files three criteria, each run in a scratch home, and one deliberately wrong example shows red.

- **Stamp each doc claim with the run and cited-file hash that last checked it** — FEATURE — value 5 — effort L — risk med — category: claim ledger
  Why: 421 docs flag claims no run has checked; hashes make staleness mechanical.
  Done when: editing a cited file flips its claims to "unproven since <hash>" in the claims table and the docs render them hatched.

- **Compute every number on the site and README from the command that prints it** — CLEAN — value 4 — effort M — risk low — category: no typed numbers
  Why: README/site stats (2358 files, 1396 skills, test counts) go stale; the landing already wires "real stats".
  Done when: a lint finds zero digit-run claims in public text that lack a data-path binding, or a `<!-- unproven -->` mark.

- **Show a per-agent "works with" matrix with proven/unproven cells** — FEATURE — value 4 — effort M — risk low — category: any-agent honesty
  Why: the README says it works with Codex, Gemini, opencode, but T-0335/6/7 are blocked and unverified; the claim outruns the proof.
  Done when: the site's agent table shows a cell per agent × capability, with unproven ones hatched and linked to the blocking task.

- **Require a proof link or "unproven" on every CHANGELOG line** — FEATURE — value 3 — effort S — risk low — category: changelog honesty
  Why: the user asked to ship the CHANGELOG alongside commits; entries are currently unverified prose.
  Done when: a CHANGELOG line with neither a task-proof reference nor an `unproven` tag fails `fm check`.

- **Publish a retraction log of corrected public claims** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: pushbacks (jarvis naming, orchestrator naming) were fixed silently; a visible log makes honesty cheap to audit.
  Done when: a site page lists each corrected claim with date, old wording class and fix commit, generated from a data file.

- **Wild: Have a cold child guess the orchestrator and local endpoint from the rendered site** — FEATURE — value 4 — effort S — risk low — category: blind leak reader (wild)
  Why: lints catch known strings; a naive reader catches inferable ones (screenshots, fonts, paths).
  Done when: a tool-less child given only the rendered pages answers "unknown" to which vendor, machine and model names are used, in 3 of 3 runs.

- **Wild: Make the orchestrator in every scene a rotating parameter** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: the user wants "any orchestrator"; a scene that cycles agent glyphs shows it instead of claiming it.
  Done when: the hero scene cycles through at least four generic agent badges on a timer, honouring reduced motion.

- **Wild: Open any claim to a replayable "show me" panel** — FEATURE — value 4 — effort L — risk med — category: proof UX (wild)
  Why: proven claims should be checkable by readers without trust; assumption: the claims table stores a command and captured output.
  Done when: clicking a README/site claim shows the command, its dated output and the file hash, or the word "unproven".

- **Wild: Age proof stamps by commits touching the cited files** — FEATURE — value 3 — effort M — risk low — category: decay (wild)
  Why: a stamp's trust should fade with change; flat "verified" ages badly.
  Done when: a claim's badge shifts from solid to hatched after N commits to its cited files without a re-run.

Next question: Which public claims does a first-time reader act on (install line, "works with X") and have those been run on a clean machine this week?
Next question: Is there any public surface outside site/, README and demo (package metadata, marketplace listing, release notes, issue templates) that the vocabulary lint never reads?
