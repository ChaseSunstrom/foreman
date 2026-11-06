# Brainstorm — lens: exam arms for local models

- **Gate each not-yet promotion on a paired path-replaced exam** — FEATURE — value 5 — effort M — risk low — category: exam gate
  Why: Steer says selfjev-4b, jeff, Jevlike and Von wait on an exam arm against the path they replace; the pack shows no such arm yet (T-2887/2908 are partial).
  Done when: `sampo louhi models --promote selfjev-4b` refuses without a stored paired run on the same held-out scenarios and prints the delta against the replaced path.

- **Add a tool-acquisition scenario family to Louhi** — FEATURE — value 5 — effort M — risk med — category: exam scenarios
  Why: Mission 7 builds find/build/test/use with install grants, but nothing measures a local model doing it. Scenarios from replayed real missing-tool moments (shellcheck, LSP, tree-sitter) with decoys already on PATH.
  Done when: `sampo exam run` has a `tools` family with ≥10 scenarios, each graded on find, build, negative-control test, use and grant request, reported per model.

- **Grade the install-grant request itself** — FEATURE — value 4 — effort S — risk low — category: exam grading
  Why: Grants are queued, never self-approved; a 4B that asks for the wrong or over-broad install is a safety failure that pass/fail on the tool hides.
  Done when: a scenario passes only if the queued grant names one tool, a pinned source and a reason, and "should have declined" scores as pass.

- **Climb a scaffold ladder per model and print the lowest rung that passes** — FEATURE — value 5 — effort M — risk low — category: scaffolding
  Why: Steer is "match frontier through scaffolding"; rungs: bare, card, card + grammar menu, frontier-assist. Without per-rung data, cards can't be shown to help.
  Done when: scorecard has one row per (model, scenario kind) with the lowest passing rung and its cost.

- **Run a bare-versus-card paired arm and store lift on each card** — FEATURE — value 5 — effort M — risk low — category: card measurement
  Why: T-2909 creates the card store with admit rules; lift is the proof they earn their place. Cards a model passes bare get retired.
  Done when: every card row in `cards.jsonl` carries `lift`, `n`, `model` and the run id, and a zero-lift card is flagged.

- **Hold out cards from the models that wrote them** — FEATURE — value 4 — effort S — risk low — category: contamination
  Why: A 27B writing cards and the same 27B grading them echoes itself; standing rule already demands signals Sampo didn't author.
  Done when: the exam refuses a card's lift number if writer model equals grader model, and the scorecard shows writer ≠ grader.

- **Batch exam arms by resident model** — PERFORMANCE — value 4 — effort S — risk low — category: exam throughput
  Why: A llama-swap switch costs ~3 minutes and isn't detectable (user steer); interleaved arms burn that repeatedly.
  Done when: a full multi-model exam run performs at most one switch per model, shown in the run log.

- **Score cost per verified pass including swap time** — FEATURE — value 3 — effort S — risk low — category: exam metrics
  Why: Local is "free" only if wall time and swaps are counted; otherwise local-vs-frontier comparisons mislead.
  Done when: scorecard prints seconds, tokens and swaps per verified pass per arm.

- **Add a paraphrase-contamination arm** — FEATURE — value 3 — effort M — risk low — category: exam validity
  Why: Small models memorize scenario wording; a paraphrased twin scenario separating cards from recall.
  Done when: each scenario has a twin from a tool-less child and the scorecard shows the pass gap.

- **Wild: Nightly gladiator league on idle local hardware** — FEATURE — value 4 — effort L — risk med — category: league
  Why: wild — every local model plays every card on closed-task replays overnight; the leaderboard lands on the Models page, one model switch each.
  Done when: morning card lists ranked models, per-card lift changes and promotions refused or allowed.

- **Wild: Poison one card per run to test blind trust** — SECURITY — value 4 — effort S — risk low — category: robustness
  Why: wild — a planted unsafe step in a card; a model that follows it blindly shouldn't get that card promoted.
  Done when: the exam reports poisoned-card follow rate per model and the Ward catches the unsafe step.

- **Wild: Dumbest-model floor printed on every card** — FEATURE — value 3 — effort M — risk low — category: card metadata
  Why: wild — run each card down the model ladder (4B up) and stamp the smallest passing model; routing then picks by it.
  Done when: cards show `floor: qwen3.5-4b` or `none`, and retrieval prefers cards at or below the active model.

- **Gate fast-to-fail: zero-token structure arm before any model call** — PERFORMANCE — value 3 — effort S — risk low — category: exam cost
  Why: Standing cadence says zero-token arms run every generation; checking that a model's output parses, names real verbs and stays in the grammar catches most 4B failures free.
  Done when: structure arm runs on all local outputs and rejects malformed ones before any grader call.

- **Wild: Race the 27B against a cold frontier apprentice on a missing tool** — FEATURE — value 3 — effort M — risk med — category: parity
  Why: wild — same Wanted entry, same tests, judged by the scenario's own checks; publishes the frontier-parity gap per task kind.
  Done when: a parity curve for tool-forge tasks appears on the Models section with dates.

Next question: Which of the held-out scenarios can a local model pass only because the scenario text names the tool, and does the exam measure that separately from finding the tool?
Next question: When the served model on the endpoint changes without notice, which stored lift and floor numbers silently go stale, and what detects it?
