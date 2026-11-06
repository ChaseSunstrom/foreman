# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Delete the drive's own agent-counting and read the host's task list only** — CLEAN — value 4 — effort M — risk med — category: drive
  Why: T-2873, T-2901 and the two earlier running-set fixes all patch event-scan heuristics that disagree with the engine's list. Each host release makes that heuristic more likely to be wrong.
  Done when: the running-set function has one source (the host's list, with a recorded "unavailable" state), and replaying 50 recorded engine shapes gives the same wait decisions with the event scan removed.

- **Make `sampo run-brief` the only thing a trigger calls, so any scheduler can start it** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: Scheduling is a commodity the host, systemd and the forge will all offer. What a host lacks is the Ward, plan, prove and done-gate wrapped around the start. If that wrapper is the product, Mission 6 survives any scheduler.
  Done when: the same brief started by cron, a systemd path unit and a CI job produces an identical receipt (Ward armed, proof recorded, done-gate verdict), and none of them needs a resident Sampo process.

- **Add a "gate stopped something" ledger for triggered sessions** — FEATURE — value 4 — effort S — risk low — category: moat evidence
  Why: The user wants overnight progress unattended. If a host-native routine would do the same work, the only defensible claim is what Sampo's gates caught. Today nothing records that per triggered run.
  Done when: each triggered run writes counts of Ward blocks, false-done refusals and unproven closes, and `sampo doctor` prints the 30-day total per trigger kind.

- **Park any trigger whose gate has stopped nothing in 30 days** — FEATURE — value 3 — effort S — risk low — category: self-retirement
  Why: assumption: a trigger that never caught anything is a candidate for the host's plain routine. This stops Sampo carrying machinery it hasn't earned.
  Done when: a trigger with zero gate events over 30 days is marked "parked: host-equivalent" in `sampo doctor` and emits a one-line way to re-arm it.

- **Replace the polling watchers with the forge's webhook or check-run events, and keep polling only as a fallback** — CLEAN — value 3 — effort M — risk med — category: watchers
  Why: CI and issue watchers by polling are what a forge's native event delivery makes obsolete. Evidence: the pack names CI and issue watchers as the Mission 6 scope with no event transport.
  Done when: with webhooks reachable the poll loop never runs (counter stays at 0 over a replayed week), and with them unreachable it falls back and says so once.

- **Run a "bare cron + plain prompt" arm against Sampo triggers on the user's real overnight queue** — PERFORMANCE — value 4 — effort M — risk low — category: obsolescence duel
  Why: The top gaps are drive stops and failed tool calls. Without the plain arm there is no way to tell whether triggers beat a cron entry running `claude -p`.
  Done when: for one week both arms get the same queued briefs and `sampo louhi` prints tasks passed, failed tool calls and cost for each, held-out.

- **Attribute failed tool calls to Sampo's hooks or to the host by running triggered sessions with hooks off** — FIX — value 4 — effort S — risk low — category: tool failures
  Why: Failed tool calls rose by half in the same generation that added hooks and injections. The cause is unknown, and a cause in Sampo itself would argue for retiring that part.
  Done when: a paired run of 20 identical triggered tasks with and without hooks reports failed-call rates per arm, and the delta is named in the next Seed.

- **Wild: Generate a host-native twin for every trigger and switch Sampo's copy off once the twin has fired** — FEATURE — value 3 — effort L — risk med — category: portability
  Why: assumption: hosts will ship routines. Each trigger compiles to a GitHub Actions workflow or host routine file, and Sampo's own firing steps aside once the twin is verified, so migration is automatic.
  Done when: one file trigger has a twin in a scratch repo, the twin fires on a planted change, and Sampo's copy logs "yielded to twin" instead of firing.

- **Wild: Run Mission 6's acceptance suite against a fake future host that has native cron, events and background tasks** — CLEAN — value 3 — effort L — risk med — category: obsolescence drill
  Why: assumption: it is cheaper to find which parts become no-ops in a simulated host than after the real release. Anything that still passes unchanged with the fake host's features on is redundant.
  Done when: the fake host exists as a test fixture and a report lists each Mission 6 capability as "still needed", "no-op" or "conflicts".

- **Wild: Hold a "manual week" drill that turns all triggers off and logs what the user does by hand** — FEATURE — value 3 — effort S — risk low — category: value proof
  Why: This is the direct test of the first earlier question: what would the user notice first? It needs the user's yes, so it is a request, not an automatic switch.
  Done when: with the user's one yes, triggers are disabled for seven days and the ledger lists hand-run actions that a trigger would have started.

- **Make the local-model background lane a pluggable provider and re-bench it monthly against the host's cheapest tier** — PERFORMANCE — value 3 — effort M — risk low — category: local models
  Why: The user wants local models used without limit for background volume. A host's cheap tier could make that lane obsolete, and only a measurement says so.
  Done when: one config line swaps the provider, and a monthly report shows pass rate per dollar and per hour for local and host-cheap on the same closed tasks.

- **Wild: Publish the trigger spec as an issue and PR template so the forge triages for itself** — FEATURE — value 2 — effort M — risk med — category: forge-native
  Why: assumption: if the forge's own template carries the brief fields (Done-when, Exam), Sampo needs no issue watcher; the forge feeds `run-brief` directly.
  Done when: opening an issue from the template starts a gated run with no watcher process, in a scratch repo.

Next question: if the host shipped scheduled, event-driven, sandboxed background agents tomorrow, which single Sampo guarantee would still be missing from it, and is it measured?
Next question: which Mission 6 piece does the user never open a receipt for, and does the ledger record that?
