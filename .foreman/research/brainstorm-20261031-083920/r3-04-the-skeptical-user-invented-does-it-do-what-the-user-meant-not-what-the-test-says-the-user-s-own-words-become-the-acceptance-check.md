# Brainstorm — lens: the skeptical user (invented): does it do what the user meant, not what the test says; the user's own words become the acceptance check

- **Quote the ask beside every green** — FEATURE — value 5 — effort S — risk low — category: meant-it
  Why: the earlier ideas ("Quote the ask's nouns in the diff evidence", "Compile each user ask into a meant-it check") stay design; the pack's asks (T-2285: a plan gate that counted `(1) --bench …` wrongly) show a green gate with the user's words nowhere near it. Show the user's verbatim sentence next to each criterion's evidence in `fm task finish`.
  Done when: finishing a task prints the original ask line above its evidence, and a test fails if a criterion row lacks a linked quote.

- **Fail the clause no test names** — FEATURE — value 5 — effort M — risk med — category: meant-it
  Why: T-2285, T-2289 and T-2327 each hid a clause (flag-first options, scratch folder, the "(2)…" steer) that a passing suite missed. Split the ask into clauses; each must map to a criterion or to a stated "not checked".
  Done when: a task with an ask of 3 clauses and 2 criteria cannot close until the third is mapped or labelled unproven; fixture covers T-2327's two-part steer.

- **Let the user write the check in their words** — FEATURE — value 4 — effort M — risk med — category: acceptance
  Why: assumption: the skeptic trusts a line they typed more than a model's test. Support `fm task accept ID "when I run X I see Y"`, stored in a file the builder can't edit, run at finish.
  Done when: the accept line runs at close, a failure blocks, and a builder edit to the file is refused by the guard.

- **Replay the user's earlier correction as a regression** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the list of asks shows repeats of one class (plan gate misses, gate false positives). When the user corrects a result, store the failing input as a fixture that every later task of that area runs.
  Done when: a correction recorded with `fm correct` creates a test that fails on the old code, and appears in the next relevant task's verify set.

- **Show "what the user would see" for non-UI changes** — FEATURE — value 4 — effort M — risk low — category: behaviour
  Why: the unproven rollup counts UI changes with no shot, but CLI/refusal-text changes (T-2289's `fm lane rm`) have no equivalent. Capture the real command's before/after output on the start tree and the current tree.
  Done when: closing a task that changes a verb's output stores both transcripts and the receipt shows the diff.

- **Rate each close by whether the user reopened it** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: "asks the user had to make" (T-2285..T-2327) are follow-ups to closes; this is the only signal Foreman doesn't author. Link a follow-up task to the earlier one it corrects and compute a per-kind reopen rate.
  Done when: `fm task new --fixes T-NNNN` records the link and `fm triggers` shows reopen rate per proof kind.

- **Refuse a green whose test passes on the old tree** — FEATURE — value 4 — effort S — risk low — category: falsifier
  Why: `fm task prove` exists for red-first; make the finish gate require it for FIX tasks whose ask names a failure, with no override except a recorded user-only accept.
  Done when: a FIX with a test that passes pre-change cannot close, tested with a fixture.

- **Show the diff nobody asked for** — FEATURE — value 3 — effort M — risk med — category: scope
  Why: assumption: skeptics fear extras (T-2289 widened to a throwaway-treatment rule). List changed behaviours with no clause in the ask.
  Done when: the finish receipt has an "unrequested" section, empty or listed, from a model pass judged by a different model.

- **Make "what I meant" editable after the fact** — FEATURE — value 3 — effort S — risk low — category: intent
  Why: the ask's wording is the contract, but the user clarifies mid-task. Allow `fm task meant ID "…"` to append a dated clarification that becomes a new criterion.
  Done when: appending creates a criterion that blocks close until evidenced.

- **Wild: Hire a literal-minded intern** — FEATURE — value 3 — effort M — risk med — category: adversarial
  Why: wild. A tool-less child that sees only the ask and the final user-facing output and says what it would assume works; mismatches against what the ask implies are listed.
  Done when: the intern's verdict is recorded and a planted mismatch fixture is caught.

- **Wild: Play the ask back as a one-line demo command** — FEATURE — value 4 — effort M — risk med — category: demo
  Why: wild. At close, print one command the user can paste to see the behaviour themselves, derived from the ask, so trust doesn't rest on the transcript.
  Done when: every closed FEATURE has a runnable demo line that exits 0 on the new tree and non-zero on the start tree.

- **Wild: Score the builder on literalness** — FEATURE — value 2 — effort L — risk med — category: calibration
  Why: wild. Replay past asks against past closes with a cold reader to estimate how often "passed" meant "not what they said"; show the rate beside the held rate.
  Done when: a literalness percentage appears in `fm exam scorecard` with its denominator.

- **Keep a skeptic's glossary** — FEATURE — value 3 — effort S — risk low — category: vocabulary
  Why: assumption: terms like "unproven", "proven", "held" mean different things to builder and user. Bind each word the user uses to a definition and a command.
  Done when: `fm glossary` lists terms with the command that produces each, and a doc-vs-code check fails on an unlisted term.

Next question: When the user's correction contradicts a criterion the builder already evidenced, which record wins and does the user see the clash?
Next question: Which of the user's asks were phrased as a symptom rather than a request, and does the plan restate the symptom as the thing to disappear?
