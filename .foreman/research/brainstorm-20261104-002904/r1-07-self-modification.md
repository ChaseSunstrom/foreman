# Brainstorm — lens: self-modification

- **Compile spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the pack names meaning as the largest unproven class (599) and asks for spec example assertions to become runnable criteria. Sampo rewrites its own plan, adding a `Check:` line per extracted example (input, command, expected output). Anything it can't compile is stamped `unproven: needs judgment`.
  Done when: planning a spec with 3 fenced examples files a task with 3 runnable criteria, and `fm task prove` fails when one expected value is edited.

- **Run doc claims through a probe table and patch the loser** — FEATURE — value 5 — effort L — risk med — category: docs
  Why: 421 docs flag claims that no run has checked. Each claim maps to a probe command. When a probe fails, Sampo drafts a patch, either a doc edit or a red-first code fix, whichever the probe supports. Claims with no probe get an `unproven` marker in the text.
  Done when: a doc claim contradicted by a probe produces a filed task carrying the failing probe output, and the unprobed claim count falls on `fm doctor`.

- **Lint public surfaces for vendor and machine names, with autofix** — FIX — value 4 — effort S — risk low — category: naming
  Why: the user pushed back on "jarvis" and on naming Claude as the orchestrator. A role map (orchestrator, planner, judge, decision model, embedder) covers site/, README, the demo SVGs and generated data. Offenders are rewritten as patches, and the ship gate refuses new ones.
  Done when: planting "jarvis" or "Claude plans" in site/index.html fails `fm ship`, and the suggested patch swaps in the role name.

- **Stamp each proof with a hash of the files it read, and expire it on change** — FEATURE — value 4 — effort M — risk low — category: proof freshness
  Why: assumption: self-edits silently stale old "proven" labels. A label stores the content hash of the probe's inputs and reads `unproven (stale)` once any of them changes.
  Done when: editing a file a claim's probe touched flips that claim from proven to stale without rerunning anything.

- **Show a claim diff on every commit that edits Sampo itself** — FEATURE — value 4 — effort M — risk low — category: self-change review
  Why: Sampo edits skills, guard and docs. Before landing, it applies the diff in a scratch copy, reruns the claim probes, and writes the proven→unproven and unproven→proven transitions into the commit trailer.
  Done when: a commit that breaks one probe lists it under `Claims lost:` and the ship gate prints the same line.

- **Type every "unproven" with its reason** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: "labelled unproven" is vague as written. Reasons are an enum: needs-model-judgment, needs-live-service, needs-user-input, no-probe-yet. Each reason names who or what can clear it.
  Done when: `fm doctor --json` returns unproven counts grouped by reason, and no unproven item has a null reason.

- **Mutate every extracted criterion to prove it can fail** — FEATURE — value 4 — effort M — risk low — category: anti-vacuity
  Why: assumption: auto-compiled criteria from examples can pass trivially (an empty `grep`, a `true` exit). Perturb each expected value and require the check to go red.
  Done when: a criterion that still passes after its expected value is changed is rejected at plan time with the reason `vacuous`.

- **Fill live numbers into docs from probes** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: the README and MASTER.md hold counts and claims that drift. `{{probe:name}}` placeholders render from command output at build time, and a failed probe renders the sentence as `unproven`.
  Done when: changing the verb count changes the README number on the next build with no hand edit.

- **Judge a self-edit with the old version's exam, and the old guard with the new** — SECURITY — value 4 — effort M — risk med — category: ward safety
  Why: the Ward stops dangerous commands, and a self-edit could weaken it. Run the old and new rule sets against each other's exam corpora and block on any divergence in refusals.
  Done when: a patch that removes one refusal rule fails the cross-check and names the case it let through.

- **Wild: Re-prove a random 5% of "proven" claims from a clean clone each week** — FEATURE — value 3 — effort M — risk low — category: proof decay
  Why: wild; proofs that ran once on the author's machine rot. A weekly sample is rerun in a hermetic checkout, and the failure rate is published as the proof half-life.
  Done when: the weekly report lists the sampled claims and the share that still pass in a clean clone.

- **Wild: Let a doc edit its own wording down to what the probe proved** — FEATURE — value 3 — effort M — risk med — category: honest docs
  Why: wild; if a probe shows "works on every model" holds for only 2 of 4, Sampo proposes the narrower sentence ("verified on 2 models") instead of failing the doc.
  Done when: a broad claim with a partial probe result produces a diff narrowing it, with the probe output attached.

- **Wild: Quine check, where Sampo's own spec reproduces its behaviour** — FEATURE — value 3 — effort L — risk high — category: self-hosting
  Why: wild; a cold child builds the plan-compiler stub from spec.md's examples alone, and Sampo's real compiler is scored against that child's output on the examples. Disagreements mark where the spec is ambiguous.
  Done when: running the quine check produces a list of spec examples where the child's compiler and the real one differ.

Next question: Which of the 421 flagged doc claims are checkable with a zero-token command, and which truly need a model reading?
Next question: When Sampo rewrites its own docs, who signs off on the narrowed claim, the user or a cold read by a different model?
