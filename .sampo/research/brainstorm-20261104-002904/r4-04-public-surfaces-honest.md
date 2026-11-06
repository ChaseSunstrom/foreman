# Brainstorm — lens: public surfaces honest

- **Render public text from a role table, fail the build on raw names** — FEATURE — value 5 — effort M — risk low — category: public vocabulary
  Why: the request says surfaces name models by role and the orchestrator as any agent; pushback "don't showcase it as jarvis… any orchestrator". Hand-typed names keep leaking. Existing ideas lint; this removes the source: captions, scene text, README, site and hook notes are templated from one `roles.toml` (planner, judge, decider, embedder, generator, orchestrator) with no free-typed model or host names.
  Done when: grep of rendered site, README and SVG text for a denylist (jarvis, qwen, claude, codex, hostnames, /home paths) returns zero, and adding a raw name to a template fails `fm doctor`.

- **Publish a claim ledger the site reads, with each public sentence tagged proven / unproven** — FEATURE — value 5 — effort L — risk med — category: honest docs
  Why: 421 docs flag claims no run has checked. Make the ledger the source: README and site sentences carry a claim id, rendered with a hatched "unproven" marker plus reason type (needs host, needs time, judgment). Unproven is visible, not hidden.
  Done when: every claim id on the landing resolves to a ledger row with run id and cited-file hash, or renders hatched; a test deletes a row and the page shows the hatch.

- **Show a "what this page cannot tell you" footer on each public page** — FEATURE — value 3 — effort S — risk low — category: honesty copy
  Why: the held-out exam is deferred to run-end, so public numbers are Haiku-smoke or free-arm. Each stat names its arm, sample size and what's not yet measured (production-model exam pending).
  Done when: every number on the landing links to arm and n; a stat without them fails the site test.

- **Make "works with any agent" a per-agent proven matrix on the site** — FEATURE — value 4 — effort M — risk low — category: claims
  Why: T-0335/0336/0337 are blocked, so codex, gemini and opencode support is unverified live, yet the headline says it works with them. Cells show proven (date, version), fixture-only, or unproven.
  Done when: the README header names no agent as supported unless its matrix cell is proven; blocked tasks show as hatched cells.

- **Add a blind leak reader to the ship gate** — SECURITY — value 4 — effort M — risk med — category: leak check
  Why: the scene mistake (jarvis, Claude) was found by the user, not a check. A tool-less child sees only the rendered pages (text extracted from SVG, alt, data JSON) and must answer "which machine, vendor, user?"; any non-"unknown" answer blocks.
  Done when: planting "jarvis" in a scene SVG makes the gate fail and naming the file; clean tree passes.

- **Extract text from SVGs, scenes, genesis data and alt attributes into one lintable corpus** — FIX — value 4 — effort S — risk low — category: lint coverage
  Why: source-only lints miss rendered text; the animated scene bug lived in drawn captions.
  Done when: the corpus file lists every visible string with origin; the leak lint runs on it and catches a planted name in `<text>`.

- **Compute every site and README number from the command that prints it** — FIX — value 4 — effort M — risk low — category: docs accuracy
  Why: 2358 files, counts and rates are typed by hand and go stale (the 599 and 421 counts themselves).
  Done when: numbers are placeholders filled at publish; changing a ledger changes the page; a hand-typed digit run in a templated block fails lint.

- **Verify CHANGELOG lines against commits and proofs** — FEATURE — value 3 — effort M — risk low — category: changelog
  Why: the CHANGELOG ships under the push grant with no check that each line matches a landed task's proof.
  Done when: a line without a task id and proof link prints "unproven" in the release notes.

- **Expire a proven claim when the files it cites change** — FEATURE — value 4 — effort M — risk low — category: staleness
  Why: proofs are point-in-time; docs are not. Stamp the cited-file hash; a changed hash flips the claim to stale.
  Done when: touching a cited file turns the claim hatched on the next publish.

- **Wild: Mystery orchestrator — every scene load rotates the orchestrator's name through generic roles and a random glyph** — FEATURE — value 3 — effort S — risk low — category: delight, neutrality
  Why: wild; makes the "any agent" rule visible and impossible to hard-code.
  Done when: two loads show different orchestrator labels, none naming a vendor.

- **Wild: Quine check — Sampo's spec regenerates a claims file that must match the real ledger** — FEATURE — value 3 — effort L — risk med — category: self-proof
  Why: wild; a cold child that reads only the public docs lists the claims it believes, and the diff against the ledger shows over-claims.
  Done when: the diff report lists claims the docs make that the ledger lacks.

- **Wild: "Show me" panel — click any claim to see the command, output and age of its proof** — FEATURE — value 4 — effort L — risk med — category: transparency UI
  Why: wild; turns the ledger into a visitor-facing replay with a "run it yourself" line.
  Done when: every proven claim opens a panel with the exact command, a captured output and a timestamp.

- **Scrub the published genesis data with a planted canary** — SECURITY — value 4 — effort S — risk low — category: publish safety
  Why: `fm genesis live` publishes data to main automatically under the standing rule; steers contain machine paths and endpoint names.
  Done when: a canary token placed in a steer never appears in the published JSON, and the publish step logs the scrub count.

Next question: which public sentences are only true for the user's own setup (local endpoints, one machine), and is there a way to detect "true here, unproven elsewhere" mechanically?
Next question: what does a first-time visitor conclude from a hatched "unproven" marker: honesty, or that the product is unfinished?
