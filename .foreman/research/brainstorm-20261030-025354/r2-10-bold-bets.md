# Brainstorm — lens: bold bets

- **Make the failing test the only finding** — FEATURE — value 5 — effort L — risk med — category: initiative core
  Why: exam s0-001 scored the deterministic finders 0/108 while plain Claude fixes 3/3 at ~0.17 USD. Mission 3 is graded on `none` and `bug` kinds in never-seen repos.
  Done when: on 5 held-out repos, `fm find` prints only findings that carry a test that is red on the untouched tree, and the red-to-green pair reruns with one command.

- **Replace the finders with a read-only hunter that must attach a repro** — FEATURE — value 5 — effort L — risk med — category: finders
  Why: fmdocs.scan and fmsecrets match patterns and miss logic bugs in js, ts, ruby, rust and c. A headless model reads a hot cluster with a bug-shaped question, and a finding with no repro is dropped.
  Done when: on exam `bug` scenarios in a language Foreman has no probe for, recall beats the 0 baseline and every shown finding has a repro file.

- **Return "clean" as a scored verdict with evidence** — FEATURE — value 5 — effort M — risk low — category: none kind
  Why: the exam includes a `none` kind and the finders have no clean result. Assumption: today an empty scan is indistinguishable from a broken one.
  Done when: on 3 planted-clean repos, `fm find` exits 0 with a "nothing proven" receipt listing files read and probes run, and shows zero invented findings.

- **Reject proofs that fail for the wrong reason** — SECURITY — value 4 — effort M — risk low — category: proof quality
  Why: a test red from an ImportError or a missing fixture is not evidence of a bug. The pack stresses "proves each finding".
  Done when: a finding whose red test fails on a syntax, import or setup error is rejected, and a test with a planted import error is shown to be dropped.

- **Calibrate the hunter on planted bugs in a scratch copy first** — FEATURE — value 4 — effort M — risk low — category: self-grading
  Why: the exam found 0/108, so nothing measures recall per repo before trust. Assumption: planting a mutation is cheap.
  Done when: before a first report on a repo, `fm find` plants 3 mutations in a throwaway worktree, prints the recall, and refuses to report if recall is below a floor.

- **Run a cold refuter against every finding before ranking** — FEATURE — value 4 — effort M — risk med — category: false positives
  Why: false positives are the main cost on `none` repos. A second model that tries to explain the test away is cheaper than a wrong fix.
  Done when: on a repo with a decoy that looks buggy but is intended, the refuter drops it and keeps the real finding.

- **Rank by value per dollar from survival data** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: the brief asks for value ranking and `fm outcomes` already records 30-day survival. Assumption: the weights can start from reach and proof strength.
  Done when: `fm find --rank` shows one score with its formula, and a test checks that the order changes when the survival weights change.

- **Keep Foreman's own setup faults out of user queues** — FIX — value 3 — effort S — risk low — category: scout hygiene
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks in user projects.
  Done when: a scout run in a clean fixture project with a broken Foreman hook files zero tasks and prints one setup line.

- **Cap a hunt by cost per confirmed finding** — PERFORMANCE — value 4 — effort S — risk low — category: budget
  Why: Foreman's session costs more than plain Claude at the same score, so spend must be bounded.
  Done when: a hunt stops after N dollars with no confirmed finding and prints the spend and the files left unread.

- **Fix in a lane with the failing test as the whole prompt** — FEATURE — value 4 — effort M — risk med — category: fix pipeline
  Why: the cheapest path to the plain-Claude score is the test plus the file, with no ceremony. Reject fixes that hardcode the test's literal.
  Done when: on 3 bug repos, the lane turns the test green, the earlier-green tests stay green, and a hardcoded-literal fix is rejected.

- **Plant canaries in the user's own repo to grade recall (wild)** — FEATURE — value 3 — effort L — risk med — category: trust
  Why: assumption: users will trust a "clean" only if Foreman shows it would have caught a bug here. wild
  Done when: `fm find --canary` mutates a scratch copy, reports which of 5 planted bugs were found, and leaves the real tree byte-identical.

- **Hold a trial: prosecutor and defender models per finding (wild)** — FEATURE — value 3 — effort L — risk med — category: adversarial
  Why: assumption: two opposed readings of the same code give a calibrated confidence that one model gives badly. wild
  Done when: each shown finding carries a one-line prosecution and defence, and disputed ones rank below unanimous ones.

- **Turn each missed exam defect into a new probe and re-score (wild)** — FEATURE — value 3 — effort L — risk high — category: self-improvement
  Why: the 108 misses are a labelled corpus. A probe that gets added must not lower the `none` score.
  Done when: a distilled probe lifts held-out recall and leaves a planted-clean repo silent, or it is reverted automatically.

- **Morning findings card with a one-key land or drop (wild)** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the nightly job exists (`fm run --fit --max 2`) but yields nothing the user can accept quickly. Assumption: dropped findings are fingerprinted so they stay gone.
  Done when: after a night run, `fm morning` lists merge-ready lanes best first, and a dropped finding does not return the next night.

Next question: What does an exam `none` scenario look like, and what does a false positive on one cost the user in trust compared to a missed bug?
Next question: Which languages in the exam can run tests with no setup, and where must the repro be a script instead of a test?
