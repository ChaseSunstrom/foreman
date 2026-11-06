# Brainstorm — lens: capability map

- **Negative-select every new rule before release** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: Brief-guard path false positives recurred and had to be fixed by hand (pack, "Fix the brief-guard path false positives"). Prior art: none found; harnesses ship rules untested against the user's own work. Better by: a candidate guard rule, lesson or trigger is run against the user's own benign history (transcripts, committed commands, the 124-case replay corpus) and is deleted before it ever fires if it matches "self". Novelty: 4.
  Done when: a rule that blocks a command from the user's last 30 days of accepted tool calls is refused at `fm` rule-add, with the offending call named.

- **Require a second signal before any learned rule acts (anergy)** — FEATURE — value 4 — effort M — risk low — category: learners
  Why: The open question is which learner was never tested with poisoned input. Prior art: none; learners act on a single source. Better by: a lesson, trigger or user-model line only goes live with a costimulating signal from an independent source (a CI outcome, a user steer, or a second harness). Without one it stays inert, and expires visibly. Novelty: 4.
  Done when: a planted single-source poisoned lesson is never injected, while the same lesson with a second confirming signal is.

- **Guard on damage signals, not just foreign patterns (danger model)** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: The guard is fixed rules on tool calls, and the sandbox-escape complaint shows that pattern rules both over-prompt and miss real harm. Prior art: Codex Guardian reviews intent; none keys on observed damage. Better by: after each call, cheap damage detectors (writes outside the fence, a red test that was green, a deleted tracked file) raise a signal. The signal can retroactively block the next similar call and propose a revert. Novelty: 4.
  Done when: a scripted call the static rules allow, but which deletes tracked files, triggers a damage signal, a revert offer and a block on its sibling call.

- **Raise a session-wide fever after harm** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: The risk budget steps autonomy down per harm, but nothing changes the whole system's posture. Prior art: none found. Better by: one named fever state makes cold-read gating, full tests and guard strictness rise together, then decay on a half-life when clean. Today's gates are separate dials. Novelty: 3.
  Done when: after an injected harm event, `fm doctor` shows fever on, three listed gates tightened, and they relax after N clean tasks.

- **Remember each incident as a memory cell with a pre-model fast path** — FEATURE — value 5 — effort M — risk low — category: memory
  Why: Lessons are recalled per file, which is slow and relies on the model reading them. Prior art: CLAUDE.md-style memory, which is advisory text. Better by: a harmful call's signature becomes a deterministic hook-level block with a one-line "seen before: T-id" reason. The second exposure costs zero model tokens. Novelty: 3.
  Done when: replaying a past incident's command in a new session is blocked in under one hook call, naming the original task.

- **Mutate and select guard rules against an evasion corpus (affinity maturation)** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: The pack records a request that Claude Code's flag is a prefix match while the sandbox flags structure. Hand-written rules lag evasions. Prior art: fuzzers, but not applied to a guard rule set. Better by: the night tick generates variants of blocked commands (quoting, env prefixes, subshells), keeps the rule patches that bind them without raising false positives on the benign corpus, and files them as a reviewable diff. Novelty: 4.
  Done when: a nightly run proposes at least one rule patch that blocks a planted evasion and passes the benign corpus, and nothing is applied without a yes.

- **Add a regulatory layer that caps reaction cascades (T-regs)** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: Captured FIX tasks, triggers and flaky reruns can each spawn work. Prior art: retry backoff exists, but not a global cascade limit. Better by: one regulator counts automated reactions in a window (FIX from CI red, fix of a fix, trigger fires) and suppresses the rest with a visible "storm held" line. Novelty: 3.
  Done when: a synthetic chain of five self-spawned tasks stops at the cap, with the held items listed.

- **Contain harm locally with a quarantine zone (inflammation)** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: The risk budget steps down autonomy globally, which punishes unrelated work. Prior art: none found. Better by: harm in a path freezes autonomy only for that subtree and its blast radius, using `fm graph blast`, until cleared. Novelty: 3.
  Done when: after harm in `plugin/lib/a.py`, unattended edits there need a yes while edits elsewhere continue.

- **Measure autoimmunity: the guard's attack rate on its own host** — FIX — value 4 — effort S — risk low — category: observability
  Why: Users report 15+ approval prompts in one session. The guard has recall in its corpus but no "self-attack" gauge. Prior art: none. Better by: a gauge of blocks the user later overrode or accepted, per rule, which auto-demotes a rule above a threshold. Novelty: 3.
  Done when: `fm doctor` lists the self-attack rate per rule, and a rule above threshold is demoted to a warning.

- **Present lane fragments to a blind inspector (antigen presentation)** — FEATURE — value 3 — effort M — risk med — category: review
  Why: The cold reader gates tower files only. Prior art: fresh-context parallel reviewers see the whole diff. Better by: each lane exposes a random sample of its claims, diff hunks and test names (a "peptide display"), and an inspector child must find the claim without evidence. It is cheaper than full multi-lens review and fits the token-economy rule. Novelty: 3.
  Done when: an inspector given a sample with one planted unsupported claim flags it more than half the time, at under a third of full-review tokens.

- **Wild: vaccinate with attenuated incidents** — FEATURE — value 3 — effort M — risk med — category: training
  Why: wild; assumption: replaying a harmless, sandboxed copy of a past incident trains a new model, harness or rule set. Prior art: none found. Better by: the replay corpus becomes a "booster" that is run when the host CLI updates, and any new miss files a task. Novelty: 4.
  Done when: a host version bump triggers the booster run, with a pass or fail per incident.

- **Wild: let a lesson fight a decoy pathogen** — FEATURE — value 3 — effort M — risk low — category: learners
  Why: wild; assumption: poisoned inputs are never tested. A child writes a plausible but harmful lesson, and the recall path must reject it. Prior art: none. Better by: this turns the open "poisoned input" question into a recurring test. Novelty: 4.
  Done when: a planted poisoned lesson is quarantined by the second-signal rule, and the test reports it.

- **Wild: grow an immune-system page in the web UI** — FEATURE — value 2 — effort M — risk low — category: UI
  Why: wild; assumption: users trust what they can see. One page shows fever, quarantine zones, memory cells, held storms and self-attack rate as a single posture view. Prior art: none. Better by: it makes the guard legible, which answers the trust complaints (75% distrust). Novelty: 3.
  Done when: the page renders the five states from fixtures, each with its cause.

Next question: Which of Foreman's own protective layers has the user overridden most, and what did that say about the layer's false-positive cost?
Next question: Which immune mechanism would be unsafe to automate, because it could loosen the guard by learning?
