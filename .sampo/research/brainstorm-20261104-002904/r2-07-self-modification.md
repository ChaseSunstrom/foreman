# Brainstorm — lens: self-modification

- **Run the fences a doc edit touches** — FEATURE — value 5 — effort M — risk low — category: docs proof
  Why: 421 docs flag claims no run has checked, and Sampo edits its own docs constantly (rename, genesis skill prose). Assumption: fenced examples in MASTER.md and README are mostly runnable.
  Done when: a commit that changes a fenced command or its quoted output without a captured run in the scratch home fails the ship gate, and a planted edit to a fence is caught.

- **Learn the criterion extractor from closed Done-whens** — FEATURE — value 5 — effort M — risk low — category: criteria
  Why: meaning is the largest unproven class (599), and Sampo's own closed tasks already pair spec examples with the commands that proved them. Assumption: enough pairs exist to mine shapes zero-token.
  Done when: the plan-time extractor turns at least 70% of a held-out batch of past spec examples into the criterion that was actually used, and lists the rest as unproven.

- **Mutate each steer's automatic check** — FIX — value 4 — effort S — risk low — category: steers
  Why: the standing rule says every steer gets an automatic check from `fm decide --check`, but nothing shows those checks can fail.
  Done when: `fm genesis sweep` plants a violation for each stored check, and any check that stays green is reported as unproven.

- **Tune skill descriptions by replayed activation** — PERFORMANCE — value 4 — effort M — risk med — category: self-tuning
  Why: 1,396 files under plugin/skills and a cc-skill-descriptions card show the trigger text is hand-written. Assumption: replaying the user's past asks is a fair activation exam.
  Done when: a proposed description edit lands only if it raises activation on a held-out ask set without losing any skill's existing hits.

- **Run a rename ledger with allow-zones** — CLEAN — value 4 — effort M — risk low — category: rename
  Why: the Foreman→Sampo rename keeps aliases and verbatim tower history, so a naive sweep either floods or misses. The mission also wants public surfaces to use roles, not vendor or machine names.
  Done when: each old-to-new pair has a declared zone (alias, history, public surface), and a sweep reports residue only in public zones, with zero false hits on history.

- **Put every self-edit on probation probes** — SECURITY — value 4 — effort M — risk med — category: self-edit safety
  Why: hooks and the guard are edited by Sampo itself, and the T-2900 and T-2901 drive bugs came from live behaviour no unit test saw.
  Done when: after a self-edit to hooks or the drive lands, the next 3 session starts run a fixed probe set, and a failure files a revert task with the probe output.

- **Close the unproven loop in one commit** — FEATURE — value 4 — effort S — risk low — category: labels
  Why: unproven labels only help if they flip when a probe arrives. Assumption: labels live in a data file and not in prose.
  Done when: adding a probe for an unproven claim flips its label in the same commit, and a label with a passing probe but no flip fails the gate.

- **Name the claim a frame growth makes provable** — FEATURE — value 3 — effort S — risk low — category: genesis
  Why: `fm genesis grow` needs evidence and a measure, but nothing says which unproven class shrinks.
  Done when: every grow entry carries a claim id plus a before and after unproven count, and a grow with no change is rejected.

- **Metamorphic self-test (wild)** — SECURITY — value 4 — effort L — risk med — category: test strength
  Why: green suites can lean on accidental properties. Apply meaning-preserving rewrites (local renames, reordered independent statements) to plugin/lib/sampo and require identical verb output on a recorded corpus.
  Done when: a transformed tree produces byte-identical `--json` output for 50 recorded invocations, and one planted order dependence is found.

- **Edit-adjacent adversary (wild)** — FEATURE — value 4 — effort M — risk low — category: adversarial
  Why: a tool-less child that sees only a diff summary, not Sampo's code, fits the rule that weakness-finding uses signals Foreman didn't author.
  Done when: after each self-edit the child writes 3 breaking scenarios, they run zero-token, and the hit rate is recorded per edit.

- **Let the spec defend itself at plan time (wild)** — FEATURE — value 4 — effort L — risk med — category: criteria
  Why: when the extractor compiles an example into a criterion, it also writes the lazy implementation that would pass it, and the plan keeps the criterion only if a second criterion rules that implementation out.
  Done when: a planted vacuous spec example is flagged as unproven at plan time.

- **Regenerate legacy shims from a table (wild-ish)** — CLEAN — value 2 — effort S — risk low — category: aliases
  Why: the fm*.py paths became shims in T-2748, and a stale cold-read list already named dead paths.
  Done when: shims are generated from one table, and a test imports each and fails if a module moved without its row.

Next question: which of Sampo's own self-edits (hooks, guard, drive, skills) have broken a live session after green tests, and what probe would have caught each?
Next question: can the plan-time criterion extractor run on a local model and still beat the zero-token baseline on the 599 meaning-class items?
