# Brainstorm — lens: reliability

- **Quarantine flaky done-when commands** — FIX — value 5 — effort M — risk low — category: verification
  Why: assumption: a done-when that passes 1 run in 3 lets "done" flip between legs. The pack shows flaky finders but no flake check on the goal's own verify commands.
  Done when: a done-when stub that fails 1 run in 5 is run 5 times at seal, flagged "flaky", and refused as a sole completion proof (test).

- **Reap orphaned child processes and budget burners** — FIX — value 4 — effort S — risk low — category: processes
  Why: assumption: a killed leg leaves detached `claude -p` children (cold reads, exam arms, publish) still spending money. The pack mentions capped children and a $ budget but no reaper.
  Done when: after SIGKILL of a parent, `fm doctor` lists and kills its children by process-group tag, and a test shows none remain.

- **Version goal files and test an N-1 reader** — FEATURE — value 4 — effort M — risk med — category: migration
  Why: assumption: goals now span days and Foreman ships daily (T-2xxx commits). A goal opened under an older schema can be misread after an upgrade, with no sign of it.
  Done when: a fixture goal written by the previous release resumes under HEAD with identical `fm goal step`, and an unknown newer version refuses to write.

- **Fingerprint git and toolchain state, and re-baseline on change** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: assumption: a branch switch, rebase, force-push, stash or compiler upgrade between days makes earlier passes meaningless. The "re-prove on resume" idea doesn't say when to re-prove.
  Done when: changing branch or Python version between legs makes resume print "environment changed: N items stale" and mark exactly the affected criteria unproven.

- **Sandbox every verify command with a timeout and group kill** — SECURITY — value 5 — effort M — risk med — category: stop hook
  Why: assumption: a hung or network-dependent done-when run from the Stop hook can wedge the session, or hit the hook time budget the bench tracks. Group kill, a wall-clock cap and a "timed out" verdict (counted as unproven) close it.
  Done when: a done-when with `sleep 9999` returns "timeout, unproven" within the cap and leaves no process behind.

- **Circuit-break crashing hooks and say so loudly** — FIX — value 4 — effort S — risk low — category: hooks
  Why: assumption: a hook that throws on every turn either blocks the user or silently stops enforcing. Today it's unclear which one happens.
  Done when: after 3 consecutive crashes the hook is bypassed with a visible notice and a ledger event, and the circuit auto-resets after one clean run (test).

- **Preflight disk, permissions and quota for the state dir** — FIX — value 3 — effort S — risk low — category: storage
  Why: assumption: the ledger lives under `~/.claude/foreman/state`, and a full or read-only disk gives half-written files. The environment is a hardened system with tmpfs paths.
  Done when: with a full tmpfs mounted as state, `fm doctor` flags it, writes refuse cleanly, and no ledger line is torn.

- **Run the whole suite under a skewed clock** — FIX — value 3 — effort M — risk low — category: time
  Why: assumption: 14-day windows, 180-day outcome fading, the 3-a-day scout cap and push debounces all read wall time. DST, suspend and clock jumps can reopen or close them early.
  Done when: tests with a fake clock jumping forward, backward and across DST show the daily caps and windows hold, ordered by ledger sequence rather than timestamp.

- **Check that every `fm` verb is idempotent** — CLEAN — value 4 — effort M — risk low — category: crash safety
  Why: a crash mid-verb means the next session re-runs it, and a repeat could duplicate an intake or a task. T-2213 already shows a duplicate-intake path.
  Done when: a property test runs each state-changing verb twice, and again after a kill at each write point, and the state hash is unchanged after the second run.

- **Validate child outputs against a schema, with deterministic fallback** — FIX — value 4 — effort M — risk low — category: auditors
  Why: the cold-read stray-quote issues (T-2228, T-2229, T-2231) show child output parsing is the fragile part. A truncated or off-format reply must read "unaudited", never pass.
  Done when: a stub child returning truncated JSON, prose or nothing yields "unaudited" plus one retry, never a pass or a crash.

- **Reap stale locks by pid plus start time** — FIX — value 3 — effort S — risk low — category: concurrency
  Why: assumption: after a reboot or crash, pid reuse makes a dead owner look alive, so a goal stays locked.
  Done when: a lock file naming a reused pid with a different start time is reclaimed with a logged takeover (test).

- **Wild: Keep a black-box recorder for hooks** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: wild: processes killed before any hook ran leave no trace (an open question). A ring buffer of the last 200 hook invocations (event, input hash, decision, ms) makes `fm blackbox` a crash post-mortem.
  Done when: after a SIGKILL mid-turn, `fm blackbox` shows the last hook, its decision and its elapsed time.

- **Wild: Run a nightly canary goal against the newest Claude Code** — FEATURE — value 5 — effort L — risk med — category: compatibility
  Why: wild: Foreman rides on Claude Code's hook protocol and a patched UI mod (T-1217, T-0418). A tiny real goal, driven end to end nightly, catches a protocol drift before the user does.
  Done when: a scheduled run on a fixture repo finishes a 3-item goal on the latest Claude Code and files a self-inbox fault when any stage regresses.

- **Wild: Mirror state to a twin and restore to any point** — FEATURE — value 4 — effort M — risk low — category: backup
  Why: wild: goals live for days, and one corrupted ledger loses the plan. An hourly append-only snapshot with `fm restore --at <time>` makes a bad write recoverable.
  Done when: after deleting a goal file, `fm restore` brings back the ledger as of 1 hour ago and `fm goal step` matches the pre-delete answer.

- **Wild: Rehearse a power cut in a throwaway VM** — FEATURE — value 3 — effort L — risk med — category: crash test
  Why: wild: kill -9 doesn't lose page-cache writes, but a power cut does. A weekly VM hard-reset test during a goal checks that fsync and rename ordering actually hold.
  Done when: a hard reset mid-write leaves a ledger whose hash chain verifies, or heals to the last sealed checkpoint.

Next question: Which Foreman writes (ledger, goal card, lessons, site export) are not atomic, and what does a reader see halfway through each?
Next question: When Claude Code itself updates, which hook fields or events does Foreman assume, and what tells us one changed?
