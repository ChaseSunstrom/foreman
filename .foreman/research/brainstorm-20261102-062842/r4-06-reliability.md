# Brainstorm — lens: reliability

Reliability lens. These are NEW, aimed at making a tick that borrows sessions, CI or replay trustworthy without the user's timer. Where I say "assumption", the pack doesn't show it.

- **Run tick git reads lock-free and test against a live user git op** — FIX — value 5 — effort S — risk low — category: user-collision
  Why: assumption: the edge tick runs `git status/diff/log` in the user's repo while they commit or rebase. A plain `git status` refreshes the index and can take `index.lock`, so it can break the user's command. That would be the worst failure of self-triggering.
  Done when: a test runs tick git calls under `GIT_OPTIONAL_LOCKS=0` in a loop against a concurrent `git commit` and `git rebase` loop for 200 iterations, with 0 user-side lock failures and no `.git/*.lock` left behind.

- **Key tick state by git common-dir and realpath, not cwd** — FIX — value 4 — effort S — risk low — category: identity
  Why: assumption: several worktrees, symlinks or a bind mount (this box runs under `/run/user/1000`) make one repo look like N. That means N fires, N "overdue" warnings, and a split lateness ledger.
  Done when: a fixture with 3 worktrees plus a symlinked path yields exactly 1 repo id, and a session in each one fires a due job once in total.

- **Measure the edge-kill rate of Stop and SessionEnd ticks** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the pack proposes session-piggyback ticks but nothing measures how often the host kills a Stop hook mid-tick. Without that number the "lazy tick" grade is optimistic.
  Done when: every edge tick writes `begun` and `ended` markers. `fm tick edges` prints begun, ended, orphaned and percent truncated per edge, per host version, and a replay fixture with a planted kill shows a non-zero orphan count.

- **Version every self-triggering grade and expire it** — FEATURE — value 4 — effort M — risk low — category: grade integrity
  Why: grades come from cold reads, the exam and the tape, and each depends on grader code and fixtures that change. A stale grade reads as current.
  Done when: each grade line stores grader hash, fixture hash, input digest and a TTL. `fm doctor` lists grades whose grader changed as "stale (regradable free)", and the zero-token ones are regraded automatically on the next tick.

- **Derive each tick job's deadline and breaker from its own p99** — FEATURE — value 3 — effort M — risk low — category: timeouts
  Why: a constant timeout is either too loose, so a hang eats the hook budget, or too tight, so slow-disk days read as failures. This is distinct from the existing poison classification because it adds a half-open probe.
  Done when: after 20 runs a job's deadline is `max(2*p99, floor)`. After 3 consecutive failures the breaker opens, and one probe run per day closes it on success. A test with an injected slow disk shows no false open.

- **Gate the tick exam on statistical power** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: no week of live ticks exists, so any grade will rest on a handful of fires. Earlier ideas say "insufficient", but nothing computes how many scenarios would be enough.
  Done when: before a tick-vs-null grade is printed, `fm exam` computes the smallest detectable difference at the observed variance. If it exceeds a pre-registered bar, the output reads "underpowered: need N more scenarios" instead of a verdict.

- **Pin planted-event fixtures hermetically with a golden tree hash** — CLEAN — value 3 — effort S — risk low — category: fixtures
  Why: the pack's tape and planted-event fixtures are built with `git` and inherit the global config, default branch, hooks and date. Fixtures that drift per machine make grades non-reproducible.
  Done when: fixtures build under `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null` and `SOURCE_DATE_EPOCH`. Two builds on different machines produce the same tree hash, and CI fails on mismatch.

- **Fault-inject the real tick below the Python layer** — FEATURE — value 4 — effort M — risk med — category: fault injection
  Why: chaos-tick ideas inject faults from inside the code. Faults injected at the syscall level (ENOSPC, EROFS, EIO, EINTR) catch paths the author never thought of. Assumption: the hardened kernel may block `ptrace`, so the fallback is an `LD_PRELOAD` shim or a FUSE faulty directory.
  Done when: a nightly run drives the real `fm` tick under 5 injected syscall faults. Every run ends with state files parseable, no partial ledger line, and an exit reason recorded.

- **Name tick outputs by hash of their inputs so concurrent ticks need no lock** — FEATURE — value 4 — effort M — risk med — category: concurrency (wild)
  Why: lock and lease designs fail on stale holders and tmpfs oddities. If output path = hash(inputs) and writes are write-then-rename, two ticks racing produce identical bytes and the loser's write is a no-op. wild.
  Done when: 8 parallel ticks on one snapshot leave exactly one output file, byte-identical to a serial run, and killing any of them leaves no partial file visible to readers.

- **Keep an alibi ledger so the user can ask "was it you?"** — FEATURE — value 4 — effort S — risk low — category: trust (wild)
  Why: it answers the earlier question about the first hour after something goes wrong. If git failed oddly at 14:03, `fm tick alibi 14:03` says which tick or lane was alive then and which paths and repos it touched, or "none". wild.
  Done when: every tick, lane and edge run records interval, pid and touched repos. `alibi` returns the matching run for a planted interval and "no Foreman process alive" for a gap.

- **Register a decoy repo whose checksum must never change** — FEATURE — value 3 — effort S — risk low — category: containment (wild)
  Why: "tick left the user's tree untouched" is proven per test. A live sentinel proves it continuously, with no install. wild.
  Done when: the state dir holds a sentinel repo registered like a real one. A tick that writes to it flips `fm doctor` to FAIL naming the job, and a planted fault job triggers that in a test.

- **Check for an unnoticed month-long skew in due-time** — CLEAN — value 3 — effort S — risk low — category: assumption audit
  Why: answering an earlier question: the learner decision nobody would notice being wrong is the due-time and interval table. Every job slowly firing at 1.5x its interval looks like normal quiet.
  Done when: `fm doctor` prints the median ratio of observed gap to configured interval per job and WARNs when it is above 1.3 over the last 10 gaps. A replay with a 2x skew triggers it.

- **Replay the tape with PYTHONHASHSEED, TZ and locale varied and demand identical outputs** — FEATURE — value 3 — effort S — risk low — category: determinism
  Why: the tape replay is proposed as the free measurement, so any ordering or locale sensitivity makes it flaky and undermines the grade.
  Done when: the golden tape replays under 5 hash seeds, 3 time zones and 2 locales to the same output hash, and CI fails otherwise.

Next question: what fraction of the user's real days have no Foreman session open during their working hours, so that session-borne ticks cannot cover them?
Next question: which self-started output did the user ever act on without opening it, and how would the tick tell that from ignoring it?
