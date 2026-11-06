---
id: T-1855
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T18:25:53Z
updated: 2026-10-28T19:42:37Z
base: 791bf4490014fb9bd94d63181d6dd06663192738
base_tree: ca02aa8e415ed71ec6b91812e5dbaaf49c8baab0
plan0_at: 2026-10-28T19:36:55Z
plan0_scope: []
verified: strong
---
# fm scene: a flag the action doesn't read exits 2 naming the actions that do
## Raw request
> fm scene metaballs --days N` accepts and ignores `--days` without a note (`fmscene.py:1394-1395`)
> (noticed by an agent; research T-1849-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] metaballs --days, terrain --balls, compile --size each exit 2 naming the owning actions; owned flags still work — verify with `python3 plugin/tests/run.py test_scene`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] flag-owner table checked against fmcli._ARGV at cmd_scene's top, test first
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 46 tests in 4.7s (13 classes, 16 at a time; slowest: Soak 4s, Import 3s, Metaballs 2s) / OK [ran] [tree 5412ab408634] (2026-10-28T19:37:31Z)
- `python3 plugin/tests/run.py test_scene` → ✗ exit 1 · Ran 46 tests in 6.4s (13 classes, 16 at a time; slowest: Soak 5s, Import 3s, Metaballs 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5412ab408634] (2026-10-28T19:38:04Z)
- `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 46 tests in 5.2s (13 classes, 16 at a time; slowest: Soak 5s, Import 3s, Metaballs 3s) / OK [ran] [tree 5412ab408634] (2026-10-28T19:38:04Z)
- (ac 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 46 tests in 4.7s (13 classes, 16 at a time; slowest: Soak 4s, Import 2s, Metaballs 1s) / OK [ran] [tree 5412ab408634] (2026-10-28T19:42:34Z)
- (audit intent) `self-review of the diff; proved red on the start tree, green now; fm check exit 0, 3993 tests` → metaballs --days, terrain --balls=3, compile --size exit 2 naming the actions that read them; owned flags unchanged (scene tests green) [tree 5412ab408634] (2026-10-28T19:42:34Z)
- (audit edge) `self-review of the diff; proved red on the start tree, green now; fm check exit 0, 3993 tests` → --flag=value split on =; --out left to every action; with no _ARGV (a direct call) nothing is refused [tree 5412ab408634] (2026-10-28T19:42:34Z)
- (audit self) `self-review of the diff; proved red on the start tree, green now; fm check exit 0, 3993 tests` → no findings [tree 5412ab408634] (2026-10-28T19:42:34Z)
## Log
- 2026-10-28T18:25:53Z created
- 2026-10-28T19:18:11Z plan: root cause is every scene flag, not just --days: one table in cmd_scene (flag -> actions that read it), checked against fmcli._ARGV (allow_abbrev is off, so exact flags); a flag the action doesn't read exits 2 naming who reads it. Test via self.fm: metaballs --days 5, terrain --balls 3, compile --size 2x2 -> 2.
- 2026-10-28T19:32:45Z flag owners confirmed from cmd_scene reads: metaballs balls/grid/seed; lookbook count; terrain,airlock days; compile hud/to/tag; turntable frames; cells cols/turn; soak seconds/budget-ms; shade size/time/set. Check fmcli._ARGV at cmd_scene top, exit 2 naming owners.
- 2026-10-28T19:36:40Z set type=FIX, tier=S, title=fm scene: a flag the action doesn't read exits 2 naming the actions that do
- 2026-10-28T19:36:54Z focused
- 2026-10-28T19:42:36Z done
- 2026-10-28T19:42:37Z committed 992b2839 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1849-review: Verdict:** approve with nits. I found no defects in the feature itself. The data sources, validation, name handling and layout all hold up. I did…
- T-1848 [FEATURE M, done, 2 steps] 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655) — lesson: Before the gates, run fm check playbooks …
- research T-1848-review: Verdict: changes needed.** The geometry is correct. One regression in the CLI error path should be fixed before this lands. I ran nothing; everyt…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Lessons
- a silently ignored flag is fixed once at the dispatcher with a flag-to-reader table, not per action
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmscene.py
- CHANGELOG.md
