**Verdict: changes needed.** Acceptance criterion 2 ("idle it shrinks to one summary line") is not implemented, and nothing tests it. I only read the code. I did not run `claude plugin test .`.

## Findings

**MEDIUM — `mods/foreman-ui/hooks/register.tsx:925-930,957-958` — the idle summary line does not exist.**
- Idle with nothing running still falls through to `return next(e)`, at line 930 when the pane is closed and line 958 when it is docked. The test at `tests/foreman-ui.test.tsx` ("with no work for a while the docked band steps aside") asserts the band is absent.
- A docked pane that has been idle for more than 2 minutes therefore shows no band at all, where the criterion asks for a one-line summary.
- Fix: when `!treeLive`, render one line (for example `this session · T-123 step 2/5 · 0 agents`, or `liveTree` with `rows: 1`). Add a test that asserts that line.
- Confidence: high.

**MEDIUM — `register.tsx:1061` — the tree can overflow `maxRows` in the undocked band.**
- The `maxRows - 7` budget assumes the band is the border (2), the head (2), one queue row, one `next` row and one button row.
- The band also renders `doneSince`, `bgs`, `paused` (which wraps to 2+ lines), `asks` and up to 2 `plans`, with no cap.
- With, say, 2 asks and a plan, the band exceeds `maxRows` even though the tree "fits". Criterion 1 requires that it fits.
- The new tests only check the docked tree's top-level children.
- Fix: subtract the real count of optional rows, or use `liveTree`'s own row count for the budget.
- Confidence: medium (plausible).

**MEDIUM — `register.tsx:668,640` — a call that throws is shown as ✓.**
- `item.ok` is set only after `next(e)` returns. If `next` throws, `ok` stays `undefined`, and `rows.tsx:204,209` treat only `ok === false` as ✗.
- Fix: set `item.ok = false` in a `catch`, or default to `false` and set `true` on success.
- Confidence: high.

**LOW — `rows.tsx:221-226` — the comment says "cut, never dropped", but the task text is dropped in narrow widths.**
- `sectionHead` only draws the subject when `subject.length <= room - 8` (`rows.tsx:62`) and ignores `rest`.
- `liveTree` floors its cut length at `Math.max(8, …)` and has a different `sectionHead` width floor (30).
- With `facts` = `3 calls · 2 agents` (18 chars) and a docked width around 40, the task, step and current work disappear.
- Fix: drop `facts` first, or pass the already-cut `task` and compute the same `room` as `sectionHead`.
- Confidence: medium.

**LOW — `register.tsx:622`, `state.ts` — `feed` is module-global and never reset.**
- It is not cleared on `session.start`, `/clear` or compaction, so old calls show for up to 2 minutes in a new session.
- It also leaks between tests: the second test's ag1 calls merge with the first test's ag1 calls.
- Fix: `feed.length = 0` in `session.start`, and reset it in the test `world()` helper.
- Confidence: medium.

**LOW — `rows.tsx:566,247` — control characters in `x.target` and `a.description` are not stripped.**
- `toolFace` only slices the first line, and `clean()` is not applied. The existing rows (`rows.tsx:358,463`) have the same weakness, so this follows precedent.
- Fix: wrap the text in `clean()` in the new rows, or fix it once in `toolFace`.
- Confidence: low.

## Acceptance criteria
1. **Tree with connectors, fitting `maxRows`: partly met.**
   - The tree, marks, per-agent branches and connectors are in `liveTree`.
   - Fitting holds for the docked case (the test asserts ≤ 8 rows).
   - It is not guaranteed for the undocked band (finding 2).
2. **Docked shows the tree; idle shrinks to one summary line: partly met.** The tree shows when docked and live. There is no idle summary line (finding 1).
3. **The band stays put while the chat scrolls:** not verifiable from this diff. The change does not touch the band's placement.

## Implicit decisions
- The tree stays for 2 minutes after the last call (120000 ms, hardcoded in two places).
- The feed is capped at 300 items.
- Display limits are 3 session calls, 2 calls per agent and then a "more" count.
- Agents are sorted running first, then most recent.
- The "no task in focus" label is shown when no task is active.
- The `maxRows - 7` constant and the `Math.max(3, maxRows)` floor in the docked case.
- Guard-denied calls are marked ✗.
- The version is bumped to 0.15.0 in `plugin.json` and `marketplace.json`, which match.
- `kit.ts` needs no edit; `spin`, `elapsed` and `agentColor` already exist.

## Not checked
- I did not run the tests.
- I did not check the live render or the actual dock width.
- I did not check how `$.ui` `Text` handles control characters.

Noticed: the 120000 ms tree window is duplicated at `register.tsx:929` and `rows.tsx:546`; extract a constant in `state.ts`.
