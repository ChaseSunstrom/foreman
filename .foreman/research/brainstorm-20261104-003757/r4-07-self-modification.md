# Brainstorm — lens: self-modification

- **Replay every forged tool before it is replaced** — FEATURE — value 4 — effort M — risk low — category: forge
  Why: assumption: the pack has "spec and tests, code as regenerable cache" and "stdlib first" ideas, but no ground truth for what a tool did when it was really used. Log each forged tool's argv, stdin, exit and stdout hash to a fixture file. A regenerated or patched version must reproduce those fixtures first.
  Done when: editing a tool so one recorded call changes output makes `sampo tool promote` refuse and print the diverging call.

- **Run a challenger tool version in shadow** — FEATURE — value 4 — effort M — risk low — category: forge
  Why: assumption: the pack has champion/challenger for decision models (the Jev/Jeff/SelfJev benches) but nothing for tools. A challenger runs after the champion on live calls, only the champion's output is used, and diffs go to a ledger. It is promoted after N agreeing calls.
  Done when: a test with a champion and challenger that disagree once records the diff and does not promote.

- **Rewrite tool errors from small-model misreads** — FEATURE — value 4 — effort M — risk med — category: small-model uplift
  Why: the standing steer is to make 4B/9B models match frontier results through scaffolding. When a Smith run's next call after a tool error is wrong, the error text is a candidate for rewriting. A rewrite is accepted only if replaying the transcript with the new text produces the right next call on that model.
  Done when: a recorded misread transcript flips to the correct next call after the rewrite, and the rewrite is stored with that replay as its proof.

- **Tune the card retriever from followed and ignored cards** — FEATURE — value 4 — effort M — risk med — category: cards
  Why: T-2909 builds the card store and grid, but ranking is static. Log which served cards the model actually followed (a step was taken or a verb was called) and which it ignored, then adjust retrieval weights. Weight changes are tested on held-out scenarios and may only be applied if the exam holds.
  Done when: a weight change that lowers the held-out score is rejected by the gate, and the ledger shows the reason.

- **Rotate one tool's self-test into each session start** — PERFORMANCE — value 3 — effort S — risk low — category: forge health
  Why: assumption: forged tools break silently when the host, a runtime or a dependency changes. Run one tool's doctest, chosen by oldest last-check, under a 200 ms cap. It is silent unless it fails, and a failure marks the tool "unproven".
  Done when: breaking one tool's doctest makes it surface within N sessions, and the hook bench shows no regression.

- **Fuse tools that are always called together** — FEATURE — value 3 — effort M — risk med — category: forge
  Why: assumption: the closed-task history shows repeated pipelines of two forged tools. Propose a fused tool whose tests are the union of both tools' tests. Both originals stay until the fused tool passes a real-path firing.
  Done when: a fixture session containing a repeated A→B pipeline produces a fusion proposal that passes both tools' tests.

- **Show payback date at forge time** — FEATURE — value 3 — effort S — risk low — category: forge economics
  Why: the budget is capped ($200) and the tower's lean rules say growth must earn its place. Store each forged tool's build cost (tokens and dollars), then show calls × estimated saved time against that cost on a "pays back by" line. A tool still unpaid at its fuse date is retired.
  Done when: `sampo tool list` prints a payback state for each tool, and an unpaid tool past its fuse is flagged for retirement.

- **Label private-repo data in cards and tools, and block export** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: cards and tools are mined from closed tasks and failures, which carry repo paths, names and sometimes secrets. Mark any card or tool derived from private material "local only". Publishing, the starter shelf, the site's Genesis data and `sampo tool export` then refuse it until it is scrubbed.
  Done when: exporting a card whose source task touched a planted secret fails, and the scrubbed version exports.

- **Imprint a repo's script style on forged tools** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: assumption: tools that follow the repo's language, flag style, lint config and test layout are easier for the user to accept and to hand-edit. Read the repo's own scripts and Makefile to produce a short style card before forging.
  Done when: a tool forged in a fixture repo uses that repo's language and test layout, and a lint check passes.

- **Wild: Forge each tool twice blind and treat disagreement as a spec bug** — FEATURE — value 4 — effort M — risk low — category: spec quality
  Why: wild. Two different models (for example the 27B and a Haiku-class model) each forge from the same passport and tests only, without seeing each other's code. Where their outputs differ on generated inputs, the spec is ambiguous, and Sampo asks for a sharper spec instead of picking a winner.
  Done when: for a deliberately ambiguous spec, a differential run reports at least one input where the two builds disagree.

- **Wild: Write a nightly "scar digest" and quiz a cold model on it** — FEATURE — value 3 — effort M — risk low — category: small-model uplift
  Why: wild. The forge leaves many scar cards from failed builds. Each night, compress them into a one-page digest. A cold 9B model is quizzed on it, and the digest ships only if the quiz score holds after compression.
  Done when: a digest that drops a key scar card fails the quiz and is rejected.

- **Wild: Let the small model file a feature request for the forge mid-task** — FEATURE — value 3 — effort M — risk med — category: self-improvement
  Why: wild. A local model that hits a gap emits a typed "I wish I had X" line. The nightly lane clusters these lines, ranks them by how often they recur, and forges only the top one under the normal gates. No model is trusted to change the forge directly.
  Done when: three fixture sessions with the same wish line produce one ranked request, and nothing is forged until it passes the gates.

- **Wild: Keep a hash-sealed "last good forge" the new forge must beat on old gaps** — SECURITY — value 4 — effort M — risk low — category: self-edit safety
  Why: wild. Before any edit to the forge's own code, snapshot its hash and replay the saved gap corpus against both versions. The edit is accepted only if the new forge solves at least what the old one solved. A second hash seals the corpus, so the corpus can't be weakened in the same change.
  Done when: an edit that drops one previously solved gap is refused, and one that tampers with the corpus hash is refused too.

Next question: which forged tools have been called by a real session path rather than only by their own tests, and what does that rate say about whether the forge is paying for itself?
Next question: when a self-edit touches the forge, the cards and the exam in one night, which of the three should be frozen so the other two can't quietly agree with each other?
