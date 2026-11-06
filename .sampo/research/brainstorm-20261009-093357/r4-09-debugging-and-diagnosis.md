# Brainstorm — lens: debugging and diagnosis

- **Keep a hypothesis tournament with elimination evidence** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: fm-debugger returns ranked hypotheses with probes, and `fm task hypo` exists, but nothing stores which hypotheses were eliminated and by what observation; after 3 failed attempts the block carries a diagnosis, not a map of what's ruled out. Assumption: hypotheses live as free text today.
  Done when: `fm task hypo` records each hypothesis with status (open/eliminated/confirmed) and the eliminating probe output, and a retry's prompt lists eliminated ones so a test shows they aren't re-proposed.

- **Replace the flat 3-attempt block with a diagnosis ladder** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: "3 failed attempts → block with diagnosis" is the only escalation. Attempt 1: fix directly; 2: forced fm-debugger with a discriminating probe; 3: reproduce-minimal + instrument-first; only then block. Assumption: the ladder is not already in debugging.md (the "stuck ladder" idea is listed, but not as rung-specific tooling).
  Done when: a scripted failing task transitions through three distinct recorded rungs, each with a different required artifact, before reaching blocked.

- **Pick the next probe by hypothesis split** — FEATURE — value 4 — effort M — risk low — category: diagnosis
  Why: ranked hypotheses are ordered by likelihood, but cheap probes that split the set in half beat testing the favourite. Go beyond "rank by cost-to-test": compute, for each candidate probe, which hypotheses it would separate, and run the best splitter first. Assumption: hypotheses can declare predicted outcomes per probe.
  Done when: given 4 hypotheses with predicted probe outcomes, `fm task hypo next` selects the probe that partitions them most evenly, and a unit test asserts it.

- **Prove the diagnosis, not just the fix, with a fix-removal probe** — FIX — value 5 — effort S — risk low — category: debugging
  Why: `fm task prove` goes red→green, but a green can come from an unrelated change or a flake. Adding "revert only the claimed causal hunk and confirm red returns" separates "symptom gone" from "cause removed". Assumption: hunks can be reverted in a worktree.
  Done when: a FIX can't close until a recorded run shows the test red with the causal hunk reverted, and a test with a coincidental fix is refused.

- **Diagnose from the first divergence between passing and failing traces** — FEATURE — value 4 — effort M — risk med — category: diagnosis
  Why: bench/replay and the ledger already record command sequences; a failure on one machine, version or commit and a pass on another are rarely diffed structurally. Align the two event/log streams and report the first differing step. Assumption: gates emit enough structured output to align.
  Done when: `fm diverge <good-run> <bad-run>` prints the first differing event with surrounding context on a fixture pair.

- **Classify the failure before touching code** — FEATURE — value 4 — effort S — risk low — category: diagnosis
  Why: the same "3 failed attempts" treatment is applied to flaky, environmental, test-bug and genuine-code failures. A cheap classifier (rerun N times, check the environment, compare to baseline-red gates) routes to the right playbook. Assumption: baseline-red recording and rerun statistics aren't wired into FIX intake.
  Done when: a FIX intake on a flaky fixture reports class=flaky with rerun counts and does not start an edit step.

- **Keep a symptom-to-cause casebook queried at intake** — FEATURE — value 3 — effort M — risk low — category: diagnosis
  Why: fm recall is BM25 over briefs and lessons, but fixed FIX tasks hold structured pairs (symptom text, confirmed root cause, location, discriminating probe) that could seed hypotheses for a new report. Assumption: finished FIX briefs record root cause in a parseable field.
  Done when: a new FIX with a symptom resembling a closed one shows the earlier root cause as a ranked starting hypothesis in its brief.

- **Demand "why didn't anything catch this" on every FIX** — FEATURE — value 4 — effort S — risk low — category: debugging
  Why: regression-test.md covers the test, but not asking which gate, lens, or lesson should have caught it. The answer feeds fm friction as a gap. Assumption: not already a done-gate item.
  Done when: closing a FIX without a non-empty escape analysis field is refused, and the field shows in fm friction.

- **Verify the instrument before trusting its reading** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: debugging.md leans on probes, but a probe that can't produce the opposite result gives false elimination. Run each probe once against a known-good state to show it can read both ways. Assumption: probes are commands recorded by hypo.
  Done when: eliminating a hypothesis requires its probe to have a recorded control run with the opposite outcome.

- **Bisect the environment, not just the commit** — FEATURE — value 3 — effort M — risk med — category: diagnosis
  Why: "works on my machine" failures like the slow-wifi login timeout, the Arch dependency block (T-0325), and hook import time depend on versions, env vars and config. Delta-debug between two environment snapshots (tool versions, env, settings). Assumption: a snapshot can be captured cheaply.
  Done when: `fm envdiff` between two captured snapshots lists differing versions/vars, and a bisect narrows a seeded difference to one item.

- **Wild: Hold a crime-scene freeze at first failure** — FEATURE — value 3 — effort M — risk low — category: debugging — wild
  Why: assumption: later attempts overwrite evidence (logs, tmp files, process state). Snapshot tree, env, logs and process list at the first red so every later hypothesis is tested against the original scene.
  Done when: first failure writes a read-only scene bundle and `fm task scene` reopens it after the tree has changed.

- **Wild: Cross-examine the bug as a witness** — FEATURE — value 3 — effort M — risk low — category: diagnosis — wild
  Why: assumption: reporters and logs hold contradictions. A tool-less agent lists every claim in the report and log ("it always fails", "after update") and generates the questions whose answers would contradict each, which become probes.
  Done when: a FIX with a pasted report yields a table of claims, each paired with a runnable check.

- **Wild: Grow a synthetic twin of the bug for a blind retest** — FEATURE — value 3 — effort L — risk med — category: debugging — wild
  Why: assumption: fixes often overfit the original repro. A fresh agent builds a different-looking minimal reproduction of the same stated cause, and the fix must pass it too.
  Done when: a fix is run against a generated variant repro and the result is recorded in the evidence.

- **Wild: Run a misdiagnosis post-mortem when the second theory wins** — FEATURE — value 3 — effort S — risk low — category: debugging — wild
  Why: assumption: when the leading hypothesis is eliminated, why it looked plausible is never recorded. Capturing the misleading evidence trains the ranking and feeds lessons.
  Done when: a task where the top-ranked hypothesis was eliminated records a "why it misled" note that fm recall can retrieve.
