# Brainstorm — lens: grid

Grid used. Surfaces: CLI verbs (`sampo`/`fm`), session hooks/decide() paths, Smith loop, web UI/tower, Louhi exam, moons funnel. Actors: user, agent, other agents, unattended run. Failure modes: missing, wrong, slow, unsafe, unclear.

- **Show the model's abstain reason in the CLI close line** — FEATURE — value 4 — effort S — risk low — category: CLI×user×unclear
  Why: assumption: a user seeing "decided by model X" with no reason can't tell a fallback from a verdict; earlier ideas cover a web UI listing, not the per-call line.
  Done when: every `decide()` output line names the slot, the model or "rules", and the abstain reason when it fell back, and a test asserts it.

- **Refuse a model whose serving settings never reached the endpoint** — FIX — value 4 — effort S — risk low — category: Smith×agent×wrong
  Why: the `think: false` fix shows gemma4:12b kept reasoning because Ollama ignored the field. A trained model benched under one setting and served under another is a silent wrong.
  Done when: before any bench or serve, a probe request echoes back the effective context, reasoning mode and sampling, and a mismatch aborts with the field named.

- **Make the training collector tolerate and report unlabelled rows** — FIX — value 3 — effort S — risk low — category: trainer×unattended×wrong
  Why: the unrated-moon crash (`wild` null in the site build) shows null fields break consumers. Assumption: the briefs have the same nulls (old outcome fields, missing criteria).
  Done when: the collector run over all 13 projects ends with a count per skipped-or-nulled field and never throws on a null.

- **Cap a training job's GPU claim so it yields to the funnel** — PERFORMANCE — value 4 — effort M — risk med — category: GPU×unattended×slow
  Why: the funnel waits ~3 min per batch and the 27B endpoint has 2 slots; a 16 GB card shared with Ollama can't take a LoRA run unannounced.
  Done when: a training run started during a moons run pauses at a step boundary when a judge call queues, resumes after, and the run log shows the pauses.

- **Quarantine training text that came from a tool result** — SECURITY — value 4 — effort M — risk med — category: trainer×other-agents×unsafe
  Why: ledger lines and journals hold repo and web text; the pack asks whether ledger text can attack the trainer. Tagging by origin (user, model, tool) is the cell no earlier idea names.
  Done when: each training row carries an origin tag, rows with tool-origin text in the instruction side are excluded by default, and a planted "ignore previous" row in a fixture never reaches the output.

- **Give a model's slot a time budget with a rules fallback** — PERFORMANCE — value 3 — effort S — risk low — category: session×agent×slow
  Why: the hook bench (`bench_hooks.py`) gates hook latency; a head that needs an embedder call on a cold Ollama could blow it.
  Done when: each model-backed hook has a deadline, a timeout returns the rules answer, and `bench_hooks.py` includes the model path under its limit.

- **Add a "what changed since the model last saw this" staleness flag** — FEATURE — value 3 — effort M — risk low — category: Rune×user×unclear
  Why: assumption: after the rename to Sampo and T-2967's path moves, features like paths and verb names shifted. A model trained before that predicts on old names.
  Done when: each model card records the vocabulary hash of verbs and paths at train time, and `sampo doctor` warns when the live vocabulary drifts past a threshold.

- **Score a model per language in Louhi, not only overall** — FEATURE — value 4 — effort M — risk low — category: exam×user×unclear
  Why: the steers ask for recall reported per language and bug type; the genericity claim for non-Sampo projects (Python volt compiler, C, Ruby) fails silently if the average hides a weak language.
  Done when: the scorecard prints a language×bug-type table with n per cell, and a model can't be adopted if any cell with n≥5 regresses.

- **Let other agents consume a model verdict as a typed hint, not text** — SECURITY — value 3 — effort M — risk med — category: hooks×other-agents×unsafe
  Why: Codex, Gemini and opencode share the discipline layer; passing model prose into their prompts opens the same text channel the Ward guards.
  Done when: model outputs reach other agents only as an enum plus a number, and a test shows free text from a model never enters an agent's context.

- **Wild: Play the model's mistakes back as a daily "wrong calls" digest** — FEATURE — value 3 — effort M — risk low — category: user×wrong — wild
  Why: assumption: the user is away for long runs and returns to a ledger of 149k lines. A ten-line digest of where the model was wrong and later corrected builds trust fast.
  Done when: after any unattended run, a digest lists each model call later contradicted by an outcome, with task ids.

- **Wild: Let the model's own bench scenarios be planted by the Ward's attacker, in one arena** — FEATURE — value 3 — effort L — risk med — category: exam×unattended×unsafe — wild
  Why: the Ward and the funnel's local models share a text channel; one adversary that generates both planted bugs and injection strings gives two measures from one generator.
  Done when: one command emits a scenario set with planted faults and injections, and the scorecard reports detection of each separately.

- **Wild: Print a one-line "model said, you did" regret ratio per slot on the tower** — FEATURE — value 2 — effort S — risk low — category: web UI×user×unclear — wild
  Why: assumption: the tower is where the user checks progress; a single ratio of followed vs overridden suggestions shows which slot earns its place.
  Done when: the tower shows per slot the share of model suggestions the user or agent overrode, drawn from ledger events.

- **Kill a model slot that has no ledger incident behind it** — CLEAN — value 3 — effort S — risk low — category: all×unattended×unclear
  Why: the pack asks which defences had incidents; the lean-substance rule already holds unmeasured growth, but no check ties a slot to evidence.
  Done when: `sampo doctor` lists any adopted slot with zero measured wins in the bench or outcomes and files a subtraction task.

**Empty cells and why:** web UI×agent (agents don't use the UI), Louhi×other-agents (exam runs one arm at a time), moons funnel×unsafe beyond the shared-channel cell above (covered by earlier red-team ideas), and every "missing" cell for CLI×user (the verbs already exist; the gaps are in clarity).

Next question: Which model-backed slot has the worst failure when it is silently wrong rather than slow, and does any ledger show that happening before?

Next question: What does a project with fewer than 20 briefs get from a shared model, and where is the line below which the model should say nothing?
