# Brainstorm — lens: simplicity

- **Flag what lacks the self-mark** (NK missing-self) — FEATURE — value 4 — effort M — risk low — category: immune
  Why: every guard so far reacts to foreign patterns; none reacts to a missing marker. Pack shows hookless harnesses and hand edits slipping past (plan-gate bypass counts, `fm code`).
  Prior art: DCO/trailer checks look for a sign-off only on commits, not on edits. Better by: diffs the working tree against the recorded edit/event log, so any change that skipped Foreman's hooks shows up. Novelty: 3.
  Done when: a file changed outside any hook event appears in `fm doctor` within one tick.

- **Keep one self-file** — CLEAN — value 4 — effort M — risk med — category: immune
  Why: negative selection, tolerance and missing-self all need "what is self"; today each learner would build its own. Assumption: accepted commands, paths and trailers are enough.
  Prior art: file-integrity baselines (AIDE, Tripwire). Better by: learned from accepted work and shared by the guard, learners and cold reader. Novelty: 2.
  Done when: one file feeds at least three consumers, and deleting it makes all three report "no self".

- **Run risky work in a sanctuary** (immune privilege) — FEATURE — value 5 — effort M — risk med — category: prompts
  Why: frontier shows 15+ approval prompts per session. Immune-privileged sites suppress response because collateral damage costs more than the threat.
  Prior art: sandboxes and devcontainers. Better by: inside a disposable worktree there are no per-call prompts, and one diff check at the border replaces them. Novelty: 3.
  Done when: a lane in a night worktree runs a 30-call task with zero prompts, and the merge shows a single gate.

- **Catch lessons that imprint** (original antigenic sin) — FEATURE — value 4 — effort M — risk low — category: learners
  Why: open question "which learner was never tested with poisoned input". A lesson recalled for a file can anchor the agent on the old fix when the new failure has a different cause.
  Prior art: none found; retrieval tools never score memory harm. Better by: ties each recall to the outcome. Novelty: 4.
  Done when: a lesson recalled before two failed or reopened tasks gets flagged "imprinted" and is withheld in a replay fixture.

- **Score each lane's vitals** (early-warning score) — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: assumption: unattended lanes die slowly (retries, edit/revert flip-flops, burn rate) before any gauge notices.
  Prior art: agent loop detectors catch repeated calls only. Better by: a clinical-style sum of five small integers with fixed escalation, to watch, then to stop. Novelty: 3.
  Done when: a fixture lane that loops edit-revert hits "stop" by score and a healthy lane never exceeds "watch".

- **Clear corpses with tombstones** (efferocytosis) — CLEAN — value 4 — effort S — risk low — category: learners
  Why: dropped-as-mistake captures polluted the user model (T-2554) and the dropped list shows repeated stale-state confusion.
  Prior art: database tombstones. Better by: one tombstone table that every learner and ledger joins at read time. Novelty: 3.
  Done when: dropping a task removes its rows from the user-model input, and a test finds no derived row that references a tombstoned id.

- **Delete rules a barrier already covers** (barrier before immunity) — CLEAN — value 3 — effort M — risk med — category: lean
  Why: the lean ratchet only grows or shrinks by size. Skin makes many immune responses unnecessary, and a read-only mount or network-off lane may make guard rules dead weight.
  Prior art: defense in depth, never pruning. Better by: replays the corpus with the barrier on and lists rules that never fire. Novelty: 3.
  Done when: `fm doctor` lists at least one rule that is dead under a named barrier, with the replay evidence.

- **Bind learned approvals to their repo and worktree kind** (MHC restriction) — SECURITY — value 3 — effort S — risk low — category: tolerance
  Why: assumption: an approval granted in a scratch tree should not become tolerance in the main tree or another repo.
  Prior art: path-scoped permission rules. Better by: the key includes where it was learned, so tolerance can't leak. Novelty: 2.
  Done when: an approval learned in a worktree is rejected for the main tree in a test.

- **Hold a warning to the next checkpoint** (kinetic proofreading) — FIX — value 3 — effort S — risk low — category: detectors
  Why: three "Breakage ahead" alarms were dropped as false (048da03, 18101f0) because they fired on a one-time snapshot.
  Prior art: alert debounce. Better by: the claim is re-checked at task finish and withdrawn if the sibling change landed. Novelty: 2.
  Done when: replaying those three commits yields zero surfaced alarms, and a true one still surfaces.

- **Wild: Grow the guard from gene segments** (V(D)J recombination) — FEATURE — value 4 — effort L — risk med — category: guard
  Why: wild. The guard is hand-written rules; the corpus has only 124 cases.
  Prior art: grammar fuzzers generate inputs, not detectors. Better by: ~30 lines of verb, target and flag segments expand into 200+ candidate rules, and any rule that matches the user's accepted history is deleted before release. Novelty: 4.
  Done when: the expansion yields survivors that block at least one corpus case the fixed rules miss, with zero hits on accepted history.

- **Wild: Add a dirty-room exam item** (hygiene hypothesis) — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild. Lanes always start in pristine worktrees, which may make agents brittle on real trees (stale lock, half-edited file, wrong branch).
  Prior art: chaos engineering; SWE-style benchmarks use clean checkouts. Better by: seeds realistic mess without destructive steps. Novelty: 3.
  Done when: the exam scores one task in a seeded-mess tree and reports a pass-rate gap against the clean version.

- **Wild: Score foreign code for tissue match** (transplant typing) — FEATURE — value 3 — effort M — risk low — category: review
  Why: wild. Pasted or other-agent code is the closest thing to a graft, and the cold reader only checks logic.
  Prior art: linters check rules, not fit. Better by: one score from naming, error style and imports against neighbouring files, with the worst mismatches shown. Novelty: 3.
  Done when: a pasted foreign function scores below a house-written one in a fixture, and its top three mismatches are named.

Next question: which of Foreman's signals fire on an absence (no trailer, no heartbeat, no edit event), and which are only pattern matchers?
Next question: which approvals or lessons are tolerated today only because no one has ever checked what they were learned from?
