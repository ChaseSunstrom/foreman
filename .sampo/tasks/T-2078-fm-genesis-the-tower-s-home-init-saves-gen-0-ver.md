---
id: T-2078
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2077]
source: followup
created: 2026-10-30T01:21:16Z
updated: 2026-10-30T01:31:19Z
base: ae98159ea4c1e10fbd41926aca9bb2624cd1be06
base_tree: 6730dbe195084ccf45ac3bda08617bf3f71cc87b
plan0_at: 2026-10-30T01:21:37Z
plan0_scope: []
verified: strong
---
# fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the tower
## Raw request
> fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the tower
## Interpretation
Genesis §0/§3 need research/genesis/ (gen-0.md never edited, gen-N/seed.md, mission-*.md, critique-*.md, gap-map.md, lineage.md, exam.jsonl) in the project state dir, which only fm may write; fm research add takes flat names and defangs text, so gen-0 can't be verbatim. This is the first slice of capability #13 (fm genesis); later slices write gen-0 from one line and run the tower.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis init --file F saves research/genesis/gen-0.md byte-identical and read-only, and refuses a second init — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- [x] fm genesis put gen-1/seed.md --file F files it; a path outside the tower shape or gen-0.md is refused — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- [x] fm genesis (status) lists gen-0, the gap map, each generation's seed/missions/critiques and the exam line count — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: (1) nested names in fm research add — mixes concerns, defang breaks verbatim; (2) new fmgenesis module, fm genesis init/put/status — the verb #13 needs anyway; (3) tower docs in the git repo — state belongs per project, and other projects' towers must not land in their repos. Choice: (2), smallest: init refuses to overwrite and makes gen-0 read-only; put accepts only tower-shaped paths (gap-map.md, lineage.md, exam.jsonl, gen-N/{seed,mission-x,critique-x}.md) and refuses gen-0; status lists generations, missions and exam lines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_genesis.py
2. [x] fmgenesis.py + fmcli registration
3. [x] docs: MASTER.md, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-30T01:27:53Z steps 3/3 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- touched since last checkpoint: plugin/tests/test_genesis.py, plugin/lib/fmgenesis.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/gap-map.md, plugin/lib/fmcli.py
- failures met: watching 0 on main, up to 0 polls
## Docs impact
~/.claude/foreman/CHANGELOG.md,~/.claude/foreman/MASTER.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → red as expected (exit 1) · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: Genesis 0s) / FAILED (1 classes) [ran] [tree 72c74326d7f9] (2026-10-30T01:23:54Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_help test_cli test_which` → exit 0 · Ran 161 tests in 22.0s (45 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 10s, CaptureAndIntake 10s) / OK [ran] [tree 4958f60d08b2] (2026-10-30T01:27:08Z)
- (step 3) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 4958f60d08b2] (2026-10-30T01:27:14Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -4` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Genesis 2s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:29:57Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -4` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Genesis 2s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:29:57Z)
- (ac 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -4` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Genesis 2s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:29:57Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_help test_cli test_which` → exit 0 · Ran 162 tests in 22.0s (45 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 11s, CaptureAndIntake 10s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:30:34Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Genesis 2s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Genesis 2s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (ac 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Genesis 2s) / OK [ran] [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (audit intent) `one fm-reviewer pass over five lenses (research T-2078-review); 4 findings confirmed and fixed test-first, LockTimeout finding dismissed (fmcli.py:2236 formats it)` → met; the secret refusal now names what matched, put reports what it redacted [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (audit adversary) `one fm-reviewer pass over five lenses (research T-2078-review); 4 findings confirmed and fixed test-first, LockTimeout finding dismissed (fmcli.py:2236 formats it)` → fixed the init race (exists check now inside the lock); put's fullmatch shape blocks traversal and gen-0 [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (audit edge) `one fm-reviewer pass over five lenses (research T-2078-review); 4 findings confirmed and fixed test-first, LockTimeout finding dismissed (fmcli.py:2236 formats it)` → non-UTF-8 gen-0 kept byte for byte; missing --file is a usage error (tested) [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (audit operator) `one fm-reviewer pass over five lenses (research T-2078-review); 4 findings confirmed and fixed test-first, LockTimeout finding dismissed (fmcli.py:2236 formats it)` → one listdir per status; no hook or injected context [tree 986026a4dba1] (2026-10-30T01:30:44Z)
- (audit maintainer) `one fm-reviewer pass over five lenses (research T-2078-review); 4 findings confirmed and fixed test-first, LockTimeout finding dismissed (fmcli.py:2236 formats it)` → failure-path test added [tree 986026a4dba1] (2026-10-30T01:30:44Z)
## Log
- 2026-10-30T01:21:16Z created
- 2026-10-30T01:21:36Z set approved=True
- 2026-10-30T01:21:36Z focused
- 2026-10-30T01:31:16Z done
- 2026-10-30T01:31:19Z committed aafc340d (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261029-104513: Request: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways [stale: de…
- research mission-20261022-172631: Request: I also know there arent a lot of skills with foreman? and they are also hardly used? why? super improve!!! [stale: demo/live.m…
- research mission-20261028-175912: Request: forever loop round 5: improve past everything shipped [stale: demo/live.mp4, demo/live.svg, plugin/lib/fmcost.py changed since…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- A write-once file needs its exists check inside the lock: os.replace overwrites a read-only file when its directory is writable
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
