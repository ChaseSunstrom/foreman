# Brainstorm — lens: meaning: did it do what the user meant

- **Compile spec examples into a failing-first criteria block at plan time** — FEATURE — value 5 — effort M — risk med — category: meaning
  Why: the request names this as the top gap (599 unproven "meaning" items). Assumption: spec examples are mostly "given X, expect Y" lines extractable by pattern.
  Done when: a planted spec with three examples yields three runnable criteria, each shown failing on the pre-change tree, and a fourth, unextractable example is listed as unproven.

- **Replay each user pushback as a standing regression probe** — FEATURE — value 5 — effort M — risk low — category: meaning
  Why: the user's recent pushbacks ("not that wild", "don't say jarvis", "any orchestrator") were each a meaning miss that was then fixed once and never checked again. Assumption: a pushback can be stored as a quote plus a check (lint, grep or rubric).
  Done when: a stored "never name the user's machine on public surfaces" probe fails when a planted "jarvis" is added to the site and passes after removal.

- **Lint public surfaces by role words, from one role table** — SECURITY — value 4 — effort M — risk low — category: public surfaces
  Why: the steer says surfaces must name models by role and the orchestrator as any agent. Assumption: the table can list forbidden vendor, host and endpoint names with the role each maps to.
  Done when: the ship gate fails on a planted vendor or machine name in README, site HTML, SVG text, alt text and scene captions, and each failure suggests its role word.

- **Stamp each doc claim with the run that checked it and the files it cites** — FEATURE — value 5 — effort L — risk med — category: docs claims
  Why: 421 docs flag claims no run has checked. Assumption: claims can be keyed by sentence hash and a cited path.
  Done when: editing a cited file turns that claim's stamp to "stale" within one `fm doctor`, and the claims table shows proven, unproven and stale counts per doc file.

- **Classify the 421 flagged claims by how they can be checked** — CLEAN — value 4 — effort S — risk low — category: docs claims
  Why: a typed split (command output, file exists, number, host behaviour, judgement) says which can be mechanised and which must stay labelled unproven. Assumption: a rule-first classifier covers most of them.
  Done when: all 421 carry a class and a reason, and the report states how many are mechanically checkable.

- **Add a mutation check for every compiled criterion** — FEATURE — value 4 — effort M — risk low — category: proof quality
  Why: a criterion that cannot fail proves nothing, which is how a green close can still miss the meaning. Assumption: a small set of wrong implementations (stub, empty output, wrong constant) is enough.
  Done when: a tautological criterion is rejected at filing, and a real one reports its kill count.

- **Make a close carry a three-valued meaning verdict** — FEATURE — value 4 — effort M — risk med — category: finish card
  Why: closes now say passed or failed, but the ask is whether it did what was meant. Assumption: proven, unproven and contradicted are enough states.
  Done when: the finish card prints "meaning: 3 proven, 2 unproven (reason)" and the unproven list is on the web UI shelf.

- **Resolve every proper noun in an ask against the repo before building** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: "jeff", "jev" and "jarvis" were each misread because no referent was checked. Assumption: a noun with no match in the repo or catalogue is a cheap, reliable signal.
  Done when: an ask containing "jev" with no referent produces one question with the nearest candidates, and unambiguous nouns produce none.

- **Turn "wild", "simple" and "like X" into a rubric at intake** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: the user said the moons were "not that wild" because nothing measured wildness. Assumption: the existing wildness score is the model for other adjectives.
  Done when: an ask containing "simple" files a Done-when with a measurable bar such as a count or line limit, and the user can edit it.

- **Wild: Run a blind leak reader over the rendered site** — SECURITY — value 4 — effort M — risk low — category: public surfaces — wild
  Why: a text lint misses what only appears once rendered. Assumption: a tool-less child can read text extracted from the rendered page.
  Done when: it names no orchestrator, vendor or host on a clean build, and names the planted one on a seeded build.

- **Wild: Rotate the orchestrator name in every scene per page load** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: "any orchestrator" is stated but each scene still shows one, so the claim is asserted rather than seen. Assumption: scene text is parameterised.
  Done when: two loads show different agent names, and none shows a vendor-specific one.

- **Wild: Have a literal-minded child run the quickstart and log every guess** — FEATURE — value 4 — effort M — risk low — category: docs claims — wild
  Why: guesses mark the places where docs depend on unstated meaning. Assumption: a small local model is enough to act as the literal reader.
  Done when: each guess becomes a doc-gap item and a clean run logs zero guesses.

- **Hatch every unproven claim with a typed reason and an expiry** — FEATURE — value 4 — effort M — risk low — category: unproven shelf
  Why: the request says what cannot be proven must be labelled. Assumption: the reason types are no probe, needs host, judgement and stale.
  Done when: no claim is untyped, and an expired one resurfaces in `fm next`.

Next question: Which of the user's past pushbacks can be rebuilt from the record into a quote-and-check pair, and what share fall into classes no cheap check can cover?
Next question: When a criterion extracted from a spec example is wrong, does the user find out at close, at review, or only by re-asking?
