# Brainstorm — lens: deepen: debugging

- **Run a debugging case file that unifies hypotheses, probes and evidence** — FEATURE — value 5 — effort M — risk low — category: debugging
  Why: the list has a tournament, a posterior, a differential table, a frontier and a crime-scene snapshot as separate ideas, and today only `fm task hypo` and fm-debugger's ranked list exist. Combine them into one `case.json` per FIX task: symptom, hypotheses with prior, probes with cost and which hypotheses each splits, observations, eliminations. Every attempt and probe appends to it, and fm-debugger and the main thread both read and write it.
  Done when: `fm task case show T-x` prints hypotheses with posterior, eliminated ones with the evidence that killed them, and the next probe chosen by split-per-cost; a test replays a fixture of three probes and checks the ranking changes.

- **Replace the 3-attempt block with an escalation ladder that changes mode** — FEATURE — value 5 — effort M — risk med — category: debugging
  Why: today "3 failed attempts → block with diagnosis" treats a wrong hypothesis, a wrong instrument and a wrong problem framing the same way. The ladder is: attempt 1–2 is the normal loop; the stuck-state classifier then picks one of reset (list what is now known), instrument check, widen the frame (fm second plus fm-recon on neighbouring code), or lateral squad. Block only after the ladder ends, and the block carries the case file.
  Done when: a simulated stuck FIX task moves through at least two distinct ladder modes before it blocks, each recorded in the ledger, and the block message includes the case-file summary.

- **Classify the stuck state from the attempt history** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: assumption: attempt records hold the command, output and diff. Cheap signals tell the stuck states apart: the same edit retried means a fixation loop, a changing failure message means progress on a different layer, an unchanged output after an edit means the edit isn't reaching the code (stale build, wrong file), and a flaky pass means timing. Each state maps to a ladder rung.
  Done when: fixtures for four stuck patterns each classify correctly, and `fm task stuck T-x` names the state with the evidence it used.

- **Verify the instrument before trusting a probe's reading** — FEATURE — value 4 — effort S — risk low — category: debugging
  Why: the category already has this idea twice, so make it a required case-file step. Before a probe's result may eliminate a hypothesis, run a known-positive control (the probe against a case where the answer is known). It catches the repro test that can't fail, the log line that never prints and the stale cache.
  Done when: a probe recorded without a control is marked "uncontrolled", and an uncontrolled result cannot eliminate a hypothesis in `fm task case`.

- **Prove the diagnosis with fix-removal and fix-isolation runs** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: `fm task prove` does red→green. Extend it to a causal check at done: revert only the fix hunk and confirm the repro goes red again, then apply only that hunk to a clean checkout and confirm green. This catches the fix that works because of an unrelated edit, and the repro that was never tied to the bug.
  Done when: `fm task prove --causal` fails on a fixture where the fix hunk isn't what turned the test green.

- **Turn every FIX into a "why wasn't this caught" action with an owner** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: merge the "demand why nothing caught this" and "auto-write the regression into gates" ideas into one finish step. A FIX can't be marked done without one of: a new test, a new gate or guard rule, a lesson, or a recorded "unfixable gap" with a reason. The check reads which of those the diff actually contains.
  Done when: finishing a FIX with none of the four is refused, and each of the four paths is accepted in tests.

- **Build the failure fingerprint index and use it across projects** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: fm recall is BM25 over briefs and lessons, which is weak for stack traces. Normalise error text (strip paths, ids and line numbers), hash it, and store fingerprint → root cause → fix commit. On any red gate, look up the fingerprint first and suggest "seen before in T-0212, root cause X". It builds on T-0435, which reads friction across projects.
  Done when: a fixture failure whose paths differ still hits the earlier task's root cause, and the hit appears in the debug note shown to the agent.

- **Bisect across commits, config and environment in one search** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: the category has "bisect the environment", and plain git bisect only covers commits. Treat the commit, lockfile, tool version, env vars and Python version as an axis list, run the repro in throwaway worktrees and temp HOMEs, and bisect the axes in turn (delta-debugging style) to name the smallest difference between a passing and a failing world.
  Done when: on a fixture where only a dependency version flips the result, `fm bisect` names that dependency, not a commit.

- **Diagnose from the first divergence between a passing trace and a failing trace** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: it fits the trace-pair idea and the predicted-vs-traced call-path idea, which can share one tool. Run the repro against the last green commit and the failing one with a lightweight tracer (`sys.settrace` or `-X importtime` for Python, wrapped output for shell), align the two traces, and report the first differing call with its arguments.
  Done when: a fixture with a changed branch condition reports the correct function and line as the first divergence.

- **Wild: Hold a cross-examination of the bug, where one agent plays the bug and another the investigator** — FEATURE — value 3 — effort M — risk med — category: debugging
  Why: wild. The "bug as witness" idea made concrete. A tool-less child is given only the symptom and the case file and must answer as the bug would ("I only appear when X; I do not appear when Y"), and a second child tries to catch contradictions with the evidence. Contradictions become new probes. It surfaces hypotheses the investigator's own framing hides.
  Done when: running it on a past solved FIX from `fm bench` produces at least one probe that matches the real root cause's discriminating condition.

- **Wild: Grow a synthetic twin of the bug and test fixes on it blind** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: wild. Have fm-builder produce a minimal standalone reproduction (the twin) in a scratch worktree without seeing the proposed fix, then apply the fix to it. A fix that works on the real code but not on the twin, or the reverse, indicates the diagnosis is partial. The twin also becomes the regression test and a bench eval.
  Done when: for a fixture bug, the twin reproduces the failure in under 5 seconds with no imports from the project.

- **Wild: Freeze a crime-scene snapshot at first failure and let later agents replay it** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: wild. At the first red result, capture git state, diff, env, command output, tool versions and the relevant log tail into a content-addressed bundle. fm-debugger then works from the frozen bundle, not the moving worktree, so its probes can't be confused by the builder's later edits, and `fm task case replay` recreates the scene.
  Done when: after the worktree is changed, `fm task case replay T-x` reproduces the original failing output byte for byte (minus timestamps).

- **Wild: Run an adversarial "debug duel" where two debuggers must commit to different root causes** — FEATURE — value 3 — effort M — risk med — category: debugging
  Why: wild. This combines the tournament with fm second's debate. Two read-only fm-debugger runs get opposite assignments ("assume the cause is in the data, assume it's in the code path") and each must name the one probe that would falsify the other. The main thread runs the cheaper probe and the loser's hypothesis is eliminated with recorded evidence, which avoids anchoring on the first plausible cause.
  Done when: on a fixture bug with two plausible causes, the duel runs exactly one probe and eliminates the wrong hypothesis in the case file.

- **Learn root-cause priors from finished FIX tasks and feed them back into case files** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: this merges the per-project priors and the bug-magnet map. At finish, record the root-cause class (off-by-one, stale cache, env, race, wrong assumption about input, etc.) and the files touched. The case file's initial priors come from these counts per project and per file, and a bench replay checks whether the priors raised the first-hypothesis hit rate. Assumption: root-cause class can be tagged at finish by a short required field.
  Done when: after a fixture history of five finished FIXes, a new FIX on a file with a prior history ranks the historically common cause first, and `fm bench` reports the hit rate with and without priors.
