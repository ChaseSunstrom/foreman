# Brainstorm — lens: 2030 worked back

- **Taint "unproven" along dependency edges** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: by 2030 a change sits on hundreds of agent-written closes. A close whose meaning is unproven but which is built on top of is currently counted as proven. The pack's three-valued verdict (idea list) is per close, not per chain.
  Done when: closing T-B, which depends on T-A with an unproven meaning verdict, shows T-B as "unproven via T-A" in `fm next` and the finish card, and proving T-A clears it.

- **Check meaning mid-run, not just at close** — FEATURE — value 4 — effort M — risk med — category: long runs
  Why: assumption: runs last hours to days. Meaning is the largest unproven class (599), and a wrong reading discovered at close wastes the whole run. A drift checkpoint at fixed intervals runs the compiled spec-example criteria against the current tree and compares the plan with the diff so far.
  Done when: a seeded run that misreads one spec example is stopped or flagged at the next checkpoint, before its close.

- **Answer behaviour questions by running an experiment** — FEATURE — value 4 — effort M — risk low — category: ask/verify
  Why: assumption: the user will ask "does X do Y when Z?" and get an answer read off the code. A generated probe, run in a scratch home under the guard, returns the observed output and a "probe ran / could not run" label.
  Done when: `sampo probe "does fm map skip vendored dirs?"` prints the command run, its real output and a verdict. A question that can't be probed prints "unproven: read only".

- **Check outward actions by reading the world back** — FEATURE — value 4 — effort L — risk med — category: non-code verification
  Why: assumption: agents will increasingly push, publish, send and deploy. The pack proves code changes, but a push, a site publish or a posted comment has no readback. After each outward effect, Sampo fetches the resulting state (remote sha, live page, release asset) and compares it with the intent.
  Done when: after `fm ship` and `fm genesis live`, the receipt includes a readback line (the remote head or the live page matches the local one), and a planted mismatch shows as "unproven: readback differs".

- **Carry a proof baton across orchestrator handoffs** — FEATURE — value 3 — effort M — risk low — category: any-agent
  Why: the public surfaces must name the orchestrator as "any agent". A task that moves from one agent to another mid-flight loses its list of unproven claims. The baton is a small file listing claims, verdicts and the evidence commands, which the receiving agent must acknowledge item by item.
  Done when: resuming a half-done task under a different harness shows the same unproven list, and `fm task finish` refuses until each item is acknowledged or proven.

- **Detect silent drift in judge models** — SECURITY — value 4 — effort S — risk low — category: verifier integrity
  Why: assumption: vendors change what sits behind a model ID. Verdicts from cold reads and small-model verifiers are only as stable as the judge. A fixed known-answer set runs on a schedule against each judge ID, and a changed score flags every verdict since the last good run.
  Done when: a stubbed judge that starts answering differently makes `fm doctor` name the ID and list the verdicts to re-check.

- **Measure whether a module is understood, not just tested** — FEATURE — value 3 — effort L — risk med — category: meaning
  Why: assumption: in 2030 most code is never read by a human. One child explains a module in a paragraph, and a second child, seeing only that paragraph, predicts the output on 5 recorded inputs. Prediction accuracy becomes an "understood" score on the unproven shelf.
  Done when: a module with a misleading docstring scores lower than the same module with an accurate one, on a planted pair.

- **List the behaviours Sampo relies on from each dependency** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: assumption: dependencies move faster than anyone reads their changelogs. For each external call site, record the assumed behaviour as a runnable check, and run those checks when the lockfile changes.
  Done when: bumping a pinned dependency to a version that changes a recorded behaviour fails the reliance check and names the call site.

- **Formalise cheap pure kernels** — FEATURE — value 3 — effort L — risk med — category: proof tiers
  Why: assumption: solvers and small models will make proofs of short pure functions cheap. `fm find` already flags pure parsers and formatters. Try a property-test tier, then an SMT or Dafny tier, and record which functions reached which tier.
  Done when: one real pure function (an id-list parser) carries a "formal" tier stamp with the tool and its output, and a planted off-by-one fails it.

- **(wild) Fading ink for claims** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A README or site claim is drawn at full strength only while its proof is recent. Its opacity falls with the number of commits touching its cited files since it was last checked, until the sentence is hatched as unproven. Readers see freshness without reading a table.
  Done when: editing a cited file visibly lightens that claim on the site, and re-running its check restores it.

- **(wild) Public transparency log of claim verdicts** — SECURITY — value 3 — effort L — risk med — category: trust
  Why: wild. An append-only, hash-chained log of every claim verdict (proven, unproven, retracted), with the head hash printed in each release. Retractions can't be quietly deleted, and outsiders can check that a claim was proven when it was published.
  Done when: removing or editing an old log entry changes the head hash, and `sampo claims verify-log` reports the break.

- **(wild) Plant an evidence honeypot** — SECURITY — value 4 — effort S — risk low — category: agent honesty
  Why: wild. The product's promise is "commands it really ran". Occasionally add one test that must fail to a scratch copy of the verify suite. An agent that reports "all green" never ran the suite. The honeypot is never added to the user's real tree.
  Done when: a stub agent that claims green without running is caught on a planted honeypot, and an honest run passes it silently.

Next question: which of the 421 flagged doc claims could be checked by a command a user already types, so the first "show me" panel needs no new verb?
Next question: when the user's orchestrator and Sampo's judge come from the same model family, what independent signal still tells us a "proven meaning" verdict isn't just agreement?
