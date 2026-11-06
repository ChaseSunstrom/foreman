# Brainstorm — lens: unspoken needs

- **Count correlated signals once (superantigen guard)** — FEATURE — value 4 — effort M — risk low — category: signals
  Why: assumption: many earlier ideas ("require two signals", fever, T-reg storm cap) assume the signals are independent, but one pasted log or one CI red can trip several detectors at once. Prior art: none found; alert deduplication exists in ops tools but not as an independence test on a harness's own learners. Better by: each signal records its source event id, so two signals from one event count as one before anergy or fever logic acts. Novelty: 4.
  Done when: a test feeds one event that trips three detectors and the confirmation count is 1; two events on different files count as 2.

- **Test every guard rule against lookalikes (molecular mimicry)** — FIX — value 5 — effort M — risk low — category: guard
  Why: the dropped "brief-guard path false positives" and the user's repeated requests to fix false alarms show benign inputs resembling bad ones. Prior art: none found; guard corpora hold known-bad and known-good cases, not generated near-misses. Better by: for each rule, derive benign variants (renamed flag, quoted path, comment text) and require the verdict to stay "allow". Novelty: 3.
  Done when: `fm replay` reports a mimicry set per rule and a rule that blocks any variant fails CI.

- **Detect first-fix anchoring (original antigenic sin)** — FEATURE — value 4 — effort M — risk med — category: lessons
  Why: assumption: lessons recalled per file may keep steering later work toward the first remedy recorded for that file after the real cause has changed. Prior art: none found; memory tools store lessons but don't measure their lock-in. Better by: flag a lesson that was recalled N times while its file's failures changed signature, and demote it. Novelty: 4.
  Done when: a fixture where a lesson is recalled for three differing failures gets flagged "anchoring" in `fm doctor`.

- **Age the detectors (immunosenescence audit)** — CLEAN — value 3 — effort S — risk low — category: ratchets
  Why: the pack shows many learners (triggers, lessons, rules) but no view of how old each is or when it last fired correctly; the user keeps asking for "known alive" reads. Prior art: none found. Better by: one table giving each learner's birth commit, last true catch and last false alarm, with the oldest silent ones listed for retirement or a booster test. Novelty: 3.
  Done when: `fm doctor` prints the table and lists any learner with no true catch in 90 days.

- **Re-expose old rules to their incident (booster shot)** — FEATURE — value 3 — effort M — risk low — category: replay
  Why: assumption: a rule's protection fades when the host CLI or its parser changes, and the 124 replay cases only test it as written. Prior art: none found. Better by: each night, replay the original incident of the oldest rule against the current host; a miss files a FIX task. Novelty: 3.
  Done when: a rule whose behaviour is broken by a mock host change is flagged by the next night tick.

- **Mark self-destruct dates on every learned artifact (apoptosis by default)** — CLEAN — value 4 — effort M — risk med — category: lean
  Why: the user steered on lean growth, subtraction by evidence and dead steers; learned artifacts only get added. Prior art: none found; caches have TTLs but lessons, triggers and rules don't. Better by: each learned item carries an expiry that only a recorded catch renews, so deletion becomes the default. Novelty: 4.
  Done when: an item with no catch past its expiry disappears from injection and shows once in the digest as "expired".

- **Catch slow drift that looks like self (immunoediting watch)** — FEATURE — value 4 — effort L — risk med — category: drift
  Why: lean ratchets and the guard catch sudden growth; cancer-style escape is a thousand small, individually acceptable changes (hook note chars, rule count, latency creeping up). Prior art: none found; trend alerts exist in monitoring but not tied to a harness's own ratchets. Better by: fit a slope to each lean metric across generations and warn on a persistent climb even when every step passed. Novelty: 3.
  Done when: a synthetic history with +1% a commit trips a drift warning while each step stays under its ratchet.

- **Sickness behaviour on self-detected damage** — FEATURE — value 3 — effort S — risk low — category: restraint
  Why: assumption: when Foreman's own organs fail (a hook crash, dead timer), more proactive output hurts. Prior art: none found; the pack's "fever" idea throttles caution, not chatter. Better by: Foreman goes terse, drops nudges and says one line, "I'm unwell: X", until the check passes. Novelty: 4.
  Done when: with a forced hook failure, a session's injected notes drop to the one status line.

- **Wild: Wall off immune-privileged files** — FEATURE — value 3 — effort S — risk med — category: guard
  Why: wild; assumption: reaction around tower files or the user's hand-edited files is more costly than elsewhere, as the brain is shielded from inflammation. Prior art: none found. Better by: for a named set, Foreman only observes and reports, never blocks or reverts. Novelty: 4.
  Done when: an edit to a privileged path is logged but never blocked, and `fm doctor` lists the set.

- **Wild: Clean-room hygiene test for overreaction** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild; hygiene hypothesis: learners trained only on tidy projects overreact on messy ones. Prior art: none found. Better by: run the guard and triggers on a deliberately messy fixture repo and count unexplained alerts. Novelty: 4.
  Done when: the exam reports an alert-per-session count on the messy fixture, with a ceiling.

- **Wild: Eat-me tags for dead state (efferocytosis)** — CLEAN — value 3 — effort M — risk low — category: state
  Why: wild; the user dropped captured-by-mistake items and test captures that kept polluting the user model. Prior art: none found. Better by: any item that is dropped, mistaken or moot carries an "eat me" tag and every learner must skip and then purge it within a day. Novelty: 3.
  Done when: a dropped item no longer appears in any learner's input after the next tick.

- **Label tolerated helpers (oral tolerance)** — FEATURE — value 3 — effort S — risk low — category: approvals
  Why: the prompt-frequency complaints suggest the same safe helper commands are asked about again and again. Prior art: Claude Code allow lists match prefixes. Better by: a command that passed N times with no harm on a path gets quietly marked tolerated, and the label is dropped after harm. Novelty: 2.
  Done when: a command that repeatedly ran safely stops prompting; one harmful run revokes it.

Next question: which of Foreman's alarms and learners share an upstream event, so they can be fooled together?
Next question: what would the user be most upset to learn Foreman silently deleted or ignored because it looked like "self"?
