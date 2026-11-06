---
id: T-0147
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-03T06:41:15Z
updated: 2026-10-03T06:43:56Z
base: 6661575eae7b40670fdafae05a0b9a6e11c9f210
base_tree: c7eaf3be2a1e83271d0790eb333462c3f124b4e8
verified: strong
---
# Stop: a turn that ends on purpose for a mod reload isn't blocked by the evidence or question nudge
## Raw request
> Stop: the evidence nudge blocks a turn that is ending on purpose for a mod reload (twice: T-0145, T-0146); when a reload hand-over is pending, skip the nudge — the resumed turn records the live evidence
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a driven turn whose dev-mods changed ends for the reload even with the current step lacking evidence — verify with `python3 plugin/tests/run.py -p test_hooks.py -k Reload`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Reload 1s) / OK (start tree + this task's tests) [ran] [tree bb5325ba9be5] (2026-10-03T06:42:27Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Reload 1s) / OK [ran] [tree bb5325ba9be5] (2026-10-03T06:42:27Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → ✗ exit 1 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Reload 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 29ccf2aced37] (2026-10-03T06:42:40Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Reload 1s) / FAILED (1 classes) [ran] [tree 29ccf2aced37] (2026-10-03T06:42:40Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → ✗ exit 1 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Reload 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 453f2d8cea0e] (2026-10-03T06:43:09Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Reload 1s) / OK [ran] [tree 453f2d8cea0e] (2026-10-03T06:43:09Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Reload 1s) / OK [ran] [tree 47499cbd1057] (2026-10-03T06:43:56Z)
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Reload 1s) / OK [ran] [tree 47499cbd1057] (2026-10-03T06:43:56Z)
- (audit self) `self: the nudges are skipped only when drive is on and this session's dev-mods changed this turn (the same test _drive uses, shared via _turn_began); every other stop runs them as before; red on the start tree, green now` → no findings [tree 47499cbd1057] (2026-10-03T06:43:56Z)
## Log
- 2026-10-03T06:41:15Z created
- 2026-10-03T06:42:17Z planned from capture
- 2026-10-03T06:42:18Z focused
- 2026-10-03T06:43:56Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- T-0015 [FEATURE L, done, 5 steps] Foreman-aware conversation view: output style, richer badge and statusline, pending-approval display, live step tracking
- research t0015-operator: T-0015 operator audit: changes needed. HIGH between git pull and /reload-plugins the dialog shows but the PermissionRequest hook isn't loaded → …
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- A gate meant to catch premature 'done' must know when the turn ends for a mechanical reason
## Files touched
- plugin/tests/test_hooks.py
- CHANGELOG.md
- plugin/lib/fmhooks.py
