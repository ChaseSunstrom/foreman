# Brainstorm — lens: reliability

- **Anchor the ledger tail outside the state dir** — SECURITY — value 4 — effort M — risk low — category: ledger integrity
  Why: T-2664 and `fm drill` rest on the hash chain, but a chain can't show that the last N lines were deleted. Each `fm ship` and nightly tick would write the ledger's head hash and line count to a second place (a `refs/foreman/head` git ref, plus a copy off tmpfs). `verify-ledger` then compares against it.
  Done when: a test deletes the last 5 lines of a ledger and `fm verify-ledger` fails naming "tail truncated, 5 lines behind the witness"; an untouched ledger passes.

- **Bracket every hook with start and end records** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: it answers the open question about decisions that leave no record. A hook the host kills on timeout writes nothing today. A cheap `start` line followed by an `end` line makes an orphan `start` mean "host killed this hook".
  Done when: a test hook that sleeps past its timeout leaves an orphan start, and `fm doctor` reports "N hooks killed by host in 7d" with the hook names.

- **Swap installs atomically and pin running sessions** — FIX — value 4 — effort M — risk med — category: upgrade safety
  Why: assumption: an upgrade rewrites the plugin tree in place while sessions are live, so a hook can import a mix of old and new modules. Install into `versions/X` and flip a symlink. A session records its version at start and hooks resolve through that record.
  Done when: a test swaps versions mid-session and the session's hooks still run entirely from the old tree. The next session uses the new one.

- **Split destructive verbs into plan and apply** — FEATURE — value 3 — effort M — risk low — category: safety
  Why: `fm tidy`, `usage --prune`, `drill`, compaction and `ship` mutate state. If apply consumes a saved plan file, what the preview showed is exactly what runs.
  Done when: `fm tidy --plan` writes a plan; `--apply PLAN` fails if the state changed since, and otherwise performs exactly the listed actions (test compares the two).

- **Send every deletion through a TTL trash** — SECURITY — value 4 — effort S — risk low — category: recoverability
  Why: the idea list has don't-eat-me marks but nothing for undoing a wrong deletion. Pruners, compaction and `tidy` would move files to `trash/DATE/` for 7 days, with `fm undelete`.
  Done when: a pruned file is restored byte-identical by `fm undelete`; after 7 simulated days it is gone.

- **Strip terminal escapes from untrusted strings at render** — SECURITY — value 3 — effort S — risk low — category: output safety
  Why: assumption: task titles, filenames, pasted steers and model output are printed raw. An ANSI/OSC sequence could rewrite the screen or set the terminal title. The fix is one `safe()` call in the shared print path.
  Done when: a task titled with `\x1b]0;x\x07\x1b[2J` prints with the escapes shown as visible `␛` text, and a test fails if any print site bypasses `safe()`.

- **Time guard regexes on pathological input** — PERFORMANCE — value 4 — effort S — risk low — category: guard reliability
  Why: a backtracking pattern on a 1 MB command can stall the hook until the host kills it, and a killed hook may fail open. A ratchet records each rule's worst-case milliseconds on adversarial inputs.
  Done when: the suite runs every guard rule on long nested-quote and repeated-token inputs and fails any rule over 50 ms. A deliberately bad rule in a test fixture is caught.

- **Add a guard lockout breaker** — FIX — value 3 — effort M — risk med — category: guard reliability
  Why: assumption: if a guard rule false-positives on something the session needs, bypass mode gets stuck in a loop. After 3 identical blocks, Foreman would print a one-line out-of-band release (`fm guard release ID`, typed by the user outside the session), recorded as an override and not as proof.
  Done when: a test blocks the same command 3 times, the third message names the release command, and running it permits one call and writes an override record.

- **Surface accepted ledger damage until it is re-anchored** — FIX — value 3 — effort S — risk low — category: ledger integrity
  Why: T-2664 added `--accept-damage`, which quietly turns a red state green. Record who accepted it, when, and which lines were lost. `fm doctor` shows an "accepted damage" row until a fresh checkpoint covers it.
  Done when: after `--accept-damage`, `fm doctor` lists the accepted range, and the row clears only after a later anchored checkpoint.

- **Stop a drive burning money without progress** — SECURITY — value 3 — effort M — risk med — category: runaway control
  Why: the dollar cap and per-task limits are absolute. A rate watchdog would pause the drive when spend per ledger-visible progress step (task transition or commit) exceeds 5× the trailing median, and file why.
  Done when: a fake agent that loops without committing trips the pause within its budget window, and a normal run does not.

- **Declare lock order and assert it under test** — CLEAN — value 3 — effort M — risk low — category: concurrency
  Why: the pack shows LockTimeout among the exits, and several ledgers and global files take locks. A declared hierarchy, with an assertion enabled only in the suite, catches inversions before they deadlock in production.
  Done when: a test that takes two ledger locks in reverse order fails with both lock names. The real verbs pass under the assertion.

- **Wild: Keep a write-set manifest per verb** — SECURITY — value 4 — effort M — risk low — category: containment — wild
  Why: assumption: a stray write is hard to attribute. An strace-derived, checked-in list of paths each verb may write, with the test running each verb under tracing, shows what a verb really touched and catches new unexpected writes before any user sees them.
  Done when: a verb that writes one undeclared path fails the manifest test, naming verb and path.

- **Wild: Tag every written file with its writer in an xattr** — FEATURE — value 2 — effort S — risk low — category: provenance — wild
  Why: assumption: with 2,000+ files and many writers, "who made this file?" is hard to answer. Setting `user.fm.writer=verb@version` (best-effort where the filesystem allows) lets `fm why PATH` answer.
  Done when: `fm why <state file>` prints the verb and version that wrote it, and says "unknown (no xattr)" on filesystems without support.

- **Wild: Make each unattended capability earn a reliability deposit** — FEATURE — value 3 — effort L — risk med — category: lean and safe — wild
  Why: a capability can run unattended only while it holds a balance of clean soak nights. Incidents withdraw from it, and at zero it disables itself with a named reason. This ties "lean" to "safe": a feature that can't stay reliable stops costing risk.
  Done when: a fake incident drops a test capability to zero, it is disabled, and `fm doctor` lists it with the cause.

- **Detect swallowed exceptions with an AST census** — CLEAN — value 3 — effort S — risk low — category: silent failure
  Why: silent death is a recurring theme in the pack. A static scan lists bare `except: pass` and broad handlers that neither log nor re-raise, ratcheted so the count may only fall.
  Done when: the census runs in the suite with a stored baseline; adding a new swallowing handler fails it.

Next question: which of Foreman's recovery paths (accept-damage, undelete, release) have the user ever actually run, and can they be rehearsed before the day they're needed?
Next question: what does the user see when Foreman is wrong about being healthy, and which outside signal would reach them first?
