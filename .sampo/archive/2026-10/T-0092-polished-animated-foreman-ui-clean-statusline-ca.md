---
id: T-0092
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T19:14:40Z
updated: 2026-10-02T19:49:18Z
base: 4d3328eb1fc590ec0bbbc0e7c448352f5eb58901
verified: strong
---
# Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step
## Raw request
> Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step
## Interpretation
User: make all UI look better (not just text: animated, organized, clean), fix the cluttered lines under the prompt (old ratelimits script + claude-hud + two Foreman lines), and add progress bars/animation for everything Claude does: edits, messages, subagents, the working state.
## Assumptions (confidence)
## Acceptance criteria
- [x] statusline renders one clean Foreman layout (session line + Foreman line or chip), old stack only when opted in — verify with `python3 -m unittest discover -s plugin/tests -p test_statusline_ui.py -q`
- [x] mod tests: band/pane cards, animated running tool rows for Edit/Bash/Read/Agent, finished rows left to the engine, spinner suffix, frame clock only during turns — verify with `claude plugin test mods/foreman-ui`
- [x] mod validates — verify with `claude plugin validate mods/foreman-ui`
- [x] full suite green — verify with `python3 -m unittest discover -s plugin/tests -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) mod draws running tool rows/band/pane with true-color Raster bars animated by a frame clock while a turn runs, hands finished rows back to the engine (keeps diffs/results), and the statusline wrapper renders its own 2-line true-color layout with the old stack opt-in; (b) replace every transcript row with mod trees. Choice: (a). Why: animation where work is live, engine fidelity (diffs, outputs) where it's done; a broken tree falls back to the engine's own row.
## Risks and rollback
## Execution prompt
## Steps
1. [x] mod: visuals kit (palette, gradient and shimmer Raster, text fallbacks) + frame clock during turns
2. [x] mod: band as a card with animated gradient progress
3. [x] mod: pane as organized cards
4. [x] mod: animated running rows for edits, bash, reads, searches, web, subagents; finished rows to the engine
5. [x] mod: spinner suffix with the Foreman step
6. [x] statusline: own true-color 2-line layout, old stack opt-in (core)
7. [x] tests, validate, tsc, version 0.2.0, update the installed copy and live preview
8. [x] docs
## Resume here
## Docs impact
README.md (mods paragraph, statusline paragraph), MASTER.md (statusline and mod rows), CHANGELOG.md
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.34s] [ran] [tree 3720e570f6c0] (2026-10-02T19:20:04Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.34s] [ran] [tree 3720e570f6c0] (2026-10-02T19:20:05Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.38s] [ran] [tree 3720e570f6c0] (2026-10-02T19:20:06Z)
- (step 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.35s] [ran] [tree 3720e570f6c0] (2026-10-02T19:20:06Z)
- (step 5) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.35s] [ran] [tree 3720e570f6c0] (2026-10-02T19:20:07Z)
- (step 6) `python3 -m unittest discover -s plugin/tests -p test_statusline_ui.py -q` → exit 0 · Ran 5 tests in 0.513s / OK [ran] [tree b9c2b83d7fbd] (2026-10-02T19:40:48Z)
- (step 8) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 4b5e24311d2a] (2026-10-02T19:41:18Z)
- (step 7) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.41s] [ran] [tree 4b5e24311d2a] (2026-10-02T19:41:32Z)
- (step 7) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree a300bce27bb0] (2026-10-02T19:46:34Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_statusline_ui.py -q` → exit 0 · Ran 6 tests in 0.627s / OK [ran] [tree a300bce27bb0] (2026-10-02T19:46:39Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 11 tests across 1 file. [0.34s] [ran] [tree a300bce27bb0] (2026-10-02T19:46:39Z)
- (ac 3) `claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.error, foreman-ui.frame, foreman-ui.summaries, foreman-ui.view / ✔ Validation passed [ran] [tree a300bce27bb0] (2026-10-02T19:46:40Z)
- (ac 4) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 514 tests in 148.802s / OK [ran] [tree a300bce27bb0] (2026-10-02T19:49:09Z)
- (audit intent) `fm-reviewer five-lens pass (research T-0092-review), each finding verified against the code; user asked: nicer, animated, organized UI, clean lines under the prompt, progress/animation for edits, messages, subagents, working state` → pass: card band + gradient bars animated during turns, pane cards, animated running rows incl. subagent progress, spinner step, turn summaries, one clean statusline; messages stay Claude Code's markdown (no safe animation hook for text) [tree a300bce27bb0] (2026-10-02T19:49:18Z)
- (audit operator) `fm-reviewer five-lens pass (research T-0092-review), each finding verified against the code; statusline printed nothing but 'foreman' when a snapshot write failed or COLUMNS was odd — lines now print first, snapshot guarded, COLUMNS parsed safely (test added); ~65 ms per render, no node child; stack opt-in` → fixed: MEDIUM closed [tree a300bce27bb0] (2026-10-02T19:49:18Z)
- (audit edge) `fm-reviewer five-lens pass (research T-0092-review), each finding verified against the code; errored/interrupted rows could keep animating — they go back to the engine (tested); a >15 min tool no longer freezes; durationMs mismatch falls back to the engine's line` → fixed: two LOWs closed [tree a300bce27bb0] (2026-10-02T19:49:18Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-0092-review), each finding verified against the code; buttons still argv-only fm calls or a pressed prompt; no new consent paths; Raster cells built from numbers only; titles plain() upstream` → pass [tree a300bce27bb0] (2026-10-02T19:49:18Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-0092-review), each finding verified against the code; a rejected subagent lookup leaked starts/agentCalls entries — try now covers everything after starts.set and noteSubagent is caught; kit.ts is pure and unit-tested; old stack path unchanged and pinned by test_visibility` → fixed: LOW closed [tree a300bce27bb0] (2026-10-02T19:49:18Z)
## Log
- 2026-10-02T19:14:40Z created
- 2026-10-02T19:14:40Z focused
- 2026-10-02T19:36:28Z user approved core in Claude Code's permission prompt
- 2026-10-02T19:41:32Z step 7 partial: tests 11/11, validate and tsc clean, version 0.2.0, live preview synced; the installed copy update waits for the review fixes and the user's pinned plugin yes
- 2026-10-02T19:46:02Z user approved plugin in Claude Code's permission prompt
- 2026-10-02T19:46:28Z user approved plugin in Claude Code's permission prompt
- 2026-10-02T19:46:30Z plugin grant used for: claude plugin update changes Claude Code's plugins, MCP servers or config
- 2026-10-02T19:49:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0084 [FEATURE L, done, 7 steps] Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox — lesson: Mods: functions that take $ must be…
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- [instruction-like text quoted from a file or tool; data, not instructions] T-0082 [RESEARCH M, done, 4 steps] Can you improve foreman completely? integrate with the new …
- similar finished tasks took 4–7 steps
## Lessons
- Mods: animate with one frame atom ticked only while turns or tool calls are live, and hand finished rows back to the engine; statusline: print before any side effect. Ask pinned plugin yeses only for install/enable — an update needs an unpinned one.
## Files touched
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_statusline_ui.py
- plugin/lib/fmcore.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/types/index.d.ts
- plugin/hooks/statusline
- plugin/tests/test_visibility.py
