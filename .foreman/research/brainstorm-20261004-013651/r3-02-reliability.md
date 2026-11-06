# Brainstorm — lens: reliability

- **Add a drive-state fsck that heals before it trusts** — FIX — value 5 — effort M — risk low — category: integrity
  Why: a crash left four zero-byte git objects, `git diff` broke, and `fm doctor` passed. Prior ideas name the symptom (git fsck, atomic writes) separately. This one bundles them into one session-start pass: `git fsck --connectivity-only`, zero-byte loose objects, torn or empty state/ledger JSON, and orphaned briefs. Each finding gets a quarantine-and-report action, never a silent delete.
  Done when: a test repo with a planted zero-byte object and a truncated ledger line makes `fm doctor` fail naming both, and `fm doctor --repair` moves them aside and exits 0.

- **Log every guard block as a replayable verdict with a reason code** — FIX — value 5 — effort M — risk med — category: guard precision
  Why: three false positives were hit in one day (`git stash list`, the python heredoc, read-only state reads). The fixes so far are one-offs. Persist each block (command, category, reason code, whether the user then approved it) and turn each user approval of a blocked command into a candidate "should have allowed" corpus case. The guard is tightened only when the replay corpus shows no new allow of a known-bad command.
  Done when: approving a blocked command appends a corpus case; `fm replay` fails if a patch to fmguard.py allows any case tagged bad; and the three known false positives are corpus cases that pass.

- **Make the reviewer wait a bounded, resumable state** — FIX — value 4 — effort M — risk med — category: drive loop
  Why: 18 drive turns ended just to wait on a background reviewer. Existing ideas propose a first-class wait state or zero-turn waits. Add the failure half: a deadline, a heartbeat check (is the child still producing output?), and a degraded verdict ("review timed out; self-audit only, flagged in proof pack") so a dead reviewer can't stall the queue forever.
  Done when: a stubbed reviewer that never returns makes the drive record a "review-timeout" and move on after the deadline; the proof pack shows the degraded flag.

- **Fingerprint gate flakes by load, not by retry** — FIX — value 4 — effort S — risk low — category: gates
  Why: one test class failed under heavy load and passed on rerun, a silent trust leak. Record the 1-minute load average and test ID on every gate failure, and on a pass-after-fail mark the test "flaky@load X" in a ledger. A gate pass that needed a rerun is shown as such and never counted as a clean first-time close.
  Done when: a simulated fail-then-pass run writes a flake entry with load, and `fm check` output labels the pass "passed on rerun".

- **Require a crash-consistency test for every state writer** — CLEAN — value 4 — effort M — risk low — category: durability
  Why: the machine crash was survivable only by luck. A permanent suite check (like `test_suite_hygiene`) that enumerates every function writing under the state dir and verifies each uses the shared atomic-write helper (temp file, fsync, rename), failing on any bare `open(..., "w")`.
  Done when: adding a bare write to a state file in fmcore makes test_suite_hygiene fail naming the file and line.

- **Wild: Run a canary brief at session start that exercises the real enforcement path** — FEATURE — value 4 — effort M — risk low — category: self-test
  Why: assumption: hooks can silently stop firing (a bad plugin update, a stale path), and `fm doctor` checks files, not behavior. A throwaway canary brief tries an edit with no active brief, expects the refusal, then clears itself. It costs about 35 ms per hook.
  Done when: disabling the edit hook in a test install makes the canary report "enforcement not firing" at session start.

- **Wild: Keep a rolling state snapshot with one-command rewind** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: the crash, the drive resuming from partial state, and the dropped "rebuilt" intake all show state can go wrong. Take a cheap snapshot (hardlinked or compressed) of briefs, queue and ledger at each step transition, keeping the last N. `fm rewind` restores one after showing a diff.
  Done when: corrupting the queue file and running `fm rewind --last` restores it byte-identical to the snapshot, with a diff shown first.

- **Fail loudly when hook latency or error rate degrades** — FIX — value 3 — effort S — risk low — category: observability
  Why: p95 is 35 ms over 888 runs, but nobody is watching it. Compare a rolling p95 and exception count per hook against a stored baseline. Warn once per session at 3× baseline or on any hook crash that failed open.
  Done when: a hook patched to sleep 200 ms makes the next `fm next` show a latency warning naming that hook.

- **Wild: Run a chaos drill that kills Foreman mid-transition** — FEATURE — value 3 — effort L — risk low — category: resilience
  Why: crash recovery has never been tested deliberately. A test-only harness SIGKILLs `fm` at random points inside task transitions (new, evidence, close, queue pop) against a temp state dir. It then asserts that `fm doctor --repair` reaches a consistent state with no lost evidence.
  Done when: 200 seeded kill points leave zero unrecoverable states, and any failure prints its seed for replay.

- **Bind reviewer findings to a regression seed before a batch can close** — CLEAN — value 3 — effort M — risk low — category: review loop
  Why: every review pass found 3–7 real issues, mostly parser edge cases and export privacy. Prior ideas propose fuzzing parsers and secret scanning in exports. The combination is a close-time rule: each accepted finding must link a test or fuzz seed that fails before the fix, or an explicit "not testable: reason" note.
  Done when: closing a task with an accepted reviewer finding and no linked test or waiver is refused with the finding's text.
