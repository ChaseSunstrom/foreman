# Brainstorm — lens: blind spots

I read the missed asks (T-2533 to T-2554) as one class: Foreman produced a number, note or learner and nothing checked its cost, source, liveness or novelty. The question a brainstorm should have asked is "who audits the auditor, and what did the auditor read?" I put that to the whole project through immune-system mechanisms.

- **Require two independent signals before any self-authored rule goes live** — FEATURE — value 4 — effort M — risk low — category: learners
  Why: anergy, where one signal without a second confirming signal is ignored. T-2554 showed one polluted input (test captures) steering the user model. Today a single source can promote a lesson, steer or trigger. Prior art: none found in coding harnesses. Novelty 4.
  Done when: a lesson, trigger or guard-rule draft backed by one source stays "pending" and is not injected, and a second independent source (a different task or a different origin tag) promotes it. A test proves this.

- **Make every new detector pass a "thymus" replay of the user's own history** — FEATURE — value 4 — effort M — risk low — category: guard, learners
  Why: negative selection. The dropped list holds three "Breakage ahead" false alarms, all firing on Foreman's own commits. Candidate detectors, lessons and guard rules should be deleted before release if they fire on known-benign history.
  Done when: `fm` refuses to enable a candidate that fires on more than N% of the last 90 days of benign events. It prints which past event tripped it.

- **Issue retractions for claims that turn out false** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: assumption: nothing recalls a wrong receipt, lesson, bet read or digest line once it has been injected or published. Give each claim an id. When one is disproven, the next session shows a correction line and every learner that consumed it is re-run.
  Done when: marking claim C as false makes the next SessionStart show "retracted: C, why", and the lessons and ledger rows derived from C are flagged.

- **Add a fever mode that freezes learning and unattended work together** — FEATURE — value 3 — effort M — risk med — category: safety
  Why: the risk budget lowers autonomy per harm, but nothing changes system-wide. On a detected infection (a learner found poisoned, CI red on main, a guard bypass), pause the triggers, freeze the learners, force cold reads and raise the checks until the user clears it.
  Done when: a planted poisoned lesson trips fever, a trigger-fired lane refuses to start, and `fm doctor` names the cause and the clear command.

- **Learn each project's self-profile and flag lane deviations as danger signals** — FEATURE — value 4 — effort L — risk med — category: observability
  Why: the danger model reacts to damage, not foreignness. Per project, keep typical diff size, test count, deleted lines and command set. Pause a lane whose diff is 10× normal or whose test count drops.
  Done when: a fixture lane that deletes 40% of the tests is paused mid-run with a one-line reason, and a normal lane is not.

- **Share one attention budget across every emitter** — FEATURE — value 4 — effort M — risk low — category: simplicity
  Why: T-reg regulation of a cytokine storm. Notes, yes-cards, heads-ups, digests and flags are capped per detector, but nothing arbitrates between them. The user asked three times to cut noise (steers on lean and quiet).
  Done when: a session with 8 pending emitters shows at most K lines, ranked by expected loss. The suppressed ones are listed in `fm doctor`.

- **Replay the earlier fix first when a failure signature recurs** — FEATURE — value 3 — effort M — risk med — category: memory
  Why: the memory-cell second response. Captured FIX tasks from CI red are filed fresh each time. Store signature → winning diff, and offer it as the first candidate lane.
  Done when: a repeated red signature starts a lane seeded with the stored patch. The receipt says "second response".

- **Turn repeated approval prompts into one allow rule, checked against the guard corpus** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: the frontier reports 15+ approvals per session because prefix allow lists collide with structure checks. The proposed rule must replay clean through the 124-case corpus before the yes-card appears.
  Done when: after 3 identical approvals a card proposes the narrowest rule. Accepting it removes the prompt in a replayed session, and the corpus stays green.

- **Log every sandbox escape-hatch use as one readable line** — SECURITY — value 3 — effort S — risk low — category: audit
  Why: the frontier issue (closed "not planned") asked for opt-in escape plus audit logging, and the vendor declined. Foreman can supply the log itself.
  Done when: an unsandboxed call appends `time, command, reason` to a local file, and `fm doctor` counts this week's calls.

- **Give exam items stable content ids so extending the exam never reassigns old ones** — FIX — value 3 — effort S — risk low — category: measurement
  Why: the steer on the fifth BEYOND row said adding one reassigns most items through `hash % len`, and recorded runs would stop being comparable.
  Done when: adding an item leaves every existing item's id and assignment unchanged. Run comparison skips items whose hash differs.

- **Re-derive each gauge through an independent slow path nightly** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: this answers the earlier question about gauges never checked against ground truth. A second implementation (recount from raw transcripts) is diffed against the printed gauge, and a mismatch is a finding.
  Done when: a planted miscount in one gauge shows up in the next night digest as "gauge X disagrees with recount".

- **Wild: run an autoimmune drill that tries to make Foreman attack itself** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: wild. A blind child makes a harmless change meant to trip the guard, breakage-ahead or the lean ratchet on Foreman's own repo, and each false alarm becomes a corpus case. Prior art: none found. Novelty 4.
  Done when: a drill run yields at least one new labelled corpus case, or a "none found" line.

- **Wild: hold a weekly germinal-centre tournament for the noisiest detector** — FEATURE — value 3 — effort L — risk med — category: learners
  Why: wild. Affinity maturation. A child writes mutated variants of the lowest-precision trigger or detector. Variants are scored on the replay corpus, and the best one is offered as a diff for the user's yes.
  Done when: a variant with higher precision at equal recall is offered with its numbers, and nothing installs without a yes.

- **Wild: export an opt-in "antibody bundle" for a new install** — FEATURE — value 2 — effort M — risk med — category: privacy
  Why: wild. Passive immunity. The user may export redacted, hash-only guard cases and lesson digests so a fresh install starts with a tuned guard. Nothing leaves the machine without an explicit setting.
  Done when: the bundle contains no paths, strings or secrets (a scan test proves it), and import stays quarantined until the thymus replay passes.

Next question: which of Foreman's outputs can a user act on that Foreman has no way to retract once published?
Next question: what does Foreman do when two of its own detectors, learners or gauges disagree, and who is shown the disagreement?
