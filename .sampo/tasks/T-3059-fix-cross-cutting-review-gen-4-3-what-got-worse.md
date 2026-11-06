---
id: T-3059
type: FIX
tier: S
status: done
priority: low
scope: [plugin/tests/test_site_build.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:08Z
updated: 2026-11-06T13:50:19Z
trigger: genesis-review
trigger_key: 58187438a6e7bdb0
base: 44ae7c50fa7078373e6d0c7457f373c30f9436db
base_tree: a9cc86cf443cd0734d2eb53127373b1121f91fb7
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:46:38Z
plan0_scope: [plugin/tests/test_site_build.py]
builder_returned: 2026-11-06T12:50:15Z
lane_stop: merged 2026-11-06T13:26:16Z
verified: strong
unproven: [meaning]
---
# The site build test proves the published share image is a real PNG, not a symlink the deploy might not follow
## Raw request
> FIX: cross-cutting review gen-4 #3 (what got worse): site/assets/share.png shrank from a real image to 33 bytes (a symlink); the share card published by Pages now depends on the deploy dereferencing it, and no shipped check proves it does. [Bin 226340 -> 33 bytes]
> genesis-review 4:3
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_site_build builds the site into a temp dir and checks assets/share.png there is a regular file (not a symlink) over 10 KB starting with the PNG signature; checked live 2026-11-05: the Pages copy is 204,666 bytes, so this pins what works — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the test (green on today's build; red if build.py copied the link itself)
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_build.Reproducible` → exit 0 · Ran 1 tests in 11.6s (1 jobs, 16 at a time; slowest: Reproducible 1s) / OK [ran] [tree f6b60cf68dad] [world 2f1906870a] (2026-11-06T12:47:05Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_site_build && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [27.05s] [ran] [tree f6b60cf68dad] [world 2f1906870a] (2026-11-06T12:50:02Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 905bf469abae] (2026-11-06T13:26:20Z)
- `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 28 tests in 49.7s (13 jobs, 16 at a time; slowest: CardsPage 12s, Landing 3s, Reproducible 1s) / OK (start tree + this task's tests) [ran] [tree 905bf469abae] [world 2f1906870a] (2026-11-06T13:28:23Z)
- `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 28 tests in 68.9s (13 jobs, 16 at a time; slowest: CardsPage 14s, Landing 2s, Reproducible 1s) / OK [ran] [tree 905bf469abae] [world 2f1906870a] (2026-11-06T13:28:23Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 905bf469abae] (2026-11-06T13:49:23Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T13:28:23Z [ran] [tree 905bf469abae] [world 2f1906870a] (2026-11-06T13:49:29Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 905bf469abae] (2026-11-06T13:49:29Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 905bf469abae] (2026-11-06T13:49:29Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 905bf469abae] (2026-11-06T13:49:29Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 905bf469abae] (2026-11-06T13:49:29Z)
## Log
- 2026-11-05T00:31:08Z created
- 2026-11-05T04:09:53Z planned from capture
- 2026-11-05T04:09:54Z set approved=True
- 2026-11-05T04:09:54Z set scope=['plugin/tests/test_site_build.py']
- 2026-11-05T04:09:55Z blocked: approved; waits for a builder slot (or the main thread between closes)
- 2026-11-06T03:53:44Z unblocked
- 2026-11-06T12:46:36Z focused
- 2026-11-06T12:46:38Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T13:26:16Z merged worktree-agent-a086c248540628331 (1 file(s))
- 2026-11-06T13:26:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a086c248540628331
- 2026-11-06T13:26:16Z focused
- 2026-11-06T13:26:20Z set scope=['plugin/tests/test_site_build.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T13:26:20Z scope: widened at merge to the reviewed lane's own diff (c9e81561b), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T13:49:20Z focused
- 2026-11-06T13:50:15Z done
- 2026-11-06T13:50:19Z committed fe5138e95 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3133 [FIX M, planned, 6 steps] Batch: FIX: cross-cutting review gen-4 #5 (wha…; FIX: cross-cutting review gen-4 #12 (wh…; FIX: cross-cutting review ge…
- T-3058 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-4 #2 (what got worse): Failed tool calls per 100 doubled…
- T-3060 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-4 #4 (what got worse): The repeat-failure firewall itself…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-05): .sampo/README.md, .sampo/archive/2026-09/T-0001-phase-3-hooks-one-dispatcher-per-event-guard-sto.md, .sampo/archive/2026-09/T-0002-phase-4-skills-rules-agents-visibility-layer-por.md, .sampo/archive/…; re-ground the plan against them before editing
## Regression test
none: the lane changes only tests (a guard that pins today's behaviour so a later change can't regress it); there was no failing behaviour to turn green, and its tests pass on the merged tree
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_site_build.py
- CHANGELOG.md
