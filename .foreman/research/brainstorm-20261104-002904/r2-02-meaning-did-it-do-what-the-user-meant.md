# Brainstorm — lens: meaning: did it do what the user meant

- **Compile spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: meaning
  Why: the request names this as the top gap (599 unproven "meaning"). Assumption: asks and docs contain "X should print Y" examples that are parseable.
  Done when: planning a task whose ask includes "`fm foo` prints bar" files a criterion that runs `fm foo`, and a planted wrong output fails it.

- **Run each criterion against a wrong implementation first** — FEATURE — value 4 — effort M — risk low — category: meaning
  Why: a criterion that passes on a stub proves nothing (vacuous measures recur in the ideas list). Assumption: a no-op stub or parent commit can be run cheaply.
  Done when: a criterion that passes on the parent commit is rejected at filing with the reason "passes without the change".

- **Label every close with a three-valued meaning verdict** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: "whatever can't be proven is labelled unproven." Each close prints proven / unproven (reason) / contradicted, per clause of the ask.
  Done when: `sampo task finish` output lists each ask clause with one of the three labels, and an unmatched clause shows as unproven.

- **Classify the 421 flagged doc claims by how they can be checked** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: 421 docs flag claims no run has checked. Assumption: most fall into a few classes (command output, path exists, number, host behaviour).
  Done when: a generated table gives counts per class, each with a checker or an explicit "no mechanical check".

- **Stamp doc claims with the run and cited-file hash that checked them** — FEATURE — value 4 — effort M — risk med — category: docs
  Why: verified claims go stale silently. Done when: editing a cited file flips its claims to unproven in the report until re-run.

- **Lint public surfaces for role words, not vendor or machine names** — SECURITY — value 4 — effort S — risk low — category: public surface
  Why: the user pushed back on "jarvis" and "Claude" as orchestrator in scenes. Assumption: a denylist plus role table covers it (models by role, orchestrator as any agent).
  Done when: ship fails on a planted "jarvis" in site/, README, SVG text or genesis data, and passes on "the orchestrator".

- **Extract text from SVGs and rendered scenes into the same lint** — FIX — value 3 — effort S — risk low — category: public surface
  Why: the animated scenes are SVG/JS where names hide from prose greps. Done when: a name planted in an SVG `<text>` and in a JS string is caught.

- **Turn each user pushback into a regression probe at once** — FEATURE — value 5 — effort M — risk med — category: meaning
  Why: the user repeated "not jarvis", "not Claude", "wilder moons", "stop asking". Each is a checkable rule that should have become a test on first utterance. Done when: a pushback message files a probe, and replaying the old mistake fails it.

- **Resolve every proper noun in an ask before building** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: "jeff", "jev" took three rounds to be read as classifier models. Assumption: unknown nouns can be searched in the repo, catalogue and the web first.
  Done when: an ask containing an unresolvable noun prints "took X to mean Y, evidence Z" or asks once, and the noun is stored.

- **Grade criteria by the bug they would have caught** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: green does not mean meaningful; mutate the fix and see whether the criterion fails. Done when: a criterion that survives three mutants is labelled weak on the card.

- **Unproven shelf grouped by reason in the web UI and pane** — FEATURE — value 4 — effort M — risk low — category: UI
  Why: unproven must be visible, not buried. Done when: the shelf shows counts by reason (needs host, needs judgement, timed out, no checker) and each row links to its claim.

- **Wild: Dispatch a literal-minded newcomer child to act on the docs** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: 421 unchecked claims; a tool-less reader following the quickstart reveals the claims that fail. Assumption: a cheap child can drive a scratch home.
  Done when: its stuck points are filed as unproven claims with the sentence quoted.

- **Wild: Cold child guesses the orchestrator and machine from the rendered site** — SECURITY — value 3 — effort S — risk low — category: public surface
  Why: greps miss paraphrase leaks. Done when: the child's guess is "unknown" on the shipped pages, else it names the leaking line.

- **Wild: Wrong-but-green game on every plan** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: the failure to catch is a result that satisfies every criterion yet misses the meaning. A child writes the laziest passing diff, and the surviving cases become extra criteria.
  Done when: a plan shows its lazy-pass attempt and the criterion added to defeat it.

- **Wild: Expire "proven" claims by the commits that touch their files** — FEATURE — value 3 — effort M — risk med — category: docs
  Why: proof ages. Done when: after N commits touching cited files, a claim renders hatched until re-run.

Next question: which of the 421 flagged doc claims has a user already contradicted or re-asked about, and does that predict which classes of claim are worth checking first?
