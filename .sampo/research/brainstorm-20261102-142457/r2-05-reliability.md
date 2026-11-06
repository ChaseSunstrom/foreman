# Brainstorm — lens: reliability

- **Run a lean-measurement deadline sweep** — FEATURE — value 4 — effort S — risk low — category: lean
  Why: T-2503 lets growth with no exam/outcome measurement sit "pending" forever, so a gauge nobody can falsify never turns red. Assumption: the sweep has no per-row age field today.
  Done when: a lean row pending more than 21 days turns red in `fm genesis sweep` and files one measurement task, and a test with a faked clock shows both the boundary day and day+1.

- **Bind each push to the tree hash its gate passed** — SECURITY — value 4 — effort S — risk low — category: ship safety
  Why: c09 (fm ship asserts pushed tree equals tested tree) was asked for, and the push grant is spent on use. Assumption: ship checks the commit, not the tree, today.
  Done when: a test that amends the tree between gate and push makes `fm ship` refuse and name the two hashes.

- **Make every ledger writer torn-tail tolerant and prove it by killing at each write** — FIX — value 5 — effort M — risk med — category: ledger integrity
  Why: T-2664 just fixed one crash-cut line under `--accept-damage`; drill drops a class but doesn't kill mid-append. Assumption: other ledgers (flakes.json, bets, tick) lack the same fix.
  Done when: a harness SIGKILLs a writer at 50 random byte offsets per ledger and every reader plus `fm verify-ledger` returns a named result, never a traceback.

- **Show a "last green" restore receipt in fm doctor** — FEATURE — value 4 — effort S — risk low — category: recovery
  Why: T-2652 built `fm drill --restore`, but nothing says when it last passed; an unrun drill proves nothing. Assumption: drill results aren't recorded.
  Done when: `fm doctor` prints days since the last restore drill and goes yellow past 14.

- **Treat "could not run" as a third result in every gate** — FIX — value 5 — effort M — risk med — category: proof integrity
  Why: repeated ideas in the pack, and the user's own caught drop in T-2651 (a failed bench had checked its step off). Assumption: some gates still map exit-code-77 or timeout to pass or fail.
  Done when: a gate whose command is missing, times out or lacks a display records "unproven: reason" and `fm task finish` refuses to call it proven.

- **Fail-closed census of swallowed exceptions in hooks** — CLEAN — value 4 — effort M — risk low — category: hook safety
  Why: assumption: broad `except` blocks in `plugin/lib` hide guard failures; the bench is the only witness to hook behaviour.
  Done when: an AST scan lists every `except` that neither re-raises nor logs, and each guard-path one either fails closed or carries a reason comment, enforced in the test suite.

- **Add a hook crash card with fail-open or fail-closed declared per hook** — FEATURE — value 4 — effort M — risk med — category: hook safety
  Why: the guard is the safety layer, so a hook exception that silently allows is the worst failure. Assumption: modes aren't declared per hook now.
  Done when: each hook has a declared mode, a forced exception test per hook shows the declared outcome, and a crash writes one line naming the hook and the exception.

- **Probe the installed copy against the source on a timer and flag drift** — FEATURE — value 3 — effort S — risk low — category: install health
  Why: T-0418 (installed foreman-ui out of date) shows the installed part lags the source. Assumption: doctor has no per-component version comparison.
  Done when: `fm doctor` lists each installed component whose version or hash differs from source.

- **Wild: Pull-the-plug day for the drive** — FEATURE — value 4 — effort L — risk med — category: chaos
  Why: wild; the drive is unattended and has had crash fixes only after the fact.
  Done when: a scripted run kills the drive with SIGKILL at 20 random points in a fixture queue, restarts it, and every task ends closed, reopened or blocked with no orphan child and no duplicate push.

- **Wild: Shadow guard in 100 lines that must agree** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: wild; "who checks the checker" is an open question and the guard has one implementation.
  Done when: a second small guard runs over the replay corpus and every disagreement is listed; the suite fails on any unexplained one.

- **Wild: Dead-man's switch that tells the user the tower stopped** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: wild; silent death of unattended paths is a recurring theme, and a sleeping machine looks the same as a dead timer. Assumption: no outside-witness alert exists.
  Done when: if no tick lands for 3× its interval, a notification or file the user reads appears, and it stays quiet while the machine is suspended.

- **Quarantine a verb that crashes repeatedly** — FEATURE — value 3 — effort M — risk med — category: error budget
  Why: crash-loop quarantine sits in deferred T-0798; many verbs write shared state. Assumption: no per-verb crash counter.
  Done when: a verb that crashed three times in 24 hours prints "quarantined, run fm doctor" and is skipped by unattended paths, not by the user's hand.

- **Check that every "Next:" command actually parses** — FIX — value 3 — effort S — risk low — category: CLI
  Why: T-2653 just added Next: lines to every nonzero exit; a wrong suggestion would mislead at the worst moment.
  Done when: a test triggers each error class and runs the printed command with `--help` and gets exit 0.

Next question: which writes Foreman makes (ledgers, grants, ship, state migrations) have no idempotence or kill-point test, and which of them does the unattended drive run?
Next question: what does Foreman do when its own tests pass in the hardened-kernel, tmpfs-heavy environment the user runs but fail on a clean distro, or the reverse?
