# Brainstorm — lens: self-modification: proof kinds that learn which checks caught real misses and which were theatre, retiring the theatre, measured and reversible

- **Keep a catch ledger per proof kind** — FEATURE — value 5 — effort M — risk low — category: proof learning
  Why: the pack shows many proof kinds (bench, migration, shot, flow, unit) but no record of which ever failed a task before a later reopen. Assumption: reopens and reverts are already in the event log.
  Done when: `fm proofs ledger` prints, per kind, runs, first-run fails, fails later confirmed real, and reopens it missed, from events alone.

- **Define "theatre" as a computed, user-readable verdict** — FEATURE — value 5 — effort S — risk low — category: proof learning
  Why: earlier ideas say "flag proof that could not have failed" but give no rule. Theatre = N runs, zero fails, zero planted-fault detections, and zero overlap with later reopens.
  Done when: a proof kind with 20 green runs and no detections shows `theatre?` with the three counts, and one with a single real catch does not.

- **Retire theatre to advisory through shadow mode first** — FEATURE — value 5 — effort M — risk med — category: self-modification
  Why: a proof kind that costs seconds and tokens and has caught nothing is a tax. Retirement must be measured and reversible. Assumption: the proof policy lives in a diffable file.
  Done when: a kind moves enforcing → shadow (runs, never blocks, logs would-have-blocked) → advisory, each step a commit to `proof-policy`, and `fm proofs restore KIND` reverts it in one command.

- **Add an automatic tripwire that un-retires a kind** — SECURITY — value 5 — effort M — risk low — category: reversibility
  Why: a retired check's absence is invisible by definition. Assumption: later reopens, reverts and red-after-merge are attributable to a task and its retired kinds.
  Done when: a reopen on a task closed while kind K was advisory, where K would have failed, returns K to enforcing and prints the evidence line.

- **Plant faults to score catch rate without waiting for real misses** — FEATURE — value 5 — effort L — risk med — category: mutation
  Why: real misses are rare, so the ledger alone starves. A saboteur applies a small mutation to a closed task's diff in a scratch worktree and records which kinds notice. Assumption: scratch worktrees (`fm lane`) are cheap.
  Done when: `fm proofs probe` mutates 10 closed tasks, and the ledger gains a "detected N of 10 planted" column per kind.

- **Gate the retirer with a user-owned floor** — SECURITY — value 5 — effort S — risk low — category: self-modification
  Why: the standing rules put consent on channels the model can't write (cf. `fm mandate set` as user-only). A self-modifying proof layer can quietly erode itself and then grade itself.
  Done when: unretirable kinds (e.g. red-first test, done-gate) are listed in a user-only file, and a test shows the retirer refuses them even when their stats look like theatre.

- **Cold-read each policy change for metric-gaming** — SECURITY — value 4 — effort S — risk low — category: self-modification
  Why: steer: every tower file gets a cold Haiku read against gen-0's MUSTs. A retirement is a policy edit that can raise "pass rate" by deleting checks. Assumption: the cold-read harness takes arbitrary files.
  Done when: a retirement that raises the held-rate with no catch-rate evidence is refused by the reader, with a verbatim quote.

- **Report theatre cost as seconds and tokens saved** — PERFORMANCE — value 4 — effort S — risk low — category: lean
  Why: the lean ratchet already tracks always-on footprint. Proof runs are untracked cost. Assumption: events carry durations.
  Done when: `fm proofs ledger` shows total run time per kind and projected saving if retired, and `fm doctor` warns if a kind exceeds a time budget with zero catches.

- **Escalate a kind that keeps missing, not only retire one that never catches** — FEATURE — value 4 — effort M — risk med — category: proof learning
  Why: learning should go both ways. If reopens cluster on tasks whose only evidence was typed, promote the stricter kind to required for that task type. Assumption: reopens carry the task type and evidence kind.
  Done when: after 3 reopens on UI tasks closed with only unit tests, `fm shot` becomes required for that type, with the policy diff shown.

- **Keep a per-task-type proof diet** — FEATURE — value 4 — effort M — risk med — category: ceremony
  Why: T-1266 (ceremony profile per task kind and model) is deferred. A catch ledger sliced by type is its missing data. Assumption: type is stored per task.
  Done when: policy resolves kinds by (type, tier) and a docs-only task is no longer asked for a migration proof, shown in `fm task focus`.

- **Wild: Run a "proof tournament" between kinds on replayed history** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: assumption: closed tasks have start and end trees. Replay each past task's bad variants (reverted commits, reopens) against every kind and score who flags them first.
  Done when: a tournament over the last 50 closed tasks outputs a ranked table of kinds by recall and cost.

- **Wild: Make proof kinds expire like milk unless they re-earn trust** — FEATURE — value 3 — effort M — risk med — category: self-modification
  Why: assumption: evidence decay is already an idea. Each kind holds a trust score that halves every 30 days without a detection, and drops it to shadow at a threshold, returning on a probe catch.
  Done when: a kind with no detection in 90 days appears as shadow with its trust history in a diff.

- **Wild: Let the user bet against a kind** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the user has hunches about which checks are fluff. `fm proofs doubt KIND` pre-registers a prediction that it will catch nothing in 30 runs; the ledger settles it and shows who was right.
  Done when: a doubt is recorded, then settled with a plain-words result after the window.

- **Wild: Publish a theatre-cost page beside the exam scores** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: the Genesis site already publishes stats daily (T-2326). Showing retired kinds, reasons and restores keeps the layer honest to strangers.
  Done when: `site/genesis` data includes per-kind catches, planted detection, cost and retirement history.

Next question: Which proof kinds can be run in shadow mode without side effects, and which (migration, infra apply) can't be run twice for scoring?
Next question: When a retired kind's later catch is the only evidence it mattered, who judges that the catch was real and not a flaky failure?
