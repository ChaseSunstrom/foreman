---
id: T-2878
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:33:45Z
updated: 2026-11-06T03:54:01Z
base_note: 
rival_at: 2026-11-05T00:44:53Z
rival_split: true
base: 5de167c784f44cc82a9dc40f1f944a571df03532
base_tree: c2d86a4e65fac0d00f45dfcb601e9aca10332e01
predict_minutes: 13
predict_attempts: 1
plan0_at: 2026-11-05T00:45:40Z
plan0_scope: []
paused_tree: 106df4e763e5958f49cb49fa89421e20088b6303
---
# Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
## Raw request
> FEATURE: Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the uncensored variant) for ideas at any volume; study their behaviour on Sampo's real work (where they fail, why, how often); make Sampo drive and control them so their results match a frontier model's (decomposition, constrained output, checks and repair loops, best-of-n with judges, routing by measured skill); write thousands of skills, playbooks, UI instructions and designs written for smaller models; and make every Rune tower generation carry and grow that corpus
## Interpretation
Reading 1 (chosen): uplift is a measured capability. Sampo drives the local qwen models through Smith so that, on held-out work, they close the gap to Claude-driven Sampo. The volume the user asked for ("go absolutely wild", thousands of skills, playbooks, UI instructions and designs) serves that number: a card, a scaffold or a tower stage stays only when it moves the held-out score or the idea yield, and every Rune generation re-measures the gap and grows the corpus where it is thin.

