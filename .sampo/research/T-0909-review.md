**Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I could not run the tests, so the other criteria are judged from the code only.

## intent: changes needed
**MEDIUM — `plugin/lib/fmwatch.py:348,375-377` — done_days reads only the last 5000 ledger events**
- `events = c.ledger_tail(p, 5000)` is reused for the 14-day window.
- Reproducer: `~/.claude/foreman/state/projects/foreman-4a056f/ledger.jsonl` has 12993 lines. Line 7994, the start of the last 5000, is dated 2026-10-09T16:15Z. Today is 10-15, so the window is 10-02 to 10-15.
- About 7 of the 14 bars are therefore 0 or understated, while the label says "N closed · 14d". The new test uses 5 events, so it can't catch this.
- Fix: scan for `task_done` over the whole file, or use `ledger_tail(p, 20000)` as `fmcost.py:336` does.
- file: `plugin/lib/fmwatch.py`, line: 348. summary: the 14-day bars use a 5000-event tail that spans about 6 days here. short_summary: done_days window truncated by ledger tail. failure_scenario: busy project, closes older than the tail are missing, so the chart shows zeros for real work. category: data-truncation. verdict: CONFIRMED.

**MEDIUM — `register.tsx:1195-1295` (new render order) vs criterion 3**
- Criterion 3 says "hero first, needs-you next". The code puts `card-asks` and the plan approvals above `fm-pane-head`, and the new test asserts `['card-asks','fm-pane-head',…]`.
- The urgency-first order is defensible, but it contradicts the criterion as written and no decision records the change.
- Fix: swap the order, or record the deviation with `fm decide` and correct the criterion.
- Criterion 3 also asks for idle and active screenshots. The diff has none.

**LOW — the size legend was deleted and its test inverted.** Nobody asked for that.

**LOW — `lanes()` text twin, `rows.tsx` (sparkText).** `sparkText(r.slots, width)` slices the last `width` of `2*width` slots, so desktop and mobile show only the newest half of a window headed "last 30 min".

## adversary: ok
Every string rendered here comes from fm's own JSON (title, verify, blockers, target); the pane puts them in `Text` and truncates, nothing reaches a shell. The new `ticks` and `running` state is bounded. No findings.

## edge: changes needed
**MEDIUM — `register.tsx:357-382` — the motion clock is not stopped by `sleep()` (~line 397)**
- `motionClock` is cancelled only in `repaint` when `turns` and `starts` are both empty. `sleep()` cancels only `clock`.
- Scenario: a turn's `turn.complete` is lost, so `turns.size > 0`. After 15 minutes `advance` stops the frame clock via the `IDLE_FRAMES` rule. The 33 ms repaint timer keeps blitting forever. Its animation is driven by `clock.now()`, so the rail comet keeps moving and the pane reads as busy.
- Fix: cancel `motionClock` in `sleep()`, and guard `repaint` against overlapping ticks.
- file: `mods/foreman-ui/hooks/register.tsx`, line: 382. summary: the 30 fps blit timer outlives the idle-sleep guard. short_summary: motionClock survives sleep(). failure_scenario: lost turn.complete leaves `turns` non-empty, so the pane animates indefinitely at 30 Hz. category: resource-leak. verdict: PLAUSIBLE.

**LOW — `fmwatch.py:376`**
- `done_days` does not intersect with `done_ids`, but `today_done` (line 373) does.
- A task that has a `task_done` event but is no longer `done` (reopened or deleted) counts in the last bar and not in "✓ N today".

**LOW — `register.tsx` (the `AskUserQuestion` face, `nowCalls`)**
- A question waiting on the person shows under "Now · 1 running" with a moving bar, and `laneOf` counts it as a `read` tick.
- That is the opposite of the intent in the new comment "it isn't work running".

## operator: changes needed
**LOW — `CHANGELOG.md` "Unreleased" (line 3) has no T-0909 entry.**
- This is the pre-audit hint for `kit.ts`, `register.tsx`, the tests, `index.d.ts`, `fmwatch.py` and `test_ui.py`: the code needs no edit, but the changelog does.
- Add the `done_days` field to `fm ui --json`, the new pane order, and the removed size legend.

## maintainer: ok with nits
- **LOW — `register.tsx:9`.** `SIZE_LEGEND` is now an unused import.
- **LOW — tests.** The 30 fps `repaint` and `$.ui.blit` path, which is the "animations" part of the request, has no test. Neither do the non-terminal twins of `rail`, `lanes`, `bars` and `eta`.
- **LOW — `register.tsx:232`.** The `flashed` map is never pruned. It is tiny.

## Acceptance criteria
- **Mod tests pass, new kit charts included:** not verifiable here. The new kit tests' arithmetic checks out by hand (`nodeAt`, `bucketize`, `etaCells`).
- **`fm ui --json` carries `done_days` (14 counts):** met in shape (`fmwatch.py:375-377`), but the counts are wrong on a real ledger (MEDIUM finding above).
- **Hero first, needs-you next, charts drawn, screenshots:** not met. The order is reversed, the charts are drawn, and no screenshots are shown.

## Implicit decisions
- Day buckets are UTC, as `today_done` already was.
- A task counts once per day, by `task_done` event.
- The lanes' window is 1 to 30 minutes and grows with the session.
- The fleet card is hidden when this session is the only one, so the "steer all" input is gone in that case.
- `AskUserQuestion` gets its own face and colour.
- Subagents' own tool calls are charted in the lanes but left out of "Now".

## Not checked
- I did not run the test suite.
- I did not check the rendered visuals.
- I did not check the mobile and desktop layouts.
- I did not review `fmcli.py`, `fmhooks.py` or `test_hooks.py`, which are modified in the working tree but not in the diff.

**Noticed:** `fmwatch.py:348` loads a 5000-event tail on every `fm ui --json`, and the poll runs often. `today_done` and `done_days` could share one pass over `task_done` events instead.
