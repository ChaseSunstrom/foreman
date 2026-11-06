---
id: T-2073
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T00:55:58Z
updated: 2026-10-30T01:42:41Z
base: 5f65f80a624a66f0379cb06c7708f3105d5dc064
base_tree: dbdbec8077d6a79f6ead2a23d7b158a0e80ca48c
plan0_at: 2026-10-30T00:56:08Z
plan0_scope: []
verified: strong
---
# Loop rounds measure how far each user-facing surface lags the code (site, demo, docs, skills, playbooks, agents) and queue the stale ones unasked
## Raw request
> Loop rounds measure how far each user-facing surface lags the code (site, demo, docs, skills, playbooks, agents) and queue the stale ones unasked
## Interpretation
User (2026-10-29): "why am i still having to even say these things to you? you need to be able to figure these things out on your own ... by thinking of every single conceivable posibility". They had to ask for more playbooks, skills and a site refresh. Cause: loop rounds review only what shipped plus lenses; nothing measures which user-facing surface has fallen behind the code, so stale surfaces wait for the user.
## Assumptions (confidence)
## Acceptance criteria
- [x] A file that usually changes with recent work but didn't is listed with the updates it owes, learned from git history; a fresh history lists none; no git says unknown — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop`
- [x] The round brief names every top-level area and carries the left-behind lines — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop`
## Non-goals
## Approach (options → choice → why)
Complete version: each round says, for any repo, which files recent work would normally have brought along but didn't, plus every top-level area and every way a user meets it. Approaches: (a) a fixed list of faces with commit or topic lag — rejected by the user ('I don't mean to have foreman be hardcoded'); (b) commit-count staleness per file — noisy, every quiet file looks stale; (c) co-change drift learned from the repo's own history: P(B|A) from the last year's commits, B owes max P over each later commit's files — chosen: no list, works on any repo, explains each line. Steps rename: step 2 is fmmap.drift + fmloop.lag + the brief's Surfaces section.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first: faces lag probe and brief section
2. [x] fmloop: FACES, lag(p), brief section; MAIN_LENSES gain skills/playbooks and site/demo
## Resume here
<!-- auto -->
- 2026-10-30T01:01:17Z steps 2/2 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmloop.py, plugin/lib/fmmap.py, plugin/tests/test_loop.py
- touched since last checkpoint: CHANGELOG.md, plugin/lib/fmloop.py, plugin/lib/fmmap.py, plugin/tests/test_loop.py
## Docs impact
CHANGELOG.md entry; MASTER.md's loop line lands after T-2053's restructure (T-2074)
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 18 tests in 5.0s (3 classes, 16 at a time; slowest: Loop 5s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree f5943cd66fea] (2026-10-30T00:57:32Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 18 tests in 5.1s (3 classes, 16 at a time; slowest: Loop 5s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree f5943cd66fea] (2026-10-30T00:57:37Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 18 tests in 5.3s (3 classes, 16 at a time; slowest: Loop 5s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree a30f1d3363db] (2026-10-30T01:03:54Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop test_map` → exit 0 · Ran 26 tests in 5.7s (6 classes, 16 at a time; slowest: Loop 5s, Map 4s, LoopReview 4s) / OK [ran] [tree a30f1d3363db] (2026-10-30T01:04:00Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 18 tests in 4.1s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 1266d4a2d9e5] (2026-10-30T01:05:51Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop test_map` → exit 0 · Ran 26 tests in 4.4s (6 classes, 16 at a time; slowest: Loop 4s, Map 3s, LoopReview 3s) / OK [ran] [tree 1266d4a2d9e5] (2026-10-30T01:05:56Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 18 tests in 4.5s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_loop` → exit 0 · Ran 18 tests in 4.5s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
- (audit intent) `self-audit after the last change: ran fm loop round live on this repo (first version flagged 8 noise files driven by CHANGELOG.md's 1-5% links; fixed with a 50% share floor, now MASTER.md / plugin.json / fmlanes.py, each a real lag), earlier fm-reviewer findings (git failure read as none, hardcoded lenses, changelog blank line) all fixed` → no folder list; the repo's own history says what usually moves with what, so any repo gets it; live run names MASTER.md trailing fmcli.py, a real gap (T-2074) [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
- (audit edge) `self-audit after the last change: ran fm loop round live on this repo (first version flagged 8 noise files driven by CHANGELOG.md's 1-5% links; fixed with a 50% share floor, now MASTER.md / plugin.json / fmlanes.py, each a real lag), earlier fm-reviewer findings (git failure read as none, hardcoded lenses, changelog blank line) all fixed` → no git or no commits → None → 'unknown' line; a file in every commit (changelog hub) no longer adds weak links (regression test: old.txt at 27% over 8 commits stays out); deleted files dropped; 20+ file commits never pair [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
- (audit adversary) `self-audit after the last change: ran fm loop round live on this repo (first version flagged 8 noise files driven by CHANGELOG.md's 1-5% links; fixed with a 50% share floor, now MASTER.md / plugin.json / fmlanes.py, each a real lag), earlier fm-reviewer findings (git failure read as none, hardcoded lenses, changelog blank line) all fixed` → file names from git are repo content → c.plain + c.defang on each line and on the areas list [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
- (audit operator) `self-audit after the last change: ran fm loop round live on this repo (first version flagged 8 noise files driven by CHANGELOG.md's 1-5% links; fixed with a 50% share floor, now MASTER.md / plugin.json / fmlanes.py, each a real lag), earlier fm-reviewer findings (git failure read as none, hardcoded lenses, changelog blank line) all fixed` → one git log over 365 days, 0.25 s on this repo; runs once per round [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
- (audit maintainer) `self-audit after the last change: ran fm loop round live on this repo (first version flagged 8 noise files driven by CHANGELOG.md's 1-5% links; fixed with a 50% share floor, now MASTER.md / plugin.json / fmlanes.py, each a real lag), earlier fm-reviewer findings (git failure read as none, hardcoded lenses, changelog blank line) all fixed` → drift() sits beside _co_change in fmmap with a docstring giving the formula; re-listing a kept file each round is captured as T-2075 [tree 1266d4a2d9e5] (2026-10-30T01:06:15Z)
## Log
- 2026-10-30T00:55:58Z created
- 2026-10-30T00:56:07Z focused
- 2026-10-30T00:58:12Z scope: CHANGELOG.md for the entry
- 2026-10-30T01:03:37Z steer: user: 'I don't mean to have foreman be hardcoded to that, I want foreman to just genuinely be smarter' → replaced the face/verb list with fmmap.drift: owed updates learned from git co-change history
- 2026-10-30T01:06:10Z scope: plugin/lib/fmmap.py gains drift(): the co-change mining lives there next to _co_change
- 2026-10-30T01:06:25Z done
- 2026-10-30T01:06:28Z committed 21f7d532 (4 files)
- 2026-10-30T01:06:44Z guard authorization added: publish
- 2026-10-30T01:42:41Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-0950 [FEATURE L, done, 4 steps] fm scout: Foreman finds its own work (Claude Code updates, library gaps, doctor findings, stale sources, friction, brainstorm when dry)…
- research mission-20261028-025205: Request: Recursive brainstorm/build rounds after the weekly reset: make Foreman insanely good, not just specific to usage; reason ahead…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Lessons
- Learn what a repo's surfaces are from its own co-change history instead of listing folders; then run it live on a real repo before closing: a hub file (changelog) makes weak links sum to noise, so require the partner to move together at least half the time
## Files touched
- plugin/tests/test_loop.py
- plugin/lib/fmloop.py
- CHANGELOG.md
- plugin/lib/fmmap.py