Reading 2 (ruled out): uplift means a big corpus of small-model prompts and heavy use of the local models for ideas, with no measurement. Ruled out because the user asked to "genuinely make sampo able ... making them match your capability", which only a held-out score can show, and because unmeasured volume repeats the moons lesson: generation without a funnel fills the catalogue with tame filler.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Louhi runs a smith arm on a local model in every scenario and records its held-out scorecard beside the Claude arm's — verify with `python3 plugin/tests/run.py test_louhi_smith`
- [ ] A failure taxonomy of the local models on Sampo's work, with rates per class, is filed: classes from the run's own records (sampo exam taxonomy's end reasons, tool-call errors and check failures in the journals), deterministic, no model judge; at least 30 failed scenarios per model — verify with `sampo research show T-2878-taxonomy`
- [ ] Smith's small-model mode raises the local model's held-out pass rate over the plain loop by at least 15 points on at least 30 held-out scenarios per model (a paired sign test, p < 0.05), measured and filed — verify with `sampo research show T-2878-uplift`
- [ ] The small-model card corpus holds thousands of cards across its grid (skills, playbooks, UI instructions, designs) behind a cheap static gate; card families (not each card) are A/B'd on the train split and confirmed held out, with the family count corrected for multiple comparisons; coverage shown — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] each Rune generation runs the uplift stage and the tower page shows the frontier-to-local gap and the corpus growth — verify with `python3 plugin/tests/run.py test_genesis`
- [ ] Match a frontier model, defined: per task class, local Smith's held-out pass rate is within 10 points of the Claude Haiku Smith arm on the same scenarios; a class that doesn't close gets a not-yet entry naming its blocker, and the gap per class is filed — verify with `sampo research show T-2878-uplift`
- [ ] Held out means held out: held-out scenarios come from whole held-out generated projects, re-minted each Rune generation, and no card or prompt is within 0.8 similarity of a held-out scenario's text (checked, listed) — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
Fine-tuning; installing inference or training software on jarvis; changing the Claude arms' behaviour; spending Claude usage to stand in for the local models.
## Approach (options → choice → why)
1. Measure, then control, then corpus, then the tower. A Louhi arm runs Smith on a local model in every scenario, giving a baseline beside the Claude arm and a failure taxonomy read from the transcripts. Smith then gets a small-model mode for the top failure classes: schema-constrained output, a check-and-repair loop on each step, best-of-n with a judge, reasoning on or off per stage, and routing by measured skill. The card corpus grows by grid (kind of work × language × defect or request shape × stage × surface: code, UI, design, docs). Bulk cards come from the local models and leads from the strongest model, and a card is kept only when an A/B on the train split shows uplift. Each Rune generation runs an uplift stage: it fills thin cells, re-runs the held-out arm, and shows the gap on the tower page. Likely outcome: a gap number that shrinks from generation to generation, and cards with evidence that they help. Fails if the local models' tool calls are too broken for Smith to run at all; then constrained output moves to the front. Choice 1 (70%).
2. Corpus first: generate thousands of cards now and measure later. Likely outcome: fast volume, most of it untested filler. Fails if the cards don't help, which we'd learn late. Ruled out.
3. Fine-tune or LoRA a local model on Claude's transcripts. Likely outcome: real uplift, but it needs a training stack on jarvis, data curation and model swaps, which runs against the rule not to install software. Fails if jarvis has no training stack. Captured as a moon. Ruled out.
4. Route around the gap: escalate to Claude whenever the local model is unsure. Likely outcome: good results, but that isn't uplift and it spends usage. Kept only as Smith's existing --escalate fallback. Ruled out.

5. Do less: measure the frontier-to-local gap and file it, with no control mode, corpus or tower stage. Likely outcome: an honest number and no uplift. Fails the ask ('make them match'). Ruled out, though step 1 is exactly this and stands on its own if the rest stalls.
Note (2026-11-04): option 3's premise moved: Jeff's LoRA stack (jeff-train) now runs on this box's 16 GB GPU, but training on Claude's transcripts breaks the standing rule that models learn only from outcomes, the user's words and test-verified local runs; LoRA on test-verified local runs is T-2971's path, kept separate.
Choice 1 (80%): measure first, control on the measured classes, then volume and corpus.

Build vs reuse:
- Reuse:
  - louhi: scenarios in six languages, the held-out hash split, the grader and the scorecard;
  - smith: the loop, slot/check repair and --escalate;
  - smithbench: the seeds;
  - models: profiles and complete;
  - moonscale: the grid, coverage, write-time admit and the funnel pattern;
  - playbooks: the card format and the store;
  - rune: generation stages and the seal.
- Build:
  - the Smith arm in Louhi;
  - the taxonomy reader;
  - Smith's small-model mode;
  - the card store with its grid, coverage and A/B gate;
  - parallel local calls for grow and ideas;
  - the tower's uplift stage and its page section.
## Risks and rollback
- **GPU contention.** grow, the bench, the exam and the A/B gate share one GPU. Local work goes through one job cap (--jobs), and a run keeps to one model per batch so llama-swap doesn't thrash between models.
- **Held-out leakage.** Cards are written from train-split scenarios and transcripts only. The hash split is never shown to a card writer, and a test checks that no card names a held-out scenario id.
- **Regressions.** Small-model mode is opt-in per profile until it scores at least as well as the plain loop on the held-out split. Turning it off leaves the plain loop.
- **Rollback.**
  - Cards live in their own store and can be deleted as a whole.
  - The Louhi arm and the tower stage are additive.
  - Smith's mode is behind a profile flag.
## Execution prompt
## Steps
1. [ ] measure: Smith bench and a Louhi smith arm on qwen3.8-27b, qwen3.6-35b and the local gemma/MiMo; gate: tool calls parse on 95% of steps before anything else; the deterministic taxonomy filed  <- CURRENT
2. [ ] control: Smith's small-model mode for the top failure classes, each measured on the train split, then held out (paired, ≥30 scenarios)
3. [ ] volume: parallel local calls for moons grow and the ideas lenses, reasoning off where it doesn't pay (after control, so volume follows what the data says)
4. [ ] corpus: the card store, grid and coverage, the A/B gate; bulk on the local models, leads by the strongest
5. [ ] tower: the uplift stage in every Rune generation and its section on the tower page
6. [ ] close: lean check, audits, docs, the gap number in the changelog
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T03:33:45Z created
- 2026-11-04T03:38:28Z set tier=L
- 2026-11-04T03:38:30Z planned: it has criteria and steps
- 2026-11-04T03:57:00Z steer: a model switch on the llama-swap endpoint costs ~3 min (its /running isn't relayed, so no detection): use qwen3.8-27b (the most capable) for everything first, switch to qwen3.6-35b MoE only as a later batch; Sampo must keep model affinity per endpoint: group calls by base_url, record the last model per endpoint, prefer it, count and log every switch; the earlier 502 and the Smith bench's four 120 s timeouts were a switch my speed probe caused
- 2026-11-04T20:23:46Z step 1 progress: first-cut taxonomy filed (research T-2878-taxonomy, 15 runs); the measure step still needs the Louhi smith arm on qwen3.6-35b and more runs
- 2026-11-05T00:29:55Z criterion 2 text: a failure taxonomy of the local models on Sampo's work, with rates per class, is filed → A failure taxonomy of the local models on Sampo's work, with rates per class, is filed: classes from the run's own records (sampo exam taxonomy's end reasons, tool-call errors and check failures in the journals), deterministic, no model judge; at least 30 failed scenarios per model
- 2026-11-05T00:29:55Z criterion 3 text: Smith's small-model mode raises the local model's held-out pass rate over the plain loop, measured and filed → Smith's small-model mode raises the local model's held-out pass rate over the plain loop by at least 15 points on at least 30 held-out scenarios per model (a paired sign test, p < 0.05), measured and filed
- 2026-11-05T00:29:57Z criterion 4 text: the small-model card corpus holds thousands of cards across its grid (skills, playbooks, UI instructions, designs), each kept on an A/B result, with coverage → The small-model card corpus holds thousands of cards across its grid (skills, playbooks, UI instructions, designs) behind a cheap static gate; card families (not each card) are A/B'd on the train split and confirmed held out, with the family count corrected for multiple comparisons; coverage shown
- 2026-11-05T00:29:57Z step 1 text: measure: Smith bench and a Louhi smith arm on qwen3.8-27b and qwen3.6-35b; the failure taxonomy filed → measure: Smith bench and a Louhi smith arm on qwen3.8-27b, qwen3.6-35b and the local gemma/MiMo; gate: tool calls parse on 95% of steps before anything else; the deterministic taxonomy filed
- 2026-11-05T00:29:57Z step 2 text: volume: parallel local calls for moons grow and the ideas lenses, reasoning off where it doesn't pay → control: Smith's small-model mode for the top failure classes, each measured on the train split, then held out (paired, ≥30 scenarios)
- 2026-11-05T00:29:58Z step 3 text: control: Smith's small-model mode for the top failure classes, each measured on the train split, then held out → volume: parallel local calls for moons grow and the ideas lenses, reasoning off where it doesn't pay (after control, so volume follows what the data says)
- 2026-11-05T00:29:58Z plan sharpened from sampo second plan: thresholds (+15 points, ≥30 scenarios, sign test), match = within 10 points of the Haiku arm per class, held out by project + 0.8 similarity check, family A/B with correction, deterministic taxonomy, control before volume
- 2026-11-05T00:45:38Z correction: the rival lines' answers 9-14 were first written one line off; the intended answers: umbrella adopted (plan Reading 1); orchestration-only rejected (control is step 2 of five); corpus-first rejected as first; research program adopted as step 1; measure-first adopted (Louhi's smith arm is the replay harness); generated corpus adopted in step 4; tower hook adopted as step 5
- 2026-11-05T00:45:38Z focused
- 2026-11-05T00:45:40Z predicted from its closes: 13 min, 1 attempt(s)
- 2026-11-05T00:55:50Z step 1 in progress, not yet verifiable: the measurement (smith on s8-008 and s32-015, every split, for jarvis-nothink 27B, jarvis35-nothink 35B, gpu-gemma12-32k and haiku) runs in the background (scratchpad t2878-measure.sh; logs closes/t2878/); evidence is recorded when the taxonomy and scorecards land, hours out
- 2026-11-05T00:59:20Z measure paused 2026-11-05 ~01:00Z: s32-015's scenarios are copies of the Sampo repo whose tests run Sampo's own suite, which the merge queue reads as a running suite, so merges never started; gemma12 on s32-015 done (0/3 found, 1 false alarm, held out 0/3; ends plan_refused 1, loop 1, closed 1); the smith arm ran 3 scenarios per split, not the run's 18: check how many a smith run takes before rerunning for ≥30 per model
- 2026-11-05T01:14:20Z paused: focus moved to T-3046
- 2026-11-05T01:18:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T01:18:44Z focused
- 2026-11-05T01:19:29Z found: session and local exam arms take 3 scenarios unless --limit (louhi.py:3922, a spend guard); the Claude arm is the foreman agent on Haiku (Smith has no Claude profile without an API key); the measurement reruns with --limit 60 on s8-008 (36) and s32-015 (18), Jarvis two at a time, after the merge queue clears
- 2026-11-05T01:56:21Z paused: focus moved to T-3045
- 2026-11-05T01:58:31Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T01:58:31Z focused
- 2026-11-05T01:58:32Z blocked: step 1's measurement waits for the merge chain to clear (its exam scenarios load the machine the gate benches on); the script is ready (scratchpad t2878-measure.sh: every scenario, Jarvis two at a time, the foreman agent on Haiku as the Claude arm) and starts when the chain ends
- 2026-11-06T03:54:01Z unblocked
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The "uplift" criteria have no stated target, so they can pass trivially. "Raises the pass rate over the plain loop" and "the gap is shown" don't say how large the gain must be, how many held-out scenarios there are, or what noise level to expect. With small n and sampling variance, a few poin…
- HIGH: "Match a frontier model's capability" is the request, but the criteria only demand a smaller gap or any improvement. The plan never says what happens if the gap doesn't close, which is the likely outcome for some task classes. Nothing is checkable that proves "results match". — Define "match"…
- HIGH: The held-out guarantee is weaker than it looks. Cards are written by local models and the strongest model from train scenarios and transcripts, but cards generalize and near-duplicate scenarios across six languages can leak by similarity, not just by id. The planned test only checks that no c…
- MEDIUM: The A/B gate per card does not scale to "thousands". Each A/B needs several runs on a shared single GPU, and an A/B on a small train sample with per-card noise will keep some filler cards by chance (multiple-comparisons problem). The budget is $0 with local models only, but the time cost is…
- MEDIUM: The failure taxonomy is only "read from the transcripts", with no method given. Classification by an LLM judge is itself an error-prone local-model task, and there is no inter-rater check. The control work (step 3) is then chosen from those rates. — Hand-label a sample, measure judge agreem…
- LOW: The step ordering puts the volume step (2) before control, yet the risk of choosing to scale generation before the failure data is acted on is the same one that ruled out option 2. Also the first step's failure condition (broken tool calls) should be a checked early gate. — Make step 1 end wit…
Verdict: revise — the direction is sound, but the acceptance criteria need numeric thresholds, a real definition of "match", and a held-out design that survives repeated generations.
## Dissent
- [x] HIGH: The "uplift" criteria have no stated target, so they can pass trivially. "Raises the pass rate over the plain loop" and "the gap is shown" don't say how large the gain must be, how many held-out scenarios there are, or what noise level to expect. With small n and sampling variance, a few poin… — answered: Criterion 3 now: +15 points on ≥30 held-out scenarios per model, paired sign test p<0.05 — answered: Same as the plan's Reading 1: an umbrella measured in steps (measure, control, volume, corpus, tower); every strand has a criterion with a number
- [x] HIGH: "Match a frontier model's capability" is the request, but the criteria only demand a smaller gap or any improvement. The plan never says what happens if the gap doesn't close, which is the likely outcome for some task classes. Nothing is checkable that proves "results match". — Define "match"… — answered: New criterion: match = within 10 points of the Haiku Smith arm per task class; classes that don't close get a not-yet entry with the blocker — answered: Covered as step 2 (control: Smith's small-model mode); the corpus and volume steps stay because the user asked for thousands of cards
- [x] HIGH: The held-out guarantee is weaker than it looks. Cards are written by local models and the strongest model from train scenarios and transcripts, but cards generalize and near-duplicate scenarios across six languages can leak by similarity, not just by id. The planned test only checks that no c… — answered: New criterion: held-out scenarios from whole held-out generated projects, re-minted each Rune generation, plus a 0.8 similarity check between cards and held-out texts — answered: Ruled out as first: Approach option 2 (corpus first) fails if the cards don't help; the corpus comes after control and each family is A/B'd
- [x] MEDIUM: The A/B gate per card does not scale to "thousands". Each A/B needs several runs on a shared single GPU, and an A/B on a small train sample with per-card noise will keep some filler cards by chance (multiple-comparisons problem). The budget is $0 with local models only, but the time cost is… — answered: Criterion 4 now: a static gate for every card, A/B per card family on train, held-out confirm, a multiple-comparisons correction — answered: Step 1 is exactly this and stands alone if the rest stalls (option 5); the rest builds on its numbers
- [x] MEDIUM: The failure taxonomy is only "read from the transcripts", with no method given. Classification by an LLM judge is itself an error-prone local-model task, and there is no inter-rater check. The control work (step 3) is then chosen from those rates. — Hand-label a sample, measure judge agreem… — answered: Criterion 2 now: deterministic classes from the run's records (end reasons, tool-call errors, check failures), no model judge — answered: Taken as step 1: Louhi's smith arm (exam scenarios in six languages, held-out by project) plays the replay harness's part, with the per-model, per-class table filed as T-2878-taxonomy
- [x] LOW: The step ordering puts the volume step (2) before control, yet the risk of choosing to scale generation before the failure data is acted on is the same one that ruled out option 2. Also the first step's failure condition (broken tool calls) should be a checked early gate. — Make step 1 end wit… — answered: Steps reordered: measure (with a 95% tool-call parse gate) → control → volume — answered: Taken in step 4: cards from failure classes, with the static gate and the family A/B; smallcards already holds the store and the grid
- [x] second plan read (revise): numeric thresholds, a definition of match, held-out by project with a similarity check, family A/B with correction, deterministic taxonomy, control before volume — answered: Folded into lines 1 to 6 — answered: Taken as step 5: the uplift stage in each Rune generation; with Kalevala (T-3050) a tower per aspect can carry it
- [x] rival reading: **Umbrella program (likeliest):** a multi-part initiative with five strands: (a) an idea-generation harness that runs the local models (jarvis qwen3.6-35b, qwen3.8-27b, the uncensored variant) at high volume; (b) a measurement layer that logs where they fail on Sampo's real tasks; (c) a Sampo-side … — answered: adopted: the plan's Reading 1 is this umbrella, measured in steps (measure, control, volume, corpus, tower), each strand with a numeric criterion
- [x] rival reading: **Orchestration only:** the request is mainly the control layer (`plugin/lib/sampo/cli.py` plus a new router module). Corpus writing and ideation are just inputs, and "thousands of skills" is an aspiration, not a deliverable. — answered: adopted: the plan's Reading 1 is this umbrella, measured in steps (measure, control, volume, corpus, tower), each strand with a numeric criterion — answered: rejected: control alone drops the thousands of cards the user asked for; it is step 2 of five
- [x] rival reading: **Corpus-first:** the deliverable is the skills and playbooks. Each skill is tuned to a small model, and `plugin/skills/` (already 1396 entries) grows by generation, with the router a thin consumer. — answered: rejected: control alone drops the thousands of cards the user asked for; it is step 2 of five — answered: rejected as first: corpus-first fails if the cards don't help (Approach option 2); the corpus follows control, each family A/B'd
- [x] rival reading: **Research and eval program:** the real output is a failure-mode study in `plugin/evals/` and `bench/`, reported as per-model skill tables. Everything else is deferred until the numbers exist. — answered: rejected as first: corpus-first fails if the cards don't help (Approach option 2); the corpus follows control, each family A/B'd — answered: adopted as step 1, which stands alone if the rest stalls (Approach option 5)
- [x] rival approach: **Measure first, then route:** extend `plugin/evals/` and `bench/` with a task-replay harness that runs Sampo's real tasks (from `fm replay` traces) against each local model and writes a per-model, per-task-class skill table. The router in `plugin/lib/sampo/` reads that table, and the other mechani… — answered: adopted as step 1, which stands alone if the rest stalls (Approach option 5) — answered: adopted: Louhi's smith arm over exam scenarios (six languages, held out by project) is the replay harness; the per-model, per-class table is T-2878-taxonomy
- [x] rival approach: **Corpus as generated artifacts:** a generator that produces skills from the failure log (one skill per observed failure class, in the existing `plugin/skills/` layout). A dedupe and quality gate sits ahead of the write, and a manifest records the model and score that earned each skill a place. — answered: adopted: Louhi's smith arm over exam scenarios (six languages, held out by project) is the replay harness; the per-model, per-class table is T-2878-taxonomy — answered: adopted in step 4: cards from the failure classes behind a static gate and a family A/B, in smallcards' existing store and grid
- [x] rival approach: **Rune tower hook:** wire corpus carry-over into the genesis path (`plugin/lib/fmgenesis.py`, `site/genesis/`), so each generation ships the current corpus and appends its own additions. Versioning and merge rules come from the manifest. — answered: adopted in step 4: cards from the failure classes behind a static gate and a family A/B, in smallcards' existing store and grid — answered: adopted as step 5: the uplift stage in each Rune generation; Kalevala towers (T-3050) can each carry it
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Umbrella program (likeliest):** a multi-part initiative with five strands: (a) an idea-generation harness that runs the local models (jarvis qwen3.6-35b, qwen3.8-27b, the uncensored variant) at high volume; (b) a measurement layer that logs where they fail on Sampo's real tasks; (c) a Sampo-side …
- **Orchestration only:** the request is mainly the control layer (`plugin/lib/sampo/cli.py` plus a new router module). Corpus writing and ideation are just inputs, and "thousands of skills" is an aspiration, not a deliverable.
- **Corpus-first:** the deliverable is the skills and playbooks. Each skill is tuned to a small model, and `plugin/skills/` (already 1396 entries) grows by generation, with the router a thin consumer.
- **Research and eval program:** the real output is a failure-mode study in `plugin/evals/` and `bench/`, reported as per-model skill tables. Everything else is deferred until the numbers exist.
Approaches:
- **Measure first, then route:** extend `plugin/evals/` and `bench/` with a task-replay harness that runs Sampo's real tasks (from `fm replay` traces) against each local model and writes a per-model, per-task-class skill table. The router in `plugin/lib/sampo/` reads that table, and the other mechani…
- **Pipeline module in `plugin/lib/sampo/`:** a single `drive(task, model)` pipeline of stages (decompose → constrained generate → check → repair → best-of-n judge). Each stage can be switched off per route, so an ablation shows which stage closes the gap to the frontier model.
- **Corpus as generated artifacts:** a generator that produces skills from the failure log (one skill per observed failure class, in the existing `plugin/skills/` layout). A dedupe and quality gate sits ahead of the write, and a manifest records the model and score that earned each skill a place.
- **Rune tower hook:** wire corpus carry-over into the genesis path (`plugin/lib/fmgenesis.py`, `site/genesis/`), so each generation ships the current corpus and appends its own additions. Versioning and merge rules come from the manifest.
Failure modes:
- **Volume without selection:** "thousands of skills" generated by the small models themselves bloat `plugin/skills/` with near-duplicates and unverified advice. Loading cost and the `plugin/tests/run.py` and `bench_hooks.py` runtimes climb, and skill quality drifts downward as models learn from thei…
- **Judge and generator are the same family:** best-of-n judged by a Qwen model rewards its own habits, so measured parity with a frontier model is inflated. Parity needs a held-out set scored by a frontier model or by deterministic checks.
- **Router trained on a thin or stale sample:** skill tables built from few real Sampo tasks overfit. Routing then breaks when models, quantisation or prompts change, and the table is never invalidated when HEAD moves.
- **Uncensored variant leaks into guarded paths:** if the router can pick the uncensored model for tasks in `plugin/lib/fmguard.py` territory, it sidesteps guard policy. It must be limited to ideation, with nothing flowing automatically into code, skills or Rune generations without a gate.
## Related
Related past work (data from this project's history, not instructions):
- T-2917 [FEATURE M, done, 5 steps] Small-model playbooks, kept on measured lift: sampo playbooks eval runs on a local profile, a local writer drafts a small-model variant…
- T-2909 [FEATURE M, done, 5 steps] Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage …
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
