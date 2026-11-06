# Brainstorm — lens: reasoning and thought process

- **Carry an invariant ledger across the plan's steps** — FEATURE — value 4 — effort M — risk low — category: reasoning
  Why: the pack has pre/postconditions per step, frame conditions and per-step predictions as separate ideas, but nothing that holds one running set of "facts I currently rely on" and re-checks each fact when a later step touches the thing it came from. Assumption: stale assumptions are a main cause of mid-task wrong turns.
  Done when: a test task where step 3 edits a file that step 1's recorded fact depended on makes `fm task` flag that fact as unverified before step 4 starts.

- **Name the reasoning move before each non-trivial step** — FEATURE — value 4 — effort M — risk low — category: reasoning
  Why: the pack covers named problem-solving methods and "learn which reasoning moves worked", but not a lightweight, recorded per-step label (reproduce, bisect, analogize, simplify, invert, probe) that the bench can later correlate with first-pass success. Assumption: step logs currently record actions, not the thinking move.
  Done when: `fm task step` accepts a move tag, the ledger stores it, and `fm bench` can print pass rate per move.

- **Make the second opinion see only the question, not the answer** — FEATURE — value 4 — effort S — risk low — category: deliberation
  Why: `fm second` exists, and blind rounds exist for `fm ideas`, but the plan/debate seconds probably receive the main thread's framing, which anchors them. Assumption: current seconds get the draft plan.
  Done when: `fm second plan --blind` runs with only the brief, and a test shows its prompt does not contain the draft plan text.

- **Rank hypotheses by cost-to-test over probability, not probability alone** — FEATURE — value 4 — effort S — risk low — category: debugging
  Why: fm-debugger returns ranked hypotheses with probes; ranking by likelihood alone makes it start with the expensive probe. Existing ideas cover information gain and posterior; this is the cheap operational version that needs no probability model.
  Done when: debugger output includes a probe cost estimate per hypothesis and the suggested order is sorted by likelihood divided by cost, verified on a fixture.

- **Detect when a plan step silently changes the question** — FEATURE — value 3 — effort M — risk med — category: drift
  Why: scope drift is checked against the diff at done, but nothing compares the current step's stated goal with the brief's interpretation mid-run. Users' repeated "never got done" complaints (cleanup) suggest goals quietly shrink. Assumption: shrinkage occurs in the steps, not only at close.
  Done when: a step whose goal text no longer overlaps any acceptance criterion or non-goal raises a warning at step start in a replayed fixture.

- **Write the "what I did not consider" section last, from the diff** — FEATURE — value 3 — effort M — risk low — category: self-critique
  Why: risks are written at plan time, before the work reveals them. A post-hoc pass reading the diff for categories the plan's risk list never mentioned (concurrency, error paths, migration, docs) catches gaps the plan could not know. Distinct from the escapes analysis, which waits for a failure.
  Done when: `fm task done` prints a short list of diff features with no matching plan risk, and a fixture diff touching a lock file produces the expected line.

- **Give every ask a default and an expiry before it interrupts** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: the pack has batching asks, deadline digests and pre-answering from a taste model; the simple shape is a required "if no answer by X, I will do Y" field on every question, so blocked work becomes timed work. Assumption: asks currently block indefinitely.
  Done when: `fm ask` rejects a question without a default, and an unanswered one resolves to its default after the timeout in a test.

- **Re-read the brief after the third step, not just at the end** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: long tasks drift and compaction loses wording; a forced re-read of the original request text (not the summary) at fixed step fractions is cheap. Differs from rolling re-plans, which react to surprises rather than time.
  Done when: resume notes include the verbatim request at the 1/3 and 2/3 step marks, with a test that the text matches the brief byte for byte.

- **Wild: Let Foreman "sleep on" a stuck problem and return with a different framing** — FEATURE — value 3 — effort M — risk low — category: reasoning — wild
  Why: assumption: stuck tasks fail because context accumulates one framing. A pause that discards the working transcript and restarts from only the brief plus a list of "what is known false" might unstick it, like a fresh night's sleep.
  Done when: a blocked task can be retried in a clean context seeded only with brief and eliminated hypotheses, and bench compares its solve rate against plain retry.

- **Wild: Keep a "tell me I'm wrong" agent that only reads the claim, never the work** — FEATURE — value 3 — effort S — risk low — category: verification — wild
  Why: reviewers see the diff and inherit its framing. An agent given just the done summary and asked "what single observation would falsify this?" produces a check to run, which differs from claim-checkers that verify existing sentences.
  Done when: at done, the agent emits one falsifying probe, the main thread runs it, and the result is recorded in the evidence.

- **Wild: Play the task backwards as a children's "how did we get here" story** — FEATURE — value 2 — effort S — risk low — category: communication — wild
  Why: assumption: the user reads close-outs hastily. A three-sentence narrative ordered effect to cause ("the login no longer times out because X, which was caused by Y, which we found by Z") tests whether Foreman actually understands its own fix; a story that cannot be written flags a lucky fix.
  Done when: `fm task done` for FIX tasks requires a cause-chain of at least two linked sentences and rejects one that merely restates the symptom in a fixture.

- **Track which kinds of questions Foreman answers from memory instead of checking** — FEATURE — value 3 — effort M — risk low — category: epistemics
  Why: the pack has epistemic status tags and the knowledge-cutoff gap, but not a measurement of where recall substitutes for a lookup and is later wrong. Assumption: transcripts show claims about APIs, flags and file contents made without a tool call.
  Done when: a report lists claims in a session made without supporting reads and the share later contradicted, run on a sample transcript.
