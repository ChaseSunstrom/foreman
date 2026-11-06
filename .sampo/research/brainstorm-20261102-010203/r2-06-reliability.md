# Brainstorm — lens: reliability

- **Sweep for missing-self (NK cells)** — FEATURE — value 4 — effort M — risk low — category: provenance
  Prior art: provenance stamps and SBOMs check presence on request; no harness has a standing patrol that flags what lacks a mark. Better by: it catches silent loss, not foreignness: unstamped state rows, un-receipted finishes, ledger entries with no task id. Novelty: 4.
  Why: the pack shows silent-death and write-only-field concerns, and "Stamp every self-started artifact with its origin". Done when: `fm night` flags a planted ledger row that lacks a task id and tree hash, and ignores a stamped control row.

- **Audit lessons for original antigenic sin** — FEATURE — value 4 — effort M — risk low — category: learners
  Prior art: memory staleness checks use age only. Better by: it re-tests the oldest lessons against a fresh-context arm and flags those whose recall steers toward a worse fix than a no-lesson run. Novelty: 5.
  Why: assumption: lessons recalled per file imprint on the first incident. The pack asks which learners were never poisoned or checked. Done when: a planted lesson with an outdated fix is flagged because the no-lesson arm beat it on a replayed task.

- **Cap epitope spreading in rules** — FIX — value 4 — effort S — risk low — category: guard
  Prior art: none found; rule linters check shadowing, not drift. Better by: each rule stores the incident that spawned it, and widening beyond the incident's shape past a set breadth needs a second incident. Novelty: 4.
  Why: the brief-guard path false positives look like over-generalised rules. Done when: widening a rule's pattern past its cap fails `fm check` unless a second incident id is cited.

- **Keep a commensal registry and a dysbiosis gauge** — FEATURE — value 3 — effort M — risk low — category: noise
  Prior art: baseline and "known issue" lists in linters. Better by: tolerated oddities (known flake, benign warning) are listed with an owner and a proportion gauge, so the harm is in the growth of tolerated noise, not in any single warning. Novelty: 4.
  Why: the pack has a flake ledger and a "refused full check" flake concern, and no measure of how much is being tolerated. Done when: `fm doctor` shows tolerated items as a share of all signals and WARNs when the share rises 2x over 14 days.

- **Declare immune-privileged sites** — FEATURE — value 3 — effort S — risk med — category: autonomy
  Prior art: protected-paths lists block edits, not reactions. Better by: some paths (tower files, ledgers) are exempt from automatic reactions such as demotion, rollback and revert, because collateral damage there costs more. Reactions there become an ask. Novelty: 4.
  Why: assumption: reactions to harm have hit state that should not auto-change (the aliasing and silent-fallback items). Done when: a planted harm signal on a privileged path files a yes-card and takes no automatic action.

- **Add a p53 checkpoint that makes a corrupt learner self-delete** — FEATURE — value 4 — effort M — risk med — category: learners
  Prior art: circuit breakers stop calls; none delete state. Better by: each learner runs a cheap integrity probe on load, and when it fails the learner quarantines its own store and rebuilds from append-only sources. Novelty: 4.
  Why: the pack proposes poisoned-input tests and rebuilding the user model from append-only sources. Done when: a corrupted lesson store is quarantined at load and rebuilt, with one doctor line naming the cause.

- **Track antigenic drift of the host CLI** — FEATURE — value 4 — effort M — risk low — category: hosts
  Prior art: version pins and changelog reads. Better by: it hashes the shape of hook payloads and tool-call schemas per host version, and measures a drift distance that decides which parts of the replay corpus must re-run. Novelty: 3.
  Why: the frontier shows Claude Code and Codex shipping permission and hook changes weekly. Done when: a changed fixture payload shape raises drift above threshold and names the guard cases it touches.

- **Do tissue typing on imported packs and lessons** — SECURITY — value 3 — effort M — risk low — category: imports
  Prior art: signing and checksums say who made it, not whether it fits. Better by: an imported rule or lesson pack is checked against the host repo's own history before it acts, and a mismatch (graft-versus-host) quarantines it. Novelty: 4.
  Why: assumption: antibody-pack export and cross-machine sharing are coming, per the earlier ideas. Done when: a pack with a rule that blocks a command the repo ran safely 20 times is held, not loaded.

- **Tag suspect artifacts with a decaying opsonin** — FEATURE — value 3 — effort S — risk low — category: taint
  Prior art: taint tracking within one run. Better by: a persisted tag travels with an artifact across sessions and reaches the cold reader, finish and ship, then decays when a clean verification clears it. Novelty: 3.
  Why: assumption: warnings today are per-session and lost on resume. Done when: a tagged file shows its tag in `fm ship` after a restart, and the tag clears after a passing check.

- **Wild: run a human-challenge trial** — FEATURE — value 4 — effort L — risk low — category: exam
  Prior art: mutation testing breaks code, not the surrounding protection. Better by: a scratch clone re-introduces one real past regression, then times which layer caught it (guard, test, cold reader, CI) and which none did. Novelty: 4.
  Why: wild; assumption: the 124 guard cases and the exam cover detection but not the detection path. Done when: a trial on a closed FIX reports the catching layer and time, or "uncaught".

- **Wild: apply the sentinel-node pattern to state migrations** — FEATURE — value 3 — effort M — risk low — category: upgrades
  Prior art: canary deploys exist for services, not for local state files. Better by: a state-format change first applies to the least valuable ledger and soaks for a day before the rest. Novelty: 3.
  Why: wild; the pack suggests checking upgrades against a copy of real state. Done when: an upgrade with a planted format bug breaks only the sentinel ledger.

- **Wild: add a fetal-tolerance window for planned breaking work** — FEATURE — value 3 — effort S — risk med — category: guard
  Prior art: temporary allow rules that the user sets by hand. Better by: a declared mass rename or migration opens a scoped tolerance, which narrows the guard, auto-expires and logs everything it let through. Novelty: 3.
  Why: wild; the user's blocks keep tripping on legitimate bulk work. Done when: the window expires on schedule and a command outside its scope is still blocked.

Next question: which of Foreman's reactions have no off-switch the user can reach while the system is already reacting?
Next question: which unattended rule has never fired on real input, and what would prove it is alive?
