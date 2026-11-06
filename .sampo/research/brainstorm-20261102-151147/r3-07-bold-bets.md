# Brainstorm — lens: bold bets

Several ideas below build on or recombine items already on the list. They are framed as whole capabilities, not tweaks. I assume `fm` state is mostly plain files and JSONL ledgers, as the pack suggests.

- **Run the whole product in a seeded simulated world** — FEATURE — value 5 — effort L — risk low — category: reliability
  Why: assumption: the pack has many separate fault ideas (fake clock, torn writes, kill-at-each-step, soak, tapes, hostile host) and the recent fixes (T-2668 guard hang, T-2669 stall spend) were found by hand. One harness would cover them all.
  Done when: `fm sim --seed N` runs drive, lanes, ship, grants and hooks under one fake clock, fake agent and injected fs/process faults. It prints the seed on failure, the same seed reproduces the failure byte-for-byte, and a planted double-push bug is found within 200 seeds.

- **Model-check the task, grant and lane state machine, then check real ledgers against it** — FEATURE — value 4 — effort L — risk low — category: formal verification
  Why: assumption: the user keeps asking for "never twice, never lost" guarantees (two-phase grant, torn writes, claim heartbeats). A small TLA+/Python model can be searched exhaustively. Real ledgers can then be replayed against it as traces.
  Done when: a model file plus checker proves "a push grant is spent at most once" and "no task closes without a proof record". Replaying the live ledgers either conforms or names the first violating record. A mutated model fails.

- **Mine invariants from the ledgers and enforce them as live tripwires** — FEATURE — value 4 — effort M — risk med — category: self-audit
  Why: assumption: hand-written conservation laws are a short list, while the ledgers hold thousands of closed tasks that would reveal the real ones. Examples: "every close has a prove", "grant spend follows a grant".
  Done when: `fm invariants mine` outputs candidate rules with support counts. Accepted rules run in `fm doctor`. A planted violating record is named by rule and record id, and a rule with fewer than 30 supporting records is never enforced.

- **Build a policy lab: every decider registered, any change replayable** — FEATURE — value 4 — effort L — risk med — category: measurement
  Why: assumption: many ideas are threshold or ceremony changes (stall dollars, pace, ceremony per task kind). Each currently needs its own bespoke replay. A registry of pure decision functions with logged inputs would let one verb estimate the effect of any change before it ships.
  Done when: `fm lab replay --decider NAME --with CONFIG` re-decides over the last N days of logged inputs and prints the changed decisions with their counts. At least 4 deciders are registered, and a decider that doesn't log its inputs fails `fm doctor`.

- **Compile a plain-words session charter into sandbox, guard rules and an after-session check** — FEATURE — value 4 — effort M — risk med — category: safety UX
  Why: assumption: the user's steers show they state limits in sentences ("don't push without asking", "stay in this repo"). Today each limit needs a rule, a grant and a check.
  Done when: `fm charter "only this repo, no network except github, no deletes"` writes the rules, lists what it could not enforce, and ends the session with a diff of what actually happened against the charter. A planted out-of-charter write is reported.

- **Ship the guard and prover as an Agent SDK permission-callback package** — FEATURE — value 3 — effort M — risk low — category: distribution
  Why: assumption: the discipline layer is currently reached through hooks. SDK-built agents have a permission callback and no hooks. This reaches users the plugin never does and fits the "not specific to Claude Code" steer.
  Done when: a tiny sample SDK agent denies a planted `rm -rf ~` through the package, and the same corpus used for the guard passes unchanged.

- **Schedule one shared quota across all registered repos by marginal yield per dollar** — FEATURE — value 3 — effort M — risk med — category: scheduling
  Why: the recent spend work (`--stall-usd`, spend receipts) is per repo. Several repos competing for one usage window is an assumption, but the cross-repo inbox idea points that way.
  Done when: with two fixture repos and a fixed budget, the scheduler gives the repo with the higher recorded yield per dollar more of it, and prints the allocation and the reason.

- **Reconstruct a minimal reproduction from any ledger failure by delta-debugging records** — FEATURE — value 3 — effort M — risk low — category: debuggability
  Why: assumption: the reader-robustness tasks (T-0035, drop-one-class drills) need small fixtures, and hand-making them is slow.
  Done when: given a state dir where `fm doctor` crashes, `fm shrink` returns a fixture of 20 records or fewer that reproduces the same crash, redacted.

- **Expose state as a mountable filesystem, Plan 9 style (wild)** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: wild; assumption: weak models in `fm code` and hookless harnesses handle file tools better than verb syntax. `cat tasks/T-0001/status` reads and `echo done > ...` goes through the real verb and its gates.
  Done when: a FUSE or 9p mount exposes tasks, lanes and grants. A write to a status file passes through `fm task finish`, and a write that would fail the gate returns EPERM with the reason.

- **Stand up a standing Anti-Foreman adversary that is scored on lies it finds (wild)** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: wild; the standing rules want signals Foreman didn't author. The adversary is a tool-less child that sees only the final report and the public repo diff, and wins points for each claim a checker confirms is false.
  Done when: the exam prints an adversary score with confirmed and refuted counts. A planted false line in a fixture report is found, and a true report scores zero.

- **Publish the forecast as a subscribable calendar feed (wild)** — FEATURE — value 2 — effort S — risk low — category: ambient
  Why: wild; assumption: dated things already exist (quota resets, proof expiries, warranty windows, credential expiry, revisit dates on deferred tasks). A local `.ics` file is read by any calendar app on a phone.
  Done when: `fm cal` writes an `.ics` with at least 4 event kinds from the ledgers, and a calendar parser reads it without error.

- **Rerun settled bets with the data that arrived later, and report which lens was wrong (wild)** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: wild; assumption: lens hit rates are settled once at close, but later reopens, reverts and user rewrites change the truth. A monthly re-settlement would catch lenses that look good only early.
  Done when: `fm bets resettle` lists bets whose outcome flipped after later evidence and shows the corrected per-lens hit rate beside the original.

Next question: which of Foreman's guarantees has the user never seen fail, and which of those would a seeded simulation break within a night?
Next question: if the user's next 20 asks arrived as one paste, which of the above would they have been forced to type out by hand?
