# Brainstorm — lens: approaches

- **Hold single-signal learners anergic until a second signal confirms** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: Mistaken captures and test-fed lines entered the user model, and the "poisoned learner" question is still open. Every learner (lessons, trigger drafts, foresight, guard candidates) acts on one signal today. Approach: a learned item is anergic (recorded, never acting) until an independent second signal arrives, such as a red-then-green test, a user correction, or a different origin. Items with no second signal expire.
  Done when: a test feeds a poisoned lesson with one origin and it never reaches the SessionStart note, while the same lesson with a second origin does.
  Prior art: none found in coding harnesses; two-source confirmation exists only in alerting systems. Better by: it gates learning itself, by origin, not output. Novelty: 4

- **Run negative selection on every new learned rule before release** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: The brief-guard has path false positives, and 124 labelled replay cases already exist. Approach: any new guard rule, trigger, or lesson candidate is replayed against a "self" corpus (the user's accepted commands, commits, kept tasks). One firing on self is deleted before release.
  Done when: a candidate rule that blocks a command in the self corpus is rejected with the offending case named.
  Prior art: Forrest-style self/non-self host intrusion detection (1990s); none found in harnesses. Better by: the self corpus is the user's own history. Novelty: 4

- **Track autoimmunity: score each rule by how often the user overrides it** — FIX — value 4 — effort S — risk low — category: guard precision
  Why: Triggers have precision with auto-demotion, but guard rules do not. Approach: when a block is followed within minutes by the user running it by hand, or by an allow, that counts as a self-attack. A rule above a threshold drops to warn-only and files a task.
  Done when: replaying a log with five overrides of one rule demotes it to warn.
  Prior art: false-positive tuning in WAFs, by hand. Better by: automatic, per rule, and reversible. Novelty: 3

- **Raise a fever: one global caution state from co-occurring signals** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: The risk budget steps down per task only. Approach: when CI red, a guard block and a tower failure co-occur in a window, `fm` enters fever. Lane budgets shrink, the plan gate becomes mandatory, triggers go shadow-only, and notes get terser. It cools by itself after clean green runs.
  Done when: a replayed signal trio flips the state, and a recorded clean streak clears it.
  Prior art: none found; ops "incident mode" is manual. Better by: automatic, cross-component, and self-resolving. Novelty: 4

- **Regulate the response like T-regs, capping response by harm** — FEATURE — value 4 — effort S — risk low — category: storm control
  Why: Triggers, flaky reruns, and captured FIX tasks all react independently. Approach: one suppressor sums spend and fires per cause and mutes the rest once response cost exceeds a multiple of the harm.
  Done when: ten captures from one red CI produce one lane and nine suppressed rows.
  Prior art: retry circuit breakers, per service. Better by: it is cross-learner and keyed on cause. Novelty: 3

- **Add danger sensors that fire on damage, not on pattern** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: The guard is foreignness-based (fixed rules on calls). Approach: post-call sensors for damage (a mass deletion beyond baseline, a test count dropping, a secret-shaped string written, a sudden diff size). They step autonomy down and snapshot, regardless of what command did it.
  Done when: a novel command that deletes 40 files trips the sensor with no rule written for it.
  Prior art: Matzinger's danger model; file-integrity monitors. Better by: it catches commands no rule names. Novelty: 3

- **Replay memory cells: fingerprint a failure and replay its proven fix** — FEATURE — value 4 — effort M — risk med — category: speed
  Why: Lessons are recalled per file, but CI-red FIX tasks start from scratch. Approach: a failure fingerprint maps to the accepted patch; a second occurrence opens a lane with the patch pre-applied and a verify step.
  Done when: a repeated fingerprint opens a lane that goes green without deliberation.
  Prior art: auto-remediation runbooks. Better by: it is learned from accepted fixes, not authored. Novelty: 3

- **Present an MHC card of each lane's insides to the cold reader** — FEATURE — value 3 — effort S — risk low — category: review
  Why: The cold reader sees everything, which is costly. Approach: each lane emits 10 lines (files touched, commands run, network, deleted paths), and the inspector reads only the card unless it flags something.
  Done when: reviewer tokens fall and a seeded bad lane is still flagged.
  Prior art: PR summaries. Better by: it is machine-extracted, so it cannot be flattering. Novelty: 3

- **Swell a path: mark files implicated in a failure as inflamed** — FEATURE — value 3 — effort M — risk low — category: containment
  Why: Lessons are recalled per file but have no active quarantine. Approach: an implicated path gets temporary read-only status for unattended lanes and forces the plan gate, then heals after N green runs.
  Done when: an unattended lane's write to an inflamed path is refused, and it clears after a green streak.
  Prior art: code freezes, by hand. Better by: path-level, automatic, and self-healing. Novelty: 3

- **Do less: define "self" as a hash set of accepted command shapes** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: This is the cheapest version of the first two ideas, with no learning. Approach: one file of normalised command shapes the user accepted. Novel shapes are announced once and then self-label on acceptance.
  Done when: a new command shape triggers one note, and the second use is silent.
  Prior art: sudo and shell allowlists. Better by: it is built from history. Novelty: 2

- **Wild: vaccinate with a deliberately poisoned entry each night** — FEATURE — value 4 — effort M — risk low — category: assurance
  Why: assumption: nobody has tested the learners with bad input. A defanged poison (a fake lesson, a hostile issue text) is planted in a sandbox copy. If any learner acts on it, the failure becomes a task.
  Done when: removing the anergy gate makes the nightly vaccine fail.
  Prior art: chaos testing, canary tokens. Better by: it trains the defences, not just checks them. Novelty: 4

- **Wild: pass on passive immunity to a new repo** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: assumption: a new repo starts with no immunity. The user's generic, repo-stripped rules and override history seed it as read-only antibodies that expire unless re-confirmed.
  Done when: a new repo's first session blocks a known user hazard with no local history.
  Prior art: none found. Better by: it is private by construction, since only abstractions move. Novelty: 4

- **Wild: nightly affinity maturation of guard rules** — FEATURE — value 3 — effort L — risk med — category: guard
  Why: assumption: rules are written by hand. Each rule is mutated into variants (flags, paths, quoting). Variants that catch red-team evasions and pass negative selection multiply; the rest are discarded and a report is written.
  Done when: a night run adds a variant that catches a held-out evasion with no self hits.
  Prior art: evolutionary fuzzing and AIS research. Better by: the fitness is the user's own self corpus. Novelty: 5

Next question: which of Foreman's response mechanisms act on a single unconfirmed signal today, and which of those could lose the user work if the signal were forged?
Next question: when a defence is wrong, does anything measure the user's cost of it, or only the cost of a miss?
