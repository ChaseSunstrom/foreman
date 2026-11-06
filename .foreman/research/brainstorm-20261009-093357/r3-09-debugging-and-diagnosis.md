# Brainstorm — lens: debugging and diagnosis

- **Bisect the environment, not just the commit** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: existing ideas cover git bisect and "what changed since it worked" only as a wild item; fm friction shows gate flakiness (T-0424 slow-gate) and version skew, which are env-driven. assumption: many "regressions" are tool/dep/Claude Code version drift, not commits.
  Done when: given a gate that passes on a recorded env snapshot and fails now, `fm task bisect-env` names the single differing variable (tool version, env var, file, dep) in a fixture test.

- **Build a failure fingerprint index across tasks** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: fm recall is BM25 over briefs/lessons; failures are matched by text, not by normalized signature. assumption: stack traces/test names/exit codes can be normalized (strip paths, ids, timestamps).
  Done when: a test failure whose normalized signature matches a prior closed FIX surfaces that task's root cause and fix commit in the first debug step, verified on a replayed fixture.

- **Require a discriminating probe before each hypothesis is ranked** — FEATURE — value 4 — effort S — risk low — category: debugging
  Why: fm-debugger already ranks hypotheses with probes; prior ideas cover posterior/info-gain selection but not a hard rule that every hypothesis names an observation that would *refute* it. assumption: unrefutable hypotheses are the common cause of thrash.
  Done when: `fm task hypo` rejects a hypothesis lacking a refute-command, and the debugger output schema test fails without it.

- **Diagnose from the first divergence in a passing-vs-failing trace pair** — FEATURE — value 5 — effort L — risk med — category: debugging
  Why: prior ideas have runtime-trace grounding and time-travel bisect, but not automatic differential tracing of a known-good run vs the failing run to the first differing event. assumption: tests can be run with cheap tracing (sys.settrace / strace-lite) on both sides.
  Done when: on a seeded bug fixture, the tool outputs the first diverging call with arguments, and fm-debugger cites it as its top hypothesis.

- **Separate "symptom gone" from "cause removed" with a fix-removal probe** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: fm task prove does red→green, but a test can go green via a side effect of an unrelated edit. assumption: hunks can be individually reverted (ablation exists as an idea, but not tied to diagnosis).
  Done when: for a FIX done-gate, reverting only the claimed-root-cause hunk turns the repro red, and reverting every other hunk keeps it green; otherwise done is refused with the offending hunk list.

- **Keep a stuck-state classifier that picks the debugging mode** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: "3 failed attempts → block" is flat; prior ideas have a stuck ladder and thrash detection, but not a classification of *why* stuck (no repro, wrong layer, observer broken, misread spec, env). assumption: the ledger's edit/probe patterns separate these classes.
  Done when: on 5 replayed stuck transcripts, the classifier assigns the labelled class at ≥4/5 and routes to the matching action (e.g. "no repro" → minimise/record, "observer broken" → verify the probe itself).

- **Verify the instrument before trusting its reading** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: debugging.md covers condition-based waiting but a log line, grep, or print that never fires can be mistaken for "not reached". assumption: wrong-observer errors recur in friction logs.
  Done when: a debug step that adds a probe must show the probe firing on a known-positive input first; `fm task hypo` records "probe validated" and the test checks it.

- **Maintain a per-file "bug magnet" map for FIX priors** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: assumption: git history plus the closed FIX briefs show which files host repeated root causes; "root-cause priors per project" exists as an idea, but not file-level seeding of suspects with fix-churn and test-gap scoring.
  Done when: `fm map suspects <symptom text>` lists files ranked by past-fix count × low test coverage, and a fixture shows the true culprit in the top 3.

- **Auto-write the "why wasn't this caught" regression into the guard/gates** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: a prior idea demands the finding; none turns it into an artifact. Guard fuzzing (T-0433) and evals (T-0455) show appetite. assumption: most escapes map to a missing test, gate or lint.
  Done when: closing a FIX yields a proposed gate/test diff, and a replay shows that diff fails on the pre-fix commit.

- **Wild: Interrogate the bug as a witness cross-exam** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: wild. A cheap agent plays "the system", answering only from observed evidence (logs, traces); the debugger must phrase each question as a command, so unanswerable questions are visibly assumptions.
  Done when: a debug session transcript shows each hypothesis linked to a question whose answer is a recorded command output, with unbacked claims flagged.

- **Wild: Grow a synthetic twin of the bug for blind retesting** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: wild. After a fix, generate 3 sibling bugs of the same class in a scratch copy; a fresh agent running the fix-pattern from the lessons must solve them, scoring whether the diagnosis generalised rather than patched one instance.
  Done when: the fix lesson is stored only if a cold fm-debugger solves ≥2 of 3 generated siblings using it.

- **Wild: Keep a "crime scene" snapshot that freezes everything at first failure** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: wild. Attempts mutate state (files, caches, temp dirs, ports) and destroy evidence; a snapshot of tree, env, process list, and logs at first red lets later hypotheses be tested against the original scene.
  Done when: `fm task scene restore` reproduces the original failure after three subsequent edits, verified in a fixture.

- **Verify the diagnosis independently with a fresh agent's blind guess** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: fm second exists, but isn't tuned for root cause; assumption: agreement between an independent blind diagnosis and the chosen one is a cheap confidence signal.
  Done when: for FIX tasks of tier M+, a blind fm-debugger gets only symptom and repro, and disagreement with the chosen cause is recorded in the brief and blocks done until addressed.
