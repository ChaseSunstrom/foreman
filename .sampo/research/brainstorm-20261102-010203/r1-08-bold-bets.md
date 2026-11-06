# Brainstorm — lens: bold bets

Lens: bold bets, from the immune-system mechanisms in the pack. Each idea carries Prior art, Better by and Novelty lines as the Mission asks. No ideas were repeated from the list.

- **Select guard rules negatively against the user's own history** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the pack shows brief-guard false positives (path matches) and users hitting 15+ approval prompts. Nothing deletes a rule that fires on legitimate work.
  Prior art: none found. Harnesses ship hand-written deny/ask lists, and Foreman's replay only measures precision on 124 labelled cases.
  Better by: every new or edited rule must stay silent on the user's whole accepted-command history (the thymus test) before release. The rule is deleted or narrowed if it fires on "self".
  Novelty: 4.
  Done when: a candidate rule that matches a command the user ran and kept 30 days ago is refused at `fm` rule-add with the matching history line named.

- **Breed guard rules by clonal selection** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: assumption: real blocks are rare, so rules improve slowly by hand.
  Prior art: none. Mutation testing and fuzzing exist, but none grows detectors by affinity.
  Better by: a rule that caught real harm spawns mutated variants (flag order, quoting, aliasing). Variants are kept only if they catch labelled evasions and pass the negative-selection test above.
  Novelty: 5.
  Done when: from one seed rule, a night run yields at least one surviving variant that blocks an evasion absent from the replay corpus, with zero self hits.

- **Require two signals before the guard escalates (anergy)** — FEATURE — value 4 — effort S — risk low — category: false positives
  Why: the approval-prompt complaint (allow list matches prefixes while the sandbox flags structure) is the single-signal problem.
  Prior art: Codex "Guardian" review is one extra reviewer, not a two-signal rule.
  Better by: a lone weak signal (path regex, odd verb) is logged and ignored. A block needs a costimulus (a destructive effect confirmed in a dry-run, or a second independent rule), so prompts fall without losing hard denies.
  Novelty: 3.
  Done when: on the replay corpus, prompts drop at least 30% with no labelled-harm case newly allowed.

- **Judge by damage, not by command shape (danger model)** — FEATURE — value 5 — effort L — risk med — category: safety
  Why: the pack says the guard is fixed rules on tool calls, so letter-defeats-intent evasions slip through.
  Prior art: sandboxes and COW snapshots contain damage. Nothing triggers escalation from observed damage signals.
  Better by: a PostToolUse sensor reads damage signals (files deleted outside the fence, tests newly red, secrets touched, size cliff). A damage signal retroactively tightens the guard and auto-snapshots, whatever the command looked like.
  Novelty: 4.
  Done when: a planted benign-looking script that deletes 40 files outside the fence triggers an autonomy step-down within the same session.

- **Raise a whole-system fever on harm** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: the risk budget steps autonomy down per harm, but other dials (reviewer depth, parallel lanes, model tier) stay put.
  Prior art: none. Rate limiters and circuit breakers act on one dial.
  Better by: one state flips several dials together (cold read on every change, lanes capped at 1, stronger model, tighter guard) and decays on a clock, with a "fever" line in the status line.
  Novelty: 4.
  Done when: after one recorded harm, `fm doctor` shows all four dials moved, and they return to baseline after the stated cooldown.

- **Cap Foreman's own alarm storms with a regulatory layer (T-regs)** — FIX — value 3 — effort S — risk low — category: noise
  Why: the pack records false-alarm "breakage ahead" notes the user had to drop, and 15+ prompts per session.
  Prior art: alert dedupe in monitoring tools. None in agent harnesses that scale suppression with the host's own alarm rate.
  Better by: when notes plus prompts exceed a per-session threshold, a regulator mutes the lowest-precision source and says so once.
  Novelty: 3.
  Done when: a replayed session with 20 flags shows at most 5 and a single "muted N low-precision sources" line.

- **Keep memory cells for fixes, with a one-step second response** — FEATURE — value 4 — effort M — risk low — category: recall
  Why: lessons are recalled per file, but a failure's signature (error text and fix diff) is not kept as a re-runnable response.
  Prior art: Aider, ECC and claudekit memories store prose. None replay a verified patch.
  Better by: a CI-red FIX that is solved stores signature, patch and verifier. A repeat signature gets the patch applied in a scratch tree and verified before any model call.
  Novelty: 4.
  Done when: a repeated failure signature closes with zero model tokens, the verifier green, and the fix flagged "memory-cell hit".

- **Present antigens: lanes show a fragment to a cold inspector (MHC)** — FEATURE — value 4 — effort M — risk med — category: oversight
  Why: the cold reader gates tower files only, and 87% of developers worry about accuracy.
  Prior art: Codex Guardian reviews with handoff context, not a fixed-size fragment the lane cannot choose.
  Better by: every N tool calls a lane must emit a sampled, hash-bound fragment of its working state (current claim, files touched). A tool-less inspector checks it against the brief and kills lanes whose fragment is "non-self".
  Novelty: 5.
  Done when: a planted off-task lane is killed by the inspector within the sampling window in a drill.

- **Track autoimmunity: guard overrides as disease** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: assumption: user overrides of blocks and dropped captures already exist in the ledgers but are not read as guard harm.
  Prior art: none found.
  Better by: a ledger rates each rule's attack-on-self rate (blocks the user later overrode or hand-ran). A rule above threshold is auto-proposed for narrowing.
  Novelty: 3.
  Done when: `fm doctor` lists the top-3 self-attacking rules with counts.

- **Wild: vaccinate sessions with attenuated past incidents** — FEATURE — value 3 — effort M — risk med — category: training
  Why: wild; builds on hostile-replay ideas but graded by dose.
  Prior art: none found.
  Better by: at low-stakes starts, a sandboxed replay of a weakened version of the user's own past harm (read-only, fenced) checks the guard still catches it. The dose rises only after it passes.
  Novelty: 5.
  Done when: the replay is stamped with its dose and a guard regression turns the next morning card red.

- **Wild: inflame-and-contain a damaged module** — FEATURE — value 3 — effort M — risk low — category: containment
  Why: wild; after a revert or red CI, scrutiny should swell locally, not globally.
  Prior art: none. Hotspot ideas exist, but none are temporary and neighbour-spreading.
  Better by: files within one import hop of a damaged file get a cold read and a no-unattended-edit rule for N days, then decay.
  Novelty: 4.
  Done when: an unattended lane edit to a neighbouring file is parked for a yes, and the same edit passes after decay.

- **Wild: complement cascade for weak suspicions** — FEATURE — value 3 — effort M — risk low — category: triage
  Why: wild; the pack's idea that single noisy signals are ignored loses true weak ones.
  Prior art: none.
  Better by: weak signals pass through ordered cheap checks (grep, test, tool-less child), each amplifying or cancelling it. Only a survivor of all reaches the user.
  Novelty: 4.
  Done when: a planted subtle problem reaches the user as one flag with its cascade trail, and a decoy dies at stage two.

Next question: Which of Foreman's learners has been tested with a poisoned input, and which detectors does the negative-selection test have no "self" data for?
Next question: Does anything in the ledger already measure harm after an allowed call, so that the danger model needs no new sensor?
