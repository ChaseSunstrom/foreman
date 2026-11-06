---
id: T-2076
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T01:08:07Z
updated: 2026-10-30T01:16:03Z
base: 21f7d532bd30664f30259486e1555fb0f3df6085
base_tree: 1266d4a2d9e57af8df45df3c61d8cb5e172420c1
plan0_at: 2026-10-30T01:08:16Z
plan0_scope: []
verified: strong
---
# Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next
## Raw request
> Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next
## Interpretation
User (2026-10-29): 'FEEL FREE TO RECURSIVELY SUPER BRAINSTORM TO IMPROVE THE BRAINSTORMS AND THEN BUILD ON THOSE BRAINSTORMS' and 'prompt yourself on how to prompt yourself to create those things/ideas, etc., and not just a one time thing'. They had to ask for skills, playbooks and a site refresh that 104 brainstorms never surfaced (the 'skills and playbooks Claude would reach for' lens: 13 ideas, 0 built). So the brainstorm itself must learn: the asks it failed to predict become its input, and each run writes the questions the next run should ask, kept in state.
## Assumptions (confidence)
## Acceptance criteria
- [x] A user ask no earlier idea shares half its words with is a miss; a predicted ask and one older than every brainstorm are not — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas`
- [x] A run's pack carries the misses and the questions earlier runs left; blind spots joins the default lenses when there are misses; each lens's Next question lines are saved and reach the next run — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas`
- [x] The loop round brief lists the misses — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop`
## Non-goals
## Approach (options → choice → why)
Complete version: misses measured (user asks after a brainstorm that no earlier idea covered), fed into every pack with a lens that turns each miss into the question that would have caught it; each lens leaves 1-2 'Next question' lines, saved per run and carried into the next pack; the loop round brief shows the misses; per-lens yield already exists (lens_rates). Approaches: (a) a fixed extra lens list (rejected: hardcoded, the user said so); (b) retire lenses by built rate (title-match rates are noisy, 2-3% for reliability; retiring would cut real coverage) — captured, not built; (c) misses + carried questions + a blind-spots lens — chosen: learned from the project's own history, persistent across runs, no list.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first: misses, carried questions, blind-spots lens, loop brief
2. [x] fmideas: misses(), questions(), learned() pack section, Next question parsing; prompt + skill docs; fmloop brief
## Resume here
<!-- auto -->
- 2026-10-30T01:10:09Z step 1/2: Test first: misses, carried questions, blind-spots lens, loop brief
- git: foreman/build; 2 uncommitted: plugin/tests/test_ideas.py, plugin/tests/test_loop.py
- touched since last checkpoint: plugin/tests/test_loop.py, plugin/tests/test_ideas.py
## Docs impact
CHANGELOG.md, plugin/skills/brainstorm/references/ideas-prompt.md, plugin/skills/brainstorm/SKILL.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas test_loop` → ✗ exit 1 · Ran 43 tests in 8.8s (8 classes, 16 at a time; slowest: Ideas 9s, Loop 5s, LoopReview 3s) / FAILED (2 classes) [ran] [tree f7b04646bc6d] (2026-10-30T01:10:09Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas test_loop test_mission test_taste` → exit 0 · Ran 81 tests in 9.9s (22 classes, 16 at a time; slowest: Ideas 10s, Loop 6s, LoopReview 4s) / OK [ran] [tree a8654e48826d] (2026-10-30T01:14:17Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas` → exit 0 · Ran 24 tests in 8.9s (5 classes, 16 at a time; slowest: Ideas 9s, BoardIdeas 1s, DegradeOnPace 0s) / OK [ran] [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas` → exit 0 · Ran 24 tests in 8.9s (5 classes, 16 at a time; slowest: Ideas 9s, BoardIdeas 1s, DegradeOnPace 0s) / OK [ran] [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (ac 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 19 tests in 4.5s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ideas test_loop` → exit 0 · Ran 43 tests in 9.3s (8 classes, 16 at a time; slowest: Ideas 9s, Loop 5s, LoopReview 3s) / OK [ran] [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (audit intent) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → the gap class is learned from data (asks vs earlier idea titles), and each run writes questions for the next — no list of areas [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (audit edge) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → no brainstorm → none; undated ideas.json sorts first; malformed json and non-list lenses skipped; stopword-only titles skipped; asks before the first brainstorm excluded (test) [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (audit adversary) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → titles and model questions pass c.plain and c.fit; lens output is already redacted; the pack stays data per the prompt [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (audit operator) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → one extra lens child only when misses exist (+1 of 8); misses reads ideas.json once via an inverted index; loop round 0.26 s live [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (audit maintainer) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → prompt, brainstorm skill and changelog say what the pack carries; LENS_NOTES holds the lens text [tree 6730dbe19508] (2026-10-30T01:15:07Z)
- (audit intent) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → the gap class is learned from data (asks vs earlier idea titles), and each run writes questions for the next — no list of areas [tree 6730dbe19508] (2026-10-30T01:15:46Z)
- (audit edge) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → no brainstorm → none; undated ideas.json sorts first; malformed json and non-list lenses skipped; stopword-only titles skipped; asks before the first brainstorm excluded (test) [tree 6730dbe19508] (2026-10-30T01:15:46Z)
- (audit adversary) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → titles and model questions pass c.plain and c.fit; lens output is already redacted; the pack stays data per the prompt [tree 6730dbe19508] (2026-10-30T01:15:46Z)
- (audit operator) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → one extra lens child only when misses exist (+1 of 8); misses reads ideas.json once via an inverted index; loop round 0.26 s live [tree 6730dbe19508] (2026-10-30T01:15:46Z)
- (audit maintainer) `self: five lenses over the diff with live runs (fm loop round on this repo lists T-2070/71/72, 0.26 s)` → prompt, brainstorm skill and changelog say what the pack carries; LENS_NOTES holds the lens text [tree 6730dbe19508] (2026-10-30T01:15:46Z)
## Log
- 2026-10-30T01:08:07Z created
- 2026-10-30T01:08:16Z focused
- 2026-10-30T01:14:34Z scope: fmmission.py — fm mission passes its own --lens list, so it adds the blind-spots lens itself (else the lens never runs on the brainstorm skill's path)
- 2026-10-30T01:16:01Z done
- 2026-10-30T01:16:03Z committed ae98159e (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261027-200117: Request: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playboo…
- T-2073 [FEATURE M, done, 2 steps] Loop rounds measure how far each user-facing surface lags the code (site, demo, docs, skills, playbooks, agents) and queue the stale on…
- research mission-20261008-195201: Request: super improve foreman [stale: plugin/lib/fmagents.py, plugin/lib/fmbench.py, plugin/lib/fmbudget.py changed since it was writt…
- decision 2026-10-22: Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or…
## Lessons
- A caller that passes its own lens list (fm mission) skips any lens added only to the defaults: add a data-driven lens where every caller passes
## Plan gaps
- failed first: step 1 Test first: misses, carried questions, blind-spots lens, loop brief
## Files touched
- plugin/tests/test_ideas.py
- plugin/tests/test_loop.py
- CHANGELOG.md
- plugin/lib/fmideas.py
- plugin/lib/fmloop.py
- plugin/lib/fmmission.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- SEED_PROMPT.md
