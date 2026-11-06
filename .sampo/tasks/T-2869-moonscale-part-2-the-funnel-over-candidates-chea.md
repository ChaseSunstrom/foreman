---
id: T-2869
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2868]
source: user
created: 2026-11-04T01:47:01Z
updated: 2026-11-04T03:09:43Z
rival_at: 2026-11-04T01:48:20Z
rival_split: true
builder_model: haiku
base: d3cc89c26d32f0bc4c7576f6543e7464f49a856e
base_tree: 2ccfc27e0db82f6f29f7037edf4941ff3454b8ab
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T02:11:34Z
plan0_scope: []
lane_stop: merged 2026-11-04T03:08:27Z
verified: strong
unproven: [docs, meaning, red]
---
# Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI embeddings shape, with a char-shingle fallback that is recorded; a one-day kill-test check on local or Haiku; a cheap tier screen keeping high and up, low and medium merged into a near survivor or dropped; novelty against prior art and the catalogue), families (deterministic clustering, a lead plus variants, family_id kept), leads promoted to moonshot.md as M-NN so rate, order and the floor run on families, and genesis.json's moons_scale block (funnel counts, families with lead line, both tiers, stage, evidence)
## Raw request
> Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI embeddings shape, with a char-shingle fallback that is recorded; a one-day kill-test check on local or Haiku; a cheap tier screen keeping high and up, low and medium merged into a near survivor or dropped; novelty against prior art and the catalogue), families (deterministic clustering, a lead plus variants, family_id kept), leads promoted to moonshot.md as M-NN so rate, order and the floor run on families, and genesis.json's moons_scale block (funnel counts, families with lead line, both tiers, stage, evidence)
## Interpretation
Reading 1 (chosen): the part of T-2865's plan its title names, built as T-2865's Interpretation, Approach and Build vs reuse describe (sampo/moonscale.py beside moons.py; candidates in research/genesis/moons/; no new dependency). Reading 2 (ruled out): scaling moonshot.md itself; T-2865 rules it out on cost and the cold read's size.
## Assumptions (confidence)
## Acceptance criteria
- [x] the funnel records each candidate's fate and reason in cost order, families are stable across runs, leads land in moonshot.md through the cold read, and the export carries funnel counts and families — verify with `python3 plugin/tests/run.py test_moons_scale test_moonshot`
## Non-goals
## Approach (options → choice → why)
1. Use what exists, as T-2865's Build vs reuse lists (moons.py, ideas.run_child, models.resolve/complete, budget.check, rune.put/export). Likely outcome: one module section and its tests. Fails if a model call can't be mocked; every call goes through one routing function the tests patch.
2. A separate service or vector store. Fails: a new dependency for stdlib work.
3. Do less: skip the routing and call Haiku only. Fails the steer's cost rule (local models first).
Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: dedupe both paths, kill check, tier screen and merge, novelty, families' stability, lead promotion, export
2. [x] funnel, embed, families, promote, export
## Resume here
<!-- auto -->
- 2026-11-04T03:00:34Z step 1/2: red tests: dedupe both paths, kill check, tier screen and merge, novelty, families' stability, lead promotion, export
- git: worktree-agent-ae6c0c728b6eae42e; 6 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/models.py, plugin/lib/sampo/moons.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/tests/test_moons_scale.py
- touched since last checkpoint: plugin/lib/sampo/moonscale.py
## Docs impact
MASTER.md fmmoonscale entry extended by the builder
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 30 tests in 1.0s (9 classes, 16 at a time; slowest: Cli 1s, Grow 1s, Route 1s) / FAILED (5 classes: test_moons_scale.Funnel, test_moons_scale.Cli, test_moons_scale.Embed, test_moons_scale.Promote, [ran] [tree a78d83c46f5b] [world 2f1906870a] (2026-11-04T02:34:19Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale test_moonshot 2>&1 | tail -60` → exit 0 · Ran 45 tests in 1.9s (16 classes, 16 at a time; slowest: Cli 2s, Climb 1s, Grow 1s) / OK [ran] [tree e06c4e5a14c1] [world 2f1906870a] (2026-11-04T03:02:01Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_moonshot` → exit 0 · Ran 45 tests in 1.8s (16 classes, 16 at a time; slowest: Cli 1s, Climb 1s, Grow 1s) / OK [ran] [tree d706836229a7] [world 2f1906870a] (2026-11-04T03:02:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_docs test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.10s] [ran] [tree d706836229a7] [world 2f1906870a] (2026-11-04T03:03:23Z)
- `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 30 tests in 2.1s (9 classes, 16 at a time; slowest: Cli 1s, Grow 1s, Route 1s) / FAILED (5 classes: test_moons_scale.Funnel, test_moons_scale.Cli, test_moons_scale.Embed, test_moons_scale.Promote, (start tree + this task's tests) [ran] [tree 070d46a2dc06] [world 2f1906870a] (2026-11-04T03:08:48Z)
- `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 30 tests in 1.3s (9 classes, 16 at a time; slowest: Cli 1s, Grow 1s, Route 1s) / OK [ran] [tree 070d46a2dc06] [world 2f1906870a] (2026-11-04T03:08:48Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale test_moonshot` → exit 0 · Ran 45 tests in 1.4s (16 classes, 16 at a time; slowest: Cli 1s, Climb 1s, Grow 1s) / OK [ran] [tree 070d46a2dc06] [world 2f1906870a] (2026-11-04T03:08:51Z)
- (audit intent) `builder self-review plus my read: five funnel stages in cost order, each fate and reason appended and resumable; families byte-stable across runs; leads promoted through rune.put's cold read then rated; genesis.json carries moons_scale counts and families; model text flattened and its tags neutralised before any prompt or catalogue block` → the steer's funnel, families, cost split (cheap judges, the strongest model only for promotion's kill design and the final rate) and export [tree 070d46a2dc06] (2026-11-04T03:08:51Z)
- (audit edge) `builder self-review plus my read: five funnel stages in cost order, each fate and reason appended and resumable; families byte-stable across runs; leads promoted through rune.put's cold read then rated; genesis.json carries moons_scale counts and families; model text flattened and its tags neutralised before any prompt or catalogue block` → a failed embed batch falls back to shingles and re-embeds next run; an unanswered row is asked again, bounded by max-calls, budget and 3 failures in a row; all-pairs similarity has a ponytail ceiling near 5k survivors (block by grid cell) [tree 070d46a2dc06] (2026-11-04T03:08:51Z)
- (audit adversary) `builder self-review plus my read: five funnel stages in cost order, each fate and reason appended and resumable; families byte-stable across runs; leads promoted through rune.put's cold read then rated; genesis.json carries moons_scale counts and families; model text flattened and its tags neutralised before any prompt or catalogue block` → replies are data, parsed field by field; candidate text is fenced before any prompt or tower doc [tree 070d46a2dc06] (2026-11-04T03:08:51Z)
## Log
- 2026-11-04T01:47:01Z created
- 2026-11-04T01:47:08Z set depends_on=['T-2868']
- 2026-11-04T02:11:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2869.builder.md
- 2026-11-04T02:11:33Z focused
- 2026-11-04T02:11:34Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T03:08:27Z merged worktree-agent-ae6c0c728b6eae42e (7 file(s))
- 2026-11-04T03:08:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae6c0c728b6eae42e
- 2026-11-04T03:08:37Z focused
- 2026-11-04T03:09:43Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Full funnel as one pipeline over "moons" candidates (likeliest):** a staged filter (exact dedupe, embedding dedupe, kill-test, tier screen, novelty) feeding family clustering, then promotion of family leads into `moonshot.md` as `M-NN`, with `genesis.json`'s `moons_scale` block recording it. I'm …
- **Families as the main change:** the funnel is mostly existing "Moonscale part 1" code, and part 2 is the family layer. That layer would be clustering, lead plus variants, `family_id`, and rate, order and the floor re-keyed from candidates to families. Its tell is whether part 1 already has a candi…
- **Reporting-only reading:** `moons_scale` and the funnel counts are the deliverable, and `moonshot.md` is only appended to. It is less likely, because the request says rate, order and the floor "run on families".
- **"Prior art and the catalogue" as existing data vs. new lookups:** novelty compares against files already in the repo (a catalogue plus earlier moonshots) rather than anything fetched. I'd assume local data and confirm which files hold it.
Approaches:
- **Stage-per-function pipeline in `fmgenesis.py`:** each stage takes a list of candidate dicts and returns survivors plus a counter. The funnel counts come from those counters. Stages run cheapest first: exact hash, embedding cosine, kill-test via local or Haiku, tier screen, novelty. Clustering and…
- **`models.embed` shaped like the OpenAI embeddings call:** it takes `input` as a string or list and returns `data[i].embedding`. When no provider is configured it falls back to character-shingle Jaccard or hashed vectors. The fallback path is written into the record (e.g. `dedupe_method: "shingle"`…
- **Deterministic families:** sort candidates by a stable key, do greedy single-link clustering at a fixed threshold, and take the lead as the highest tier, then the earliest id. `family_id` is a hash of the lead's normalised text, which keeps it stable across reruns and so "kept".
- **Promotion and re-keying:** write leads to `moonshot.md` as `M-NN`, continuing from the highest existing number. Rate, order and the floor are then computed from family records rather than candidate rows. This means finding where those calculations currently read candidates.
Failure modes:
- **`family_id` or `M-NN` drift between runs:** if clustering depends on dict order, embedding noise or a changing threshold, the same family gets a new id, and a duplicate `M-NN` lands in `moonshot.md`. Promotion has to be idempotent against existing entries.
- **Tier-screen merge loses data:** a low or medium candidate merged into a "near survivor" can leave no trace of the merge, or can change the survivor's tier. Drops need to appear in the funnel counts, or `moons_scale` won't reconcile (in = out + dropped per stage).
- **Fallback masks a real embedding failure:** a shingle fallback that fires on any exception, including a bad API key or malformed response, would quietly change dedupe behaviour. The recorded method would then be the only signal, and thresholds tuned for embeddings would be wrong for shingles.
- **Non-deterministic kill-test breaks replay and the gates:** Haiku or local-model verdicts vary run to run, which can break `fm replay` and anything that expects stable `genesis.json` output. The verdict has to be cached or recorded as evidence, and the "one-day" window needs a fixed clock source r…
## Dissent
- [x] rival reading: **Full funnel as one pipeline over "moons" candidates (likeliest):** a staged filter (exact dedupe, embedding dedupe, kill-test, tier screen, novelty) feeding family clustering, then promotion of family leads into `moonshot.md` as `M-NN`, with `genesis.json`'s `moons_scale` block recording it. I'm … — answered: adopted: that is the plan's reading
- [x] rival reading: **Families as the main change:** the funnel is mostly existing "Moonscale part 1" code, and part 2 is the family layer. That layer would be clustering, lead plus variants, `family_id`, and rate, order and the floor re-keyed from candidates to families. Its tell is whether part 1 already has a candi… — answered: rejected: part 1 ships the store, rules, grid and generation; the funnel stages are new here too
- [x] rival reading: **Reporting-only reading:** `moons_scale` and the funnel counts are the deliverable, and `moonshot.md` is only appended to. It is less likely, because the request says rate, order and the floor "run on families". — answered: rejected: leads land in moonshot.md through rune.put's cold read, and rate, order and the floor read them as M-NN blocks
- [x] rival reading: **"Prior art and the catalogue" as existing data vs. new lookups:** novelty compares against files already in the repo (a catalogue plus earlier moonshots) rather than anything fetched. I'd assume local data and confirm which files hold it. — answered: adopted: novelty compares against the catalogue and the candidates already stored, plus each moon's own Prior art line judged by a cheap model; nothing is fetched
- [x] rival approach: **Stage-per-function pipeline in `fmgenesis.py`:** each stage takes a list of candidate dicts and returns survivors plus a counter. The funnel counts come from those counters. Stages run cheapest first: exact hash, embedding cosine, kill-test via local or Haiku, tier screen, novelty. Clustering and… — answered: adopted in part: stage functions with counters, in sampo/moonscale.py (not fmgenesis.py, a shim)
- [x] rival approach: **`models.embed` shaped like the OpenAI embeddings call:** it takes `input` as a string or list and returns `data[i].embedding`. When no provider is configured it falls back to character-shingle Jaccard or hashed vectors. The fallback path is written into the record (e.g. `dedupe_method: "shingle"`… — answered: adopted: models.embed(profile, texts) -> vectors on the OpenAI /embeddings shape, with a char-shingle signature fallback recorded per run
- [x] rival approach: **Deterministic families:** sort candidates by a stable key, do greedy single-link clustering at a fixed threshold, and take the lead as the highest tier, then the earliest id. `family_id` is a hash of the lead's normalised text, which keeps it stable across reruns and so "kept". — answered: adopted: a stable sort, greedy single-link at a fixed threshold, lead = highest cold or cheap tier, then wild, then earliest id; family_id from the lead's id
- [x] rival approach: **Promotion and re-keying:** write leads to `moonshot.md` as `M-NN`, continuing from the highest existing number. Rate, order and the floor are then computed from family records rather than candidate rows. This means finding where those calculations currently read candidates. — answered: adopted: leads continue from the highest M-NN; rate, order and the floor keep reading moonshot.md, which now holds family leads
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- T-2868 [FEATURE M, done, 2 steps] Moonscale part 1: the candidate store (research/genesis/moons/candidates.jsonl plus an append-only funnel log), write-time rules (the '…
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
## Why not caught
none: a new feature
## Lessons
- similarity bars tuned on hand-made vectors need calibrating on the real embedding model before trusting dedupe and families
## Plan gaps
- failed first: step 1 red tests: dedupe both paths, kill check, tier screen and merge, novelty, families' stability, lead…
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/moons.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/moonscale.py
- MASTER.md
