# Brainstorm — lens: unspoken needs

**Questions left earlier, answered through this lens:**
- Poisoned input: the learners that read issue and CI text and then write lessons or tasks are the likeliest never to have faced a poisoned input, because their input is the only place an outsider's words enter. I can't confirm from the pack that none has been tested.
- Trusted gauge: the pack shows no gauge checked against ground truth. The three dropped breakage-ahead alarms suggest the detectors have no measured precision.

**Ideas**

- **Retest lessons when the model changes** — FEATURE — value 4 — effort M — risk low — category: memory/lean
  Why: assumption: many lessons patch an older model's habits, and the Claude 5 family keeps arriving. Prior art: none found. Better by: each lesson records its origin model, and on a new model its incident is replayed once. A lesson the new model passes unaided is demoted to "unneeded" and stops being injected (the way maternal antibodies wane). Novelty 4.
  Done when: after a model-ID change, `fm doctor` lists lessons as retained or demoted, each with a replay result, and demoted ones drop out of the injected context.

- **Prime neighbour repos when one is hit** — FEATURE — value 4 — effort M — risk low — category: cross-repo
  Why: assumption: the user has several repos on one machine, and the pack shows a cross-repo goal picker. Prior art: Dependabot works per repo. Better by: a failure class caused by a dependency version, workflow action or lockfile pattern triggers a local exposure scan of the other repos, which get pre-armed checks. This mimics interferon alerting nearby cells. Nothing leaves the machine. Novelty 4.
  Done when: a fixture failure in repo A produces a "repo B shares this exposure" note in B's next session.

- **Catch fixes that win by weakening the detector** — SECURITY — value 4 — effort M — risk med — category: fix integrity
  Why: CI-red FIX tasks are captured automatically, and 66% of developers complain about near-miss AI output. Prior art: mutation testing, but nothing that diffs a fix for lost strength. Better by: antibiotic resistance selects the evasive variant, so this compares test files before and after a FIX for removed assertions, new skips, loosened expectations and added retries. Novelty 3.
  Done when: a fixture FIX that deletes an assertion is flagged "green by weakening" at `fm task finish`.

- **Trace contacts of a bad commit and recall them** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: ship bets are settled by CI and tasks run in parallel lanes. Prior art: bisect finds the culprit but nothing finds what depended on it. Better by: once commit C is proven bad, list the tasks, lanes and ship bets whose verification ran on a tree containing C and re-verify them, as in a product recall. Novelty 4.
  Done when: marking a commit bad lists the dependent tasks and files re-verify items for them.

- **Keep memory in the tissue: per-directory lesson sidecars in git** — FEATURE — value 4 — effort L — risk med — category: memory/team
  Why: the pack says memory files go stale and differ between tools. Prior art: nested CLAUDE.md and AGENTS.md, which are hand-written and have no evidence or expiry. Better by: machine-written, evidence-linked lessons that expire, travel with branches and merge through git, so an abandoned branch's lessons die with it. It is opt-in, since it publishes into the repo. Novelty 3.
  Done when: with the setting on, a lesson committed on a branch is recalled by a fresh clone and absent after the branch is deleted.

- **Turn public fix notes into guard replay cases (convalescent serum)** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the frontier lists host fixes such as deny rules on nested compound commands (v2.1.289). Prior art: CVE-driven regression tests, but none found in a harness. Better by: `fm research ask` output is converted into labelled replay cases, so Foreman knows whether its own guard fails the same way before a user hits it. Novelty 3.
  Done when: one release note yields at least one labelled case in `fm replay` with a verdict.

- **Confirm in two tiers and report each detector's precision** — FIX — value 4 — effort M — risk low — category: trust
  Why: three breakage-ahead alarms were dropped as false, and the trust questions are open. Prior art: none found; anergy asks for two signals but not for sequential tests of different design. Better by: a cheap screen with high sensitivity, then a differently built confirmatory check, then a state shown as "screen-positive" or "confirmed". Each detector's positive predictive value is published. Novelty 3.
  Done when: `fm doctor` shows PPV per detector, and a screen-positive item is never worded as fact.

- **Compile a recurring FIX into a narrow, expiring fixer (phage)** — FEATURE — value 4 — effort L — risk med — category: automation
  Why: CI-red FIX tasks recur and flaky reruns exist. Prior art: Renovate and codemods are generic. Better by: a script built from the user's own repeated fix diffs for one failure signature, tested on its originals, that expires and asks before running. Novelty 3.
  Done when: three same-signature FIXes yield a draft fixer that reproduces all three diffs.

- **Read untrusted text only through an airlock child** — SECURITY — value 4 — effort M — risk low — category: injection
  Why: watchers and CI text are an outsider channel. Prior art: the dual-LLM pattern, rarely default. Better by: a tool-less disposable child reads the raw text and emits only a fixed schema with capped fields, and the main agent never sees the raw text. Novelty 2.
  Done when: a planted instruction in a fixture CI log never appears in the main context.

- **Titrate the guard dial on the user's own history** — FEATURE — value 4 — effort S — risk low — category: permissions
  Why: users report 15+ prompts in one session. Prior art: none found. Better by: replay a month of calls at each strictness and plot the prompts versus the blocks of replay-labelled harm. The user sets the dial at the knee of that curve. Novelty 3.
  Done when: `fm replay --titrate` prints prompts and misses per setting.

- **Measure the window period of defects** — FEATURE — value 3 — effort M — risk low — category: gauges
  Why: assumption: the user can't see how long defects live before capture. Prior art: DORA metrics. Better by: commits from introduction to capture, split by which detector caught it, so the slowest catcher shows. Novelty 2.
  Done when: `fm outcomes` shows a median lag per detector.

- **Keep a latent-infection register (wild)** — FEATURE — value 3 — effort M — risk low — category: debt
  Why: wild; assumption: skipped tests, quarantined flakes, workarounds and muted detectors suppress a problem without curing it. Prior art: debt trackers. Better by: like shingles, they reactivate under stress, so a large diff or dependency bump in the module resurfaces them. Novelty 4.
  Done when: touching a module with a skipped test and a big diff prints that item.

- **Map referred pain from symptom to fix site (wild)** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: wild; assumption: closed FIX tasks record both where a failure showed and where it was fixed. Prior art: fault localization from coverage. Better by: it learns the user's own displacement from symptom file to fix file, with no model call. Novelty 3.
  Done when: a new failure lists the likeliest fix files, and hit@3 is scored on closed FIXes.

- **Grow a repo organoid (wild)** — FEATURE — value 3 — effort L — risk med — category: testing
  Why: wild; assumption: exams and drills are costly on full repos. Prior art: generic fixture repos. Better by: a tiny miniature that keeps the user's real hazards (lockfile, migrations, secret patterns) as a cheap test bed for guard, learner and chaos drills. Novelty 4.
  Done when: the drills run on the organoid in under a minute and fail on a planted hazard.

Next question: which of Foreman's detectors has a known precision, and which has only ever been judged by the user dropping its output?
Next question: what does Foreman keep that was true only for an older model or host version, and who would notice when it stops being true?
