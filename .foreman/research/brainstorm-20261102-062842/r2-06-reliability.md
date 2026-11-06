# Brainstorm — lens: reliability

- **Grade the tick's grader with mutants** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the pack says self-triggering is "unmeasured until the end-of-run exam". A new install-free grader that has never gone red proves nothing, and its first red would arrive at the final exam.
  Done when: `fm exam tick-mutants` applies at least 8 seeded mutations to a scratch copy of the tick (a finder disabled, the interval off by one, dedupe removed, the lock skipped). Every mutant turns the tick score red, and any survivor is printed with its mutation.

- **Freeze a golden tape corpus and ratchet it at ship** — FEATURE — value 5 — effort M — risk low — category: regression
  Why: assumption: replay tapes (virtual clock plus planted events) exist or are being built this mission. Without a frozen set, a change to the tick can pass today's grader by changing the tape.
  Done when: `fm ship` replays every tape in `evals/tick-tapes/` (each carrying a schema version) and fails if any tape's verdicts differ from its stored golden, or if any tape older than the current version fails to load.

- **Prove a hung tick can't slow a hook** — FIX — value 5 — effort S — risk low — category: isolation
  Why: the session-piggyback tick runs where the hook p95 ratchet already bites (T-2605 compares median wall time on a loaded bench). The tick's isolation from the hook path is asserted, not tested.
  Done when: `plugin/tests/bench_hooks.py --tick-hang` makes the piggyback tick sleep forever and kill-9s it mid-write. Hook median and p95 stay within the existing budget, and the next tick recovers the lock.

- **Test confluence across clock sources** — FEATURE — value 4 — effort M — risk med — category: correctness
  Why: assumption: with a timer, session piggyback and replay all able to tick, the same event may reach three paths. The idempotency keys from earlier ideas are never tested in interleaved order.
  Done when: a seeded property test shuffles 200 interleavings of the three sources over one tape. The final ledger, task set and fire count are byte-identical across all of them.

- **Model scheduler faults, not just clock jumps** — FEATURE — value 4 — effort M — risk low — category: simulation
  Why: assumption: a faked clock covers time but not scheduler behaviour. systemd coalesces with `AccuracySec`/`RandomizedDelaySec`, `Persistent=` replays one miss, cron drops runs while the machine sleeps, and launchd coalesces.
  Done when: a stub scheduler replays one tape under four profiles (systemd, cron, launchd-like, session-only). The grade shows per-profile missed, doubled and late fires, with the lateness bound each profile promises.

- **Run the finders across a git-state matrix** — FIX — value 4 — effort M — risk low — category: robustness
  Why: assumption: tick finders and `fm ci-watch` pollers assume a clean checkout. A tick fires at arbitrary moments, including mid-rebase, detached HEAD, shallow clone, linked worktree, submodule, sparse checkout or merge conflict.
  Done when: a fixture matrix of 8 git states runs the tick and each state gives a distinct outcome (acted, skipped with a reason, or errored), never a crash or a write into the user's tree.

- **Run the tick under an environment-invariance matrix** — FIX — value 4 — effort S — risk low — category: robustness
  Why: a detached piggyback child and a timer unit don't inherit the interactive shell. Variables such as LANG, TZ, HOME, PATH, umask and TTY can be absent or different, and parsing breaks on non-English git output or filenames with newlines.
  Done when: the tick runs under `env -i`, `LANG=de_DE`, `TZ=Pacific/Auckland` and with no TTY. It produces identical decisions on one tape, and filenames with unicode and newlines go through `-z` paths.

- **Read newer ledgers after a downgrade** — FIX — value 3 — effort S — risk low — category: compatibility
  Why: the user can roll back the plugin while ledgers written by a newer version remain. An older tick may then misread or truncate them, and the pack's schema-version idea covers only refusal to fire.
  Done when: a test writes ledgers with an unknown field and a higher version, runs the older tick, and shows it keeps unknown fields on rewrite and reports "newer state, read-only" rather than losing data.

- **Keep a single-point-of-failure register with a kill test each** — CLEAN — value 4 — effort M — risk low — category: resilience
  Why: assumption: the tick depends on one interpreter path, one lock file, one ledger, one library copy and one unit. No list names them or tests each loss.
  Done when: `fm doctor --spof` lists each single point of failure, and a test removes or corrupts each in a scratch state dir. The tick reports a named degraded state and the next session says so in one line.

- **Report time-to-detect and time-to-recover per fault class** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: assumption: the pack has fault drills but no recovery number. "It recovered" is not graded against "how long a user was uncovered".
  Done when: the compressed-week soak injects 6 fault classes and prints MTTD and MTTR for each in ticks and virtual minutes. `fm doctor` shows the worst, and a ratchet fails if it grows.

- **Wild: Fuzz tapes and shrink failures into regression tapes** — FEATURE — value 4 — effort M — risk med — category: fuzzing — wild
  Why: assumption: a seeded fuzzer reorders, duplicates, drops, delays and clock-jumps events in recorded tapes. It is the cheapest way to find the tick's unknown unknowns without the user's install.
  Done when: `fm exam tick-fuzz --seed N --runs 500` finds an invariant break, shrinks it to a minimal tape and writes it into the golden corpus. A planted bug is found within the budget.

- **Wild: Rebuild the tick's state from sources and diff it** — FEATURE — value 3 — effort M — risk low — category: recovery — wild
  Why: assumption: if the beat and fire ledgers are lost, the tick should be able to reconstruct "what was due and what ran" from git, tasks and captures.
  Done when: a drill deletes the tick ledgers in a scratch copy mid-tape. The tick rebuilds them, and the next tick makes the same decisions as an undamaged run, with any difference listed.

- **Wild: Run the tape twice in different sandboxes and compare hashes** — FEATURE — value 3 — effort S — risk low — category: determinism — wild
  Why: assumption: any hidden dependence on PID, hostname, mtime, dict order, locale or random seed in a pure-function tick shows up as a hash mismatch, and no install is needed to find it.
  Done when: CI runs one tape in two sandboxes that differ in PID namespace, hostname, `PYTHONHASHSEED` and file mtimes. The decision-log hashes match, or the first differing row is printed.

- **Degrade the tick in named tiers** — FEATURE — value 3 — effort M — risk med — category: degradation
  Why: assumption: under high load, low battery or an exhausted budget, the tick is either on or off, so the user loses all coverage when one step is expensive.
  Done when: the tick has tiers (full, finders-only, beat-only). The chosen tier and its reason are written to the ledger each run, each tier has a test, and `fm doctor` shows the share of ticks per tier over 7 days.

Next question: Which of Foreman's current "ran fine" signals would still read green if the tick had silently done nothing for a week, and what is the cheapest independent probe that would turn each red?
Next question: When the user finally installs the timer, what do they lose or gain compared with the session-piggyback tick, and is that difference measured on the same tape?
