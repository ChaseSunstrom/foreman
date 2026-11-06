# Brainstorm — lens: deepen: guard

- **Run a guard thymus: every rule must pass self-tolerance and potency before release** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the list repeats negative selection many times, and the pack has the pieces (124 replay cases, user history, lessons). Merge these into one gate. A rule ships only if it fires on none of the user's last N accepted commands (self) and on at least one planted harmful case (potency), and it reports both numbers.
  Done when: `fm guard add` on a rule that matches a command from the user's history is refused with the matching history line, and a rule that matches no harmful case is refused as impotent.

- **Add a second-signal rule: a block needs damage evidence or a conserved danger class** — FEATURE — value 5 — effort M — risk med — category: guard
  Why: the pack reports 15+ approval prompts because prefix allow-lists disagree with sandbox structure. Combine the danger model, anergy and the conserved-class idea. A shape match alone only tags. It blocks only with a second signal, such as a protected path, an irreversible verb or a prior harm in this session.
  Done when: in the replay corpus, a shape-only match produces a tag and no prompt, a match with a second signal blocks, and the prompt count on a recorded session drops against baseline with no new misses.

- **Audit every unsandboxed or overridden call in a tamper-evident log** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the user coygeek's request for audit logging of escape-hatch commands was closed "not planned", and Codex is adding guardian review. Foreman can log each guard decision (allow, tag, block, override) with the rule, signals and hash chain.
  Done when: `fm guard log --verify` passes on an untouched log and reports the first broken entry after a line is edited.

- **Treat user overrides as allergy and tolerance data, then propose rule edits** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: Foreman already demotes noisy triggers. Do the same for guard rules the user overrides by hand. A rule overridden K times with the same shape gets a proposed narrowing, shown with the diff. It is never auto-applied, and it can only tighten when the change is learned.
  Done when: after K recorded overrides, `fm doctor` shows a narrowing proposal that replays clean on the 124 cases, and nothing changes until the user accepts it.

- **Mature rules overnight against a mutated evasion corpus** — PERFORMANCE — value 4 — effort M — risk med — category: guard
  Why: `fm night` already ticks unattended. Combine the nightly affinity-maturation and germinal-centre ideas. Mutate each blocked case (quoting, env prefixes, subshells, `bash -c` wrappers, the nested compound parts that Claude Code fixed in v2.1.289) and keep the variants that slip past. Propose a rule widening for each, and run the widening through the thymus gate.
  Done when: a night tick adds at least one mutated variant to the replay corpus as a labelled case, and the digest lists variants caught and variants missed.

- **Detect composition: harmless steps that become harm together** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: this joins the hapten and composed-harm ideas. Single-call rules miss "write script, chmod, run" or "read credential, then curl". Keep a short per-session window of tags and fire when an ordered chain completes.
  Done when: a replay case of three individually allowed calls that together exfiltrate a credential is blocked on the third, and each call alone still passes.

- **Ingest rival fixes as labelled replay cases, with provenance** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: the frontier names Claude Code's deny/ask fix on nested parts of compound commands (v2.1.289) and Codex's approval changes. These fix notes are free, labelled test cases. Combine the serum, convalescent and rival-bug ideas into one `fm replay import` that stores source, date and expected verdict.
  Done when: importing a fix note adds cases tagged with their source, and the replay run reports pass rate by source.

- **Shadow-run every new or edited rule before it can act** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: it joins "let detectors tag but never act", shadow retirement and the serosurvey. A new rule runs silently for a window, and Foreman records what it would have hit. Promotion needs a clean shadow read. Retirement uses the same path in reverse.
  Done when: a new rule shows "shadow: N would-blocks, M overridden-by-history" in `fm doctor`, and it blocks nothing until promoted.

- **Guard the guard: lint rule text and learned lessons for injection** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the earlier question "which learner has never been tested with a poisoned input" applies here. Rules, lessons and imported cases are text that an agent reads. Run a check that rejects instruction-like content, and a test that feeds poisoned lessons in.
  Done when: a lesson containing "ignore previous rules" is rejected on write, and a poisoned-input test exists for each learner.

- **Declare quarantine zones with expiry and a break-glass reason** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: this merges the immune-privileged path and fetal-tolerance ideas. Some files (credentials, the guard's own config) are walled off from agent writes. A planned breaking change can open a zone for a bounded window with a stated reason, and the window is logged.
  Done when: a write to a walled path is blocked, a declared window with expiry lets it pass, and the same write after expiry is blocked again.

- **Wild: Run a guard vaccination drill, a planted harmless bait the agent must refuse** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: wild. Seed a scratch sandbox with a fake secret file and a decoy destructive script, run an exam arm against it, and measure whether the guard fires. This checks the guard against ground truth, which the earlier question asks for, instead of only against a frozen corpus.
  Done when: `fm exam run --drill` reports a catch rate on planted baits, and a rule removed on purpose shows up as a miss.

- **Wild: Give each rule a visible fever state across the whole harness** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: wild. After a harm event, move all rules to a stricter tier at once (more tags become blocks, subagent budgets shrink), and cool down by clean steps. This is the fever idea, built on the risk budget Foreman already has.
  Done when: a recorded harm event raises the tier shown in the status line, and N clean steps return it to normal with each transition logged.

- **Wild: Hold a neutralize-instead-of-block mode that rewrites a risky call into a dry run** — FEATURE — value 3 — effort L — risk high — category: guard
  Why: wild. Instead of a prompt, turn `rm -rf X` into a move to a trash directory, or `git push --force` into `--force-with-lease`. This answers prompt fatigue without lowering protection.
  Done when: a replay case of a deletion is rewritten to a reversible move, the user can undo it with one command, and the original call never ran.

- **Wild: Cross-harness guard memory, so a rule learned in one harness protects the others** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: wild. The pack notes that bets already record the harness, and that cross-tool memory is a stated pain point. Share vetted rules and the audit log across Claude Code, `fm code`, Codex and others, keyed by rule id.
  Done when: a rule promoted in one harness blocks the same replay case in another harness with the source recorded.

Next question: Which guard rule has the highest override rate today, and was it ever checked against ground truth rather than the 124 labelled cases?
Next question: What does the user lose when the guard errs toward blocking, in prompts per session, and is that number tracked anywhere?
