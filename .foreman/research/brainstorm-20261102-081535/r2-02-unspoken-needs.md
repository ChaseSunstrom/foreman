# Brainstorm — lens: unspoken needs

Questions earlier brainstorms left, answered through my lens: when a user disagrees with a "done" a week later, the usual causes are proof run against the wrong build (idea 1), a later amendment to the ask (5), an unrelated thing that broke (4), or a proof that covered only a sample (3). Each idea below targets one of these.

- **Prove the running thing is the changed thing** — FEATURE — value 4 — effort S — risk low — category: UI proof
  Why: assumption: `fm shot` and `fm flow` can hit a stale dev server or an old installed copy (T-0418 shows installed foreman-ui lagging the source).
  Done when: a shot or flow against a process started before the last relevant commit prints "unproven: stale build" and refuses to stamp proven.

- **Disclose the sample on every proof** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: the request says unprovable parts must be labelled, but "N of M examined, chosen by X" is not required today. Assumption: some provers sample silently.
  Done when: every proof record carries `examined/total/how`, and a proof without them is shown as "scope unknown".

- **Prove what did not change** — FEATURE — value 4 — effort M — risk med — category: regression
  Why: "does it do what the user meant" includes "and nothing else broke". Assumption: current proofs only target the diff.
  Done when: for a diff touching module A, a before/after snapshot of untouched surfaces (screens, `--help` text, outputs chosen by dependency distance) runs, and an unexpected difference blocks "proven".

- **Prove removals** — FEATURE — value 4 — effort M — risk low — category: simplicity
  Why: T-0794 (slim Foreman, retire adapters), `plugin/skills` holding 1388 of 2117 files, and the standing lean steers all lead to deletions. Nothing proves a deletion is safe.
  Done when: after a deletion, a sweep over code, docs, configs, installed copies and the MASTER.md clauses finds no live reference to the removed symbol. Leftovers are listed; none means "removal proven".

- **Bind proofs to the wording of the ask they proved** — FEATURE — value 3 — effort M — risk low — category: intent
  Why: the user's stream is full of amendments ("T-2334's late start point applies only to open tasks", the re-scoped criteria). A proof of the old sentence is quietly stale.
  Done when: restating or amending a task marks proofs made under the earlier wording "proved the old ask", and the finish card lists them.

- **Pass unproven status down to dependent tasks** — FEATURE — value 4 — effort M — risk med — category: debt
  Why: assumption: a task that builds on an unproven predecessor currently shows clean.
  Done when: closing a task whose dependency has an open "unproven" claim prints "rests on unproven T-xxxx" on the receipt, and the label clears when that claim is proven.

- **Classify the unprovable up front** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: tokens spent trying to prove taste, future behaviour or third-party state buy nothing. T-0335, T-0336 and T-0337 are blocked waiting on real CLIs.
  Done when: a claim typed as judgment, future or external is labelled with its reason code in under a second, with no model call and no prover run.

- **Show which provers can run on this machine today** — FEATURE — value 4 — effort S — risk low — category: ops
  Why: T-0325 is blocked on a missing package and T-0336 on missing CLIs. The user can't tell "unprovable" from "tool not installed".
  Done when: `fm doctor` lists each proof kind as runnable, missing a named tool, or unreachable, with the one install command per gap queued through `fm ask`.

- **Adopt commits made outside Foreman as unproven** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: assumption: the user commits by hand sometimes, and those never enter the proof ledger, so "all proven" overstates.
  Done when: a post-commit hook (or the night tick) records any commit lacking a Foreman receipt as "unproven, made outside Foreman" and tries the cheap provers on it.

- **Answer "did we ever check X?" from the ledger** — FEATURE — value 3 — effort S — risk low — category: recall
  Why: the user asks a week later whether something was verified.
  Done when: `fm proof ask "<phrase>"` returns the matching proofs with date, kind and strength, or "no record", never a guess.

- **Write proof and unproven trailers into commits and PR text** — FEATURE — value 3 — effort S — risk low — category: collaboration
  Why: the discipline layer is invisible to reviewers who don't run Foreman.
  Done when: a shipped commit carries `Proved:` and `Unproven:` trailers that `fm` can parse back, and the PR body mirrors them.

- **Wild: put an expiry date on public claims** — FEATURE — value 3 — effort M — risk med — category: site/docs
  Why: wild; the README and site make dated claims ("passes", a "real session" demo, numbers).
  Done when: each claim carries a re-prove-by date, and a lapsed one opens a draft change that either re-proves or removes it.

- **Wild: turn the user's fears into standing probes** — FEATURE — value 3 — effort M — risk low — category: intent
  Why: wild; the unspoken need is "what would I be most embarrassed to find wrong?" A one-time five-question interview could compile the answers into probes that run at every finish.
  Done when: answering the interview adds named probes, and the next finish card shows each as pass, fail or unproven.

- **Wild: run a planted-lie drill on the human reader** — FEATURE — value 2 — effort M — risk med — category: trust
  Why: wild; no check exists that the user reads receipts closely enough to catch an overclaim.
  Done when: a weekly draft receipt with one planted false claim is posted, the user's catch or miss is recorded, and misses shorten the receipt format.

- **Wild: give every demo asset a provenance sidecar** — FIX — value 3 — effort S — risk low — category: site/docs
  Why: wild; `demo/live.svg` is presented as a real session. The sweep could go red on an asset older than the code it shows.
  Done when: each image or recording has a sidecar naming the command, commit and date, and a stale one fails the proof-before-presentation sweep.

Next question: which proof the user trusted most turned out wrong in the past, and was the prover or the claim at fault?
Next question: which proofs are never read, and would a proof the user can't read in ten seconds count as proof at all?
