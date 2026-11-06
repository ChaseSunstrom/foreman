# Brainstorm — lens: reliability

Lens: reliability, applied to the immune-system mission. Cells I propose as single capabilities are marked **wild** when they are speculative.

- **Meter the backlog when a muted defence returns** (IRIS) — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: timers, nudges and detectors get disabled (ablation, demotion, outages), and when re-armed they release everything suppressed at once. IRIS is that flood after immunity is restored.
  Prior art: cron catch-up and coalescing exist for missed schedules only; none found for muted detectors. Better by: re-enabling drains the backlog at a capped rate, shown as one digest line. Novelty: 3.
  Done when: re-enabling a detector with 50 held signals emits at most N notes in its first hour plus one summary.

- **Map degenerate pathways per harm class** — FEATURE — value 5 — effort M — risk low — category: assurance
  Why: the pack lists many independent catchers (guard, replay corpus, CI, cold reader, risk budget) but no map of which harm class has more than one.
  Prior art: defence-in-depth diagrams are hand-drawn. Better by: generated from the code and the exam, naming classes with a single pathway. Novelty: 3.
  Done when: `fm doctor` lists each harm class with its count of independent catchers, and a class with one is flagged.

- **Keep a last-good generation of every state file** (mismatch repair) — FIX — value 4 — effort M — risk low — category: durability
  Why: the pack shows learners and ledgers corrupting silently, and the state dir is tmpfs-adjacent. A parse failure should restore the older strand and say so.
  Prior art: editors and databases keep backups; the harness doesn't. Better by: the reader falls back and files a task naming the file. Novelty: 2.
  Done when: truncating a ledger file makes the next read use the prior generation, and the failure is reported.

- **Bundle the first hour after harm** (sepsis bundle) — FEATURE — value 4 — effort M — risk med — category: incident response
  Why: the risk budget steps autonomy down after harm, but each reaction is separate. Sepsis protocols run a fixed bundle without waiting for a diagnosis.
  Prior art: runbooks in ops tools; none found in coding harnesses. Better by: one deterministic macro that snapshots state, freezes unattended lanes, replays the guard corpus and writes the incident line. Novelty: 3.
  Done when: a simulated harm event produces all five bundle artifacts within one tick.

- **Ledger lessons that precede worse outcomes** (antibody-dependent enhancement) — FIX — value 4 — effort M — risk low — category: learner safety
  Why: lessons are recalled per file, but nothing checks that recalling one lowers the reopen rate afterwards. A harmful lesson would never be noticed.
  Prior art: A/B holdouts in recommender systems. Better by: it runs on the existing ablation duels and names the lesson. Novelty: 4.
  Done when: a planted lesson that raises reopens in a fixture history is listed as net-harmful.

- **Add a don't-eat-me mark honoured by every deleter** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: the idea list proposes many deleters (retention, cold shelves, apoptosis, ablation cleanup, GC). One wrong prune loses a user's irreplaceable state.
  Prior art: legal hold flags in retention systems. Better by: one marker file and a library check that all deleters call. Novelty: 3.
  Done when: a pinned artifact survives every cleanup verb in a test that runs them all.

- **Install natural antibodies on day one** (annotate-only broad net) — FEATURE — value 3 — effort S — risk low — category: guard
  Why: assumption: a new repo has no incident history, so negative selection and memory have nothing to learn from. Innate-like cells are broad and low affinity from birth.
  Prior art: default deny lists in guards. Better by: broad damage shapes (mass deletes, writes outside the repo) only annotate until a second signal corroborates. Novelty: 3.
  Done when: a mass-delete in a fresh repo is annotated but not blocked, and blocked once a test goes red.

- **Make the guard immune to its own rule text** (self-mark) — FIX — value 3 — effort S — risk low — category: guard
  Why: the brief guard already produced false positives on paths. Rule files and the 124-case corpus contain the strings they forbid.
  Prior art: CRISPR avoids self-targeting through the PAM motif. Better by: a test that every corpus string is allowed when read, edited or grepped. Novelty: 3.
  Done when: reading and editing the rule files and corpus is allowed in every harness.

- **Detect alarms that recur on a rhythm** (periodic fever) — FEATURE — value 3 — effort S — risk low — category: observability — **wild**
  Why: assumption: repeating false alarms point to hidden collisions (cron overlap, DST, log rotation). Periodic fever syndromes are diagnosed by their rhythm.
  Prior art: alert-fatigue tools cluster by text, not period. Better by: autocorrelation over the existing alarm ledger. Novelty: 4.
  Done when: a fixture with a weekly 03:00 alarm is reported with its period.

- **Have a dying lane write last words** (pyroptosis) — FEATURE — value 3 — effort M — risk med — category: lanes — **wild**
  Why: assumption: killed lanes leave only a stale heartbeat. A doomed cell releases a final signal to its neighbours.
  Prior art: crash reporters in process supervisors. Better by: a pre-armed handler writes what it was doing and its last file, to siblings and the tower. Novelty: 3.
  Done when: a SIGKILL'd test lane leaves a readable note within the next tick (best-effort for SIGKILL).

- **Prove a lesson causal by adoptive transfer** — FEATURE — value 3 — effort L — risk med — category: learner safety — **wild**
  Why: ablation shows a lesson isn't needed, but not that it causes a good outcome. Immunologists transfer cells to a naive host to prove cause.
  Prior art: none found in coding harnesses. Better by: a fresh worktree arm receives one lesson and replays a past failure scenario. Novelty: 4.
  Done when: a lesson verified by transfer is tagged causal in the ledger, and one that fails is not.

- **Fix Foreman's own failures with a recipient-donor chimera test** — FEATURE — value 2 — effort L — risk high — category: reliability — **wild**
  Why: assumption: hidden learned state may be why a task passes here and fails on a fresh install.
  Prior art: clean-install testing. Better by: it runs the same scenario under donor state and seed state, then names the state keys that explain the difference. Novelty: 4.
  Done when: a planted state key that flips a verdict is named by the diff.

Next question: which of Foreman's deleters and re-enablers (retention, shelving, demotion, ablation cleanup) share a safety check, and which have never been run against a pinned or irreplaceable artifact?
Next question: when a lane is killed by the host or the OOM killer rather than by Foreman, does anything outside the session notice before the user does?
