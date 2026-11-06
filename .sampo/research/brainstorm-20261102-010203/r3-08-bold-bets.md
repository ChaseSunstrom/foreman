# Brainstorm — lens: bold bets

Every common immune mechanism is already in the list, so these use mechanisms the list lacks: neutralizing antibodies, AIRE, receptor editing, interferon, wound healing, sepsis, tertiary lymphoid structures, mucosal IgA, trained immunity, neoantigens, neutrophil traps, phage and twin studies. Each idea carries its Prior art, Better by and Novelty lines.

- **Neutralize the call instead of blocking it** — FEATURE — value 5 — effort M — risk med — category: guard
  Why: the frontier reports 15+ approval prompts in one session, and the guard's only verbs are allow and deny. A neutralizing antibody binds the toxin and leaves the cell alive.
  Done when: a PreToolUse pass rewrites `rm -r X` to a move into a trash dir, `git push --force` to `--force-with-lease`, and a bare `DROP` into a transaction. The lane continues without a prompt, and all 124 replay cases keep their verdicts.
  Prior art: safe-rm and trash-cli wrappers; no harness has rule-bound rewrite. Better by: the rewrite is chosen per guard rule and logged with its undo. Novelty: 4.

- **Teach the thymus the user's rare legitimate commands (AIRE)** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the thymus expresses organ-specific antigens it would never meet in the blood. A replay of shell history misses the legitimate deploy, migrate and release commands that appear in Makefiles, package scripts, CI files and crontab.
  Done when: the negative-selection corpus includes commands harvested from those files, and a new rule that blocks one of them fails release.
  Prior art: none found. Better by: this is self-coverage beyond history, which cuts false positives on rarely run commands. Novelty: 4.

- **Edit the receptor before deleting the rule** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: a rule that hits the self corpus is currently just rejected. B cells get one chance to rewrite their receptor first.
  Done when: a rule failing the self replay is narrowed automatically by the counterexample, for example by adding an anchor or an exclusion, until it passes the self corpus while still catching its attack corpus. If it cannot, it is deleted.
  Prior art: program-repair tools; rule synthesis from examples. Better by: the narrowing is bounded by both corpora. Novelty: 4.

- **Lock down the capability class, not the attack (antiviral state)** — SECURITY — value 4 — effort M — risk med — category: containment
  Why: interferon makes neighbouring cells block the replication machinery without recognizing the virus. After a supply-chain or exfil signal, restricting only installs or egress for an hour stops the attack class, including unseen variants.
  Done when: one hazard event sets a time-boxed deny on a named capability, such as network, package install or push, for all lanes. `fm doctor` shows the active locks, and the locks expire.
  Prior art: a global kill switch exists in some CLIs; no capability-scoped, signal-triggered lock. Better by: lanes keep working on everything else. Novelty: 4.

- **Run incidents through the four wound-healing phases** — FEATURE — value 3 — effort M — risk low — category: incidents
  Why: the immune list has detection but no incident lifecycle. Hemostasis, inflammation, proliferation and remodeling map onto freeze, diagnose, fix, and turn the fix into a permanent test.
  Done when: an incident has a phase; the clot (a snapshot and write lock) expires automatically; and closing it requires a regression test and a deleted clot. A count of unremodeled scars is shown.
  Prior art: incident runbooks, but none keep a clot that auto-expires. Better by: the freeze is automatic and expires. Novelty: 3.

- **Audit immunoparalysis after an alarm storm** — FIX — value 3 — effort S — risk low — category: alarms
  Why: sepsis ends in suppression after an overreaction. Capping, muting after two dismissals and throttling all suppress warnings, and nothing checks whether a suppressed warning later came true.
  Done when: a muted or throttled nudge is stored with its signature, and `fm doctor` reports the count of suppressed warnings that were later followed by harm. A rate above a set bar loosens the mute.
  Prior art: alert-fatigue metrics. Better by: it scores suppression itself against outcomes. Novelty: 4.

- **Spin up a tertiary lymphoid structure on a chronic hotspot** — FEATURE — value 3 — effort M — risk med — category: hotspots
  Why: chronic inflammation grows a local lymph-node-like structure. The pack shows per-file lessons and captured FIX tasks, but nothing local that forms around a file that keeps failing.
  Done when: a file with N captured failures gets a mini-unit of a targeted test, a watcher and its lesson set. The unit dissolves after a clean run of N weeks.
  Prior art: none found. Better by: effort concentrates where damage recurs and is released afterwards. Novelty: 4.

- **Neutralize hostile fetched text silently (mucosal IgA)** — SECURITY — value 4 — effort M — risk med — category: ingress
  Why: secretory IgA excludes antigens without inflammation. Frontier trust and security worry is high, and every nudge costs context.
  Done when: instruction-shaped spans in issue, CI and web text are replaced with an inert marker before the model sees them. The only trace is a counter in `fm doctor`, and zero context bytes are added.
  Prior art: prompt-injection filters that warn loudly. Better by: it is silent and has a context cost of zero. Novelty: 3.

- **Tune innate thresholds per repo after incidents (trained immunity)** — FEATURE — value 3 — effort S — risk low — category: tuning
  Why: innate cells keep a persistent sensitivity shift after exposure without a new receptor. Fever is global and temporary, and memory cells are new rules.
  Done when: a repo's harm history lowers guard thresholds on that class only. `fm doctor` shows the dial and its slow decay, and a clean repo stays at default.
  Prior art: none found. Better by: no new rules and no recall cost. Novelty: 3.

- **Find the neoantigen: mine the discriminating feature of a failure** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: tumour immunity targets what differs from the host's own cells. Captured red CI and healthy runs already exist to diff.
  Done when: from N failing and N passing logs or diffs, a draft detector is produced that flags the failing set and not the passing set on held-out runs, then goes to the thymus exam.
  Prior art: fault localization; invariant mining. Better by: its output is a gated, executable detector. Novelty: 3.

- **Wild: trap a runaway lane in a decoy room (neutrophil trap)** — FEATURE — value 3 — effort L — risk high — category: containment
  Why: assumption: a lane that keeps retrying a blocked call gets stuck in a loop. Neutrophils eject DNA nets that entangle a pathogen and die.
  Done when: after M blocked retries, the lane's tool calls run against a scratch copy with a cost cap, and the lane's output is returned for review.
  Prior art: honeypots, not applied to the agent's own lane. Novelty: 5.

- **Wild: send a one-signature phage** — FEATURE — value 3 — effort M — risk med — category: cleanup
  Why: assumption: recurring anti-patterns, such as the flipped-assertion class, return after each fix. A phage targets one host species, replicates, then lyses.
  Done when: a task spawns a single-purpose script that finds and fixes every instance of one signature repo-wide. It is deleted after one pass, and a replay shows zero remaining hits.
  Prior art: codemods. Better by: it is born from a captured failure and self-deletes. Novelty: 4.

- **Wild: run a twin study of learned state** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: assumption: it is unknown how much learned state matters. Twin studies split nature from nurture.
  Done when: two installs with different learned state replay the same history and a report lists the verdicts that diverge, to find noisy learners.
  Prior art: ablation duels, which use one arm. Novelty: 4.

Next question: which decisions has Foreman made for the user that the user could not undo with one command?
Next question: does the guard know what a command does, or only what it looks like?
