# Brainstorm — lens: bold bets

- **Trace what every verify command really touched** — FEATURE — value 5 — effort L — risk med — category: evidence
  Why: assumption: "vacuous proofs" and "tests that never ran the changed code" are the usual false-done. Running verify under bwrap/strace gives a language-agnostic effect manifest (files read and written, hosts contacted, processes spawned) that the proof carries.
  Done when: a verify command that never opens or executes the changed artifact is stamped "unexercised", and one that writes outside the repo or reaches an undeclared host fails. A planted fixture of each is caught.

- **Add a sink bay for outward effects** — FEATURE — value 5 — effort L — risk med — category: flows
  Why: assumption: `fm flow` can prove what a screen shows but not "the email went out" or "the webhook fired". Bundle local sinks (SMTP catcher, webhook catcher, S3-compatible store, mock OIDC IdP, payment mock, injectable clock) that flows assert against.
  Done when: a fixture app's signup flow passes only if the SMTP sink received a message with the right link, and fails when the send is removed.

- **Prove scripts and migrations by running them twice and undoing them** — FEATURE — value 4 — effort M — risk low — category: ops proof
  Why: assumption: the pack asks for infra and data proof, and idempotence and reversibility are common unclaimed properties. Apply, apply again, revert, and diff snapshots of files, DB dump and env. Any diff on the second run names its source (time, randomness, ordering).
  Done when: a fixture installer that appends a line on every run fails the second-run diff with that line named, and a clean one passes.

- **Drive desktop GUIs through the accessibility tree** — FEATURE — value 3 — effort L — risk med — category: UI proof
  Why: Foreman Desktop exists (T-0325, T-0352) and `fm shot`/`fm flow` cover only the web. AT-SPI on Linux (UIA/AX later) gives clicks, text and state assertions without pixels.
  Done when: a flow opens Foreman Desktop, clicks a named control and asserts a label, and reports "unproven: no a11y bus" where the bus is absent.

- **Prove generated documents, not just code** — FEATURE — value 3 — effort M — risk low — category: deliverables
  Why: assumption: the request says "verifying anything", but PDFs, slide decks and spreadsheets have no prover. Render to images, extract text, check overflow, missing fonts and broken links, and recompute spreadsheet formulas independently.
  Done when: a fixture xlsx with a wrong total and a PDF with clipped text are both flagged with page and cell references.

- **Synthesize fuzz harnesses for changed parsers and pure functions** — FEATURE — value 4 — effort L — risk med — category: deep prover
  Why: assumption: parsers are where Foreman's own work lives (`fm find`, intake, exam grading). A tool-less child writes a harness from the signature, a native fuzzer (atheris, cargo-fuzz, go fuzz) runs it overnight, and each crash becomes a regression test.
  Done when: a planted off-by-one in a fixture parser is found within the time box and the shrunk input is saved as a test.

- **Learn volatile-region masks for `fm shot` automatically** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: assumption: whole-page pixel diffs flake on clocks, avatars and ads. Run the flow N times, find regions that differ with no code change, and mask only those.
  Done when: a fixture page with a ticking clock gives zero false diffs, and a real layout change outside the mask still fails.

- **Time-travel flows with an injected clock** — FEATURE — value 4 — effort M — risk med — category: flows
  Why: assumption: trial expiry, token refresh and billing cycles can't be proven in real time. Run the product process under libfaketime and advance days between flow steps.
  Done when: a fixture "trial ends after 14 days" flow passes at +13d and +15d, and the proof lists the clock offsets used.

- **Prove cost claims** — FEATURE — value 3 — effort M — risk low — category: perf and cost
  Why: assumption: "cheaper" and "smaller" are common claims with no prover. Check infra cost delta from a plan (infracost-style), bundle and binary size, tokens per request for LLM features, and CI minutes, each against a stored baseline.
  Done when: a size-budget claim on a fixture bundle passes or fails with the byte delta, and "no pricing data" is labelled unproven.

- **Run the cross-OS proof on a throwaway CI branch** — FEATURE — value 3 — effort M — risk high — category: matrix
  Why: assumption: "works on my machine" is the unprovable-locally case. `fm prove --ci` pushes a scratch branch, waits for the matrix, pulls results back as proof records and deletes the branch. It is outward-facing, so it asks first.
  Done when: with a grant, a two-OS matrix result lands as proof records and the branch is deleted. Without one, the claim is labelled unproven with that reason.

- **Wild: trace every number on screen back to its source** — FEATURE — value 4 — effort L — risk high — category: data lineage
  Why: wild: "does the dashboard total match the data" is the classic UI-and-data gap. Taint the DB cell, follow it through the API into the rendered DOM text, and show the lineage path for each checked number.
  Done when: a fixture report with a double-counted join is flagged, with the query and the DOM node named.

- **Wild: stage a synthetic population of 200 stub users** — FEATURE — value 3 — effort L — risk med — category: simulation
  Why: wild: one flow proves a path, not a distribution. Stub users with seeded behaviours (hesitant, mistyping, back-button) hit staging, and the funnel completion rate becomes the proof, with its noise floor stated.
  Done when: a fixture app with a broken step for mobile-width users shows a completion drop for that segment, and the seed reproduces it exactly.

- **Wild: hold a viva on the diff** — FEATURE — value 3 — effort M — risk low — category: intent
  Why: wild: "does it do what the user meant" is the weakest class. A cold child gets the diff and the user's sentence, asks the builder one question per hunk ("which words of the request does this serve?"), and flags hunks with no answer or an invented one.
  Done when: a fixture diff with an unrequested refactor yields a "serves no stated need" flag on that hunk, and a tight diff yields none.

- **Wild: keep a proof-sparring page in the web UI** — FEATURE — value 2 — effort M — risk low — category: web UI
  Why: wild: the user types a claim on a page, and a hostile-reviewer child picks provers and runs them live while the user watches, with a veto and an "I'd also try…" box. This turns "verify anything" into a conversation.
  Done when: typing a claim shows the chosen provers streaming and ends with a proof record or an "unproven: reason" line.

Next question: Which claim classes in the last 90 days of closed tasks were finished with no machine-checkable evidence, and what would the cheapest prover for each have cost to build?
Next question: Which verify commands in this repo have never failed once, and does a planted break make any of them fail?
