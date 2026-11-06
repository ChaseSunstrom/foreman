# Brainstorm — lens: reliability

- **Make every state file write atomic with a torn-write sentinel** — FIX — value 5 — effort M — risk med — category: durability
  Why: a machine crash left four zero-byte git objects and Foreman never noticed. The same crash can truncate briefs, ledger, or queue JSON. Prior ideas mention atomic writes only in passing. This one pairs temp-file + fsync + rename with a checksum footer, and read paths quarantine a bad file and restore from the last good copy.
  Done when: a test truncates each state file type to 0 bytes and half its length; the next `fm` command reports the file, restores the previous generation, and exits 0.

- **Run `git fsck` in a cheap doctor tier and at session start** — FIX — value 4 — effort S — risk low — category: doctor
  Why: `fm doctor` passed with empty loose objects that broke `git diff`. Existing ideas say "detect and repair," but this one specifies a bounded fast check (zero-byte objects under `.git/objects`, a `HEAD` that resolves) with a full `fsck` only on demand, plus a repair that moves bad objects aside and refetches or reports.
  Done when: a fixture repo with one zero-byte loose object makes `fm doctor` fail naming the path, and `fm doctor --repair` makes `git diff` work.

- **Give each guard block a stable reason code and an allow-once escape hatch** — FEATURE — value 4 — effort M — risk med — category: guard precision
  Why: three false positives (`git stash list`, a python heredoc editing lib source, read-only python on state files). Each block should print its rule ID and the minimal precise allow it would take. Every user-granted allow is logged as a false-positive candidate that becomes a replay case. This makes the guard more precise without weakening it.
  Done when: the three known commands are allowed by the replay corpus, a true positive such as `git stash drop` is still blocked, and the block message contains a rule ID.

- **Add a flake ledger keyed by test ID with a load probe** — FEATURE — value 3 — effort M — risk low — category: gates
  Why: one test class failed once under load and passed on rerun, so a rerun looks like a pass. The gate should record machine load at failure. On a pass-after-fail it logs a flake entry marked "passed on rerun, load N" and never silently equates it with a clean pass. Three flakes flag the test in `fm next`.
  Done when: a test that fails once and then passes makes `fm check` report "flaky" with load, and the entry appears in `fm friction`.

- **Bound every reviewer wait with a deadline and a degraded verdict** — FIX — value 4 — effort M — risk med — category: drive
  Why: the drive ended a turn 18 times waiting on a reviewer. Add a drive state "waiting: reviewer, deadline T". If the deadline passes, the audit records "lens unrun" rather than hanging, so the task cannot close as audited. This complements the existing first-class wait-state idea by covering the failure case.
  Done when: with a stubbed reviewer that never returns, the drive records "lens unrun" after the deadline, and the task refuses audited closure.

- **Fuzz every new parser from reviewer findings, and require one fuzz seed per parser** — CLEAN — value 3 — effort M — risk low — category: test hygiene
  Why: each review batch found 3–7 issues, mostly edge cases in new parsers. Extend `test_suite_hygiene` so any module that parses user text (routing JSON, revisit triggers, assumption tags) has a stdlib-random fuzz test with a fixed seed that asserts no exceptions and idempotence.
  Done when: hygiene fails on a parser module without a fuzz test, and passes once one is added.

- **Wild: Run a crash-injection drill that kills Foreman mid-write** — FEATURE — value 4 — effort M — risk low — category: chaos
  Why: assumption: a real crash is the least-tested path. `fm drill` forks a child doing a brief close or ledger append, SIGKILLs it at random points over N trials in a temp copy of state, then runs `fm doctor` and asserts that state is either old or new, never torn.
  Done when: 50 seeded kills leave zero unreadable state files, and a deliberately non-atomic writer makes the drill fail.

- **Wild: Keep a canary brief that proves the enforcement path end to end** — FEATURE — value 4 — effort S — risk low — category: self-test
  Why: hooks can fail open silently. A synthetic session attempts an edit with no brief and expects a refusal, and claims done with no evidence and expects a refusal. `fm doctor --canary` runs it, and session start runs it at most once a day.
  Done when: disabling the edit hook in a fixture makes the canary fail naming that hook.

- **Wild: Keep a rolling state snapshot with a one-command rewind** — FEATURE — value 3 — effort M — risk low — category: recovery
  Why: assumption: the user will eventually hit state corruption or a bad bulk edit. Hardlink-based snapshots of the `.foreman` state are taken before risky commands (batch, evolve, drive start) and kept by count. `fm rewind` lists them and restores one after showing the diff.
  Done when: after a deliberately damaging command, `fm rewind` restores byte-identical state, and snapshot disk use stays under a cap.

- **Fail loudly when a hook's own latency or error rate degrades** — PERFORMANCE — value 2 — effort S — risk low — category: hooks
  Why: hook p95 is 35 ms over 888 runs, which is good, but nothing alerts if it drifts. Record the per-hook p95 and exception counts, and have `fm doctor` flag a hook over a threshold or one that has fallen back to fail-open.
  Done when: a fixture hook that sleeps 500 ms makes `fm doctor` flag it by name.
