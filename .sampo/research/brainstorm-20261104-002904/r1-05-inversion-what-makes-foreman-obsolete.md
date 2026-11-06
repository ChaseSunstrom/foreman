# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Compile spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the pack's top gap is meaning, with 599 unproven items, and the request names "spec example assertions should become runnable criteria". Obsolescence angle: a plain agent can run tests, but nothing in the host turns a spec's own "X gives Y" lines into checks before the edit.
  Done when: `fm plan` on a spec containing three "input → output" examples writes three criteria into the Done-when, each one a command that runs, and a deliberately wrong implementation fails all three.

- **Mutate every compiled criterion to prove it can fail** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: assumption: a criterion extracted from prose is often vacuous (it matches anything). Flip its expected value and rerun; if it still passes, label it `vacuous` and refuse to count it as proof.
  Done when: a planted criterion with an always-true assertion is reported `vacuous`, while a real one is not.

- **Stamp each docs claim with the cited-file hash it was last run against** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: 421 docs flag claims no run has checked. A claim carrying `ran@<hash of the files it cites>` goes stale on change, which a host cannot do for prose.
  Done when: editing a file cited by a claim flips that claim from `checked` to `stale` in the docs report, and `fm doctor` counts the stale ones.

- **Lint public surfaces for role names, not vendor or machine names** — SECURITY — value 5 — effort S — risk low — category: privacy
  Why: the user pushed back on showing "jarvis" and on naming Claude as the orchestrator. A ship-gate check should reject any public text that names a local endpoint, host, or vendor model where a role ("planner", "decision model", "embedder", "the orchestrator") belongs.
  Done when: a planted "jarvis" in `site/` or `README.md` fails `fm ship`, and the current tree passes with a one-line allowlist of intentional vendor mentions.

- **Print proven versus unproven by class on every finish card** — FEATURE — value 5 — effort S — risk low — category: observability
  Why: the mission says unproven things must be labelled. One line per class (behaviour, meaning, docs, UI, safety) with counts makes the label the product. Obsolescence angle: this honesty is what a bare agent's "done" lacks.
  Done when: a finish card shows `meaning: 3 proven / 2 unproven`, and the unproven items are listed with the command that would prove each one.

- **Track "works with any agent" as a per-agent proven matrix** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: the user wants any orchestrator to work, yet T-0336 (live-verify on codex, gemini, opencode) is blocked. If the claim stays unproven, a Claude-only integration will be copied natively. A matrix of agent × capability, each cell `proven`, `fake-only` or `unproven`, shows it plainly.
  Done when: the site and `fm doctor` render the matrix, and a cell turns `proven` only after a recorded run on that agent.

- **Retire a verb when a host-native run reproduces its result** — CLEAN — value 4 — effort L — risk med — category: simplicity
  Why: the inversion lens. For each verb, keep a held-out scenario; if a bare agent passes it for 30 days, mark the verb `covered natively` and drop it from default help. Assumption: the ablation harness can be pointed at a single verb.
  Done when: one verb with a passing bare arm is auto-listed as a retirement candidate with the evidence run ids.

- **Verify UI claims by DOM assertions on the web UI** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: "Surfaces: web UI" and many of the unchecked docs claims are about what a screen shows. A claim of the form `page X shows Y` becomes a headless fetch plus selector check, with no remote origin.
  Done when: a docs claim about the tower page runs against the local server and passes or fails, and a removed element makes it fail.

- **Wild: run a naive-reader child over the docs and file every sentence it cannot act on** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: the 421 unchecked claims suggest nobody has tried to follow the docs cold. A tool-less child with only the public docs attempts the quick-start, and each step that needs knowledge the docs lack becomes an `unproven` claim.
  Done when: the run yields a list of failed steps, each linked to a doc line, and a fixed line disappears on the next run.

- **Wild: let the repo prove itself out of existence** — FEATURE — value 3 — effort L — risk med — category: simplicity
  Why: a quarterly `fm obsolescence` report lists what Sampo still adds over a bare model, per gap class. It states the margin plainly and says "nothing" when the margin is zero. Assumption: the held-out arms exist.
  Done when: the report prints a margin per class, and a class with margin zero is stated outright in the report.

- **Wild: give every unproven label an expiry and a bounty** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: labels that sit forever become noise. Each `unproven` item gets a 14-day review date, and the nightly lane picks the cheapest to prove first. Items nobody proves in 14 days are listed in the morning card.
  Done when: an item past its date shows up in the next morning card, and one proven overnight is gone.

- **Wild: replay the user's missed asks as unproven-class tests** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: the pack lists asks the user had to make (T-2884 to T-2901). Each becomes a regression scenario in the meaning class, so the same kind of miss is checked before it is asked again.
  Done when: the eight listed asks each exist as a runnable scenario, and each fails on the commit before its fix.

Next question: which of the 599 meaning-class items would a bare agent also have caught, since only the rest is Sampo's margin?
Next question: when a docs claim is checked against a stale install rather than the source tree, which one does the label certify?
