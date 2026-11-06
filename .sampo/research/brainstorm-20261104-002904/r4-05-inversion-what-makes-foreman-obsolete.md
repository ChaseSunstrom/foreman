# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run a native-parity probe per verb** — FEATURE — value 5 — effort M — risk low — category: obsolescence
  Why: Mission 4 asks what is proven; "does the bare host already do this" is the unproven class nobody has measured. Pack lists T-0794 (slim Foreman) deferred with no evidence. Assumption: hosts ship plan/verify features each quarter.
  Done when: `sampo parity` prints, for each verb with a session path, a bare-agent arm result on the same scenario (same/worse/better) and a retire-candidate list.

- **Attach a retire-when predicate to every verb and skill** — CLEAN — value 4 — effort M — risk low — category: lifecycle
  Why: Lean rows exist as "pending measurement" with no deadline; the standing rule says only proven harm or duplication removes an idea. A predicate makes that testable.
  Done when: `fm doctor` fails if any verb/skill lacks a `retire_when:` line, and prints which predicates are currently true.

- **Watch host release notes and flag overlaps** — FEATURE — value 4 — effort M — risk med — category: host drift
  Why: Gate list shows hook protocol dependence (T-0337 Gemini Stop unwired, Claude Code plugin pane paint issue T-1217). Assumption: release notes are fetchable and the user permits network reads.
  Done when: a weekly job diffs the host's release notes against verb descriptions and files one "possibly native now" task per hit, each quoting the note line.

- **Publish the discipline as a harness-neutral spec with a conformance fake** — FEATURE — value 5 — effort L — risk med — category: portability
  Why: Standing rule: Sampo isn't specific to Claude Code; T-0335/0336 show non-Claude hosts unverified. If the host absorbs the discipline, the spec is what survives.
  Done when: a spec file plus a fake adapter passes the same criteria on three orchestrators, with unmet clauses listed as unproven per agent.

- **Run a monthly bare-model ablation on public surfaces** — PERFORMANCE — value 4 — effort M — risk low — category: measurement
  Why: T-1231 (beat Claude Code on the duel) and T-0866 (bench vs plain) are deferred for lack of cases; the standing exam rule puts a free arm first. Without this, "Sampo adds value" is unproven.
  Done when: a dated table shows pass rate, cost and time for bare vs Sampo on the same held-out scenarios, with the delta and an interval.

- **Tag lessons and guard rules with the model that taught them** — FEATURE — value 3 — effort S — risk low — category: model drift
  Why: T-0217 gives lessons a confidence; a newer model may no longer need them. Assumption: the model is recorded at lesson write time.
  Done when: each lesson shows its source model, and `sampo lessons --stale` lists those never recalled on a newer model.

- **Brown out unused verbs for a shadow week** — PERFORMANCE — value 3 — effort M — risk med — category: lean
  Why: Many verbs have no session path (standing rule on reach); the lean row waits on a measurement that nothing produces.
  Done when: a flag hides N chosen verbs for 7 days, and a report shows asks that hit a hidden verb versus none.

- **Stamp each doc claim "needs Sampo?"** — FEATURE — value 3 — effort S — risk low — category: claims
  Why: 421 docs claims are unchecked; some describe things any agent now does alone. Assumption: a claim can be classed by a cheap check.
  Done when: every flagged claim carries needs-sampo yes/no/unknown, and unknown ones appear on the unproven shelf.

- **Wild: Generate a shell-only fossil checker each release** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: if the harness or model is replaced, the only durable value is the proofs. Assumption: criteria compile to plain shell.
  Done when: a standalone script with no Sampo or Python dependency re-runs every filed criterion and prints pass/fail/unproven.

- **Wild: Self-dissolution plan on demand** — FEATURE — value 3 — effort M — risk low — category: exit
  Why: the lock-in meter idea has no inverse; the user's steers favour honesty over ceremony. Assumption: ledgers are exportable.
  Done when: `sampo eject` writes a plain-markdown bundle (steers, lessons, open tasks, criteria) and a README that a stock agent follows, verified by a cold child.

- **Wild: Ask each new model to design its own harness** — FEATURE — value 4 — effort M — risk med — category: obsolescence
  Why: when a stronger model joins, its unprompted discipline design shows what Sampo still adds. Assumption: a tool-less child can be given only the Mission goal.
  Done when: a diff lists which Sampo rules the model reinvented unprompted and which it never produced, filed against the retire-when list.

- **Wild: Petition to retire Sampo's own checker** — FEATURE — value 2 — effort S — risk low — category: humility
  Why: self-checks that keep passing without catching anything are the clearest obsolescence signal; gate tests exist but no catch record does.
  Done when: each gate reports its catch count over 60 days, and a zero-catch gate files a retirement task with the evidence.

- **Report a model-free proof share** — FEATURE — value 3 — effort S — risk low — category: durability
  Why: proofs that need no model survive any model change; Mission 4 labels the rest unproven.
  Done when: the finish card prints the share of closes proved by commands alone versus judged by a model.

Next question: which verbs does the user invoke by hand versus those only the drive calls, and does the bare host now cover the hand-invoked set?
Next question: what would the user have to lose for them to prefer plain Claude over Sampo for a week, and is that loss measured anywhere?
