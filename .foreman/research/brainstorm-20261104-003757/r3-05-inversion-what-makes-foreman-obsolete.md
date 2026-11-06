# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Store each forged tool as spec, tests and a rebuild receipt, and treat the code as an evictable cache** — FEATURE — value 4 — effort M — risk low — category: simplicity
  Why: assumption: models keep getting better at writing small tools, so the durable asset is the spec plus the negative-control test. A rebuild receipt (tokens, seconds, model) lets the shelf keep a tool only when rebuilding costs more than keeping it.
  Done when: deleting a tool's code dir and running `sampo tool NAME` rebuilds it from spec, passes its tests, and prints the rebuild cost against a stored threshold.

- **Add a spec-only acquisition mode for orchestrators that already build well** — FEATURE — value 4 — effort M — risk low — category: capability
  Why: assumption: hosts will ship their own find-and-build. Sampo's part that is hard to replace is the Exam, the quarantine and the grant. In this mode it emits only spec, tests and a pass/fail checker, and the host does the building.
  Done when: a stub orchestrator given only the spec file produces a tool, and `sampo tool check` grades it with no Sampo-authored code in it.

- **Classify every missing-tool moment before acting: knowledge, permission, capability or taste** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the pack's tool-gap ladder treats all gaps alike. Only capability gaps need acquisition, and the other three are a note, a grant or a question. A small decision model (Kev or Jeff) can label them, and the labelled history shows how much of the loop was never needed.
  Done when: replaying the stored gap records yields a label histogram, and acquisition fires only on "capability".

- **Build tools ephemeral by default and promote them only after repeated real use** — FEATURE — value 4 — effort M — risk low — category: simplicity
  Why: a tool that vanishes at run end cannot go stale, drift or need retirement. Promoting after N reuses (the pack's rule-of-three), with the first build kept in scratch, inverts "install then maintain".
  Done when: a first-use tool lives only in a per-run scratch dir and is gone at close; the third use triggers a promotion card with the call counts.

- **Run a randomized live counterfactual: one in twenty gap sessions solves inline with acquisition off** — FEATURE — value 5 — effort M — risk med — category: measurement
  Why: the pack's replay arms use recorded gaps, not live behaviour. A seeded holdout of real sessions measures whether acquisition changes outcome survival, and the loop's own obsolescence shows up as a flat difference. It needs the user's opt-in setting.
  Done when: `sampo outcomes --acq-holdout` prints survival for held-out and treated gap sessions with an interval, and the holdout is off unless set.

- **Hide shelf entries from models that pass the gap bare, without deleting them** — PERFORMANCE — value 3 — effort S — risk low — category: context cost
  Why: the pack covers retiring cards, but not conditional visibility. The shelf manifest would carry a per-model bare-pass bit refreshed when the served model id changes, so a 27B sees fewer tool descriptions than a 4B.
  Done when: the same repo, served with two profiles, injects different tool lists, and the diff cites the bare-pass rows.

- **Probe each search source nightly with known-good queries and park dead ones** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: registries and indexes change shape or vanish. A silent source returning nothing looks the same as "no tool exists", which would fake a build-it verdict.
  Done when: a source that returns zero for a canary query is marked parked in `sampo plugins find` output, and no "not found" verdict is issued from it.

- **Wild: let the 27B write a replacement for the acquisition loop each night and file Sampo's retirement if it ties** — FEATURE — value 4 — effort L — risk med — category: self-obsolescence
  Why: wild. A cold local model gets only the gap corpus and the tool exam, writes a 200-line find/build/test loop, and runs the same arms. A tie or win on the exam files a "replace ours" task with its diff.
  Done when: a nightly lane writes `candidate-loop/`, scores it on the tool exam beside Sampo's, and prints the margin.

- **Wild: on a new model id at the endpoint, sweep every gap bare and post "this model retired N tools" to the morning card** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild. The Foreman→Sampo rename and the 3-minute model-switch cost make model changes events worth a ritual. Obsolescence becomes a gift: a count of tools the new model no longer needs, each with its bare-pass transcript.
  Done when: changing the profile's model id triggers one lane run and a card listing retired and kept tools with links.

- **Wild: ask each frontier model weekly what tools it wishes it had, and delete shelf entries it never mentions** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: wild. The model's own wish-list, taken with no shelf in context, is an unbiased demand signal. Shelf tools with no match for weeks are probably builder fiction.
  Done when: `sampo tool wishes` shows a matched/unmatched table against the shelf, and unmatched entries get a sunset date.

- **Wild: hold a monthly empty-shelf drill that rebuilds the top gaps from a 20-line bootstrapper** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: wild. If a scratch clone with an empty shelf recloses the last month's gaps within budget, the shelf is a cache and can be pruned or shared freely. If it doesn't, the shelf has value worth protecting.
  Done when: the drill prints closed/total gaps, time and spend, and fails the doctor check when it is under a stated ratio.

- **Make the grant queue the only unmodelable surface and show its size first** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: grants are what only the user can supply; find and build can be replaced. A web-UI line "of N acquisitions, K needed a grant, M didn't" tells the user where Sampo's real role is.
  Done when: the pane and web UI show N, K and M for the last 30 days from ledgers alone.

- **Pin a search cost ceiling per gap so acquisition cannot cost more than writing the one-liner** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: assumption: for many gaps the host's own inline script is cheaper than search, vet and quarantine. A priced cutoff based on the median inline solve (tokens, seconds) for that gap class keeps the loop from over-serving.
  Done when: a gap whose estimated search cost exceeds the class's inline median skips straight to an inline script and logs why.

Next question: Which gaps in the corpus were ever closed by something the user already had installed or in their repo, and is that share growing?
Next question: If the loop is made spec-only for strong orchestrators, which Exam signal would still tell the user Sampo earned its place?
