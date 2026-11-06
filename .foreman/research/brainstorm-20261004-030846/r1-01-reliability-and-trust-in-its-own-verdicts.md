# Brainstorm — lens: reliability and trust in its own verdicts

- **Pin every spawned binary to an absolute path** — FIX — value 5 — effort S — risk low — category: harness safety
  Why: the stub `claude` that lost its shebang fell through PATH to the real one and cost $0.42. Any harness that shadows `claude` has the same trap.
  Done when: a test puts a non-executable stub first on PATH, and the spawn wrapper aborts with a named error and zero spend instead of falling through.

- **Trigger a security pass from what the diff touches** — FEATURE — value 5 — effort M — risk low — category: review
  Why: a background review found prompt injection, SSRF and terminal escapes that the in-loop reviewer graded MEDIUM/LOW. Network fetch, manifest or registry parsing, and text-to-terminal or text-to-prompt code get an adversary-only pass automatically before close.
  Done when: a fixture diff that adds an `urllib` fetch makes `fm audit prep` require the adversary lens, and the task can't close without it.

- **Check taint at the sinks** — SECURITY — value 5 — effort M — risk med — category: untrusted text
  Why: all three issues above were untrusted text reaching a sink (prompt, URL, terminal). Quarantine of lessons is already an idea, but this one is structural. Strings from web, registry, manifest or diff are wrapped as `Tainted`. The child runner, URL opener and terminal writer reject or escape them unless a named sanitizer is applied.
  Done when: a suite test fails if any sink accepts a raw `Tainted` value, and a fixture with an ESC sequence arrives escaped in the pane.

- **Score reviewer severity against what escapes later** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the pack shows grades (MEDIUM/LOW) that a later pass overturned. Record each finding's severity and the severity a later review or bug assigns the same defect. Auto-bump the severity of any finding class the reviewer has under-graded twice.
  Done when: replaying two recorded mis-grades makes `fm audit` print the class bumped, with the history.

- **Attribute escapes back to the closing task** — FEATURE — value 4 — effort M — risk low — category: verdict accuracy
  Why: assumption: no ledger yet links a later fix to the earlier "done" it contradicts. When a new task's failing test or hand-edit touches files an earlier closed task proved, record an escape against that task and the gate that passed it.
  Done when: `fm friction` lists an escape for a fixture pair of tasks, naming which criterion and gate missed it.

- **Re-derive each criterion blind** — FEATURE — value 4 — effort M — risk med — category: two-key verdict
  Why: "done" currently rests on fm-run evidence plus one reviewer who sees the story. A no-tools child gets only the criterion and the diff and says met, unmet or can't-tell. Disagreement with the run is surfaced, not auto-resolved. Run it for tier M/L only, to keep cost down.
  Done when: a fixture where the verify passes vacuously but the diff doesn't implement the criterion yields a disagreement line in the proof pack.

- **Re-run judge calibration when the model ID changes** — CLEAN — value 3 — effort S — risk low — category: judge drift
  Why: bench judges, reviewers and the quorum are all model-dependent. A frozen known-answer set runs once when `claude --version` or a configured model ID changes, and flips are reported. Judge calibration suites are already proposed, but this adds the trigger.
  Done when: changing the recorded model ID in a test fixture makes the next `fm doctor` run the set and print "N verdicts flipped".

- **Wild: Plant defects in review diffs, blind** — FEATURE — value 4 — effort L — risk med — category: live recall
  Why: wild. At a low rate, a scratch copy of the diff gets one seeded defect, and the reviewer isn't told. Whether it's caught gives a live measure of reviewer recall, and a miss is logged as reviewer drift. Nothing is planted in the real tree.
  Done when: a stub reviewer that ignores the plant produces a recorded miss, and the real working tree stays byte-identical.

- **Wild: Let proofs decay with churn** — FEATURE — value 3 — effort M — risk low — category: stale evidence
  Why: wild. A passing run's confidence fades as files in its impact set change, even if the exact tree stamp is not yet stale. The pane shows the fade, and `fm pr` refuses a proof below a threshold without a re-run.
  Done when: editing a file the map links to a criterion drops that criterion's pane state from "proven" to "aging", and `fm pr` names it.

- **Wild: Swap reviewer seats to find soft verdicts** — FEATURE — value 3 — effort M — risk med — category: verdict stability
  Why: wild. For tasks that closed on a single MEDIUM-or-lower pass, re-run the same lens on a different model, or with the evidence order shuffled. A flip marks the verdict "soft" in the ledger and the proof pack. Spend counts against `fm budget`.
  Done when: a fixture reviewer stub that flips on reordering marks the task soft, and a stable stub does not.
