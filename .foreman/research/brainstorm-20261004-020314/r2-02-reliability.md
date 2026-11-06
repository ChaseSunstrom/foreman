# Brainstorm — lens: reliability

- **Make every hook idempotent under replay** — FIX — value 4 — effort M — risk low — category: hooks
  Why: Crash left empty git objects, and drive resumes after background waits and reload races. assumption: hooks like PostToolUse/Stop mutate ledger or state and can double-fire after a resume.
  Done when: a test feeds the same hook payload twice (same session and tool-use id) and the ledger and state are byte-identical to feeding it once.

- **Stamp every verify run with the tree it ran against** — FEATURE — value 5 — effort M — risk med — category: evidence
  Why: "nothing is done without evidence fm ran itself", but evidence can go stale after a later edit or a hand-edit. assumption: close checks only the exit code, not the tree hash.
  Done when: editing a touched file after a passing run makes `fm task close` refuse with "evidence stale for criterion N", and a rerun clears it.

- **Detect vacuous verify commands by mutating the target** — FEATURE — value 5 — effort M — risk med — category: evidence
  Why: Guard tests passed for the wrong reason (word scan caught what the parser should). The same shape hits verify commands: `grep` or `-k` selectors that match nothing still exit 0 (the run.py `-k` correction). assumption: no check currently proves a verify can fail.
  Done when: for a criterion, `fm task verify-lint` reverts the step's diff in a scratch lane and reports the verify still passing as "vacuous". A planted always-true verify is flagged.

- **Split every guard test into a "parse-only" twin** — CLEAN — value 4 — effort S — risk low — category: tests
  Why: Channel tests passed via the quoted-payload word scan. Tests should prove the parser, not the fallback.
  Done when: the guard test harness has a switch disabling the word scan, and the full channel suite still passes with it off (suite check in test_suite_hygiene).

- **Give hooks a process-wide time and output budget with a recorded degrade** — FIX — value 4 — effort M — risk med — category: hooks
  Why: p95 is 35 ms, but the tail is unmeasured. A hung hook in a drive stalls the turn, and a runaway log blows context. assumption: no per-hook deadline exists today.
  Done when: a hook given a stalled subprocess returns within its deadline, logs a `degraded` event naming the hook, and `fm doctor` lists degraded events from the last day.

- **Make gate flakes observable before they are quarantined** — FIX — value 3 — effort S — risk low — category: gates
  Why: One test class failed once under load and passed on rerun. Retrying silently hides it. assumption: reruns are not logged.
  Done when: a gate that fails then passes on rerun writes a flake record (test id, load average) and `fm friction` lists tests with 2+ records.

- **Wild: Run a "crash at every write" sweep** — TYPE FIX — value 4 — effort L — risk low — category: durability
  Why: wild. A machine crash left zero-byte objects and `fm doctor` passed. Instrument the state writer to raise at the Nth write across a scripted task lifecycle, then check that doctor and the next session recover or flag every N.
  Done when: the sweep over a canned lifecycle ends with zero N where `fm state` loads cleanly yet differs silently from the pre-crash truth.

- **Wild: Keep a poisoned-hook canary that must be blocked** — SECURITY — value 4 — effort S — risk low — category: enforcement
  Why: wild. Hooks refuse edits without a brief, but nothing proves that enforcement is live after a plugin update or reload (the reload race happened). At session start, a dry-run payload must be refused, or Foreman announces "enforcement OFF".
  Done when: disabling the PreToolUse hook in a test makes the session-start canary print a loud warning, and the normal path stays silent.

- **Wild: Let reviewer findings become automatic regression seeds with provenance** — CLEAN — value 4 — effort M — risk low — category: review
  Why: wild. Every review found 3–7 real issues, mostly parser edge cases and export privacy. Each finding should carry a `fm seed` test stub, so the same class cannot recur silently. Seeds are tied to the finding id.
  Done when: closing a reviewer finding without a linked test or an explicit waiver is refused, and the linked test fails on the pre-fix commit.

- **Re-verify the guard's allow-list approvals on expiry and on guard change** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: The guard evolves (new git channels), but user-granted approvals were made under the old rules. assumption: approvals are stored without a guard version.
  Done when: an approval granted at guard version N is shown as "needs reconfirm" after the guard's rule set changes category coverage, and is not auto-applied until confirmed.

- **Make the "turn ended to wait" state first-class in the ledger** — FIX — value 3 — effort S — risk low — category: drive
  Why: 18 drive turns ended only to wait on a reviewer subagent. Without a record of what is awaited, a lost completion looks like a stall. assumption: the wait is not recorded with an expected-by time.
  Done when: the drive records `waiting_on` with an id and deadline, and a missed deadline surfaces in `fm next` with a degraded-verdict option.
