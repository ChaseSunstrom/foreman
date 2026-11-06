# Brainstorm — lens: reliability

Lens: reliability, using immune-system mechanisms. Ideas are ordered best first.

- **Run a thymus school for every new guard rule** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the brief-guard path false positives (two dropped tasks) are autoimmunity: a rule that reacts to self.
  Prior art: none found. Rule tests exist, but none auto-delete a rule that fires on the user's own history.
  Better by: before release, each rule replays against the user's real command and transcript history. A rule that blocks known-good work is rejected, not tuned.
  Novelty: 4
  Done when: a rule that matches 1 labelled-good historical call fails `fm replay --thymus` and cannot ship.

- **Require two signals before any learner updates** — SECURITY — value 5 — effort M — risk low — category: learners
  Why: an earlier brainstorm asked "which learner has never seen a poisoned input?". Tolerance and anergy answer it: a single signal is ignored.
  Prior art: none found. Memory tools commonly write on one observation.
  Better by: a lesson, trigger weight or user-model fact needs a second, independent confirmation (a different session or a CI outcome) before it affects behaviour.
  Novelty: 4
  Done when: a lesson planted once in a fixture is never injected; planted twice from separate sessions, it is.

- **React to damage, not foreignness** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: the guard matches command shapes, and the frontier shows prefix-matching approval prompts that fire constantly.
  Prior art: sandboxes and allow lists match foreignness; no harness is found that triggers on post-hoc damage.
  Better by: a damage sensor watches test-count drops, mass deletions, diff size spikes and secret-shaped additions. It steps autonomy down and rolls back whatever the rules never named.
  Novelty: 4
  Done when: a scripted lane that deletes 40 tests through an unlisted command is stopped and reverted within one tool call.

- **Inject a harmless canary into every learner nightly** — SECURITY — value 4 — effort S — risk low — category: vaccination
  Why: the open question about poisoned inputs, and the contamination-canary idea.
  Prior art: canary tokens exist for exfiltration only; none found for learner poisoning.
  Better by: the night tick plants a labelled fake into each learner's input, checks it was quarantined, then removes it. A learner that absorbs it turns doctor red.
  Novelty: 4
  Done when: `fm doctor` lists one vaccination result per learner, and a learner with its filter disabled in a test fails it.

- **Add a regulatory brake on reaction cascades** — FIX — value 4 — effort M — risk low — category: stability
  Why: risk-budget step-downs, captured FIX tasks from CI red, flaky reruns and trigger fires can each trigger the others. That is a cytokine storm.
  Prior art: retry caps and circuit breakers exist per call, not across reactions.
  Better by: one T-reg counter spans all self-started reactions. Past N reactions per hour the system only reports and never acts, and it logs why.
  Novelty: 3
  Done when: a simulated red CI that triggers a chain of 20 reactions stops at the cap, with one digest line.

- **Run a fever mode after harm** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the risk budget lowers autonomy per lane; nothing changes the whole system's posture.
  Prior art: none found.
  Better by: after a harm event, every lane gets a stricter state: a mandatory cold read, no unattended shipping, shorter leashes. It decays on a clean streak, with the reason visible.
  Novelty: 4
  Done when: a harm fixture flips the state, `fm status` shows it, and N clean tasks later it reverts.

- **Show an antigen fragment before every merge** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the cold reader gates tower files only. Reviewers read narrated summaries, not what is inside the lane.
  Prior art: diff review exists, but the lane writes its own summary.
  Better by: Foreman, not the lane, extracts a fixed fragment: the files touched, tests added or removed, new network or exec calls, and deleted assertions. It presents that to the inspector.
  Novelty: 3
  Done when: a merge of a lane that removed an assertion shows "assertions −1" in the fragment regardless of the lane's summary.

- **Keep memory cells for failure signatures** — PERFORMANCE — value 4 — effort M — risk low — category: recall
  Why: CI-red captures and flaky reruns start from scratch each time.
  Prior art: dedupe by error string in CI tools.
  Better by: a normalised signature (test, stack-shape, dependency delta) maps to the fix that held, with a survival count. The second occurrence opens with that fix as the first attempt.
  Novelty: 3
  Done when: the same planted failure the second time gets the recorded fix applied first, and it is dropped if CI is still red.

- **Contain inflammation to a path** — SECURITY — value 3 — effort M — risk med — category: containment
  Why: harm today steps autonomy down for the whole repo.
  Prior art: sandboxes limit by process, not by where damage was seen.
  Better by: harm in `src/x/` quarantines only that subtree for unattended lanes, and the quarantine lifts when tests there pass again.
  Novelty: 3
  Done when: after a harm fixture, a lane touching an unrelated path runs unchanged while the damaged path demands a human.

- **Measure the autoimmune rate** — FIX — value 4 — effort S — risk low — category: observability
  Why: trigger precision is measured, but not guard blocks that the user overrode or immediately redid by hand.
  Prior art: none found.
  Better by: a block followed by the user running the same intent counts as an autoimmune event. The per-rule rate is shown and a rule is auto-flagged at a threshold.
  Novelty: 3
  Done when: `fm doctor` shows per-rule override rates, and a rule that is overridden 3 times is flagged.

- **Wild: Affinity-mature the guard overnight** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: wild; assumption: the replay corpus can score variants.
  Prior art: none found. Fuzzers exist, but none breed rules.
  Better by: a night job mutates rules that caught real harm into variants. It keeps the ones that catch more labelled-bad cases and fewer labelled-good ones, and lists them as proposals for a human yes.
  Novelty: 5
  Done when: one run turns a seed rule into a proposal that catches at least one bad corpus case the seed missed.

- **Wild: Make a lymph-node drill of a pretend pathogen** — FEATURE — value 3 — effort M — risk low — category: drills
  Why: wild; the exam checks capabilities, not whether the response chain (guard, damage sensor, brake, fever) fires together.
  Prior art: chaos engineering, but not on an agent's own defences.
  Better by: weekly, a fake attacker lane tries an escalating sequence, and the report names the layer that caught it.
  Novelty: 4
  Done when: the drill prints a caught-by layer for each of 5 scripted attacks.

- **Wild: Add a blood test of the user's work** — FEATURE — value 3 — effort S — risk low — category: sensing
  Why: wild; damage sensing runs only in sessions.
  Prior art: none found.
  Better by: the night tick samples the repo for slow-onset damage (coverage drift, growing skips) and reports a single readout.
  Novelty: 4
  Done when: a planted rise in skipped tests appears in the next digest.

Next question: which of Foreman's defences have never been shown to catch damage that no rule names?
Next question: when two defences disagree (guard allows, damage sensor alarms), who wins, and has that ever been tested?
