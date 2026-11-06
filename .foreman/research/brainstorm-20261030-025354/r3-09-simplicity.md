# Brainstorm — lens: simplicity

- **Delete the deterministic finders and ship one `fm find` that asks a model** — FIX — value 5 — effort M — risk med — category: initiative core
  Why: the exam shows fmdocs.scan + fmsecrets found 0 of 108 planted defects while plain Claude finds 3/3 at ~0.17 USD. Four verbs (adopt, scout, deps, docs) overlap; one path to maintain beats four that score zero.
  Done when: on the held-out exam's `bug` and `none` kinds in never-seen repos, `fm find` recalls more than 0 planted defects, and `fm adopt`, `fm scout`, `fm deps`, `fm docs` print "use fm find" or are removed.

- **Make the failing test the entire finding** — FEATURE — value 5 — effort S — risk low — category: proof
  Why: the mission says "proves each finding with a failing test". A finding is one test file plus its run command, with no prose schema, no severity field and no separate report object to keep in sync.
  Done when: `fm find` output for any finding is a path to a test file that exits non-zero on the untouched tree, and a finding without one is never printed.

- **Hand the fixer the failing test as its whole prompt** — FEATURE — value 4 — effort S — risk low — category: lane fix
  Why: a lane already exists (`fm run`, PARALLEL_MAX 3). Reuse it instead of building a fix pipeline: the task text is "make this test pass without editing it", and the existing prove step judges the result.
  Done when: a finding becomes a queued task in one call, and `fm task prove` shows red before the change and green after, with the test file unmodified in the diff.

- **Rank by one number from facts already in `fm map`** — FEATURE — value 3 — effort S — risk low — category: ranking
  Why: the gap list asks for value ranking (3 gaps). A hot-file count times the number of importing files, divided by fix diff lines, is a one-line formula with no model call and no new store.
  Done when: findings print sorted by that number, the formula is shown in `--help`, and a golden-file test pins the order on a fixture.

- **Print "nothing proven" as a normal result** — FEATURE — value 4 — effort S — risk low — category: none verdict
  Why: the exam grades the `none` kind, and a finder that must always produce something will invent defects. A one-line receipt that names the files read costs nothing and removes the pressure to pad.
  Done when: on a clean fixture repo `fm find` exits 0 with "nothing proven (N files read)" and files zero tasks.

- **Cap a run at three proven findings** — CLEAN — value 3 — effort S — risk low — category: budget
  Why: PARALLEL_MAX is 3 and unasked work should not flood the user's queue. A hard constant replaces a budget system, a per-day cap setting and a ranking-before-capping stage.
  Done when: a fixture with ten planted bugs yields exactly three queued tasks and a line saying seven were left unfiled.

- **Keep dismissals in one plain text file** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: without it the same finding returns each run. A file of `test-name file-hash` lines checked by grep needs no database, and a changed file hash naturally revives the finding.
  Done when: dropping a finding means a rerun on unchanged files does not print it, and editing the file makes it eligible again.

- **Stop scout filing Foreman's own setup failures in user projects** — FIX — value 3 — effort S — risk low — category: noise
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks. The simplest fix is to delete that probe from the user-project path and keep it only under `fm doctor`.
  Done when: running scout in a fixture project with a broken Foreman install files no task and `fm doctor` still reports the fault.

- **Say "cannot prove here" when no single test can be run** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: unfamiliar stacks across the exam's six languages will have no runnable test command. A named refusal beats a guess that looks like a finding.
  Done when: a repo with no discoverable test runner prints that line and files nothing.

- **Wild: delete code before adding any** — FEATURE — value 2 — effort M — risk med — category: simplification (wild)
  Why: assumption: dead code and unused dependencies are the cheapest findings to prove, since removing them leaves the suite green and the build smaller. A finder of this kind starts there before hunting for bugs.
  Done when: on a fixture with a planted unused module, `fm find` proposes its removal with the suite passing before and after.

- **Wild: reject any finding that doesn't fit in one sentence** — FEATURE — value 2 — effort S — risk low — category: precision (wild)
  Why: assumption: vague findings are the likeliest false positives. If the test's name cannot state the defect in a single line, the finder has not understood it.
  Done when: the test name is the finding's title, and any candidate whose name is longer than one line or contains "and" is dropped before filing.

- **Wild: use the git history as the finder** — FEATURE — value 3 — effort M — risk med — category: sibling hunt (wild)
  Why: assumption: past fixes mark where the author's bugs live. Take the last ten `fix` commits and ask whether the same mistake exists in a sibling function, with no probe code to write.
  Done when: on a fixture where a past fix patched one of two copied functions, `fm find` produces a failing test for the unpatched copy.

- **Drop any finding that is not red twice for the same reason** — FIX — value 4 — effort S — risk low — category: flake guard
  Why: a test that fails once may be a flake or a broken harness. Running it twice and comparing the failure message removes the wrong-reason class without a model.
  Done when: a fixture test that fails with different errors on two runs is discarded, and one failing identically twice is kept.

Next question: Which of the exam's 108 planted defects would one plain `claude -p` pass over each file have caught, and is the remaining gap worth any Foreman code at all?
