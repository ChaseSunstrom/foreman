# Brainstorm — lens: unspoken needs

**Answers to earlier questions (my lens only)**
- *Which learner was never poisoned on purpose?* The pack shows the user model absorbed test captures and mistaken captures (T-2554). Lessons recall, trigger precision and the calibration ledger have no poisoned-input test that I can see.
- *Which gauge is trusted but never checked against ground truth?* The trigger-precision and bet-Brier numbers. Both are scored from outcomes Foreman itself files or labels.

**Ideas**

- **Run negative selection on every new detector** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: brief-guard false positives (T-2499–2504 era) and noisy triggers were found only after firing. Prior art: none found in coding harnesses (WAFs test rules, but not against the owner's own history). Better by: before any new guard rule, trigger or forecaster goes live, replay it against the user's "self" corpus (their accepted commands, kept diffs, benign captures). It is deleted if it fires on self, so false positives die before release. Novelty: 3.
  Done when: a rule that blocks a command from the user's accepted-command history is refused at `fm ship`, with the offending case named.

- **Require a second signal before a learner acts (tolerance/anergy)** — FIX — value 5 — effort M — risk low — category: learners
  Why: test-fed and mistaken captures polluted the user model. Prior art: none; memory tools write on one signal. Better by: a lesson, steer or forecast input changes behaviour only when a second, independent signal confirms it (a git outcome, a repeat, a CI result). A single unconfirmed signal is held as inert. Novelty: 4.
  Done when: a test feeds one fake capture and the forecast is unchanged; adding a confirming git outcome changes it.

- **React to damage, not command shape (danger model)** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: users report 15+ prompts per session because prefix matching and structure flagging disagree. Prior art: sandboxes and allow-lists classify the command up front. Better by: pre-allow more, then run a damage sensor after each step (files deleted, test count dropped, writes outside the repo, new network targets). A hit rolls back from a checkpoint and steps the risk budget down. Novelty: 4.
  Done when: a scripted lane that deletes 30 test files after an allowed call is reverted and demoted, with zero prompts for the benign calls before it.

- **Vaccinate every learner nightly with attenuated poison** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: poisoned-input question left open. Prior art: none found. Better by: the night tick feeds each learner a labelled harmless poison (fake capture, hostile issue text, forged outcome). `fm doctor` shows each learner's last-vaccinated date and whether it resisted. Novelty: 4.
  Done when: `fm doctor` lists every learner with a vaccination result, and a deliberately weakened learner shows FAIL.

- **Enter a whole-system fever on clustered harm** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the risk budget steps down per autonomy, but triggers, night tick and drafts keep running. Prior art: none. Better by: three harm signals within a window (revert, red CI, guard block) freeze all unattended starts, tighten gates and show a status-line state. It lifts itself after a clean window. Novelty: 4.
  Done when: replayed signals freeze triggers and the state clears automatically after a quiet period.

- **Regulate proactive output with one suppressor (T-reg)** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: dozens of earlier ideas each add a nudge, flag or card. Prior art: per-feature caps only. Better by: one cross-component cap on unsolicited notes per session, scaled down by recent dismissals and up by confirmed hits. Novelty: 3.
  Done when: a session that triggers 10 sources shows at most N notes, with the rest queued.

- **Key memory on failure signature for a fast second response** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: lessons are recalled per file, not per failure. Prior art: per-file memory. Better by: a ledger of failure signatures and the fix that worked. On a repeat CI red, the known fix is drafted as a patch within seconds. Novelty: 3.
  Done when: a repeated seeded failure gets a drafted patch citing the earlier fix.

- **Quarantine a bad lane's output locally (inflammation)** — FEATURE — value 3 — effort M — risk low — category: containment
  Why: assumption: a harmful lane today halts or taints too much. Prior art: worktrees. Better by: its commits and learner inputs are tagged tainted, and dependents are blocked until a cold read clears them. Novelty: 3.
  Done when: a lane marked harmful cannot feed lessons or the user model until cleared.

- **Mature guard rules by affinity (clonal selection)** — FEATURE — value 3 — effort L — risk med — category: guard
  Why: the replay corpus (124 cases) gives a fitness function. Prior art: none found. Better by: nightly, a tool-less child mutates the best-blocking rules into variants, replay scores them, and only strictly better ones are proposed to the user. Novelty: 4.
  Done when: a proposal appears only if it beats the parent on corpus score and fires on no self case.

- **Grade responses on a ladder (complement cascade)** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: prompts are binary; fatigue comes from asking too early. Better by: hint, then require reason, then ask, then deny, with each rung logged. Novelty: 2.
  Done when: a repeated borderline call escalates one rung per recurrence.

- **Wild: Export a signed antibody pack to a new repo** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: wild. Assumption: a new repo starts naive. Better by: only rules with several confirmed blocks, stripped of paths, are offered on a local export or import, with nothing sent anywhere. Novelty: 4.
  Done when: a fresh repo imports the pack, and a path-leak scan finds none.

- **Wild: Use a naive-cell reviewer on the day's anomalies** — FEATURE — value 3 — effort S — risk low — category: review
  Why: wild. Better by: a tool-less child that has never seen the session reads only a digest of what a lane touched (antigen presentation) and says what looks foreign. Novelty: 4.
  Done when: a planted odd edit is named from the digest alone.

- **Wild: Run an autoimmunity drill on each Foreman release** — FEATURE — value 4 — effort S — risk low — category: release
  Why: wild. Better by: before install, the new version replays the user's last month of normal work and must block nothing the user did. Novelty: 3.
  Done when: a release that blocks a past kept command fails the drill.

Next question: which of Foreman's own protections have ever blocked something the user then did by hand anyway, and was that treated as a miss in the gauges?
Next question: what would one clean "self" corpus (accepted commands, kept diffs, benign captures) have to contain for several of these checks to share it?
