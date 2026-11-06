# Brainstorm — lens: verification reasoning

- **Pair each criterion with a negative twin** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the pile has "reject vacuous proof" and "mutation proof", but nothing that makes every acceptance criterion ship with its own *must-fail* input (a fixture where the verify command is expected to go red). The T-0342 note, where a `-k a or b` verify ran no tests, is the evidence: a verify that can't fail went unnoticed.
  Done when: `fm task criterion add` refuses a criterion lacking a twin, and a unit test shows a verify that exits 0 on the twin input is rejected.

- **Count tests actually executed by each verify** — FIX — value 5 — effort S — risk low — category: verification
  Why: T-0342 (a verify ran zero tests and passed) is a concrete failure. Parse the runner's output (collected/ran counts) and treat "0 ran" as not-evaluated, not pass. Assumption: pytest-style and run.py output are the common runners.
  Done when: a criterion whose verify runs zero tests records "not evaluated" and blocks `fm task done`, covered by a test using the `-k a or b` case.

- **Verify the verifier's selector against the diff** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: a verify can run real tests that never touch the changed code. The test→source map in `fm map` already exists. Check that at least one test in the verify's run is linked to a file in the diff, and flag "ran, but unrelated".
  Done when: a task whose diff touches `fmguard.py` and whose verify runs only `test_bench.py` gets an "unrelated evidence" warning at done.

- **Record a verification oath before the build** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: the brief has acceptance criteria but no commitment to what *would convince the main thread it's wrong*. Add a one-line "I would be wrong if…" per criterion, written at plan time, and check at done that each was tested. Assumption: it fits into the existing brief schema.
  Done when: a FEATURE M/L brief lacking oaths fails the plan gate, and done lists each oath with the evidence that addressed it.

- **Score verification by what it could have caught historically** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "score each gate by what it alone catches" exists, but not per verify *pattern* (grep-only, exit-code-only, snapshot, behavioural). Mine the bench and ledger for escapes and rank patterns by miss rate, then warn when a task relies on a weak pattern alone.
  Done when: `fm friction` prints a table of verify patterns with escape rates, and a grep-only criterion triggers a prompt to add a behavioural check.

- **Verify across a perturbed second run** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: single-run passes hide order, time and environment dependence. Rerun the final verify once under a shuffled test order, a different TZ and an empty cache, and compare outcomes. Assumption: the gates are cheap enough to run twice.
  Done when: a gate that passes normally but fails under shuffled order is flagged as order-dependent at done.

- **Separate "I checked" from "I inferred" in close-outs** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: close-outs mix observed and inferred claims. Require each sentence in the summary to carry a tag (ran / read / inferred), with "ran" requiring a ledger event id, and block "ran" tags with no matching event.
  Done when: a close-out claiming "tests pass" without a matching recorded run is rejected by the done gate.

- **Replay the verify against an intentionally broken sibling** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: the pile mentions mutation and red-first, but not mutating *the neighbouring behaviour* a change might regress. Generate sibling mutants (callers of the changed function) and require that some gate fails for each, which reveals blind spots outside the diff.
  Done when: for a changed function with three callers, the report lists which caller mutants were killed and which survived.

- **Wild: Hold a "verification heist" where a red-team agent forges a pass** — FEATURE — value 4 — effort L — risk med — category: adversarial verify
  Why: wild. Instead of finding bugs, the agent's goal is to make the done gate say yes with a *wrong* change (hardcode outputs, weaken asserts, stub the check). Each successful forgery becomes a new rule against the gates.
  Done when: a seeded wrong change is forged past an old gate in a test, and the post-fix gate rejects the forgery.

- **Wild: Print a "proof receipt" users can verify without Foreman** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: wild. Each done emits a standalone shell script that reruns the exact verify commands on a clean checkout of the tree hash and prints match/mismatch. Anyone, including the user a month later, can re-check without trusting the ledger.
  Done when: running the generated script on a fresh clone reproduces the recorded exit codes for a sample task.

- **Wild: Keep a "lie detector" cheap model that reads only the close-out and the diff stat** — FEATURE — value 3 — effort S — risk low — category: verification
  Why: wild. A Haiku-level scout with no repo access guesses what was claimed versus what the diff stat could plausibly support (e.g. "fixed login timeout" with only docs touched). Disagreement is a flag, not a block.
  Done when: a seeded close-out claiming a code fix over a README-only diff is flagged.

- **Check claims against what the user would observe** — FEATURE — value 4 — effort M — risk med — category: acceptance
  Why: the user's recurring complaint (cleanup never done, bug feedback relayed) suggests criteria pass while the user's actual view doesn't change. For each criterion, require a "what the user sees" line and run the cheapest observation (CLI output, screenshot) as evidence.
  Done when: a task closes with a captured observation for each user-visible criterion, and a missing one blocks done.

- **Age evidence and re-verify when its inputs change** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: evidence "bound to the tree" is in the pile as a tree hash, but not partial staleness: a later task touching a file the earlier proof read should mark that proof stale and queue a cheap rerun at night.
  Done when: editing a file read by a closed task's verify marks that task "evidence stale" and `fm night` reruns its verify.
