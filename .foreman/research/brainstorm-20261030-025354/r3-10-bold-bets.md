# Brainstorm — lens: bold bets

- **Make the model the hunter and the failing test the only admission ticket** — FEATURE — value 5 — effort L — risk med — category: initiative core
  Why: exam run s0-001 shows deterministic finders (fmdocs.scan + fmsecrets) found 0 of 108 planted defects while plain Claude found 3/3 held-out bugs at ~0.17 USD. Assumption: a per-file read-only model pass ("what input breaks this?") plus a one-file reproduction beats regex probes on `bug` and `none` kinds.
  Done when: on a never-seen exam repo with 3 planted bugs, `fm find` outputs ≥2 findings, each with a test that fails on the untouched tree and passes after its fix lane, and the 108-defect exam recall is above 0.

- **Ship "clean" as a scored verdict with an inspected-ground receipt** — FEATURE — value 5 — effort M — risk low — category: none-kind
  Why: Mission 3 is graded on the exam's `none` kind; a hunter that always finds something fails it. Assumption: the tool currently has no way to say "nothing here" with evidence.
  Done when: running `fm find` on an exam `none` repo prints a verdict "clean" listing files read, tests run and probes tried, and files zero tasks.

- **Calibrate on planted canaries before trusting any result** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: the exam plants defects; the same trick in a scratch copy of the user's repo grades recall and false-positive rate per project before a real scan is believed. Assumption: mutation of a worktree copy is cheap.
  Done when: `fm find --calibrate` mutates N functions in a throwaway worktree, reports recall as a number, and the real repo's tree hash is unchanged.

- **Reject proofs that fail for the wrong reason** — FIX — value 4 — effort M — risk low — category: proof quality
  Why: "red" from an import error or missing fixture proves nothing. Assumption: current prove accepts any non-zero exit.
  Done when: a test failing on ImportError/collection error is refused with a typed verdict "harness", while an assertion failure naming the claimed symptom is accepted (unit test with both).

- **Run a cold refuter against each finding before it is ranked** — FEATURE — value 4 — effort M — risk med — category: precision
  Why: false positives cost the user attention and the exam's `none` score. Assumption: a second model seeing only the test and the code, not the finder's argument, can say "this is intended behavior".
  Done when: a seeded intended-behavior finding is dropped by the refuter while a real bug survives, in a fixture run.

- **Fold adopt, scout, deps and docs into one `fm find` pipeline with a resumable step** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: four partial one-shot entry points exist (fmeco adopt, fmscout, deps, docs) and the Genesis `step` pattern already gives resume-after-kill. Assumption: they can share one findings ledger.
  Done when: killing `fm find` mid-prove and rerunning resumes at that stage, and the old verbs print a pointer to `fm find`.

- **Keep Foreman's own setup failures out of user-project findings** — FIX — value 3 — effort S — risk low — category: noise
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks in user projects.
  Done when: with a broken Foreman hook in a fixture project, `fm find` files no task whose subject is Foreman itself.

- **Rank by value per dollar with the formula printed, weights learned from 30-day survival** — FEATURE — value 4 — effort M — risk med — category: ranking
  Why: the mission requires value ranking and `fm outcomes` already measures survival. Assumption: kind weights start fixed and drift with data.
  Done when: each finding shows `score = reach × proof strength ÷ est. cost` and a golden-file test pins the ordering for a fixed input.

- **Make a settled-findings ledger by fingerprint** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: dismissals recur and nightly runs would refile them; the user's habit is to drop items for good (see the dropped list).
  Done when: a dropped finding is not refiled on the next scan unless its files' hashes changed.

- **Reject fixes that pass by hardcoding the test's literal** — SECURITY — value 3 — effort M — risk med — category: fix integrity
  Why: a lane told "make this test pass" can cheat. Assumption: no such check exists.
  Done when: a fixture fix that special-cases the test input is rejected by a second varied-input run, and an honest fix passes.

- **Wild: a morning card of proven findings, one key to land or drop** — FEATURE — value 4 — effort M — risk low — category: delight (wild)
  Why: night queue exists (`fm night`); assumption: the user wants to wake to merge-ready lanes, not a list of hunches.
  Done when: after a night shift, `fm morning` shows one line per proven finding with its score and test name, and `l`/`d` lands or drops it.

- **Wild: a prosecutor and a defender model argue each finding; a judge sees only the test** — FEATURE — value 3 — effort L — risk med — category: precision (wild)
  Why: single-model hunters over-report; adversarial framing targets the `none` kind. Assumption: cost stays under the 0.17 USD plain-Claude baseline per finding.
  Done when: on 10 mixed fixtures, precision with the trial exceeds precision without it at ≤ equal cost.

- **Wild: pit the night shift against plain Claude on the user's own repo and publish the head-to-head** — FEATURE — value 3 — effort L — risk med — category: honesty (wild)
  Why: the critique says Foreman costs more for the same score; the user's standing steer is outside-signal weakness finding.
  Done when: `fm find --duel` prints both arms' proven findings, cost and time on one page.

Next question: Which stacks in the held-out exam have no runnable single-test command, and what does Foreman say there instead of guessing?
Next question: Does a finding's proof strength predict 30-day survival at all, or is the ranking formula untested decoration?
