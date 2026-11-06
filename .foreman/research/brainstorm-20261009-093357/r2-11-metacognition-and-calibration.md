# Brainstorm — lens: metacognition and calibration

- **Declare a working mode and flag mode violations** — FEATURE — value 4 — effort M — risk low — category: self-monitoring
  Why: assumption: edits made while still diagnosing and "done" claims made while still exploring are a common failure. The pack shows per-step discipline but nothing that notices the kind of activity has changed.
  Done when: each step records explore/decide/build/verify/ship, and a test shows an edit in a task declared "explore" is flagged by a hook and written to the ledger.

- **Split confidence into four separate axes** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: assumption: one "confidence" number hides which kind of belief fails. The four axes are diagnosis right, change complete, nothing else broke, and matches what the user meant. The pack's `fm bench` and rework data could score each axis separately.
  Done when: `fm task done` stores four values, and `fm friction` prints a per-axis hit rate over the last N tasks.

- **Make confidence trigger falsification in proportion** — FEATURE — value 4 — effort S — risk low — category: reasoning discipline
  Why: assumption: sure-sounding claims are the ones least often checked. The rule is that the higher the stated confidence on a load-bearing claim, the more it must try to disprove itself (a probe that could fail, run before the claim is recorded).
  Done when: a brief with a "high" confidence claim and no falsifier probe fails a lint, and the passing case shows the recorded probe command and its output.

- **Alarm on suspiciously smooth tasks** — FEATURE — value 4 — effort M — risk low — category: surprise tracking
  Why: assumption: Foreman has failure signals (blocks, retries) but not "too good to be true". A task with no red gate, no surprise and no retry, in an area with a high historical surprise rate (from `fm recall` and the ledger), gets a forced independent probe before done.
  Done when: a replay of a smooth task in a historically rough file produces the alarm, and a smooth task in a quiet file does not.

- **Triage every unknown as know, find out, or ask** — FEATURE — value 4 — effort M — risk low — category: feeling-of-knowing
  Why: the pack has "ask by information gain", but no explicit three-way router before a question reaches the user. The rule: answer from memory only if recall confirms it, send a bounded fm-scout/recon pass if the answer is findable, and ask the user only if neither works. Each route is later scored on whether it was right.
  Done when: the ledger logs a route for each open question and `fm friction` reports the share of asks that a scout could have answered.

- **Test whether stated reasons are the real reasons** — FEATURE — value 4 — effort L — risk med — category: introspection accuracy
  Why: assumption: rationale in briefs and decisions may be post-hoc. The test re-runs a decision step with the cited reason removed from context, and flags the reason as unfaithful if the choice doesn't change. This is related to the existing context-ablation idea but audits stated reasons, not injected context.
  Done when: on a bench of recorded decisions, `fm bench` outputs a faithfulness rate per rationale, and a planted fake rationale is detected.

- **Track confidence laundering across handoffs** — FEATURE — value 4 — effort M — risk low — category: uncertainty provenance
  Why: assumption: a sub-agent's "probably" turns into the main thread's "is" and then the user's "done". Each claim in the final report carries its weakest upstream hedge, and the report is checked for claims stronger than their source.
  Done when: a fixture where fm-recon says "unverified" produces a done summary lint failure if it states the claim flatly.

- **Detect hindsight rewriting in close-outs** — FEATURE — value 3 — effort M — risk low — category: bias detection
  Why: assumption: close-out lessons often say "as expected" about things the intake brief rated low-probability. Compare the intake risks and confidence to the closing narrative, and flag a story that contradicts what was written at the time.
  Done when: a test pair (brief rating a risk 10%, close-out calling it "obvious") is flagged and the original wording is shown beside it.

- **Refit calibration on every model change** — FEATURE — value 3 — effort M — risk low — category: calibration drift
  Why: the pack stamps model and build on events (a seen idea), and T-0217 gives lessons a confidence. Calibration curves are model-specific, so a new model id should start with wide, conservative thresholds and tighten as its own track record fills in.
  Done when: after a model id change, `fm doctor` shows "calibration: provisional (n=3/30)" and escalation thresholds use the provisional values.

- **Wild: Make the user and Foreman bet on outcomes** — FEATURE — value 3 — effort M — risk low — category: shared calibration (wild)
  Why: wild: at intake, one tap lets the user guess "first-try pass? Y/N". A weekly scoreboard compares their calibration with Foreman's. The user's gut feel also becomes a labelled signal about which tasks are secretly hard.
  Done when: `fm task new` accepts an optional guess, and `fm friction` prints the two Brier scores side by side after 20 tasks.

- **Wild: Re-derive each L decision cold the next morning** — FEATURE — value 3 — effort M — risk low — category: test-retest reliability (wild)
  Why: wild: a fresh context, given only the question and not the answer, decides again overnight. If the two answers differ, the decision was fragile and gets reopened with both rationales shown. It differs from "ask only when sampled plans disagree" because it tests stability across time and context.
  Done when: a planted flaky decision is flagged in the morning digest and a stable one is not.

- **Wild: Keep a journal of "I was sure and wrong" moments** — FEATURE — value 3 — effort S — risk low — category: overconfidence casebook (wild)
  Why: wild: every high-confidence miss is stored with the surface features of the situation. At intake, Foreman is warned in plain words ("you were sure about migrations and wrong 3 of 4 times"). The warnings are matched on features, not tags.
  Done when: seeding three misses of one kind makes a similar new task show the warning in its brief.

- **Add a doubt budget that scales with irreversibility** — FEATURE — value 4 — effort M — risk med — category: stakes-aware metacognition
  Why: assumption: "cap deliberation by stakes" exists, but doubt is not tied to one-way doors. Before an irreversible action (push, delete, migration), Foreman must name its top two ways of being wrong and the probe that rules each out, and the number of required probes grows as confidence falls.
  Done when: an irreversible command in the guard demo is held until two named failure modes and passing probes are in the ledger.
