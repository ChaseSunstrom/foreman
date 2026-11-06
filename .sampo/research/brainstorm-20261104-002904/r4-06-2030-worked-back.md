# Brainstorm — lens: 2030 worked back

- **Bisect every flipped claim to its commit** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the pack shows claim stamps expiring on cited-file change, but nothing names the commit that broke a claim; by 2030 agents land commits faster than humans can read them. Assumption: the claims table stores a runnable probe per claim.
  Done when: flipping a planted doc claim on a scratch repo makes `sampo` print the first bad commit and file one task naming claim id and sha, with no model call.

- **Widen each spec example into its neighbourhood** — FEATURE — value 4 — effort M — risk med — category: criteria
  Why: meaning is the largest unproven class (599) and an example is a single point. Assumption: examples have parseable inputs.
  Done when: a criterion compiled from "foo(2) → 4" also runs ten nearby inputs (type, boundary, empty) and reports "example holds, neighbourhood unproven" if outputs differ in shape from the example.

- **Run proofs against next-release dependencies nightly** — FEATURE — value 3 — effort M — risk low — category: forward-compat
  Why: proofs that pass only on today's pins give false comfort in 2030. Assumption: manifests expose a prerelease channel.
  Done when: a scratch run with a bumped pin shows which proven claims would flip, labelled "forecast", never changing the main verdict.

- **Turn a pasted screenshot or repro into a criterion** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: user pushbacks ("not that wild", the animation showing "jarvis") were visual, and the criteria extractor only reads text. Assumption: a vision-capable model is available in the session.
  Done when: a screenshot with a visible forbidden name yields a rendered-text check that fails on that screenshot and passes on a fixed one.

- **Set a verification SLO per repo** — FEATURE — value 4 — effort S — risk low — category: governance
  Why: unproven counts exist per class, but no budget says when to stop adding features. Assumption: the user will accept a halt.
  Done when: with the proven share below the set target, `sampo next` leads with a verification task and says "error budget spent".

- **Print the weakest link of every plan** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: a plan has many steps but one least-proven assumption decides whether it holds. Assumption: criteria carry a proof tier.
  Done when: a plan with one unproven step ends in a single line naming it and what would prove it.

- **Order lane landings by proven share** — FEATURE — value 3 — effort M — risk low — category: ship
  Why: parallel lanes merge in mission order, so an unproven lane can sit under proven ones. Assumption: lane hand-backs expose their proof counts.
  Done when: two lanes with different proven shares show a merge order that puts the better-proven one first, with the reason printed.

- **Store a proof dataset that belongs to the owner** — FEATURE — value 3 — effort M — risk low — category: local-first
  Why: (claim, probe, verdict, 14-day survival) tuples are the only signal Sampo didn't author. Assumption: survival data is rich enough to be worth keeping.
  Done when: one local file holds those tuples with no prose from the repo, and `sampo doctor` reports its row count.

- **Wild: Ship a time capsule of sealed claims for 2030** — FEATURE — value 2 — effort S — risk low — category: wild
  Why: assumption: long-lived projects will want to know how today's claims aged. Hash today's claim set and probes, and re-run them on a set date.
  Done when: `sampo capsule open` re-runs a sealed set and prints which claims held, flipped, or could not run.

- **Wild: Have an outside clock stamp each claim check** — SECURITY — value 2 — effort M — risk med — category: wild
  Why: a "checked on" date can be backdated, and tamper-evident ledgers are listed but anchored only locally. Opt-in only, because it sends a hash out.
  Done when: with the setting on, a claim stamp carries a public timestamp proof that verifies offline; with it off, nothing leaves the machine.

- **Wild: Give a stranger agent only the claims file and time its trust** — CLEAN — value 3 — effort M — risk low — category: wild
  Why: a 2030 reader may be an agent with no Sampo. Measure how long and how wrong it is when judging the repo from the claims file alone.
  Done when: a tool-less child reads only the claims file and its list of working features matches the proven set within a recorded error rate.

- **Wild: Let a local model hunt counterexamples overnight** — PERFORMANCE — value 3 — effort M — risk low — category: wild
  Why: idle local hardware is already in use for ideas. Report only hits against "proven" claims, never new passes.
  Done when: a planted claim with a hidden edge case is found by the overnight run, and a clean run prints nothing.

Next question: which proof tier does the user actually trust enough to stop reading the diff, and does that tier's later survival rate justify it?
Next question: what happens to claims and probes when the orchestrator, the judge model and the host CLI all change in the same month?
