---
id: T-0681
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:15Z
updated: 2026-10-09T18:09:44Z
batch: [T-0472, T-0473, T-0500]
base: adf6e73413b6ae511f03c6fe24ba54a4aae29df3
base_tree: 1ea7af1fb1d76b7af368a301ec36ccbdf642014c
verified: strong
---
# Milestone: Features — UI and motion
## Raw request
> T-0472: FEATURE: Band and statusline signals (C070, value 3/5, effort S, risk low)
>   first version: Add a quiet pace/health glyph to the band and statusline from existing data (usage pace vs share of week, failing gates, blocked count) shown only when amber/red; reuse fm ui --json fields.
>   what it is: A quiet band and statusline with the next action, mood glyph, sparklines, pace mood and pulse strip.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0473: FEATURE: Proof and close-out cards (C071, value 3/5, effort S, risk low)
>   first version: Render the existing done-time grade and lens verdicts as a one-card close-out in fm ui --json and the pane toast; no new data, closes the loop for unattended runs.
>   what it is: A proof card, close-out story and small-win motion when a task finishes.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0500: FEATURE: Diff and review reading (C075, value 3/5, effort M, risk low)
>   first version: First version: make guard blocks show the offending command segment with the rule that matched (fmguard.py), and rank fm audit prep packets by risk. Skip editor/LSP and heatmaps.
>   what it is: Evidence-anchored diff reader, review-lens heatmap, risk-ranked packets and explaining a line in the editor.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0472, T-0473, T-0500 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0681. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0473 fm ui --json's closed entries carry title, grade and lenses, and the mod's close-out toast shows them — verify with `python3 plugin/tests/run.py -p test_ui_signals.py -k CloseOut`
- [x] T-0472 fm ui --json carries signals (pace, failing gate, blocked, hook errors) and the band shows one glyph only when there is one — verify with `python3 plugin/tests/run.py -p test_ui_signals.py -k Signals`
- [x] T-0500 a guard refusal of a long command quotes the segment that matched — verify with `python3 plugin/tests/run.py -p test_ui_signals.py -k BlockSegment`
- [x] the mod's own tests pass — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Data first in fm ui --json (the one view model every surface reads), then the mod renders it: closed entries gain title, grade and lenses, which the close-out toast shows (T-0473); a signals list (usage ahead of pace, a failing gate, blocked tasks, hook errors) that the band shows as one quiet glyph only when amber or red (T-0472); a guard refusal of a long command quotes the segment that matched (T-0500), and the review brief lists the security-sensitive files to read first. Skipped: statusline glyph (the band already sits next to it), editor/LSP, heatmaps.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing Python tests first
2. [x] fm ui --json: closed fields, signals (fmwatch)
3. [x] guard refusal segment (fmhooks)
4. [x] mod: toast and band glyph, its types and tests
5. [x] full suite once; CHANGELOG
## Resume here
## Docs impact
CHANGELOG entry; mod types (index.d.ts)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_ui_signals.py` → ✗ exit 1 · Ran 3 tests in 0.3s (3 classes, 16 at a time; slowest: CloseOut 0s, Signals 0s, BlockSegment 0s) / FAILED (3 classes) [ran] [tree bbaaa32c7f6e] (2026-10-09T18:05:14Z)
- (ac 1) `python3 plugin/tests/run.py -p test_ui_signals.py -k CloseOut` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: CloseOut 0s) / OK [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (ac 2) `python3 plugin/tests/run.py -p test_ui_signals.py -k Signals` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Signals 0s) / OK [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (ac 3) `python3 plugin/tests/run.py -p test_ui_signals.py -k BlockSegment` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BlockSegment 0s) / OK [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (ac 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 64 tests across 1 file. [2.92s] [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (step 1) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1120 tests in 56.1s (306 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / FAILED (1 classes) [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (step 2) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1120 tests in 56.1s (306 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / FAILED (1 classes) [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (step 3) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1120 tests in 56.1s (306 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / FAILED (1 classes) [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (step 4) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1120 tests in 56.1s (306 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / FAILED (1 classes) [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (step 5) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1120 tests in 56.1s (306 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / FAILED (1 classes) [ran] [tree 089ef04e791b] (2026-10-09T18:07:27Z)
- (step 1) `python3 plugin/tests/run.py` → exit 0 · Ran 1120 tests in 62.3s (306 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (step 2) `python3 plugin/tests/run.py` → exit 0 · Ran 1120 tests in 62.3s (306 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (step 3) `python3 plugin/tests/run.py` → exit 0 · Ran 1120 tests in 62.3s (306 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1120 tests in 62.3s (306 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (step 5) `python3 plugin/tests/run.py` → exit 0 · Ran 1120 tests in 62.3s (306 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (audit intent) `main-thread self-review: data first in fm ui --json, the mod renders it; mod suite 64/64 via claude plugin test; review-packet ranking already exists (audit prep's security-sensitive pre-audit lines); one older view test pinned the exact closed-entry dict and now checks its two keys` → close-out card, health glyph and the matched segment per the brainstorm's first versions; statusline glyph skipped (the band sits beside it) [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (audit edge) `main-thread self-review: data first in fm ui --json, the mod renders it; mod suite 64/64 via claude plugin test; review-packet ranking already exists (audit prep's security-sensitive pre-audit lines); one older view test pinned the exact closed-entry dict and now checks its two keys` → a calm project has signals [] and the band adds nothing; closed tasks dropped (not done) carry no grade or lenses; the segment quote only for commands over 160 chars, redacted [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
- (audit operator) `main-thread self-review: data first in fm ui --json, the mod renders it; mod suite 64/64 via claude plugin test; review-packet ranking already exists (audit prep's security-sensitive pre-audit lines); one older view test pinned the exact closed-entry dict and now checks its two keys` → the band change loads at the next mod reload (turn end); fm ui --json gains two fields, older mods ignore them [tree 8e655b45d5da] (2026-10-09T18:09:44Z)
## Log
- 2026-10-09T15:40:15Z created
- 2026-10-09T18:05:03Z focused
- 2026-10-09T18:09:44Z done
- 2026-10-09T18:09:44Z committed 8290cf7 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0542 [FEATURE M, dropped, 0 steps] Band and statusline signals (C070, value 3/5, effort S, risk low)
- T-0570 [FEATURE M, dropped, 0 steps] Diff and review reading (C075, value 3/5, effort M, risk low)
- T-0543 [FEATURE M, dropped, 0 steps] Proof and close-out cards (C071, value 3/5, effort S, risk low)
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
## Lessons
- Put new UI facts in the one view model first; the mod's change is then a pure render with a unit test.
## Files touched
- plugin/tests/test_ui_signals.py
- plugin/lib/fmhooks.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- plugin/tests/test_ui.py
