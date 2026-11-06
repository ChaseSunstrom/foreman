# Brainstorm — lens: reasoning and thought process

- **Track what Foreman actually saw** — FEATURE — value 4 — effort M — risk low — category: epistemics
  Why: assumption: hooks see each tool result, including truncation (`head`, paged reads, capped output). Absence and exhaustiveness claims ("only caller", "no other uses") are only as good as the output behind them. The T-0342 `-k` incident, where tests silently ran nothing, is the same bug class.
  Done when: in a fixture, a "no other uses" claim made after a truncated grep gets a note citing the truncation, and the same claim after a full grep gets none.

- **Escalate patch trains to a design pass** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: recent commits show a train of guard fixes (T-0414/0421/0422, the `bash -lc` cluster fix), each correct locally. Nothing asks "what is the class, and what is the structural fix?" after the third patch in one area.
  Done when: a third fix to the same module within N tasks makes `fm task new` require a class-of-bug line and a design-or-defer decision before it proceeds.

- **Rank assumptions by plan sensitivity and bind them to steps** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: briefs carry assumptions with confidence, but nothing links an assumption to the steps that depend on it. For each assumption, ask cheaply "if false, which steps change?". Probe the high-impact, cheap-to-test ones first.
  Done when: `fm task assume --affects S2,S4` exists, and falsifying that assumption marks only S2 and S4 stale, with a test.

- **Settle disagreements between code, tests, docs and brief with a verdict** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: the MASTER.md drift tasks and the "working as intended" drop show artifacts disagreeing often. Today Foreman silently picks one. Instead it should record which artifact is authoritative for this fact, and why.
  Done when: in a fixture where the doc says X and the code does Y, the case file holds a verdict (doc stale, code bug or test wrong) with evidence, before any edit.

- **Name the hidden trade-off at intake** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: assumption: requests like "make it fast", "keep it fresh" and "don't ask me" hide tensions (cache vs fresh, speed vs safety, autonomy vs oversight). The pile covers explicit contradictions, not implied ones. Use a small tension table, and record the chosen side as a decision.
  Done when: an intake fixture containing "always fresh" and "make it faster" yields a brief line naming the tension and the chosen side.

- **Diff the predicted call path against the traced one** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: FIX tasks rank hypotheses, but nothing tests Foreman's mental model of the code. Before diagnosing, it writes the path it expects the symptom to take, then compares it to a runtime trace or hook log. The first divergence is where its understanding is wrong.
  Done when: a FIX fixture with a planted surprise (a callback that skips the expected function) reports the divergence point from the predicted vs traced path.

- **Prove "unused" across dynamic references before deleting** — FEATURE — value 4 — effort M — risk low — category: cleanup
  Why: the user's steer says cleanup requests never got done. Deleting is risky partly because Foreman's skills, hooks and commands are referenced by string from manifests, JSON and md. A sweep over names built from strings, `getattr`, manifests, docs, tests and other projects would make deletion safe enough to do.
  Done when: a fixture function referenced only through a manifest string is flagged as used, and a truly dead one gets a recorded proof listing the sweeps run.

- **Blame a red criterion three ways before editing** — FIX — value 3 — effort S — risk low — category: verification
  Why: T-0342's criterion had a verify command that ran no tests. A red check can mean the product is wrong, the criterion is wrong, or the verify command is wrong, and Foreman currently assumes the first.
  Done when: a red check requires a one-line blame verdict (product, criterion or command) with a probe, and a test shows a no-op verify classed as "command".

- **Require a re-representation before the third attempt** — FEATURE — value 3 — effort S — risk low — category: stuck-handling
  Why: the stuck rule is three failed attempts, then block. Before the third, force a change of representation (state table, timeline, dataflow, truth table) written as an artifact. Often the bug is visible once the problem is drawn differently.
  Done when: after two failed attempts, `fm task` refuses a third without a representation note attached to the hypothesis.

- **Keep a units-and-frames register for each task** — FEATURE — value 3 — effort S — risk low — category: reasoning
  Why: the canonical example, "login times out on slow wifi", is a timeout bug. The same class shows up in hook SLOs, heartbeats, and pace limits. Each quantity gets a unit, a source and a frame (ms vs s, UTC vs local, relative vs absolute path). The review lens then checks seams.
  Done when: a fixture diff mixing seconds and milliseconds across a seam is flagged by the register check.

- **Add a Fermi check to performance and size claims** — FEATURE — value 3 — effort S — risk low — category: estimation
  Why: slow-gate and hook-latency work (T-0424, `bench_hooks`) rests on measurements. A pre-measurement order-of-magnitude guess, compared with the result, exposes a misunderstanding when they differ by more than 10x.
  Done when: a performance brief carries an expected-magnitude line, and `fm task prove` prints the ratio and flags a >10x mismatch.

- **Hire a genie to hunt loopholes in the criteria** — FEATURE — value 4 — effort M — risk low — category: intake — wild
  Why: wild. Before building, a no-tools agent is told to satisfy every acceptance criterion with the laziest malicious-compliance implementation it can imagine. Each loophole it finds becomes a tightened criterion.
  Done when: on a fixture brief with a known loophole (a verify that passes on an empty output), the genie reports it and a criterion is added.

- **Find the pivot belief behind every failure** — FEATURE — value 4 — effort M — risk med — category: learning — wild
  Why: wild. The pile has counterfactual replay of passes and agents, but not of beliefs. For a blocked or reworked task, flip each recorded belief or assumption in turn, replay cheaply, and name the one whose flip changes the outcome. A pivot-belief ledger shows which kinds of beliefs Foreman gets wrong.
  Done when: on a recorded failure with a planted wrong assumption, the analysis names that assumption as pivotal.

- **Deal a dumb-question card at each phase change** — FEATURE — value 3 — effort S — risk low — category: reasoning — wild
  Why: wild. Foreman's costliest misses are basic ones: did it run at all, what's the actual unit, did it read the real error. A rotating deck of Feynman-style beginner questions is drawn at plan→execute and execute→verify, and each is answered with a probe. Every escape adds a card.
  Done when: crossing a phase boundary prints one card, and answering it records a probe result in the ledger.
