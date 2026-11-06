# Brainstorm — lens: reliability

- **Journal multi-step verbs before running them** — FIX — value 4 — effort M — risk med — category: crash safety
  Why: assumption: `fm task finish` and `fm ship` do several things in sequence (prove, commit, push, close, publish grant spent). "Crash points on the drive" covers the drive, not these verbs, and a half-done ship to main is the worst case. A write-ahead intent record would let a rerun resume or roll back.
  Done when: a test kills `fm ship` after each step, and the rerun either completes it once or reports the exact half-state. It never double-pushes and never leaves the grant spent without a push.

- **Cap unattended side effects per hour** — SECURITY — value 5 — effort S — risk low — category: blast radius
  Why: the night tick, `fm drive`, Genesis towers and parallel lanes all run unattended, and "advances itself" plus the push grant are standing rules. Nothing in the pack caps commits, pushes, files touched or children spawned per window. The only brake is usage.
  Done when: a stress test on a scratch repo shows an unattended run that exceeds its commit/push/file cap stops, files one inbox item, and `fm doctor` names the cap hit.

- **Add a HALT file every unattended path checks** — FEATURE — value 4 — effort S — risk low — category: kill switch
  Why: assumption: there is no single off switch across the timers, drive, tower and lanes. The user has paused things by steer ("pause every long-horizon exam run now"), which was a prose rule, not a mechanism.
  Done when: `touch ~/.foreman/HALT` makes the night tick, drive and genesis loop exit within one cycle with a logged reason, and removing it resumes them. A test covers each entry point.

- **Run a synthetic task through the installed copy hourly** — FEATURE — value 5 — effort M — risk low — category: synthetic monitor
  Why: `roundtrip.py` is a gate that runs at ship time on the working copy. The risk is that the installed plugin and timers drift or break between ships, which T-2605's committed-library fallback hints at. Doctor reading green because Foreman wrote the gauges is the known blind spot.
  Done when: a timer creates a throwaway task in a scratch repo, plans, proves, finishes and deletes it through the installed binaries. A deliberately broken installed hook turns `fm doctor` red within one interval.

- **Check cross-ledger references with `fm fsck`** — CLEAN — value 4 — effort M — risk low — category: integrity
  Why: Foreman keeps tasks, bets, steers, decisions, lessons and exam lines, all keyed by T-ids or bet ids. Earlier ideas test one record class missing; none checks that references between ledgers still resolve (a commit with a T-id absent from the tasks, a bet naming a closed task that never existed).
  Done when: `fm fsck` on a fixture with one planted dangling reference per pair of ledgers reports each, and exits clean on a healthy copy.

- **Schema-validate and retry every headless child's output** — FIX — value 4 — effort M — risk low — category: child contracts
  Why: brainstorm, cold reads, exam scenario writers and lanes are all `claude -p` children, and T-0831 already notes capped children losing partial results. A malformed or truncated reply is probably handled differently in each caller. A shared contract would count the malformed rate per verb and fall back one model tier before failing.
  Done when: a fault-injecting stub returning truncated, empty and non-JSON replies makes every caller retry once, then record a named failure. No caller treats a bad reply as "no findings".

- **Bound ledger growth with verified compaction** — PERFORMANCE — value 3 — effort M — risk med — category: retention
  Why: assumption: append-only ledgers (outcomes, friction, exam lines, hook decisions) grow forever, and `fm` readers are on hot hook paths where `bench_hooks.py` already tracks p95. Compaction is only safe if readers agree before and after.
  Done when: a 100k-record fixture is compacted by a command. Every reader's output is byte-identical before and after, and the largest reader gets at least 2x faster.

- **Run the suite in a hostile environment matrix nightly** — FIX — value 3 — effort S — risk low — category: determinism
  Why: the LeanKind flake (T-2605) came from wall-time noise, and the stack runs on one Arch box. Nothing shows the tests surviving random order, a different `TZ` and locale, a read-only or missing `HOME`, no TTY, or an odd umask.
  Done when: a nightly job runs the suite under at least four such settings and a seeded random order. Any failure files a task that names the setting.

- **Roll self-changes out to one lane first, with auto-rollback** — FEATURE — value 4 — effort L — risk med — category: staged rollout
  Why: the self-change gate compares bench times at ship time. Once a change lands on main, every session and timer gets it at once. Only hook errors that appear after the change can show a bad hook, and nothing watches for them.
  Done when: a ship that makes a hook error in the canary lane is reverted automatically within one tick, and the rest of the install keeps the previous revision.

- **Verify the pushed tree equals the tested tree** — SECURITY — value 4 — effort S — risk low — category: ship integrity
  Why: every push goes through `fm ship` gated by the full suite under a push grant. After the push, nothing compares the remote's tree hash to the tree that was tested, which would catch a rebase, hook rewrite or race that changed it.
  Done when: a test that mutates the tree between test and push makes `fm ship` report the mismatch and file a revert task.

- **Wild: Emit a repro bundle on any hook or verb crash** — FEATURE — value 4 — effort M — risk low — category: debuggability
  Why: wild; assumption: a crash that happens once in a hook is hard to reproduce. The bundle would be one redacted archive of stdin, env subset, ledger tail, versions and a fake-clock seed, replayable with one command.
  Done when: `fm repro <bundle>` reproduces an injected hook crash on another machine, and a secret planted in the input is absent from the bundle.

- **Wild: Hold a suspend-and-resume test for the whole day** — FIX — value 3 — effort M — risk med — category: time
  Why: wild; assumption: the laptop sleeps mid-drive. "Fake clock" covers readers, but not a real stop where PIDs, leases and usage-limit waits resume hours later.
  Done when: a harness SIGSTOPs a drive for 6 simulated hours and on SIGCONT it neither duplicates a task nor loses its lease, and it reports the gap.

- **Wild: Compare a second implementation of the guard** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: wild; the guard is the one part that must not fail silently. A deliberately dumb second matcher (regex-only, written by a separate child that never sees the first) is run over every command in the hook log. Any command one allows and the other blocks is a candidate bug.
  Done when: over a recorded month of commands the disagreement list is produced, and each disagreement is classed as a guard bug, a matcher bug or an intended difference.

- **Mark sessions that ended without a clean close** — FEATURE — value 3 — effort S — risk low — category: session hygiene
  Why: assumption: killed terminals leave a task claimed, a bet open or a pane state stale. The next session start can't tell a crash from a quiet pause.
  Done when: killing a session mid-task makes the next start print one line naming the task and the last recorded step, and offers resume or release.

Next question: Which Foreman operations are not idempotent, and which of them run unattended where a retry after a crash could repeat them?
Next question: When the installed copy, the working copy and main differ, which of them does each timer actually run, and who would notice?
