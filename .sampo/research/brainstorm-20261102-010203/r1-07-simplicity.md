# Brainstorm — lens: simplicity

- **Release no learned rule before it passes a self-test** — FEATURE — value 5 — effort M — risk low — category: learners
  Why: thymus negative selection. The brief-guard false positives and trigger auto-demotion both catch bad detectors only after they have annoyed the user. Here, any new lesson, guard rule or trigger is replayed against the user's accepted history (clean sessions, kept diffs) and deleted before release if it fires on any of it. One gate would replace per-learner precision logic.
  Prior art: none found. Harnesses gate rules by review or by after-the-fact stats. Better by: it blocks at birth, so the user never meets the false positive. Novelty: 4.
  Done when: a planted rule that matches a command from the user's accepted history is refused at `fm` rule-add with the matching history line named.

- **Require two signals before any block or nudge acts** — FIX — value 4 — effort S — risk low — category: guard
  Why: anergy and costimulation. A pattern match alone is logged only. It acts when a second, independent signal agrees (path outside the fence, test red, secret in output, a prior harm). The brief-guard false positives are single-signal matches.
  Prior art: Codex Guardian and Claude Code prefix rules use one signal. Better by: a replay-corpus-measured drop in blocks on benign cases while the 124 labelled cases still block. Novelty: 3.
  Done when: `fm replay` shows zero false positives on the two known brief-guard cases and no lost true blocks.

- **Compile repeated lessons into fixed rules and delete the memory** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: germline versus somatic immunity. A lesson recalled and acted on three or more times is promoted into a fixed rule or test, and its stored entry is removed. Learned state shrinks as Foreman matures. Evidence: the lean ratchet, plus lessons recalled per file that only ever accumulate.
  Prior art: none found; memory tools only append. Better by: the learned layer stays small and the fixed layer is testable. Novelty: 4.
  Done when: a lesson with three recalls becomes a rule or test via one command, and its lesson file is gone.

- **Run one inflammation governor over every output** — FEATURE — value 4 — effort S — risk low — category: context
  Why: T-reg regulation of a cytokine storm. One per-session counter of notes, nudges and blocks; past N, all non-essential injection mutes, with a single line saying so. It replaces per-feature caps ("cap flags per session", "mute after two dismissals") with one dial.
  Prior art: none found. Better by: one number to tune and a bounded worst case for hook-note chars. Novelty: 3.
  Done when: a scripted session that triggers 30 notes injects at most N and ends with one "muted: storm" line.

- **Wall off a failing component with one quarantine file** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: local containment of inflammation. A crashing hook, learner, watcher or lane writes `quarantine/<name>`. Everything else reads that one file, skips the component, and `fm doctor` lists it with the cause. Today each silent failure needs its own liveness row.
  Prior art: circuit breakers exist in services, not in coding harnesses. Better by: one primitive covers hooks, triggers and learners. Novelty: 3.
  Done when: a deliberately crashing learner is skipped on the next call, and doctor shows it quarantined with its error.

- **Take a fever posture after harm, then let it decay** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: fever is a whole-system state change. The risk budget steps autonomy down only for the agent. A single posture file also tightens the guard, forces cold reads, pauses triggers and defers installs, then decays on its own clock. It replaces scattered knobs with one state.
  Prior art: Codex approval modes are static, set by the user. Better by: it is automatic, global, time-limited, and tested through one file. Novelty: 4.
  Done when: a recorded harm event flips the posture, and the same scripted session behaves stricter until the decay time passes.

- **Show a one-screen digest instead of the diff to the cold reader** — PERFORMANCE — value 3 — effort M — risk med — category: review
  Why: antigen presentation shows an inspector fragments, not the whole cell. A lane emits a fixed 10-line card (files touched, commands run, tests changed, outside-fence writes) and the cold reader reads that first, opening the full diff only on an anomaly. Evidence: cold-read cost is an open question.
  Prior art: PR summaries exist but are written by the author. Better by: the card is computed from the ledger, not self-reported. Novelty: 3.
  Done when: a seeded lane diff with one fence violation is flagged from the card alone, with fewer tokens read than a full-diff pass.

- **Mutate and select guard regexes against the replay corpus** — CLEAN — value 3 — effort M — risk med — category: guard
  Why: affinity maturation. Each night, variants of a rule that is too loose or too tight are scored on the 124 cases plus the user's history, and the best variant is proposed as a diff. The user stays the approver.
  Prior art: fuzzing exists; none found that tunes guard rules. Better by: rules converge toward fewer false positives and fewer misses with no hand edits. Novelty: 4.
  Done when: a deliberately over-broad rule yields a proposed narrower variant with equal true blocks and fewer false positives.

- **Memoise guard verdicts as memory cells** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Why: memory cells give a fast second response. An exact (tool, normalised args, rule-version) key returns its stored verdict and skips parsing. The key includes the rule hash, so editing a rule invalidates it. This helps the hook p95 ratchet.
  Prior art: none found in harnesses. Better by: the p95 gain costs nothing to the user. Novelty: 2.
  Done when: the second identical call is measurably faster, and a rule edit forces a fresh verdict.

- **Wild: Block, then watch whether the user does it by hand** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: autoimmunity detection. If a block is followed within minutes by the user running the same command, the rule is an attack on self. It is auto-suspended pending a one-word keep/drop. Evidence: false-positive fixes today come only from user complaints. wild.
  Prior art: none found. Better by: the false-positive signal comes from behaviour, not a complaint. Novelty: 4.
  Done when: in a simulated session a blocked command re-run by the user suspends its rule and appears in the next card.

- **Wild: Let the guard vaccinate itself with an attenuated attack each night** — SECURITY — value 3 — effort M — risk low — category: assurance
  Why: vaccination. A harmless, labelled mutation of a known-bad command goes through the real hook path to prove the guard is alive and still catches variants. It is the same family as the weekly canary but tests variants, not one fixed string. wild.
  Prior art: none found (chaos tests exist elsewhere). Better by: it checks coverage of variants, not just liveness. Novelty: 3.
  Done when: a rule deleted in a scratch copy makes the nightly vaccine miss and report the variant.

- **Wild: Give every capability a clonal "binding" score and cull the lowest tenth monthly** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: clonal selection. Verbs, cards and rules that "bind" (are used and were acted on) get renewed; the least-bound tenth is archived by default. The lean ratchet only blocks growth and never subtracts. wild.
  Prior art: usage-based pruning exists, as with unused permissions. Better by: renewal needs proof of use, so deletion is the default. Novelty: 3.
  Done when: a month of unused cards produces a reversible archive list, and one use restores a card.

Next question: which of Foreman's learned or injected signals has never been scored against what the user did next, and could the same self/non-self replay test score all of them?
Next question: what is the smallest set of fixed rules that would survive if every learner were deleted, and does the exam still pass?
