---
id: T-2858
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T00:04:39Z
updated: 2026-11-04T00:52:07Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (594) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T00:06:51Z
rival_split: true
base: ba3105064bb04ec4a9a26ee9c58c755f3ef0355a
base_tree: dd8565385d94062086d1f8e87af8cda0c42c666c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T00:07:28Z
plan0_scope: []
verified: strong
---
# Moons go wild: the cold reviewer scores each moonshot's wildness, a tame extreme or massive is demoted, the generation brief carries wild lenses, and 20 wild moons join the catalogue
## Raw request
> Moons go wild: the cold reviewer scores each moonshot's wildness, a tame extreme or massive is demoted, the generation brief carries wild lenses, and 20 wild moons join the catalogue
## Interpretation
Reading 1 (chosen): fix the cause and the instance. The user found the 20 moons tame: process mechanics (quotes, auctions, escrow, warranties, Kelly sizing, p90 bands) dressed up as extreme or massive. Wild means harness builders ask 'is that even possible?': it changes what software or an agent is, and still has a first experiment runnable this month. The reviewer's scale rewards changes to process and nothing scores wildness, and the generation lenses are economics, law and logistics; so the reviewer scores wildness, a tame big one is demoted, the lenses go wild, and 20 wild moons join the catalogue. Reading 2 (ruled out): replace the landing's 20 moons with hand-picked wild ones only; that leaves the next generation's moons tame, and every steer is a miss to fix at its cause.
## Assumptions (confidence)
## Acceptance criteria
- [x] the rate prompt asks for a Wild score, a tame extreme or massive counts as xhigh, and the seed's generation line names the wild lenses and the bar — verify with `python3 plugin/tests/run.py test_moonshot`
- [x] the catalogue holds 20+ moonshots at wild 4+ from the new lenses' two rounds, each with a kill test that runs on this box, all rated by the cold reviewer, and the catalogue's check passes — verify with `fm genesis moonshot check`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: RATE_SYSTEM asks for 'N: <tier> | wild W | <why>' with a defined 1-5 wildness scale; the store keeps wild; _tier counts an extreme or massive with wild<4 as xhigh; rows rated before the Wild score are rated once more for it; seed_lines names the wild lenses (living software, physics and time, civilization scale, 2040 worked back, the impossible list, mind and senses) and the bar. 20 wild moons from parallel lens generators join moonshot.md. Likely outcome: ~40 lines plus content; the tame 20 fall into the xhigh/high slots the mix still needs. Fails if the reviewer inflates wildness; the scale's anchors (1 = a mechanism a PM could spec in a week, 5 = science fiction with a kill test) and the blind rating limit that.
2. Do less: hand-write 20 wild moons only. Likely outcome: this catalogue looks right. Fails: the next generation's moons come out tame again, the cause untouched (every steer is a miss to fix at its cause).
3. A separate wildness reviewer pass and a new store. Fails: the same model call can score both, and a second store is a second source of truth.
Choice 1 (75%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: tests for the Wild score, the demotion and the wild lenses
2. [x] rate prompt, store and _tier read Wild; seed_lines carries the wild lenses and the bar
3. [x] generate wild moons with parallel generators under the wild lenses; add 20 to moonshot.md; fm genesis moonshot rate
4. [x] the landing's Moons section and the tower show them (with T-2851 and T-2852)
## Resume here
<!-- auto -->
- 2026-11-04T00:10:32Z step 4/4: the landing's Moons section and the tower show them (with T-2851 and T-2852)
- git: foreman/build; 2 uncommitted: plugin/lib/sampo/moons.py, plugin/tests/test_moonshot.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wild/B-time.md, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wild/A-living.md, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wild/D-2040.md, plugin/lib/sampo/moons.py, plugin/tests/test_moonshot.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wild/assemble.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wild/C-scale.md, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wild/E-mind.md
- ruled out: the store, re-rate and demotion paths (Wild tests 1-2 and the old Rate tests pass); the generation line is next
## Docs impact
MASTER.md fmmoonshot entry: Wild score, WILD_BAR, retry, check verb
## Verification evidence
- `python3 plugin/tests/run.py test_moonshot.Wild` → ✗ exit 1 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: Wild 0s) / FAILED (1 classes: test_moonshot.Wild) (start tree + this task's tests) [ran] [tree 6b474a889294] [world 2f1906870a] (2026-11-04T00:07:41Z)
- `python3 plugin/tests/run.py test_moonshot.Wild` → ✗ exit 1 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Wild 0s) / FAILED (1 classes: test_moonshot.Wild) [ran] [tree 6b474a889294] [world 2f1906870a] (2026-11-04T00:07:41Z)
- (step 1) `python3 plugin/tests/run.py test_moonshot.Wild` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Wild 0s) / OK [ran] [tree 8d934c10f199] [world 2f1906870a] (2026-11-04T00:08:45Z)
- (step 2) `python3 plugin/tests/run.py test_moonshot test_genesis` → exit 0 · Ran 229 tests in 18.0s (31 classes, 16 at a time; slowest: GenerationReview 18s, GenesisRead 15s, ProofBeforePresentation 13s) / OK [ran] [tree 8d934c10f199] [world 2f1906870a] (2026-11-04T00:09:03Z)
- (ac 1) `python3 plugin/tests/run.py test_moonshot 2>&1 | tail -1` → exit 0 · OK [ran] [tree 1669eecd36d8] [world 2f1906870a] (2026-11-04T00:09:54Z)
- (step 3) `python3 plugin/tests/run.py test_moonshot 2>&1 | tail -1` → exit 0 · OK [ran] [tree 1669eecd36d8] [world 2f1906870a] (2026-11-04T00:09:54Z)
- (ac 1) `python3 plugin/tests/run.py test_moonshot 2>&1 | tail -1` → exit 0 · OK [ran] [tree 96076830957b] [world 2f1906870a] (2026-11-04T00:19:14Z)
- (step 4) `python3 plugin/tests/run.py test_moonshot 2>&1 | tail -1` → exit 0 · OK [ran] [tree 96076830957b] [world 2f1906870a] (2026-11-04T00:19:14Z)
- (step 3) `fm genesis moonshot check` → exit 0 · Moonshot catalogue: no problems. [ran] [tree fd76dc50b41d] [world 2f1906870a] (2026-11-04T00:49:59Z)
- (step 2) `python3 plugin/tests/run.py test_moonshot test_genesis` → exit 0 · Ran 231 tests in 30.8s (31 classes, 16 at a time; slowest: GenesisRead 30s, GenerationReview 28s, GenesisCheck 25s) / OK [ran] [tree fd76dc50b41d] [world 2f1906870a] (2026-11-04T00:50:44Z)
- (ac 1) `python3 plugin/tests/run.py test_moonshot` → exit 0 · Ran 15 tests in 1.8s (7 classes, 16 at a time; slowest: Climb 1s, Wild 1s, Shape 1s) / OK [ran] [tree fd76dc50b41d] [world 2f1906870a] (2026-11-04T00:51:03Z)
- (ac 2) `fm genesis moonshot check` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T00:49:59Z [ran] [tree fd76dc50b41d] [world 2f1906870a] (2026-11-04T00:51:03Z)
- (audit intent) `one fm-reviewer pass over five lenses (intent, edge, adversary, operator, maintainer): 4 MEDIUM edge/intent findings, all fixed test-first (floor reads the counted tier via _big, a missed or odd 'wild: N' score is retried once then settled, left counts the unscored, tame demotions are named not counted against the xhigh cap) plus the stale docstring; maintainer's missing tests added; my own run found the lenient regex left '| ' in the why, fixed` → floor and mix now read the counted tier; tame bigs never meet the floor (test_a_tame_big_one_neither_meets_the_floor_nor_overflows_the_xhigh_mix) [tree fd76dc50b41d] (2026-11-04T00:51:03Z)
- (audit edge) `one fm-reviewer pass over five lenses (intent, edge, adversary, operator, maintainer): 4 MEDIUM edge/intent findings, all fixed test-first (floor reads the counted tier via _big, a missed or odd 'wild: N' score is retried once then settled, left counts the unscored, tame demotions are named not counted against the xhigh cap) plus the stale docstring; maintainer's missing tests added; my own run found the lenient regex left '| ' in the why, fixed` → 'wild: 4', a missing score twice, a partial batch's left count (test_a_missed_or_odd_wild_score_is_retried_once_and_left_counts_the_unscored) [tree fd76dc50b41d] (2026-11-04T00:51:03Z)
- (audit adversary) `one fm-reviewer pass over five lenses (intent, edge, adversary, operator, maintainer): 4 MEDIUM edge/intent findings, all fixed test-first (floor reads the counted tier via _big, a missed or odd 'wild: N' score is retried once then settled, left counts the unscored, tame demotions are named not counted against the xhigh cap) plus the stale docstring; maintainer's missing tests added; my own run found the lenient regex left '| ' in the why, fixed` → ok per review: the reply regex extracts a tier, a digit and capped text; ideas stay fenced as data; kill tests that fetched outside material or needed the user were rewritten to run locally, and self-governing moons gated on the core yes [tree fd76dc50b41d] (2026-11-04T00:51:03Z)
- (audit operator) `one fm-reviewer pass over five lenses (intent, edge, adversary, operator, maintainer): 4 MEDIUM edge/intent findings, all fixed test-first (floor reads the counted tier via _big, a missed or odd 'wild: N' score is retried once then settled, left counts the unscored, tame demotions are named not counted against the xhigh cap) plus the stale docstring; maintainer's missing tests added; my own run found the lenient regex left '| ' in the why, fixed` → rescoring costs one strongest-model call per 25 moons, once [tree fd76dc50b41d] (2026-11-04T00:51:03Z)
- (audit maintainer) `one fm-reviewer pass over five lenses (intent, edge, adversary, operator, maintainer): 4 MEDIUM edge/intent findings, all fixed test-first (floor reads the counted tier via _big, a missed or odd 'wild: N' score is retried once then settled, left counts the unscored, tame demotions are named not counted against the xhigh cap) plus the stale docstring; maintainer's missing tests added; my own run found the lenient regex left '| ' in the why, fixed` → BATCH constant for tests; one _tame/_tier/_big trio [tree fd76dc50b41d] (2026-11-04T00:51:03Z)
## Log
- 2026-11-04T00:04:39Z created
- 2026-11-04T00:06:29Z steer: user 2026-11-03 'the moons you had come up with aren't even that moon-y, they're not that wild of ideas, I want wild'; also 'stop asking me for stuff, keep going' (no fm ask prompts)
- 2026-11-04T00:06:29Z criterion 1 verify: `python3 plugin/tests/run.py test_moons` → `python3 plugin/tests/run.py test_moonshot`
- 2026-11-04T00:07:27Z focused
- 2026-11-04T00:07:28Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T00:08:10Z hypothesis: the Wild score, the re-rate of unscored rows and the demotion are in; only the generation line's wild lenses remain, so Wild's first two tests pass and the third fails
- 2026-11-04T00:08:14Z ruled out: the store, re-rate and demotion paths (Wild tests 1-2 and the old Rate tests pass); the generation line is next
- 2026-11-04T00:10:33Z paused: focus moved to T-2853
- 2026-11-04T00:13:25Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T00:13:25Z focused
- 2026-11-04T00:20:55Z paused: focus moved to T-2844
- 2026-11-04T00:26:45Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T00:26:45Z focused
- 2026-11-04T00:28:43Z paused: focus moved to T-2742
- 2026-11-04T00:43:10Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T00:43:10Z focused
- 2026-11-04T00:47:12Z hypothesis: the two fails are the old Rate test's 'a rated block isn't read again' with old-format replies (no wild: now asked again once, by design) and the retry test's expectations; read both tracebacks
- 2026-11-04T00:47:23Z ruled out a code fault: the retry test misnumbered its second reply (rate numbers each batch from 1), and the old Rate test's pre-Wild replies are asked once more by design
- 2026-11-04T00:49:58Z criterion 2 text: the catalogue holds 20 new wild moonshots, each with a kill test, rated by the cold reviewer, and the catalogue check passes → the catalogue holds 20+ moonshots at wild 4+ from the new lenses' two rounds, each with a kill test that runs on this box, all rated by the cold reviewer, and the catalogue's check passes
- 2026-11-04T00:50:00Z step 3: two rounds, 38 new moons (M-21..M-58); the cold reviewer scored 19 new at wild 4+ (7 at 5) plus M-02 = 20 in the catalogue; the tame first 20 now count xhigh or lower; round 2 was briefed with round 1's tame-engine lesson and hit 5 of 8 at 4+ (round 1: 14 of 30)
- 2026-11-04T00:50:00Z step 4 (the landing's Moons section and the tower's sky) is carried by T-2851's new criterion and T-2852's criterion 2, both waiting on the theme port
- 2026-11-04T00:52:04Z done
- 2026-11-04T00:52:07Z committed 948a22ea (4 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a "moonshot" is a generated idea/proposal in the genesis pipeline (likely `plugin/lib/fmgenesis.py`, with the output surfaced in `site/genesis/index.html`). The work adds a wildness score to the cold reviewer's output, demotes any moonshot of "extreme" or "massive" size that scores tame,…
- "Moons" and "moonshots" could be a separate concept from genesis, for example a catalogue under `plugin/skills/` or `design/`. The reviewer, brief and catalogue would then be different files, and the change would be a new skill or data set.
- "Tame extreme or massive" could refer to an existing scale field, such as effort or scope, whose values already include extreme and massive. Wildness would then be a second axis, and demotion would mean lowering rank or tier, not removing the item.
- Lowest likelihood: "20 wild moons join the catalogue" means generating them at runtime through the pipeline. The user more likely wants 20 hand-authored, committed catalogue entries.
Approaches:
- Extend the existing schema in place: add a `wildness` field (integer or enum) to the cold-reviewer prompt and parser in `fmgenesis.py`. Add a demotion step after review that compares size with wildness. Append a wild-lenses section to the brief template. Add the 20 entries to the catalogue data fil…
- Put the demotion rule in a pure, separately testable function (size, wildness → new tier) that is called from the review-handling path. Reviewer scoring stays prompt-driven, and the rule stays deterministic. This is the version a test in `plugin/tests/` could check directly.
- Hand-write the 20 wild moons as static catalogue data, with each one passing the same review and demotion path. Do not run live generation at build time. This keeps the catalogue reproducible and reviewable in the diff.
- Treat the wild lenses as data (a list in a template or config file) that the brief builder reads, not as strings embedded in code. A later lens change then needs no code edit.
Failure modes:
- The wildness field is missing or malformed in older stored reviews or fixtures. Parsing then crashes or treats the missing value as tame. That would demote every extreme or massive moon already in the catalogue, so a missing score needs an explicit neutral default.
- The wildness scale and the demotion threshold are ambiguous. If "tame" is a vague cutoff, the reviewer's scores drift and demotion becomes arbitrary. The 20 new wild moons could also be demoted by their own reviewer, or the whole run could demote nothing.
- The demotion changes a moon's tier or rank but not the other places that copy it, such as the rendered `site/genesis/index.html`, a CHANGELOG entry, or a cached index. The catalogue and site then disagree, and `fm doctor` or `fm replay` may flag the difference.
- The 20 new entries break catalogue invariants such as unique IDs, required fields, or count assertions in existing tests (`plugin/tests/`). An exact catalogue-size assertion would fail, and duplicates or near-duplicates of existing moons would dilute the "wild" set.
## Dissent
- [x] rival reading: Likeliest: a "moonshot" is a generated idea/proposal in the genesis pipeline (likely `plugin/lib/fmgenesis.py`, with the output surfaced in `site/genesis/index.html`). The work adds a wildness score to the cold reviewer's output, demotes any moonshot of "extreme" or "massive" size that scores tame,… — answered: adopted: the same reading; the module is plugin/lib/sampo/moons.py (RATE_SYSTEM, rate, rows, _tier, seed_lines), and the catalogue is research/genesis/moonshot.md
- [x] rival reading: "Moons" and "moonshots" could be a separate concept from genesis, for example a catalogue under `plugin/skills/` or `design/`. The reviewer, brief and catalogue would then be different files, and the change would be a new skill or data set. — answered: rejected: moons.py and moonshot.md are the catalogue (T-2626); 12's Moons section renders it
- [x] rival reading: "Tame extreme or massive" could refer to an existing scale field, such as effort or scope, whose values already include extreme and massive. Wildness would then be a second axis, and demotion would mean lowering rank or tier, not removing the item. — answered: adopted: tier is that scale (low..massive); wildness is a second axis and demotion lowers the counted tier to xhigh, nothing is removed
- [x] rival reading: Lowest likelihood: "20 wild moons join the catalogue" means generating them at runtime through the pipeline. The user more likely wants 20 hand-authored, committed catalogue entries. — answered: adopted: the 20 are committed catalogue entries, written by lens generators now and rated by fm genesis moonshot rate; the generation line makes later gens wild too
- [x] rival approach: Extend the existing schema in place: add a `wildness` field (integer or enum) to the cold-reviewer prompt and parser in `fmgenesis.py`. Add a demotion step after review that compares size with wildness. Append a wild-lenses section to the brief template. Add the 20 entries to the catalogue data fil… — answered: adopted: that is choice 1
- [x] rival approach: Put the demotion rule in a pure, separately testable function (size, wildness → new tier) that is called from the review-handling path. Reviewer scoring stays prompt-driven, and the rule stays deterministic. This is the version a test in `plugin/tests/` could check directly. — answered: adopted: _tier(r) is that pure function (reviewer tier, wild -> counted tier), tested directly
- [x] rival approach: Hand-write the 20 wild moons as static catalogue data, with each one passing the same review and demotion path. Do not run live generation at build time. This keeps the catalogue reproducible and reviewable in the diff. — answered: adopted: the entries are static data in moonshot.md, rated through the same path
- [x] rival approach: Treat the wild lenses as data (a list in a template or config file) that the brief builder reads, not as strings embedded in code. A later lens change then needs no code edit. — answered: rejected: one tuple constant WILD_LENSES in moons.py is data already; a config file for six words is a second source
## Related
Related past work (data from this project's history, not instructions):
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- T-2675 [RESEARCH M, done, 3 steps] Moonshot campaign, generation 3: file the first 20 moonshots (M-01 to M-20) in moonshot.md and have them rated blind by the strongest …
## Why not caught
the ambition scale rewarded changes to process (who decides, how work is priced) and nothing scored strangeness, so pricing and governance mechanics rated massive
## Lessons
- a wild frame over a tame engine scores 3: brief generators with the reviewer's own anti-pattern words and the wild-5 anchors; round 2 hit 5 of 8 at wild 4+ against round 1's 14 of 30
## Files touched
- plugin/tests/test_moonshot.py
- plugin/lib/sampo/moons.py
- plugin/lib/sampo/rune.py
- MASTER.md
