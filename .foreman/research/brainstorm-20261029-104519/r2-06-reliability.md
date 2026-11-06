# Brainstorm — lens: reliability

Lens: reliability. Evidence comes from the pack's recent commits (overlapping suites, mid-word cuts, dry-streak miscounts, dropped @path lines, dead-end "no match" errors). Ideas here are not repeats of the listed ones: a single-writer lock, a did-you-mean helper, a stress harness, a flaky quarantine and an atomic close are already in the list.

- **Persist loop state in a crash-safe journal** — FEATURE — value 5 — effort M — risk med — category: loop reliability
  Why: the forever-loop's dry streak, budget-dropped rounds and "2 dry rounds" stop are in-memory decisions that were miscounted (T-1991, T-1992). assumption: the state is not yet append-only.
  Done when: killing the loop mid-round and restarting resumes with the same dry count, round number and dropped-work flags, checked by a test that kills the process.

- **Write every counter as a derived value, not a stored one** — CLEAN — value 4 — effort M — risk low — category: invariants
  Why: the dry streak counted a round that had no ideas fan-out. Counters that are stored and incremented drift; ones recomputed from the round log cannot. assumption: rounds are already logged.
  Done when: a test that replays a round log with budget-limited rounds yields the same streak as the live loop, and the stored counter is removed.

- **Assert state invariants at every task transition** — FEATURE — value 4 — effort M — risk low — category: invariants
  Why: T-1998 (core-integrity warning for in-scope edits) and the `_theirs` scope gap at close show checks disagreeing about whose file is whose. assumption: no single check validates focus, scope and dirty files together after each transition.
  Done when: `fm doctor --invariants` fails on a fixture where a task closes with another task's dirty file in its scope list, and passes on a clean tree.

- **Make every gate declare the files it reads and writes** — FEATURE — value 4 — effort M — risk med — category: gate hygiene
  Why: the check_paths test noted gate 1 never saw another gate's write. Undeclared writes cause reruns and missed reruns. assumption: gates declare only read paths.
  Done when: a gate that writes under another gate's paths without declaring it fails `fm doctor`, shown with a fixture.

- **Make timeouts and retries explicit for every child process** — FIX — value 4 — effort M — risk low — category: child processes
  Why: capped `claude -p` children lose partial results (T-0831 is deferred) and gates can hang. assumption: some call sites rely on defaults.
  Done when: a grep-based test finds no subprocess call without a timeout argument, and a hung fixture child is killed with its name in the error.

- **Give `fm doctor` a self-heal for stale state with a dry run** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: crashes can leave stale locks, running-flags and `gates_running` markers, and the ambient and ship overlap fixes depend on those markers being truthful. assumption: markers carry a pid but are not verified against it.
  Done when: a marker whose pid is dead is reported by `fm doctor` and removed with `--fix`, covered by a test.

- **Fuzz parse_intake with round-trip properties** — FIX — value 4 — effort S — risk low — category: parsing
  Why: three intake bugs in a row (@path-only lines, mid-word cuts, capitalized commands) came from hand-picked cases. assumption: no generative test exists.
  Done when: a seeded property test generates 1,000 intake texts and asserts that no line is lost, titles never end mid-word, and DONE-WHEN text survives intact.

- **Wild: Run a "crash at every line" test over task close** — FEATURE — value 4 — effort L — risk low — category: atomicity
  Why: assumption: close is multi-step (docs-impact, scope, proofs, commit). The test injects a kill after each write and checks that the next `fm` call either finishes or cleanly rolls back. (wild)
  Done when: a harness kills close at each of its N steps and the follow-up `fm doctor` is clean every time.

- **Wild: Keep a canary project that Foreman works on every night** — FEATURE — value 4 — effort L — risk low — category: canary
  Why: dogfooding found most recent bugs by accident (a scratchpad write set off a note). A fixed fixture repo run through intake, task, prove and ship each night would catch regressions before the user does. (wild)
  Done when: a scheduled run on a fixture repo reports pass or fail with the failing step, and a deliberately broken commit turns it red.

- **Wild: Version the on-disk state and replay migrations in CI** — SECURITY — value 3 — effort M — risk med — category: state schema
  Why: assumption: task, lesson and ledger files have changed shape over about 2,000 tasks. CI loads state snapshots from old versions and checks that current code reads or migrates them. (wild)
  Done when: an old-version snapshot fixture loads without error and a deliberately incompatible change fails CI.

- **Measure and budget hook latency failures, not just averages** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: `bench_hooks.py` is a gate, but the guard hook blocks every command in bypass mode, so a p99 spike or an exception is a safety hole. assumption: only a mean or median is checked. A hook that errors should fail closed for dangerous commands and open for plain reads.
  Done when: a test that makes the guard raise gets a deny for a destructive command and an allow for `ls`, and the bench fails above a stated p99.

- **Show the cause chain when a gate fails twice in a row** — FEATURE — value 3 — effort S — risk low — category: diagnostics
  Why: assumption: repeated failures are re-reported verbatim. A short line would say "same failure as the previous run; the changed files are X", which separates flakes from real faults.
  Done when: two consecutive identical gate failures print a repeat notice naming the files changed in between.
