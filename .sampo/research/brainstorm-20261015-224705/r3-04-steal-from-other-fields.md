# Brainstorm — lens: steal from other fields

- **Teach each fix its contraindications** — FEATURE — value 4 — effort M — risk low — category: learned fixes
  Why: from pharmacy labels. The learned-fix store (T-1032) scores hits and misses but doesn't say *when not* to apply a fix. The user's ask is "apply it every time", so a fix that misfires only on, say, node<20 gets retired instead of narrowed (assumption: misses are recorded with their environment).
  Done when: after a fix misses, `fm fixes show ID` lists a "not when" condition derived from the miss-vs-hit context diff (OS, tool version, branch, path). A replay where that condition holds skips the fix, and the receipt says why.

- **Post a double-entry trial balance at close** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: from accounting. Every changed hunk must be "posted" to an acceptance criterion or plan step. The user's pack shows scope drift ("chases every new idea") and plan-bigger-than-request warnings only at plan time. Nothing audits the finished diff.
  Done when: `fm task finish` on a diff with a hunk linked to no criterion prints an unposted "suspense" list (file:hunk) and refuses until each one is annotated or dropped.

- **Show an animatic before building UI** — FEATURE — value 4 — effort M — risk low — category: pane
  Why: from animation pre-visualisation. The user keeps steering the pane after seeing it ("still cluttered", "graphs too big", "fill the dock"). Goldens lock a look only after it's built.
  Done when: a UI-tagged task's plan step 0 stores a plain-text frame of the intended pane at 120×40 and 36 columns. The close check compares the real fixture render's section order and row counts to the approved frame and fails on mismatch.

- **Add a placebo arm to improvement experiments** — FEATURE — value 3 — effort S — risk low — category: self-measurement
  Why: from clinical trials. `fm improve` plans an A/B holdout, but any extra instruction may change behaviour regardless of content. Without a sham arm, a "win" can be a Hawthorne effect (assumption: holdout compares rule vs none).
  Done when: an experiment can run three arms (rule, none, same-length inert text). The report flags a win as "not beyond placebo" unless the rule beats the sham arm.

- **Carry the commander's intent into every replan** — FEATURE — value 3 — effort S — risk low — category: plan integrity
  Why: from military doctrine. Resume capsules and plans store steps but not the purpose or the non-negotiables. A builder that replans mid-task has nothing to check its new plan against.
  Done when: `fm task plan` accepts an intent line (purpose plus "never trade off X"). A replan that edits or removes steps touching X is held for a decision, and the intent shows in the resume capsule.

- **Explore routes with a Thompson-sampling bandit** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: from bandit theory. Model/effort tables and card injection are chosen from past data only, so they never learn that a cheaper option would have passed. Assumption: pass/fail is attributable per task class.
  Done when: with a 10% exploration quota, the router occasionally tries the next-cheaper model or effort for a task class. The outcome goes in a counterfactual log, and `fm digest` shows each class's pass rate by arm.

- **Keep a punch list and gate release on it** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: from construction handover. Compromises like skipped tests, hardcoded values and "good enough" calls disappear into prose. Deferred items pile up (30+ open) and T-0431 shows release work waiting.
  Done when: `fm task finish --accept "reason"` writes a typed punch item. `fm release` lists open items and refuses while any is older than 14 days.

- **Declare a load-shedding order** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: from power-grid brownout plans. Pacing and daily caps exist, but when spend or rate limits near the ceiling nothing says what gets dropped first, so a brainstorm can starve a gate.
  Done when: a configured ladder (brainstorm → speculative lanes → night jobs → reviewers, never gates) is applied at 80% of the cap. The ledger records each shed with the cap it was shedding for.

- **Sign a turnaround contract at plan time** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: from mountaineering and Ulysses contracts. Cap and tier tripwires exist, but nothing pre-commits against in-the-moment overrides. Assumption: unattended runs overrun on summit fever.
  Done when: `fm bind --turnaround 40% --scope 6files` is enforced by a hook. Lifting it mid-task needs a typed reason and waits 60 seconds.

- **Halt a lane when its diff breaches a volatility band** — FEATURE — value 3 — effort S — risk med — category: runaway control — wild
  Why: from stock-exchange circuit breakers. Plan-size warnings run only at plan time. A lane that suddenly churns 40 files against a 5-file plan gets no run-time brake.
  Done when: a lane whose changed-file count or lines per minute exceeds its band (a multiple of the plan estimate) pauses for a "re-read intent" prompt, and the halt is logged.

- **Post a "days since a never-event" sign** — FEATURE — value 3 — effort S — risk low — category: trust — wild
  Why: from factory safety boards and hospital never-events lists. Foreman guards many things but shows no single streak. Assumption: about 8 outcomes can be named (secret committed, ungated push, user file destroyed).
  Done when: each never-event has a detector over the ledger and git, and the pane's idle line shows days since the last one. A trip resets the count and links to the incident.

- **Hold a machine roll call through git** — FEATURE — value 3 — effort S — risk low — category: portability — wild
  Why: from ham-radio nets. The user wants fixes shared across sessions, clones and machines. A pulled brain can be silently stale or on an old Foreman version, and no one knows.
  Done when: each Foreman appends a one-line check-in (brain hash, version, last sync) under `.foreman/roll/`. `fm roll` lists the machines and flags any that is more than 7 days stale or on a different brain hash.
