# Brainstorm — lens: deepen: verification

- **Compile every criterion into a Proof Contract** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the list has many separate ideas (typed claims, negative twins, executed-test counts, oath, failure-mode checklist, verifier selector). They are facets of one object. Assumption: criteria are currently free text plus a verify command. A contract holds the claim type, the verify command, a negative twin, a minimum executed-test count, known blind spots and an evidence expiry. `fm task done` refuses a criterion with no contract.
  Done when: a criterion lacking a twin or test count is rejected at plan time, and a fixture with a vacuous verify (`-k` matching zero tests, as in the T-0342 incident) fails the contract check.

- **Run a mutation-backed verify audit on each changed file** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: C101 (test the test suite) is queued, and the T-0342 verify that "ran no tests" shows green can be meaningless. Generalise it: at done, mutate only the diff's lines (flip an operator, delete a branch) and run the task's verify. If every mutant survives, the verify cannot see the change, so block with the surviving mutants listed.
  Done when: a task whose verify passes regardless of the diff gets blocked with named surviving mutants, and a well-tested diff passes.

- **Gate done on a historical catch-rate score** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "score verification by what it could have caught" and the verification-cost ledger are listed. Combine them using fm bench history. Replay each verify command against past real failures (the fm eval capture from T-0035) and keep a per-command catch rate. Low-scoring verifies (e.g. `grep -q`, `python -c import`) are flagged and the plan must add a stronger one. Spend verification effort by risk × catch-gap.
  Done when: `fm verify score <cmd>` prints a catch rate from at least 5 recorded failures, and plan review cites it for a weak verify.

- **Split the close-out into a claims ledger with evidence pointers** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "checked vs inferred" and "type every claim" are one mechanism. Each sentence of a close-out is tagged observed (linked to a ledger run id), inferred (names the premise) or assumed (re-check command, per C052). The done gate reads the tags, and a claim of "all", "never" or "fixed" with no observed link is bounced. The user's rule is "evidence before claims", and this enforces it mechanically.
  Done when: a close-out saying "all callers updated" with no enumeration run is rejected, and the same close-out with a grep-count evidence id is accepted.

- **Prove the diagnosis with a fix-removal and blind-guess pair** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: fix-removal probes and fresh-agent blind guesses are listed separately. Run them together for FIX tasks. First revert only the fix hunk and confirm the red test returns, so the symptom was caused by that hunk. Then give a tool-less fm-debugger the symptom and the test only, and compare its top hypothesis with the claimed root cause. A disagreement blocks done and opens a "diagnosis disputed" note. The existing fm task prove is red→green only.
  Done when: a FIX whose fix hunk is irrelevant to the red test (the test goes green with the hunk reverted) is blocked as "cause not removed".

- **Re-verify automatically when evidence inputs change** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "age evidence" and the edit-time sentinel (T-0214) fit together. Each piece of evidence stores a hash of the files, test files and tool version it depends on, taken from fm map test links. Sentinel or night marks evidence stale when an input changes and reruns just those verifies. Finished tasks whose proof went stale are surfaced in fm friction.
  Done when: editing a file linked to a closed task's verify marks that task's evidence stale, and `fm sentinel` reruns it and records the result.

- **Make interpretation-splitting checks part of the oracle** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: fm oracle already produces ambiguities, and "require a check that tells interpretations apart" is listed. For each ambiguity with 2 or more readings, generate a probe whose result differs between readings and attach it to the brief. If no such probe exists, the ambiguity goes to the user, not to a guess. Assumption: oracle output is structured enough to extend.
  Done when: a brief with a flagged ambiguity cannot enter execution until it has a discriminating probe or a recorded user answer.

- **Rehearse the verdict with an adversarial verifier panel** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: cross-validating verifiers and detecting the wrong layer are listed. At L tier, three tool-less claude -p children get only the criteria, the diff stat and the evidence. One argues "this is not done", one lists what the evidence cannot show, and one maps each criterion to the layer tested (unit, integration, user-visible). Disagreement above a threshold forces one extra real check. Cost is bounded because only L tier gets the panel.
  Done when: a seeded case where unit tests pass but the user-visible path is broken is flagged "wrong layer" by the panel.

- **Run perturbed double verification** — PERFORMANCE — value 3 — effort S — risk low — category: verification
  Why: "verify across a perturbed second run" and the flaky-gate signal from T-0424 point at the same gap. Rerun the verify with shuffled test order, a changed TZ, a fresh temp HOME and a cold cache. A pass in one run and a fail in another marks the evidence "fragile", not "passed". This is cheap because it is a second invocation of an existing command.
  Done when: a test depending on order passes the plain run, fails the shuffled one, and the task is marked fragile in the ledger.

- **Wild: Hire a "future you" saboteur to break the shipped change** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: wild. After a task is merged in a scratch worktree, a read-only agent has one goal: produce an input, config or sequence that makes the new behaviour fail, with a runnable repro. A repro that works becomes a regression test candidate and reopens the task. A found break is the strongest evidence the verify missed something, and an empty result with the attempts logged is real evidence of robustness.
  Done when: a seeded off-by-one in a merged diff is found by the saboteur, which emits a failing repro.

- **Wild: Keep a verification flight recorder that can replay the proof** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: wild. Capture commands, outputs, env, tool versions and file hashes for each verify into one replayable bundle (`fm proof replay T-xxxx`). A reviewer, a later session or the user can re-run exactly what was claimed months later. This also feeds eval capture (T-0035) and the stale-evidence mechanism.
  Done when: `fm proof replay` reproduces a finished task's verify output byte-for-byte, or reports exactly which input drifted.

- **Wild: Bet the verify against a pre-registered failure prediction** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: wild. Before building, the planner writes "the most likely way this ships broken is X" and "the verify would/would not catch it". After done, any user steer or reopened task is scored against that prediction. Over time the miss rate calibrates how much the planner's confidence about verification can be trusted, and feeds the lesson-confidence work in T-0217.
  Done when: fm friction shows per-tier prediction hit rates computed from at least 10 tasks.

- **Verify the user's intent with a one-glance acceptance artifact** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "rehearse the user's acceptance glance" and "done looks like snippet" combine. Each brief gets a 5-line artifact (a command output, screenshot path or diff) that shows the user at a glance that the request was met. It is written before the build and compared with the real one after, and a mismatch is a visible discrepancy in the close-out. This follows the user's repeated complaint that work is claimed but not seen (cleanup never done).
  Done when: a close-out shows the predicted and actual artifacts side by side, and a mismatch blocks done until explained.
