---
id: T-2675
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T21:36:08Z
updated: 2026-11-02T21:48:08Z
base: 525eb957f7a83d340ffcaddd783bef503030a831
base_tree: 3f668e7c8b003d3c85ac119426453cb60e2015f4
plan0_at: 2026-11-02T21:36:18Z
plan0_scope: []
paused_tree: e4df593efc7ef43dfdeb169144b3b2501d9bbb31
verified: strong
unproven: [docs, research-uncited]
---
# Moonshot campaign, generation 3: file the first 20 moonshots (M-01 to M-20) in moonshot.md and have them rated blind by the strongest model
## Raw request
> Moonshot campaign, generation 3: file the first 20 moonshots (M-01 to M-20) in moonshot.md and have them rated blind by the strongest model
## Interpretation
1. (chosen) MOONSHOT.md part A's campaign starts in generation 3 (the user's steer: integrate it into each generation): the first batch of 20 on a top-weighted slice of the mix, rated blind, with one extreme or massive kill test for the floor.
2. All 100 at once. Rejected: the campaign grows across generations, each with its own far-domain lens.
## Assumptions (confidence)
## Acceptance criteria
- [x] moonshot.md holds M-01 to M-20, fm genesis moonshot rate has rated each, and fm genesis check reports no moonshot problem — verify with `fm genesis moonshot status`
## Non-goals
## Approach (options → choice → why)
1. Put the curated catalogue, run fm genesis moonshot rate, then choose the cheapest big kill test. Likely outcome: some tiers demoted, one kill test chosen. Fails if: fm genesis check finds a duplicate of built or queued work (the curator excluded nine).
2. use what exists: rate later in the moonshot Mission. Fails if: the floor needs a rated extreme or massive moonshot advanced this generation.
3. do less: file 10. Fails if: the mix needs the big tiers, and 10 can't hold 5 of each.
Choice 1 (85%): the checker and the rater already exist; this is their first real input.
## Risks and rollback
## Execution prompt
## Steps
1. [x] file the catalogue (fm genesis put moonshot.md)
2. [x] fm genesis moonshot rate, then read the moves between author and reviewer tiers
3. [x] pick the cheapest extreme or massive kill test for this generation's floor
## Resume here
## Docs impact
none: the catalogue is Foreman state in the Genesis tower, not a repo doc
## Verification evidence
- (step 1) `fm genesis moonshot rate > /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/rate.txt 2>&1` → exit 0 · (no output) [ran] [tree 3f668e7c8b00] [world 2f1906870a] (2026-11-02T21:37:09Z)
- (step 1) `test -s state/projects/foreman-4a056f/research/genesis/moonshot.md` → exit 0 · (no output) [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:41:41Z)
- (step 2) `fm genesis moonshot status` → exit 0 · - Floor: advance at least one extreme or massive moonshot by a stage and write 'Advanced: M-NN <stage> (T-NNNN)' in gen-3/mission-moonshot.md; fm genesis check holds it once gen-4 exists. Every built [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:41:42Z)
- (step 3) `fm genesis moonshot order` → exit 0 · M-14 full (high): Breed lane strategies by tournament, with heritable genomes / M-19 full (medium): Hold every self-promotion to a false-discovery bar [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:41:43Z)
- (ac 1) `fm genesis moonshot status` → exit 0 · - Floor: advance at least one extreme or massive moonshot by a stage and write 'Advanced: M-NN <stage> (T-NNNN)' in gen-3/mission-moonshot.md; fm genesis check holds it once gen-4 exists. Every built [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:41:43Z)
- (ac 1) `fm genesis moonshot status` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T21:41:43Z [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:41:45Z)
- (audit intent) `self: the catalogue passed fm genesis put's cold read after one kill test was made local; the rater (fable, blind to the author tiers) left 4 big and demoted 13` → MOONSHOT part A's first batch, rated by a cold reviewer on the strongest model with the author tier kept beside it [tree 25470459a4ab] (2026-11-02T21:41:45Z)
- (audit edge) `self: the catalogue passed fm genesis put's cold read after one kill test was made local; the rater (fable, blind to the author tiers) left 4 big and demoted 13` → 20 of 100 on the author's mix; the reviewer's mix is lower, which the next batch must make up at the top [tree 25470459a4ab] (2026-11-02T21:41:45Z)
- (audit intent) `self: the catalogue passed fm genesis put's cold read after one kill test was made local; the rater (fable, blind to the author tiers) left 4 big and demoted 13` → MOONSHOT part A's first batch, rated by a cold reviewer on the strongest model with the author tier kept beside it [tree 25470459a4ab] (2026-11-02T21:43:57Z)
- (audit edge) `self: the catalogue passed fm genesis put's cold read after one kill test was made local; the rater (fable, blind to the author tiers) left 4 big and demoted 13` → 20 of 100 on the author's mix; the reviewer's mix is lower, which the next batch must make up at the top [tree 25470459a4ab] (2026-11-02T21:43:57Z)
- (audit intent) `self: the catalogue passed fm genesis put's cold read after one kill test was made local; the rater (fable, blind to the author tiers) left 4 big and demoted 13` → MOONSHOT part A's first batch, rated by a cold reviewer on the strongest model with the author tier kept beside it [tree 25470459a4ab] (2026-11-02T21:46:05Z)
- (audit edge) `self: the catalogue passed fm genesis put's cold read after one kill test was made local; the rater (fable, blind to the author tiers) left 4 big and demoted 13` → 20 of 100 on the author's mix; the reviewer's mix is lower, which the next batch must make up at the top [tree 25470459a4ab] (2026-11-02T21:46:05Z)
## Log
- 2026-11-02T21:36:08Z created
- 2026-11-02T21:36:17Z focused
- 2026-11-02T21:38:25Z paused: focus moved to T-2672
- 2026-11-02T21:48:08Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part A] [check: pending T-2626] Standing rule (MOONSHOT.md part A): the moonshot campaign is que…
- research T-2626-review: Verdict: changes needed.** The floor can be met by a typed line plus any finished task, and it is only enforced after the generation has already …
## Decision
Recommendation: the floor's kill test this generation is M-02's (rebuild three deleted spec-suite modules from their specs and tests alone, two attempts each), the cheapest of the four moonshots still extreme or massive after the blind rating (M-01, M-02, M-03 massive; M-06 extreme). The rater demoted 13 of 20 and promoted none: the author's tiers ran high. Would change if: the spec-suite has no three modules with their own tests, in which case M-06's ledger backtest goes first.
## Lessons
- The author tiers ran high (13 of 20 demoted, none promoted): a curator should hold its massive picks to the 'news to harness builders' test before rating, not after
## Files touched
- plugin/lib/fmideas.py
- plugin/skills/brainstorm/SKILL.md
- plugin/tests/test_brainstorm_skill.py
- plugin/tests/test_ideas.py
