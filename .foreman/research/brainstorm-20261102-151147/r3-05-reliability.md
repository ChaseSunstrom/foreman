# Brainstorm — lens: reliability

- **Wrap every unattended entry in one run envelope** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: the tick, `fm run`, lanes and provers each carry their own preflight and cleanup, so a gap in one is invisible to the others. The envelope checks installed-equals-source, disk, creds, clock and grants before starting. After the run it checks that no stray processes, spend or tree changes are left, and it writes one record for each run.
  Done when: a planted fault (full disk, orphan child, dirty tree) on each of the four entry paths yields the same named envelope failure line, and the planted-leak test fails without the envelope.

- **Remember the task a stall stopped on** — FIX — value 4 — effort S — risk low — category: drive
  Why: `--stall-usd` (T-2669) stops one run, but nothing carries over, so the next `fm run` can pick the same expensive task first and burn the same dollars. Assumption: the picker has no memory across runs.
  Done when: after a stall stop, the next `fm run` skips that task until its brief changes or the user releases it, and the receipt says so.

- **Charge killed children from their transcript tail** — FIX — value 3 — effort S — risk low — category: spend gauge
  Why: the stall and spend caps only work if spend is counted, and a `claude -p` child killed by a cap may never report its usage (T-0831 touches this). Assumption: usage lands only at clean exit.
  Done when: a fake child killed mid-run has its transcript usage added to the since-last-close total, and a test shows `--stall-usd` fires on that spend.

- **Gate `fm genesis live` on a clean ledger read** — FIX — value 4 — effort S — risk low — category: publish
  Why: the standing rule auto-publishes site data to main. If a reader skipped torn or damaged lines, the public page shows wrong numbers with no flag. Assumption: the publish step doesn't check whether the read was degraded.
  Done when: a ledger with one damaged line makes the publish refuse and name the line, and a clean ledger publishes as before.

- **Drive lint, doctor and help from one verb contract table** — CLEAN — value 4 — effort M — risk med — category: verbs
  Why: idempotence, resumability, fail-open or fail-closed, deadline, write-set and exit codes are proposed above as separate lints. One table (`verbs.toml`) that all of them read removes the drift between them. Assumption: no such table exists.
  Done when: removing a declared deadline or write-set for any verb fails the gate, and `fm help VERB` prints the contract.

- **Prove task-id allocation is collision-free under concurrent lanes** — FIX — value 3 — effort S — risk low — category: concurrency
  Why: Missions 5–8 file briefs from parallel lanes, and a duplicate T-id would corrupt every link between ledgers. Assumption: allocation is only tested serially.
  Done when: eight processes each filing 50 tasks yield 400 unique ids, and a planted non-atomic allocator fails the test.

- **Compare-and-swap Foreman's own writes into the user's tree** — FIX — value 3 — effort S — risk low — category: data safety
  Why: the user edits in an IDE while Foreman writers touch repo files (docs, `fm tidy`, generated sections). Assumption: these writers use plain overwrite.
  Done when: a file changed between a writer's read and write is left alone, with a "changed under me" line printed.

- **Make tower files merge-safe when lanes land** — FIX — value 3 — effort M — risk med — category: lanes
  Why: lanes are merged in mission order (standing steer), and generated files such as `coverage.md` and the `site/genesis` data are touched by several. Assumption: conflicts today get hand-fixed.
  Done when: two lanes editing different rows merge with no conflict and the sweep still passes, or the file is regenerated at merge.

- **Differential-check any warm hook daemon against the cold path** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: warm-daemon ideas recur above, and the failure they invite is a daemon that answers differently from a fresh process, or goes stale after an upgrade. Assumption: this is adopted.
  Done when: 1,000 recorded hook payloads give byte-identical output cold and warm, and a daemon on stale code is replaced rather than answering.

- **Ratchet the number of distinct lines the hook path executes** — CLEAN — value 3 — effort M — risk low — category: hooks
  Why: hooks run on every tool call, so each executed line is crash surface. A line-coverage trace over the recorded corpus gives a number that can only fall.
  Done when: the gate fails when the recorded corpus executes more hook-path lines than the stored ceiling.

- **Stamp lane records with a vector clock (wild)** — FEATURE — value 3 — effort M — risk med — category: ledgers
  Why: wild. Wall-clock and per-file sequence numbers can't say which lane's record happened before which after a merge. A vector clock restores causal order.
  Done when: two lanes' ledgers merged out of order replay in the same causal order as the original run.

- **Run a recovery theater in a scratch home (wild)** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. The user never sees recovery work. One command breaks a scratch home on purpose (torn ledger, missing grant, stale lock) and narrates each repair, so trust comes from watching it.
  Done when: `fm drill --show` breaks and repairs three faults in a scratch home, leaves the real home byte-identical, and prints a before and after for each.

- **Run a silence drill that times who notices (wild)** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: wild. This answers the open question about who notices first when a capability dies. A scratch install kills one unattended path, and the drill records how long until any surface (doctor, session start, pane) mentions it.
  Done when: each unattended path has a recorded notice time, and any path with none fails the drill.

Next question: which unattended path has no human-visible surface that would mention its death within a day?
Next question: what does `fm run` remember between runs, and what would a repeat offender (task, lane, model) have to do before anything notices?
