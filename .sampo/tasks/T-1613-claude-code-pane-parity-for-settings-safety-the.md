---
id: T-1613
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:54:21Z
updated: 2026-10-23T12:03:18Z
group: pane safety and width
base: 1b096483945971ed8bde9f5cc2839feaba1faabf
base_tree: 64bbe520a430bfe194ab610a591582d0aba9ee48
plan0_at: 2026-10-23T12:01:49Z
plan0_scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: strong
---
# Claude Code pane parity for settings safety: the foreman-ui pane boots its last good setti
## Raw request
> Claude Code pane parity for settings safety: the foreman-ui pane boots its last good settings and merges outside edits like the fm code app (follow-up of T-1543)
## Interpretation
Parity with the fm code app's settings safety (T-1543) for the foreman-ui pane: an option set to a value the pane can't use keeps its last good value (not the default), is said once as a toast, and the last good values are kept in the mod's store so a restarted pane starts with them. Outside edits already apply live (T-1574).
## Assumptions (confidence)
## Acceptance criteria
- [x] an unusable option keeps its last good value with one toast; a restarted pane reads the last good values from its store, checked — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (1) one usable() pass over the options: each value checked by a per-option rule, a bad one replaced by the last good value, the kept names returned for one toast (chosen: the rules applyOptions already encodes, in one table); (2) refuse the whole set when one is bad, as the app does for a file (rejected: options are independent, unlike one tui.toml); (3) validate in fm settings set only (rejected: /config and hand edits bypass it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] usable() and the last good store, test first
## Resume here
## Docs impact
CHANGELOG line; the pane's options keep their descriptions in the plugin manifest; no doc names the old fall-back-to-default behaviour.
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 13 tests across 4 files. [0.92s] [ran] [tree 5ab3a22c13cd] (2026-10-23T12:01:56Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 148 tests across 4 files. [11.65s] [ran] [tree 5a15c99cbacf] (2026-10-23T12:02:14Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 148 tests across 4 files. [11.72s] [ran] [tree 5a15c99cbacf] (2026-10-23T12:02:37Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 148 tests across 4 files. [11.63s] [ran] [tree 5a15c99cbacf] (2026-10-23T12:02:50Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): one table of per-option rules replaces nothing in applyOptions (it still defaults a missing option); usable() runs before it on each poll and at session start; the store copy is checked by the same rules when read` → a typo in an option keeps the pane as it was and says so once; a restarted pane takes the last good values, like fm code's last good tui.toml [tree 5a15c99cbacf] (2026-10-23T12:02:50Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): one table of per-option rules replaces nothing in applyOptions (it still defaults a missing option); usable() runs before it on each poll and at session start; the store copy is checked by the same rules when read` → a removed option goes back to its default (not the last good: removing is a choice); the same bad value is said once, not every poll; a damaged store entry is checked like any value; an engine without the store or toast loses only the memory, not the pane [tree 5a15c99cbacf] (2026-10-23T12:02:50Z)
## Log
- 2026-10-22T20:54:21Z created
- 2026-10-23T11:44:59Z set tier=M, scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md']
- 2026-10-23T12:01:48Z focused
- 2026-10-23T12:03:17Z done
- 2026-10-23T12:03:18Z committed 71fadccc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1543 [FEATURE M, done, 4 steps] Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren — lesson: A file watcher must stat before it…
- research T-1543-review: Verdict: approve with nits.** The three-part acceptance criterion is met. I could not run the tests, because I had no shell in this audit. The ta…
- research T-1574-review: Verdict: changes needed.** One MEDIUM bypass of the guard (in code from T-1496, which the new command calls through) and one MEDIUM test gap. I c…
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx; re-ground the plan against them before editing
## Lessons
- Parity with a whole-file last-good scheme, for independent options, is per option: keep each good value, refuse each bad one
## Plan gaps
- failed first: step 1 usable() and the last good store, test first
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- mods/foreman-ui/hooks/register.tsx
