# Brainstorm — lens: understanding the user

- **Read the project's season** — FEATURE — value 4 — effort M — risk low — category: intent
  Why: the requests move in phases (brainstorm, infrastructure, security, UI, now "how it thinks"), and the user steers when the phase changes. Foreman reacts to each request without noticing the phase. Assumption: the phase is visible in request types and ledger mix.
  Done when: `fm status` shows a one-line season (e.g. "hardening → polishing") derived from the last N requests, and a test replays a fixture ledger to the expected season. Next-task offers and the product check change tone with it.

- **Protect the user's muscle memory** — FEATURE — value 4 — effort M — risk low — category: stability
  Why: the pack proposes collapsing to about 25 verbs, pruning unused surface and deprecating commands, while the user runs 90+ `fm` commands daily. Nothing guards the commands they actually type. Assumption: command frequency is in the ledger.
  Done when: the top-N commands by the user's own usage are tagged habitual. Removing or renaming one fails the release gate unless an alias and a migration line exist.

- **Calibrate pushback from overrides** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: several of the user's requests were closed as "YAGNI" or "working as intended", but nothing records whether the user accepted that. Pushback is either too timid or too stubborn, and Foreman can't tell which.
  Done when: every decline stores its reason and the user's next reaction (accepted, re-asked, overrode). `fm friction` reports a re-insist rate per decline kind, and a decline kind with a high re-insist rate gets a softer default.

- **Fit the user's loss function** — FEATURE — value 4 — effort M — risk med — category: taste
  Why: the user complained about both guard false positives (refusals, the 75% budget block) and silent omissions (cleanup "never got done"). Their tolerance differs by error type, and Foreman treats them as equal.
  Done when: corrections are labelled by error type (over-block, under-do, over-build, wrong-guess, noise). A small table of weights is visible with `fm taste`, and at least one threshold, such as ask-vs-act, reads from it.

- **Show completion by request kind** — FEATURE — value 3 — effort S — risk low — category: attrition
  Why: cleanup requests died unnoticed, and the existing ideas fix cleanup specifically. This is the general version: a funnel per kind (cleanup, docs, deletion, UI, security) of asked → captured → done → verified.
  Done when: `fm friction` prints a table of per-kind completion rates, and a kind below the median by a set margin raises a captured task.

- **Tag which hat the user wears** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: Foreman is both the user's product and the tool they work with. "FIX: python3 -c refused" is a consumer complaint about the guard, while "T-0166 move band out of register.tsx" is an author's chore. Same words, different defaults.
  Done when: intake records hat (author, consumer, evaluating), inferred from project and phrasing and overridable in one word. The tag changes tier defaults and where the fix is routed, and a fixture test covers three examples.

- **Infer why each project exists** — FEATURE — value 3 — effort M — risk low — category: intent
  Why: projects differ in purpose (a personal tool, a published desktop app per T-0352, an experiment), and the right rigor, README polish and release bar differ with it. Assumption: purpose can be inferred from the remote, the release pipeline and the user's wording.
  Done when: each project has a purpose card with a confidence value, shown once at adoption for confirmation. At least two defaults (release gate strictness, docs depth) read from it.

- **Detect the decision the user keeps dodging** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: there are 16+ deferred tasks (T-0034, T-0035 and others). Some are deferred because the choice is hard, not because the work is low value.
  Done when: items viewed, listed or mentioned N times without a state change are flagged. Foreman proposes the smallest decision (a yes/no or a split) instead of the whole item, and the user can answer in one keystroke.

- **Steer the queue by theme budget** — FEATURE — value 4 — effort M — risk med — category: portfolio
  Why: the user redirected the second brainstorm from infrastructure to thinking. Rebalancing now takes a paragraph, and the 400+ queued tasks don't respond to it.
  Done when: `fm theme thinking=40 security=20 ui=20 infra=20` sets weights and the drive's offered next task follows them. Weekly drift against the weights is reported, and a test shows task order changing when the weights change.

- **Learn visual taste from reference apps** — FEATURE — value 3 — effort M — risk low — category: design
  Why: the user steered "beautiful UI with smooth animations" and the project has many UI ideas, but "beautiful" is undefined. Assumption: the user can supply screenshots or recordings of apps they admire.
  Done when: dropping reference images yields a token profile (radii, spacing, motion durations and easing). A lint compares the Desktop UI to it and lists the biggest deviations.

- **Wild: Read the workstation for implied values** — FEATURE — value 2 — effort S — risk med — category: personalization
  Why: wild. The environment says a lot unasked: a hardened kernel, a private-mail address, Arch and no sudo assumptions. These suggest privacy-first, minimal-dependency, no-telemetry defaults. Assumption: it is opt-in, local, and every inference is shown for ratification.
  Done when: `fm know-me --workstation` lists up to 5 inferred preferences with the evidence for each. Nothing is written until each is accepted, and nothing leaves the machine.

- **Wild: Mine shell history for the user's own repeated routines** — FEATURE — value 3 — effort M — risk med — category: automation
  Why: wild. Foreman learns its own repetition, but the user's repeated manual command chains outside Foreman (build, deploy, git dances) are the clearest evidence of unspoken wants. Assumption: opt-in, local, secrets redacted.
  Done when: the history is scanned locally and the top 3 repeated sequences are offered as `fm flow` candidates. Accepting one creates a tested flow, and a fixture history yields the expected candidates.

- **Wild: Know the user's reporters** — FEATURE — value 3 — effort M — risk low — category: stakeholders
  Why: wild. The user relays "new bug feedback" (T-0317) from other people. Foreman treats a relayed report like the user's own and loses who it came from, how technical they are and what they care about.
  Done when: relayed items carry a reporter tag with a short profile built from past reports. The brief states the reproduction at that reporter's level, and Foreman drafts a reply in the user's voice for the user to send.
